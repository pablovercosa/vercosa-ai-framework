"""Governed preparation pipeline for Agent Assignment execution.

The pipeline composes already existing Policy, Context, Token Budget, Guardian,
Model Selection and Audit contracts before the Agent Orchestrator crosses the
runtime boundary. It is explicit, injectable and side-effect free except for an
optional in-memory/event-log port supplied by the caller.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from vercosa_ai_framework.agents.types import AgentProfile
from vercosa_ai_framework.audit.event_log import EventLog
from vercosa_ai_framework.audit.integrations import (
    agent_execution_event,
    model_selection_event,
    record_context_package_event,
    record_guardian_decision_event,
    record_policy_resolution_event,
)
from vercosa_ai_framework.context import ContextItem, ContextPackage, ContextRequest, ContextRouter, ContextSource, TokenBudget
from vercosa_ai_framework.guardian import GuardianAction, GuardianEngine, GuardianEvaluationContext, GuardianMode
from vercosa_ai_framework.model_selection import ModelSelectionError, ModelSelectionPolicy, ModelSelector, SelectionDecision
from vercosa_ai_framework.policy import (
    DeterministicPolicyEngine,
    PolicyEngine,
    PolicyEvaluationContext,
    PolicyResolutionResult,
    PolicyScope,
    PolicySet,
    ResolvedPolicySet,
)
from vercosa_ai_framework.tasks import Task, TaskAttempt


class ExecutionGovernanceError(ValueError):
    """Raised when governed preparation cannot safely continue."""


@dataclass(frozen=True, slots=True)
class AgentExecutionGovernanceResult:
    """Structured result of a governed Agent Assignment preparation."""

    preparation_id: str
    policy_resolution: PolicyResolutionResult
    resolved_policy_set: ResolvedPolicySet
    context_request: ContextRequest
    context_package: ContextPackage
    planning_guardian_decision: Any
    context_guardian_decision: Any
    model_selection_decision: SelectionDecision | None = None
    audit_event_refs: tuple[str, ...] = field(default_factory=tuple)
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)
    approval_requirements: tuple[str, ...] = field(default_factory=tuple)
    blocked: bool = False

    @property
    def guardian_decision_refs(self) -> tuple[str, ...]:
        """Return Guardian decision refs emitted during preparation."""

        refs = (
            self.planning_guardian_decision.evaluation_id,
            self.context_guardian_decision.evaluation_id,
        )
        return tuple(ref for ref in refs if ref)

    @property
    def selected_model_id(self) -> str | None:
        """Return the selected model id, if selection completed."""

        if self.model_selection_decision is None:
            return None
        return self.model_selection_decision.selected_model.id


class AgentExecutionGovernance:
    """Prepare an Agent Assignment through explicit governance boundaries."""

    def __init__(
        self,
        *,
        context_router: ContextRouter,
        policy_engine: PolicyEngine | None = None,
        guardian_engine: GuardianEngine | None = None,
        model_selector: ModelSelector | None = None,
        event_log: EventLog | None = None,
        policy_sets: tuple[PolicySet, ...] = (),
        default_token_budget: TokenBudget = TokenBudget(max_input_tokens=4096, reserved_output_tokens=1024),
        require_model_selection: bool = True,
        guardian_mode: GuardianMode = GuardianMode.STANDARD,
        workspace: str = ".",
        spec_refs: tuple[str, ...] = (),
    ) -> None:
        self.policy_engine = policy_engine or DeterministicPolicyEngine()
        self.context_router = context_router
        self.guardian_engine = guardian_engine or GuardianEngine()
        self.model_selector = model_selector
        self.event_log = event_log
        self.policy_sets = policy_sets
        self.default_token_budget = default_token_budget
        self.require_model_selection = require_model_selection
        self.guardian_mode = guardian_mode
        self.workspace = workspace
        self.spec_refs = spec_refs

    def prepare(
        self,
        task: Task,
        attempt: TaskAttempt,
        profile: AgentProfile,
        *,
        assignment_id: str,
    ) -> AgentExecutionGovernanceResult:
        """Run deterministic governance preparation for one agent assignment."""

        preparation_id = f"{assignment_id}:governance"
        audit_refs: list[str] = []
        warnings: list[str] = []
        errors: list[str] = []
        approvals: list[str] = []

        policy_sets = _policy_sets_from_task(task) or self.policy_sets
        policy_resolution = self.policy_engine.resolve(
            policy_sets,
            self._policy_context(task, profile, assignment_id),
        )
        resolved_policy_set = policy_resolution.resolved_policy_set
        audit_refs.append(
            record_policy_resolution_event(
                policy_resolution,
                event_log=self.event_log,
                considered_policy_count=len(policy_sets),
                metadata=_safe_flow_metadata(task, attempt, assignment_id, profile),
            ).event_id
        )

        planning_decision = self.guardian_engine.evaluate(
            GuardianEvaluationContext(
                mission_id=task.mission_id,
                evaluation_id=f"{assignment_id}:agent_assignment_planning",
                evaluation_type="agent_assignment_planning",
                guardian_mode=self.guardian_mode,
                mission_goal=task.goal,
                spec_refs=self.spec_refs,
                guardian_refs=task.guardian_decision_refs,
                workspace=self.workspace,
                requested_action=f"Prepare task {task.task_id} with agent profile {profile.agent_profile_id}",
                execution_limits=_mapping(task.metadata.get("execution_limits")),
                resolved_policy_set=resolved_policy_set,
                metadata={
                    "task_type": task.task_type,
                    "risk_level": task.risk_level,
                    "policy_resolution_id": resolved_policy_set.resolution_id,
                },
            )
        )

        context_request = self._context_request(
            task,
            attempt,
            profile,
            assignment_id,
            resolved_policy_set,
            (planning_decision.evaluation_id,),
        )
        context_candidates = context_request.candidate_items
        context_package = self.context_router.route(context_request, context_candidates)
        audit_refs.append(
            record_context_package_event(
                context_package,
                event_log=self.event_log,
                candidate_count=len(context_candidates),
                metadata=_safe_flow_metadata(task, attempt, assignment_id, profile),
            ).event_id
        )

        context_decision = self.guardian_engine.evaluate_context_package(
            context_package,
            mission_id=task.mission_id,
            guardian_mode=self.guardian_mode,
            evaluation_id=f"{assignment_id}:context_package_pre_delivery",
        )
        audit_refs.append(
            record_guardian_decision_event(
                context_decision,
                event_log=self.event_log,
                origin="context_package_pre_delivery",
                metadata={
                    **_safe_flow_metadata(task, attempt, assignment_id, profile),
                    "context_package_id": context_package.context_package_id,
                },
            ).event_id
        )

        warnings.extend(policy_resolution.warnings)
        warnings.extend(context_package.warnings)
        warnings.extend(planning_decision.warnings)
        warnings.extend(context_decision.warnings)
        approvals.extend(planning_decision.approval_requirements)
        approvals.extend(context_decision.approval_requirements)

        if planning_decision.decision in {GuardianAction.BLOCK, GuardianAction.REQUIRE_APPROVAL}:
            errors.extend(planning_decision.reasons)
            audit_refs.append(self._record_preparation_event("blocked", task, attempt, assignment_id, profile, errors).event_id)
            return self._result(
                preparation_id,
                policy_resolution,
                context_request,
                context_package,
                planning_decision,
                context_decision,
                audit_refs,
                warnings,
                errors,
                approvals,
                blocked=True,
            )

        if context_decision.decision in {GuardianAction.BLOCK, GuardianAction.REQUIRE_APPROVAL}:
            errors.extend(context_decision.reasons)
            audit_refs.append(self._record_preparation_event("blocked", task, attempt, assignment_id, profile, errors).event_id)
            return self._result(
                preparation_id,
                policy_resolution,
                context_request,
                context_package,
                planning_decision,
                context_decision,
                audit_refs,
                warnings,
                errors,
                approvals,
                blocked=True,
            )

        try:
            model_decision = self._select_model(task, profile, context_package, resolved_policy_set)
        except ExecutionGovernanceError as exc:
            errors.append(str(exc))
            audit_refs.append(self._record_preparation_event("blocked", task, attempt, assignment_id, profile, errors).event_id)
            return self._result(
                preparation_id,
                policy_resolution,
                context_request,
                context_package,
                planning_decision,
                context_decision,
                audit_refs,
                warnings,
                errors,
                approvals,
                blocked=True,
            )
        if model_decision is not None:
            audit_refs.append(
                self._record_model_selection(model_decision, task, attempt, assignment_id, profile, context_package.context_package_id).event_id
            )
            warnings.extend(model_decision.security_notes)
            warnings.extend(model_decision.token_budget_warnings)
            if model_decision.requires_user_approval:
                approvals.append("model_selection_requires_user_approval")
                errors.append("model selection requires explicit user approval")
                audit_refs.append(self._record_preparation_event("blocked", task, attempt, assignment_id, profile, errors).event_id)
                return self._result(
                    preparation_id,
                    policy_resolution,
                    context_request,
                    context_package,
                    planning_decision,
                    context_decision,
                    audit_refs,
                    warnings,
                    errors,
                    approvals,
                    model_decision=model_decision,
                    blocked=True,
                )

        return self._result(
            preparation_id,
            policy_resolution,
            context_request,
            context_package,
            planning_decision,
            context_decision,
            audit_refs,
            warnings,
            errors,
            approvals,
            model_decision=model_decision,
        )

    def record_execution_start(self, task: Task, attempt: TaskAttempt, assignment_id: str, profile: AgentProfile) -> str | None:
        """Record governed execution start when an event log is configured."""

        return self._record_preparation_event("started", task, attempt, assignment_id, profile, ()).event_id

    def record_runtime_result(self, task: Task, attempt: TaskAttempt, assignment_id: str, profile: AgentProfile, runtime_result: Any) -> str | None:
        """Record sanitized runtime result metadata."""

        metadata = {
            **_safe_flow_metadata(task, attempt, assignment_id, profile),
            "runtime_id": getattr(runtime_result, "runtime_id", None),
            "runtime_status": getattr(getattr(runtime_result, "status", None), "value", getattr(runtime_result, "status", None)),
            "artifact_count": len(getattr(runtime_result, "artifacts", ()) or ()),
            "changed_file_count": len(getattr(runtime_result, "changed_files", ()) or ()),
            "warning_count": len(getattr(runtime_result, "warnings", ()) or ()),
            "error_count": len(getattr(runtime_result, "errors", ()) or ()),
        }
        event = agent_execution_event("runtime_result", result="success", metadata=metadata)
        return self.event_log.record(event).event_id if self.event_log is not None else event.event_id

    def record_guardian_decision(self, decision: Any, *, origin: str, metadata: dict[str, Any] | None = None) -> str | None:
        """Record a Guardian decision through the same optional EventLog."""

        event = record_guardian_decision_event(decision, event_log=self.event_log, origin=origin, metadata=metadata)
        return event.event_id

    def record_final_result(self, task: Task, attempt: TaskAttempt, assignment_id: str, profile: AgentProfile, result: Any) -> str | None:
        """Record sanitized final Agent Assignment result metadata."""

        metadata = {
            **_safe_flow_metadata(task, attempt, assignment_id, profile),
            "success": bool(getattr(result, "success", False)),
            "state": getattr(getattr(result, "state", None), "value", getattr(result, "state", None)),
            "warning_count": len(getattr(result, "warnings", ()) or ()),
            "error_count": len(getattr(result, "errors", ()) or ()),
        }
        event = agent_execution_event("final_result", result="success" if metadata["success"] else "failed", metadata=metadata)
        return self.event_log.record(event).event_id if self.event_log is not None else event.event_id

    def _policy_context(self, task: Task, profile: AgentProfile, assignment_id: str) -> PolicyEvaluationContext:
        return PolicyEvaluationContext(
            mission_id=task.mission_id,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            agent_id=profile.agent_profile_id,
            target_scope=PolicyScope.TASK,
            requested_scopes=(PolicyScope.GLOBAL, PolicyScope.MISSION, PolicyScope.WORKFLOW, PolicyScope.TASK, PolicyScope.AGENT, PolicyScope.CONTEXT, PolicyScope.MODEL),
            metadata={
                "agent_assignment_id": assignment_id,
                "agent_role": profile.role.value,
                "task_type": task.task_type,
                "risk_level": task.risk_level,
            },
        )

    def _context_request(
        self,
        task: Task,
        attempt: TaskAttempt,
        profile: AgentProfile,
        assignment_id: str,
        resolved_policy_set: ResolvedPolicySet,
        guardian_decision_refs: tuple[str, ...],
    ) -> ContextRequest:
        metadata = _mapping(task.metadata.get("context_request"))
        return ContextRequest(
            request_id=str(metadata.get("request_id") or f"{assignment_id}:context"),
            request_goal=str(metadata.get("request_goal") or task.goal),
            mission_id=task.mission_id,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            attempt_id=attempt.attempt_id,
            agent_assignment_id=assignment_id,
            task_type=task.task_type,
            agent_role=profile.role.value,
            required_sources=_tuple_str(metadata.get("required_sources")),
            optional_sources=_tuple_str(metadata.get("optional_sources")),
            scope=str(metadata.get("scope") or task.task_type),
            token_budget=_token_budget(task, profile, self.default_token_budget),
            citation_required=bool(metadata.get("citation_required", task.metadata.get("citation_required", False))),
            policy_refs=resolved_policy_set.matched_policy_refs,
            resolved_policy_set=resolved_policy_set,
            guardian_decision_refs=guardian_decision_refs,
            prior_context_package_refs=task.context_refs,
            candidate_sources=_context_sources(task),
            candidate_items=_context_items(task),
            metadata={
                "mission_id": task.mission_id,
                "workflow_id": task.workflow_id,
                "task_id": task.task_id,
                "agent_assignment_id": assignment_id,
                "policy_resolution_id": resolved_policy_set.resolution_id,
            },
        )

    def _select_model(
        self,
        task: Task,
        profile: AgentProfile,
        context_package: ContextPackage,
        resolved_policy_set: ResolvedPolicySet,
    ) -> SelectionDecision | None:
        if self.model_selector is None:
            if self.require_model_selection:
                raise ExecutionGovernanceError("model selector is required for governed execution")
            return None

        policy_values = dict(profile.default_model_policy)
        policy_values.update(_mapping(task.metadata.get("model_policy")))
        policy_values.setdefault("task_role", profile.role.value)
        policy_values.setdefault("complexity", str(task.metadata.get("complexity") or "medium"))
        policy_values.setdefault("context_size", int(context_package.model_requirements.get("minimum_context_window", 0) or 0))
        policy = ModelSelectionPolicy.from_mapping(policy_values)
        try:
            return self.model_selector.select(
                policy,
                resolved_policy_set=resolved_policy_set,
                token_budget_requirements=context_package.model_requirements,
            )
        except (ModelSelectionError, ValueError) as exc:
            raise ExecutionGovernanceError(f"model selection failed: {exc}") from exc

    def _record_model_selection(
        self,
        decision: SelectionDecision,
        task: Task,
        attempt: TaskAttempt,
        assignment_id: str,
        profile: AgentProfile,
        context_package_id: str,
    ):
        event = model_selection_event(
            decision,
            metadata={
                **_safe_flow_metadata(task, attempt, assignment_id, profile),
                "context_package_id": context_package_id,
            },
        )
        return self.event_log.record(event) if self.event_log is not None else event

    def _record_preparation_event(self, status: str, task: Task, attempt: TaskAttempt, assignment_id: str, profile: AgentProfile, errors: Any):
        event = agent_execution_event(
            f"governance_{status}",
            result="blocked" if status == "blocked" else "success",
            metadata={
                **_safe_flow_metadata(task, attempt, assignment_id, profile),
                "error_count": len(tuple(errors or ())),
            },
        )
        return self.event_log.record(event) if self.event_log is not None else event

    def _result(
        self,
        preparation_id: str,
        policy_resolution: PolicyResolutionResult,
        context_request: ContextRequest,
        context_package: ContextPackage,
        planning_decision: Any,
        context_decision: Any,
        audit_refs: list[str],
        warnings: list[str],
        errors: list[str],
        approvals: list[str],
        *,
        model_decision: SelectionDecision | None = None,
        blocked: bool = False,
    ) -> AgentExecutionGovernanceResult:
        return AgentExecutionGovernanceResult(
            preparation_id=preparation_id,
            policy_resolution=policy_resolution,
            resolved_policy_set=policy_resolution.resolved_policy_set,
            context_request=context_request,
            context_package=context_package,
            planning_guardian_decision=planning_decision,
            context_guardian_decision=context_decision,
            model_selection_decision=model_decision,
            audit_event_refs=tuple(audit_refs),
            warnings=tuple(dict.fromkeys(warnings)),
            errors=tuple(dict.fromkeys(errors)),
            approval_requirements=tuple(dict.fromkeys(approvals)),
            blocked=blocked,
        )


def _policy_sets_from_task(task: Task) -> tuple[PolicySet, ...]:
    value = _metadata_or_input(task, "policy_sets")
    if isinstance(value, tuple) and all(isinstance(item, PolicySet) for item in value):
        return value
    if isinstance(value, list) and all(isinstance(item, PolicySet) for item in value):
        return tuple(value)
    return ()


def _context_items(task: Task) -> tuple[ContextItem, ...]:
    value = _metadata_or_input(task, "context_items")
    if isinstance(value, tuple) and all(isinstance(item, ContextItem) for item in value):
        return value
    if isinstance(value, list) and all(isinstance(item, ContextItem) for item in value):
        return tuple(value)
    return ()


def _context_sources(task: Task) -> tuple[ContextSource, ...]:
    value = _metadata_or_input(task, "context_sources")
    if isinstance(value, tuple) and all(isinstance(item, ContextSource) for item in value):
        return value
    if isinstance(value, list) and all(isinstance(item, ContextSource) for item in value):
        return tuple(value)
    return ()


def _token_budget(task: Task, profile: AgentProfile, default: TokenBudget) -> TokenBudget:
    values: dict[str, Any] = {}
    values.update(_mapping(_metadata_or_input(task, "token_budget")))
    limits = dict(profile.default_execution_limits)
    limits.update(_mapping(task.metadata.get("execution_limits")))
    for source_key, target_key in (
        ("max_input_tokens", "max_input_tokens"),
        ("reserved_output_tokens", "reserved_output_tokens"),
        ("max_output_tokens", "max_output_tokens"),
        ("instruction_tokens", "instruction_tokens"),
        ("safety_margin_tokens", "safety_margin_tokens"),
    ):
        if source_key in limits and target_key not in values:
            values[target_key] = limits[source_key]

    return TokenBudget(
        max_input_tokens=int(values.get("max_input_tokens", default.max_input_tokens)),
        reserved_output_tokens=int(values.get("reserved_output_tokens", default.reserved_output_tokens)),
        max_output_tokens=_optional_int(values.get("max_output_tokens", default.max_output_tokens)),
        instruction_tokens=int(values.get("instruction_tokens", default.instruction_tokens)),
        safety_margin_tokens=int(values.get("safety_margin_tokens", default.safety_margin_tokens)),
    )


def _safe_flow_metadata(task: Task, attempt: TaskAttempt, assignment_id: str, profile: AgentProfile) -> dict[str, Any]:
    return {
        "mission_id": task.mission_id,
        "workflow_id": task.workflow_id,
        "task_id": task.task_id,
        "attempt_id": attempt.attempt_id,
        "agent_assignment_id": assignment_id,
        "agent_profile_id": profile.agent_profile_id,
        "task_type": task.task_type,
        "risk_level": task.risk_level,
    }


def _metadata_or_input(task: Task, key: str) -> Any:
    if key in task.metadata:
        return task.metadata.get(key)
    return _mapping(task.metadata.get("inputs")).get(key)


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    return int(value)


def _tuple_str(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple | list):
        return tuple(str(item) for item in value)
    return (str(value),)


def _mapping(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


__all__ = [
    "AgentExecutionGovernance",
    "AgentExecutionGovernanceResult",
    "ExecutionGovernanceError",
]

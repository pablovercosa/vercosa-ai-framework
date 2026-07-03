"""Agent Orchestrator MVP.

This module coordinates provider-neutral agent execution. It selects an agent
profile, asks Guardian and Model Selection engines when configured, builds a
normalized AgentExecutionRequest, and delegates concrete execution to a
RuntimeAdapter. It never calls OpenCode, MCPs, providers, APIs, databases, or
subprocesses directly.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from vercosa_ai_framework.agents.registry import AgentRegistry, AgentRegistryError
from vercosa_ai_framework.agents.types import (
    AgentExecutionRequest,
    AgentExecutionResult,
    AgentProfile,
    AgentRole,
    AgentState,
)
from vercosa_ai_framework.guardian import GuardianAction, GuardianEngine, GuardianEvaluationContext, GuardianMode
from vercosa_ai_framework.model_selection import ModelProfile, ModelSelectionError, ModelSelectionPolicy, ModelSelector, SelectionDecision
from vercosa_ai_framework.runtime import RuntimeAdapter, RuntimeExecutionRequest, RuntimeExecutionResult, RuntimeStatus
from vercosa_ai_framework.tasks import Task, TaskAttempt


SPEC_REF = "specs/framework/0008-agent-orchestrator.md"
DEFAULT_EXECUTION_LIMITS = {
    "max_cycles": 3,
    "max_replans": 0,
    "max_subagents": 0,
    "max_parallel_agents": 1,
}


class AgentOrchestratorError(ValueError):
    """Raised when the Agent Orchestrator cannot safely start execution."""


class NoCompatibleAgentError(AgentOrchestratorError):
    """Raised when no registered agent profile is compatible with the task."""


class AgentOrchestrator:
    """Sequential Agent Orchestrator MVP from Spec 0008."""

    def __init__(
        self,
        *,
        registry: AgentRegistry,
        runtime_adapter: RuntimeAdapter,
        guardian_engine: GuardianEngine | None = None,
        model_selector: ModelSelector | None = None,
        model_catalog: tuple[ModelProfile, ...] = (),
        workspace: str = ".",
        spec_refs: tuple[str, ...] = (SPEC_REF,),
        guardian_mode: GuardianMode = GuardianMode.STANDARD,
    ) -> None:
        self.registry = registry
        self.runtime_adapter = runtime_adapter
        self.guardian_engine = guardian_engine or GuardianEngine()
        self.model_selector = model_selector or (ModelSelector(model_catalog) if model_catalog else None)
        self.workspace = workspace
        self.spec_refs = spec_refs
        self.guardian_mode = guardian_mode

    def execute_task(self, task: Task, attempt: TaskAttempt | None = None) -> AgentExecutionResult:
        """Execute one task through a selected agent and runtime adapter."""

        attempt_id = attempt.attempt_id if attempt is not None else str(uuid4())
        assignment_id = str(uuid4())
        transitions: list[str] = []
        guardian_decision_refs: list[str] = list(task.guardian_decision_refs)

        profile = self.select_agent(task)
        transitions.append(self._transition(AgentState.IDLE, AgentState.PLANNING))

        planning_decision = self._evaluate_guardian(task, assignment_id, "agent_assignment_planning")
        guardian_decision_refs.append(planning_decision.evaluation_id)
        if planning_decision.decision in {GuardianAction.BLOCK, GuardianAction.REQUIRE_APPROVAL}:
            transitions.append(self._transition(AgentState.PLANNING, AgentState.FAILED))
            return self._failed_result(
                task,
                attempt_id,
                assignment_id,
                profile,
                tuple(planning_decision.reasons or ("guardian blocked agent assignment",)),
                transitions,
                guardian_decision_refs,
            )

        model_decision = self._select_model_if_configured(task, profile, assignment_id)
        request = self.build_execution_request(
            task,
            attempt_id=attempt_id,
            assignment_id=assignment_id,
            profile=profile,
            model_decision=model_decision,
            guardian_decision_refs=tuple(guardian_decision_refs),
        )

        transitions.append(self._transition(AgentState.PLANNING, AgentState.EXECUTING))
        runtime_result = self.runtime_adapter.execute_task(self._runtime_request(task, request, model_decision))
        transitions.append(self._transition(AgentState.EXECUTING, AgentState.VALIDATING))

        validation_decision = self._evaluate_guardian(
            task,
            assignment_id,
            "agent_assignment_validation",
            runtime_result=runtime_result,
        )
        guardian_decision_refs.append(validation_decision.evaluation_id)

        runtime_success = runtime_result.status == RuntimeStatus.DONE
        guardian_success = validation_decision.decision in {GuardianAction.ALLOW, GuardianAction.WARN}
        final_state = AgentState.DONE if runtime_success and guardian_success else AgentState.FAILED
        transitions.append(self._transition(AgentState.VALIDATING, final_state))

        return self._result_from_runtime(
            task,
            attempt_id,
            request,
            runtime_result,
            final_state,
            tuple(guardian_decision_refs),
            transitions,
            validation_errors=() if guardian_success else tuple(validation_decision.reasons),
        )

    def select_agent(self, task: Task) -> AgentProfile:
        """Select a compatible profile deterministically or fail safely."""

        metadata = task.metadata
        role = _optional_role(metadata.get("role") or _mapping(metadata.get("model_policy")).get("role"))
        domain = _optional_str(metadata.get("domain"))
        tags = _tuple_str(metadata.get("tags"))
        complexity = _optional_str(metadata.get("complexity"))

        try:
            return self.registry.select_one(
                role=role,
                domain=domain,
                tags=tags,
                required_capabilities=task.required_capabilities,
                task_type=task.task_type,
                complexity=complexity,
                risk_level=task.risk_level,
            )
        except AgentRegistryError as exc:
            msg = f"no compatible agent profile found for task {task.task_id}"
            raise NoCompatibleAgentError(msg) from exc

    def build_execution_request(
        self,
        task: Task,
        *,
        attempt_id: str,
        assignment_id: str,
        profile: AgentProfile,
        model_decision: SelectionDecision | None = None,
        guardian_decision_refs: tuple[str, ...] = (),
    ) -> AgentExecutionRequest:
        """Build the normalized agent request sent across the runtime boundary."""

        limits = dict(DEFAULT_EXECUTION_LIMITS)
        limits.update(profile.default_execution_limits)
        limits.update(_mapping(task.metadata.get("execution_limits")))

        return AgentExecutionRequest(
            mission_id=task.mission_id,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            attempt_id=attempt_id,
            agent_assignment_id=assignment_id,
            agent_profile=profile,
            required_capabilities=task.required_capabilities,
            task_type=task.task_type,
            state=AgentState.PLANNING,
            model_selection_decision_ref=model_decision.selected_model.id if model_decision else None,
            guardian_decision_refs=guardian_decision_refs,
            context_refs=task.context_refs,
            expected_outputs=_tuple_str(task.metadata.get("expected_outputs")),
            acceptance_criteria=_tuple_str(task.metadata.get("acceptance_criteria")),
            execution_limits=limits,
            logging_policy=_mapping(task.metadata.get("logging_policy")),
            security_policy=_mapping(task.metadata.get("security_policy")),
            approval_policy=_mapping(task.metadata.get("approval_policy")),
            allowed_paths=_tuple_str(task.metadata.get("allowed_paths")),
            denied_paths=_tuple_str(task.metadata.get("denied_paths")),
            metadata={"task_title": task.title, "task_goal": task.goal},
        )

    def _select_model_if_configured(
        self,
        task: Task,
        profile: AgentProfile,
        assignment_id: str,
    ) -> SelectionDecision | None:
        if self.model_selector is None:
            return None

        policy_values = dict(profile.default_model_policy)
        policy_values.update(_mapping(task.metadata.get("model_policy")))
        if not policy_values:
            return None

        policy_values.setdefault("task_role", profile.role.value)
        policy_values.setdefault("complexity", _optional_str(task.metadata.get("complexity")) or "medium")
        policy_values.setdefault("context_size", int(task.metadata.get("context_size", 0) or 0))
        try:
            return self.model_selector.select(ModelSelectionPolicy.from_mapping(policy_values))
        except (ModelSelectionError, ValueError) as exc:
            msg = f"model selection failed for agent assignment {assignment_id}: {exc}"
            raise AgentOrchestratorError(msg) from exc

    def _evaluate_guardian(
        self,
        task: Task,
        assignment_id: str,
        evaluation_type: str,
        *,
        runtime_result: RuntimeExecutionResult | None = None,
    ):
        target_paths = _tuple_str(task.metadata.get("allowed_paths")) + _tuple_str(task.metadata.get("denied_paths"))
        if runtime_result is not None:
            target_paths = target_paths + runtime_result.artifacts + runtime_result.changed_files

        return self.guardian_engine.evaluate(
            GuardianEvaluationContext(
                mission_id=task.mission_id,
                evaluation_id=f"{assignment_id}:{evaluation_type}",
                evaluation_type=evaluation_type,
                guardian_mode=self.guardian_mode,
                mission_goal=task.goal,
                spec_refs=self.spec_refs,
                guardian_refs=task.guardian_decision_refs,
                workspace=self.workspace,
                requested_action=f"Execute task {task.task_id} with agent assignment {assignment_id}",
                target_paths=target_paths,
                execution_limits=_mapping(task.metadata.get("execution_limits")),
                current_cycle=0,
                metadata={
                    "deliverables": task.metadata.get("expected_outputs", ("agent execution result",)),
                    "acceptance_criteria": task.metadata.get("acceptance_criteria", ("runtime result validated",)),
                    "task_type": task.task_type,
                    "risk_level": task.risk_level,
                },
            )
        )

    def _runtime_request(
        self,
        task: Task,
        request: AgentExecutionRequest,
        model_decision: SelectionDecision | None,
    ) -> RuntimeExecutionRequest:
        return RuntimeExecutionRequest(
            mission_id=task.mission_id,
            workspace=self.workspace,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            context={
                "prompt": task.goal,
                "agent_execution_request": request,
                "agent_profile_id": request.agent_profile.agent_profile_id,
                "agent_role": request.agent_profile.role.value,
                "context_refs": request.context_refs,
                "acceptance_criteria": request.acceptance_criteria,
            },
            permissions={"mcp_direct_access": False, "providers_direct_access": False},
            execution_limits=request.execution_limits,
            selection_decision=model_decision,
            logging_policy=request.logging_policy,
            approval_policy=request.approval_policy,
            plugin_policy={"allowed_plugins": ()},
            fallback_policy={"model_fallback": bool(model_decision and model_decision.fallback_chain)},
        )

    def _result_from_runtime(
        self,
        task: Task,
        attempt_id: str,
        request: AgentExecutionRequest,
        runtime_result: RuntimeExecutionResult,
        final_state: AgentState,
        guardian_decision_refs: tuple[str, ...],
        transitions: list[str],
        *,
        validation_errors: tuple[str, ...] = (),
    ) -> AgentExecutionResult:
        errors = runtime_result.errors + validation_errors
        warnings = runtime_result.warnings
        if runtime_result.requires_review:
            warnings = warnings + ("runtime result requires review",)
        return AgentExecutionResult(
            mission_id=task.mission_id,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            attempt_id=attempt_id,
            agent_assignment_id=request.agent_assignment_id,
            agent_profile_id=request.agent_profile.agent_profile_id,
            state=final_state,
            success=final_state == AgentState.DONE,
            artifact_refs=runtime_result.artifacts + runtime_result.changed_files,
            evidence_refs=(runtime_result.audit_log_ref,) if runtime_result.audit_log_ref else (),
            validation_results=runtime_result.validation_results,
            warnings=warnings,
            errors=errors,
            runtime_result_ref=runtime_result.audit_log_ref,
            audit_log_ref=runtime_result.audit_log_ref,
            cycle_count=len(transitions),
            metadata={
                "state_transitions": tuple(transitions),
                "guardian_decision_refs": guardian_decision_refs,
                "selected_model": request.model_selection_decision_ref,
                "runtime_id": runtime_result.runtime_id,
            },
        )

    def _failed_result(
        self,
        task: Task,
        attempt_id: str,
        assignment_id: str,
        profile: AgentProfile,
        errors: tuple[str, ...],
        transitions: list[str],
        guardian_decision_refs: list[str],
    ) -> AgentExecutionResult:
        return AgentExecutionResult(
            mission_id=task.mission_id,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            attempt_id=attempt_id,
            agent_assignment_id=assignment_id,
            agent_profile_id=profile.agent_profile_id,
            state=AgentState.FAILED,
            success=False,
            errors=errors,
            cycle_count=len(transitions),
            metadata={
                "state_transitions": tuple(transitions),
                "guardian_decision_refs": tuple(guardian_decision_refs),
            },
        )

    def _transition(self, previous: AgentState, new: AgentState) -> str:
        return f"{previous.value}->{new.value}"


def _optional_role(value: object) -> AgentRole | None:
    if value is None:
        return None
    return AgentRole(str(value))


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text or None


def _tuple_str(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, tuple):
        return tuple(str(item) for item in value)
    if isinstance(value, list):
        return tuple(str(item) for item in value)
    return (str(value),)


def _mapping(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


__all__ = ["AgentOrchestrator", "AgentOrchestratorError", "NoCompatibleAgentError"]

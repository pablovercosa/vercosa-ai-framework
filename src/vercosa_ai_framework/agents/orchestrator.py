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
from vercosa_ai_framework.agents.governance import AgentExecutionGovernance, AgentExecutionGovernanceResult, ExecutionGovernanceError
from vercosa_ai_framework.agents.types import (
    AgentExecutionRequest,
    AgentExecutionResult,
    AgentProfile,
    AgentRole,
    AgentState,
)
from vercosa_ai_framework.capabilities import (
    CapabilityExecutionResult,
    CapabilityExecutor,
    CapabilityRequest,
    CapabilityResolutionError,
    CapabilityResolutionResult,
    CapabilityResolver,
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


class CapabilityExecutionFailed(CapabilityResolutionError):
    """Raised when a resolved capability execution fails."""

    def __init__(self, message: str, executions: tuple[CapabilityExecutionResult, ...]) -> None:
        super().__init__(message)
        self.executions = executions


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
        capability_resolver: CapabilityResolver | None = None,
        require_capability_resolution: bool = False,
        capability_executor: CapabilityExecutor | None = None,
        require_capability_execution: bool = False,
        workspace: str = ".",
        spec_refs: tuple[str, ...] = (SPEC_REF,),
        guardian_mode: GuardianMode = GuardianMode.STANDARD,
        execution_governance: AgentExecutionGovernance | None = None,
        require_execution_governance: bool = False,
    ) -> None:
        self.registry = registry
        self.runtime_adapter = runtime_adapter
        self.guardian_engine = guardian_engine or GuardianEngine()
        self.model_selector = model_selector or (ModelSelector(model_catalog) if model_catalog else None)
        self.capability_resolver = capability_resolver
        self.require_capability_resolution = require_capability_resolution
        self.capability_executor = capability_executor
        self.require_capability_execution = require_capability_execution
        self.workspace = workspace
        self.spec_refs = spec_refs
        self.guardian_mode = guardian_mode
        self.execution_governance = execution_governance
        self.require_execution_governance = require_execution_governance

    def execute_task(self, task: Task, attempt: TaskAttempt | None = None) -> AgentExecutionResult:
        """Execute one task through a selected agent and runtime adapter."""

        attempt_id = attempt.attempt_id if attempt is not None else str(uuid4())
        assignment_id = str(uuid4())
        transitions: list[str] = []
        guardian_decision_refs: list[str] = list(task.guardian_decision_refs)

        profile = self.select_agent(task)
        transitions.append(self._transition(AgentState.IDLE, AgentState.PLANNING))

        governance_result: AgentExecutionGovernanceResult | None = None
        if self.execution_governance is not None:
            try:
                governance_result = self.execution_governance.prepare(task, _attempt(task, attempt, attempt_id), profile, assignment_id=assignment_id)
            except ExecutionGovernanceError as exc:
                transitions.append(self._transition(AgentState.PLANNING, AgentState.FAILED))
                return self._failed_result(
                    task,
                    attempt_id,
                    assignment_id,
                    profile,
                    (str(exc),),
                    transitions,
                    guardian_decision_refs,
                )
            guardian_decision_refs.extend(governance_result.guardian_decision_refs)
            if governance_result.blocked:
                transitions.append(self._transition(AgentState.PLANNING, AgentState.FAILED))
                return self._failed_result(
                    task,
                    attempt_id,
                    assignment_id,
                    profile,
                    governance_result.errors or ("governed preparation blocked execution",),
                    transitions,
                    guardian_decision_refs,
                    governance_result=governance_result,
                )
        elif self.require_execution_governance:
            transitions.append(self._transition(AgentState.PLANNING, AgentState.FAILED))
            return self._failed_result(
                task,
                attempt_id,
                assignment_id,
                profile,
                ("execution governance is required but was not configured",),
                transitions,
                guardian_decision_refs,
            )

        if governance_result is None:
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

        model_decision = governance_result.model_selection_decision if governance_result else self._select_model_if_configured(task, profile, assignment_id)
        try:
            capability_results = self._resolve_required_capabilities(
                task,
                attempt_id=attempt_id,
                assignment_id=assignment_id,
                profile=profile,
                guardian_decision_refs=tuple(guardian_decision_refs),
                governance_result=governance_result,
            )
            capability_executions = self._execute_required_capabilities(capability_results)
        except CapabilityExecutionFailed as exc:
            transitions.append(self._transition(AgentState.PLANNING, AgentState.FAILED))
            return self._failed_result(
                task,
                attempt_id,
                assignment_id,
                profile,
                (str(exc),),
                transitions,
                guardian_decision_refs,
                capability_resolutions=capability_results,
                capability_executions=exc.executions,
                governance_result=governance_result,
            )
        except CapabilityResolutionError as exc:
            transitions.append(self._transition(AgentState.PLANNING, AgentState.FAILED))
            return self._failed_result(
                task,
                attempt_id,
                assignment_id,
                profile,
                (str(exc),),
                transitions,
                guardian_decision_refs,
                capability_resolutions=(),
                capability_executions=(),
                governance_result=governance_result,
            )
        request = self.build_execution_request(
            task,
            attempt_id=attempt_id,
            assignment_id=assignment_id,
            profile=profile,
            model_decision=model_decision,
            guardian_decision_refs=tuple(guardian_decision_refs),
            capability_resolutions=capability_results,
            capability_executions=capability_executions,
            governance_result=governance_result,
        )

        transitions.append(self._transition(AgentState.PLANNING, AgentState.EXECUTING))
        if governance_result is not None and self.execution_governance is not None:
            self.execution_governance.record_execution_start(task, _attempt(task, attempt, attempt_id), assignment_id, profile)
        runtime_result = self.runtime_adapter.execute_task(self._runtime_request(task, request, model_decision))
        if governance_result is not None and self.execution_governance is not None:
            self.execution_governance.record_runtime_result(task, _attempt(task, attempt, attempt_id), assignment_id, profile, runtime_result)
        transitions.append(self._transition(AgentState.EXECUTING, AgentState.VALIDATING))

        validation_decision = self._evaluate_guardian(
            task,
            assignment_id,
            "agent_assignment_validation",
            runtime_result=runtime_result,
            governance_result=governance_result,
        )
        guardian_decision_refs.append(validation_decision.evaluation_id)
        if governance_result is not None and self.execution_governance is not None:
            self.execution_governance.record_guardian_decision(
                validation_decision,
                origin="agent_assignment_validation",
                metadata={
                    "mission_id": task.mission_id,
                    "workflow_id": task.workflow_id,
                    "task_id": task.task_id,
                    "agent_assignment_id": assignment_id,
                    "policy_resolution_id": governance_result.resolved_policy_set.resolution_id,
                    "context_package_id": governance_result.context_package.context_package_id,
                    "selected_model_id": governance_result.selected_model_id,
                },
            )

        runtime_success = runtime_result.status == RuntimeStatus.DONE
        guardian_success = validation_decision.decision in {GuardianAction.ALLOW, GuardianAction.WARN}
        final_state = AgentState.DONE if runtime_success and guardian_success else AgentState.FAILED
        transitions.append(self._transition(AgentState.VALIDATING, final_state))

        result = self._result_from_runtime(
            task,
            attempt_id,
            request,
            runtime_result,
            final_state,
            tuple(guardian_decision_refs),
            transitions,
            validation_errors=() if guardian_success else tuple(validation_decision.reasons),
            governance_result=governance_result,
        )
        if governance_result is not None and self.execution_governance is not None:
            self.execution_governance.record_final_result(task, _attempt(task, attempt, attempt_id), assignment_id, profile, result)
        return result

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
        capability_resolutions: tuple[CapabilityResolutionResult, ...] = (),
        capability_executions: tuple[CapabilityExecutionResult, ...] = (),
        governance_result: AgentExecutionGovernanceResult | None = None,
    ) -> AgentExecutionRequest:
        """Build the normalized agent request sent across the runtime boundary."""

        limits = dict(DEFAULT_EXECUTION_LIMITS)
        limits.update(profile.default_execution_limits)
        limits.update(_mapping(task.metadata.get("execution_limits")))

        governance_metadata = _governance_metadata(governance_result)
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
            context_refs=_context_refs(task, governance_result),
            expected_outputs=_tuple_str(task.metadata.get("expected_outputs")),
            acceptance_criteria=_tuple_str(task.metadata.get("acceptance_criteria")),
            execution_limits=limits,
            logging_policy=_mapping(task.metadata.get("logging_policy")),
            security_policy=_mapping(task.metadata.get("security_policy")),
            approval_policy=_mapping(task.metadata.get("approval_policy")),
            allowed_paths=_tuple_str(task.metadata.get("allowed_paths")),
            denied_paths=_tuple_str(task.metadata.get("denied_paths")),
            metadata={
                "task_title": task.title,
                "task_goal": task.goal,
                "capability_resolutions": tuple(
                    _capability_resolution_metadata(result) for result in capability_resolutions
                ),
                "capability_executions": tuple(
                    _capability_execution_metadata(result) for result in capability_executions
                ),
                **governance_metadata,
            },
        )

    def _resolve_required_capabilities(
        self,
        task: Task,
        *,
        attempt_id: str,
        assignment_id: str,
        profile: AgentProfile,
        guardian_decision_refs: tuple[str, ...],
        governance_result: AgentExecutionGovernanceResult | None = None,
    ) -> tuple[CapabilityResolutionResult, ...]:
        if not task.required_capabilities:
            return ()
        if self.capability_resolver is None:
            if self.require_capability_resolution:
                raise CapabilityResolutionError("capability resolver is required for tasks with required_capabilities")
            return ()

        results: list[CapabilityResolutionResult] = []
        seen: set[str] = set()
        for capability in task.required_capabilities:
            if capability in seen:
                raise CapabilityResolutionError(f"duplicated required capability in assignment: {capability}")
            seen.add(capability)
            request = self._capability_request(
                task,
                attempt_id=attempt_id,
                assignment_id=assignment_id,
                profile=profile,
                capability=capability,
                guardian_decision_refs=guardian_decision_refs,
                governance_result=governance_result,
            )
            results.append(self.capability_resolver.resolve(request))
        return tuple(results)

    def _execute_required_capabilities(
        self,
        resolutions: tuple[CapabilityResolutionResult, ...],
    ) -> tuple[CapabilityExecutionResult, ...]:
        if not resolutions:
            return ()
        if self.capability_executor is None:
            if self.require_capability_execution:
                raise CapabilityResolutionError("capability executor is required for required_capabilities execution")
            return ()

        executions: list[CapabilityExecutionResult] = []
        for resolution in resolutions:
            result = self.capability_executor.execute(resolution)
            executions.append(result)
            if not result.success:
                details = "; ".join(result.errors) if result.errors else "capability execution failed"
                raise CapabilityExecutionFailed(
                    f"capability execution failed for {resolution.capability.name}: {details}",
                    tuple(executions),
                )
        if len(executions) != len(resolutions):
            raise CapabilityExecutionFailed("partial capability execution is not allowed", tuple(executions))
        return tuple(executions)

    def _capability_request(
        self,
        task: Task,
        *,
        attempt_id: str,
        assignment_id: str,
        profile: AgentProfile,
        capability: str,
        guardian_decision_refs: tuple[str, ...],
        governance_result: AgentExecutionGovernanceResult | None = None,
    ) -> CapabilityRequest:
        capability_inputs = _mapping(task.metadata.get("capability_inputs"))
        nested_inputs = _mapping(task.metadata.get("inputs")).get("capability_inputs")
        if not capability_inputs:
            capability_inputs = _mapping(nested_inputs)
        limits = dict(profile.default_execution_limits)
        limits.update(_mapping(task.metadata.get("execution_limits")))
        return CapabilityRequest(
            capability=capability,
            mission_id=task.mission_id,
            workflow_id=task.workflow_id,
            task_id=task.task_id,
            agent_assignment_id=assignment_id,
            inputs=_mapping(capability_inputs.get(capability)),
            context_refs=task.context_refs,
            granted_permissions=_granted_permissions(task),
            risk_level=task.risk_level,
            limits=limits,
            guardian_decision_refs=guardian_decision_refs,
            metadata={
                "attempt_id": attempt_id,
                "agent_profile_id": profile.agent_profile_id,
                "task_type": task.task_type,
                "declarative_resolution_only": True,
                "allowed_tools": _allowed_tools(task, capability),
                "allowed_effects": _allowed_effects(task, capability),
                "policy_resolution_id": governance_result.resolved_policy_set.resolution_id if governance_result else None,
                "matched_policy_refs": governance_result.resolved_policy_set.matched_policy_refs if governance_result else (),
                "context_package_id": governance_result.context_package.context_package_id if governance_result else None,
                "model_selection_decision_ref": governance_result.selected_model_id if governance_result else None,
            },
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
        governance_result: AgentExecutionGovernanceResult | None = None,
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
                resolved_policy_set=governance_result.resolved_policy_set if governance_result else None,
                metadata={
                    "deliverables": task.metadata.get("expected_outputs", ("agent execution result",)),
                    "acceptance_criteria": task.metadata.get("acceptance_criteria", ("runtime result validated",)),
                    "task_type": task.task_type,
                    "risk_level": task.risk_level,
                    "policy_resolution_id": governance_result.resolved_policy_set.resolution_id if governance_result else None,
                    "context_package_id": governance_result.context_package.context_package_id if governance_result else None,
                    "selected_model_id": governance_result.selected_model_id if governance_result else None,
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
                "capability_resolutions": request.metadata.get("capability_resolutions", ()),
                "capability_executions": request.metadata.get("capability_executions", ()),
                "context_package": request.metadata.get("context_package"),
                "policy_resolution_id": request.metadata.get("policy_resolution_id"),
                "context_package_id": request.metadata.get("context_package_id"),
                "model_selection_decision_ref": request.metadata.get("model_selection_decision_ref"),
                "guardian_decision_refs": request.guardian_decision_refs,
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
        governance_result: AgentExecutionGovernanceResult | None = None,
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
                "capability_resolutions": request.metadata.get("capability_resolutions", ()),
                "capability_executions": request.metadata.get("capability_executions", ()),
                **_governance_result_metadata(governance_result),
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
        *,
        capability_resolutions: tuple[CapabilityResolutionResult, ...] = (),
        capability_executions: tuple[CapabilityExecutionResult, ...] = (),
        governance_result: AgentExecutionGovernanceResult | None = None,
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
                "capability_resolutions": tuple(
                    _capability_resolution_metadata(result) for result in capability_resolutions
                ),
                "capability_executions": tuple(
                    _capability_execution_metadata(result) for result in capability_executions
                ),
                **_governance_result_metadata(governance_result),
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


def _granted_permissions(task: Task) -> tuple[str, ...]:
    direct = _tuple_str(task.metadata.get("granted_permissions"))
    if direct:
        return direct
    return _tuple_str(_mapping(task.metadata.get("inputs")).get("granted_permissions"))


def _allowed_tools(task: Task, capability: str) -> tuple[str, ...]:
    direct = task.metadata.get("allowed_tools")
    if isinstance(direct, dict):
        return _tuple_str(direct.get(capability))
    values = _tuple_str(direct)
    if values:
        return values
    nested = _mapping(task.metadata.get("inputs")).get("allowed_tools")
    if isinstance(nested, dict):
        return _tuple_str(nested.get(capability))
    return _tuple_str(nested)


def _allowed_effects(task: Task, capability: str) -> tuple[str, ...]:
    direct = task.metadata.get("allowed_effects")
    if isinstance(direct, dict):
        return _tuple_str(direct.get(capability))
    values = _tuple_str(direct)
    if values:
        return values
    nested = _mapping(task.metadata.get("inputs")).get("allowed_effects")
    if isinstance(nested, dict):
        return _tuple_str(nested.get(capability))
    return _tuple_str(nested)


def _capability_resolution_metadata(result: CapabilityResolutionResult) -> dict[str, Any]:
    return {
        "request_id": result.request.request_id,
        "capability_id": result.capability.capability_id,
        "capability": result.capability.name,
        "capability_version": result.capability.version,
        "skill_id": result.skill.skill_id,
        "skill_version": result.skill.version,
        "fallback_applied": result.fallback_applied,
        "fallback_from": result.fallback_from,
        "guardian_decision_ref": result.guardian_decision.evaluation_id if result.guardian_decision else None,
        "reasons": result.reasons,
        "declarative_resolution_only": True,
    }


def _capability_execution_metadata(result: CapabilityExecutionResult) -> dict[str, Any]:
    return {
        "capability": result.capability,
        "skill_id": result.skill,
        "mission_id": result.mission_id,
        "workflow_id": result.workflow_id,
        "task_id": result.task_id,
        "agent_assignment_id": result.agent_assignment_id,
        "success": result.success,
        "capability_request_id": result.capability_request_id,
        "skill_request_id": result.skill_request_id,
        "skill_result_ref": result.skill_result_ref,
        "evidence_refs": result.evidence_refs,
        "warnings": result.warnings,
        "errors": result.errors,
        "outputs": result.outputs,
        "guardian_decision_refs": result.guardian_decision_refs,
        "metadata": result.metadata,
    }


def _attempt(task: Task, attempt: TaskAttempt | None, attempt_id: str) -> TaskAttempt:
    if attempt is not None:
        return attempt
    return TaskAttempt(
        task_id=task.task_id,
        workflow_id=task.workflow_id,
        mission_id=task.mission_id,
        attempt_number=max(1, task.attempt_count + 1),
        attempt_id=attempt_id,
    )


def _context_refs(task: Task, governance_result: AgentExecutionGovernanceResult | None) -> tuple[str, ...]:
    refs = list(task.context_refs)
    if governance_result is not None:
        refs.append(governance_result.context_package.context_package_id)
    return tuple(dict.fromkeys(refs))


def _governance_metadata(governance_result: AgentExecutionGovernanceResult | None) -> dict[str, Any]:
    if governance_result is None:
        return {}
    model_decision = governance_result.model_selection_decision
    context_package = governance_result.context_package
    return {
        "governance_preparation_id": governance_result.preparation_id,
        "policy_resolution_id": governance_result.resolved_policy_set.resolution_id,
        "matched_policy_refs": governance_result.resolved_policy_set.matched_policy_refs,
        "context_request_id": governance_result.context_request.request_id,
        "context_package_id": context_package.context_package_id,
        "context_package": context_package,
        "estimated_context_tokens": context_package.token_estimate.estimated_tokens,
        "reserved_output_tokens": context_package.output_token_reservation,
        "available_context_tokens": context_package.metadata.get("available_context_tokens"),
        "model_selection_decision_ref": model_decision.selected_model.id if model_decision else None,
        "selected_model_id": model_decision.selected_model.id if model_decision else None,
        "guardian_decision_refs": governance_result.guardian_decision_refs,
        "audit_event_refs": governance_result.audit_event_refs,
        "approval_requirements": governance_result.approval_requirements,
        "governance_warnings": governance_result.warnings,
    }


def _governance_result_metadata(governance_result: AgentExecutionGovernanceResult | None) -> dict[str, Any]:
    metadata = _governance_metadata(governance_result)
    metadata.pop("context_package", None)
    return metadata


__all__ = ["AgentOrchestrator", "AgentOrchestratorError", "NoCompatibleAgentError"]

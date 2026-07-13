from __future__ import annotations

from collections.abc import Iterable

from vercosa_ai_framework.agents import AgentExecutionGovernance, AgentOrchestrator, AgentProfile, AgentRegistry, AgentRole, AgentTaskExecutor
from vercosa_ai_framework.audit import InMemoryEventLog
from vercosa_ai_framework.audit.types import EventCategory
from vercosa_ai_framework.capabilities import CapabilityProfile, CapabilityRegistry, CapabilityResolver, ResolvedCapabilityExecutor
from vercosa_ai_framework.context import ContextItem, ContextItemType, ContextSource, ContextSourceType, DeterministicContextRouter
from vercosa_ai_framework.guardian import GuardianAction, GuardianDecision, GuardianEngine, GuardianEvaluationContext, GuardianMode
from vercosa_ai_framework.model_selection import ModelProfile, ModelSelector
from vercosa_ai_framework.policy import PolicyEffect, PolicyRule, PolicyScope, PolicySet, PolicySource
from vercosa_ai_framework.providers import ProviderGateway, ProviderKind, ProviderProfile, ProviderRegistry
from vercosa_ai_framework.runtime import RuntimeAdapter, RuntimeExecutionPlan, RuntimeExecutionRequest, RuntimeExecutionResult, RuntimeInfo, RuntimeStatus
from vercosa_ai_framework.skills import SkillExecutor, SkillProfile, SkillRegistry
from vercosa_ai_framework.tasks import Task, TaskQueue, TaskQueueState, TaskScheduler
from vercosa_ai_framework.tools import ToolExecutor, ToolProfile, ToolRegistry
from vercosa_ai_framework.workflows import Workflow, WorkflowEngine, WorkflowStatus, WorkflowTask


class FakeRuntimeAdapter(RuntimeAdapter):
    def __init__(self) -> None:
        self.requests: list[RuntimeExecutionRequest] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self) -> tuple[ModelProfile, ...]:
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return self.execute_task(request)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.requests.append(request)
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake-runtime",
            status=RuntimeStatus.DONE,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            selected_model=request.selection_decision.selected_model.id if request.selection_decision else None,
            artifacts=("artifact-0107.md",),
            audit_log_ref="memory://runtime/0107",
        )

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return ()

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(self, mission_id: str, expected_artifacts: Iterable[str]) -> tuple[str, ...]:
        return tuple(expected_artifacts)


class CountingGuardian(GuardianEngine):
    def __init__(self, *, context_action: GuardianAction = GuardianAction.ALLOW) -> None:
        super().__init__()
        self.evaluations: list[GuardianEvaluationContext] = []
        self.context_action = context_action

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        self.evaluations.append(context)
        return super().evaluate(context)

    def evaluate_context_package(self, package, *, mission_id=None, guardian_mode=GuardianMode.STANDARD, evaluation_id=None):
        decision = super().evaluate_context_package(package, mission_id=mission_id, guardian_mode=guardian_mode, evaluation_id=evaluation_id)
        if self.context_action is GuardianAction.ALLOW:
            return decision
        return GuardianDecision(
            mission_id=decision.mission_id,
            evaluation_id=decision.evaluation_id,
            decision=self.context_action,
            guardian_mode=decision.guardian_mode,
            reasons=(f"context guardian forced {self.context_action.value}",),
            approval_requirements=("approve context",) if self.context_action is GuardianAction.REQUIRE_APPROVAL else (),
        )


class CountingProviderAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, request, profile):
        self.calls += 1
        return {"called": True}


def profile() -> AgentProfile:
    return AgentProfile(
        agent_profile_id="agent-0107",
        role=AgentRole.IMPLEMENTATION_ARCHITECT,
        domain="framework",
        supported_task_types=("integration-test",),
        supported_capabilities=("ReadContext",),
        complexity_range=("low", "medium", "high"),
        risk_range=("low", "medium", "high"),
        default_model_policy={"quality": "standard", "reasoning": "light", "memory": "short", "allow_paid": False, "prefer_local": True},
        default_execution_limits={"max_input_tokens": 64, "reserved_output_tokens": 16},
    )


def policy_set(*rules: PolicyRule) -> PolicySet:
    return PolicySet(
        policy_set_id="policy-0107",
        name="0107",
        source=PolicySource.MISSION,
        scope=PolicyScope.TASK,
        rules=rules,
    )


def allow_rule() -> PolicyRule:
    return PolicyRule("policy.allow.local", "network", PolicyEffect.ALLOW, scope=PolicyScope.GLOBAL, value="deny")


def task_with_governance(*, rules: tuple[PolicyRule, ...] = (allow_rule(),), model_policy: dict[str, object] | None = None) -> Task:
    source = ContextSource("src-0107", source_type=ContextSourceType.SPEC, trust_level="high", sensitivity="public")
    small = ContextItem("ctx-small", source_ref="src-0107", content="Resumo curto", item_type=ContextItemType.INSTRUCTION, rank=0)
    large = ContextItem("ctx-large", source_ref="src-0107", content="x" * 400, item_type=ContextItemType.INSTRUCTION, rank=1)
    metadata = {
        "role": "implementation_architect",
        "domain": "framework",
        "policy_sets": (policy_set(*rules),),
        "context_sources": (source,),
        "context_items": (small, large),
        "token_budget": {"max_input_tokens": 64, "reserved_output_tokens": 16},
        "model_policy": model_policy or {"quality": "standard", "reasoning": "light", "memory": "short", "allow_paid": False},
        "granted_permissions": ("read_workspace",),
        "capability_inputs": {"ReadContext": {"query": "0107"}},
        "allowed_tools": ("workspace_search",),
        "allowed_effects": ("read",),
        "expected_outputs": ("AgentExecutionResult",),
        "acceptance_criteria": ("fluxo governado validado",),
    }
    return Task(
        title="0107",
        goal="Executar fluxo minimo governado. Entregaveis: resultado. Criterios de aceite: validado.",
        workflow_id="wf-0107",
        mission_id="mission-0107",
        task_id="task-0107",
        task_type="integration-test",
        required_capabilities=("ReadContext",),
        metadata=metadata,
    )


def capability_stack():
    adapter = CountingProviderAdapter()
    capability_registry = CapabilityRegistry((CapabilityProfile(name="ReadContext", version="1.0", description="Ler contexto", intent="Ler contexto governado", domain="framework", capability_id="cap-read", required_permissions=("read_workspace",)),))
    skill_registry = SkillRegistry((SkillProfile(skill_id="skill-read", name="read_context", version="1.0", description="Skill local", implemented_capabilities=("ReadContext",), domain="framework", required_tools=("workspace_search",), permission_requirements=("read_workspace",)),))
    tool_registry = ToolRegistry((ToolProfile(tool_id="tool-search", name="workspace_search", version="1.0", description="Tool local", provider_type="mock", provider_ref="provider-local", operation_type="search", domain="framework", effects=("read",), required_permissions=("read_workspace",), network_policy="none"),))
    provider_registry = ProviderRegistry((ProviderProfile(provider_id="provider-local", name="local", version="1.0", description="Provider local", kind=ProviderKind.MOCK, adapter_ref="adapters.local", supported_operations=("search",), effects=("read",), required_permissions=("read_workspace",), network_policy="none"),))
    provider_gateway = ProviderGateway(provider_registry, adapters={"adapters.local": adapter})
    tool_executor = ToolExecutor(tool_registry, provider_gateway=provider_gateway)
    skill_executor = SkillExecutor(skill_registry, tool_registry, tool_executor)
    return CapabilityResolver(capability_registry, skill_registry, tool_registry), ResolvedCapabilityExecutor(skill_executor, dry_run=True), adapter


def governed_orchestrator(runtime: FakeRuntimeAdapter, event_log: InMemoryEventLog, guardian: GuardianEngine | None = None, models: tuple[ModelProfile, ...] | None = None) -> tuple[AgentOrchestrator, CountingProviderAdapter]:
    capability_resolver, capability_executor, adapter = capability_stack()
    governance = AgentExecutionGovernance(
        context_router=DeterministicContextRouter(),
        guardian_engine=guardian or CountingGuardian(),
        model_selector=ModelSelector(models or (ModelProfile(id="local-model", provider="local", runtime="fake", context_window=256, local=True, free=True),)),
        event_log=event_log,
        spec_refs=("specs/framework/0001-framework-foundation.md",),
    )
    return AgentOrchestrator(
        registry=AgentRegistry((profile(),)),
        runtime_adapter=runtime,
        capability_resolver=capability_resolver,
        require_capability_resolution=True,
        capability_executor=capability_executor,
        require_capability_execution=True,
        execution_governance=governance,
        require_execution_governance=True,
    ), adapter


def test_governed_flow_propagates_policy_context_budget_model_audit_and_dry_run_capability():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    orchestrator, provider_adapter = governed_orchestrator(runtime, event_log)

    queue = TaskQueue(workflow_id="wf-0107", mission_id="mission-0107")
    queue.add_task(task_with_governance())
    scheduler_result = TaskScheduler().run_until_idle(queue, AgentTaskExecutor(orchestrator))

    finished = queue.list_tasks()[0]
    outcome = finished.metadata["agent_execution_result"]
    runtime_request = runtime.requests[0]
    agent_request = runtime_request.context["agent_execution_request"]
    context_package = runtime_request.context["context_package"]
    event_names = tuple(event.name for event in event_log.list_events())

    assert scheduler_result.status == "done"
    assert finished.state == TaskQueueState.DONE
    assert len(runtime.requests) == 1
    assert provider_adapter.calls == 0
    assert context_package.context_package_id == agent_request.metadata["context_package_id"]
    assert context_package.token_estimate.estimated_tokens <= context_package.metadata["available_context_tokens"]
    assert context_package.omission_reasons[0].item_ref == "ctx-large"
    assert runtime_request.selection_decision.selected_model.id == "local-model"
    assert agent_request.metadata["policy_resolution_id"]
    assert agent_request.metadata["matched_policy_refs"] == ("policy.allow.local",)
    assert outcome["policy_resolution_id"] == agent_request.metadata["policy_resolution_id"]
    assert outcome["context_package_id"] == context_package.context_package_id
    assert outcome["selected_model_id"] == "local-model"
    assert event_names[:4] == (
        "policy.resolution",
        "context.package",
        "guardian.decision",
        "model_selection.decision",
    )
    assert "agent_execution.governance_started" in event_names
    assert "agent_execution.runtime_result" in event_names
    assert "agent_execution.final_result" in event_names
    assert all("Resumo curto" not in repr(event.metadata) for event in event_log.list_events())


def test_guardian_block_stops_before_capability_executor_and_runtime():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    orchestrator, provider_adapter = governed_orchestrator(runtime, event_log, guardian=CountingGuardian(context_action=GuardianAction.BLOCK))

    result = orchestrator.execute_task(task_with_governance())

    assert result.success is False
    assert runtime.requests == []
    assert provider_adapter.calls == 0
    assert result.metadata["context_package_id"]
    assert "context guardian forced block" in result.errors
    assert tuple(event.name for event in event_log.list_events())[-1] == "agent_execution.governance_blocked"


def test_guardian_require_approval_stops_before_runtime_without_explicit_approval():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    orchestrator, provider_adapter = governed_orchestrator(runtime, event_log, guardian=CountingGuardian(context_action=GuardianAction.REQUIRE_APPROVAL))

    result = orchestrator.execute_task(task_with_governance())

    assert result.success is False
    assert runtime.requests == []
    assert provider_adapter.calls == 0
    assert result.metadata["approval_requirements"] == ("approve context",)


def test_guardian_warn_allows_execution_and_preserves_warning():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    warn_rule = PolicyRule("policy.warn.context", "context", PolicyEffect.WARN, scope=PolicyScope.CONTEXT)
    orchestrator, _ = governed_orchestrator(runtime, event_log)

    result = orchestrator.execute_task(task_with_governance(rules=(allow_rule(), warn_rule)))

    assert result.success is True
    assert len(runtime.requests) == 1
    assert any("politica resolvida" in warning or "context package contem warning" in warning for warning in result.metadata["governance_warnings"])


def test_model_incompatible_with_context_budget_fails_before_runtime():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    tiny_model = ModelProfile(id="tiny", provider="local", runtime="fake", context_window=8, local=True, free=True)
    orchestrator, provider_adapter = governed_orchestrator(runtime, event_log, models=(tiny_model,))

    result = orchestrator.execute_task(task_with_governance())

    assert result.success is False
    assert runtime.requests == []
    assert provider_adapter.calls == 0
    assert "model selection failed" in result.errors[0]


def test_policy_deny_excludes_model_before_runtime():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    deny_model = PolicyRule("policy.deny.model", "model", PolicyEffect.DENY, scope=PolicyScope.MODEL, value="local-model")
    orchestrator, _ = governed_orchestrator(runtime, event_log)

    result = orchestrator.execute_task(task_with_governance(rules=(allow_rule(), deny_model)))

    assert result.success is False
    assert runtime.requests == []
    assert "model selection failed" in result.errors[0]


def test_require_execution_governance_without_dependency_fails_legacy_opt_in():
    runtime = FakeRuntimeAdapter()
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((profile(),)),
        runtime_adapter=runtime,
        require_execution_governance=True,
    )

    result = orchestrator.execute_task(task_with_governance())

    assert result.success is False
    assert runtime.requests == []
    assert result.errors == ("execution governance is required but was not configured",)


def test_events_do_not_store_sensitive_context_or_prompt_fields():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    orchestrator, _ = governed_orchestrator(runtime, event_log)

    orchestrator.execute_task(task_with_governance())


    forbidden = ("Resumo curto", "x" * 40, "prompt", "content")
    for event in event_log.list_events():
        payload = repr(dict(event.metadata))
        assert not any(value in payload for value in forbidden)
    assert event_log.filter_by_category(EventCategory.MODEL_SELECTION)


def test_workflow_engine_queue_path_runs_governed_agent_flow_end_to_end():
    runtime = FakeRuntimeAdapter()
    event_log = InMemoryEventLog()
    orchestrator, _ = governed_orchestrator(runtime, event_log)
    source_task = task_with_governance()
    workflow_task = WorkflowTask(
        task_id=source_task.task_id,
        workflow_id=source_task.workflow_id,
        mission_id=source_task.mission_id,
        title=source_task.title,
        goal=source_task.goal,
        task_type=source_task.task_type,
        required_capabilities=source_task.required_capabilities,
        inputs={
            "policy_sets": source_task.metadata["policy_sets"],
            "context_sources": source_task.metadata["context_sources"],
            "context_items": source_task.metadata["context_items"],
            "token_budget": source_task.metadata["token_budget"],
            "granted_permissions": source_task.metadata["granted_permissions"],
            "capability_inputs": source_task.metadata["capability_inputs"],
            "allowed_tools": source_task.metadata["allowed_tools"],
            "allowed_effects": source_task.metadata["allowed_effects"],
        },
        model_policy=source_task.metadata["model_policy"],
        expected_outputs=("AgentExecutionResult",),
        acceptance_criteria=("WorkflowResult done",),
    )
    workflow = Workflow(
        workflow_id=source_task.workflow_id,
        mission_id=source_task.mission_id,
        title="0107 workflow",
        goal="Executar workflow governado",
        tasks=(workflow_task,),
    )
    engine = WorkflowEngine(runtime, CountingGuardian(), queue_task_executor=AgentTaskExecutor(orchestrator))

    result = engine.execute_with_queue(workflow)

    assert result.status == WorkflowStatus.DONE
    assert result.task_results[0].status.value == "done"
    assert len(runtime.requests) == 1
    assert runtime.requests[0].context["policy_resolution_id"]
    assert runtime.requests[0].context["context_package_id"]
    assert runtime.requests[0].selection_decision.selected_model.id == "local-model"

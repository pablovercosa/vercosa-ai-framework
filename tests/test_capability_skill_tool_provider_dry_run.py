from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from vercosa_ai_framework.agents import AgentOrchestrator, AgentProfile, AgentRegistry, AgentRole, AgentTaskExecutor
from vercosa_ai_framework.capabilities import (
    CapabilityProfile,
    CapabilityRequest,
    CapabilityRegistry,
    CapabilityResolver,
    ResolvedCapabilityExecutor,
)
from vercosa_ai_framework.providers import ProviderGateway, ProviderKind, ProviderProfile, ProviderRegistry
from vercosa_ai_framework.runtime import RuntimeAdapter, RuntimeExecutionPlan, RuntimeExecutionRequest, RuntimeExecutionResult, RuntimeInfo, RuntimeStatus
from vercosa_ai_framework.skills import SkillExecutor, SkillProfile, SkillRegistry
from vercosa_ai_framework.tasks import Task, TaskQueue, TaskQueueState, TaskScheduler
from vercosa_ai_framework.tools import ToolExecutor, ToolProfile, ToolRegistry


class FakeRuntimeAdapter(RuntimeAdapter):
    def __init__(self) -> None:
        self.requests: list[RuntimeExecutionRequest] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        return RuntimeInfo(runtime_id="fake", runtime_name="Fake", available=True)

    def list_models(self):
        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        return RuntimeExecutionPlan(mission_id=request.mission_id, workspace=request.workspace)

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        return self.execute_task(request)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        self.requests.append(request)
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id="fake",
            status=RuntimeStatus.DONE,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            artifacts=("artifact-0106.md",),
            audit_log_ref="memory://runtime/0106",
        )

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        return ()

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(mission_id=mission_id, runtime_id="fake", status=RuntimeStatus.STOPPED)

    def validate_artifacts(self, mission_id: str, expected_artifacts: Iterable[str]) -> tuple[str, ...]:
        return tuple(expected_artifacts)


class CountingProviderAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def execute(self, request, profile):
        self.calls += 1
        return {"called": True}


def capability(name: str = "ReadContext", *, permissions: tuple[str, ...] = ("read_workspace",)) -> CapabilityProfile:
    return CapabilityProfile(
        capability_id=f"cap-{name}",
        name=name,
        version="1.0",
        description="Capability de teste 0106.",
        intent="Ler contexto governado.",
        domain="framework",
        required_permissions=permissions,
    )


def skill(name: str = "ReadContext", *, tool: str = "workspace_search") -> SkillProfile:
    return SkillProfile(
        skill_id=f"skill-{name}",
        name=f"skill_{name}",
        version="1.0",
        description="Skill de teste 0106.",
        implemented_capabilities=(name,),
        domain="framework",
        required_tools=(tool,),
        permission_requirements=("read_workspace",),
    )


def tool(
    *,
    name: str = "workspace_search",
    provider_ref: str = "provider-local",
    effects: tuple[str, ...] = ("read",),
    permissions: tuple[str, ...] = ("read_workspace",),
) -> ToolProfile:
    return ToolProfile(
        tool_id=f"tool-{name}",
        name=name,
        version="1.0",
        description="Tool de teste 0106.",
        provider_type="mock",
        provider_ref=provider_ref,
        operation_type="search",
        domain="framework",
        effects=effects,
        required_permissions=permissions,
        timeout=2.0,
        network_policy="none",
    )


def provider(
    *,
    provider_id: str = "provider-local",
    enabled: bool = True,
    blocked: bool = False,
    dangerous: bool = False,
    deprecated: bool = False,
    effects: tuple[str, ...] = ("read",),
    permissions: tuple[str, ...] = ("read_workspace",),
    data_sensitivity_allowed: tuple[str, ...] = ("public",),
) -> ProviderProfile:
    return ProviderProfile(
        provider_id=provider_id,
        name="local_mock_provider",
        version="1.0",
        description="Provider declarativo local para dry-run.",
        kind=ProviderKind.MOCK,
        adapter_ref="adapters.local_mock",
        supported_operations=("search",),
        supported_domains=("framework",),
        effects=effects,
        required_permissions=permissions,
        network_policy="none",
        data_sensitivity_allowed=data_sensitivity_allowed,
        default_timeout=3.0,
        enabled=enabled,
        blocked=blocked,
        dangerous=dangerous,
        deprecated=deprecated,
    )


def agent_profile(capabilities: tuple[str, ...] = ("ReadContext",)) -> AgentProfile:
    return AgentProfile(
        agent_profile_id="agent-0106",
        role=AgentRole.IMPLEMENTATION_ARCHITECT,
        domain="framework",
        supported_task_types=("integration-test",),
        supported_capabilities=capabilities,
        complexity_range=("low", "medium", "high"),
        risk_range=("low", "medium", "high"),
    )


def make_task(
    *,
    required_capabilities: tuple[str, ...] = ("ReadContext",),
    permissions: tuple[str, ...] = ("read_workspace",),
    allowed_tools: object = ("workspace_search",),
    allowed_effects: object = ("read",),
) -> Task:
    return Task(
        title="0106",
        goal="Executar Capability por Skill, Tool e Provider Gateway em dry-run.",
        workflow_id="wf-0106",
        mission_id="mission-0106",
        task_id="task-0106",
        task_type="integration-test",
        required_capabilities=required_capabilities,
        context_refs=("docs/examples/minimal-capability-skill-tool-provider-dry-run.md",),
        metadata={
            "granted_permissions": permissions,
            "capability_inputs": {name: {"query": name} for name in required_capabilities},
            "allowed_tools": allowed_tools,
            "allowed_effects": allowed_effects,
            "execution_limits": {"timeout": 1.5},
        },
    )


def make_stack(*, capabilities: tuple[CapabilityProfile, ...] = (capability(),), providers: tuple[ProviderProfile, ...] = (provider(),)):
    adapter = CountingProviderAdapter()
    capability_registry = CapabilityRegistry(capabilities)
    skill_registry = SkillRegistry(tuple(skill(profile.name) for profile in capabilities))
    tool_registry = ToolRegistry((tool(),))
    provider_gateway = ProviderGateway(
        ProviderRegistry(providers),
        adapters={"adapters.local_mock": adapter},
        default_timeout=4.0,
    )
    tool_executor = ToolExecutor(tool_registry, provider_gateway=provider_gateway)
    skill_executor = SkillExecutor(skill_registry, tool_registry, tool_executor)
    capability_resolver = CapabilityResolver(capability_registry, skill_registry, tool_registry)
    capability_executor = ResolvedCapabilityExecutor(skill_executor, dry_run=True)
    return capability_resolver, capability_executor, adapter


def run_through_scheduler(task: Task, *, providers: tuple[ProviderProfile, ...] = (provider(),), capabilities: tuple[CapabilityProfile, ...] = (capability(),)):
    runtime = FakeRuntimeAdapter()
    capability_resolver, capability_executor, adapter = make_stack(capabilities=capabilities, providers=providers)
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((agent_profile(tuple(profile.name for profile in capabilities)),)),
        runtime_adapter=runtime,
        capability_resolver=capability_resolver,
        require_capability_resolution=True,
        capability_executor=capability_executor,
        require_capability_execution=True,
    )
    queue = TaskQueue(workflow_id=task.workflow_id, mission_id=task.mission_id)
    queue.add_task(task)
    result = TaskScheduler().run_until_idle(queue, AgentTaskExecutor(orchestrator))
    return queue, result, runtime, adapter


def test_capability_resolution_result_builds_skill_execution_request_and_preserves_selected_skill():
    resolver, executor, _ = make_stack()
    request = make_task().metadata["capability_inputs"]["ReadContext"]
    resolution = resolver.resolve(
        CapabilityRequest(
            capability="ReadContext",
            mission_id="mission-0106",
            workflow_id="wf-0106",
            task_id="task-0106",
            agent_assignment_id="assignment-0106",
            inputs=request,
            granted_permissions=("read_workspace",),
            limits={"timeout": 1.5},
            metadata={"allowed_tools": ("workspace_search",), "allowed_effects": ("read",)},
        )
    )

    skill_request = executor.build_skill_request(resolution)

    assert skill_request.skill == resolution.skill.skill_id
    assert skill_request.capability == "ReadContext"
    assert skill_request.mission_id == "mission-0106"
    assert skill_request.workflow_id == "wf-0106"
    assert skill_request.task_id == "task-0106"
    assert skill_request.agent_assignment_id == "assignment-0106"
    assert skill_request.inputs == {"query": "ReadContext"}
    assert skill_request.allowed_tools == ("workspace_search",)
    assert skill_request.limits["timeout"] == 1.5
    assert skill_request.request_id == resolution.request.request_id


def test_full_task_agent_capability_skill_tool_provider_dry_run_flow_preserves_traceability():
    queue, scheduler_result, runtime, adapter = run_through_scheduler(make_task())

    finished = queue.list_tasks()[0]
    runtime_request = runtime.requests[0]
    agent_request = runtime_request.context["agent_execution_request"]
    capability_execution = agent_request.metadata["capability_executions"][0]

    assert scheduler_result.status == "done"
    assert finished.state == TaskQueueState.DONE
    assert adapter.calls == 0
    assert capability_execution["success"] is True
    assert capability_execution["mission_id"] == "mission-0106"
    assert capability_execution["workflow_id"] == "wf-0106"
    assert capability_execution["task_id"] == "task-0106"
    assert capability_execution["agent_assignment_id"] == agent_request.agent_assignment_id
    assert capability_execution["metadata"]["provider_request_id"]
    assert capability_execution["metadata"]["provider_result_id"]
    assert capability_execution["metadata"]["provider_id"] == "provider-local"
    assert capability_execution["metadata"]["provider_status"] == "dry_run"
    assert capability_execution["outputs"]["dry_run"] is True
    assert "provider adapter was not executed" in capability_execution["warnings"][0]
    assert capability_execution["outputs"]["timeout"] == 1.5
    assert runtime_request.context["capability_executions"] == agent_request.metadata["capability_executions"]


def test_missing_permissions_block_before_provider_gateway_and_runtime():
    queue, _, runtime, adapter = run_through_scheduler(make_task(permissions=()))

    finished = queue.list_tasks()[0]
    assert finished.state == TaskQueueState.FAILED
    assert "permissions" in (finished.last_error or "")
    assert runtime.requests == []
    assert adapter.calls == 0


def test_disallowed_tool_blocks_execution_before_runtime():
    queue, _, runtime, adapter = run_through_scheduler(make_task(allowed_tools=("other_tool",)))

    finished = queue.list_tasks()[0]
    assert finished.state == TaskQueueState.FAILED
    assert "not allowed" in (finished.last_error or "")
    assert runtime.requests == []
    assert adapter.calls == 0


def test_incompatible_effects_block_execution_before_runtime():
    queue, _, runtime, adapter = run_through_scheduler(make_task(allowed_effects=("write",)))
    finished = queue.list_tasks()[0]
    assert finished.state == TaskQueueState.FAILED
    assert "effects" in (finished.last_error or "")
    assert runtime.requests == []
    assert adapter.calls == 0


def test_blocked_disabled_dangerous_deprecated_or_incompatible_provider_fails():
    provider_variants = (
        provider(blocked=True),
        provider(enabled=False),
        provider(dangerous=True),
        provider(deprecated=True),
        provider(permissions=("other_permission",)),
        provider(data_sensitivity_allowed=("confidential",)),
    )

    for provider_profile in provider_variants:
        queue, _, runtime, adapter = run_through_scheduler(make_task(), providers=(provider_profile,))
        finished = queue.list_tasks()[0]
        assert finished.state == TaskQueueState.FAILED
        assert runtime.requests == []
        assert adapter.calls == 0


def test_multiple_capabilities_execute_in_required_order_and_partial_execution_fails():
    capabilities = (capability("ReadContext"), capability("SearchCode"))
    queue, _, runtime, _ = run_through_scheduler(
        make_task(
            required_capabilities=("ReadContext", "SearchCode"),
            allowed_tools={"ReadContext": ("workspace_search",), "SearchCode": ("other_tool",)},
            allowed_effects={"ReadContext": ("read",), "SearchCode": ("read",)},
        ),
        capabilities=capabilities,
    )

    finished = queue.list_tasks()[0]
    executions = finished.metadata["agent_execution_result"]["capability_executions"]

    assert finished.state == TaskQueueState.FAILED
    assert runtime.requests == []
    assert tuple(item["capability"] for item in executions) == ("ReadContext", "SearchCode")
    assert executions[0]["success"] is True
    assert executions[1]["success"] is False


def test_legacy_path_without_capability_executor_remains_compatible():
    runtime = FakeRuntimeAdapter()
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((agent_profile(),)),
        runtime_adapter=runtime,
    )

    result = orchestrator.execute_task(make_task())

    assert result.success is True
    assert len(runtime.requests) == 1
    assert result.metadata["capability_executions"] == ()


def test_required_capability_execution_without_executor_blocks_runtime():
    runtime = FakeRuntimeAdapter()
    resolver, _, _ = make_stack()
    orchestrator = AgentOrchestrator(
        registry=AgentRegistry((agent_profile(),)),
        runtime_adapter=runtime,
        capability_resolver=resolver,
        require_capability_resolution=True,
        require_capability_execution=True,
    )

    result = orchestrator.execute_task(make_task())

    assert result.success is False
    assert "capability executor is required" in result.errors[0]
    assert runtime.requests == []


def test_static_boundaries_keep_tasks_and_orchestrator_decoupled():
    for path in Path("src/vercosa_ai_framework/tasks").glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "vercosa_ai_framework.skills" not in source
        assert "vercosa_ai_framework.tools" not in source
        assert "vercosa_ai_framework.providers" not in source

    orchestrator = Path("src/vercosa_ai_framework/agents/orchestrator.py").read_text(encoding="utf-8")
    assert "ToolExecutor" not in orchestrator
    assert "ProviderGateway" not in orchestrator
    assert "ProviderAdapter" not in orchestrator
    assert "adapters." not in orchestrator


def test_new_dry_run_tests_do_not_use_network_database_or_process_modules():
    source = Path(__file__).read_text(encoding="utf-8")
    assert "".join(("import ", "socket")) not in source
    assert "".join(("import ", "requests")) not in source
    assert "".join(("import ", "urllib")) not in source
    assert "".join(("import ", "http.client")) not in source
    assert "".join(("import ", "psycopg")) not in source
    assert "".join(("import ", "subprocess")) not in source

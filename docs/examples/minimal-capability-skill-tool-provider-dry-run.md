# Fluxo Capability, Skill, Tool E Provider Gateway Em Dry-Run

Links principais: [README principal](../../README.md) | [Exemplos](README.md) | [Capabilities, Skills e Tools](../capabilities-skills-tools.md) | [Agent Orchestrator](../agent-orchestrator.md)

## Objetivo

Mostrar o caminho mínimo validado pela missão 0106:

```text
Task
-> AgentTaskExecutor
-> AgentOrchestrator
-> CapabilityResolver
-> ResolvedCapabilityExecutor
-> SkillExecutor
-> ToolExecutor
-> ProviderGateway em dry-run
-> AgentExecutionResult
-> TaskExecutionOutcome
```

## Estado

Status: `MVP`.

O exemplo é coberto por `tests/test_capability_skill_tool_provider_dry_run.py`. Ele usa fakes locais, registries em memória e `ProviderGateway` real em `dry_run=True`.

## Responsabilidades

- `TaskScheduler` aciona somente um executor injetado.
- `AgentTaskExecutor` adapta `AgentExecutionResult` para `TaskExecutionOutcome`.
- `AgentOrchestrator` resolve e executa capabilities por contratos injetáveis antes do `RuntimeAdapter`.
- `ResolvedCapabilityExecutor` transforma `CapabilityResolutionResult` em `SkillExecutionRequest` preservando a skill selecionada.
- `SkillExecutor` constrói `ToolExecutionRequest`.
- `ToolExecutor` constrói `ProviderRequest` e chama `ProviderGateway`.
- `ProviderGateway` retorna `ProviderResult` com status `dry_run` sem chamar adapter.

## Não Responsabilidades

- Não chama provider real.
- Não acessa rede, banco, MCP ou API externa.
- Não executa subprocesso.
- Não transforma OpenCode em núcleo do fluxo.
- Não integra Policy Engine, Context Router, Token Budget, Model Selection ou Audit/Event Log ao fluxo inteiro; isso permanece para missão futura.

## Exemplo Mínimo

```python
from vercosa_ai_framework.capabilities import CapabilityProfile, CapabilityRegistry, CapabilityResolver, ResolvedCapabilityExecutor
from vercosa_ai_framework.providers import ProviderGateway, ProviderKind, ProviderProfile, ProviderRegistry
from vercosa_ai_framework.skills import SkillExecutor, SkillProfile, SkillRegistry
from vercosa_ai_framework.tools import ToolExecutor, ToolProfile, ToolRegistry

capability = CapabilityProfile(
    capability_id="cap-read-context",
    name="ReadContext",
    version="1.0",
    description="Ler contexto permitido.",
    intent="read governed context",
    domain="framework",
    required_permissions=("read_workspace",),
)

skill = SkillProfile(
    skill_id="skill-read-context",
    name="skill_read_context",
    version="1.0",
    description="Skill local para leitura governada.",
    implemented_capabilities=("ReadContext",),
    domain="framework",
    required_tools=("workspace_search",),
    permission_requirements=("read_workspace",),
)

tool = ToolProfile(
    tool_id="tool-workspace-search",
    name="workspace_search",
    version="1.0",
    description="Tool declarativa para busca local simulada.",
    provider_type="mock",
    provider_ref="provider-local",
    operation_type="search",
    domain="framework",
    effects=("read",),
    required_permissions=("read_workspace",),
    network_policy="none",
)

provider = ProviderProfile(
    provider_id="provider-local",
    name="local_mock_provider",
    version="1.0",
    description="Provider declarativo para dry-run.",
    kind=ProviderKind.MOCK,
    adapter_ref="adapters.local_mock",
    supported_operations=("search",),
    supported_domains=("framework",),
    effects=("read",),
    required_permissions=("read_workspace",),
    network_policy="none",
)

capability_registry = CapabilityRegistry((capability,))
skill_registry = SkillRegistry((skill,))
tool_registry = ToolRegistry((tool,))
provider_gateway = ProviderGateway(ProviderRegistry((provider,)))

tool_executor = ToolExecutor(tool_registry, provider_gateway=provider_gateway)
skill_executor = SkillExecutor(skill_registry, tool_registry, tool_executor)
capability_resolver = CapabilityResolver(capability_registry, skill_registry, tool_registry)
capability_executor = ResolvedCapabilityExecutor(skill_executor, dry_run=True)
```

Na integração com `AgentOrchestrator`, o chamador injeta `capability_resolver`, `capability_executor`, `require_capability_resolution=True` e `require_capability_execution=True`.

## Saídas Esperadas

- `ProviderResult.status == "dry_run"`.
- `ProviderResult.success is True`.
- `ToolExecutionResult.outputs["dry_run"] is True`.
- Warnings indicam que o adapter não foi executado.
- `AgentExecutionRequest.metadata["capability_executions"]` preserva referências de capability, skill, tool e provider.

## Validação

```bash
pytest tests/test_capability_skill_tool_provider_dry_run.py
```

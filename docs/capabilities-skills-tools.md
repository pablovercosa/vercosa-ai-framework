# Capabilities, Skills E Tools MVP

Este MVP implementa contratos da cadeia governada da Spec 0009:

`CapabilityRequest -> CapabilityResolver -> CapabilityExecutor -> SkillExecutor -> ToolExecutor -> ProviderGateway em dry-run`

Agentes solicitam capabilities. Eles não recebem providers, MCPs, APIs, bancos, subprocessos ou tools concretas.

## Components

- `CapabilityResolver` maps a `CapabilityRequest` to a compatible `SkillProfile` using the Capability, Skill, and optional Tool registries.
- `ResolvedCapabilityExecutor` transforma o `CapabilityResolutionResult` em `SkillExecutionRequest` sem escolher outra skill.
- `SkillExecutor` builds a `ToolExecutionRequest` from an authorized `SkillExecutionRequest` and selected tool contract.
- `ToolExecutor` validates permissions/effects, calls Guardian Engine before execution, supports `dry_run`, and delegates provider operations only through `ProviderGateway` when configured.
- `ProviderGateway` seleciona e valida `ProviderProfile` declarativo; em `dry_run=True`, retorna `ProviderResult` com status `dry_run` sem chamar adapter concreto.
- `ToolAdapter` e `ProviderAdapter` são fronteiras para integrações futuras; no fluxo 0106 testado, nenhum adapter concreto é chamado.

No fluxo integrado da missão 0106, `AgentOrchestrator` pode receber `capability_executor` injetado e `require_capability_execution=True`. Nesse modo, todas as capabilities obrigatórias são resolvidas e executadas em ordem antes do `RuntimeAdapter`; qualquer falha bloqueia o runtime. O comportamento legado sem `capability_executor` permanece compatível.

## Governance

- Permissions are explicit and denied by default when missing.
- Guardian decisions `block` and `require_approval` stop execution.
- `dry_run=True` returns a plan-like result and does not call the adapter.
- Fallback is deterministic and limited to alternatives declared in `fallback_skills` or `fallback_tools`.
- No real tools, subprocesses, `sudo`, external APIs, database, network access, MCPs, or real providers are executed by this MVP.
- A skill selecionada durante a resolução é preservada e executada pelo `SkillExecutor`; o executor de capability não seleciona outra skill silenciosamente.

## Rastreabilidade 0106

O caminho integrado preserva referências de `mission_id`, `workflow_id`, `task_id`, `attempt_id`, `agent_assignment_id`, request de capability, resolução de capability, request/result de skill, request/result de tool, request/result de provider, warnings, errors e referências Guardian quando existirem.

Os resumos aparecem em:

- `AgentExecutionRequest.metadata["capability_resolutions"]`.
- `AgentExecutionRequest.metadata["capability_executions"]`.
- `AgentExecutionResult.metadata["capability_executions"]`.
- `TaskExecutionOutcome.metadata["agent_execution_result"]["capability_executions"]`.

## Provider Agnostic Boundary

Capabilities remain functional intent. Skills remain reusable procedures. Tools encapsulate concrete mechanisms behind adapters. MCPs and providers stay outside agents and outside the core contracts.

Exemplo mínimo: [Fluxo Capability, Skill, Tool e Provider Gateway em dry-run](examples/minimal-capability-skill-tool-provider-dry-run.md).

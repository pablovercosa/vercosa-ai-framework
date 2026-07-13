# Capabilities, Skills E Tools MVP

Este MVP implementa contratos da cadeia governada da Spec 0009:

`CapabilityRequest -> CapabilityResolver -> SkillProfile declarativa`

Agentes solicitam capabilities. Eles não recebem providers, MCPs, APIs, bancos, subprocessos ou tools concretas.

## Components

- `CapabilityResolver` maps a `CapabilityRequest` to a compatible `SkillProfile` using the Capability, Skill, and optional Tool registries.
- `SkillExecutor` builds a `ToolExecutionRequest` from an authorized `SkillExecutionRequest` and selected tool contract.
- `ToolExecutor` validates permissions/effects, calls Guardian Engine before execution, supports `dry_run`, and invokes only an injected `ToolAdapter` or callable.
- `ToolAdapter` is the abstract boundary where future provider, MCP, API, database, filesystem, or runtime integrations must live.

No fluxo integrado da missão 0105, somente `CapabilityResolver` participa do caminho operacional. `SkillExecutor`, `ToolExecutor` e `ToolAdapter` existem como contratos/MVPs, mas não são chamados por esse fluxo.

## Governance

- Permissions are explicit and denied by default when missing.
- Guardian decisions `block` and `require_approval` stop execution.
- `dry_run=True` returns a plan-like result and does not call the adapter.
- Fallback is deterministic and limited to alternatives declared in `fallback_skills` or `fallback_tools`.
- No real tools, subprocesses, `sudo`, external APIs, or providers are executed by this MVP.
- A skill selecionada durante a resolução é evidência declarativa, não execução de skill.

## Provider Agnostic Boundary

Capabilities remain functional intent. Skills remain reusable procedures. Tools encapsulate concrete mechanisms behind adapters. MCPs and providers stay outside agents and outside the core contracts.

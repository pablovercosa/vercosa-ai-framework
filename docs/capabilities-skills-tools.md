# Capabilities, Skills and Tools MVP

This MVP implements the governed resolution chain from Spec 0009:

`CapabilityRequest -> CapabilityResolver -> SkillExecutor -> ToolExecutor -> ToolAdapter`

Agents request capabilities only. They do not receive providers, MCPs, APIs, databases, subprocesses, or concrete tools.

## Components

- `CapabilityResolver` maps a `CapabilityRequest` to a compatible `SkillProfile` using the Capability, Skill, and optional Tool registries.
- `SkillExecutor` builds a `ToolExecutionRequest` from an authorized `SkillExecutionRequest` and selected tool contract.
- `ToolExecutor` validates permissions/effects, calls Guardian Engine before execution, supports `dry_run`, and invokes only an injected `ToolAdapter` or callable.
- `ToolAdapter` is the abstract boundary where future provider, MCP, API, database, filesystem, or runtime integrations must live.

## Governance

- Permissions are explicit and denied by default when missing.
- Guardian decisions `block` and `require_approval` stop execution.
- `dry_run=True` returns a plan-like result and does not call the adapter.
- Fallback is deterministic and limited to alternatives declared in `fallback_skills` or `fallback_tools`.
- No real tools, subprocesses, `sudo`, external APIs, or providers are executed by this MVP.

## Provider Agnostic Boundary

Capabilities remain functional intent. Skills remain reusable procedures. Tools encapsulate concrete mechanisms behind adapters. MCPs and providers stay outside agents and outside the core contracts.

# Roadmap

## Roadmap Purpose

This roadmap recommends the next architectural blocks after the current alignment checkpoint. It is not an implementation authorization by itself.

No source code should be implemented from this document alone. Each implementation block still needs an approved Spec or an explicit update to an existing approved Spec.

## Guiding Principle

Prefer integration of existing MVP contracts before adding new frameworks, new providers, new databases, or new agent behaviors.

The next phase should reduce ambiguity, not increase feature surface.

## Block 0: Alignment Freeze

Goal: make the current architecture explicit before further implementation.

Recommended actions:

- Review the six `docs/alignment/` documents.
- Confirm vocabulary for Mission Runner, Mission Orchestrator, Workflow Engine, Task Queue, Agent Orchestrator, Policy Engine, Guardian Engine, Knowledge Hub, Context Router, and Semantic Index.
- Identify conflicts between current code, MVP docs, and specs.
- Convert unresolved architectural decisions into ADRs.

Exit criteria:

- The team agrees which components are core, which are adapters, and which are future optional integrations.
- No new implementation proceeds through ambiguous boundaries.

## Block 1: Policy Boundary Decision

Goal: resolve Policy Engine versus Guardian Engine.

Recommended decision paths:

- Option A: Guardian Engine is the concrete Policy Engine for the current framework phase.
- Option B: Policy Engine becomes a resolver/orchestrator of policies, and Guardian Engine becomes the risk/security/approval evaluator.

Recommended output:

- ADR for Policy Engine and Guardian Engine boundary.
- Update affected specs if the decision changes terminology.
- Define where policy precedence is resolved.

Why this comes first:

Policy decisions affect every other layer: mission execution, tools, providers, runtimes, context routing, model selection, logs, approvals, and validation.

## Block 2: Context Architecture

Goal: separate persistent memory, Knowledge Hub, Semantic Index, and Context Router.

Recommended actions:

- Define Context Router as a first-class component.
- Define what inputs it receives: mission, spec refs, task, agent role, risk, token budget, model decision, and retrieval needs.
- Define what outputs it produces: context bundle, citations, redactions, warnings, and omitted-context reasons.
- Define how Knowledge Hub serves canonical documents and retrieval results.
- Define how Semantic Index supports retrieval without becoming memory itself.

Recommended output:

- Spec or ADR for Context Router.
- Update Spec 0011 if needed.
- Define minimal retrieval contract before implementing embeddings.

Why this comes before pgvector:

Without a Context Router contract, semantic search can become an ungoverned prompt-expansion mechanism that wastes tokens and bypasses policy.

## Block 3: Mission-To-Task Integration

Goal: connect existing mission, workflow, and task MVPs through explicit contracts.

Recommended actions:

- Define Mission Orchestrator as distinct from Mission Runner.
- Define Mission Orchestrator output as Workflow Plan or workflow selection decision.
- Define Workflow Engine handoff to Task Queue.
- Define how Task Queue returns task execution state to Workflow Engine and Mission Runner.

Recommended output:

- ADR or Spec update for Mission Orchestrator boundary.
- Contract between Mission Runner and Workflow Engine.
- Contract between Workflow Engine and Task Queue.

Implementation should remain sequential until policy for parallelism and locks exists.

## Block 4: Task-To-Agent Integration

Goal: connect task execution to Agent Orchestrator without giving agents infrastructure access.

Recommended actions:

- Define default executor from Task Queue to Agent Orchestrator.
- Define Agent Assignment lifecycle.
- Define how an agent requests capabilities.
- Define how agent output becomes task output, validation evidence, and audit records.

Recommended output:

- Contract between Task Queue and Agent Orchestrator.
- Contract between Agent Orchestrator and Capability Resolver.
- Agent profile registry persistence decision.

Guardrail:

Agents must not call tools, providers, MCPs, runtime adapters, shell, or databases directly.

## Block 5: Capability-To-Provider Integration

Goal: make the Capabilities -> Skills -> Tools -> Provider Gateway path the default for concrete side effects.

Recommended actions:

- Define essential capability catalog.
- Define essential skill catalog.
- Define allowed local tools and their permission/effect model.
- Define Provider Gateway audit events.
- Define MCP adapter shape under tools/providers, not under agents.

Recommended output:

- Capability catalog MVP.
- Skill catalog MVP.
- Tool permission matrix.
- Provider Gateway contract tests.

Guardrail:

MCPs are external mechanisms behind tools/providers. They are not agent dependencies.

## Block 6: Persistence Integration

Goal: persist critical records through ports before adding database-specific adapters.

Recommended actions:

- Define stores for missions, workflows, tasks, Guardian decisions, model decisions, audit logs, canonical documents, and knowledge documents.
- Use filesystem adapter as the first governed persistence implementation.
- Define deterministic JSON records and hash semantics.
- Define retention policy for logs.

Recommended output:

- Persistence contract tests.
- Filesystem layout decision.
- Migration path document for future SQLite/PostgreSQL adapters.

Guardrail:

Do not make PostgreSQL the required default before persistence ports are stable.

## Block 7: Semantic Index MVP

Goal: add semantic retrieval only after Context Router and Knowledge Hub contracts are stable.

Recommended actions:

- Define document chunking strategy.
- Define embedding provider adapter contract.
- Define vector store adapter contract.
- Define pgvector adapter as one implementation, not the only option.
- Define local embedding default as capability detection, not assumption.

Recommended output:

- Semantic Index Spec or Spec 0011 update.
- ADR for initial pgvector/Ollama/nomic-embed-text adapter if selected.
- Tests for retrieval determinism, citation preservation, and redaction behavior.

Guardrail:

Semantic search must return cited, policy-filtered context. It must not dump raw retrieved text into prompts without Context Router approval.

## Block 8: Runtime Adapter Expansion

Goal: keep OpenCode initial while preparing parity for other runtimes.

Recommended actions:

- Formalize common RuntimeAdapter operations.
- Define capability detection schema.
- Define model discovery schema.
- Define execution result schema.
- Define adapter conformance tests.

Candidate future adapters:

- Claude Code;
- Codex CLI;
- Cursor;
- VS Code;
- JetBrains;
- Web UI;
- API.

Guardrail:

Do not add runtime-specific behavior to core modules.

## Block 9: External Orchestration Framework Evaluation

Goal: decide if LangGraph, MetaGPT, or AutoGen should be used as optional adapters, references, or not at all.

Recommended actions:

- Evaluate each framework against provider agnosticism, local-first support, state machine support, auditability, dependency footprint, and adapter feasibility.
- Map each framework to possible roles: workflow backend, agent runtime backend, simulation/reference implementation, or external adapter.
- Avoid adopting any external orchestration framework as the core until Vercosa contracts are stable.

Recommended output:

- ADR for external orchestration framework positioning.

## Block 10: Validation And Commit Governance

Goal: make Spec -> Plan -> Tasks -> Implement -> Validate -> Commit enforceable.

Recommended actions:

- Define validation result records.
- Define how tests, static checks, human review, Guardian decisions, and agent reviews are attached to tasks and missions.
- Define auto-commit policy and default disabled behavior.
- Define how commits reference mission IDs, specs, and validation evidence.

Recommended output:

- SDD lifecycle contract.
- Commit policy ADR or Spec update.

## Recommended Near-Term Order

1. Review alignment docs.
2. ADR: Policy Engine versus Guardian Engine.
3. ADR or Spec: Context Router and memory architecture.
4. ADR or Spec: Mission Orchestrator boundary.
5. Contract: Mission Runner -> Workflow Engine -> Task Queue.
6. Contract: Task Queue -> Agent Orchestrator -> Capability Resolver.
7. Contract tests for existing MVP boundaries.
8. Persistence integration through filesystem adapter.
9. Knowledge Hub semantic index design.
10. Runtime adapter conformance before adding new runtimes.

## Work To Avoid For Now

Avoid these until the above boundaries are settled:

- hardcoding LangGraph, MetaGPT, or AutoGen into the core;
- connecting agents directly to MCPs;
- making pgvector mandatory;
- making Ollama mandatory;
- expanding OpenCode behavior into core orchestration;
- adding autonomous multi-agent parallelism without locks, budgets, and validation;
- implementing infinite memory claims without precise retrieval, retention, and policy rules;
- auto-committing by default;
- adding provider-specific code outside adapters.

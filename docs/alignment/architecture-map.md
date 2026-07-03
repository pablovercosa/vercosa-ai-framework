# Architecture Map

## Architectural Spine

The framework architecture is mission-driven and specification-governed.

Canonical chain:

```text
Mission
↓
Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Agents
↓
Subagents
↓
Capabilities
↓
Policy Engine / Guardian Engine
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Providers / MCPs / APIs / Runtimes
```

The main rule is dependency inversion: upper layers express intent; lower layers provide replaceable execution mechanisms.

## Layer Map

| Layer | Purpose | Current State | Must Not Do |
| --- | --- | --- | --- |
| Mission | User/system intent and required deliverables | Represented by `missions/types.py` and queue files | Encode runtime-specific commands as architecture |
| Mission Runner | Operational lifecycle, queue, cycles, validation, final state | MVP exists in `missions/runner.py` and `missions/queue.py` | Replace Mission Orchestrator or Workflow Engine permanently |
| Mission Orchestrator | Decide which workflow should satisfy a mission | Conceptual, not clearly implemented as distinct module | Become a runtime adapter or CLI command |
| Workflow Engine | Build/execute workflow plan and task order | Sequential MVP exists in `workflows/engine.py` | Own mission lifecycle, agent registry, or provider execution |
| Task Queue | Manage task states, dependencies, attempts, retries | MVP exists in `tasks/` | Execute concrete providers or choose agents by itself |
| Agent Orchestrator | Select agent profile and prepare agent execution | MVP exists in `agents/` | Call OpenCode, MCPs, APIs, databases, or tools directly |
| Agents/Subagents | Execute domain responsibilities through framework boundaries | Conceptual/MVP profile level | Know concrete providers or infrastructure |
| Capabilities | Abstract requested abilities | MVP exists in `capabilities/` | Encode concrete tool/provider details |
| Policy/Guardian | Enforce specs, risks, permissions, limits, approvals | Guardian MVP exists; Policy Engine boundary is still ambiguous | Execute commands or mutate state directly |
| Skills | Reusable procedures implementing capabilities | MVP exists in `skills/` | Bypass tools or provider gateway for side effects |
| Tools | Governed concrete action boundary | MVP exists in `tools/` | Hide direct provider calls from governance |
| Provider Gateway | Normalize provider access after tool approval | MVP exists in `providers/` | Become model selector, runtime adapter, or agent layer |
| Providers/MCPs/APIs/Runtimes | Concrete external mechanisms | OpenCode runtime MVP exists; providers are injectable MVP contracts | Leak into core or agent abstractions |

## Source Module Map

`src/vercosa_ai_framework/core/`

Shared domain models and policy primitives. This should stay independent from external infrastructure.

`src/vercosa_ai_framework/cli.py`

User-facing CLI. It is an interface adapter, not the orchestration core.

`src/vercosa_ai_framework/missions/`

Mission records, queue, and runner. The current runner can execute bounded cycles through Guardian and RuntimeAdapter. It should eventually delegate workflow creation/replanning to Mission Orchestrator and Workflow Engine.

`src/vercosa_ai_framework/workflows/`

Workflow and task execution. Current MVP is sequential and dependency-aware. It uses Guardian before runtime execution.

`src/vercosa_ai_framework/tasks/`

Task queue and scheduler. It tracks task state, dependency eligibility, attempts, and deterministic selection.

`src/vercosa_ai_framework/guardian/`

Policy decision engine MVP. It detects dangerous commands, probable secrets, `sudo`, global config changes, and applies modes. It currently stands in for broader policy behavior.

`src/vercosa_ai_framework/model_selection/`

Model policy and selection contracts. This should sit below policy resolution and above runtime/provider execution.

`src/vercosa_ai_framework/runtime/`

Runtime adapter boundary. Current OpenCode adapter builds controlled `opencode run` commands, supports dry-run, avoids shell expansion, avoids global config mutation, and redacts secret-like metadata.

`src/vercosa_ai_framework/agents/`

Agent profile registry and orchestrator MVP. It prepares provider-neutral agent execution requests and delegates concrete execution to RuntimeAdapter.

`src/vercosa_ai_framework/capabilities/`

Capability registry and resolver. It maps requested capabilities to compatible skills.

`src/vercosa_ai_framework/skills/`

Skill registry and executor. It converts authorized skill execution into tool execution.

`src/vercosa_ai_framework/tools/`

Tool registry and executor. It validates permissions/effects, consults Guardian, supports dry-run, and invokes only injected adapters/callables.

`src/vercosa_ai_framework/providers/`

Provider registry, adapter contract, and provider gateway. The MVP is intentionally side-effect-free unless an adapter/callable is injected.

`src/vercosa_ai_framework/knowledge/`

Knowledge document types, Markdown ingestion, in-memory store, and deterministic text search. This is not yet the semantic Knowledge Hub.

`src/vercosa_ai_framework/canonicalizer/`

Canonicalization contracts and text/Markdown MVP. It prepares canonical Markdown-like documents before indexing or knowledge use.

`src/vercosa_ai_framework/persistence/`

Persistence records, repository abstractions, and filesystem repository MVP. Database adapters are future work.

## Current Integration Paths

Mission Runner path:

```text
Mission file or queued Mission
↓
DirectoryMissionQueue
↓
MissionRunner
↓
GuardianEngine
↓
RuntimeAdapter
↓
OpenCodeRuntimeAdapter or injected fake adapter
↓
MissionResult
```

Workflow path:

```text
Workflow file
↓
WorkflowEngine
↓
GuardianEngine per task
↓
RuntimeAdapter.execute_task()
↓
WorkflowResult
```

Capability path:

```text
CapabilityRequest
↓
CapabilityResolver
↓
SkillExecutor
↓
ToolExecutor
↓
GuardianEngine
↓
ToolAdapter or ProviderGateway
↓
ProviderAdapter or callable
```

Knowledge path:

```text
Markdown source
↓
Markdown parser or Canonicalizer
↓
KnowledgeDocument or CanonicalDocument
↓
InMemoryKnowledgeStore
↓
Deterministic text search
```

Persistence path:

```text
PersistedRecord
↓
Repository contract
↓
FilesystemRepository
↓
Deterministic JSON file
```

## Missing Bridges

The main missing bridges are:

- Mission Orchestrator to Workflow Engine.
- Workflow Engine to Task Queue as the default execution substrate.
- Task Queue to Agent Orchestrator as the default task executor.
- Agent Orchestrator to Capability Resolver for agent-requested capabilities.
- Capability/Skill/Tool path to Provider Gateway as the default side-effect path.
- Knowledge Hub retrieval to Context Router.
- Context Router to Mission Runner, Workflow Engine, Agent Orchestrator, and Model Selection.
- Persistence Layer to missions, workflows, tasks, Guardian decisions, model decisions, knowledge documents, and audit logs.

## Boundary Decisions Needed

Policy Engine versus Guardian Engine:

The specs mention both. Current code implements Guardian Engine. The architecture needs one clear decision: either Guardian Engine is the concrete policy engine, or Policy Engine is a broader resolver that delegates risk/security decisions to Guardian Engine.

Mission Runner versus Mission Orchestrator:

Mission Runner owns operational state. Mission Orchestrator should choose workflows and orchestration strategy. Current MVP risks accumulating orchestration logic inside Mission Runner if this is not separated.

Workflow Engine versus Task Queue:

Workflow Engine should define workflow/task graph semantics. Task Queue should own task state, dependency eligibility, attempts, and scheduling. Current sequential workflow execution can remain MVP, but future execution should use Task Queue intentionally.

Runtime Adapter versus Provider Gateway:

Runtime Adapter executes agent/runtime sessions such as OpenCode. Provider Gateway normalizes concrete provider access behind tools. They should not collapse into one abstraction.

Knowledge Hub versus Context Router:

Knowledge Hub stores and retrieves knowledge. Context Router decides what context to include for a mission/task/agent/model call under token, risk, and policy constraints.

Semantic Index versus Persistent Memory:

Semantic Index is retrieval infrastructure. Persistent memory is durable stored facts, artifacts, decisions, logs, and documents. They overlap but are not the same.

## Memory Terms

Infinite memory:

Not an architectural component. It is a product promise or user-facing shorthand that should mean controlled long-term recall through durable storage, retrieval, summarization, indexing, and policy filtering. The framework should avoid claiming literal infinite memory. Real systems have retention, cost, privacy, storage, token, and relevance limits.

Persistent memory:

Durable stored information that survives a process, agent session, model context window, CLI invocation, or runtime restart. It can include specs, ADRs, decisions, audit logs, missions, workflows, tasks, validation results, conversations, summaries, canonical documents, and learned project facts. Persistent memory is about durability, not necessarily semantic retrieval.

Knowledge Hub:

The governed knowledge subsystem. It owns canonical documents, metadata, provenance, citations, source classification, sensitivity, and retrieval surfaces. It can contain specs, documentation, code references, ADRs, conversations, decisions, legal documents, books, commands, hooks, agents, skills, and project knowledge.

Semantic Index:

An index optimized for semantic retrieval, usually based on embeddings and vector search. It is derived from canonical documents or approved sources. It is not the source of truth; it is a retrieval acceleration and relevance mechanism. It must preserve references back to canonical sources.

Context Router:

The decision component that chooses what context is sent to a model, agent, skill, runtime, or validation step. It should consider mission goal, task, agent role, model context window, token budget, risk, privacy, Guardian decisions, retrieval results, citations, redactions, and required evidence. Context Router consumes Knowledge Hub and Semantic Index results, but it is not a storage layer.

Relationship:

```text
Persistent Memory
↓ durable records and documents
Knowledge Hub
↓ canonical documents and governed retrieval
Semantic Index
↓ similarity candidates with citations
Context Router
↓ policy-filtered context bundle
Agent / Model / Runtime
```

## Architecture Guardrails

- Agents request capabilities; they do not call MCPs, providers, APIs, databases, or shell directly.
- Skills use tools; tools use provider/MCP/API adapters.
- OpenCode, Claude Code, Codex CLI, Cursor, IDEs, Web UI, and API are runtime/interface adapters.
- LangGraph, MetaGPT, and AutoGen can be optional workflow/agent orchestration adapters or references, not the core dependency.
- PostgreSQL, pgvector, Ollama, and tree-sitter are valid local-first adapters, not mandatory assumptions.
- Every loop needs a stop condition.
- Every implementation needs an approved Spec.
- Every external side effect needs Guardian/policy evaluation.
- Every material architectural boundary change should produce a Spec update or ADR.

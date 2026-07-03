# Open Questions

## Purpose

This document lists architectural questions that should be answered before the next significant implementation wave.

Questions are grouped by decision area. Each unresolved item should become an ADR, Spec update, or explicit project decision when it affects implementation.

## Core Boundaries

1. Is Guardian Engine the concrete Policy Engine for the current phase, or should Policy Engine be a separate component that delegates to Guardian Engine?
2. Where is policy precedence resolved: Guardian Engine, Policy Engine, Mission Runner, or a dedicated resolver?
3. Should Mission Orchestrator be implemented as a separate module before expanding Mission Runner?
4. What is the exact boundary between Mission Runner and Mission Orchestrator?
5. What is the exact boundary between Workflow Engine and Task Queue?
6. Should Workflow Engine always use Task Queue, or can it retain a direct sequential executor for simple local workflows?
7. What component owns re-planning after validation failure?
8. What component owns final mission closure and validation evidence aggregation?

## SDD Lifecycle

1. What counts as an approved Spec for implementation?
2. Where is Spec approval recorded?
3. Can documentation-only missions proceed without an approved feature Spec?
4. What minimum Plan artifact is required before Tasks are created?
5. What minimum Task artifact is required before implementation starts?
6. What validations are mandatory before a task can be marked done?
7. What validations are mandatory before a mission can be marked done?
8. What metadata must be included in a commit created by the framework?
9. Should auto-commit remain disabled globally unless explicitly enabled per mission?
10. How should failed validation loop back into Plan or Tasks?

## Memory And Context

1. What is the formal difference between persistent memory, Knowledge Hub, Semantic Index, and Context Router?
2. Should Context Router be a new top-level module?
3. What is the minimal Context Router request and response contract?
4. What policies can exclude context from a prompt?
5. How should context redaction be represented in audit logs?
6. How should citations be preserved from retrieval to final agent output?
7. What should be stored permanently versus recomputed from canonical documents?
8. What retention policy applies to conversations, prompts, logs, and decisions?
9. Should conversation history be part of Knowledge Hub by default or opt-in?
10. How should sensitive knowledge be indexed without exposing secrets?

## Knowledge Hub And Semantic Index

1. What are the first canonical document types beyond Markdown?
2. Should PDF/DOCX/PPTX support wait for separate adapter specs?
3. What chunking strategy should be used for semantic indexes?
4. What metadata is mandatory for every indexed chunk?
5. What is the first embedding provider adapter contract?
6. Is `nomic-embed-text` the initial local default only when detected, or a documented recommended adapter?
7. Is pgvector the first vector store adapter or only the current environment target?
8. How should semantic indexes be invalidated when canonical documents change?
9. What is the fallback when embeddings are unavailable?
10. How should Code Intelligence share or separate indexes from Knowledge Hub?

## Agents And Capabilities

1. What is the minimum agent profile schema for real use?
2. How are agent profiles approved, versioned, and stored?
3. Can agents request multiple capabilities in one task, or must capabilities be resolved one at a time?
4. What component decides whether to delegate to subagents?
5. What is the maximum delegation depth?
6. What is the default stop condition for agent loops?
7. What capabilities are essential for the first end-to-end implementation path?
8. What capabilities require human approval?
9. How are agent outputs validated before becoming task outputs?
10. How is agent confidence represented without letting the model self-certify completion?

## Skills, Tools, Providers, And MCPs

1. What is the first approved capability catalog?
2. What is the first approved skill catalog?
3. What local tools are allowed in the initial safe profile?
4. What effects must every tool declare?
5. How should tool permissions map to Guardian decisions?
6. Where do MCP adapters live: tools, providers, runtime, or a distinct adapter package?
7. What is the safety review process for an MCP server?
8. Can a tool call a runtime adapter, or should runtimes remain separate from provider/tool execution?
9. What provider operations are allowed in dry-run only?
10. How should provider fallback be audited?

## Runtime Adapters

1. What is the formal RuntimeAdapter conformance contract?
2. What capabilities must every runtime adapter report?
3. What does model discovery mean across OpenCode, Claude Code, Codex CLI, IDEs, Web UI, and API?
4. How should runtime-specific features be represented without leaking into core?
5. Should Claude Code and Codex CLI be treated identically to OpenCode at the adapter level?
6. How should runtimes without headless execution be supported?
7. How should interactive approval be represented across CLI, Web UI, and IDEs?
8. How should runtime logs be normalized?
9. What runtime failures are retryable?
10. Can one mission switch runtime mid-execution?

## External Frameworks

1. Should LangGraph be used as a workflow backend, a reference, or not at all?
2. Should MetaGPT be used as an agent organization reference, an adapter, or not at all?
3. Should AutoGen be used as a multi-agent conversation backend, an adapter, or not at all?
4. What dependency footprint is acceptable for optional framework adapters?
5. Can external frameworks satisfy Vercosa audit and policy requirements without invasive wrappers?
6. How are external framework states mapped to Vercosa mission/workflow/task states?
7. How are external framework tool calls forced through Vercosa capabilities/skills/tools?
8. What features from external frameworks should influence Vercosa design without being copied?
9. What disqualifies an external framework from core use?
10. Should external framework adapters live outside the core package?

## Persistence And Audit

1. What stores are required for the first integrated MVP?
2. What data must be persisted for mission recovery after crash?
3. What data must never be persisted in cleartext?
4. What is the audit log schema?
5. What is the retention policy for audit logs?
6. Should filesystem persistence remain the default until database adapters mature?
7. What is the first database adapter: SQLite, PostgreSQL, or both?
8. How are migrations represented and validated?
9. How are record hashes computed across adapters?
10. How are backups and restores handled without leaking secrets?

## Security And Governance

1. What is the default Guardian mode for local development?
2. What is the default Guardian mode for automation or daemon execution?
3. What commands are blocked across all operating systems?
4. What commands require approval across all operating systems?
5. How are false-positive secret detections approved without exposing values?
6. What policy controls network access?
7. What policy controls paid provider access?
8. What policy controls external provider access with project context?
9. How are policy exceptions approved, scoped, and expired?
10. What governance records are required before changing architecture?

## Model Selection

1. Where is Model Registry persisted?
2. What is the minimal Model Profile schema for the next phase?
3. How are OpenCode-discovered models merged with configured provider models?
4. How should model cost be represented when providers do not expose accurate cost?
5. What qualifies as `small_model`?
6. How should model fallback be audited?
7. Can a model decision expire?
8. When is cross-review mandatory?
9. How does Model Selection consume Context Router estimates?
10. How are local-only privacy policies enforced across model selection and runtime execution?

## Recommended ADRs

Create ADRs for these decisions before new code if possible:

- Policy Engine versus Guardian Engine boundary.
- Mission Runner versus Mission Orchestrator boundary.
- Context Router and memory architecture.
- Knowledge Hub versus Semantic Index boundary.
- Runtime Adapter conformance model.
- External framework positioning for LangGraph, MetaGPT, and AutoGen.
- MCP adapter placement and safety review process.
- Persistence adapter order: filesystem, SQLite, PostgreSQL.

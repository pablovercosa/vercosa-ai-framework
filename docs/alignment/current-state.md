# Current State

## Purpose

This document records the architectural state of the Vercosa AI Framework before the next implementation wave.

The checkpoint is documentation-only. It does not approve new code, new runtime behavior, global configuration changes, privileged operations, or feature expansion.

## What The Framework Is

The Vercosa AI Framework is an open source framework for specification-driven software development assisted by AI.

Its central purpose is to organize software engineering around missions, specs, workflows, policies, agents, capabilities, knowledge, validation, auditability, and provider-agnostic adapters.

The framework is intended to be:

- Specification First: specs are the source of truth for implementation.
- AI Native: AI participates across planning, implementation, review, validation, documentation, and learning.
- Provider Agnostic: models, providers, runtimes, vector stores, IDEs, APIs, MCPs, and databases are replaceable adapters.
- Local First: local execution must be possible when capabilities exist, without making local infrastructure mandatory.
- Extensible by Design: every concrete mechanism must sit behind contracts or adapters.
- Security by Design: Guardian Specs and Guardian Engine decisions constrain execution.
- Token Efficient: context should be selected, compressed, referenced, or retrieved instead of redundantly sent.
- Governance by Design: decisions, criteria, policies, validations, risks, and logs must be explicit.

## What The Framework Is Not

The framework is not:

- an IDE;
- an MCP server;
- a single agent;
- an OpenCode wrapper;
- a Claude Code wrapper;
- a Codex CLI wrapper;
- a LangGraph, MetaGPT, or AutoGen distribution;
- a PostgreSQL-only product;
- an Ollama-only product;
- an ARM64-specific project;
- a prompt collection;
- a runtime-specific automation script;
- a replacement for specs, validation, security review, or human approval where policy requires them.

OpenCode is currently the initial runtime and laboratory. It is not the architectural center.

## Repository State

The repository is in foundation/MVP phase.

Existing high-level assets:

- `AGENTS.md`: central operating context and architectural rules for agents.
- `README.md`: public project summary and current foundation status.
- `knowledge/`: vision, principles, and core architecture notes.
- `specs/framework/`: framework specs 0001 through 0013.
- `docs/`: MVP documentation for implemented or partially implemented components.
- `src/vercosa_ai_framework/`: provider-agnostic Python skeleton and MVP components.

## Specs State

Framework specs currently define the architecture more broadly than the code implements.

Current specs:

- `0001-framework-foundation.md`: approved conceptually; defines project identity, principles, Guardian Specs, OpenCode as initial runtime, Knowledge Hub, Canonicalizer, AI orchestration, model selection, agents, skills, MCPs, policies, loops, and missions.
- `0002-model-selection-engine.md`: proposed; defines model selection as policy-driven and provider-agnostic.
- `0003-opencode-runtime-adapter.md`: proposed; defines OpenCode as a runtime adapter, not the core.
- `0004-mission-runner.md`: proposed; defines mission lifecycle, queue, cycles, logs, validation, budgets, and future API/systemd modes.
- `0005-guardian-engine.md`: proposed; defines policy decisions, risk classification, security gates, token/cost limits, and command controls.
- `0006-workflow-engine.md`: proposed; defines workflows, task decomposition, dependencies, execution order, validation, and replan boundaries.
- `0007-task-queue.md`: proposed; defines task state, dependencies, attempts, retries, deterministic scheduling, and queue behavior.
- `0008-agent-orchestrator.md`: proposed; defines agent and subagent selection without direct provider/tool/MCP coupling.
- `0009-capabilities-skills-tools.md`: proposed; defines the chain from capabilities to skills to tools to providers/MCPs/APIs.
- `0010-provider-gateway.md`: proposed; defines the governed boundary between tools and concrete providers.
- `0011-knowledge-hub.md`: proposed; defines canonical documents, semantic indexes, sources, retrieval, and governance.
- `0012-canonicalizer.md`: proposed; defines conversion to canonical Markdown and guarded normalization.
- `0013-persistence-layer.md`: proposed; defines persistence ports, adapters, deterministic records, retention, and future database adapters.

## Implemented MVP Modules

The current `src/vercosa_ai_framework/` package contains MVP implementations and contracts for these areas:

- `core/`: shared domain primitives and policy enums.
- `cli.py`: `vaf` CLI for version/status, mission checks, mission execution, worker execution, workflow status, workflow validation, and workflow dry-run/run.
- `missions/`: mission types, directory-backed mission queue, and mission runner.
- `workflows/`: workflow types and sequential workflow engine.
- `tasks/`: task types, task queue, deterministic scheduler, attempts, and state transitions.
- `guardian/`: deterministic Guardian Engine MVP with structured decisions.
- `model_selection/`: policy, request/decision types, and selector MVP.
- `runtime/`: provider-neutral runtime adapter contract and OpenCode runtime adapter MVP.
- `agents/`: agent profiles, registry, and orchestrator MVP.
- `capabilities/`: capability profiles, registry, and resolver.
- `skills/`: skill profiles, registry, and executor.
- `tools/`: tool profiles, registry, and executor.
- `providers/`: provider profiles, registry, adapter contract, and provider gateway.
- `knowledge/`: Markdown ingestion, knowledge document types, in-memory store, and deterministic text search.
- `canonicalizer/`: canonicalization types, engine, Markdown/text adapter, hashes, redaction warnings, and conversion toward Knowledge Hub documents.
- `persistence/`: persistence types, repository contract, and local filesystem repository MVP.

## Current Module Responsibilities

`missions/` owns mission lifecycle at the operational level. It registers, queues, selects, executes, validates, and completes or fails missions. It should not decide architecture, choose models directly, call concrete providers directly, or bypass Guardian decisions.

`workflows/` owns decomposition execution at workflow/task level. The MVP executes tasks sequentially, respects dependencies, consults Guardian before task execution, and delegates concrete execution to a runtime adapter.

`tasks/` owns task state, deterministic eligibility, dependency tracking, attempts, retries, and sequential scheduling. It is not the agent layer and should not execute concrete tools directly.

`guardian/` owns policy evaluation. It returns structured `allow`, `warn`, `block`, or `require_approval` decisions. It is not a runtime, tool executor, model selector, or secret scanner replacement.

`model_selection/` owns model decision contracts and selection logic. It should receive policy and model catalog information, then emit auditable model decisions. It should not be embedded inside runtime adapters or agents.

`runtime/` owns the execution boundary to concrete runtimes. The OpenCode adapter translates governed runtime requests into OpenCode CLI invocation while avoiding global config mutation and privileged execution.

`agents/` owns agent profile selection and agent execution request preparation. It should not call providers, MCPs, tools, databases, or subprocesses directly.

`capabilities/` owns resolution from abstract requested capability to compatible skills.

`skills/` owns reusable procedure execution by preparing authorized tool execution requests.

`tools/` owns governed tool execution and the abstract boundary to concrete tool adapters.

`providers/` owns provider registry and provider gateway behavior after tools delegate concrete effects. It should remain side-effect-free unless an approved adapter is injected.

`knowledge/` owns local Markdown ingestion and deterministic search for the current MVP. It does not yet implement embeddings, pgvector, PostgreSQL, semantic chunking, or context routing.

`canonicalizer/` owns conversion of textual inputs into canonical Markdown-like documents with deterministic hashes and metadata. It is the entry point before Knowledge Hub ingestion for supported formats.

`persistence/` owns repository contracts and deterministic local filesystem persistence. It is not yet the final database, migration, backup, encryption, or pgvector layer.

`cli.py` is an interface layer. It should not become the core orchestration engine.

## Current Execution Chain

The desired architecture is:

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

The current MVP execution chain is narrower:

```text
CLI or Python caller
↓
Mission Runner or Workflow Engine
↓
Guardian Engine
↓
Runtime Adapter
↓
OpenCode adapter in dry-run or controlled execution mode
```

The capabilities/skills/tools/provider chain exists as MVP contracts and governed execution pieces, but it is not yet fully integrated into the whole mission-to-agent loop.

## Current Documentation State

Existing MVP docs describe implemented boundaries for:

- Mission Runner;
- Workflow Engine;
- Task Queue;
- Agent Orchestrator;
- Guardian Engine;
- OpenCode Runtime Adapter;
- Capabilities, Skills, and Tools;
- Provider Gateway;
- Knowledge Hub;
- Canonicalizer;
- Persistence Layer;
- CLI;
- development setup.

This alignment checkpoint adds cross-cutting architectural orientation across those docs.

## Important Gaps

The project still lacks final alignment or implementation for:

- Mission Orchestrator as a distinct layer from Mission Runner.
- Formal Policy Engine boundary relative to Guardian Engine.
- End-to-end Mission -> Workflow -> Task Queue -> Agent Orchestrator -> Capability -> Skill -> Tool -> Provider flow.
- Context Router as a first-class module.
- Semantic Index implementation with embeddings.
- PostgreSQL/pgvector adapter for Knowledge Hub and Code Intelligence.
- Runtime adapter contract parity for Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI, and API.
- Formal model registry persistence.
- Formal audit log persistence and retention policy.
- Contract tests across ports/adapters.
- ADRs for boundary decisions that are still ambiguous.

## Risk Of Continuing Without Alignment

Continuing implementation without alignment risks:

- turning OpenCode into the accidental core;
- letting agents call providers, MCPs, tools, or databases directly;
- duplicating policy logic across Guardian, runtime, CLI, tools, and providers;
- mixing Mission Runner, Mission Orchestrator, Workflow Engine, and Task Queue responsibilities;
- building memory, Knowledge Hub, semantic indexes, and context routing as one blurred subsystem;
- hardcoding PostgreSQL, Ollama, pgvector, ARM64, or a specific model provider;
- adding LangGraph, MetaGPT, AutoGen, or MCPs as dependencies instead of optional adapters/capabilities;
- losing traceability from Spec to Plan to Tasks to Implementation to Validation to Commit;
- increasing token cost through repeated broad context loading;
- creating security gaps around secrets, tools, external providers, and runtime permissions.

## Alignment Recommendation

Before new implementation, freeze architectural vocabulary and choose the next block deliberately.

Recommended immediate focus:

- keep source changes blocked unless a specific approved Spec authorizes them;
- resolve the Policy Engine versus Guardian Engine boundary;
- define Context Router and Semantic Index contracts before implementing advanced memory;
- define Mission Orchestrator boundaries before expanding Mission Runner;
- integrate existing MVPs through contracts before adding external orchestration frameworks;
- write ADRs for external framework positioning and memory architecture if decisions remain contested.

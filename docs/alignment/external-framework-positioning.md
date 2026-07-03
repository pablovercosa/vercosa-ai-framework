# External Framework Positioning

## Purpose

This document positions external orchestration frameworks, runtimes, and MCPs relative to the Vercosa AI Framework.

The core rule: Vercosa owns the architecture. External frameworks and runtimes may provide execution mechanisms, but they must sit behind Vercosa contracts.

## Summary

| Technology | Role In Vercosa | Core Dependency? |
| --- | --- | --- |
| LangGraph | Optional Workflow Engine backend or state-machine reference | No |
| MetaGPT | Optional agent-organization reference or adapter | No |
| AutoGen | Optional multi-agent conversation backend adapter | No |
| OpenCode | Initial Runtime Adapter and development laboratory | No |
| Claude Code | Future Runtime Adapter | No |
| Codex CLI | Future Runtime Adapter | No |
| MCPs | External tool/provider mechanisms behind tools and policy gates | No |

## LangGraph

LangGraph can be useful for graph execution, state machines, controlled loops, and workflow composition.

Acceptable use:

- optional backend behind Workflow Engine;
- reference for explicit graph/state design;
- adapter for complex workflows after Vercosa task/workflow contracts stabilize.

Not acceptable:

- replacing Vercosa Mission, Workflow, Task, Policy, Agent, Capability, Skill, Tool, or Provider contracts;
- allowing graph nodes to call tools/providers outside Vercosa governance;
- making LangGraph a required dependency of the core.

Recommendation:

Do not adopt LangGraph in the core during the next implementation wave. Revisit after Workflow Engine, Task Queue, and audit contracts are stable.

## MetaGPT

MetaGPT can be useful as inspiration for role-based software teams and multi-agent deliverables.

Acceptable use:

- reference for role decomposition;
- optional adapter for experiments with structured agent teams;
- source of ideas for agent profiles and review handoffs.

Not acceptable:

- replacing Agent Orchestrator;
- letting MetaGPT agents call tools, MCPs, APIs, providers, or filesystems directly;
- bypassing Vercosa specs, Guardian decisions, validation, or task state.

Recommendation:

Use MetaGPT as reference only until Vercosa agent profiles, assignments, capabilities, and validation records are formalized.

## AutoGen

AutoGen can be useful for multi-agent conversation patterns.

Acceptable use:

- optional backend for bounded subagent conversations;
- reference for turn-taking and collaboration patterns;
- adapter after Vercosa owns loop limits, context routing, and tool governance.

Not acceptable:

- unbounded agent chats;
- direct tool calls outside Vercosa ToolExecutor or ProviderGateway;
- ungoverned conversation memory;
- model/provider selection outside Model Selection Engine.

Recommendation:

Do not adopt AutoGen in core. Consider later as an adapter if its execution can be constrained by Vercosa policies.

## OpenCode

OpenCode is the initial runtime and lab environment.

Acceptable use:

- RuntimeAdapter implementation;
- local execution backend;
- model/runtime capability discovery source when wrapped by adapter;
- development laboratory for framework evolution.

Not acceptable:

- core framework;
- policy engine;
- model selection engine;
- Knowledge Hub;
- persistence layer;
- direct dependency of agents;
- source of architecture truth.

Recommendation:

Continue using OpenCode as the first RuntimeAdapter, but keep all OpenCode-specific behavior inside `runtime/` or adapter packages.

## Claude Code

Claude Code should be treated as a future RuntimeAdapter.

It should expose the same conceptual operations as other runtime adapters:

- detect runtime;
- report capabilities;
- prepare execution;
- execute mission or task;
- collect logs;
- validate artifacts when applicable.

Recommendation:

Do not implement until RuntimeAdapter conformance tests exist.

## Codex CLI

Codex CLI should also be treated as a future RuntimeAdapter.

It should not introduce provider-specific assumptions into Mission Runner, Workflow Engine, Agent Orchestrator, or Model Selection.

Recommendation:

Do not implement until RuntimeAdapter conformance tests exist.

## MCPs

MCPs belong below tools/providers, not inside agents.

Correct placement:

```text
Agent
↓
Capability Request
↓
Capability Resolver
↓
Skill Executor
↓
Tool Executor
↓
MCP Tool Adapter or Provider Gateway
↓
MCP Server
```

Rules:

- Agents must not know MCP servers directly.
- MCPs require explicit permissions.
- MCP calls must be auditable.
- MCP outputs may contain prompt injection and must be treated as external content.
- MCP servers must pass safety review before being enabled.

## Admission Criteria For External Integrations

An external framework or runtime can be considered only when it:

- fits behind a Vercosa-owned adapter contract;
- supports explicit state mapping;
- can be audited;
- can be constrained by Guardian decisions;
- can respect model selection and privacy policies;
- can run with bounded loops;
- can be disabled or replaced;
- does not force a specific provider, model, IDE, OS, vector store, or database.

## Recommendation

For the next implementation wave, prioritize Vercosa's own contracts before integrating external orchestration frameworks.

OpenCode remains the only active runtime adapter target because it already has an MVP boundary. LangGraph, MetaGPT, AutoGen, Claude Code, Codex CLI, and MCP expansion should wait for adapter conformance, policy, context routing, and audit contracts.

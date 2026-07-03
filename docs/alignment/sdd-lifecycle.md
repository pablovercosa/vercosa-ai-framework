# SDD Lifecycle

## Purpose

This document defines the desired Specification-Driven Development lifecycle for the Vercosa AI Framework.

Target lifecycle:

```text
Spec → Plan → Tasks → Implement → Validate → Commit
```

The lifecycle is intended to make AI-assisted development reproducible, auditable, policy-governed, and provider-agnostic.

## Lifecycle Principles

- Specs are the source of truth.
- Implementation does not start without an approved Spec.
- Plans explain how a Spec will be satisfied before code changes begin.
- Tasks are bounded, traceable units of execution.
- Implementation occurs through governed agents, capabilities, skills, tools, and runtime adapters.
- Validation is mandatory before completion.
- Commits are evidence-bearing checkpoints, not automatic side effects by default.
- Every loop has a stop condition.
- Every external side effect is policy-evaluated.

## Stage 1: Spec

Purpose:

Define the problem, scope, constraints, policy requirements, acceptance criteria, and boundaries.

Inputs:

- user mission;
- existing specs;
- Guardian Specs;
- ADRs;
- project context;
- relevant knowledge documents.

Required outputs:

- Spec reference;
- status;
- objective;
- scope;
- non-scope;
- architectural decisions or decision candidates;
- acceptance criteria;
- security, privacy, cost, token, quality, and validation constraints;
- pending questions.

Approval rule:

Implementation requires an approved Spec. Documentation-only alignment work can proceed when the mission explicitly restricts changes to documentation and does not create features or source changes.

Framework implication:

Mission Runner or Guardian Engine should block implementation missions without an approved Spec reference.

## Stage 2: Plan

Purpose:

Translate the Spec into an execution approach without changing implementation artifacts yet.

Inputs:

- approved Spec;
- architecture map;
- affected modules;
- dependency and risk analysis;
- available runtime and provider capabilities;
- Context Router output when implemented.

Required outputs:

- implementation strategy;
- affected files/modules;
- expected tasks;
- validation strategy;
- risk classification;
- required approvals;
- model/provider policy request;
- stop conditions;
- rollback or manual review strategy.

Owner:

Mission Orchestrator should own workflow choice. Workflow Engine should own workflow plan structure. Agent Orchestrator should not invent the full plan independently.

Guardrails:

- The plan should prefer smallest correct changes.
- The plan should not add providers, MCPs, frameworks, databases, or runtime assumptions unless the Spec requires them.
- The plan should identify whether an ADR is needed before implementation.

## Stage 3: Tasks

Purpose:

Break the plan into bounded, ordered, validated work units.

Inputs:

- plan;
- workflow policy;
- dependency graph;
- risk and validation requirements;
- available agents/capabilities.

Required outputs:

- task IDs;
- task goals;
- dependencies;
- required capabilities;
- acceptance criteria per task;
- allowed paths;
- denied paths;
- execution limits;
- validation requirements;
- expected artifacts.

Owner:

Workflow Engine should produce or normalize task structure. Task Queue should own task state, dependency eligibility, attempts, retries, and scheduling.

Guardrails:

- Tasks should be small enough to validate independently.
- Dependencies should be explicit.
- Parallelism should remain disabled until artifact locks and policy exist.
- Each task should know when it is done or failed.

## Stage 4: Implement

Purpose:

Execute tasks through governed framework boundaries.

Inputs:

- task;
- agent profile;
- capability request;
- policy decisions;
- context bundle;
- model decision;
- runtime/tool permissions.

Expected execution path:

```text
Task Queue
↓
Agent Orchestrator
↓
Agent or Subagent
↓
Capability Request
↓
Capability Resolver
↓
Skill Executor
↓
Tool Executor
↓
Provider Gateway or Runtime Adapter
↓
Concrete provider, MCP, API, runtime, or filesystem adapter
```

Current MVP path may be simpler:

```text
Mission Runner or Workflow Engine
↓
Guardian Engine
↓
Runtime Adapter
↓
OpenCode adapter or fake adapter
```

Implementation rules:

- Do not bypass Guardian decisions.
- Do not call providers or MCPs directly from agents.
- Do not mutate global config unless explicitly approved by policy and Spec.
- Do not use `sudo` by default.
- Do not expose secrets to logs, prompts, commits, or external providers.
- Do not hardcode provider, model, database, runtime, IDE, OS, or architecture.
- Do not continue loops without finite limits.

## Stage 5: Validate

Purpose:

Prove that task and mission outputs satisfy the Spec, plan, task criteria, Guardian Specs, and quality requirements.

Validation sources:

- automated tests;
- syntax checks;
- lint/static analysis;
- type checks;
- architectural review;
- security review;
- documentation review;
- acceptance criteria checks;
- artifact existence checks;
- human approval;
- cross-review by another agent/model when policy requires it.

Required outputs:

- validation result;
- commands or checks run;
- pass/fail status;
- warnings;
- skipped validations and reasons;
- policy decisions referenced;
- artifacts validated;
- residual risks.

Rules:

- A task should not be marked done without applicable validation or a recorded policy-approved reason.
- A mission should not be marked done until required tasks and deliverables are validated.
- Failure should route to replan, retry, manual review, or mission failure according to policy.
- Critical validation should not rely only on the same agent that performed implementation.

## Stage 6: Commit

Purpose:

Create a version-control checkpoint after validation.

Default policy:

Auto-commit is disabled unless explicitly authorized.

Commit prerequisites:

- approved Spec reference;
- completed plan/tasks;
- validation evidence;
- reviewed changed files;
- no unrelated user changes included;
- no secrets;
- no generated sensitive artifacts;
- commit policy permits it.

Commit metadata should include:

- mission ID;
- Spec references;
- summary of changes;
- validation performed;
- known limitations if any.

Rules:

- Do not commit changes outside the mission scope.
- Do not amend or rewrite history unless explicitly requested.
- Do not push automatically without separate policy and approval.
- Worktree ambiguity should block automatic commit or require manual review.

## Desired State Machine

Mission state:

```text
created
↓
spec_required or spec_approved
↓
planned
↓
tasks_ready
↓
running
↓
validating
↓
done | failed | cancelled | requires_review
```

Task state:

```text
pending
↓
eligible
↓
running
↓
validating
↓
done | failed | blocked | skipped | cancelled | requires_review
```

Agent loop state:

```text
IDLE
↓
PLANNING
↓
EXECUTING
↓
REFLECTING
↓
VALIDATING
↓
REPLANNING
↓
DONE
```

Every loop must include maximum cycles, retry limits, budget limits, and stop conditions.

## Mapping To Current MVP

Current repository support:

- Spec artifacts exist under `specs/framework/`.
- Mission Runner MVP supports queued/running/done/failed/cancelled style execution.
- Workflow Engine MVP supports sequential task execution and Guardian checks.
- Task Queue MVP supports task states, dependencies, attempts, retries, and deterministic scheduling.
- Guardian Engine MVP supports structured allow/warn/block/require_approval decisions.
- OpenCode Runtime Adapter MVP supports governed runtime execution and dry-run.
- CLI supports mission checks, run-one, worker, workflow status, validation, and workflow run/dry-run.

Missing or partial:

- formal Spec approval registry;
- formal Plan artifact;
- Mission Orchestrator layer;
- full Task Queue integration into Workflow Engine;
- full Agent Orchestrator integration into task execution;
- Context Router;
- persistent audit log integration;
- validation evidence store;
- commit governance automation;
- cross-review policy execution.

## Recommended Next SDD Improvement

Before implementing more features, define the minimal artifact schemas for:

- Spec approval record;
- Plan record;
- Task record;
- Validation result;
- Guardian decision reference;
- Model decision reference;
- Commit decision record.

These records should be persisted through the Persistence Layer rather than embedded only in CLI output or in-memory state.

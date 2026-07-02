# CLI

The `vaf` CLI exposes the first Mission Runner commands with no heavy runtime dependency in the command layer.

## Commands

```bash
vaf version
vaf status
vaf check-mission <file> [--guardian-mode standard]
vaf run-one [mission_id] [--dry-run] [--guardian-mode strict]
vaf run-worker [--dry-run] [--max-missions N] [--guardian-mode strict]
vaf workflow-status <workflow.json>
vaf workflow-validate <workflow.json> [--guardian-mode standard]
vaf workflow-run <workflow.json> [--dry-run] [--guardian-mode standard]
```

The legacy `vaf --version` and `vaf diagnose` commands remain supported.

## Queue Directory

Commands use `.vaf/missions` by default. Override it with `--queue-dir`:

```bash
vaf --queue-dir /path/to/missions status
```

The queue is backed by `DirectoryMissionQueue`, with one JSON file per mission.

## Status

`vaf status` prints framework version, queue counts by mission state, and declared OpenCode runtime capabilities.

It calls `OpenCodeRuntimeAdapter.detect_runtime()` only. It does not execute OpenCode and does not read global OpenCode configuration.

## Check Mission

`vaf check-mission <file>` validates a mission file with the Guardian Engine and prints the policy decision:

```bash
vaf check-mission mission.md
vaf check-mission mission.json --guardian-mode strict
```

JSON files are parsed as `Mission` records. Other files are treated as plain mission text. The command does not execute OpenCode, does not call external services, and exits with `1` when Guardian returns `block` or `require_approval`.

## Run One

`vaf run-one` selects the next queued mission. Passing a mission id runs that specific mission.

Use dry-run to inspect the command without changing mission state or executing OpenCode:

```bash
vaf run-one --dry-run
vaf run-one mission-id --dry-run --model provider/model --guardian-mode strict
```

Dry-run evaluates Guardian first, then prepares the adapter command only if the decision allows execution. Without `--dry-run`, the command delegates execution to `MissionRunner` with `GuardianEngine` injected before `OpenCodeRuntimeAdapter` can run.

## Run Worker

`vaf run-worker` processes queued missions sequentially. The MVP defaults to one mission per invocation:

```bash
vaf run-worker --max-missions 3
vaf run-worker --dry-run --max-missions 3 --guardian-mode strict
```

In dry-run mode, each selected mission is prepared without being started, completed, failed, or sent to real OpenCode.

## Workflow Status

`vaf workflow-status <workflow.json>` reads a local workflow file and prints its current state and task counts:

```bash
vaf workflow-status workflow.json
```

The command only reads the provided file. It does not execute a runtime and does not inspect global OpenCode configuration.

## Workflow Validate

`vaf workflow-validate <workflow.json>` validates the initial Workflow Engine file format, sequential dependency references, and Guardian policy for each task:

```bash
vaf workflow-validate workflow.json
vaf workflow-validate workflow.json --guardian-mode strict
```

It exits with `2` for malformed workflow files and `1` when Guardian blocks a task.

## Workflow Run

`vaf workflow-run <workflow.json>` executes tasks through the provider-neutral `WorkflowEngine` and the configured runtime adapter. Use `--dry-run` to prepare commands without executing OpenCode:

```bash
vaf workflow-run workflow.json --dry-run
vaf workflow-run workflow.json --dry-run --workspace /path/to/project
```

Dry-run evaluates Guardian first, then asks the runtime adapter to prepare each task command with `dry_run=True`. It does not call real OpenCode.

The structured MVP workflow file is JSON:

```json
{
  "workflow_id": "wf-example",
  "mission_id": "mission-example",
  "title": "Example workflow",
  "goal": "Prepare an auditable task",
  "tasks": [
    {
      "task_id": "task-example",
      "title": "Prepare",
      "goal": "Prepare task output",
      "acceptance_criteria": ["dry-run command is printed"],
      "inputs": {
        "planned_command": "opencode run Prepare task output"
      }
    }
  ]
}
```

Plain text files are also accepted as a simple one-task workflow. The file stem becomes the workflow id, mission id, title, and task title; the file content becomes the workflow and task goal.

The CLI intentionally avoids YAML or other heavier parsing dependencies in this MVP.

## Guardian Mode

Supported modes are `permissive`, `standard`, and `strict`. `run-one` and `run-worker` can override the mission mode for the current CLI invocation with `--guardian-mode` without mutating queued mission files.

## Security Notes

- The CLI does not use `sudo`.
- The CLI does not access global OpenCode configuration.
- Tests use dry-run or Guardian-blocked paths and do not execute real OpenCode.
- `--auto-approve` is explicit opt-in and is passed only to the runtime adapter.

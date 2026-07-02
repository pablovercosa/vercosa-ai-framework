# CLI

The `vaf` CLI exposes the first Mission Runner commands with no heavy runtime dependency in the command layer.

## Commands

```bash
vaf version
vaf status
vaf check-mission <file> [--guardian-mode standard]
vaf run-one [mission_id] [--dry-run] [--guardian-mode strict]
vaf run-worker [--dry-run] [--max-missions N] [--guardian-mode strict]
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

## Guardian Mode

Supported modes are `permissive`, `standard`, and `strict`. `run-one` and `run-worker` can override the mission mode for the current CLI invocation with `--guardian-mode` without mutating queued mission files.

## Security Notes

- The CLI does not use `sudo`.
- The CLI does not access global OpenCode configuration.
- Tests use dry-run or Guardian-blocked paths and do not execute real OpenCode.
- `--auto-approve` is explicit opt-in and is passed only to the runtime adapter.

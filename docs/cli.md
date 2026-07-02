# CLI

The `vaf` CLI exposes the first Mission Runner commands with no heavy runtime dependency in the command layer.

## Commands

```bash
vaf version
vaf status
vaf run-one [mission_id] [--dry-run]
vaf run-worker [--dry-run] [--max-missions N]
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

## Run One

`vaf run-one` selects the next queued mission. Passing a mission id runs that specific mission.

Use dry-run to inspect the command without changing mission state or executing OpenCode:

```bash
vaf run-one --dry-run
vaf run-one mission-id --dry-run --model provider/model
```

Without `--dry-run`, the command delegates execution to `MissionRunner` and `OpenCodeRuntimeAdapter`.

## Run Worker

`vaf run-worker` processes queued missions sequentially. The MVP defaults to one mission per invocation:

```bash
vaf run-worker --max-missions 3
vaf run-worker --dry-run --max-missions 3
```

In dry-run mode, each selected mission is prepared without being started, completed, failed, or sent to real OpenCode.

## Security Notes

- The CLI does not use `sudo`.
- The CLI does not access global OpenCode configuration.
- Tests use dry-run and do not execute real OpenCode.
- `--auto-approve` is explicit opt-in and is passed only to the runtime adapter.

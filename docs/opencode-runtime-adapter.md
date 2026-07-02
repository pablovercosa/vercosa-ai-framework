# OpenCode Runtime Adapter

The OpenCode Runtime Adapter is the first concrete runtime adapter for the Vercosa AI Framework. It translates a governed `RuntimeExecutionRequest` into an OpenCode CLI command while keeping framework core code independent from OpenCode internals and global user configuration.

## MVP Scope

- Build an OpenCode command using `opencode run`.
- Support `dry_run` so callers can inspect the command without executing OpenCode.
- Support `model` and `small_model` from either adapter options or the Model Selection decision.
- Support `auto_approve` as an explicit opt-in flag.
- Support `cwd` without changing process-global state.
- Capture `exit_code`, `stdout`, and `stderr` through a testable executor interface.
- Avoid `sudo`, shell expansion, global config mutation, and secret exposure in recorded metadata.

## Runtime Boundary

The adapter exposes `OpenCodeRuntimeAdapter`, which implements the provider-neutral `RuntimeAdapter` contract.

Process execution is isolated behind `CommandExecutor`. Production use defaults to `SubprocessCommandExecutor`, which calls `subprocess.run` with `shell=False`, `capture_output=True`, and `check=False`. Tests can inject a fake executor and must not invoke real OpenCode.

## Command Shape

The MVP command shape is:

```text
opencode run [--model MODEL] [--small-model SMALL_MODEL] [--auto-approve] [extra args...] PROMPT
```

The prompt comes from `request.context["prompt"]`, then `request.context["mission_goal"]`, then a minimal fallback containing the mission id.

Runtime options can be supplied at adapter construction time with `OpenCodeRunOptions` or per request under `request.context["opencode_options"]`.

## Security Notes

- The adapter never uses `sudo`; attempts to set `sudo` as executable or extra command part are blocked.
- The adapter does not read or modify global OpenCode configuration.
- The adapter does not expose environment variables in metadata.
- Secret-like command fragments such as `api_key=...`, `token=...`, `password=...`, and `secret=...` are redacted in recorded command strings and captured output metadata.
- `auto_approve` is disabled by default and should only be enabled after policy approval.

## Validation

Required checks for this MVP:

```bash
pytest
python3 -m compileall src
```

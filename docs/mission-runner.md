# Mission Runner

The Mission Runner MVP executes one queued mission at a time while keeping the framework core independent from concrete runtimes such as OpenCode.

## MVP Scope

- Register missions in `DirectoryMissionQueue`.
- Select one queued mission with `run_next()`.
- Move mission state through `queued -> running -> done` or `queued -> running -> failed`.
- Execute bounded cycles with an explicit `max_cycles` limit.
- Call a provider-neutral `RuntimeAdapter` through `RuntimeExecutionRequest`.
- Validate the mission with an injected Guardian Engine before runtime execution.
- Convert runtime output into `MissionResult`.
- Validate expected artifacts through the runtime adapter boundary.
- Support `auto_commit` through an injected `AutoCommitter` interface.
- Keep audit events and last mission results in memory for the MVP.

## Runtime Boundary

`MissionRunner` receives a `RuntimeAdapter` instance. It does not import or instantiate OpenCode, does not call subprocesses, and does not know runtime-specific CLI flags.

Before `execute_mission()` is called, the runner may consult an injected `GuardianEvaluator`. This keeps Guardian policy decisions outside the runtime adapter and prevents concrete runtimes from bypassing mission governance.

The request sent to the adapter contains:

- mission id;
- workspace;
- mission title and goal;
- spec references;
- acceptance criteria;
- current cycle number;
- effective cycle limit;
- mission security policy as permissions;
- mission execution limits.

## Cycle Limit

The runner resolves the effective mission limit from:

1. `mission.execution_limits["max_cycles_per_mission"]`;
2. `mission.execution_limits["max_cycles"]`;
3. `mission.max_cycles`.

If the effective value is lower than `1`, the mission fails safely. If all cycles are consumed without a terminal runtime result, the mission fails with `max cycle limit reached`.

## Guardian Gate

`MissionRunner` accepts an optional `guardian` implementing `evaluate(GuardianEvaluationContext) -> GuardianDecision`.

Supported modes are `permissive`, `standard`, and `strict`. The runner default is `standard`; a mission can override it with `Mission.guardian_mode`.

Decision handling:

- `allow`: execute the runtime normally;
- `warn`: execute the runtime normally and append Guardian warnings to `MissionResult.warnings`;
- `require_approval`: do not execute the runtime in non-interactive mode, fail the mission safely, and mark `requires_review=True`;
- `block`: do not execute the runtime and fail the mission safely.

The MVP does not implement an interactive approval flow. If approval is required, execution remains stopped until a future approval interface is defined.

## Validation

When `mission.validation_policy["expected_artifacts"]` is present, the runner asks the runtime adapter to validate those artifact references. Missing artifacts fail the mission.

When no expected artifacts are declared and the runtime returned `done`, the MVP records a minimal validation note: `runtime result accepted; no expected artifacts declared`.

## Auto-Commit

`auto_commit` is disabled by default.

Supported policies:

- `disabled`: no commit action;
- `after_validation`: call the injected `AutoCommitter` only after runtime success and validation success;
- `manual_approval_required`: do not commit and mark the result as requiring review.

The runner never executes git directly. If `after_validation` is requested without an injected committer, the mission fails safely.

## Testing Notes

Tests use fake runtime and commit implementations. They must not invoke real OpenCode or real git.

Required checks:

```bash
pytest
python3 -m compileall src
```

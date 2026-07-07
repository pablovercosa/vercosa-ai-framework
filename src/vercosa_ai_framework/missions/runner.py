"""Mission Runner MVP.

The runner coordinates queue state, bounded cycles, runtime execution,
validation, and optional commit integration without depending on a concrete
runtime such as OpenCode or executing git directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol

from vercosa_ai_framework.audit import (
    AuditEvent,
    EventLog,
    mission_completed_event,
    mission_failed_event,
    mission_queued_event,
    mission_started_event,
    record_mission_event,
)
from vercosa_ai_framework.guardian import (
    GuardianAction,
    GuardianDecision,
    GuardianEvaluationContext,
    GuardianMode,
)
from vercosa_ai_framework.missions.queue import DirectoryMissionQueue, MissionQueueError
from vercosa_ai_framework.missions.types import Mission, MissionResult, MissionStatus
from vercosa_ai_framework.runtime import RuntimeAdapter, RuntimeExecutionRequest, RuntimeStatus


class MissionRunnerError(RuntimeError):
    """Raised when the Mission Runner cannot complete a governed execution."""


@dataclass(frozen=True, slots=True)
class AutoCommitResult:
    """Result returned by an injected auto-commit implementation."""

    committed: bool
    summary: str = ""
    commit_ref: str | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)


class AutoCommitter(Protocol):
    """Testable boundary for commit integrations.

    Implementations may call git, but the Mission Runner core never does.
    """

    def commit(self, mission: Mission, result: MissionResult) -> AutoCommitResult:
        """Commit files produced by the mission after validation."""


class GuardianEvaluator(Protocol):
    """Testable boundary for Guardian Engine integrations."""

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        """Evaluate mission policy before runtime execution."""


class MissionRunner:
    """Execute one queued mission at a time through a Runtime Adapter."""

    def __init__(
        self,
        queue: DirectoryMissionQueue,
        runtime: RuntimeAdapter,
        *,
        auto_committer: AutoCommitter | None = None,
        guardian: GuardianEvaluator | None = None,
        guardian_mode: GuardianMode | str = GuardianMode.STANDARD,
        interactive: bool = False,
        runner_id: str = "mission-runner",
        event_log: EventLog | None = None,
    ) -> None:
        self.queue = queue
        self.runtime = runtime
        self.auto_committer = auto_committer
        self.guardian = guardian
        self.guardian_mode = GuardianMode(guardian_mode)
        self.interactive = interactive
        self.runner_id = runner_id
        self.event_log = event_log
        self.results: dict[str, MissionResult] = {}
        self.audit_log: list[str] = []

    def register(self, mission: Mission) -> Mission:
        """Register a mission in the queue."""

        queued = self.queue.enqueue(mission)
        self._log(queued.mission_id, "mission queued")
        self._record_event(mission_queued_event, queued)
        return queued

    def run_next(self) -> MissionResult | None:
        """Execute the next queued mission, if any."""

        mission = self.queue.next()
        if mission is None:
            return None
        return self.run(mission.mission_id)

    def run(self, mission_id: str) -> MissionResult:
        """Run one mission from queued to done or failed."""

        running = self.queue.start(mission_id, locked_by=self.runner_id)
        self._log(mission_id, "mission started")
        self._record_event(mission_started_event, running)

        try:
            guardian_decision = self._evaluate_guardian(running)
            if guardian_decision is not None:
                policy_result = self._result_from_guardian(running, guardian_decision)
                if policy_result is not None:
                    self.queue.fail(mission_id, self._error_summary(policy_result))
                    self._record_result(policy_result)
                    return policy_result

            max_cycles = self._max_cycles_for(running)
            if max_cycles < 1:
                return self._fail(running, "mission requires max_cycles >= 1")

            last_result = None
            for cycle_number in range(1, max_cycles + 1):
                running = self.queue.record_cycle(mission_id, cycle_number)
                self._log(mission_id, f"cycle {cycle_number} started")
                request = self._request_for(running, cycle_number, max_cycles)
                runtime_result = self.runtime.execute_mission(request)
                last_result = runtime_result
                self._log(mission_id, f"cycle {cycle_number} runtime status={runtime_result.status.value}")

                if runtime_result.status == RuntimeStatus.DONE:
                    result = self._result_from_runtime(running, MissionStatus.DONE, runtime_result)
                    result = self._apply_guardian_warnings(result, guardian_decision)
                    result = self._validate(running, result)
                    if result.status == MissionStatus.DONE:
                        result = self._auto_commit(running, result)
                    if result.status == MissionStatus.DONE:
                        self.queue.complete(mission_id)
                    else:
                        self.queue.fail(mission_id, self._error_summary(result))
                    self._record_result(result)
                    return result

                if runtime_result.status in {RuntimeStatus.FAILED, RuntimeStatus.STOPPED}:
                    result = self._result_from_runtime(running, MissionStatus.FAILED, runtime_result)
                    result = self._apply_guardian_warnings(result, guardian_decision)
                    self.queue.fail(mission_id, self._error_summary(result))
                    self._record_result(result)
                    return result

            error = f"max cycle limit reached: {max_cycles}"
            result = self._result_from_runtime(
                running,
                MissionStatus.FAILED,
                last_result,
                errors=(error,),
            )
            result = self._apply_guardian_warnings(result, guardian_decision)
            self.queue.fail(mission_id, error)
            self._record_result(result)
            return result
        except Exception as exc:
            try:
                self.queue.fail(mission_id, str(exc))
            except MissionQueueError:
                pass
            result = MissionResult(mission_id=mission_id, status=MissionStatus.FAILED, errors=(str(exc),))
            self._record_result(result)
            return result

    def _request_for(self, mission: Mission, cycle_number: int, max_cycles: int) -> RuntimeExecutionRequest:
        context = {
            "mission_title": mission.title,
            "mission_goal": mission.goal,
            "spec_refs": mission.spec_refs,
            "acceptance_criteria": mission.acceptance_criteria,
            "cycle_number": cycle_number,
            "max_cycles": max_cycles,
        }
        return RuntimeExecutionRequest(
            mission_id=mission.mission_id,
            workspace=mission.workspace,
            context=context,
            permissions=dict(mission.security_policy),
            execution_limits={**mission.execution_limits, "max_cycles": max_cycles},
            logging_policy={"sanitize_secrets": True},
            approval_policy=dict(mission.commit_policy),
        )

    def _evaluate_guardian(self, mission: Mission) -> GuardianDecision | None:
        if self.guardian is None:
            return None

        mode = GuardianMode(mission.guardian_mode or self.guardian_mode)
        context = GuardianEvaluationContext(
            mission_id=mission.mission_id,
            evaluation_type="mission_pre_execution",
            guardian_mode=mode,
            mission_goal=mission.goal,
            spec_refs=mission.spec_refs,
            guardian_refs=mission.guardian_refs,
            workspace=mission.workspace,
            requested_action=mission.title,
            target_paths=self._tuple_from(mission.constraints.get("target_paths", ())),
            data_sensitivity=mission.security_policy.get("data_sensitivity"),
            network_policy=dict(mission.security_policy.get("network_policy", {})),
            provider_policy=dict(mission.security_policy.get("provider_policy", {})),
            budget_policy=dict(mission.budget_policy),
            execution_limits=dict(mission.execution_limits),
            metadata={
                "acceptance_criteria": mission.acceptance_criteria,
                "deliverables": mission.validation_policy.get("expected_artifacts", ()),
                "requested_by": mission.requested_by,
            },
        )
        decision = self.guardian.evaluate(context)
        self._log(mission.mission_id, f"guardian decision={decision.decision.value} mode={decision.guardian_mode.value}")
        return decision

    def _tuple_from(self, value: object) -> tuple[str, ...]:
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(item) for item in value)

    def _result_from_guardian(self, mission: Mission, decision: GuardianDecision) -> MissionResult | None:
        if decision.decision == GuardianAction.ALLOW or decision.decision == GuardianAction.WARN:
            return None

        reason = self._guardian_reason(decision)
        if decision.decision == GuardianAction.REQUIRE_APPROVAL:
            error = f"guardian approval required: {reason}"
            if not self.interactive:
                return MissionResult(
                    mission_id=mission.mission_id,
                    status=MissionStatus.FAILED,
                    warnings=self._guardian_warnings(decision),
                    errors=(error,),
                    requires_review=True,
                )
        else:
            error = f"guardian blocked mission: {reason}"
            return MissionResult(
                mission_id=mission.mission_id,
                status=MissionStatus.FAILED,
                warnings=self._guardian_warnings(decision),
                errors=(error,),
            )

        return MissionResult(
            mission_id=mission.mission_id,
            status=MissionStatus.FAILED,
            warnings=self._guardian_warnings(decision),
            errors=("guardian approval flow is not implemented",),
            requires_review=True,
        )

    def _apply_guardian_warnings(self, result: MissionResult, decision: GuardianDecision | None) -> MissionResult:
        if decision is None or decision.decision != GuardianAction.WARN:
            return result
        warnings = (*result.warnings, *self._guardian_warnings(decision))
        return self._copy_result(result, warnings=warnings)

    def _guardian_warnings(self, decision: GuardianDecision) -> tuple[str, ...]:
        warnings = decision.warnings or decision.reasons
        return tuple(f"guardian warning: {warning}" for warning in warnings)

    def _guardian_reason(self, decision: GuardianDecision) -> str:
        parts = decision.reasons or decision.approval_requirements or decision.blocked_items or decision.required_actions
        return "; ".join(parts) or decision.decision.value

    def _validate(self, mission: Mission, result: MissionResult) -> MissionResult:
        expected = tuple(mission.validation_policy.get("expected_artifacts", ()))
        validation_results = list(result.validation_results)
        errors = list(result.errors)

        if expected:
            validated = self.runtime.validate_artifacts(mission.mission_id, expected)
            missing = tuple(artifact for artifact in expected if artifact not in validated)
            validation_results.append(f"validated artifacts: {len(validated)}")
            if missing:
                errors.append(f"missing expected artifacts: {', '.join(missing)}")
        elif not validation_results:
            validation_results.append("runtime result accepted; no expected artifacts declared")

        status = MissionStatus.FAILED if errors else MissionStatus.DONE
        return MissionResult(
            mission_id=result.mission_id,
            status=status,
            summary=result.summary,
            artifacts=result.artifacts,
            changed_files=result.changed_files,
            validation_results=tuple(validation_results),
            warnings=result.warnings,
            errors=tuple(errors),
            requires_review=result.requires_review,
            audit_log_ref=result.audit_log_ref,
        )

    def _auto_commit(self, mission: Mission, result: MissionResult) -> MissionResult:
        policy = mission.commit_policy.get("auto_commit", "disabled")
        if policy == "disabled":
            return result
        if policy == "manual_approval_required":
            return self._copy_result(
                result,
                warnings=(*result.warnings, "auto_commit requires manual approval"),
                requires_review=True,
            )
        if policy != "after_validation":
            return self._copy_result(
                result,
                status=MissionStatus.FAILED,
                errors=(*result.errors, f"unsupported auto_commit policy: {policy}"),
            )
        if self.auto_committer is None:
            return self._copy_result(
                result,
                status=MissionStatus.FAILED,
                errors=(*result.errors, "auto_commit requested but no committer configured"),
            )

        commit_result = self.auto_committer.commit(mission, result)
        warnings = (*result.warnings, *commit_result.warnings)
        if commit_result.committed:
            summary = result.summary
            if commit_result.commit_ref:
                summary = f"{summary} commit={commit_result.commit_ref}".strip()
            return self._copy_result(result, summary=summary, warnings=warnings)
        return self._copy_result(
            result,
            status=MissionStatus.FAILED,
            warnings=warnings,
            errors=(*result.errors, *commit_result.errors, commit_result.summary or "auto_commit failed"),
        )

    def _fail(self, mission: Mission, error: str) -> MissionResult:
        self.queue.fail(mission.mission_id, error)
        result = MissionResult(mission_id=mission.mission_id, status=MissionStatus.FAILED, errors=(error,))
        self._record_result(result)
        return result

    def _result_from_runtime(
        self,
        mission: Mission,
        status: MissionStatus,
        runtime_result: object | None,
        *,
        errors: tuple[str, ...] = (),
    ) -> MissionResult:
        if runtime_result is None:
            return MissionResult(mission_id=mission.mission_id, status=status, errors=errors)
        return MissionResult(
            mission_id=mission.mission_id,
            status=status,
            summary=getattr(runtime_result, "metadata", {}).get("summary", ""),
            artifacts=tuple(getattr(runtime_result, "artifacts", ())),
            changed_files=tuple(getattr(runtime_result, "changed_files", ())),
            validation_results=tuple(getattr(runtime_result, "validation_results", ())),
            warnings=tuple(getattr(runtime_result, "warnings", ())),
            errors=(*tuple(getattr(runtime_result, "errors", ())), *errors),
            requires_review=bool(getattr(runtime_result, "requires_review", False)),
            audit_log_ref=getattr(runtime_result, "audit_log_ref", None),
        )

    def _max_cycles_for(self, mission: Mission) -> int:
        value = mission.execution_limits.get("max_cycles_per_mission")
        if value is None:
            value = mission.execution_limits.get("max_cycles", mission.max_cycles)
        return int(value)

    def _record_result(self, result: MissionResult) -> None:
        self.results[result.mission_id] = result
        self._log(result.mission_id, f"result status={result.status.value}")
        if result.status == MissionStatus.DONE:
            event_factory = mission_completed_event
        elif result.status == MissionStatus.FAILED:
            event_factory = mission_failed_event
        else:
            return
        self._record_event(event_factory, self.queue.get(result.mission_id), result=result)

    def _copy_result(self, result: MissionResult, **changes: object) -> MissionResult:
        data = {
            "mission_id": result.mission_id,
            "status": result.status,
            "summary": result.summary,
            "artifacts": result.artifacts,
            "changed_files": result.changed_files,
            "validation_results": result.validation_results,
            "warnings": result.warnings,
            "errors": result.errors,
            "requires_review": result.requires_review,
            "audit_log_ref": result.audit_log_ref,
        }
        data.update(changes)
        return MissionResult(**data)

    def _error_summary(self, result: MissionResult) -> str:
        return "; ".join(result.errors) or "mission failed"

    def _log(self, mission_id: str, message: str) -> None:
        self.audit_log.append(f"mission={mission_id} {message}")

    def _record_event(
        self,
        event_factory: Callable[..., AuditEvent],
        mission: Mission,
        *,
        result: MissionResult | None = None,
    ) -> None:
        if self.event_log is None:
            return
        metadata = {
            "mission_id": mission.mission_id,
            "mission_name": mission.title,
            "commit_hash": self._commit_hash_from_result(result),
        }
        event = event_factory(metadata=metadata)
        record_mission_event(event, event_log=self.event_log)

    def _commit_hash_from_result(self, result: MissionResult | None) -> str | None:
        if result is None or "commit=" not in result.summary:
            return None
        return result.summary.rsplit("commit=", maxsplit=1)[-1].split(maxsplit=1)[0]


__all__ = [
    "AutoCommitResult",
    "AutoCommitter",
    "GuardianEvaluator",
    "MissionRunner",
    "MissionRunnerError",
]

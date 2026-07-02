"""OpenCode Runtime Adapter MVP.

The adapter builds a concrete OpenCode command while keeping subprocess usage
behind an injectable executor so tests and higher layers do not invoke OpenCode
directly.
"""

from __future__ import annotations

import subprocess
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from vercosa_ai_framework.model_selection import ModelProfile
from vercosa_ai_framework.runtime.adapter import RuntimeAdapter
from vercosa_ai_framework.runtime.types import (
    RuntimeCapability,
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
    RuntimeStatus,
)


RUNTIME_ID = "opencode"


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Captured process result returned by a command executor."""

    exit_code: int
    stdout: str = ""
    stderr: str = ""


class CommandExecutor(Protocol):
    """Testable boundary around process execution."""

    def run(self, command: Sequence[str], cwd: str | None = None) -> CommandResult:
        """Run a command and capture exit code, stdout, and stderr."""


class SubprocessCommandExecutor:
    """Command executor backed by subprocess without shell expansion."""

    def run(self, command: Sequence[str], cwd: str | None = None) -> CommandResult:
        completed = subprocess.run(
            list(command),
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
        return CommandResult(
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )


@dataclass(frozen=True, slots=True)
class OpenCodeRunOptions:
    """Execution options specific to the OpenCode CLI adapter."""

    executable: str = "opencode"
    dry_run: bool = False
    model: str | None = None
    small_model: str | None = None
    auto_approve: bool = False
    cwd: str | None = None
    extra_args: tuple[str, ...] = field(default_factory=tuple)


class OpenCodeRuntimeAdapter(RuntimeAdapter):
    """Runtime adapter that translates governed requests to OpenCode CLI calls."""

    def __init__(
        self,
        executor: CommandExecutor | None = None,
        options: OpenCodeRunOptions | None = None,
    ) -> None:
        self.executor = executor or SubprocessCommandExecutor()
        self.options = options or OpenCodeRunOptions()
        self._logs: list[str] = []

    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        """Return declared MVP capabilities without reading global configs."""

        return RuntimeInfo(
            runtime_id=RUNTIME_ID,
            runtime_name="OpenCode",
            available=True,
            capabilities=(
                RuntimeCapability("headless_run", metadata={"command": self.options.executable}),
                RuntimeCapability("dry_run"),
                RuntimeCapability("model"),
                RuntimeCapability("small_model"),
                RuntimeCapability("auto_approve", limitations=("policy_controlled",)),
                RuntimeCapability("cwd"),
            ),
            limitations=(
                "MVP does not inspect global OpenCode configuration",
                "MVP does not discover models from OpenCode",
            ),
            security_warnings=("auto_approve must not be used for sensitive actions",),
        )

    def list_models(self) -> tuple[ModelProfile, ...]:
        """Model discovery is intentionally deferred to the Model Registry."""

        return ()

    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        """Prepare a command plan without executing OpenCode."""

        options = self._options_for(request)
        blocked_reasons = self._validate_options(options)
        selected_provider = None
        selected_model = options.model
        if request.selection_decision is not None:
            selected_provider = request.selection_decision.selected_provider
            selected_model = options.model or request.selection_decision.selected_model.id

        approvals_required: tuple[str, ...] = ()
        if not options.auto_approve:
            approvals_required = ("human_approval",)

        context_included = tuple(sorted(str(key) for key in request.context.keys()))
        return RuntimeExecutionPlan(
            mission_id=request.mission_id,
            workspace=request.workspace,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            selected_provider=selected_provider,
            selected_model=selected_model,
            context_included=context_included,
            permissions_granted=dict(request.permissions),
            plugins_allowed=tuple(request.plugin_policy.get("allowed_plugins", ())),
            limits_applied=dict(request.execution_limits),
            approvals_required=approvals_required,
            blocked_reasons=blocked_reasons,
        )

    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        """Execute or dry-run an OpenCode mission command."""

        return self._execute(request)

    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        """Execute or dry-run an OpenCode task command."""

        return self._execute(request)

    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        """Return sanitized in-memory log events for this MVP."""

        prefix = f"mission={mission_id}"
        if task_id is not None:
            prefix = f"{prefix} task={task_id}"
        return tuple(log for log in self._logs if log.startswith(prefix))

    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        """Report a safe stop request for synchronous MVP executions."""

        self._logs.append(f"mission={mission_id} task={task_id} stopped")
        return RuntimeExecutionResult(
            mission_id=mission_id,
            runtime_id=RUNTIME_ID,
            status=RuntimeStatus.STOPPED,
            task_id=task_id,
            warnings=("No long-running OpenCode process is tracked by the MVP adapter",),
        )

    def validate_artifacts(
        self, mission_id: str, expected_artifacts: Iterable[str]
    ) -> tuple[str, ...]:
        """Return expected artifact references for higher-level validation."""

        artifacts = tuple(expected_artifacts)
        self._logs.append(f"mission={mission_id} validate_artifacts count={len(artifacts)}")
        return artifacts

    def build_command(self, request: RuntimeExecutionRequest) -> tuple[str, ...]:
        """Build the OpenCode CLI command for a governed request."""

        options = self._options_for(request)
        blocked_reasons = self._validate_options(options)
        if blocked_reasons:
            msg = "; ".join(blocked_reasons)
            raise ValueError(msg)

        prompt = self._prompt_for(request)
        command = [options.executable, "run"]
        model = options.model
        if model is None and request.selection_decision is not None:
            model = request.selection_decision.selected_model.id
        small_model = options.small_model
        if small_model is None and request.selection_decision is not None:
            small_model_profile = request.selection_decision.small_model
            small_model = small_model_profile.id if small_model_profile is not None else None

        if model:
            command.extend(("--model", model))
        if small_model:
            command.extend(("--small-model", small_model))
        if options.auto_approve:
            command.append("--auto-approve")
        command.extend(options.extra_args)
        command.append(prompt)
        return tuple(command)

    def _execute(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        options = self._options_for(request)
        plan = self.prepare_execution(request)
        if plan.blocked_reasons:
            return self._result(
                request,
                plan,
                RuntimeStatus.FAILED,
                errors=plan.blocked_reasons,
                metadata={"exit_code": None},
            )

        command = self.build_command(request)
        sanitized_command = self._sanitize_command(command)
        metadata = {"command": sanitized_command, "cwd": self._cwd_for(request, options)}
        if options.dry_run:
            metadata.update({"dry_run": True, "exit_code": 0, "stdout": "", "stderr": ""})
            self._logs.append(f"mission={request.mission_id} task={request.task_id} dry_run command={sanitized_command}")
            return self._result(request, plan, RuntimeStatus.PREPARED, metadata=metadata)

        process = self.executor.run(command, cwd=metadata["cwd"])
        metadata.update(
            {
                "dry_run": False,
                "exit_code": process.exit_code,
                "stdout": self._sanitize_text(process.stdout),
                "stderr": self._sanitize_text(process.stderr),
            }
        )
        status = RuntimeStatus.DONE if process.exit_code == 0 else RuntimeStatus.FAILED
        errors = () if process.exit_code == 0 else (metadata["stderr"] or "OpenCode exited with failure",)
        self._logs.append(
            f"mission={request.mission_id} task={request.task_id} exit_code={process.exit_code} command={sanitized_command}"
        )
        return self._result(request, plan, status, errors=errors, metadata=metadata)

    def _result(
        self,
        request: RuntimeExecutionRequest,
        plan: RuntimeExecutionPlan,
        status: RuntimeStatus,
        errors: tuple[str, ...] = (),
        metadata: dict[str, object] | None = None,
    ) -> RuntimeExecutionResult:
        return RuntimeExecutionResult(
            mission_id=request.mission_id,
            runtime_id=RUNTIME_ID,
            status=status,
            workflow_id=request.workflow_id,
            task_id=request.task_id,
            selected_provider=plan.selected_provider,
            selected_model=plan.selected_model,
            small_model_used=self._small_model_used(request),
            commands_executed=(metadata.get("command"),) if metadata and metadata.get("command") else (),
            warnings=(),
            errors=errors,
            requires_review=request.selection_decision.requires_review if request.selection_decision else False,
            audit_log_ref=f"memory://opencode/{request.mission_id}",
            metadata=metadata or {},
        )

    def _options_for(self, request: RuntimeExecutionRequest) -> OpenCodeRunOptions:
        runtime_options = request.context.get("opencode_options", {})
        if not isinstance(runtime_options, dict):
            runtime_options = {}

        return OpenCodeRunOptions(
            executable=str(runtime_options.get("executable", self.options.executable)),
            dry_run=bool(runtime_options.get("dry_run", self.options.dry_run)),
            model=runtime_options.get("model", self.options.model),
            small_model=runtime_options.get("small_model", self.options.small_model),
            auto_approve=bool(runtime_options.get("auto_approve", self.options.auto_approve)),
            cwd=runtime_options.get("cwd", self.options.cwd),
            extra_args=tuple(runtime_options.get("extra_args", self.options.extra_args)),
        )

    def _prompt_for(self, request: RuntimeExecutionRequest) -> str:
        prompt = request.context.get("prompt") or request.context.get("mission_goal")
        if prompt is None:
            prompt = f"Execute mission {request.mission_id}"
        return str(prompt)

    def _cwd_for(self, request: RuntimeExecutionRequest, options: OpenCodeRunOptions) -> str:
        cwd = options.cwd or request.workspace
        return str(Path(cwd))

    def _validate_options(self, options: OpenCodeRunOptions) -> tuple[str, ...]:
        blocked: list[str] = []
        command_parts = (options.executable, *options.extra_args)
        if any(part == "sudo" or part.startswith("sudo ") for part in command_parts):
            blocked.append("sudo is not allowed by the OpenCode Runtime Adapter")
        return tuple(blocked)

    def _small_model_used(self, request: RuntimeExecutionRequest) -> bool:
        options = self._options_for(request)
        return bool(options.small_model or (request.selection_decision and request.selection_decision.small_model))

    def _sanitize_command(self, command: Sequence[str]) -> str:
        return " ".join(self._sanitize_text(part) for part in command)

    def _sanitize_text(self, value: object) -> str:
        text = str(value)
        redacted = text
        for marker in ("token=", "api_key=", "apikey=", "password=", "secret="):
            lower = redacted.lower()
            index = lower.find(marker)
            while index != -1:
                end = redacted.find(" ", index)
                if end == -1:
                    end = len(redacted)
                redacted = f"{redacted[:index]}{marker}<redacted>{redacted[end:]}"
                lower = redacted.lower()
                index = lower.find(marker, index + len(marker) + len("<redacted>"))
        return redacted


__all__ = [
    "CommandExecutor",
    "CommandResult",
    "OpenCodeRunOptions",
    "OpenCodeRuntimeAdapter",
    "SubprocessCommandExecutor",
]

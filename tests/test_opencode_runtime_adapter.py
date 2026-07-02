from __future__ import annotations

from collections.abc import Sequence

import pytest

from vercosa_ai_framework.model_selection import ModelProfile, SelectionDecision
from vercosa_ai_framework.runtime import RuntimeExecutionRequest, RuntimeStatus
from vercosa_ai_framework.runtime.opencode import (
    CommandResult,
    OpenCodeRunOptions,
    OpenCodeRuntimeAdapter,
)


class RecordingExecutor:
    def __init__(self, result: CommandResult | None = None) -> None:
        self.result = result or CommandResult(exit_code=0, stdout="ok", stderr="")
        self.calls: list[tuple[tuple[str, ...], str | None]] = []

    def run(self, command: Sequence[str], cwd: str | None = None) -> CommandResult:
        self.calls.append((tuple(command), cwd))
        return self.result


def selection_decision() -> SelectionDecision:
    selected = ModelProfile(id="openai/gpt-5.1", provider="openai", runtime="opencode")
    small = ModelProfile(
        id="openai/gpt-5.1-mini",
        provider="openai",
        runtime="opencode",
        small=True,
    )
    return SelectionDecision(selected_model=selected, small_model=small)


def test_builds_opencode_command_with_models_auto_approve_and_cwd():
    adapter = OpenCodeRuntimeAdapter(
        options=OpenCodeRunOptions(
            dry_run=True,
            model="anthropic/claude-sonnet-4",
            small_model="openai/gpt-5.1-mini",
            auto_approve=True,
            cwd="/tmp/workspace",
        )
    )
    request = RuntimeExecutionRequest(
        mission_id="m-1",
        workspace="/workspace",
        context={"prompt": "Implement approved spec"},
    )

    command = adapter.build_command(request)

    assert command == (
        "opencode",
        "run",
        "--model",
        "anthropic/claude-sonnet-4",
        "--small-model",
        "openai/gpt-5.1-mini",
        "--auto-approve",
        "Implement approved spec",
    )


def test_dry_run_does_not_execute_opencode():
    executor = RecordingExecutor()
    adapter = OpenCodeRuntimeAdapter(executor=executor, options=OpenCodeRunOptions(dry_run=True))
    request = RuntimeExecutionRequest(
        mission_id="m-2",
        workspace="/workspace",
        context={"prompt": "Dry run only"},
        selection_decision=selection_decision(),
    )

    result = adapter.execute_mission(request)

    assert executor.calls == []
    assert result.status == RuntimeStatus.PREPARED
    assert result.metadata["dry_run"] is True
    assert result.metadata["exit_code"] == 0
    assert "opencode run" in result.commands_executed[0]
    assert result.selected_model == "openai/gpt-5.1"
    assert result.small_model_used is True


def test_executes_through_injected_executor_and_captures_output():
    executor = RecordingExecutor(CommandResult(exit_code=7, stdout="partial", stderr="failed"))
    adapter = OpenCodeRuntimeAdapter(executor=executor, options=OpenCodeRunOptions(cwd="/tmp/project"))
    request = RuntimeExecutionRequest(
        mission_id="m-3",
        workspace="/workspace",
        task_id="t-1",
        context={"prompt": "Run task"},
    )

    result = adapter.execute_task(request)

    assert executor.calls == [(("opencode", "run", "Run task"), "/tmp/project")]
    assert result.status == RuntimeStatus.FAILED
    assert result.metadata["exit_code"] == 7
    assert result.metadata["stdout"] == "partial"
    assert result.metadata["stderr"] == "failed"
    assert result.errors == ("failed",)


def test_request_context_can_override_runtime_options():
    adapter = OpenCodeRuntimeAdapter(options=OpenCodeRunOptions(dry_run=False, model="base-model"))
    request = RuntimeExecutionRequest(
        mission_id="m-4",
        workspace="/workspace",
        context={
            "prompt": "Override",
            "opencode_options": {
                "dry_run": True,
                "model": "override-model",
                "small_model": "override-small",
                "auto_approve": True,
            },
        },
    )

    result = adapter.execute_mission(request)

    assert result.status == RuntimeStatus.PREPARED
    assert "--model override-model" in result.commands_executed[0]
    assert "--small-model override-small" in result.commands_executed[0]
    assert "--auto-approve" in result.commands_executed[0]


def test_blocks_sudo_and_redacts_secret_like_values():
    adapter = OpenCodeRuntimeAdapter(
        options=OpenCodeRunOptions(
            dry_run=True,
            extra_args=("--metadata", "api_key=super-secret"),
        )
    )
    request = RuntimeExecutionRequest(
        mission_id="m-5",
        workspace="/workspace",
        context={"prompt": "Do not leak"},
    )

    result = adapter.execute_mission(request)

    assert "super-secret" not in result.commands_executed[0]
    assert "api_key=<redacted>" in result.commands_executed[0]

    blocked = OpenCodeRuntimeAdapter(options=OpenCodeRunOptions(executable="sudo"))
    with pytest.raises(ValueError, match="sudo is not allowed"):
        blocked.build_command(request)


def test_detect_runtime_declares_mvp_capabilities_without_global_config_dependency():
    adapter = OpenCodeRuntimeAdapter()

    info = adapter.detect_runtime("/workspace")

    assert info.runtime_id == "opencode"
    assert info.available is True
    assert {capability.name for capability in info.capabilities} >= {
        "dry_run",
        "model",
        "small_model",
        "auto_approve",
        "cwd",
    }
    assert any("global OpenCode configuration" in item for item in info.limitations)

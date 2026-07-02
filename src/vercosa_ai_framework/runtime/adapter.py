"""Abstract Runtime Adapter contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from vercosa_ai_framework.model_selection import ModelProfile
from vercosa_ai_framework.runtime.types import (
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
)


class RuntimeAdapter(ABC):
    """Provider-agnostic interface implemented by concrete runtimes."""

    @abstractmethod
    def detect_runtime(self, workspace: str) -> RuntimeInfo:
        """Detect runtime presence, version, capabilities, and limitations."""

    @abstractmethod
    def list_models(self) -> tuple[ModelProfile, ...]:
        """Return models exposed by this runtime without selecting one."""

    @abstractmethod
    def prepare_execution(self, request: RuntimeExecutionRequest) -> RuntimeExecutionPlan:
        """Prepare a governed execution plan without running the mission."""

    @abstractmethod
    def execute_mission(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        """Execute a governed mission through the concrete runtime."""

    @abstractmethod
    def execute_task(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        """Execute one governed mission task through the concrete runtime."""

    @abstractmethod
    def collect_logs(self, mission_id: str, task_id: str | None = None) -> tuple[str, ...]:
        """Collect sanitized log references or events for audit."""

    @abstractmethod
    def stop_execution(self, mission_id: str, task_id: str | None = None) -> RuntimeExecutionResult:
        """Request safe stop for an in-flight execution."""

    @abstractmethod
    def validate_artifacts(
        self, mission_id: str, expected_artifacts: Iterable[str]
    ) -> tuple[str, ...]:
        """Validate expected artifact presence or references."""

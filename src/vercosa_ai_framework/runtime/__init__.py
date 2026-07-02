"""Runtime Adapter public contracts."""

from vercosa_ai_framework.runtime.adapter import RuntimeAdapter
from vercosa_ai_framework.runtime.opencode import (
    CommandExecutor,
    CommandResult,
    OpenCodeRunOptions,
    OpenCodeRuntimeAdapter,
    SubprocessCommandExecutor,
)
from vercosa_ai_framework.runtime.types import (
    RuntimeCapability,
    RuntimeExecutionPlan,
    RuntimeExecutionRequest,
    RuntimeExecutionResult,
    RuntimeInfo,
    RuntimeStatus,
)

__all__ = [
    "CommandExecutor",
    "CommandResult",
    "OpenCodeRunOptions",
    "OpenCodeRuntimeAdapter",
    "RuntimeAdapter",
    "RuntimeCapability",
    "RuntimeExecutionPlan",
    "RuntimeExecutionRequest",
    "RuntimeExecutionResult",
    "RuntimeInfo",
    "RuntimeStatus",
    "SubprocessCommandExecutor",
]

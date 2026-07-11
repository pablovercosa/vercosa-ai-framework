"""Mission Runner to Workflow Engine integration contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from vercosa_ai_framework.missions.types import Mission
from vercosa_ai_framework.workflows import Workflow, WorkflowEngine, WorkflowResult


class MissionWorkflowProvider(Protocol):
    """Resolve a normalized Mission into a deterministic Workflow."""

    def resolve(self, mission: Mission) -> Workflow:
        """Return a workflow for the mission or raise a clear local error."""


class MissionWorkflowExecutor(Protocol):
    """Execute a resolved Workflow and return a normalized WorkflowResult."""

    def execute(self, workflow: Workflow) -> WorkflowResult:
        """Execute the workflow without changing Mission Runner state."""


@dataclass(frozen=True, slots=True)
class InMemoryWorkflowProvider:
    """Deterministic local provider used by tests and examples."""

    workflows: dict[str, Workflow]

    def resolve(self, mission: Mission) -> Workflow:
        try:
            workflow = self.workflows[mission.mission_id]
        except KeyError as exc:
            raise ValueError(f"no workflow configured for mission: {mission.mission_id}") from exc
        if workflow.mission_id != mission.mission_id:
            raise ValueError(
                f"workflow mission_id mismatch: mission={mission.mission_id} workflow={workflow.mission_id}"
            )
        return workflow


@dataclass(frozen=True, slots=True)
class QueueBackedWorkflowExecutor:
    """Adapter that makes WorkflowEngine.execute_with_queue injectable."""

    engine: WorkflowEngine

    def execute(self, workflow: Workflow) -> WorkflowResult:
        return self.engine.execute_with_queue(workflow)


__all__ = [
    "InMemoryWorkflowProvider",
    "MissionWorkflowExecutor",
    "MissionWorkflowProvider",
    "QueueBackedWorkflowExecutor",
]

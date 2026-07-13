"""Agent Orchestrator public contracts."""

from vercosa_ai_framework.agents.registry import AgentRegistry, AgentRegistryError
from vercosa_ai_framework.agents.orchestrator import AgentOrchestrator, AgentOrchestratorError, NoCompatibleAgentError
from vercosa_ai_framework.agents.task_executor import AgentTaskExecutor, agent_result_to_task_outcome
from vercosa_ai_framework.agents.types import (
    AgentCapabilityRequest,
    AgentExecutionRequest,
    AgentExecutionResult,
    AgentMode,
    AgentProfile,
    AgentRole,
    AgentState,
)

__all__ = [
    "AgentCapabilityRequest",
    "AgentExecutionRequest",
    "AgentExecutionResult",
    "AgentMode",
    "AgentOrchestrator",
    "AgentOrchestratorError",
    "AgentProfile",
    "AgentRegistry",
    "AgentRegistryError",
    "AgentRole",
    "AgentState",
    "AgentTaskExecutor",
    "NoCompatibleAgentError",
    "agent_result_to_task_outcome",
]

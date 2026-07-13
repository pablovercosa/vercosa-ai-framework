"""Task Scheduler to Agent Orchestrator execution bridge."""

from __future__ import annotations

from dataclasses import dataclass

from vercosa_ai_framework.agents.orchestrator import AgentOrchestrator
from vercosa_ai_framework.agents.types import AgentExecutionResult
from vercosa_ai_framework.tasks import Task, TaskAttempt, TaskExecutionOutcome, TaskQueueState


@dataclass(frozen=True, slots=True)
class AgentTaskExecutor:
    """Adapt Agent Orchestrator results to Task Scheduler outcomes.

    The bridge is the only explicit coupling point for the integrated path. It
    does not select agents, resolve capabilities, execute skills, or decide
    queue retries.
    """

    orchestrator: AgentOrchestrator

    def __call__(self, task: Task, attempt: TaskAttempt) -> TaskExecutionOutcome:
        result = self.orchestrator.execute_task(task, attempt)
        return agent_result_to_task_outcome(task, result)


def agent_result_to_task_outcome(task: Task, result: AgentExecutionResult) -> TaskExecutionOutcome:
    """Normalize an AgentExecutionResult for Task Scheduler consumption."""

    metadata = {
        "agent_assignment_ref": result.agent_assignment_id,
        "agent_profile_id": result.agent_profile_id,
        "agent_execution_result": {
            "state": result.state.value,
            "success": result.success,
            "evidence_refs": result.evidence_refs,
            "validation_results": result.validation_results,
            "warnings": result.warnings,
            "errors": result.errors,
            "capability_resolutions": result.metadata.get("capability_resolutions", ()),
            "capability_executions": result.metadata.get("capability_executions", ()),
            "policy_resolution_id": result.metadata.get("policy_resolution_id"),
            "matched_policy_refs": result.metadata.get("matched_policy_refs", ()),
            "context_package_id": result.metadata.get("context_package_id"),
            "context_request_id": result.metadata.get("context_request_id"),
            "estimated_context_tokens": result.metadata.get("estimated_context_tokens"),
            "reserved_output_tokens": result.metadata.get("reserved_output_tokens"),
            "selected_model_id": result.metadata.get("selected_model_id"),
            "guardian_decision_refs": result.metadata.get("guardian_decision_refs", ()),
            "audit_event_refs": result.metadata.get("audit_event_refs", ()),
            "runtime_result_ref": result.runtime_result_ref,
        },
    }
    if result.success:
        return TaskExecutionOutcome(
            status=TaskQueueState.DONE,
            artifact_refs=result.artifact_refs,
            retryable=False,
            agent_assignment_ref=result.agent_assignment_id,
            runtime_result_ref=result.runtime_result_ref,
            audit_log_ref=result.audit_log_ref,
            metadata=metadata,
        )

    error_message = "; ".join(result.errors) if result.errors else "agent assignment failed"
    return TaskExecutionOutcome(
        status=TaskQueueState.FAILED,
        error_message=error_message,
        retryable=_agent_failure_retryable(task),
        agent_assignment_ref=result.agent_assignment_id,
        runtime_result_ref=result.runtime_result_ref,
        audit_log_ref=result.audit_log_ref,
        metadata=metadata,
    )


def _agent_failure_retryable(task: Task) -> bool:
    retry_policy = task.metadata.get("retry_policy")
    if not isinstance(retry_policy, dict):
        return False
    return bool(retry_policy.get("retryable_agent_failures", False))


__all__ = ["AgentTaskExecutor", "agent_result_to_task_outcome"]

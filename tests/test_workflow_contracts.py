from __future__ import annotations

from dataclasses import asdict

from vercosa_ai_framework.workflows import (
    TaskDependency,
    TaskResult,
    TaskStatus,
    Workflow,
    WorkflowResult,
    WorkflowStatus,
    WorkflowTask,
)


def test_workflow_statuses_match_spec_0006():
    assert {status.value for status in WorkflowStatus} == {
        "draft",
        "ready",
        "running",
        "paused",
        "replanning",
        "done",
        "failed",
        "cancelled",
    }


def test_task_statuses_match_spec_0006():
    assert {status.value for status in TaskStatus} == {
        "pending",
        "ready",
        "running",
        "blocked",
        "validating",
        "done",
        "failed",
        "skipped",
        "cancelled",
    }


def test_workflow_task_captures_traceability_policy_and_dependencies():
    dependency = TaskDependency(
        dependency_type="requires_completion",
        target_ref="task-setup",
        reason="Implementation starts after planning is validated.",
    )
    task = WorkflowTask(
        task_id="task-impl",
        workflow_id="wf-1",
        mission_id="mission-1",
        title="Implement contracts",
        goal="Create initial Workflow Engine contracts",
        task_type="implementation",
        expected_outputs=("src/vercosa_ai_framework/workflows/types.py",),
        acceptance_criteria=("pytest passes", "compileall passes"),
        dependencies=(dependency,),
        required_capabilities=("python_contract_design",),
        model_policy={"role": "developer", "model": "auto", "provider": "auto"},
    )

    assert task.status == TaskStatus.PENDING
    assert task.dependencies[0].required is True
    assert task.retry_policy == {"max_attempts": 1}
    assert task.model_policy["model"] == "auto"
    assert asdict(task)["dependencies"][0]["target_ref"] == "task-setup"


def test_workflow_defaults_are_sequential_and_provider_agnostic():
    task = WorkflowTask(
        task_id="task-validate",
        workflow_id="wf-1",
        mission_id="mission-1",
        title="Validate",
        goal="Run local validations",
        acceptance_criteria=("local validation completed",),
    )
    workflow = Workflow(
        workflow_id="wf-1",
        mission_id="mission-1",
        title="Workflow Engine MVP",
        goal="Plan initial workflow contracts",
        spec_refs=("specs/framework/0006-workflow-engine.md",),
        tasks=(task,),
    )

    assert workflow.status == WorkflowStatus.DRAFT
    assert workflow.execution_mode == "sequential"
    assert workflow.execution_limits == {"max_parallel_tasks": 1}
    assert workflow.tasks[0].workflow_id == workflow.workflow_id
    assert "opencode" not in asdict(workflow)


def test_status_helpers_return_copies_without_mutating_originals():
    workflow = Workflow(mission_id="mission-1", title="Plan", goal="Create a plan")
    task = WorkflowTask(
        workflow_id=workflow.workflow_id,
        mission_id="mission-1",
        title="Task",
        goal="Do traceable work",
    )

    ready_workflow = workflow.with_status(WorkflowStatus.READY)
    ready_task = task.with_status(TaskStatus.READY, blocked_by=())

    assert workflow.status == WorkflowStatus.DRAFT
    assert ready_workflow.status == WorkflowStatus.READY
    assert task.status == TaskStatus.PENDING
    assert ready_task.status == TaskStatus.READY


def test_task_and_workflow_results_are_auditable_without_runtime_execution():
    task_result = TaskResult(
        task_id="task-1",
        workflow_id="wf-1",
        mission_id="mission-1",
        status=TaskStatus.DONE,
        artifacts=("src/vercosa_ai_framework/workflows/types.py",),
        validation_results=("pytest passed",),
    )
    workflow_result = WorkflowResult(
        workflow_id="wf-1",
        mission_id="mission-1",
        status=WorkflowStatus.DONE,
        task_results=(task_result,),
        closure_recommendation="conclude",
    )

    assert workflow_result.task_results[0].status == TaskStatus.DONE
    assert workflow_result.closure_recommendation == "conclude"
    assert workflow_result.errors == ()

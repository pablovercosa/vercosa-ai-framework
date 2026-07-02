"""Command line interface for the Vercosa AI Framework."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

from vercosa_ai_framework import __version__
from vercosa_ai_framework.guardian import GuardianDecision, GuardianEngine, GuardianEvaluationContext, GuardianMode
from vercosa_ai_framework.missions import DirectoryMissionQueue, Mission, MissionResult, MissionRunner, MissionStatus
from vercosa_ai_framework.runtime import OpenCodeRunOptions, OpenCodeRuntimeAdapter, RuntimeExecutionRequest
from vercosa_ai_framework.workflows import (
    TaskDependency,
    TaskStatus,
    Workflow,
    WorkflowEngine,
    WorkflowResult,
    WorkflowStatus,
    WorkflowTask,
)


DEFAULT_QUEUE_DIR = ".vaf/missions"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser without binding it to a runtime provider."""
    parser = argparse.ArgumentParser(
        prog="vaf",
        description="Vercosa AI Framework command line interface.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the framework version and exit.",
    )
    parser.add_argument(
        "--queue-dir",
        default=DEFAULT_QUEUE_DIR,
        help=f"Mission queue directory. Defaults to {DEFAULT_QUEUE_DIR}.",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("diagnose", help="Print basic local environment diagnostics.")
    subparsers.add_parser("version", help="Print the framework version and exit.")

    status = subparsers.add_parser("status", help="Print Mission Runner and runtime status.")
    status.add_argument("--workspace", default=".", help="Workspace used for runtime detection.")

    check_mission = subparsers.add_parser("check-mission", help="Validate a mission file with the Guardian Engine.")
    check_mission.add_argument("file", help="Mission file to validate. JSON Mission files and plain text are supported.")
    check_mission.add_argument(
        "--guardian-mode",
        choices=[mode.value for mode in GuardianMode],
        default=GuardianMode.STANDARD.value,
        help="Guardian mode used for validation. Defaults to standard.",
    )

    run_one = subparsers.add_parser("run-one", help="Run one queued mission.")
    run_one.add_argument("mission_id", nargs="?", help="Mission id. Defaults to the next queued mission.")
    run_one.add_argument("--workspace", help="Override the mission workspace.")
    run_one.add_argument("--dry-run", action="store_true", help="Prepare the OpenCode command without executing it.")
    run_one.add_argument(
        "--guardian-mode",
        choices=[mode.value for mode in GuardianMode],
        help="Override Guardian mode for this execution.",
    )
    run_one.add_argument("--model", help="OpenCode model id.")
    run_one.add_argument("--small-model", help="OpenCode small model id.")
    run_one.add_argument("--auto-approve", action="store_true", help="Pass --auto-approve to OpenCode.")

    run_worker = subparsers.add_parser("run-worker", help="Run queued missions sequentially.")
    run_worker.add_argument("--workspace", help="Override each mission workspace.")
    run_worker.add_argument("--dry-run", action="store_true", help="Prepare commands without executing missions.")
    run_worker.add_argument("--max-missions", type=int, default=1, help="Maximum missions to process. Defaults to 1.")
    run_worker.add_argument(
        "--guardian-mode",
        choices=[mode.value for mode in GuardianMode],
        help="Override Guardian mode for each execution.",
    )
    run_worker.add_argument("--model", help="OpenCode model id.")
    run_worker.add_argument("--small-model", help="OpenCode small model id.")
    run_worker.add_argument("--auto-approve", action="store_true", help="Pass --auto-approve to OpenCode.")

    workflow_status = subparsers.add_parser("workflow-status", help="Print status for a workflow file.")
    workflow_status.add_argument("file", help="Workflow JSON file to inspect.")

    workflow_validate = subparsers.add_parser("workflow-validate", help="Validate a workflow file.")
    workflow_validate.add_argument("file", help="Workflow JSON file to validate.")
    workflow_validate.add_argument(
        "--guardian-mode",
        choices=[mode.value for mode in GuardianMode],
        default=GuardianMode.STANDARD.value,
        help="Guardian mode used for task validation. Defaults to standard.",
    )

    workflow_run = subparsers.add_parser("workflow-run", help="Run a workflow file through the Workflow Engine.")
    workflow_run.add_argument("file", help="Workflow JSON file to run.")
    workflow_run.add_argument("--workspace", default=".", help="Workspace used for task execution. Defaults to current directory.")
    workflow_run.add_argument("--dry-run", action="store_true", help="Prepare task commands without executing OpenCode.")
    workflow_run.add_argument(
        "--guardian-mode",
        choices=[mode.value for mode in GuardianMode],
        default=GuardianMode.STANDARD.value,
        help="Guardian mode used for task execution. Defaults to standard.",
    )
    workflow_run.add_argument("--model", help="OpenCode model id.")
    workflow_run.add_argument("--small-model", help="OpenCode small model id.")
    workflow_run.add_argument("--auto-approve", action="store_true", help="Pass --auto-approve to OpenCode.")
    return parser


def run(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version or args.command == "version":
        print(f"vercosa-ai-framework {__version__}")
        return 0

    if args.command == "diagnose":
        print(f"vercosa-ai-framework: {__version__}")
        print(f"python: {platform.python_version()}")
        print(f"system: {platform.system() or 'unknown'}")
        print(f"machine: {platform.machine() or 'unknown'}")
        return 0

    if args.command == "status":
        return _print_status(args.queue_dir, args.workspace)

    if args.command == "check-mission":
        return _check_mission(args.file, args.guardian_mode)

    if args.command == "run-one":
        return _run_one(args)

    if args.command == "run-worker":
        return _run_worker(args)

    if args.command == "workflow-status":
        return _workflow_status(args.file)

    if args.command == "workflow-validate":
        return _workflow_validate(args.file, args.guardian_mode)

    if args.command == "workflow-run":
        return _workflow_run(args)

    parser.print_help()
    return 0


def _print_status(queue_dir: str, workspace: str) -> int:
    queue = DirectoryMissionQueue(queue_dir)
    runtime = OpenCodeRuntimeAdapter()
    info = runtime.detect_runtime(workspace)

    print(f"vercosa-ai-framework: {__version__}")
    print(f"queue: {Path(queue_dir)}")
    for status in MissionStatus:
        print(f"missions.{status.value}: {len(queue.list(status))}")
    print(f"runtime: {info.runtime_id}")
    print(f"runtime.available: {str(info.available).lower()}")
    if info.limitations:
        print(f"runtime.limitations: {'; '.join(info.limitations)}")
    return 0


def _run_one(args: argparse.Namespace) -> int:
    queue = DirectoryMissionQueue(args.queue_dir)
    mission = queue.get(args.mission_id) if args.mission_id else queue.next()
    if mission is None:
        print("no queued missions")
        return 0
    if args.workspace:
        mission = mission.with_status(mission.status, workspace=args.workspace)

    runtime = _runtime_from_args(args)
    if args.dry_run:
        return _print_dry_run(runtime, mission, args.guardian_mode)

    runner = MissionRunner(
        queue,
        runtime,
        guardian=_guardian_from_args(args),
        guardian_mode=_guardian_mode_from_args(args, mission),
    )
    result = runner.run(mission.mission_id)
    return _print_result(result)


def _run_worker(args: argparse.Namespace) -> int:
    if args.max_missions < 1:
        print("--max-missions must be >= 1", file=sys.stderr)
        return 2

    queue = DirectoryMissionQueue(args.queue_dir)
    runtime = _runtime_from_args(args)
    exit_code = 0
    processed = 0

    for _ in range(args.max_missions):
        mission = queue.next()
        if mission is None:
            if processed == 0:
                print("no queued missions")
            break
        if args.workspace:
            mission = mission.with_status(mission.status, workspace=args.workspace)
        if args.dry_run:
            exit_code = max(exit_code, _print_dry_run(runtime, mission, args.guardian_mode))
        else:
            result = MissionRunner(
                queue,
                runtime,
                guardian=_guardian_from_args(args),
                guardian_mode=_guardian_mode_from_args(args, mission),
            ).run(mission.mission_id)
            exit_code = max(exit_code, _print_result(result))
        processed += 1

    print(f"processed: {processed}")
    return exit_code


def _runtime_from_args(args: argparse.Namespace) -> OpenCodeRuntimeAdapter:
    return OpenCodeRuntimeAdapter(
        options=OpenCodeRunOptions(
            dry_run=bool(args.dry_run),
            model=args.model,
            small_model=args.small_model,
            auto_approve=bool(args.auto_approve),
        )
    )


def _workflow_status(file_path: str) -> int:
    try:
        workflow = _load_workflow_file(Path(file_path))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"workflow: {workflow.workflow_id}")
    print(f"mission: {workflow.mission_id}")
    print(f"status: {workflow.status.value}")
    print(f"tasks: {len(workflow.tasks)}")
    for status in TaskStatus:
        count = sum(1 for task in workflow.tasks if task.status == status)
        print(f"tasks.{status.value}: {count}")
    return 0


def _workflow_validate(file_path: str, guardian_mode: str) -> int:
    try:
        workflow = _load_workflow_file(Path(file_path))
        _validate_workflow(workflow)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(f"workflow: {workflow.workflow_id}")
    print("validation: ok")
    for task in workflow.tasks:
        decision = _evaluate_workflow_task(workflow, task, GuardianMode(guardian_mode), workspace=".")
        print(f"task: {task.task_id}")
        _print_guardian_decision(decision)
        if not decision.allowed:
            return 1
    return 0


def _workflow_run(args: argparse.Namespace) -> int:
    try:
        workflow = _load_workflow_file(Path(args.file))
        _validate_workflow(workflow)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    runtime = _runtime_from_args(args)
    guardian_mode = GuardianMode(args.guardian_mode)
    if args.dry_run:
        return _print_workflow_dry_run(runtime, workflow, guardian_mode, args.workspace)

    result = WorkflowEngine(
        runtime,
        GuardianEngine(),
        workspace=args.workspace,
        guardian_mode=guardian_mode,
    ).execute(workflow)
    return _print_workflow_result(result)


def _load_workflow_file(path: Path) -> Workflow:
    if not path.exists() or not path.is_file():
        msg = f"workflow file not found: {path}"
        raise ValueError(msg)
    if path.suffix.lower() != ".json":
        goal = path.read_text(encoding="utf-8")
        workflow_id = path.stem
        mission_id = path.stem
        return Workflow(
            workflow_id=workflow_id,
            mission_id=mission_id,
            title=path.stem,
            goal=goal,
            tasks=(
                WorkflowTask(
                    workflow_id=workflow_id,
                    mission_id=mission_id,
                    title=path.stem,
                    goal=goal,
                ),
            ),
        )

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        msg = f"invalid workflow JSON: {exc}"
        raise ValueError(msg) from exc
    if not isinstance(data, dict):
        msg = "invalid workflow JSON: expected object"
        raise ValueError(msg)

    required = ("mission_id", "title", "goal")
    missing = [key for key in required if key not in data]
    if missing:
        msg = f"invalid workflow JSON: missing required field(s): {', '.join(missing)}"
        raise ValueError(msg)

    workflow_id = str(data.get("workflow_id") or data["mission_id"])
    mission_id = str(data["mission_id"])
    tasks_data = data.get("tasks", ())
    if not isinstance(tasks_data, list | tuple):
        msg = "invalid workflow JSON: tasks must be an array"
        raise ValueError(msg)

    tasks = tuple(_workflow_task_from_data(item, workflow_id, mission_id) for item in tasks_data)
    workflow_kwargs = {
        "workflow_id": workflow_id,
        "mission_id": mission_id,
        "title": str(data["title"]),
        "goal": str(data["goal"]),
        "status": WorkflowStatus(data.get("status", WorkflowStatus.DRAFT.value)),
        "spec_refs": _tuple_from(data.get("spec_refs", ())),
        "guardian_refs": _tuple_from(data.get("guardian_refs", ())),
        "policy_refs": _tuple_from(data.get("policy_refs", ())),
        "tasks": tasks,
        "dependency_graph": _dict_of_tuples(data.get("dependency_graph", {})),
        "execution_mode": str(data.get("execution_mode", "sequential")),
        "execution_limits": _dict_from(data.get("execution_limits", {"max_parallel_tasks": 1})),
        "budget_policy": _dict_from(data.get("budget_policy", {})),
        "validation_policy": _dict_from(data.get("validation_policy", {})),
        "retry_policy": _dict_from(data.get("retry_policy", {"max_replans": 0})),
    }
    return Workflow(**workflow_kwargs)


def _workflow_task_from_data(data: object, workflow_id: str, mission_id: str) -> WorkflowTask:
    if not isinstance(data, dict):
        msg = "invalid workflow JSON: each task must be an object"
        raise ValueError(msg)
    required = ("title", "goal")
    missing = [key for key in required if key not in data]
    if missing:
        msg = f"invalid workflow JSON: task missing required field(s): {', '.join(missing)}"
        raise ValueError(msg)

    dependencies = data.get("dependencies", ())
    if not isinstance(dependencies, list | tuple):
        msg = "invalid workflow JSON: task dependencies must be an array"
        raise ValueError(msg)

    task_kwargs = {
        "workflow_id": workflow_id,
        "mission_id": mission_id,
        "title": str(data["title"]),
        "goal": str(data["goal"]),
        "task_id": str(data["task_id"]) if data.get("task_id") else WorkflowTask(title="", goal="", workflow_id=workflow_id, mission_id=mission_id).task_id,
        "task_type": str(data.get("task_type", "generic")),
        "status": TaskStatus(data.get("status", TaskStatus.PENDING.value)),
        "inputs": _dict_from(data.get("inputs", {})),
        "expected_outputs": _tuple_from(data.get("expected_outputs", ())),
        "acceptance_criteria": _tuple_from(data.get("acceptance_criteria", ())),
        "dependencies": tuple(_task_dependency_from_data(item) for item in dependencies),
        "blocked_by": _tuple_from(data.get("blocked_by", ())),
        "priority": int(data.get("priority", 100)),
        "risk_level": str(data.get("risk_level", "low")),
        "required_capabilities": _tuple_from(data.get("required_capabilities", ())),
        "model_policy": _dict_from(data.get("model_policy", {})),
        "execution_limits": _dict_from(data.get("execution_limits", {})),
        "retry_policy": _dict_from(data.get("retry_policy", {"max_attempts": 1})),
        "validation_policy": _dict_from(data.get("validation_policy", {})),
        "assigned_agent_ref": data.get("assigned_agent_ref"),
        "artifacts": _tuple_from(data.get("artifacts", ())),
    }
    return WorkflowTask(**task_kwargs)


def _task_dependency_from_data(data: object) -> TaskDependency:
    if not isinstance(data, dict):
        msg = "invalid workflow JSON: task dependency must be an object"
        raise ValueError(msg)
    if "target_ref" not in data:
        msg = "invalid workflow JSON: task dependency missing required field: target_ref"
        raise ValueError(msg)
    return TaskDependency(
        dependency_type=str(data.get("dependency_type", "requires_completion")),
        target_ref=str(data["target_ref"]),
        reason=str(data.get("reason", "")),
        required=bool(data.get("required", True)),
        metadata=_dict_from(data.get("metadata", {})),
    )


def _validate_workflow(workflow: Workflow) -> None:
    if workflow.execution_mode != "sequential":
        msg = f"unsupported execution mode: {workflow.execution_mode}"
        raise ValueError(msg)
    task_ids = {task.task_id for task in workflow.tasks}
    if len(task_ids) != len(workflow.tasks):
        msg = "invalid workflow: duplicate task_id"
        raise ValueError(msg)
    for task in workflow.tasks:
        for dependency in task.dependencies:
            if dependency.required and dependency.target_ref not in task_ids:
                msg = f"unresolvable dependency: task {task.task_id} requires {dependency.target_ref}"
                raise ValueError(msg)


def _dict_from(value: object) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        msg = "invalid workflow JSON: expected object"
        raise ValueError(msg)
    return dict(value)


def _dict_of_tuples(value: object) -> dict[str, tuple[str, ...]]:
    return {str(key): _tuple_from(item) for key, item in _dict_from(value).items()}


def _print_workflow_dry_run(
    runtime: OpenCodeRuntimeAdapter,
    workflow: Workflow,
    guardian_mode: GuardianMode,
    workspace: str,
) -> int:
    print(f"workflow: {workflow.workflow_id}")
    print("status: dry-run")
    for task in workflow.tasks:
        decision = _evaluate_workflow_task(workflow, task, guardian_mode, workspace)
        print(f"task: {task.task_id}")
        _print_guardian_decision(decision)
        if not decision.allowed:
            return 1
        request = _request_for_workflow_task(workflow, task, workspace)
        result = runtime.execute_task(request)
        if result.errors:
            print(f"task.status: blocked")
            print(f"errors: {'; '.join(result.errors)}")
            return 1
        print("task.status: dry-run")
        if result.commands_executed:
            print(f"command: {result.commands_executed[0]}")
    return 0


def _evaluate_workflow_task(
    workflow: Workflow,
    task: WorkflowTask,
    guardian_mode: GuardianMode,
    workspace: str,
) -> GuardianDecision:
    return GuardianEngine().evaluate(
        GuardianEvaluationContext(
            mission_id=workflow.mission_id,
            evaluation_type="workflow_task_pre_execution",
            evaluation_id=f"{workflow.workflow_id}:{task.task_id}",
            guardian_mode=guardian_mode,
            mission_goal=workflow.goal,
            spec_refs=workflow.spec_refs,
            guardian_refs=workflow.guardian_refs,
            workspace=workspace,
            requested_action=f"{task.title}\n{task.goal}",
            planned_command=str(task.inputs.get("planned_command")) if task.inputs.get("planned_command") else None,
            target_paths=_tuple_from(task.inputs.get("target_paths", ())) + task.expected_outputs + task.artifacts,
            budget_policy=dict(workflow.budget_policy),
            execution_limits={**workflow.execution_limits, **task.execution_limits},
            metadata={
                "workflow_id": workflow.workflow_id,
                "task_id": task.task_id,
                "task_type": task.task_type,
                "risk_level": task.risk_level,
                "acceptance_criteria": task.acceptance_criteria,
                "required": bool(task.validation_policy.get("required", True)),
            },
        )
    )


def _request_for_workflow_task(workflow: Workflow, task: WorkflowTask, workspace: str) -> RuntimeExecutionRequest:
    return RuntimeExecutionRequest(
        mission_id=workflow.mission_id,
        workspace=workspace,
        workflow_id=workflow.workflow_id,
        task_id=task.task_id,
        context={
            "workflow_title": workflow.title,
            "workflow_goal": workflow.goal,
            "task_title": task.title,
            "task_goal": task.goal,
            "prompt": task.goal,
            "task_type": task.task_type,
            "inputs": task.inputs,
            "expected_outputs": task.expected_outputs,
            "acceptance_criteria": task.acceptance_criteria,
            "model_policy": task.model_policy,
        },
        execution_limits=dict(task.execution_limits),
        logging_policy={"sanitize_secrets": True},
        approval_policy=dict(task.validation_policy),
    )


def _print_workflow_result(result: WorkflowResult) -> int:
    print(f"workflow: {result.workflow_id}")
    print(f"mission: {result.mission_id}")
    print(f"status: {result.status.value}")
    if result.summary:
        print(f"summary: {result.summary}")
    for task_result in result.task_results:
        print(f"task: {task_result.task_id}")
        print(f"task.status: {task_result.status.value}")
    if result.errors:
        print(f"errors: {'; '.join(result.errors)}")
    return 0 if result.status == WorkflowStatus.DONE else 1


def _check_mission(file_path: str, guardian_mode: str) -> int:
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        print(f"mission file not found: {path}", file=sys.stderr)
        return 2

    try:
        mission = _load_mission_file(path)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    decision = _evaluate_mission(mission, GuardianMode(guardian_mode))
    _print_guardian_decision(decision)
    return 0 if decision.allowed else 1


def _load_mission_file(path: Path) -> Mission:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() != ".json":
        return Mission(title=path.stem, goal=text, workspace=str(path.parent))

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        msg = f"invalid mission JSON: {exc}"
        raise ValueError(msg) from exc
    if not isinstance(data, dict):
        msg = "invalid mission JSON: expected object"
        raise ValueError(msg)
    if "status" in data:
        data["status"] = MissionStatus(data["status"])
    for key in ("spec_refs", "guardian_refs", "acceptance_criteria"):
        data[key] = tuple(data.get(key, ()))
    return Mission(**data)


def _guardian_from_args(args: argparse.Namespace) -> GuardianEngine:
    mode = getattr(args, "guardian_mode", None)
    if mode is None:
        return GuardianEngine()
    return GuardianModeOverride(GuardianEngine(), GuardianMode(mode))


def _guardian_mode_from_args(args: argparse.Namespace, mission: Mission) -> GuardianMode:
    mode = getattr(args, "guardian_mode", None) or mission.guardian_mode
    return GuardianMode(mode)


class GuardianModeOverride:
    """Guardian wrapper used by CLI overrides without mutating queued missions."""

    def __init__(self, guardian: GuardianEngine, guardian_mode: GuardianMode) -> None:
        self.guardian = guardian
        self.guardian_mode = guardian_mode

    def evaluate(self, context: GuardianEvaluationContext) -> GuardianDecision:
        return self.guardian.evaluate(replace(context, guardian_mode=self.guardian_mode))


def _request_for(mission: Mission) -> RuntimeExecutionRequest:
    return RuntimeExecutionRequest(
        mission_id=mission.mission_id,
        workspace=mission.workspace,
        context={
            "mission_title": mission.title,
            "mission_goal": mission.goal,
            "spec_refs": mission.spec_refs,
            "acceptance_criteria": mission.acceptance_criteria,
        },
        permissions={**dict(mission.security_policy), "guardian_mode": mission.guardian_mode},
        execution_limits=dict(mission.execution_limits),
    )


def _print_dry_run(runtime: OpenCodeRuntimeAdapter, mission: Mission, guardian_mode: str | None = None) -> int:
    mode = GuardianMode(guardian_mode or mission.guardian_mode)
    decision = _evaluate_mission(mission, mode)
    _print_guardian_decision(decision)
    if not decision.allowed:
        return 1

    request = _request_for(mission)
    result = runtime.execute_mission(request)
    if result.errors:
        print(f"mission: {mission.mission_id}")
        print("status: blocked")
        print(f"errors: {'; '.join(result.errors)}")
        return 1
    print(f"mission: {mission.mission_id}")
    print("status: dry-run")
    if result.commands_executed:
        print(f"command: {result.commands_executed[0]}")
    return 0


def _evaluate_mission(mission: Mission, guardian_mode: GuardianMode) -> GuardianDecision:
    return GuardianEngine().evaluate(
        GuardianEvaluationContext(
            mission_id=mission.mission_id,
            evaluation_type="mission_pre_execution",
            guardian_mode=guardian_mode,
            mission_goal=mission.goal,
            spec_refs=mission.spec_refs,
            guardian_refs=mission.guardian_refs,
            workspace=mission.workspace,
            requested_action=mission.title,
            target_paths=_tuple_from(mission.constraints.get("target_paths", ())),
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
    )


def _tuple_from(value: object) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def _print_guardian_decision(decision: GuardianDecision) -> None:
    print(f"guardian.decision: {decision.decision.value}")
    print(f"guardian.risk_level: {decision.risk_level.value}")
    print(f"guardian.mode: {decision.guardian_mode.value}")
    if decision.matched_policies:
        print(f"guardian.policies: {', '.join(decision.matched_policies)}")
    if decision.reasons:
        print(f"guardian.reasons: {'; '.join(decision.reasons)}")
    if decision.required_actions:
        print(f"guardian.required_actions: {'; '.join(decision.required_actions)}")
    if decision.safe_alternatives:
        print(f"guardian.safe_alternatives: {'; '.join(decision.safe_alternatives)}")


def _print_result(result: MissionResult) -> int:
    print(f"mission: {result.mission_id}")
    print(f"status: {result.status.value}")
    if result.summary:
        print(f"summary: {result.summary}")
    if result.errors:
        print(f"errors: {'; '.join(result.errors)}")
    return 0 if result.status == MissionStatus.DONE else 1


def main() -> None:
    """Console script entrypoint."""
    raise SystemExit(run())


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))

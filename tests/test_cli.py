from vercosa_ai_framework.missions import DirectoryMissionQueue, Mission
from vercosa_ai_framework.cli import run


def test_cli_version(capsys):
    exit_code = run(["--version"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "vercosa-ai-framework" in captured.out


def test_cli_version_command(capsys):
    exit_code = run(["version"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "vercosa-ai-framework" in captured.out


def test_cli_diagnose(capsys):
    exit_code = run(["diagnose"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "python:" in captured.out
    assert "system:" in captured.out
    assert "machine:" in captured.out


def test_cli_status_prints_queue_and_runtime(capsys, tmp_path):
    queue_dir = tmp_path / "missions"
    DirectoryMissionQueue(queue_dir).enqueue(Mission(title="Queued", goal="Wait"))

    exit_code = run(["--queue-dir", str(queue_dir), "status"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "missions.queued: 1" in captured.out
    assert "runtime: opencode" in captured.out


def test_cli_check_mission_prints_guardian_decision(capsys, tmp_path):
    mission_file = tmp_path / "mission.md"
    mission_file.write_text(
        "Entregaveis: documentacao.\nCriterios de aceite: decisao Guardian impressa.",
        encoding="utf-8",
    )

    exit_code = run(["check-mission", str(mission_file)])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "guardian.decision: allow" in captured.out
    assert "guardian.risk_level:" in captured.out


def test_cli_check_mission_blocks_strict_implementation_without_spec(capsys, tmp_path):
    mission_file = tmp_path / "mission.md"
    mission_file.write_text(
        "Implementar codigo. Entregaveis: modulo. Criterios de aceite: testes passando.",
        encoding="utf-8",
    )

    exit_code = run(["check-mission", str(mission_file), "--guardian-mode", "strict"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "guardian.decision: block" in captured.out
    assert "mission.requires_spec" in captured.out


def test_cli_run_one_dry_run_does_not_execute_opencode(capsys, tmp_path):
    queue_dir = tmp_path / "missions"
    mission = DirectoryMissionQueue(queue_dir).enqueue(
        Mission(title="Dry", goal="Prepare only", workspace=str(tmp_path))
    )

    exit_code = run(["--queue-dir", str(queue_dir), "run-one", "--dry-run"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert f"mission: {mission.mission_id}" in captured.out
    assert "status: dry-run" in captured.out
    assert "opencode run Prepare only" in captured.out


def test_cli_run_one_strict_guardian_blocks_before_opencode(capsys, tmp_path):
    queue_dir = tmp_path / "missions"
    mission = DirectoryMissionQueue(queue_dir).enqueue(
        Mission(
            title="Implement",
            goal="Implementar codigo. Entregaveis: modulo. Criterios de aceite: testes passando.",
            workspace=str(tmp_path),
        )
    )

    exit_code = run(["--queue-dir", str(queue_dir), "run-one", "--guardian-mode", "strict"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "guardian blocked mission" in captured.out
    assert "opencode run" not in captured.out
    assert DirectoryMissionQueue(queue_dir).get(mission.mission_id).status.value == "failed"


def test_cli_run_worker_dry_run_limits_processed_missions(capsys, tmp_path):
    queue_dir = tmp_path / "missions"
    queue = DirectoryMissionQueue(queue_dir)
    queue.enqueue(Mission(title="One", goal="First", priority=1))
    queue.enqueue(Mission(title="Two", goal="Second", priority=2))

    exit_code = run(["--queue-dir", str(queue_dir), "run-worker", "--dry-run", "--max-missions", "1"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status: dry-run" in captured.out
    assert "processed: 1" in captured.out

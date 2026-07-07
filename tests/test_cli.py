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


def test_cli_status_prints_operational_mission_counts(capsys, tmp_path):
    (tmp_path / "missions" / "queue").mkdir(parents=True)
    (tmp_path / "missions" / "queue" / "missao.md").write_text("missao", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "status"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "queue:   1" in captured.out
    assert "running: 0" in captured.out
    assert "done:    0" in captured.out
    assert "failed:  0" in captured.out


def test_cli_nao_implementa_execucao_de_missoes(capsys):
    exit_code = run(["run-one"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "invalid choice" in captured.err

from vercosa_ai_framework.cli import run


def test_cli_version(capsys):
    exit_code = run(["--version"])

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

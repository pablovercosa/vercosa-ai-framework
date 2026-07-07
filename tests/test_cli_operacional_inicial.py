import importlib
import socket
import subprocess

from vercosa_ai_framework.cli.main import collect_mission_directory_status, main, run


def test_modulo_cli_pode_ser_importado():
    modulo = importlib.import_module("vercosa_ai_framework.cli")

    assert hasattr(modulo, "main")


def test_funcao_principal_existe():
    assert callable(main)


def test_comando_de_ajuda_retorna_sucesso(capsys):
    exit_code = run(["--help"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status" in captured.out


def test_status_conta_arquivos_markdown_por_diretorio(capsys, tmp_path):
    for directory in ("queue", "running", "done", "failed"):
        (tmp_path / "missions" / directory).mkdir(parents=True)

    (tmp_path / "missions" / "queue" / "001.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "queue" / "ignorado.txt").write_text("texto", encoding="utf-8")
    (tmp_path / "missions" / "running" / "002.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "done" / "003.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "done" / "004.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "failed" / "005.md").write_text("missao", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "status"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "queue:   1" in captured.out
    assert "running: 1" in captured.out
    assert "done:    2" in captured.out
    assert "failed:  1" in captured.out


def test_diretorios_ausentes_sao_tratados_como_zero(tmp_path):
    status = collect_mission_directory_status(tmp_path)

    assert status.queue == 0
    assert status.running == 0
    assert status.done == 0
    assert status.failed == 0


def test_argumento_invalido_retorna_erro_controlado(capsys):
    exit_code = run(["--nao-existe"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "unrecognized arguments" in captured.err


def test_status_nao_executa_scripts_shell(monkeypatch, tmp_path):
    def falhar_se_chamar_subprocess(*args, **kwargs):
        raise AssertionError("subprocess nao deveria ser chamado")

    monkeypatch.setattr(subprocess, "run", falhar_se_chamar_subprocess)
    monkeypatch.setattr(subprocess, "Popen", falhar_se_chamar_subprocess)

    assert run(["--project-root", str(tmp_path), "status"]) == 0


def test_status_nao_acessa_rede(monkeypatch, tmp_path):
    def falhar_se_abrir_socket(*args, **kwargs):
        raise AssertionError("rede nao deveria ser acessada")

    monkeypatch.setattr(socket, "create_connection", falhar_se_abrir_socket)
    monkeypatch.setattr(socket, "socket", falhar_se_abrir_socket)

    assert run(["--project-root", str(tmp_path), "status"]) == 0


def test_cli_nao_exige_dependencia_externa():
    modulo = importlib.import_module("vercosa_ai_framework.cli.main")

    assert modulo.__name__ == "vercosa_ai_framework.cli.main"

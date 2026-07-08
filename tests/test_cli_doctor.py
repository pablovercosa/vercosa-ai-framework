import importlib
import socket
import subprocess

from vercosa_ai_framework.cli.main import diagnose_project, run


def criar_estrutura_minima(root, *, incluir_docs=True):
    for directory in ("queue", "running", "done", "failed"):
        (root / "missions" / directory).mkdir(parents=True)
    (root / "src" / "vercosa_ai_framework").mkdir(parents=True)
    (root / "README.md").write_text("# Projeto\n", encoding="utf-8")
    if incluir_docs:
        (root / "docs" / "operations").mkdir(parents=True)
        (root / "docs" / "roadmap").mkdir(parents=True)
        (root / "docs" / "operations" / "post-batch-validation-checklist.md").write_text(
            "# Checklist\n",
            encoding="utf-8",
        )
        (root / "docs" / "roadmap" / "mission-backlog.md").write_text(
            "# Backlog\n",
            encoding="utf-8",
        )


def snapshot_arquivos(root):
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


def test_comando_doctor_existe(capsys):
    exit_code = run(["--help"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "doctor" in captured.out


def test_doctor_retorna_sucesso_para_estrutura_minima_saudavel(capsys, tmp_path):
    criar_estrutura_minima(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "diagnostico: local nao destrutivo" in captured.out
    assert "status_geral: ok" in captured.out
    assert "pronto_para_missao: sim" in captured.out


def test_doctor_retorna_erro_controlado_quando_missions_nao_existe(capsys, tmp_path):
    (tmp_path / "src" / "vercosa_ai_framework").mkdir(parents=True)
    (tmp_path / "README.md").write_text("# Projeto\n", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "status_geral: error" in captured.out
    assert "error[missions_missing]" in captured.out


def test_doctor_retorna_erro_controlado_quando_src_vercosa_ai_framework_nao_existe(capsys, tmp_path):
    criar_estrutura_minima(tmp_path)
    (tmp_path / "src" / "vercosa_ai_framework").rmdir()

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "status_geral: error" in captured.out
    assert "error[package_root_missing]" in captured.out


def test_doctor_reporta_problema_quando_failed_contem_arquivos(capsys, tmp_path):
    criar_estrutura_minima(tmp_path)
    (tmp_path / "missions" / "failed" / "falha.md").write_text("falha", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "failed:  1" in captured.out
    assert "failed_vazio: nao" in captured.out
    assert "error[failed_not_empty]" in captured.out


def test_doctor_reporta_problema_quando_running_contem_arquivos(capsys, tmp_path):
    criar_estrutura_minima(tmp_path)
    (tmp_path / "missions" / "running" / "presa.md").write_text("presa", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "running: 1" in captured.out
    assert "running_vazio: nao" in captured.out
    assert "error[running_not_empty]" in captured.out


def test_doctor_reporta_contagens_de_todos_os_diretorios(capsys, tmp_path):
    criar_estrutura_minima(tmp_path)
    (tmp_path / "missions" / "queue" / "001.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "running" / "002.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "done" / "003.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "done" / "004.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "failed" / "005.md").write_text("missao", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "queue:   1" in captured.out
    assert "running: 1" in captured.out
    assert "done:    2" in captured.out
    assert "failed:  1" in captured.out


def test_doctor_trata_documentos_opcionais_ausentes_como_warning(capsys, tmp_path):
    criar_estrutura_minima(tmp_path, incluir_docs=False)

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    captured = capsys.readouterr()
    result = diagnose_project(tmp_path)

    assert exit_code == 0
    assert result.status == "warning"
    assert "status_geral: warning" in captured.out
    assert "warning[optional_document_missing]" in captured.out


def test_doctor_nao_altera_arquivos(tmp_path):
    criar_estrutura_minima(tmp_path)
    before = snapshot_arquivos(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "doctor"])
    after = snapshot_arquivos(tmp_path)

    assert exit_code == 0
    assert after == before


def test_doctor_nao_executa_scripts_shell_git_pytest_ou_compileall(monkeypatch, tmp_path):
    criar_estrutura_minima(tmp_path)

    def falhar_se_chamar_subprocess(*args, **kwargs):
        raise AssertionError("subprocess nao deveria ser chamado")

    monkeypatch.setattr(subprocess, "run", falhar_se_chamar_subprocess)
    monkeypatch.setattr(subprocess, "Popen", falhar_se_chamar_subprocess)

    assert run(["--project-root", str(tmp_path), "doctor"]) == 0


def test_doctor_nao_acessa_rede(monkeypatch, tmp_path):
    criar_estrutura_minima(tmp_path)

    def falhar_se_abrir_socket(*args, **kwargs):
        raise AssertionError("rede nao deveria ser acessada")

    monkeypatch.setattr(socket, "create_connection", falhar_se_abrir_socket)
    monkeypatch.setattr(socket, "socket", falhar_se_abrir_socket)

    assert run(["--project-root", str(tmp_path), "doctor"]) == 0


def test_doctor_nao_exige_dependencia_externa():
    modulo = importlib.import_module("vercosa_ai_framework.cli.main")

    assert modulo.__name__ == "vercosa_ai_framework.cli.main"


def test_validate_continua_funcionando(capsys, tmp_path):
    criar_estrutura_minima(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "validate"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "resultado: saudavel" in captured.out


def test_status_continua_funcionando(capsys, tmp_path):
    criar_estrutura_minima(tmp_path)
    (tmp_path / "missions" / "queue" / "001.md").write_text("missao", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "queue:   1" in captured.out

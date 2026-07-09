import socket
import subprocess

from vercosa_ai_framework.cli.main import list_missions, run


def criar_estrutura_missoes(root):
    for directory in ("queue", "running", "done", "failed"):
        (root / "missions" / directory).mkdir(parents=True)


def snapshot_arquivos(root):
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


def test_comando_missions_existe(capsys):
    exit_code = run(["--help"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "missions" in captured.out


def test_missions_lista_arquivos_por_estado_com_contagens(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "queue" / "002.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "queue" / "001.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "queue" / "ignorado.txt").write_text("texto", encoding="utf-8")
    (tmp_path / "missions" / "running" / "003.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "done" / "005.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "done" / "004.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "failed" / "006.md").write_text("missao", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "missions"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "filtro_estado: todos" in captured.out
    assert "queue:   2" in captured.out
    assert "running: 1" in captured.out
    assert "done:    2" in captured.out
    assert "failed:  1" in captured.out
    assert "queue (2, presente):" in captured.out
    assert captured.out.index("- 001.md") < captured.out.index("- 002.md")
    assert captured.out.index("- 004.md") < captured.out.index("- 005.md")
    assert "ignorado.txt" not in captured.out


def test_missions_filtra_por_estado_mantendo_contagens_gerais(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "queue" / "001.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "failed" / "falha.md").write_text("missao", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "missions", "--state", "failed"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "filtro_estado: failed" in captured.out
    assert "queue:   1" in captured.out
    assert "failed:  1" in captured.out
    assert "failed (1, presente):" in captured.out
    assert "- falha.md" in captured.out
    assert "queue (1, presente):" not in captured.out
    assert "- 001.md" not in captured.out


def test_missions_mostra_estado_vazio(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "missions", "--state", "queue"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "queue:   0" in captured.out
    assert "queue (0, presente):" in captured.out
    assert "- (vazio)" in captured.out


def test_missions_trata_diretorio_ausente_sem_traceback(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "failed").rmdir()

    exit_code = run(["--project-root", str(tmp_path), "missions", "--state", "failed"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "failed:  0" in captured.out
    assert "failed (0, ausente):" in captured.out
    assert "diretorio ausente:" in captured.out


def test_list_missions_retorna_ordenacao_deterministica(tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "queue" / "b.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "queue" / "a.md").write_text("missao", encoding="utf-8")

    result = list_missions(tmp_path)
    queue = next(state for state in result.states if state.state == "queue")

    assert queue.files == ("a.md", "b.md")
    assert result.mission_status.queue == 2


def test_missions_nao_altera_arquivos(tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "queue" / "001.md").write_text("missao", encoding="utf-8")
    before = snapshot_arquivos(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "missions"])
    after = snapshot_arquivos(tmp_path)

    assert exit_code == 0
    assert after == before


def test_missions_nao_executa_scripts_shell_git_pytest_ou_compileall(monkeypatch, tmp_path):
    criar_estrutura_missoes(tmp_path)

    def falhar_se_chamar_subprocess(*args, **kwargs):
        raise AssertionError("subprocess nao deveria ser chamado")

    monkeypatch.setattr(subprocess, "run", falhar_se_chamar_subprocess)
    monkeypatch.setattr(subprocess, "Popen", falhar_se_chamar_subprocess)

    assert run(["--project-root", str(tmp_path), "missions"]) == 0


def test_missions_nao_acessa_rede(monkeypatch, tmp_path):
    criar_estrutura_missoes(tmp_path)

    def falhar_se_abrir_socket(*args, **kwargs):
        raise AssertionError("rede nao deveria ser acessada")

    monkeypatch.setattr(socket, "create_connection", falhar_se_abrir_socket)
    monkeypatch.setattr(socket, "socket", falhar_se_abrir_socket)

    assert run(["--project-root", str(tmp_path), "missions"]) == 0


def test_comandos_existentes_continuam_funcionando(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "src" / "vercosa_ai_framework").mkdir(parents=True)
    (tmp_path / "README.md").write_text("# Projeto\n", encoding="utf-8")

    assert run(["--project-root", str(tmp_path), "status"]) == 0
    assert run(["--project-root", str(tmp_path), "validate"]) == 0
    assert run(["--project-root", str(tmp_path), "doctor"]) == 0

    captured = capsys.readouterr()
    assert "resultado: saudavel" in captured.out

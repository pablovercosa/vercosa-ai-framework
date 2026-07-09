import socket
import subprocess

from vercosa_ai_framework.cli.main import run, summarize_batch


def criar_estrutura_missoes(root):
    for directory in ("queue", "running", "done", "failed"):
        (root / "missions" / directory).mkdir(parents=True)


def snapshot_arquivos(root):
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


def test_comando_batch_summary_existe(capsys):
    exit_code = run(["--help"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "batch-summary" in captured.out


def test_batch_summary_mostra_resumo_limpo_com_ultimo_log(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "done" / "001.md").write_text("missao", encoding="utf-8")
    (tmp_path / "missions" / "done" / "002.md").write_text("missao", encoding="utf-8")
    (tmp_path / "logs").mkdir()
    primeiro = tmp_path / "logs" / "001.log"
    ultimo = tmp_path / "logs" / "002.out"
    primeiro.write_text("log", encoding="utf-8")
    ultimo.write_text("log", encoding="utf-8")
    primeiro.touch()
    ultimo.touch()

    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "diagnostico: resumo pos-batch local somente leitura" in captured.out
    assert "queue:   0" in captured.out
    assert "running: 0" in captured.out
    assert "done:    2" in captured.out
    assert "failed:  0" in captured.out
    assert f"ultimo_log: {ultimo}" in captured.out
    assert "estado operacional aparentemente limpo, sem validacao completa pela CLI" in captured.out


def test_batch_summary_indica_atencao_quando_failed_contem_arquivo(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "failed" / "falha.md").write_text("falha", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "failed:  1" in captured.out
    assert "missions/failed contem arquivo(s); revisar falhas antes de continuar." in captured.out


def test_batch_summary_indica_atencao_quando_running_contem_arquivo(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "running" / "presa.md").write_text("presa", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "running: 1" in captured.out
    assert "missions/running contem arquivo(s); verificar worker e missao presa." in captured.out


def test_batch_summary_indica_fila_pendente(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "queue" / "pendente.md").write_text("pendente", encoding="utf-8")

    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "queue:   1" in captured.out
    assert "missions/queue ainda contem missao(oes) pendente(s)." in captured.out


def test_batch_summary_trata_logs_ausentes(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "logs_dir: ausente" in captured.out
    assert "ultimo_log: nenhum log encontrado" in captured.out


def test_batch_summary_trata_diretorios_ausentes_sem_traceback(capsys, tmp_path):
    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "queue:   0" in captured.out
    assert "running: 0" in captured.out
    assert "done:    0" in captured.out
    assert "failed:  0" in captured.out


def test_batch_summary_nao_altera_arquivos(tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "missions" / "done" / "001.md").write_text("missao", encoding="utf-8")
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "001.log").write_text("log", encoding="utf-8")
    before = snapshot_arquivos(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    after = snapshot_arquivos(tmp_path)

    assert exit_code == 0
    assert after == before


def test_batch_summary_contem_lembretes_de_validacao(capsys, tmp_path):
    criar_estrutura_missoes(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "batch-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "rode pytest manualmente" in captured.out
    assert "rode python3 -m compileall src manualmente" in captured.out
    assert "verifique git status --short manualmente" in captured.out
    assert "faca push somente apos validar" in captured.out


def test_summarize_batch_usa_ultimo_log_por_mtime_e_nome(tmp_path):
    criar_estrutura_missoes(tmp_path)
    (tmp_path / "logs").mkdir()
    antigo = tmp_path / "logs" / "antigo.log"
    ultimo = tmp_path / "logs" / "ultimo.log"
    ignorado = tmp_path / "logs" / "ultimo.txt"
    antigo.write_text("log", encoding="utf-8")
    ultimo.write_text("log", encoding="utf-8")
    ignorado.write_text("texto", encoding="utf-8")
    antigo.touch()
    ultimo.touch()

    result = summarize_batch(tmp_path)

    assert result.last_log == ultimo


def test_batch_summary_nao_executa_scripts_shell_git_pytest_ou_compileall(monkeypatch, tmp_path):
    criar_estrutura_missoes(tmp_path)

    def falhar_se_chamar_subprocess(*args, **kwargs):
        raise AssertionError("subprocess nao deveria ser chamado")

    monkeypatch.setattr(subprocess, "run", falhar_se_chamar_subprocess)
    monkeypatch.setattr(subprocess, "Popen", falhar_se_chamar_subprocess)

    assert run(["--project-root", str(tmp_path), "batch-summary"]) == 0


def test_batch_summary_nao_acessa_rede(monkeypatch, tmp_path):
    criar_estrutura_missoes(tmp_path)

    def falhar_se_abrir_socket(*args, **kwargs):
        raise AssertionError("rede nao deveria ser acessada")

    monkeypatch.setattr(socket, "create_connection", falhar_se_abrir_socket)
    monkeypatch.setattr(socket, "socket", falhar_se_abrir_socket)

    assert run(["--project-root", str(tmp_path), "batch-summary"]) == 0

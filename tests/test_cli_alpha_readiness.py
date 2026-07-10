import socket
import subprocess

from vercosa_ai_framework.cli.main import (
    ALPHA_READINESS_EXIT_CODE_WITH_WARNINGS,
    ALPHA_REQUIRED_DIRECTORIES,
    ALPHA_REQUIRED_FILES,
    check_alpha_readiness,
    run,
)


def criar_estrutura_alpha(root, *, incluir_ci=True):
    for directory in ALPHA_REQUIRED_DIRECTORIES:
        (root / directory).mkdir(parents=True, exist_ok=True)
    for file_path in ALPHA_REQUIRED_FILES:
        path = root / file_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {path.name}\n", encoding="utf-8")
    if incluir_ci:
        (root / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
        (root / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")


def snapshot_arquivos(root):
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


def test_alpha_readiness_pronto(capsys, tmp_path):
    criar_estrutura_alpha(tmp_path)

    result = check_alpha_readiness(tmp_path)
    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    captured = capsys.readouterr()

    assert result.classification == "PRONTO"
    assert exit_code == 0
    assert "classificacao: PRONTO" in captured.out
    assert "pendencias_bloqueantes:" in captured.out
    assert "- nenhuma pendencia bloqueante encontrada" in captured.out


def test_alpha_readiness_retorna_nao_pronto_quando_arquivo_obrigatorio_ausente(capsys, tmp_path):
    criar_estrutura_alpha(tmp_path)
    (tmp_path / "SECURITY.md").unlink()

    result = check_alpha_readiness(tmp_path)
    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    captured = capsys.readouterr()

    assert result.classification == "NÃO PRONTO"
    assert exit_code == 1
    assert "classificacao: NÃO PRONTO" in captured.out
    assert "Arquivo obrigatorio ausente: SECURITY.md" in captured.out


def test_alpha_readiness_retorna_nao_pronto_quando_failed_tem_arquivo(capsys, tmp_path):
    criar_estrutura_alpha(tmp_path)
    (tmp_path / "missions" / "failed" / "falha.md").write_text("falha", encoding="utf-8")

    result = check_alpha_readiness(tmp_path)
    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    captured = capsys.readouterr()

    assert result.classification == "NÃO PRONTO"
    assert exit_code == 1
    assert "failed:  1" in captured.out
    assert "missions/failed contem 1 arquivo(s) .md" in captured.out


def test_alpha_readiness_retorna_nao_pronto_quando_running_tem_arquivo(capsys, tmp_path):
    criar_estrutura_alpha(tmp_path)
    (tmp_path / "missions" / "running" / "presa.md").write_text("presa", encoding="utf-8")

    result = check_alpha_readiness(tmp_path)
    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    captured = capsys.readouterr()

    assert result.classification == "NÃO PRONTO"
    assert exit_code == 1
    assert "running: 1" in captured.out
    assert "missions/running contem 1 arquivo(s) .md" in captured.out


def test_alpha_readiness_retorna_ressalva_quando_queue_tem_arquivo(capsys, tmp_path):
    criar_estrutura_alpha(tmp_path)
    (tmp_path / "missions" / "queue" / "pendente.md").write_text("pendente", encoding="utf-8")

    result = check_alpha_readiness(tmp_path)
    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    captured = capsys.readouterr()

    assert result.classification == "PRONTO COM RESSALVAS"
    assert exit_code == ALPHA_READINESS_EXIT_CODE_WITH_WARNINGS
    assert "queue:   1" in captured.out
    assert "missions/queue contem 1 arquivo(s) .md pendente(s)" in captured.out


def test_alpha_readiness_retorna_ressalva_quando_ci_ausente(capsys, tmp_path):
    criar_estrutura_alpha(tmp_path, incluir_ci=False)

    result = check_alpha_readiness(tmp_path)
    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    captured = capsys.readouterr()

    assert result.classification == "PRONTO COM RESSALVAS"
    assert exit_code == ALPHA_READINESS_EXIT_CODE_WITH_WARNINGS
    assert "workflow de CI ausente: .github/workflows/ci.yml" in captured.out


def test_alpha_readiness_nao_altera_arquivos(tmp_path):
    criar_estrutura_alpha(tmp_path)
    before = snapshot_arquivos(tmp_path)

    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    after = snapshot_arquivos(tmp_path)

    assert exit_code == 0
    assert after == before


def test_alpha_readiness_nao_executa_scripts_shell_git_pytest_compileall_ou_publicacao(monkeypatch, tmp_path):
    criar_estrutura_alpha(tmp_path)

    def falhar_se_chamar_subprocess(*args, **kwargs):
        raise AssertionError("subprocess nao deveria ser chamado")

    monkeypatch.setattr(subprocess, "run", falhar_se_chamar_subprocess)
    monkeypatch.setattr(subprocess, "Popen", falhar_se_chamar_subprocess)

    assert run(["--project-root", str(tmp_path), "alpha-readiness"]) == 0


def test_alpha_readiness_nao_acessa_rede(monkeypatch, tmp_path):
    criar_estrutura_alpha(tmp_path)

    def falhar_se_abrir_socket(*args, **kwargs):
        raise AssertionError("rede nao deveria ser acessada")

    monkeypatch.setattr(socket, "create_connection", falhar_se_abrir_socket)
    monkeypatch.setattr(socket, "socket", falhar_se_abrir_socket)

    assert run(["--project-root", str(tmp_path), "alpha-readiness"]) == 0


def test_alpha_readiness_retorna_ressalva_quando_release_notes_sao_preliminares(capsys, tmp_path):
    criar_estrutura_alpha(tmp_path)
    (tmp_path / "docs" / "release" / "release-notes-alpha.md").write_text(
        "# Notas preliminares\n",
        encoding="utf-8",
    )

    result = check_alpha_readiness(tmp_path)
    exit_code = run(["--project-root", str(tmp_path), "alpha-readiness"])
    captured = capsys.readouterr()

    assert result.classification == "PRONTO COM RESSALVAS"
    assert exit_code == ALPHA_READINESS_EXIT_CODE_WITH_WARNINGS
    assert "release notes alfa existem, mas permanecem preliminares" in captured.out


def test_alpha_readiness_comando_aparece_na_ajuda(capsys):
    exit_code = run(["--help"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "alpha-readiness" in captured.out

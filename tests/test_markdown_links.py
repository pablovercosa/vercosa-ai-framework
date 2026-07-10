import socket
import subprocess

from vercosa_ai_framework.cli.main import collect_markdown_documentation_files, run, validate_markdown_links


def snapshot_arquivos(root):
    return sorted(str(path.relative_to(root)) for path in root.rglob("*") if path.is_file())


def test_docs_links_valida_link_relativo_existente(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "README.md").write_text("[Guia](docs/guia.md)\n", encoding="utf-8")
    (tmp_path / "docs" / "guia.md").write_text("# Guia\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)

    assert result.ok
    assert len(result.markdown_files) == 2


def test_docs_links_detecta_link_relativo_quebrado(capsys, tmp_path):
    (tmp_path / "README.md").write_text("[Ausente](docs/ausente.md)\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)
    exit_code = run(["docs-links", "--base-dir", str(tmp_path)])
    captured = capsys.readouterr()

    assert not result.ok
    assert result.issues[0].target == "docs/ausente.md"
    assert exit_code == 1
    assert "resultado: links Markdown relativos quebrados" in captured.out
    assert "README.md:1 -> docs/ausente.md" in captured.out


def test_docs_links_ignora_link_externo_sem_rede(monkeypatch, tmp_path):
    (tmp_path / "README.md").write_text("[Site](https://example.com/docs)\n", encoding="utf-8")

    def falhar_se_abrir_socket(*args, **kwargs):
        raise AssertionError("rede nao deveria ser acessada")

    monkeypatch.setattr(socket, "create_connection", falhar_se_abrir_socket)
    monkeypatch.setattr(socket, "socket", falhar_se_abrir_socket)

    assert validate_markdown_links(tmp_path).ok
    assert run(["docs-links", "--base-dir", str(tmp_path)]) == 0


def test_docs_links_ignora_ancora_interna_pura(tmp_path):
    (tmp_path / "README.md").write_text("[Secao](#secao)\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)

    assert result.ok


def test_docs_links_valida_arquivo_existente_com_ancora(tmp_path):
    (tmp_path / "README.md").write_text("[Guia](docs/guia.md#instalacao)\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guia.md").write_text("# Outro Titulo\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)

    assert result.ok


def test_docs_links_valida_imagem_relativa_basica(tmp_path):
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guia.md").write_text("![Diagrama](assets/diagrama.svg)\n", encoding="utf-8")
    (tmp_path / "docs" / "assets").mkdir()
    (tmp_path / "docs" / "assets" / "diagrama.svg").write_text("<svg />\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)

    assert result.ok


def test_docs_links_valida_multiplos_arquivos_markdown(tmp_path):
    (tmp_path / "README.md").write_text("[Contribuir](CONTRIBUTING.md)\n", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text("[Guia](docs/guia.md)\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "guia.md").write_text("[Raiz](../README.md)\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)

    relative_files = {path.relative_to(tmp_path).as_posix() for path in result.markdown_files}

    assert result.ok
    assert relative_files == {"README.md", "CONTRIBUTING.md", "docs/guia.md"}


def test_docs_links_ignora_diretorios_nao_publicos(tmp_path):
    (tmp_path / "README.md").write_text("# Raiz\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "publico.md").write_text("# Publico\n", encoding="utf-8")
    (tmp_path / "docs" / ".pytest_cache").mkdir()
    (tmp_path / "docs" / ".pytest_cache" / "ignorado.md").write_text("[Quebrado](ausente.md)\n", encoding="utf-8")
    (tmp_path / "logs").mkdir()
    (tmp_path / "logs" / "ignorado.md").write_text("[Quebrado](ausente.md)\n", encoding="utf-8")

    files = collect_markdown_documentation_files(tmp_path)
    result = validate_markdown_links(tmp_path)

    assert result.ok
    assert {path.relative_to(tmp_path).as_posix() for path in files} == {"README.md", "docs/publico.md"}


def test_docs_links_inclui_readme_de_modulo_runtime(tmp_path):
    (tmp_path / "src" / "vercosa_ai_framework" / "runtime").mkdir(parents=True)
    (tmp_path / "src" / "vercosa_ai_framework" / "runtime" / "README.md").write_text(
        "[Raiz](../../../README.md)\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# Projeto\n", encoding="utf-8")

    files = collect_markdown_documentation_files(tmp_path)
    result = validate_markdown_links(tmp_path)

    assert result.ok
    assert "src/vercosa_ai_framework/runtime/README.md" in {path.relative_to(tmp_path).as_posix() for path in files}


def test_docs_links_ignora_links_em_blocos_de_codigo(tmp_path):
    (tmp_path / "README.md").write_text(
        "```markdown\n[Quebrado](docs/ausente.md)\n```\n",
        encoding="utf-8",
    )

    result = validate_markdown_links(tmp_path)

    assert result.ok


def test_docs_links_ignora_links_em_codigo_inline(tmp_path):
    (tmp_path / "README.md").write_text("Use `[Texto](docs/ausente.md)` como exemplo.\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)

    assert result.ok


def test_docs_links_trata_espacos_codificados(tmp_path):
    (tmp_path / "README.md").write_text("[Arquivo](docs/arquivo%20com%20espaco.md)\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "arquivo com espaco.md").write_text("# Arquivo\n", encoding="utf-8")

    result = validate_markdown_links(tmp_path)

    assert result.ok


def test_docs_links_nao_altera_arquivos(tmp_path):
    (tmp_path / "README.md").write_text("# Projeto\n", encoding="utf-8")
    before = snapshot_arquivos(tmp_path)

    exit_code = run(["docs-links", "--base-dir", str(tmp_path)])
    after = snapshot_arquivos(tmp_path)

    assert exit_code == 0
    assert after == before


def test_docs_links_retorna_erro_para_base_dir_inexistente(capsys, tmp_path):
    exit_code = run(["docs-links", "--base-dir", str(tmp_path / "ausente")])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "diretorio base nao encontrado" in captured.out


def test_docs_links_nao_executa_scripts_shell_git_pytest_ou_compileall(monkeypatch, tmp_path):
    (tmp_path / "README.md").write_text("# Projeto\n", encoding="utf-8")

    def falhar_se_chamar_subprocess(*args, **kwargs):
        raise AssertionError("subprocess nao deveria ser chamado")

    monkeypatch.setattr(subprocess, "run", falhar_se_chamar_subprocess)
    monkeypatch.setattr(subprocess, "Popen", falhar_se_chamar_subprocess)

    assert run(["docs-links", "--base-dir", str(tmp_path)]) == 0

from __future__ import annotations

from pathlib import Path

import pytest

from vercosa_ai_framework.missions.prompt_composer import (
    PromptCompositionError,
    compose_mission_prompt,
    main,
)


def criar_projeto(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "missions" / "queue").mkdir(parents=True)
    (root / "missions" / "base").mkdir(parents=True)
    (root / ".opencode" / "agents").mkdir(parents=True)
    (root / "AGENTS.md").write_text("# AGENTS\n\nRegras globais.\n", encoding="utf-8")
    (root / "missions" / "base" / "EXECUTION_CONTRACT.md").write_text(
        "---\nversion: v1\n---\n\n# Contrato\n\nRegras comuns.\n",
        encoding="utf-8",
    )
    (root / ".opencode" / "agents" / "mission-executor-base.md").write_text(
        "# mission-executor-base\n\nAgente base.\n",
        encoding="utf-8",
    )
    (root / ".opencode" / "agents" / "framework-architect.md").write_text(
        "# framework-architect\n\nAgente especializado.\n",
        encoding="utf-8",
    )
    return root


def escrever_missao(root: Path, content: str, name: str = "0103-missao.md") -> Path:
    path = root / "missions" / "queue" / name
    path.write_text(content, encoding="utf-8")
    return path


def missao_compacta(extra: str = "") -> str:
    return f"""---
id: "0103"
title: "Inventariar repositório"
base_contract: "v1"
roles:
  - repository-auditor
agents:
  - framework-architect
network: deny
database: deny
providers: deny
git_push: deny
git_tag: deny
release: deny
package_publish: deny
sudo: deny
destructive_commands: deny
{extra}---

# Objetivo

Inventariar o repositório.
"""


def test_compoe_missao_compacta_na_ordem_obrigatoria(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, missao_compacta())

    composed = compose_mission_prompt(mission, root)

    assert composed.metadata.mission_format == "compact"
    content = composed.content
    markers = [
        "<<< VAF SECTION: AGENTS.md >>>",
        "<<< VAF SECTION: Contrato base de execução (v1) >>>",
        "<<< VAF SECTION: Agente executor base: mission-executor-base >>>",
        "<<< VAF SECTION: Agente operacional especializado: framework-architect >>>",
        "<<< VAF SECTION: Permissões declaradas >>>",
        "<<< VAF SECTION: Papéis temporários declarados >>>",
        "<<< VAF SECTION: Missão específica: 0103-missao.md >>>",
    ]
    positions = [content.index(marker) for marker in markers]
    assert positions == sorted(positions)
    assert "# Objetivo" in content


def test_aplica_defaults_deny_quando_capacidades_estao_ausentes(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(
        root,
        """---
id: "0103"
title: "Missão compacta"
base_contract: "v1"
---

# Objetivo

Executar com defaults.
""",
    )

    composed = compose_mission_prompt(mission, root)

    assert all(value == "deny" for value in composed.metadata.capabilities.values())
    assert "- network: deny" in composed.content


@pytest.mark.parametrize(
    ("field", "value"),
    [("network", "allow"), ("network", "local-only"), ("database", "read-only"), ("database", "allow")],
)
def test_aceita_permissoes_explicitas_validas(tmp_path: Path, field: str, value: str):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(
        root,
        """---
id: "0103"
title: "Missão compacta"
base_contract: "v1"
%s: %s
---

# Objetivo

Executar com permissão explícita.
"""
        % (field, value),
    )

    composed = compose_mission_prompt(mission, root)

    assert composed.metadata.capabilities[field] == value
    assert f"- {field}: {value}" in composed.content


def test_rejeita_contrato_inexistente(tmp_path: Path):
    root = criar_projeto(tmp_path)
    (root / "missions" / "base" / "EXECUTION_CONTRACT.md").unlink()
    mission = escrever_missao(root, missao_compacta())

    with pytest.raises(PromptCompositionError, match="contrato base não encontrado"):
        compose_mission_prompt(mission, root)


def test_rejeita_versao_de_contrato_invalida(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, missao_compacta().replace('base_contract: "v1"', 'base_contract: "v2"'))

    with pytest.raises(PromptCompositionError, match="versão de contrato inexistente"):
        compose_mission_prompt(mission, root)


def test_rejeita_agente_base_inexistente(tmp_path: Path):
    root = criar_projeto(tmp_path)
    (root / ".opencode" / "agents" / "mission-executor-base.md").unlink()
    mission = escrever_missao(root, missao_compacta())

    with pytest.raises(PromptCompositionError, match="agente mission-executor-base não encontrado"):
        compose_mission_prompt(mission, root)


def test_rejeita_agente_especializado_inexistente(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, missao_compacta().replace("framework-architect", "security-reviewer"))

    with pytest.raises(PromptCompositionError, match="agente security-reviewer não encontrado"):
        compose_mission_prompt(mission, root)


def test_role_sem_agente_correspondente_permanece_valida_e_preserva_ordem(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(
        root,
        """---
id: "0103"
title: "Missão compacta"
base_contract: "v1"
roles:
  - mission-system-architect
  - security-reviewer
---

# Objetivo

Executar com roles.
""",
    )

    composed = compose_mission_prompt(mission, root)

    assert composed.metadata.roles == ("mission-system-architect", "security-reviewer")
    assert "agente security-reviewer" not in composed.content


def test_deduplica_agente_base_e_agente_especializado(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(
        root,
        """---
id: "0103"
title: "Missão compacta"
base_contract: "v1"
agents:
  - mission-executor-base
  - framework-architect
  - framework-architect
---

# Objetivo

Executar com agentes duplicados.
""",
    )

    composed = compose_mission_prompt(mission, root)

    assert composed.metadata.agents == ("framework-architect",)
    assert composed.content.count("Agente executor base: mission-executor-base") == 2
    assert composed.content.count("Agente operacional especializado: framework-architect") == 2


def test_rejeita_path_traversal_em_nome_de_agente(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(
        root,
        """---
id: "0103"
title: "Missão compacta"
base_contract: "v1"
agents:
  - ../secrets
---

# Objetivo

Executar.
""",
    )

    with pytest.raises(PromptCompositionError, match="nome de agente operacional inválido"):
        compose_mission_prompt(mission, root)


@pytest.mark.parametrize("field", ["id", "title", "base_contract"])
def test_rejeita_missao_compacta_sem_campo_obrigatorio(tmp_path: Path, field: str):
    root = criar_projeto(tmp_path)
    lines = [
        "---",
        'id: "0103"',
        'title: "Missão compacta"',
        'base_contract: "v1"',
        "---",
        "",
        "# Objetivo",
        "",
        "Executar.",
    ]
    lines = [line for line in lines if not line.startswith(f"{field}:")]
    mission = escrever_missao(root, "\n".join(lines))

    with pytest.raises(PromptCompositionError, match=f"campo obrigatório ausente ou inválido: {field}"):
        compose_mission_prompt(mission, root)


def test_rejeita_valor_de_capacidade_invalido(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, missao_compacta().replace("network: deny", "network: read-only"))

    with pytest.raises(PromptCompositionError, match="valor inválido para network"):
        compose_mission_prompt(mission, root)


def test_missao_legada_nao_precisa_frontmatter_e_usa_contrato_padrao(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, "# Missão Legada\n\nExecutar sem frontmatter.\n")

    composed = compose_mission_prompt(mission, root)

    assert composed.metadata.mission_format == "legacy"
    assert composed.metadata.base_contract == "v1"
    assert "# Missão Legada" in composed.content


def test_composicao_nao_modifica_arquivos_de_origem(tmp_path: Path):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, missao_compacta())
    before = mission.read_text(encoding="utf-8")

    compose_mission_prompt(mission, root)

    assert mission.read_text(encoding="utf-8") == before


def test_modo_validate_retorna_sucesso_sem_imprimir_prompt(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, missao_compacta())

    status = main(["--validate", str(mission), "--project-root", str(root)])

    captured = capsys.readouterr()
    assert status == 0
    assert "composição válida" in captured.out
    assert "Regras globais" not in captured.out


def test_cli_compose_retorna_erro_antes_de_execucao(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    root = criar_projeto(tmp_path)
    mission = escrever_missao(root, missao_compacta().replace("framework-architect", "agente-ausente"))

    status = main(["--compose", str(mission), "--project-root", str(root)])

    captured = capsys.readouterr()
    assert status == 1
    assert captured.out == ""
    assert "erro de composição" in captured.err
    assert "agente-ausente" in captured.err

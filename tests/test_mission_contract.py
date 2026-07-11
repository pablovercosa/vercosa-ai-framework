from pathlib import Path


def test_contrato_base_v1_existe_e_declara_regras_obrigatorias():
    path = Path("missions/base/EXECUTION_CONTRACT.md")

    content = path.read_text(encoding="utf-8")

    assert "version: v1" in content
    assert "Precedência" in content
    assert "Negação" in content or "negação" in content
    assert "Não usar `sudo`" in content
    assert "Não usar `git add .`" in content
    assert "pytest" in content
    assert "python3 -m compileall src" in content


def test_template_compacto_existe_sem_repetir_contrato_completo():
    path = Path("missions/templates/COMPACT_MISSION_TEMPLATE.md")

    content = path.read_text(encoding="utf-8")

    assert 'base_contract: "v1"' in content
    assert "# Objetivo" in content
    assert "missions/base/EXECUTION_CONTRACT.md" in content
    assert "Não reescrever histórico Git" not in content


def test_agente_executor_base_existe_no_diretorio_operacional_canonico():
    path = Path(".opencode/agents/mission-executor-base.md")

    content = path.read_text(encoding="utf-8")

    assert path.is_file()
    assert "# mission-executor-base" in content
    assert "contrato base" in content
    assert "Diferencie planejado, implementado, integrado e validado" in content


def test_runner_shell_compoe_prompt_antes_de_chamar_opencode():
    content = Path("scripts/vaf-run-one-mission.sh").read_text(encoding="utf-8")

    composer_position = content.index("vercosa_ai_framework.missions.prompt_composer --compose")
    opencode_position = content.index("opencode \\")
    assert composer_position < opencode_position
    assert "mv \"$RUNNING\" \"$MISSION\"" in content
    assert "git add -A" not in content
    assert "git add ." not in content

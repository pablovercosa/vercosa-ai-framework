import tomllib
from pathlib import Path

from vercosa_ai_framework.cli.main import main


def carregar_pyproject():
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    return tomllib.loads(pyproject.read_text(encoding="utf-8"))


def test_pyproject_declara_empacotamento_minimo_em_src():
    data = carregar_pyproject()

    assert data["build-system"]["build-backend"] == "setuptools.build_meta"
    assert data["project"]["name"] == "vercosa-ai-framework"
    assert data["project"]["version"] == "0.1.0a1"
    assert data["project"]["readme"] == "README.md"
    assert data["project"]["dependencies"] == []
    assert data["tool"]["setuptools"]["packages"]["find"]["where"] == ["src"]
    assert data["tool"]["setuptools"]["packages"]["find"]["include"] == ["vercosa_ai_framework*"]


def test_entrypoint_vaf_aponta_para_cli_existente():
    data = carregar_pyproject()

    assert callable(main)
    assert data["project"]["scripts"] == {"vaf": "vercosa_ai_framework.cli.main:main"}

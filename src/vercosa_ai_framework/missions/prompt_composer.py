"""Composição determinística de contexto para execução de missões."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


class PromptCompositionError(ValueError):
    """Erro controlado de validação ou composição de missão."""


CAPABILITY_VALUES: dict[str, set[str]] = {
    "network": {"deny", "local-only", "allow"},
    "database": {"deny", "read-only", "allow"},
    "providers": {"deny", "allow"},
    "git_push": {"deny", "allow"},
    "git_tag": {"deny", "allow"},
    "release": {"deny", "allow"},
    "package_publish": {"deny", "allow"},
    "sudo": {"deny"},
    "destructive_commands": {"deny"},
}
DEFAULT_CAPABILITIES = {name: "deny" for name in CAPABILITY_VALUES}
BASE_AGENT_NAME = "mission-executor-base"
CONTRACT_VERSION = "v1"
AGENT_NAME_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")


@dataclass(frozen=True, slots=True)
class MissionMetadata:
    """Metadados validados da missão."""

    mission_format: str
    mission_id: str | None
    title: str | None
    base_contract: str
    roles: tuple[str, ...]
    agents: tuple[str, ...]
    capabilities: dict[str, str]


@dataclass(frozen=True, slots=True)
class ComposedPrompt:
    """Resultado da composição de contexto."""

    metadata: MissionMetadata
    content: str


def compose_mission_prompt(mission_path: str | Path, project_root: str | Path) -> ComposedPrompt:
    """Compor o contexto final da missão a partir de arquivos versionados."""

    root = _resolve_root(project_root)
    mission_file = _resolve_inside_root(root, mission_path)
    if not mission_file.is_file():
        raise PromptCompositionError(f"missão não encontrada: {mission_file}")

    mission_text = mission_file.read_text(encoding="utf-8")
    frontmatter, mission_body = _split_frontmatter(mission_text)
    metadata = _metadata_from_frontmatter(frontmatter)

    agents_text = _load_agents(root, metadata.agents)
    sections = [
        ("AGENTS.md", _read_required(root / "AGENTS.md", "AGENTS.md")),
        (
            f"Contrato base de execução ({metadata.base_contract})",
            _load_contract(root, metadata.base_contract),
        ),
        ("Agente executor base: mission-executor-base", _read_agent(root, BASE_AGENT_NAME)),
    ]

    for agent_name, agent_text in agents_text:
        sections.append((f"Agente operacional especializado: {agent_name}", agent_text))

    sections.append(("Permissões declaradas", _format_capabilities(metadata.capabilities)))
    if metadata.roles:
        sections.append(("Papéis temporários declarados", "\n".join(f"- {role}" for role in metadata.roles)))
    sections.append((f"Missão específica: {mission_file.name}", mission_body.strip() + "\n"))

    return ComposedPrompt(metadata=metadata, content=_join_sections(sections))


def validate_mission_prompt(mission_path: str | Path, project_root: str | Path) -> ComposedPrompt:
    """Validar a composição sem gravar o prompt em arquivo."""

    return compose_mission_prompt(mission_path, project_root)


def _resolve_root(project_root: str | Path) -> Path:
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise PromptCompositionError(f"raiz do projeto inválida: {root}")
    return root


def _resolve_inside_root(root: Path, path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root):
        raise PromptCompositionError(f"caminho fora da raiz autorizada: {path}")
    return resolved


def _split_frontmatter(text: str) -> tuple[dict[str, object] | None, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        raise PromptCompositionError("frontmatter iniciado sem delimitador final '---'")

    frontmatter_text = "\n".join(lines[1:closing_index])
    body = "\n".join(lines[closing_index + 1 :]).lstrip("\n")
    return _parse_frontmatter(frontmatter_text), body


def _parse_frontmatter(text: str) -> dict[str, object]:
    result: dict[str, object] = {}
    current_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line.startswith("  - "):
            if current_key is None:
                raise PromptCompositionError("lista de frontmatter sem campo associado")
            current = result.setdefault(current_key, [])
            if not isinstance(current, list):
                raise PromptCompositionError(f"campo {current_key} não aceita lista")
            current.append(_unquote(raw_line.strip()[2:].strip()))
            continue
        if raw_line.startswith(" "):
            raise PromptCompositionError(f"linha de frontmatter não suportada: {raw_line.strip()}")
        if ":" not in raw_line:
            raise PromptCompositionError(f"linha de frontmatter inválida: {raw_line}")

        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        if not key:
            raise PromptCompositionError("campo de frontmatter vazio")
        value = raw_value.strip()
        if not value:
            result[key] = []
            current_key = key
        else:
            result[key] = _unquote(value)
            current_key = key
    return result


def _unquote(value: str) -> str:
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def _metadata_from_frontmatter(frontmatter: dict[str, object] | None) -> MissionMetadata:
    if frontmatter is None:
        return MissionMetadata(
            mission_format="legacy",
            mission_id=None,
            title=None,
            base_contract=CONTRACT_VERSION,
            roles=(),
            agents=(),
            capabilities=dict(DEFAULT_CAPABILITIES),
        )

    mission_id = _required_string(frontmatter, "id")
    title = _required_string(frontmatter, "title")
    base_contract = _required_string(frontmatter, "base_contract")
    roles = _optional_string_list(frontmatter, "roles")
    declared_agents = _optional_string_list(frontmatter, "agents")
    agents = _dedupe_agents(declared_agents)
    capabilities = _capabilities_from(frontmatter)
    _reject_unknown_fields(frontmatter)

    return MissionMetadata(
        mission_format="compact",
        mission_id=mission_id,
        title=title,
        base_contract=base_contract,
        roles=roles,
        agents=agents,
        capabilities=capabilities,
    )


def _required_string(frontmatter: dict[str, object], key: str) -> str:
    value = frontmatter.get(key)
    if not isinstance(value, str) or not value.strip():
        raise PromptCompositionError(f"campo obrigatório ausente ou inválido: {key}")
    return value.strip()


def _optional_string_list(frontmatter: dict[str, object], key: str) -> tuple[str, ...]:
    value = frontmatter.get(key, [])
    if value == []:
        return ()
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise PromptCompositionError(f"campo {key} deve ser uma lista simples de strings")
    return tuple(item.strip() for item in value)


def _capabilities_from(frontmatter: dict[str, object]) -> dict[str, str]:
    capabilities = dict(DEFAULT_CAPABILITIES)
    for name, accepted in CAPABILITY_VALUES.items():
        raw_value = frontmatter.get(name, "deny")
        if not isinstance(raw_value, str):
            raise PromptCompositionError(f"capacidade {name} deve ser string")
        value = raw_value.strip()
        if value not in accepted:
            accepted_values = ", ".join(sorted(accepted))
            raise PromptCompositionError(f"valor inválido para {name}: {value}; aceitos: {accepted_values}")
        capabilities[name] = value
    return capabilities


def _reject_unknown_fields(frontmatter: dict[str, object]) -> None:
    allowed = {"id", "title", "base_contract", "roles", "agents", *CAPABILITY_VALUES.keys()}
    unknown = sorted(set(frontmatter) - allowed)
    if unknown:
        raise PromptCompositionError(f"campos de frontmatter não suportados: {', '.join(unknown)}")


def _dedupe_agents(agent_names: Sequence[str]) -> tuple[str, ...]:
    result: list[str] = []
    seen = {BASE_AGENT_NAME}
    for name in agent_names:
        _validate_agent_name(name)
        if name in seen:
            continue
        seen.add(name)
        result.append(name)
    return tuple(result)


def _validate_agent_name(name: str) -> None:
    if not name or name.startswith("/") or ".." in name or "/" in name or "\\" in name:
        raise PromptCompositionError(f"nome de agente operacional inválido: {name}")
    if any(char not in AGENT_NAME_CHARS for char in name):
        raise PromptCompositionError(f"nome de agente operacional contém caractere incompatível: {name}")


def _load_contract(root: Path, version: str) -> str:
    if version != CONTRACT_VERSION:
        raise PromptCompositionError(f"versão de contrato inexistente: {version}")
    contract_path = root / "missions" / "base" / "EXECUTION_CONTRACT.md"
    contract_text = _read_required(contract_path, "contrato base")
    if f"version: {version}" not in contract_text:
        raise PromptCompositionError(f"contrato base não declara a versão esperada: {version}")
    return contract_text


def _load_agents(root: Path, agents: Sequence[str]) -> tuple[tuple[str, str], ...]:
    return tuple((agent_name, _read_agent(root, agent_name)) for agent_name in agents)


def _read_agent(root: Path, agent_name: str) -> str:
    _validate_agent_name(agent_name)
    return _read_required(root / ".opencode" / "agents" / f"{agent_name}.md", f"agente {agent_name}")


def _read_required(path: Path, description: str) -> str:
    if not path.is_file():
        raise PromptCompositionError(f"{description} não encontrado: {path}")
    return path.read_text(encoding="utf-8")


def _format_capabilities(capabilities: dict[str, str]) -> str:
    return "\n".join(f"- {name}: {capabilities[name]}" for name in CAPABILITY_VALUES)


def _join_sections(sections: Sequence[tuple[str, str]]) -> str:
    rendered: list[str] = []
    for title, content in sections:
        rendered.append(f"\n<<< VAF SECTION: {title} >>>\n")
        rendered.append(content.rstrip() + "\n")
        rendered.append(f"<<< END VAF SECTION: {title} >>>\n")
    return "".join(rendered).lstrip("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compor ou validar contexto de execução de missão.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--validate", action="store_true", help="validar sem imprimir o prompt composto")
    mode.add_argument("--compose", action="store_true", help="imprimir o prompt composto em stdout")
    parser.add_argument("mission", help="caminho da missão Markdown")
    parser.add_argument("--project-root", default=".", help="raiz do projeto")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        composed = compose_mission_prompt(args.mission, args.project_root)
    except PromptCompositionError as exc:
        print(f"erro de composição: {exc}", file=sys.stderr)
        return 1

    if args.compose:
        print(composed.content, end="")
    else:
        print(f"composição válida: formato={composed.metadata.mission_format} contrato={composed.metadata.base_contract}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

"""CLI operacional local e deterministica do Vercosa AI Framework."""

from __future__ import annotations

import argparse
import platform
import sys
from dataclasses import dataclass
from pathlib import Path

from vercosa_ai_framework import __version__


MISSION_DIRECTORIES = ("queue", "running", "done", "failed")


@dataclass(frozen=True, slots=True)
class MissionDirectoryStatus:
    """Resumo imutavel dos diretorios operacionais de missao."""

    queue: int = 0
    running: int = 0
    done: int = 0
    failed: int = 0


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """Problema estrutural encontrado pela validacao local."""

    code: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Resultado deterministico da validacao estrutural local."""

    project_root: Path
    mission_status: MissionDirectoryStatus
    issues: tuple[ValidationIssue, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.issues


def build_parser() -> argparse.ArgumentParser:
    """Cria o parser da CLI operacional sem acoplar a scripts shell."""

    parser = argparse.ArgumentParser(
        prog="vaf",
        description="CLI operacional local do Vercosa AI Framework.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Mostra a versao minima operacional e encerra.",
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Caminho raiz do projeto usado para leitura local. Padrao: diretorio atual.",
    )
    parser.add_argument(
        "--queue-dir",
        help="Reservado para compatibilidade futura; nao executa missoes nesta fase.",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("version", help="Mostra a versao minima operacional e encerra.")
    subparsers.add_parser("diagnose", help="Mostra diagnostico local basico do Python e sistema.")
    subparsers.add_parser("status", help="Conta missoes locais em queue, running, done e failed.")
    subparsers.add_parser("validate", help="Valida a estrutura local basica sem executar missoes.")
    return parser


def run(argv: list[str] | None = None) -> int:
    """Executa a CLI e retorna codigo de saida controlado."""

    args_list = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()
    try:
        args = parser.parse_args(args_list)
    except SystemExit as exc:
        return int(exc.code or 0)

    if args.version or args.command == "version":
        print(f"vercosa-ai-framework {__version__}")
        return 0

    if args.command == "diagnose":
        print(f"vercosa-ai-framework: {__version__}")
        print(f"python: {platform.python_version()}")
        print(f"system: {platform.system() or 'unknown'}")
        print(f"machine: {platform.machine() or 'unknown'}")
        return 0

    if args.command == "status":
        return print_status(Path(args.project_root))

    if args.command == "validate":
        return print_validation(Path(args.project_root))

    parser.print_help()
    return 0


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada invocavel por Python e console script."""

    return run(argv)


def collect_mission_directory_status(project_root: str | Path) -> MissionDirectoryStatus:
    """Conta arquivos Markdown nos diretorios operacionais de missao.

    Diretorios ausentes contam como zero para manter comportamento previsivel em
    instalacoes novas, testes temporarios e worktrees parciais.
    """

    root = Path(project_root)
    counts = {
        name: _count_markdown_files(root / "missions" / name)
        for name in MISSION_DIRECTORIES
    }
    return MissionDirectoryStatus(**counts)


def print_status(project_root: str | Path) -> int:
    """Imprime status operacional basico sem executar scripts ou missoes."""

    root = Path(project_root)
    status = collect_mission_directory_status(root)

    print(f"vercosa-ai-framework: {__version__}")
    print(f"project_root: {root}")
    print(f"missions_root: {root / 'missions'}")
    print(f"queue:   {status.queue}")
    print(f"running: {status.running}")
    print(f"done:    {status.done}")
    print(f"failed:  {status.failed}")
    return 0


def validate_project_structure(project_root: str | Path) -> ValidationResult:
    """Valida estrutura local minima sem executar comandos externos."""

    root = Path(project_root)
    status = collect_mission_directory_status(root)
    issues: list[ValidationIssue] = []

    if not root.exists():
        issues.append(ValidationIssue("project_root_missing", f"Diretorio raiz nao existe: {root}"))
        return ValidationResult(project_root=root, mission_status=status, issues=tuple(issues))

    if not root.is_dir():
        issues.append(ValidationIssue("project_root_not_directory", f"Raiz informada nao e diretorio: {root}"))

    missions_root = root / "missions"
    if not missions_root.is_dir():
        issues.append(ValidationIssue("missions_missing", f"Diretorio obrigatorio ausente: {missions_root}"))
    else:
        for name in MISSION_DIRECTORIES:
            directory = missions_root / name
            if not directory.is_dir():
                issues.append(ValidationIssue("mission_subdir_missing", f"Diretorio obrigatorio ausente: {directory}"))

    if status.running > 0:
        issues.append(
            ValidationIssue(
                "running_not_empty",
                f"missions/running contem {status.running} arquivo(s) .md; revise missao presa antes de continuar.",
            )
        )

    if status.failed > 0:
        issues.append(
            ValidationIssue(
                "failed_not_empty",
                f"missions/failed contem {status.failed} arquivo(s) .md; revise falhas antes de continuar.",
            )
        )

    package_root = root / "src" / "vercosa_ai_framework"
    if not package_root.is_dir():
        issues.append(ValidationIssue("package_root_missing", f"Diretorio obrigatorio ausente: {package_root}"))

    readme = root / "README.md"
    if not readme.is_file():
        issues.append(ValidationIssue("readme_missing", f"Arquivo obrigatorio ausente: {readme}"))

    return ValidationResult(project_root=root, mission_status=status, issues=tuple(issues))


def print_validation(project_root: str | Path) -> int:
    """Imprime validacao estrutural local e retorna codigo controlado."""

    result = validate_project_structure(project_root)
    status = result.mission_status

    print(f"vercosa-ai-framework: {__version__}")
    print(f"project_root: {result.project_root}")
    print("validacao: estrutural local")
    print(f"queue:   {status.queue}")
    print(f"running: {status.running}")
    print(f"done:    {status.done}")
    print(f"failed:  {status.failed}")

    if result.ok:
        print("resultado: saudavel")
        return 0

    print("resultado: invalido")
    for issue in result.issues:
        print(f"problema[{issue.code}]: {issue.message}")
    return 1


def _count_markdown_files(directory: Path) -> int:
    if not directory.is_dir():
        return 0
    return sum(1 for path in directory.iterdir() if path.is_file() and path.suffix == ".md")


if __name__ == "__main__":
    raise SystemExit(main())

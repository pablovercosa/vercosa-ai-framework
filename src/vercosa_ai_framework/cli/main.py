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
class MissionStateListing:
    """Lista deterministica de arquivos de missao por estado."""

    state: str
    directory: Path
    exists: bool
    files: tuple[str, ...] = ()

    @property
    def count(self) -> int:
        return len(self.files)


@dataclass(frozen=True, slots=True)
class MissionListingResult:
    """Resultado de leitura local dos diretorios de missao."""

    project_root: Path
    states: tuple[MissionStateListing, ...]

    @property
    def mission_status(self) -> MissionDirectoryStatus:
        counts = {state.state: state.count for state in self.states}
        return MissionDirectoryStatus(**counts)


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


@dataclass(frozen=True, slots=True)
class DiagnosticIssue:
    """Item de diagnostico local classificado por severidade."""

    severity: str
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class DiagnosticResult:
    """Resultado deterministico do comando doctor."""

    project_root: Path
    validation: ValidationResult
    issues: tuple[DiagnosticIssue, ...] = ()

    @property
    def status(self) -> str:
        if any(issue.severity == "error" for issue in self.issues):
            return "error"
        if any(issue.severity == "warning" for issue in self.issues):
            return "warning"
        return "ok"


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
    missions_parser = subparsers.add_parser(
        "missions",
        help="Lista arquivos de missao por estado sem executar ou mover missoes.",
    )
    missions_parser.add_argument(
        "--state",
        choices=MISSION_DIRECTORIES,
        help="Filtra a listagem para um estado: queue, running, done ou failed.",
    )
    subparsers.add_parser("validate", help="Valida a estrutura local basica sem executar missoes.")
    subparsers.add_parser("doctor", help="Executa diagnostico local amigavel e nao destrutivo.")
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

    if args.command == "missions":
        return print_missions(Path(args.project_root), state=args.state)

    if args.command == "validate":
        return print_validation(Path(args.project_root))

    if args.command == "doctor":
        return print_doctor(Path(args.project_root))

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


def list_missions(project_root: str | Path) -> MissionListingResult:
    """Lista arquivos Markdown de missao por estado, sem efeitos colaterais."""

    root = Path(project_root)
    states = tuple(
        _list_mission_state(root / "missions" / state, state)
        for state in MISSION_DIRECTORIES
    )
    return MissionListingResult(project_root=root, states=states)


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


def print_missions(project_root: str | Path, *, state: str | None = None) -> int:
    """Imprime lista local de missoes por estado sem executar nada."""

    result = list_missions(project_root)
    status = result.mission_status
    selected_states = tuple(
        state_listing
        for state_listing in result.states
        if state is None or state_listing.state == state
    )

    print(f"vercosa-ai-framework: {__version__}")
    print(f"project_root: {result.project_root}")
    print(f"missions_root: {result.project_root / 'missions'}")
    print(f"filtro_estado: {state or 'todos'}")
    print("contagens:")
    print(f"queue:   {status.queue}")
    print(f"running: {status.running}")
    print(f"done:    {status.done}")
    print(f"failed:  {status.failed}")
    print("missoes:")

    for state_listing in selected_states:
        directory_status = "presente" if state_listing.exists else "ausente"
        print(f"{state_listing.state} ({state_listing.count}, {directory_status}):")
        if state_listing.files:
            for filename in state_listing.files:
                print(f"- {filename}")
        elif state_listing.exists:
            print("- (vazio)")
        else:
            print(f"- (diretorio ausente: {state_listing.directory})")

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


def diagnose_project(project_root: str | Path) -> DiagnosticResult:
    """Executa diagnostico local sem efeitos colaterais ou comandos externos."""

    validation = validate_project_structure(project_root)
    issues = [
        DiagnosticIssue("error", issue.code, issue.message)
        for issue in validation.issues
    ]
    root = validation.project_root

    optional_documents = (
        root / "docs" / "operations" / "post-batch-validation-checklist.md",
        root / "docs" / "roadmap" / "mission-backlog.md",
    )
    for document in optional_documents:
        if not document.is_file():
            issues.append(
                DiagnosticIssue(
                    "warning",
                    "optional_document_missing",
                    f"Documento operacional opcional ausente: {document}",
                )
            )

    return DiagnosticResult(
        project_root=root,
        validation=validation,
        issues=tuple(issues),
    )


def print_doctor(project_root: str | Path) -> int:
    """Imprime diagnostico operacional amigavel e retorna codigo controlado."""

    result = diagnose_project(project_root)
    status = result.validation.mission_status

    print(f"vercosa-ai-framework: {__version__}")
    print(f"project_root: {result.project_root}")
    print("diagnostico: local nao destrutivo")
    print(f"status_geral: {result.status}")
    print(f"queue:   {status.queue}")
    print(f"running: {status.running}")
    print(f"done:    {status.done}")
    print(f"failed:  {status.failed}")
    print(f"running_vazio: {'sim' if status.running == 0 else 'nao'}")
    print(f"failed_vazio: {'sim' if status.failed == 0 else 'nao'}")

    if result.status == "error":
        print("pronto_para_missao: nao")
        print("pronto_para_batch: nao")
        print("acao_sugerida: corrigir erros estruturais antes de iniciar ou retomar execucao.")
    elif result.status == "warning":
        print("pronto_para_missao: sim, com aviso")
        print("pronto_para_batch: sim, com revisao dos avisos")
        print("acao_sugerida: revisar avisos antes de batch ou investigacao pos-batch.")
    else:
        print("pronto_para_missao: sim")
        print("pronto_para_batch: sim")
        print("acao_sugerida: usar scripts seguros para executar missoes quando apropriado.")

    if result.issues:
        for issue in result.issues:
            print(f"{issue.severity}[{issue.code}]: {issue.message}")
    else:
        print("resultado: nenhum problema local detectado")

    print("limites: nao executa missoes, scripts shell, git, pytest, compileall, rede, banco ou providers.")
    return 1 if result.status == "error" else 0


def _count_markdown_files(directory: Path) -> int:
    if not directory.is_dir():
        return 0
    return sum(1 for path in directory.iterdir() if path.is_file() and path.suffix == ".md")


def _list_mission_state(directory: Path, state: str) -> MissionStateListing:
    if not directory.is_dir():
        return MissionStateListing(state=state, directory=directory, exists=False)

    files = tuple(
        sorted(path.name for path in directory.iterdir() if path.is_file() and path.suffix == ".md")
    )
    return MissionStateListing(state=state, directory=directory, exists=True, files=files)


if __name__ == "__main__":
    raise SystemExit(main())

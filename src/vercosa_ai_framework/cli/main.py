"""CLI operacional local e deterministica do Vercosa AI Framework."""

from __future__ import annotations

import argparse
import platform
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

from vercosa_ai_framework import __version__


MISSION_DIRECTORIES = ("queue", "running", "done", "failed")
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]*)\)")
EXTERNAL_LINK_SCHEMES = {"http", "https", "mailto", "tel"}
IGNORED_DOCS_DIRECTORIES = {".git", ".venv", "__pycache__", "logs", "dist", "build", ".pytest_cache"}


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


@dataclass(frozen=True, slots=True)
class BatchSummaryResult:
    """Resumo local e somente leitura para revisao pos-batch."""

    project_root: Path
    mission_status: MissionDirectoryStatus
    logs_directory: Path
    logs_directory_exists: bool
    last_log: Path | None = None

    @property
    def attention_items(self) -> tuple[str, ...]:
        items: list[str] = []
        if self.mission_status.running > 0:
            items.append("missions/running contem arquivo(s); verificar worker e missao presa.")
        if self.mission_status.failed > 0:
            items.append("missions/failed contem arquivo(s); revisar falhas antes de continuar.")
        if self.mission_status.queue > 0:
            items.append("missions/queue ainda contem missao(oes) pendente(s).")
        if self.mission_status.queue == 0 and self.mission_status.running == 0 and self.mission_status.failed == 0:
            items.append("estado operacional aparentemente limpo, sem validacao completa pela CLI.")
        return tuple(items)


@dataclass(frozen=True, slots=True)
class MarkdownLinkIssue:
    """Link Markdown relativo quebrado encontrado em documento local."""

    source: Path
    line: int
    target: str
    resolved_path: Path


@dataclass(frozen=True, slots=True)
class MarkdownLinkValidationResult:
    """Resultado deterministico da validacao local de links Markdown."""

    base_dir: Path
    markdown_files: tuple[Path, ...]
    issues: tuple[MarkdownLinkIssue, ...] = ()

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
    subparsers.add_parser("batch-summary", help="Mostra resumo pos-batch local, seguro e somente leitura.")
    docs_links_parser = subparsers.add_parser(
        "docs-links",
        help="Valida links relativos em Markdown local sem acessar rede.",
    )
    docs_links_parser.add_argument(
        "--base-dir",
        help="Diretorio base para localizar documentos Markdown. Padrao: valor de --project-root.",
    )
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

    if args.command == "batch-summary":
        return print_batch_summary(Path(args.project_root))

    if args.command == "docs-links":
        return print_markdown_link_validation(Path(args.base_dir or args.project_root))

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


def summarize_batch(project_root: str | Path) -> BatchSummaryResult:
    """Coleta resumo pos-batch sem comandos externos e sem alterar arquivos."""

    root = Path(project_root)
    logs_directory = root / "logs"
    return BatchSummaryResult(
        project_root=root,
        mission_status=collect_mission_directory_status(root),
        logs_directory=logs_directory,
        logs_directory_exists=logs_directory.is_dir(),
        last_log=_find_last_log(logs_directory),
    )


def validate_markdown_links(base_dir: str | Path) -> MarkdownLinkValidationResult:
    """Valida links relativos de Markdown local sem rede e sem parser completo."""

    root = Path(base_dir)
    markdown_files = collect_markdown_documentation_files(root)
    issues: list[MarkdownLinkIssue] = []

    for markdown_file in markdown_files:
        try:
            content = markdown_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_number, raw_target in _iter_markdown_links(content):
            target = _normalize_markdown_link_target(raw_target)
            if _should_ignore_markdown_link(target):
                continue

            target_without_anchor = target.split("#", 1)[0]
            target_without_query = target_without_anchor.split("?", 1)[0]
            decoded_target = unquote(target_without_query)
            if not decoded_target:
                continue

            resolved_path = (markdown_file.parent / decoded_target).resolve(strict=False)
            if not resolved_path.exists():
                issues.append(
                    MarkdownLinkIssue(
                        source=markdown_file,
                        line=line_number,
                        target=target,
                        resolved_path=resolved_path,
                    )
                )

    return MarkdownLinkValidationResult(base_dir=root, markdown_files=markdown_files, issues=tuple(issues))


def collect_markdown_documentation_files(base_dir: str | Path) -> tuple[Path, ...]:
    """Localiza documentos Markdown publicos relevantes para validacao local."""

    root = Path(base_dir)
    if not root.is_dir():
        return ()

    candidates: set[Path] = set()
    for filename in ("README.md", "CONTRIBUTING.md", "CHANGELOG.md", "SECURITY.md", "CODE_OF_CONDUCT.md"):
        path = root / filename
        if path.is_file():
            candidates.add(path)

    docs_root = root / "docs"
    if docs_root.is_dir():
        candidates.update(_iter_markdown_files(docs_root, ignore_runtime=True))

    package_root = root / "src" / "vercosa_ai_framework"
    if package_root.is_dir():
        candidates.update(
            path
            for path in _iter_markdown_files(package_root)
            if path.name == "README.md"
        )

    return tuple(sorted(candidates, key=lambda path: path.relative_to(root).as_posix()))


def print_markdown_link_validation(base_dir: str | Path) -> int:
    """Imprime validacao local de links Markdown e retorna codigo controlado."""

    root = Path(base_dir)
    if not root.is_dir():
        print(f"vercosa-ai-framework: {__version__}")
        print(f"base_dir: {root}")
        print("validacao: links Markdown locais")
        print("resultado: invalido")
        print(f"problema: diretorio base nao encontrado: {root}")
        return 1

    result = validate_markdown_links(base_dir)
    print(f"vercosa-ai-framework: {__version__}")
    print(f"base_dir: {result.base_dir}")
    print("validacao: links Markdown locais")
    print(f"arquivos_markdown: {len(result.markdown_files)}")

    if result.ok:
        print("resultado: links Markdown relativos validos")
        print("limites: links externos e ancoras internas puras foram ignorados; ancoras em arquivos existentes nao sao validadas.")
        return 0

    print("resultado: links Markdown relativos quebrados")
    for issue in result.issues:
        try:
            source = issue.source.relative_to(result.base_dir)
        except ValueError:
            source = issue.source
        print(f"problema: {source}:{issue.line} -> {issue.target} (nao encontrado: {issue.resolved_path})")
    print("limites: links externos e ancoras internas puras foram ignorados; ancoras em arquivos existentes nao sao validadas.")
    return 1


def print_batch_summary(project_root: str | Path) -> int:
    """Imprime diagnostico auxiliar pos-batch sem executar validacoes."""

    result = summarize_batch(project_root)
    status = result.mission_status

    print(f"vercosa-ai-framework: {__version__}")
    print(f"project_root: {result.project_root}")
    print("diagnostico: resumo pos-batch local somente leitura")
    print(f"queue:   {status.queue}")
    print(f"running: {status.running}")
    print(f"done:    {status.done}")
    print(f"failed:  {status.failed}")
    print(f"logs_dir: {'presente' if result.logs_directory_exists else 'ausente'}")
    if result.last_log is None:
        print("ultimo_log: nenhum log encontrado")
    else:
        print(f"ultimo_log: {result.last_log}")
    print("worker: nao verificado pela CLI; confirme com ./scripts/vaf-status.sh quando necessario.")
    print("git: nao verificado pela CLI; rode git status --short manualmente.")
    print("atencao:")
    for item in result.attention_items:
        print(f"- {item}")
    print("lembretes:")
    print("- rode pytest manualmente; este comando nao executa testes.")
    print("- rode python3 -m compileall src manualmente; este comando nao compila modulos.")
    print("- verifique git status --short manualmente antes de push.")
    print("- faca push somente apos validar testes, compileall, Git, logs, commits e checklist pos-batch.")
    print("limites: diagnostico auxiliar; nao substitui scripts seguros, checklist pos-batch, pytest, compileall, revisao de logs ou revisao de commits.")
    return 0


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


def _find_last_log(logs_directory: Path) -> Path | None:
    if not logs_directory.is_dir():
        return None

    candidates = tuple(
        path
        for path in logs_directory.iterdir()
        if path.is_file() and path.suffix in {".log", ".out"}
    )
    if not candidates:
        return None
    return max(candidates, key=lambda path: (path.stat().st_mtime_ns, path.name))


def _iter_markdown_files(directory: Path, *, ignore_runtime: bool = False) -> tuple[Path, ...]:
    files: list[Path] = []
    for path in directory.rglob("*.md"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DOCS_DIRECTORIES for part in path.parts):
            continue
        if ignore_runtime and "runtime" in path.parts:
            continue
        if "missions" in path.parts and "done" in path.parts:
            continue
        files.append(path)
    return tuple(files)


def _iter_markdown_links(content: str) -> tuple[tuple[int, str], ...]:
    links: list[tuple[int, str]] = []
    in_fenced_code = False

    for line_number, line in enumerate(content.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fenced_code = not in_fenced_code
            continue
        if in_fenced_code:
            continue
        for match in MARKDOWN_LINK_PATTERN.finditer(_remove_inline_code_spans(line)):
            links.append((line_number, match.group(1)))

    return tuple(links)


def _normalize_markdown_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")].strip()
    return target.split()[0] if target.split() else ""


def _remove_inline_code_spans(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def _should_ignore_markdown_link(target: str) -> bool:
    if not target or target.startswith("#"):
        return True
    parsed = urlparse(target)
    if parsed.scheme.lower() in EXTERNAL_LINK_SCHEMES:
        return True
    if parsed.scheme or parsed.netloc:
        return True
    return False


if __name__ == "__main__":
    raise SystemExit(main())

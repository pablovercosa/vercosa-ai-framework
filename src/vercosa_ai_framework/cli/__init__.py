"""CLI operacional inicial do Vercosa AI Framework."""

from importlib import import_module

__all__ = [
    "MissionDirectoryStatus",
    "DiagnosticIssue",
    "DiagnosticResult",
    "ValidationIssue",
    "ValidationResult",
    "build_parser",
    "diagnose_project",
    "main",
    "run",
    "validate_project_structure",
]


def __getattr__(name: str):
    if name in __all__:
        module = import_module("vercosa_ai_framework.cli.main")
        return getattr(module, name)
    raise AttributeError(f"module 'vercosa_ai_framework.cli' has no attribute {name!r}")

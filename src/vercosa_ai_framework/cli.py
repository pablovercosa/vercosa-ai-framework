"""Command line interface for the Vercosa AI Framework."""

from __future__ import annotations

import argparse
import platform
import sys

from vercosa_ai_framework import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser without binding it to a runtime provider."""
    parser = argparse.ArgumentParser(
        prog="vaf",
        description="Vercosa AI Framework command line interface.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the framework version and exit.",
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("diagnose", help="Print basic local environment diagnostics.")
    return parser


def run(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"vercosa-ai-framework {__version__}")
        return 0

    if args.command == "diagnose":
        print(f"vercosa-ai-framework: {__version__}")
        print(f"python: {platform.python_version()}")
        print(f"system: {platform.system() or 'unknown'}")
        print(f"machine: {platform.machine() or 'unknown'}")
        return 0

    parser.print_help()
    return 0


def main() -> None:
    """Console script entrypoint."""
    raise SystemExit(run())


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))

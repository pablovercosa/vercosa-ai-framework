"""Operational CLI for deterministic Usage/API Limit Guard checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from vercosa_ai_framework.guardian.usage_limits import detect_usage_limit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Detecta sinais textuais de limite de uso/API em um log local.",
    )
    parser.add_argument("log_path", help="Caminho do log local a ser inspecionado.")
    args = parser.parse_args(argv)

    log_path = Path(args.log_path)
    try:
        message = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"Uso/API Limit Guard: não foi possível ler o log '{log_path}': {exc}", file=sys.stderr)
        return 2

    detection = detect_usage_limit(
        message,
        origin="mission_log",
        runtime="opencode",
        metadata={"log_path": str(log_path)},
    )

    if not detection.is_usage_limit:
        return 1

    print("Uso/API Limit Guard: limitação externa detectada no log da missão.")
    print(f"Tipo: {detection.limit_type.value}")
    print(f"Severidade: {detection.severity.value}")
    print(f"Ação recomendada: {detection.recommended_action.value}")
    print(f"Parada segura do worker: {'sim' if detection.should_stop_worker else 'não'}")
    print(f"Retry futuro possível: {'sim' if detection.can_retry_later else 'não'}")
    if detection.matched_patterns:
        print(f"Padrões detectados: {', '.join(detection.matched_patterns)}")
    print(f"Mensagem original preservada em: {log_path}")
    print("Ação segura: parar a execução e investigar limites, quota, rate limit ou billing do provider.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

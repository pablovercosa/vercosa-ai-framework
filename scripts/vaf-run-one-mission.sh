#!/usr/bin/env bash
set -euo pipefail

cd /home/projetos/vercosa-ai-framework

mkdir -p missions/queue missions/running missions/done missions/failed logs

MISSION="$(find missions/queue -maxdepth 1 -type f -name '*.md' | sort | head -1)"

if [ -z "${MISSION:-}" ]; then
  echo "Nenhuma missão pendente."
  exit 2
fi

BASE="$(basename "$MISSION")"
NAME="${BASE%.md}"
RUNNING="missions/running/$BASE"
LOG="logs/${NAME}-$(date +%Y%m%d-%H%M%S).log"

mv "$MISSION" "$RUNNING"

echo "== Missão =="
echo "$RUNNING"
echo
echo "== Log =="
echo "$LOG"
echo

set +e

AUTO_ARGS=()
if [ "${VAF_AUTO_APPROVE:-0}" = "1" ]; then
  AUTO_ARGS+=(--auto)
fi

opencode \
  "${AUTO_ARGS[@]}" \
  --print-logs \
  --log-level INFO \
  run "$(cat "$RUNNING")" \
  2>&1 | tee "$LOG"

STATUS="${PIPESTATUS[0]}"
set -e

if [ "$STATUS" -eq 0 ]; then
  mv "$RUNNING" "missions/done/$BASE"

  if [ "${VAF_AUTO_COMMIT:-0}" = "1" ]; then
    git add -A
    if ! git diff --cached --quiet; then
      COMMIT_MESSAGE="${VAF_COMMIT_MESSAGE:-}"
      if [ -z "$COMMIT_MESSAGE" ]; then
        COMMIT_MESSAGE="missão: ${NAME}"
      fi
      git commit -m "$COMMIT_MESSAGE"
    else
      echo "Nenhuma alteração para commit."
    fi
  fi

  echo "Missão concluída: $BASE"
  exit 0
else
  if PYTHONPATH=src python3 -m vercosa_ai_framework.guardian.usage_limit_cli "$LOG"; then
    echo "Falha classificada como limitação externa de uso/API. Worker deve parar para revisão de quota, rate limit ou billing."
  fi
  mv "$RUNNING" "missions/failed/$BASE"
  echo "Missão falhou: $BASE"
  exit "$STATUS"
fi

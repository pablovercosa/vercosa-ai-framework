#!/usr/bin/env bash
set -euo pipefail

cd /home/projetos/vercosa-ai-framework

MAX_CYCLES="${VAF_MAX_CYCLES:-3}"
SLEEP_SECONDS="${VAF_SLEEP_SECONDS:-10}"

echo "VAF Worker iniciado."
echo "MAX_CYCLES=$MAX_CYCLES"
echo "VAF_AUTO_APPROVE=${VAF_AUTO_APPROVE:-0}"
echo "VAF_AUTO_COMMIT=${VAF_AUTO_COMMIT:-0}"
echo

cycle=1

while [ "$cycle" -le "$MAX_CYCLES" ]; do
  echo "== Ciclo $cycle/$MAX_CYCLES =="

  if ! find missions/queue -maxdepth 1 -type f -name '*.md' | grep -q .; then
    echo "Fila vazia. Encerrando worker."
    exit 0
  fi

  if ./scripts/vaf-run-one-mission.sh; then
    echo "Ciclo concluído."
  else
    status="$?"
    if [ "$status" -eq 2 ]; then
      echo "Fila vazia."
      exit 0
    fi
    echo "Erro no ciclo $cycle. Encerrando para revisão."
    exit "$status"
  fi

  cycle=$((cycle + 1))
  sleep "$SLEEP_SECONDS"
done

echo "Limite de ciclos atingido. Encerrando."

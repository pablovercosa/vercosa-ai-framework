#!/usr/bin/env bash
set -euo pipefail

cd /home/projetos/vercosa-ai-framework

if [ ! -f logs/vaf-worker.pid ]; then
  echo "Nenhum PID encontrado."
  exit 0
fi

PID="$(cat logs/vaf-worker.pid)"

if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "Worker parado: $PID"
else
  echo "Processo não está rodando: $PID"
fi

rm -f logs/vaf-worker.pid

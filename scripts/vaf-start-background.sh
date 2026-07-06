#!/usr/bin/env bash
set -euo pipefail

cd /home/projetos/vercosa-ai-framework

mkdir -p logs

if [ -f logs/vaf-worker.pid ] && kill -0 "$(cat logs/vaf-worker.pid)" 2>/dev/null; then
  echo "Worker já está rodando com PID $(cat logs/vaf-worker.pid)"
  exit 0
fi

VAF_MAX_CYCLES="${VAF_MAX_CYCLES:-3}" \
VAF_AUTO_APPROVE="${VAF_AUTO_APPROVE:-1}" \
VAF_AUTO_COMMIT="${VAF_AUTO_COMMIT:-1}" \
VAF_COMMIT_MESSAGE="${VAF_COMMIT_MESSAGE:-}" \
nohup ./scripts/vaf-worker.sh > logs/vaf-worker.out 2>&1 &

echo $! > logs/vaf-worker.pid

echo "Worker iniciado em background."
echo "PID: $(cat logs/vaf-worker.pid)"
echo "Log: logs/vaf-worker.out"

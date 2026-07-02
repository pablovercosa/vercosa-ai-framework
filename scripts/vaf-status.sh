#!/usr/bin/env bash
set -euo pipefail

cd /home/projetos/vercosa-ai-framework

echo "== Git =="
git status --short

echo
echo "== Branch =="
git branch --show-current

echo
echo "== Missions =="
echo "queue:   $(find missions/queue -maxdepth 1 -type f -name '*.md' | wc -l)"
echo "running: $(find missions/running -maxdepth 1 -type f -name '*.md' | wc -l)"
echo "done:    $(find missions/done -maxdepth 1 -type f -name '*.md' | wc -l)"
echo "failed:  $(find missions/failed -maxdepth 1 -type f -name '*.md' | wc -l)"

echo
echo "== Worker =="
if [ -f logs/vaf-worker.pid ] && kill -0 "$(cat logs/vaf-worker.pid)" 2>/dev/null; then
  echo "running: $(cat logs/vaf-worker.pid)"
else
  echo "stopped"
fi

echo
echo "== Last log =="
ls -t logs/*.log logs/*.out 2>/dev/null | head -5 || true

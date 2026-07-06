#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

count_missions() {
  local directory="$1"
  find "$directory" -maxdepth 1 -type f -name '*.md' | wc -l
}

worker_is_running() {
  [ -f logs/vaf-worker.pid ] && kill -0 "$(cat logs/vaf-worker.pid)" 2>/dev/null
}

require_git_clean() {
  if [ -n "$(git status --porcelain)" ]; then
    echo "Git possui alterações pendentes. Faça commit, stash ou limpe o worktree antes de executar."
    git status --short
    exit 1
  fi
}

require_worker_stopped() {
  if worker_is_running; then
    echo "Worker já está em execução com PID $(cat logs/vaf-worker.pid). Pare o worker antes de executar o runner seguro."
    exit 1
  fi
}

require_queue_consistent_before_start() {
  local running_count
  running_count="$(count_missions missions/running)"

  if [ "$running_count" -ne 0 ]; then
    echo "Estado inconsistente: missions/running contém $running_count missão(ões) antes da execução."
    exit 1
  fi
}

require_no_failed_missions() {
  local failed_count
  failed_count="$(count_missions missions/failed)"

  if [ "$failed_count" -ne 0 ]; then
    echo "Há $failed_count missão(ões) em missions/failed. Revise as falhas antes de continuar."
    exit 1
  fi
}

print_summary() {
  local tests_result="$1"
  local compile_result="$2"
  local push_result="$3"

  echo
  echo "== Resumo =="
  echo "Último commit: $(git log -1 --oneline 2>/dev/null || printf 'nenhum commit encontrado')"
  echo "Missões: queue=$(count_missions missions/queue) running=$(count_missions missions/running) done=$(count_missions missions/done) failed=$(count_missions missions/failed)"
  echo "Testes: $tests_result"
  echo "Compileall: $compile_result"
  echo "Push: $push_result"
}

mkdir -p missions/queue missions/running missions/done missions/failed logs

echo "== Preflight =="
require_git_clean
require_worker_stopped
require_queue_consistent_before_start
require_no_failed_missions

export VAF_MAX_CYCLES="${VAF_MAX_CYCLES:-1}"
export VAF_AUTO_APPROVE="${VAF_AUTO_APPROVE:-1}"
export VAF_AUTO_COMMIT="${VAF_AUTO_COMMIT:-1}"

echo "Executando worker em foreground com VAF_MAX_CYCLES=$VAF_MAX_CYCLES."
./scripts/vaf-worker.sh

echo
echo "== Status do worker =="
./scripts/vaf-status.sh

require_worker_stopped

if [ "$(count_missions missions/running)" -ne 0 ]; then
  echo "Estado inconsistente: missions/running não ficou vazio após a execução."
  exit 1
fi

require_no_failed_missions

echo
echo "== Testes =="
pytest
TESTS_RESULT="pytest passou"

echo
echo "== Compileall =="
python3 -m compileall src
COMPILE_RESULT="compileall passou"

if [ "$VAF_AUTO_COMMIT" = "1" ]; then
  require_git_clean
else
  if [ -n "$(git status --porcelain)" ]; then
    echo "VAF_AUTO_COMMIT=0: há alterações pendentes. Faça commit manual antes de push ou entrega final."
    git status --short
  fi
fi

PUSH_RESULT="não solicitado"

if [ "${VAF_AUTO_PUSH:-0}" = "1" ]; then
  echo
  echo "== Push automático =="

  current_branch="$(git branch --show-current)"
  if [ "$current_branch" != "main" ]; then
    echo "Push automático bloqueado: branch atual é '$current_branch', mas somente 'main' é permitida."
    exit 1
  fi

  require_git_clean
  require_worker_stopped
  require_no_failed_missions

  if ! git remote get-url origin >/dev/null 2>&1; then
    echo "Push automático bloqueado: remoto origin não está configurado."
    exit 1
  fi

  git push origin "$current_branch"
  PUSH_RESULT="executado para origin/$current_branch"
fi

print_summary "$TESTS_RESULT" "$COMPILE_RESULT" "$PUSH_RESULT"

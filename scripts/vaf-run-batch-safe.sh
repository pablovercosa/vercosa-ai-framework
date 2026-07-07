#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

MAX_BATCH_SIZE=10
BATCH_SIZE="${VAF_BATCH_SIZE:-3}"
REQUESTED_AUTO_PUSH="${VAF_AUTO_PUSH:-0}"
EXECUTED_MISSIONS=0
TESTS_RESULT="não executado"
COMPILE_RESULT="não executado"
PUSH_RESULT="não solicitado"
SUMMARY_PRINTED=0

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
    echo "Worker já está em execução com PID $(cat logs/vaf-worker.pid). Pare o worker antes de executar o batch seguro."
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
  SUMMARY_PRINTED=1
  echo
  echo "== Resumo do batch seguro =="
  echo "Missões solicitadas: $BATCH_SIZE"
  echo "Missões executadas: $EXECUTED_MISSIONS"
  echo "Último commit: $(git log -1 --oneline 2>/dev/null || printf 'nenhum commit encontrado')"
  echo "Missões: queue=$(count_missions missions/queue) running=$(count_missions missions/running) done=$(count_missions missions/done) failed=$(count_missions missions/failed)"
  echo "Testes: $TESTS_RESULT"
  echo "Compileall: $COMPILE_RESULT"
  echo "Push: $PUSH_RESULT"
}

require_valid_batch_size() {
  if ! [[ "$BATCH_SIZE" =~ ^[0-9]+$ ]]; then
    echo "VAF_BATCH_SIZE deve ser um número inteiro entre 1 e $MAX_BATCH_SIZE."
    exit 1
  fi

  if [ "$BATCH_SIZE" -lt 1 ]; then
    echo "VAF_BATCH_SIZE deve ser maior ou igual a 1."
    exit 1
  fi

  if [ "$BATCH_SIZE" -gt "$MAX_BATCH_SIZE" ]; then
    echo "VAF_BATCH_SIZE=$BATCH_SIZE excede o limite máximo seguro inicial de $MAX_BATCH_SIZE."
    exit 1
  fi
}

run_final_validations() {
  echo
  echo "== Validação final: pytest =="
  pytest
  TESTS_RESULT="pytest passou"

  echo
  echo "== Validação final: compileall =="
  python3 -m compileall src
  COMPILE_RESULT="compileall passou"
}

push_if_requested() {
  if [ "$REQUESTED_AUTO_PUSH" != "1" ]; then
    PUSH_RESULT="não solicitado"
    return
  fi

  echo
  echo "== Push automático ao final do batch =="

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
}

mkdir -p missions/queue missions/running missions/done missions/failed logs

trap 'status=$?; if [ "$SUMMARY_PRINTED" -ne 1 ]; then print_summary; fi; exit "$status"' EXIT

require_valid_batch_size

if [ -n "${VAF_COMMIT_MESSAGE:-}" ]; then
  echo "Aviso: VAF_COMMIT_MESSAGE será repassada para cada missão do batch. Use apenas quando a mesma mensagem fizer sentido para todos os commits."
fi

echo "== Batch seguro =="
echo "VAF_BATCH_SIZE=$BATCH_SIZE"
echo "VAF_AUTO_PUSH=$REQUESTED_AUTO_PUSH"

if [ "$(count_missions missions/queue)" -eq 0 ]; then
  echo "Nenhuma missão pendente. Encerrando batch seguro."
  print_summary
  exit 0
fi

while [ "$EXECUTED_MISSIONS" -lt "$BATCH_SIZE" ]; do
  if [ "$(count_missions missions/queue)" -eq 0 ]; then
    echo "Nenhuma missão pendente. Encerrando batch seguro."
    break
  fi

  echo
  echo "== Missão $((EXECUTED_MISSIONS + 1))/$BATCH_SIZE =="

  VAF_AUTO_PUSH=0 ./scripts/vaf-run-next-safe.sh
  EXECUTED_MISSIONS=$((EXECUTED_MISSIONS + 1))

  require_git_clean
  require_worker_stopped
  require_no_failed_missions

  if [ "$(count_missions missions/running)" -ne 0 ]; then
    echo "Estado inconsistente: missions/running não ficou vazio após a missão."
    exit 1
  fi
done

run_final_validations
require_git_clean
require_worker_stopped
require_no_failed_missions
push_if_requested
print_summary

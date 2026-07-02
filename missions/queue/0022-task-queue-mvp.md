Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0007-task-queue.md
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/workflows/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP operacional da Task Queue.

Entregáveis esperados:
- atualizar src/vercosa_ai_framework/tasks/queue.py
- criar src/vercosa_ai_framework/tasks/scheduler.py
- tests/test_task_scheduler.py
- docs/task-queue.md

Requisitos:
- selecionar próxima task por dependência, prioridade e ordem de criação;
- bloquear task quando dependência falhar;
- permitir retries com limite de tentativas;
- marcar task como running, done, failed, skipped ou blocked;
- manter execução determinística;
- não executar OpenCode real;
- não usar subprocess;
- não usar sudo;
- não acessar configs globais.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

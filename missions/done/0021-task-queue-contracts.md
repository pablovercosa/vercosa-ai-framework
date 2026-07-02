Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0007-task-queue.md
- src/vercosa_ai_framework/workflows/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python da Task Queue interna.

Entregáveis esperados:
- src/vercosa_ai_framework/tasks/__init__.py
- src/vercosa_ai_framework/tasks/types.py
- src/vercosa_ai_framework/tasks/queue.py
- tests/test_task_queue_contracts.py

Requisitos:
- criar Task;
- criar TaskQueue;
- criar TaskPriority;
- criar TaskQueueState;
- criar TaskAttempt;
- criar TaskQueueResult, se necessário;
- suportar adicionar task;
- suportar listar por estado;
- suportar próxima task executável;
- respeitar dependências simples;
- não executar RuntimeAdapter;
- não chamar OpenCode real;
- não chamar APIs externas;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0006-workflow-engine.md
- src/vercosa_ai_framework/workflows/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/runtime/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP do Workflow Engine.

Entregáveis esperados:
- src/vercosa_ai_framework/workflows/engine.py
- tests/test_workflow_engine.py
- docs/workflow-engine.md

Requisitos:
- executar tasks sequencialmente;
- respeitar dependências simples;
- bloquear workflow se task obrigatória falhar;
- pular task se dependência falhou;
- integrar Guardian Engine antes de executar task;
- usar RuntimeAdapter abstrato;
- não executar OpenCode real nos testes;
- não usar subprocess real nos testes;
- não usar sudo.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

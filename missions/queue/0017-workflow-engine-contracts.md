Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0006-workflow-engine.md
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/model_selection/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais do Workflow Engine.

Entregáveis esperados:
- src/vercosa_ai_framework/workflows/__init__.py
- src/vercosa_ai_framework/workflows/types.py
- tests/test_workflow_contracts.py

Requisitos:
- criar Workflow;
- criar WorkflowTask;
- criar WorkflowStatus;
- criar TaskStatus;
- criar TaskDependency;
- criar WorkflowResult;
- criar TaskResult;
- não executar OpenCode real;
- não chamar APIs externas;
- manter provider agnostic;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

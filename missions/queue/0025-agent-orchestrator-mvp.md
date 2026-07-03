Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0008-agent-orchestrator.md
- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/runtime/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP do Agent Orchestrator.

Entregáveis esperados:
- src/vercosa_ai_framework/agents/orchestrator.py
- tests/test_agent_orchestrator.py
- docs/agent-orchestrator.md

Requisitos:
- receber uma task;
- escolher agente compatível por role/domínio/tags;
- validar execução com Guardian Engine;
- selecionar modelo via Model Selection Engine quando catálogo/política forem fornecidos;
- montar AgentExecutionRequest;
- executar via RuntimeAdapter abstrato;
- retornar AgentExecutionResult;
- suportar erro quando nenhum agente compatível existir;
- suportar estado simples: planning -> executing -> validating -> done/failed;
- não executar OpenCode real nos testes;
- não chamar APIs externas;
- não usar subprocess real;
- não usar sudo;
- manter MCP fora dos agentes.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

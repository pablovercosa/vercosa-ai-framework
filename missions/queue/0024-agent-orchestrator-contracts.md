Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0008-agent-orchestrator.md
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/runtime/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais do Agent Orchestrator.

Entregáveis esperados:
- src/vercosa_ai_framework/agents/__init__.py
- src/vercosa_ai_framework/agents/types.py
- src/vercosa_ai_framework/agents/registry.py
- tests/test_agent_contracts.py
- tests/test_agent_registry.py

Requisitos:
- criar AgentProfile;
- criar AgentRole;
- criar AgentMode;
- criar AgentState;
- criar AgentCapabilityRequest;
- criar AgentExecutionRequest;
- criar AgentExecutionResult;
- criar AgentRegistry em memória;
- suportar registrar agentes;
- suportar buscar agente por role;
- suportar filtrar por tags/domínio;
- não executar OpenCode real;
- não chamar APIs externas;
- não usar subprocess;
- manter provider agnostic;
- manter MCP fora dos agentes.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

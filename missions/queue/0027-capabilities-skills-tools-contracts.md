Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0009-capabilities-skills-tools.md
- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais para Capabilities, Skills e Tools.

Entregáveis esperados:
- src/vercosa_ai_framework/capabilities/__init__.py
- src/vercosa_ai_framework/capabilities/types.py
- src/vercosa_ai_framework/capabilities/registry.py
- src/vercosa_ai_framework/skills/__init__.py
- src/vercosa_ai_framework/skills/types.py
- src/vercosa_ai_framework/skills/registry.py
- src/vercosa_ai_framework/tools/__init__.py
- src/vercosa_ai_framework/tools/types.py
- src/vercosa_ai_framework/tools/registry.py
- tests/test_capability_contracts.py
- tests/test_skill_contracts.py
- tests/test_tool_contracts.py

Requisitos:
- criar CapabilityProfile;
- criar SkillProfile;
- criar ToolProfile;
- criar CapabilityRequest;
- criar SkillExecutionRequest;
- criar ToolExecutionRequest;
- criar SkillExecutionResult;
- criar ToolExecutionResult;
- criar registries em memória;
- suportar busca por nome, tags e domínio;
- não executar ferramentas reais;
- não chamar APIs externas;
- não usar subprocess;
- manter MCP fora dos agentes.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

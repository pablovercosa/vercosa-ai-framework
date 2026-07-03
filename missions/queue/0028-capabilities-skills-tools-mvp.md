Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0009-capabilities-skills-tools.md
- src/vercosa_ai_framework/capabilities/
- src/vercosa_ai_framework/skills/
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP da resolução Capability -> Skill -> Tool.

Entregáveis esperados:
- src/vercosa_ai_framework/capabilities/resolver.py
- src/vercosa_ai_framework/skills/executor.py
- src/vercosa_ai_framework/tools/executor.py
- tests/test_capability_resolution.py
- tests/test_skill_executor.py
- tests/test_tool_executor.py
- docs/capabilities-skills-tools.md

Requisitos:
- CapabilityResolver deve mapear uma CapabilityRequest para SkillProfile compatível;
- SkillExecutor deve montar uma ToolExecutionRequest;
- ToolExecutor deve usar ToolAdapter abstrato ou callable injetável;
- integrar Guardian Engine antes de executar Tool;
- bloquear tool quando Guardian bloquear;
- suportar dry_run;
- suportar fallback simples de skills/tools;
- não executar ferramentas reais nos testes;
- não chamar APIs externas;
- não usar subprocess real nos testes;
- não usar sudo;
- manter provider agnostic;
- manter MCP fora dos agentes.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

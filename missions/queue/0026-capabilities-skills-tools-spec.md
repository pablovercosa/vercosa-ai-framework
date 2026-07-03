Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0008-agent-orchestrator.md
- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/guardian/

Assuma o papel de framework-architect.

Missão:
Criar a Spec da camada Capabilities, Skills e Tools do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0009-capabilities-skills-tools.md

A Spec deve cobrir:
- diferença entre Capability, Skill e Tool;
- regra central: agente não conhece MCP diretamente;
- Capability como intenção funcional;
- Skill como procedimento reutilizável;
- Tool como execução concreta;
- Provider/MCP/API como infraestrutura externa;
- Capability Registry;
- Skill Registry;
- Tool Registry;
- permissões;
- integração com Guardian Engine;
- integração com Agent Orchestrator;
- integração futura com Policy Engine;
- segurança contra tool misuse;
- segurança contra prompt injection;
- rastreabilidade;
- logs;
- fallback de tools;
- provider agnostic;
- OpenCode como runtime inicial, não núcleo.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

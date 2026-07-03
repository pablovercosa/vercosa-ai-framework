Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0006-workflow-engine.md
- specs/framework/0007-task-queue.md
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/workflows/

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Agent Orchestrator do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0008-agent-orchestrator.md

A Spec deve cobrir:
- papel do Agent Orchestrator na arquitetura;
- relação Task Queue -> Agent Orchestrator -> Agents -> Subagents;
- agentes como state machines;
- estados: idle, planning, executing, reflecting, validating, replanning, done, failed;
- separação entre Agent, Capability, Skill, Tool, Provider e MCP;
- regra: agente não conhece MCP diretamente;
- seleção de agente por role, domínio, complexidade e risco;
- integração com Model Selection Engine;
- integração com Guardian Engine;
- integração com Runtime Adapter;
- execução inicial sequencial;
- execução paralela futura;
- delegação para subagents;
- critérios de parada;
- limites de custo/tokens/ciclos;
- logs e rastreabilidade;
- segurança contra prompt injection;
- provider agnostic;
- OpenCode como runtime inicial, não núcleo.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

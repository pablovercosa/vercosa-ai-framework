Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0006-workflow-engine.md
- src/vercosa_ai_framework/workflows/

Assuma o papel de framework-architect.

Missão:
Criar a Spec da Task Queue interna do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0007-task-queue.md

A Spec deve cobrir:
- diferença entre Mission Queue e Task Queue;
- Task Queue como componente interno do Workflow Engine;
- estados de task: queued, running, done, failed, blocked, skipped, cancelled;
- prioridade;
- dependências;
- retries;
- backoff;
- limite de tentativas;
- ordenação determinística;
- execução sequencial inicial;
- execução paralela futura;
- integração com Guardian Engine;
- integração com Runtime Adapter;
- integração futura com Agent Orchestrator;
- logs;
- rastreabilidade;
- persistência local inicial;
- provider agnostic;
- segurança e limites.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0004-mission-runner.md
- specs/framework/0006-workflow-engine.md
- specs/framework/0011-knowledge-hub.md
- specs/framework/0012-canonicalizer.md
- src/vercosa_ai_framework/

Assuma o papel de framework-architect.

Missão:
Criar a Spec da Persistence Layer do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0013-persistence-layer.md

A Spec deve cobrir:
- persistência como porta/adaptador;
- storage agnostic;
- armazenamento inicial em memória e filesystem;
- suporte futuro a SQLite, PostgreSQL e PostgreSQL + pgvector;
- persistência de Missions;
- persistência de Workflows;
- persistência de Tasks;
- persistência de Knowledge Documents;
- persistência de Canonical Documents;
- persistência de Guardian Decisions;
- persistência de Model Decisions;
- logs e audit trail;
- serialização determinística;
- versionamento de schema;
- migrations futuras;
- segurança de segredos;
- redaction;
- backup;
- rastreabilidade;
- limites de dados;
- integração com Provider Gateway;
- integração com Guardian Engine;
- provider agnostic.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

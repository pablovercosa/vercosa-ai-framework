Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0002-model-selection-engine.md

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Mission Runner.

Entregável obrigatório:
- specs/framework/0004-mission-runner.md

A Spec deve cobrir:
- conceito de Mission;
- fila de missões;
- estados: queued, running, done, failed, cancelled;
- execução em ciclos;
- limite de ciclos;
- logs;
- auto-commit;
- validação;
- critérios de aceite;
- rollback ou revisão manual;
- orçamento de tokens/custo;
- políticas de segurança;
- execução local;
- execução futura via systemd;
- execução futura via API;
- integração com Guardian Specs;
- integração futura com Workflow Engine.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

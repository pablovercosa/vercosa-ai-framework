Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0004-mission-runner.md
- specs/framework/0005-guardian-engine.md

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Workflow Engine.

Entregável obrigatório:
- specs/framework/0006-workflow-engine.md

A Spec deve cobrir:
- relação Mission -> Workflow -> Task;
- decomposição de missão em tarefas;
- estados de workflow;
- estados de task;
- dependências entre tarefas;
- execução sequencial inicial;
- execução paralela futura;
- integração com Guardian Engine;
- integração com Model Selection Engine;
- integração com Mission Runner;
- critérios de aceite por task;
- logs;
- rastreabilidade;
- retries;
- limites de custo/tokens/ciclos;
- encerramento seguro;
- relação futura com Agent Orchestrator.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

---
id: "0104"
title: "Integrar Mission Runner Workflow Engine e Task Queue"
base_contract: "v1"
roles:
  - integration-architect
  - workflow-engineer
  - task-queue-engineer
  - test-engineer
agents:
  - framework-architect
network: deny
database: deny
providers: deny
git_push: deny
git_tag: deny
release: deny
package_publish: deny
sudo: deny
destructive_commands: deny
---

# Objetivo

Integrar Mission Runner, Workflow Engine, Task Queue e Task Scheduler em um fluxo mínimo, determinístico, validável e inteiramente local, preservando as responsabilidades arquiteturais de cada componente e a compatibilidade com os caminhos legados existentes.

O fluxo mínimo esperado é:

Mission
-> Mission Runner
-> resolução de Workflow
-> Workflow Engine
-> Task Queue
-> Task Scheduler
-> executor injetado
-> Workflow Result
-> Mission Result

# Contexto Específico

A auditoria da missão 0101 classificou o projeto como `ALINHADO COM RESSALVAS` e identificou como lacuna prioritária a ausência de integração real entre Mission Runner, Workflow Engine e Task Queue.

A missão 0103 explicitou o fluxo de valor pretendido e confirmou que o Mission Runner é infraestrutura operacional, não o produto inteiro.

A implementação atual possui três caminhos independentes:

1. `MissionRunner` controla o ciclo de vida da Mission, mas chama diretamente `RuntimeAdapter.execute_mission()`.

2. `WorkflowEngine` percorre `WorkflowTask` em um loop próprio e chama diretamente `RuntimeAdapter.execute_task()`.

3. `TaskQueue` e `TaskScheduler` mantêm outro loop operacional sobre `tasks.Task`, usando um executor injetado.

Também existem dois contratos de tarefa:

- `vercosa_ai_framework.workflows.WorkflowTask`;
- `vercosa_ai_framework.tasks.Task`.

Eles possuem campos, estados e responsabilidades diferentes.

A integração não pode simplesmente encadear os loops existentes, pois isso produziria duplicação de execução, estados concorrentes e tentativas inconsistentes.

No caminho integrado desta missão:

- Mission Runner deve continuar responsável pela fila, pelo estado global da Mission, pelos limites globais, pela validação final e pelo encerramento;
- Workflow Engine deve continuar responsável pela semântica, pelo estado e pelo resultado do Workflow;
- Task Queue deve controlar estado operacional, dependências, elegibilidade, tentativas e retries;
- Task Scheduler deve ser o único loop que avança Tasks no caminho integrado;
- o executor injetado deve executar a Task elegível sem permitir que Task Queue conheça agentes, tools, providers ou OpenCode;
- a Mission somente pode ser concluída após recomendação compatível do Workflow Result e validação final do Mission Runner.

A missão não deve implementar um Mission Orchestrator completo.

A resolução da Mission para um Workflow deve ocorrer por contrato pequeno, explícito e injetável.

# Entradas Específicas

## Código

- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/workflows/
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/audit/

## Testes

- tests/test_mission_runner.py
- tests/test_mission_runner_guardian.py
- tests/test_workflow_contracts.py
- tests/test_workflow_engine.py
- tests/test_task_queue_contracts.py
- tests/test_task_scheduler.py
- tests/test_audit_mission_events.py

## Specs E Documentação

- specs/framework/0004-mission-runner.md
- specs/framework/0006-workflow-engine.md
- specs/framework/0007-task-queue.md
- docs/mission-runner.md
- docs/workflow-engine.md
- docs/task-queue.md
- docs/alignment/architecture-map.md
- docs/alignment/current-state.md
- docs/alignment/implementation-status.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/roadmap/mission-backlog.md
- README.md
- CHANGELOG.md

# Arquitetura Obrigatória

## 1. Responsabilidades

Mission Runner deve:

- controlar estado global da Mission;
- iniciar e encerrar a Mission;
- aplicar avaliação de missão já existente;
- fornecer a Mission normalizada à integração;
- receber resultado normalizado do Workflow;
- validar artefatos globais;
- decidir o estado terminal da Mission;
- preservar auto-commit existente;
- preservar eventos de missão existentes.

Mission Runner não deve:

- decompor diretamente uma Mission complexa em Tasks;
- controlar dependências internas de Tasks;
- executar o loop da Task Queue;
- escolher agentes;
- resolver capabilities;
- executar tools;
- chamar providers;
- conhecer detalhes internos do Task Scheduler.

Workflow Engine deve:

- receber ou resolver um Workflow associado à Mission;
- validar o Workflow;
- materializar as Tasks operacionais;
- preservar semântica e rastreabilidade do Workflow;
- fornecer o executor de Task ao Task Scheduler;
- converter estados e resultados operacionais em WorkflowTask e TaskResult;
- produzir WorkflowResult e recomendação de encerramento.

Workflow Engine não deve:

- alterar o estado global da Mission;
- manter um segundo loop de execução sobre as mesmas Tasks no caminho integrado;
- escolher agentes;
- chamar providers diretamente;
- executar OpenCode diretamente.

Task Queue deve:

- controlar elegibilidade;
- controlar estado operacional;
- controlar dependências;
- registrar tentativas;
- aplicar retries finitos;
- preservar ordenação determinística;
- reportar estados ao Workflow Engine.

Task Queue não deve:

- planejar Workflow;
- marcar Mission como concluída;
- avaliar objetivo global da Mission;
- escolher agentes;
- conhecer WorkflowTask diretamente, caso isso crie dependência circular;
- chamar runtime, provider, tool ou OpenCode.

Task Scheduler deve:

- ser o único loop de avanço das Tasks no caminho integrado;
- usar executor injetado;
- normalizar exceções do executor;
- respeitar Task Queue;
- retornar resultado determinístico ao Workflow Engine.

## 2. Direção De Dependências

A direção preferencial deve ser:

missions
-> workflows
-> tasks

O módulo `tasks` não deve importar:

- missions;
- workflows;
- agents;
- capabilities;
- skills;
- tools;
- providers.

O mapeamento entre WorkflowTask e Task deve ficar na camada de workflows ou em módulo de integração acima de tasks.

Evitar import circular.

## 3. Resolução De Workflow

Criar um contrato pequeno e injetável para obter um Workflow a partir de uma Mission.

O nome pode seguir a convenção real do projeto, por exemplo:

- WorkflowProvider;
- MissionWorkflowProvider;
- WorkflowResolver;
- MissionWorkflowExecutor.

A decisão final deve ser simples e documentada.

O contrato deve:

- receber uma Mission normalizada;
- retornar um Workflow válido ou erro claro;
- ser determinístico;
- não acessar rede;
- não acessar banco;
- não chamar provider;
- não decompor silenciosamente a Mission dentro do Mission Runner.

Nos testes, usar implementação em memória ou fake explícito.

Não implementar catálogo persistente de workflows nesta missão.

## 4. Caminho Integrado Do Mission Runner

Mission Runner deve aceitar o caminho integrado por injeção explícita.

Requisitos:

- preservar o comportamento legado quando nenhuma integração de Workflow for configurada;
- não chamar `runtime.execute_mission()` quando o caminho de Workflow estiver configurado;
- não alterar a API legada sem compatibilidade;
- falhar claramente quando a integração estiver parcialmente configurada;
- não marcar a Mission como done antes do Workflow Result;
- mapear falha, pausa, revisão e cancelamento de forma conservadora;
- usar `requires_review=True` quando não houver estado equivalente seguro;
- não ocultar erro do Workflow;
- preservar artefatos, validações, warnings, errors e audit references quando disponíveis.

Preferir serviço ou bridge separado para impedir que `MissionRunner` acumule lógica de Workflow.

## 5. Task Queue Como Substrato Operacional

No caminho integrado, o Workflow Engine deve usar Task Queue e Task Scheduler como substrato operacional.

Pode haver compatibilidade temporária com o caminho direto antigo, mas:

- o novo teste de integração não pode usar o loop direto legado;
- somente Task Scheduler deve avançar as Tasks no caminho integrado;
- a mesma Task não pode ser executada duas vezes por loops distintos;
- tentativas e retries devem pertencer à Task Queue;
- Workflow Engine deve observar o resultado da Queue e produzir WorkflowResult.

Se o caminho direto antigo permanecer, ele deve ser identificado claramente como compatibilidade legada e não como fluxo canônico novo.

## 6. Mapeamento WorkflowTask Para Task

Criar mapeamento explícito, determinístico e testável.

Preservar no mínimo:

- mission_id;
- workflow_id;
- task_id;
- title;
- goal;
- task_type;
- priority;
- risk_level;
- required_capabilities;
- dependências obrigatórias;
- política de retry;
- limites de execução;
- critérios de aceite;
- entradas;
- saídas esperadas;
- política de modelo;
- política de validação;
- referências de auditoria quando existentes.

Regras:

- `task_id` deve ser preservado;
- dependências obrigatórias devem virar dependências operacionais da Queue;
- dependências opcionais devem ser preservadas em metadata ou estrutura equivalente;
- `max_attempts` deve derivar de retry policy de forma explícita;
- campos sem equivalente direto devem ser preservados em metadata, não descartados silenciosamente;
- o mapeamento inverso deve preservar estado, artefatos, tentativas e erro;
- nenhuma conversão pode alterar os objetos de origem;
- campos ausentes devem usar defaults documentados;
- valores inválidos devem produzir erro claro antes da execução.

Documentar a tabela de conversão.

## 7. Mapeamento De Estados

Definir e testar o mapeamento entre:

Workflow TaskStatus:

- pending;
- ready;
- running;
- blocked;
- validating;
- done;
- failed;
- skipped;
- cancelled.

Task Queue State:

- queued;
- running;
- done;
- failed;
- blocked;
- skipped;
- cancelled.

O mapeamento deve:

- ser explícito;
- preservar estados terminais;
- não marcar done antes da validação aplicável;
- tratar estado validating sem inventar estado inexistente na Queue;
- tratar blocked e review de forma conservadora;
- registrar divergência quando não houver equivalência exata.

## 8. Execução Da Task

O executor fornecido ao Task Scheduler deve:

- receber Task e TaskAttempt;
- recuperar o contexto correspondente da WorkflowTask;
- executar avaliação Guardian já pertencente ao Workflow Engine;
- chamar RuntimeAdapter.execute_task();
- normalizar RuntimeExecutionResult em TaskExecutionOutcome;
- preservar artefatos e erros;
- não acessar rede nos testes;
- não chamar provider real;
- não escolher agente;
- não resolver capability;
- não chamar tool.

Pode usar fakes nos testes.

A Task Queue e o Task Scheduler devem permanecer runtime agnostic.

## 9. Resultado Do Workflow

Workflow Engine deve produzir WorkflowResult com:

- workflow_id;
- mission_id;
- status;
- TaskResults;
- artefatos consolidados;
- validações;
- warnings;
- errors;
- requires_review;
- audit_log_ref;
- recomendação de encerramento.

A recomendação deve distinguir, quando aplicável:

- conclude;
- fail;
- review;
- cancel;
- pause.

Não ocultar Tasks bloqueadas, puladas ou canceladas.

## 10. Encerramento Da Mission

Mission Runner deve concluir a Mission somente quando:

- o Workflow Result estiver concluído;
- a recomendação for compatível com conclusão;
- as validações globais da Mission passarem;
- o auto-commit, quando habilitado, passar.

Mission Runner deve falhar ou solicitar revisão de forma conservadora quando:

- Workflow falhar;
- Workflow ficar bloqueado;
- Workflow exigir aprovação;
- não existir Workflow;
- IDs de Mission e Workflow divergirem;
- resultado do Workflow for inconsistente;
- recomendação de encerramento não for reconhecida.

# Entregáveis

## Código

Criar ou atualizar os módulos necessários para:

- contrato de resolução Mission para Workflow;
- integração Mission Runner para Workflow;
- materialização WorkflowTask para Task;
- execução queue-backed do Workflow;
- mapeamento de resultados;
- compatibilidade legada.

Preferir módulos pequenos.

Não colocar toda a integração em `runner.py` ou `engine.py`.

## Testes

Criar:

- tests/test_mission_workflow_task_integration.py

Atualizar testes existentes apenas quando necessário.

## Documentação

Criar:

- docs/architecture/mission-workflow-task-integration.md

Criar ou atualizar um exemplo local mínimo, preferencialmente:

- docs/examples/minimal-mission-workflow-task-flow.md

Atualizar quando necessário:

- README.md;
- CHANGELOG.md;
- docs/mission-runner.md;
- docs/workflow-engine.md;
- docs/task-queue.md;
- docs/alignment/architecture-map.md;
- docs/alignment/current-state.md;
- docs/alignment/implementation-status.md;
- docs/alignment/roadmap.md;
- docs/alignment/open-questions.md;
- docs/architecture/module-index.md;
- docs/roadmap/mission-backlog.md;
- READMEs internos dos módulos alterados.

Não reescrever Specs nesta missão.

Registrar divergências que deverão ser revisadas pela missão 0108.

# Testes Obrigatórios

## Fluxo Bem-Sucedido

Testar uma Mission com Workflow de pelo menos duas Tasks dependentes.

Confirmar:

- Mission sai de queued para running;
- Workflow é resolvido;
- Workflow Task é materializada na Task Queue;
- Task Scheduler executa em ordem;
- dependência é respeitada;
- tentativa é criada;
- cada Task é executada uma única vez;
- artefatos retornam ao Workflow;
- Workflow termina done;
- Mission termina done;
- IDs permanecem rastreáveis.

## Falha De Task Obrigatória

Confirmar:

- Task obrigatória falha;
- retry respeita max_attempts;
- dependentes não executam;
- estado bloqueado ou pulado é preservado;
- Workflow termina failed;
- Mission termina failed;
- erro aparece no MissionResult.

## Compatibilidade Legada

Confirmar:

- MissionRunner sem integração de Workflow mantém o comportamento atual;
- testes existentes continuam passando;
- runtime.execute_mission continua usado apenas no caminho legado;
- o caminho integrado não chama runtime.execute_mission.

## Fronteiras

Confirmar:

- tasks não importa workflows ou missions;
- Task Queue não chama runtime;
- Task Queue não chama provider;
- Task Queue não chama agente;
- Task Scheduler usa executor injetado;
- Workflow Engine não mantém segundo loop concorrente no caminho integrado;
- Mission Runner não manipula dependências internas de Tasks.

## Segurança E Isolamento

Confirmar:

- nenhum teste acessa rede;
- nenhum teste acessa banco;
- nenhum teste chama provider real;
- nenhum teste chama OpenCode;
- nenhum teste usa subprocesso real;
- nenhuma dependência externa é adicionada.

## Regressão

Executar:

- pytest;
- python3 -m compileall src;
- validação de links da documentação disponível.

# Restrições Específicas

- Não implementar Mission Orchestrator completo.
- Não implementar Agent Orchestrator.
- Não integrar capabilities.
- Não integrar skills.
- Não integrar tools.
- Não integrar Provider Gateway.
- Não chamar providers reais.
- Não alterar scripts shell.
- Não alterar workflow de CI.
- Não alterar compositor de missões.
- Não alterar contrato base de execução.
- Não criar agentes operacionais.
- Não adicionar dependências.
- Não acessar rede.
- Não acessar banco.
- Não implementar persistência externa.
- Não implementar PostgreSQL.
- Não implementar pgvector.
- Não implementar RAG.
- Não implementar internacionalização.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não fazer push.
- Não ampliar silenciosamente o escopo.
- Não declarar fluxo Agent, Capability, Skill, Tool ou Provider como integrado.
- Não tratar teste unitário isolado como prova do fluxo integrado.
- Não reescrever Specs nesta missão.

# Critérios Específicos De Aceite

- Existe fluxo integrado Mission Runner -> Workflow Engine -> Task Queue.
- Task Scheduler é o único loop operacional de Tasks nesse fluxo.
- Mission Runner não executa diretamente a Mission via runtime no caminho integrado.
- Workflow Engine não executa um segundo loop concorrente no caminho integrado.
- WorkflowTask é convertida explicitamente em Task.
- O mapeamento preserva IDs, dependências, prioridades, retries, limites e critérios.
- Estados são convertidos explicitamente.
- Tentativas pertencem à Task Queue.
- Retries pertencem à Task Queue.
- Resultado da Queue retorna ao Workflow Engine.
- WorkflowResult retorna ao Mission Runner.
- Mission só termina após resultado e validação do Workflow.
- Fluxo bem-sucedido com duas Tasks é testado.
- Falha de Task obrigatória é testada.
- Compatibilidade legada é preservada.
- Não existe chamada de provider real.
- Não existe chamada de Agent Orchestrator.
- Não existe chamada de capabilities, skills ou tools.
- Não existe acesso a rede ou banco.
- Não existe nova dependência externa.
- Documentação diferencia fluxo integrado, compatibilidade legada e limites.
- implementation-status registra a integração como validada somente se o teste ponta a ponta passar.
- backlog marca 0104 concluída sem antecipar 0105.
- Specs não foram reescritas.
- pytest passa.
- python3 -m compileall src passa.
- links da documentação passam.
- commit automático usa mensagem em português do Brasil.

# Referência Operacional

O contrato base de execução está em `missions/base/EXECUTION_CONTRACT.md` e é composto obrigatoriamente pelo runner. Não copie o contrato para dentro da missão.

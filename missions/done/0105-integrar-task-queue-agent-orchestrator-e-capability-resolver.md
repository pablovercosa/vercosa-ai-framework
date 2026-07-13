---
id: "0105"
title: "Integrar Task Queue Agent Orchestrator e Capability Resolver"
base_contract: "v1"
roles:
  - integration-architect
  - agent-orchestration-engineer
  - capability-governance-engineer
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

Integrar o caminho mínimo:

Task Queue
-> Task Scheduler
-> Agent Orchestrator
-> Capability Resolver
-> Runtime Adapter
-> Agent Execution Result
-> Task Execution Outcome
-> Task Queue

A integração deve ser determinística, local, testável e compatível com o fluxo Mission Runner -> Workflow Engine -> Task Queue concluído na missão 0104.

A missão deve demonstrar que uma Task elegível pode ser executada por um Agent Profile compatível somente após a resolução declarativa de suas Capabilities obrigatórias.

A missão não deve executar Skills, Tools, MCPs, APIs ou Providers.

# Contexto Específico

A missão 0104 integrou Mission Runner, Workflow Engine e Task Queue por contratos injetáveis.

No fluxo integrado atual:

- Mission Runner controla o ciclo global da Mission;
- Workflow Engine controla a semântica e o resultado do Workflow;
- Task Queue controla estado, dependências, tentativas e retries;
- Task Scheduler é o único loop operacional das Tasks;
- um executor injetado realiza a execução concreta da Task.

O próximo executor canônico deve usar o Agent Orchestrator.

A implementação existente já oferece:

- `TaskScheduler.run_until_idle(queue, executor)`;
- `AgentOrchestrator.execute_task(task, attempt)`;
- `AgentRegistry`;
- `AgentProfile`;
- `AgentExecutionRequest`;
- `AgentExecutionResult`;
- `CapabilityRegistry`;
- `CapabilityResolver`;
- `CapabilityRequest`;
- `CapabilityResolutionResult`;
- registries declarativos de Skills;
- Runtime Adapter injetável.

Entretanto, esses módulos ainda não formam um fluxo operacional único.

O Agent Orchestrator atualmente:

- recebe `Task` e `TaskAttempt`;
- seleciona Agent Profile;
- cria `agent_assignment_id`;
- consulta Guardian;
- pode consultar Model Selection;
- chama Runtime Adapter;
- devolve AgentExecutionResult.

O Capability Resolver atualmente:

- recebe CapabilityRequest;
- seleciona Capability Profile;
- valida permissões;
- pode consultar Guardian;
- seleciona Skill Profile compatível;
- devolve CapabilityResolutionResult;
- não executa Skills ou Tools.

Nesta missão, selecionar um Skill Profile significa apenas registrar uma resolução declarativa da Capability.

Não significa que a Skill foi executada, que uma Tool está disponível ou que um Provider foi chamado.

# Entradas Específicas

## Código

- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/capabilities/
- src/vercosa_ai_framework/skills/
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/workflows/
- src/vercosa_ai_framework/missions/

## Testes

- tests/test_task_queue_contracts.py
- tests/test_task_scheduler.py
- tests/test_agent_contracts.py
- tests/test_agent_registry.py
- tests/test_agent_orchestrator.py
- tests/test_capability_contracts.py
- tests/test_capability_resolution.py
- tests/test_mission_workflow_task_integration.py

## Specs E Documentação

- specs/framework/0007-task-queue.md
- specs/framework/0008-agent-orchestrator.md
- specs/framework/0009-capabilities-skills-tools.md
- docs/task-queue.md
- docs/agent-orchestrator.md
- docs/capabilities-skills-tools.md
- docs/architecture/mission-workflow-task-integration.md
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

## 1. Fronteira Task Queue Para Agent Orchestrator

Criar uma ponte pequena e explícita entre o executor injetado do Task Scheduler e o Agent Orchestrator.

A ponte pode assumir nome coerente com o projeto, por exemplo:

- AgentTaskExecutor;
- TaskAgentExecutor;
- AgentOrchestratorTaskExecutor;
- TaskExecutionBridge.

A ponte deve implementar o contrato funcional:

- receber `Task`;
- receber `TaskAttempt`;
- chamar o Agent Orchestrator;
- normalizar AgentExecutionResult;
- devolver TaskExecutionOutcome.

A Task Queue e o Task Scheduler não devem:

- importar AgentRegistry;
- selecionar Agent Profile;
- criar Agent Assignment;
- resolver Capability;
- chamar Runtime Adapter;
- chamar Skill;
- chamar Tool;
- chamar Provider.

O módulo `tasks` deve continuar dependendo somente do contrato de executor injetado.

## 2. Responsabilidade Do Agent Orchestrator

O Agent Orchestrator deve continuar responsável por:

- selecionar Agent Profile compatível;
- criar um único Agent Assignment por tentativa;
- preservar `mission_id`;
- preservar `workflow_id`;
- preservar `task_id`;
- preservar `attempt_id`;
- gerar e preservar `agent_assignment_id`;
- aplicar Guardian nos pontos já definidos;
- aplicar Model Selection somente quando configurado;
- construir AgentExecutionRequest;
- chamar Runtime Adapter;
- normalizar AgentExecutionResult.

O Agent Orchestrator não deve:

- alterar estado da Task Queue;
- controlar retries da Task;
- alterar dependências;
- alterar prioridade;
- marcar Mission ou Workflow como concluído;
- executar Skill;
- executar Tool;
- acessar MCP;
- acessar Provider diretamente;
- acessar rede;
- acessar banco;
- chamar OpenCode diretamente.

## 3. Integração Com Capability Resolver

Integrar Capability Resolver ao ciclo do Agent Assignment por contrato explícito e injetável.

A integração pode ocorrer:

- dentro do Agent Orchestrator por dependência opcional; ou
- em um serviço de preparação de Agent Assignment usado pelo Agent Orchestrator.

A decisão deve preservar separação de responsabilidades e evitar lógica duplicada.

No caminho integrado da missão 0105:

- Capability Resolver deve ser obrigatório quando a Task declarar `required_capabilities`;
- ausência de Capability Resolver nesse caminho deve produzir falha clara antes do Runtime Adapter;
- cada Capability obrigatória deve gerar uma CapabilityRequest;
- todas as Capabilities obrigatórias devem ser resolvidas antes da execução do runtime;
- falha em uma Capability obrigatória deve impedir a chamada ao Runtime Adapter;
- resolução parcial não deve ser tratada como sucesso;
- ordem de resolução deve ser determinística;
- uma mesma Capability não deve ser resolvida duas vezes na mesma Assignment sem motivo registrado.

O comportamento legado do Agent Orchestrator sem essa integração deve permanecer compatível para testes e consumidores já existentes.

O novo caminho integrado deve configurar explicitamente a resolução de Capabilities.

## 4. Capability Request

Cada CapabilityRequest deve preservar no mínimo:

- capability;
- mission_id;
- workflow_id;
- task_id;
- agent_assignment_id;
- inputs;
- context_refs;
- granted_permissions;
- risk_level;
- limits;
- guardian_decision_refs;
- metadata rastreável.

O `agent_assignment_id` usado nas Capability Requests deve ser o mesmo usado no AgentExecutionRequest e no AgentExecutionResult.

As permissões devem vir de metadados explícitos da Task ou de política normalizada.

Não inventar permissões amplas como fallback.

Ausência de permissão obrigatória deve bloquear a resolução.

Os inputs por Capability podem vir de estrutura explícita semelhante a:

- `task.metadata["capability_inputs"]`;
- chave por nome de Capability.

Quando não houver input específico, usar somente estrutura mínima segura e documentada.

Não usar o conteúdo integral da Task como input implícito de todas as Capabilities.

## 5. Resultado Da Resolução

Para cada Capability, registrar evidência declarativa suficiente:

- capability_id;
- nome;
- versão;
- skill_id selecionada;
- versão da Skill, quando disponível;
- fallback aplicado;
- origem do fallback;
- Guardian Decision, quando existir;
- razões da resolução;
- request_id.

Essas informações devem ser preservadas no Agent Execution Request, Agent Execution Result, metadata ou estrutura equivalente.

Não registrar conteúdo sensível integral.

Não apresentar Skill selecionada como Skill executada.

Não apresentar Tool declarada como Tool disponível.

Não apresentar Provider como chamado.

## 6. Skills E Tools Nesta Missão

O Capability Resolver existente devolve um Skill Profile.

Nesta missão, o Skill Profile deve ser usado somente como:

- resultado declarativo da resolução;
- evidência de compatibilidade;
- referência rastreável para a futura missão 0106.

É proibido nesta missão:

- chamar SkillExecutor;
- executar Skill;
- chamar ToolExecutor;
- executar Tool;
- exigir Tool Registry no fluxo mínimo;
- chamar Provider Gateway;
- chamar Provider Adapter;
- chamar MCP;
- chamar API externa;
- executar subprocesso real.

Nos testes integrados, usar Skills declarativas sem efeito concreto.

Preferir Skills com `required_tools` vazio para não sugerir prontidão de Tool.

## 7. Agent Profile E Capabilities

A seleção do Agent Profile deve continuar verificando:

- role;
- domínio;
- tags;
- task_type;
- complexidade;
- risco;
- supported_capabilities.

Um Agent Profile incompatível com qualquer Capability obrigatória deve ser rejeitado antes do Runtime Adapter.

A compatibilidade declarada pelo Agent Profile não substitui a resolução pelo Capability Resolver.

São verificações complementares:

1. Agent Profile declara que suporta a Capability;
2. Capability Resolver confirma que a Capability existe, está ativa, é permitida e possui Skill declarativa compatível.

## 8. Resultado Para Task Scheduler

Criar mapeamento explícito entre AgentExecutionResult e TaskExecutionOutcome.

Quando AgentExecutionResult indicar sucesso:

- TaskExecutionOutcome deve ser `done`;
- artifact_refs devem ser preservadas;
- evidências e referências relevantes devem ser preservadas na Task, Attempt ou metadata apropriada;
- `agent_assignment_ref` deve ser preservado.

Quando AgentExecutionResult indicar falha:

- TaskExecutionOutcome deve ser `failed`, salvo estado conservador mais apropriado já suportado;
- errors devem ser preservados;
- warnings relevantes devem permanecer auditáveis;
- retry não deve ser decidido pelo Agent Orchestrator;
- retry deve continuar pertencendo à Task Queue e ao Task Scheduler.

A ponte pode informar se a falha é retryable somente por política explícita da Task.

Não considerar toda falha de agente como retryable por padrão.

## 9. Rastreabilidade Operacional

O fluxo integrado deve permitir reconstruir:

Mission
-> Workflow
-> Task
-> TaskAttempt
-> AgentAssignment
-> CapabilityRequest
-> CapabilityResolution
-> AgentExecutionRequest
-> RuntimeExecutionResult
-> AgentExecutionResult
-> TaskExecutionOutcome

Preservar no mínimo:

- mission_id;
- workflow_id;
- task_id;
- attempt_id;
- agent_assignment_id;
- agent_profile_id;
- capability request IDs;
- capability IDs;
- Skill IDs selecionadas;
- Guardian decision references;
- runtime result reference;
- audit log reference;
- artifacts;
- errors.

Se os contratos atuais não tiverem campo suficiente, ampliar somente de forma aditiva e compatível.

Não criar persistência externa.

## 10. Compatibilidade

Preservar:

- TaskScheduler com qualquer executor compatível;
- Task Queue sem conhecimento de agentes;
- AgentOrchestrator atual quando Capability Resolver não estiver configurado no caminho legado;
- testes existentes;
- Runtime Adapter injetável;
- caminho integrado da missão 0104;
- execução sequencial;
- retries finitos pertencentes à Task Queue.

O fluxo canônico novo deve configurar explicitamente:

- AgentRegistry;
- AgentOrchestrator;
- CapabilityRegistry;
- SkillRegistry declarativo;
- CapabilityResolver;
- ponte Task Executor;
- Runtime Adapter fake ou in-memory nos testes.

# Entregáveis

## Código

Criar ou atualizar módulos pequenos para:

- ponte Task Scheduler -> Agent Orchestrator;
- integração Agent Orchestrator -> Capability Resolver;
- construção determinística de Capability Requests;
- preservação de resultados de Capability;
- mapeamento AgentExecutionResult -> TaskExecutionOutcome;
- rastreabilidade de Agent Assignment na Task e Attempt;
- compatibilidade legada.

Evitar concentrar toda a implementação em:

- tasks/scheduler.py;
- agents/orchestrator.py.

Não criar dependência de `tasks` para `agents`.

## Testes

Criar:

- tests/test_task_agent_capability_integration.py

Atualizar testes existentes somente quando necessário.

## Documentação

Criar:

- docs/architecture/task-agent-capability-integration.md

Criar exemplo mínimo:

- docs/examples/minimal-task-agent-capability-flow.md

Atualizar quando necessário:

- README.md;
- CHANGELOG.md;
- docs/task-queue.md;
- docs/agent-orchestrator.md;
- docs/capabilities-skills-tools.md;
- docs/alignment/architecture-map.md;
- docs/alignment/current-state.md;
- docs/alignment/implementation-status.md;
- docs/alignment/roadmap.md;
- docs/alignment/open-questions.md;
- docs/architecture/module-index.md;
- docs/roadmap/mission-backlog.md;
- READMEs internos dos módulos alterados.

Não reescrever Specs nesta missão.

Registrar divergências para revisão na missão 0108.

# Testes Obrigatórios

## 1. Fluxo Bem-Sucedido

Testar pelo menos uma Task com:

- TaskAttempt real da Task Queue;
- uma Capability obrigatória;
- Agent Profile compatível;
- Capability Profile ativa;
- Skill Profile declarativa compatível;
- Runtime Adapter fake;
- resultado bem-sucedido.

Confirmar:

- Task Scheduler inicia tentativa;
- ponte recebe Task e TaskAttempt;
- Agent Orchestrator seleciona Agent Profile;
- Agent Assignment é criado;
- Capability Request usa o mesmo agent_assignment_id;
- Capability é resolvida antes do runtime;
- Skill Profile é selecionada apenas declarativamente;
- Runtime Adapter é chamado uma única vez;
- AgentExecutionResult retorna sucesso;
- TaskExecutionOutcome retorna done;
- Task Queue termina a Task como done;
- IDs e referências são preservados.

## 2. Fluxo Integrado Completo Incremental

Estender ou criar teste que demonstre:

Mission Runner
-> Workflow Engine
-> Task Queue
-> Task Scheduler
-> Agent Orchestrator
-> Capability Resolver
-> Runtime Adapter fake
-> resultado da Task
-> resultado do Workflow
-> resultado da Mission

O teste deve ser local e determinístico.

Não é necessário integrar SkillExecutor, ToolExecutor ou Provider Gateway.

## 3. Capability Inexistente

Confirmar:

- Capability obrigatória não existe;
- resolução falha;
- Runtime Adapter não é chamado;
- Agent Assignment retorna falha normalizada;
- Task Queue registra falha;
- erro é visível;
- retry segue política da Task Queue.

## 4. Permissão Ausente

Confirmar:

- Capability exige permissão;
- Task não concede essa permissão;
- resolução falha antes do runtime;
- nenhuma Skill é executada;
- nenhuma Tool é chamada;
- nenhum Provider é chamado.

## 5. Agent Incompatível

Confirmar:

- nenhum Agent Profile suporta todas as Capabilities;
- seleção falha;
- Capability Resolver ou runtime não são usados indevidamente;
- erro é normalizado para a Task Queue.

## 6. Retry

Confirmar:

- primeira Agent Assignment falha;
- Task Queue decide retry conforme max_attempts;
- nova tentativa possui novo attempt_id;
- nova Agent Assignment possui novo agent_assignment_id;
- a Task não é executada além do limite;
- Agent Orchestrator não controla o retry.

## 7. Fronteiras

Confirmar por teste ou inspeção estática:

- tasks não importa agents;
- tasks não importa capabilities;
- Task Queue não seleciona Agent;
- Task Scheduler não seleciona Agent;
- Agent Orchestrator não chama SkillExecutor;
- Agent Orchestrator não chama ToolExecutor;
- Agent Orchestrator não chama Provider Gateway;
- Capability Resolver não executa Skill;
- Capability Resolver não executa Tool;
- runtime continua injetado;
- nenhuma dependência externa foi adicionada.

## 8. Regressão

Executar:

- pytest;
- python3 -m compileall src;
- validação de links da documentação disponível.

# Restrições Específicas

- Não implementar SkillExecutor.
- Não executar Skills.
- Não integrar ToolExecutor.
- Não executar Tools.
- Não integrar Provider Gateway ao fluxo.
- Não chamar Provider.
- Não chamar MCP.
- Não chamar API externa.
- Não acessar rede.
- Não acessar banco.
- Não usar subprocesso real nos testes.
- Não implementar subagents.
- Não implementar delegação.
- Não implementar paralelismo.
- Não implementar persistência externa.
- Não implementar PostgreSQL.
- Não implementar pgvector.
- Não implementar RAG.
- Não implementar internacionalização.
- Não alterar scripts shell.
- Não alterar workflows de CI.
- Não alterar compositor de missões.
- Não alterar contrato base de execução.
- Não criar agentes operacionais.
- Não adicionar dependências.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não fazer push.
- Não reescrever Specs.
- Não antecipar a missão 0106.
- Não declarar Capability -> Skill -> Tool -> Provider como integrado.
- Não tratar Skill selecionada como Skill executada.
- Não tratar Tool declarada como Tool disponível.
- Não tratar Runtime Adapter como Provider Gateway.

# Critérios Específicos De Aceite

- Existe ponte explícita Task Scheduler -> Agent Orchestrator.
- Task Queue permanece sem dependência de agents.
- Task Scheduler permanece baseado em executor injetado.
- Agent Orchestrator recebe Task e TaskAttempt.
- Agent Profile é selecionado deterministicamente.
- Agent Assignment é rastreável.
- Capability Resolver é consultado no caminho integrado.
- Todas as Capabilities obrigatórias são resolvidas antes do runtime.
- Capability Request preserva IDs e permissões.
- Falha de Capability bloqueia o runtime.
- Falta de permissão bloqueia o runtime.
- Agent incompatível bloqueia a execução.
- Skill Profile é apenas evidência declarativa.
- Nenhuma Skill é executada.
- Nenhuma Tool é executada.
- Nenhum Provider é chamado.
- AgentExecutionResult é convertido explicitamente em TaskExecutionOutcome.
- Task Queue continua responsável por tentativas e retries.
- Retry cria novo Attempt e nova Agent Assignment.
- Resultado retorna ao Workflow Engine e ao Mission Runner no teste incremental.
- Fluxo local completo até Capability Resolver é validado.
- Compatibilidade legada é preservada.
- Documentação distingue resolução declarativa de execução concreta.
- implementation-status registra somente o fluxo efetivamente validado.
- backlog marca 0105 concluída sem antecipar 0106.
- Specs não são reescritas.
- pytest passa.
- python3 -m compileall src passa.
- links da documentação passam.
- commit automático usa mensagem em português do Brasil.

# Referência Operacional

O contrato base de execução está em `missions/base/EXECUTION_CONTRACT.md` e é composto obrigatoriamente pelo runner. Não copie o contrato para dentro da missão.

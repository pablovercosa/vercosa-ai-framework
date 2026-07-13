---
id: "0107"
title: "Integrar Policy Guardian Context Token Model e Audit ao fluxo mínimo"
base_contract: "v1"
roles:
  - integration-architect
  - policy-governance-engineer
  - context-engineer
  - model-selection-engineer
  - audit-engineer
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

Integrar ao fluxo mínimo validado nas missões 0104, 0105 e 0106:

- Policy Engine;
- Guardian Engine;
- Context Router;
- Token Budget Manager;
- Model Selection Engine;
- Audit/Event Log.

O fluxo deve permanecer local, determinístico, injetável, testável e sem
providers reais, rede, banco, MCP, API externa ou subprocessos.

O caminho mínimo esperado deve demonstrar:

Mission Runner
-> Workflow Engine
-> Task Queue
-> Agent Orchestrator
-> resolução de políticas
-> montagem governada de contexto
-> aplicação do orçamento de tokens
-> avaliação Guardian
-> seleção de modelo
-> Capability Resolver
-> Capability Executor
-> Skill Executor
-> Tool Executor
-> Provider Gateway em dry-run
-> Runtime Adapter fake ou injetado
-> validação Guardian
-> Audit/Event Log
-> AgentExecutionResult
-> TaskExecutionOutcome
-> WorkflowResult
-> MissionResult

# Estado De Partida

O projeto já possui:

- DeterministicPolicyEngine;
- PolicySet, PolicyRule, PolicyEvaluationContext e ResolvedPolicySet;
- GuardianEngine e GuardianEvaluationContext;
- DeterministicContextRouter;
- SimpleTokenBudgetManager;
- ContextRequest e ContextPackage;
- ModelSelector;
- ModelSelectionPolicy e SelectionDecision;
- EventLog em memória;
- JsonlAuditEventLog opt-in;
- helpers de auditoria para Policy, Guardian e Context;
- AgentOrchestrator com Guardian e Model Selection opcionais;
- CapabilityResolver;
- ResolvedCapabilityExecutor;
- SkillExecutor;
- ToolExecutor;
- ProviderGateway em dry-run;
- AgentTaskExecutor;
- WorkflowEngine.execute_with_queue();
- MissionRunner com integração opcional de Workflow e Task.

Esses componentes não devem ser reimplementados.

# Problema A Resolver

As integrações atuais são parciais e dependem de chamadas explícitas isoladas.

O fluxo mínimo completo ainda não comprova, em uma única execução:

1. resolução declarativa de políticas;
2. propagação do ResolvedPolicySet;
3. construção de ContextPackage;
4. aplicação real do Token Budget Manager;
5. avaliação Guardian do planejamento e do contexto;
6. Model Selection usando políticas e requisitos de contexto;
7. propagação dessas decisões até o runtime;
8. registro auditável e ordenado das decisões;
9. bloqueio antes do runtime quando governança reprovar;
10. compatibilidade com a cadeia Capability -> Skill -> Tool -> Provider
    Gateway em dry-run.

# Arquitetura Obrigatória

## 1. Coordenador De Governança Da Execução

Criar ou consolidar uma fronteira pequena, explícita e injetável responsável
pela preparação governada de uma execução de Agent Assignment.

Nomes aceitáveis, caso uma nova abstração seja necessária:

- AgentExecutionGovernance;
- ExecutionGovernancePipeline;
- AgentExecutionPreparation;
- GovernedExecutionPlanner;
- ExecutionPreparationPipeline.

A solução não deve transformar o AgentOrchestrator em uma god function.

O coordenador deve produzir um resultado estruturado equivalente a:

- PolicyResolutionResult;
- ResolvedPolicySet;
- ContextPackage;
- GuardianDecision do contexto;
- SelectionDecision;
- referências de eventos de auditoria;
- warnings;
- erros;
- requisitos de aprovação;
- referências rastreáveis.

Evitar novo componente quando composição clara dos contratos existentes for
suficiente.

## 2. Ordem Do Fluxo De Preparação

A preparação governada deve seguir ordem determinística:

1. receber Task, TaskAttempt e AgentProfile selecionado;
2. resolver PolicySets explícitos;
3. construir ContextRequest com candidatos explícitos;
4. aplicar Context Router e Token Budget Manager;
5. avaliar ContextPackage pelo Guardian;
6. selecionar modelo usando:
   - ModelSelectionPolicy;
   - ResolvedPolicySet;
   - requisitos de orçamento derivados do ContextPackage;
7. registrar eventos estruturados;
8. devolver resultado imutável e rastreável ao AgentOrchestrator.

A ordem não deve depender de sets, hashes não ordenados ou descoberta externa.

## 3. Policy Engine

O caminho integrado deve aceitar PolicySets por dependência explícita,
provider injetável ou metadados normalizados da Task.

Não buscar políticas em rede, banco ou filesystem arbitrário.

O PolicyEvaluationContext deve preservar quando disponíveis:

- mission_id;
- workflow_id;
- task_id;
- agent_id ou agent_profile_id;
- scopes solicitados;
- referências da execução;
- metadados seguros.

O resultado deve ser um único ResolvedPolicySet efetivo por preparação.

O ResolvedPolicySet deve ser propagado para:

- GuardianEvaluationContext;
- ContextRequest;
- ModelSelector;
- CapabilityRequest quando aplicável;
- Tool/Provider por metadados ou referências normalizadas quando aplicável;
- Audit/Event Log.

Não aplicar efeitos de política diretamente dentro do Policy Engine.

Policy Engine resolve declarações.

Guardian e fronteiras concretas fazem enforcement.

## 4. Guardian Engine

O fluxo deve usar Guardian nos pontos mínimos:

- planejamento do Agent Assignment;
- ContextPackage antes de sua entrega ao runtime;
- ações de Capability, Tool e Provider nos pontos já existentes;
- validação posterior ao Runtime Adapter.

As decisões BLOCK e REQUIRE_APPROVAL devem impedir avanço automático quando
não houver aprovação explícita representada no contrato.

WARN pode permitir avanço, preservando warnings e referências.

O Guardian deve receber o ResolvedPolicySet quando o contrato existente
permitir.

Não duplicar regras do Guardian no coordenador.

Não interpretar strings manualmente fora das APIs existentes quando houver
contrato estruturado.

## 5. Context Router

O contexto deve ser construído apenas com candidatos explícitos.

Fontes aceitáveis nesta missão:

- ContextItems fornecidos pela Task;
- ContextItems fornecidos por dependency/provider injetável local;
- referências já existentes na Task;
- candidatos fake em testes.

Não implementar:

- RAG;
- busca vetorial;
- pgvector;
- PostgreSQL;
- crawling;
- acesso a arquivos arbitrários;
- internet;
- provider externo;
- memória global.

O ContextRequest deve preservar:

- request_goal;
- scope;
- candidatos;
- fontes;
- token budget;
- citation_required;
- policy_refs;
- ResolvedPolicySet;
- guardian_decision_refs;
- mission_id, workflow_id, task_id e agent_assignment_id em metadados seguros.

O ContextPackage deve ser preservado por referência no pedido enviado ao
runtime.

Não copiar conteúdo completo para logs ou metadados auditáveis.

## 6. Token Budget Manager

O orçamento de tokens deve ser efetivamente aplicado pelo Context Router.

O orçamento deve ser derivado de configuração explícita, por exemplo:

- Task.metadata["token_budget"];
- AgentProfile.default_execution_limits;
- políticas resolvidas;
- defaults conservadores documentados.

Não inventar orçamento ilimitado.

Preservar no mínimo:

- max_input_tokens;
- reserved_output_tokens;
- available_context_tokens;
- estimated_context_tokens;
- itens omitidos;
- motivos de omissão;
- minimum_context_window requerido.

Itens que excedem orçamento devem ser omitidos de forma determinística e
auditável.

O ContextPackage.model_requirements deve alimentar o Model Selection Engine.

## 7. Model Selection

O ModelSelector deve receber:

- ModelSelectionPolicy normalizada;
- catálogo em memória injetado;
- ResolvedPolicySet;
- requisitos de orçamento derivados do ContextPackage.

Não descobrir modelos por rede ou provider.

A seleção deve preservar:

- selected_model;
- small_model quando existente;
- fallback_chain;
- reason;
- estimated_cost;
- policy_sources;
- token_budget_requirements;
- token_budget_compatibility;
- warnings;
- requires_review;
- requires_user_approval.

Quando a decisão exigir aprovação humana, a execução automática deve ser
bloqueada antes do Runtime Adapter.

Quando não houver modelo compatível, retornar falha estruturada sem chamar
Capability Executor ou Runtime Adapter.

O modelo selecionado deve chegar ao RuntimeExecutionRequest somente por
referência/contrato normalizado.

## 8. Audit/Event Log

O caminho integrado deve aceitar EventLog injetável.

Usar InMemoryEventLog ou equivalente nos testes.

JsonlAuditEventLog deve permanecer opt-in e não deve ser ativado globalmente.

Registrar em ordem determinística, quando os resultados existirem:

1. resolução de políticas;
2. montagem do ContextPackage;
3. decisão Guardian sobre contexto;
4. decisão de Model Selection;
5. início da execução governada;
6. falha ou bloqueio de preparação, quando ocorrer;
7. resultado do runtime;
8. decisão Guardian de validação;
9. resultado final do Agent Assignment.

Reutilizar helpers existentes de auditoria.

Adicionar helper para Model Selection ou execução de Agent somente quando
necessário para manter contratos claros.

Eventos não devem conter:

- prompts completos;
- conteúdo integral do contexto;
- secrets;
- tokens de autenticação;
- comandos sensíveis completos;
- credenciais;
- respostas brutas de providers.

Eventos devem preservar apenas IDs, contagens, estados, referências,
classificações, warnings e metadados seguros.

## 9. Resultado Estruturado

O AgentExecutionRequest e o AgentExecutionResult devem preservar por referência,
sem duplicar conteúdo sensível:

- policy_resolution_id;
- matched_policy_refs;
- context_package_id;
- context_request_id;
- estimated_context_tokens;
- reserved_output_tokens;
- model_selection_decision_ref;
- selected_model_id;
- guardian_decision_refs;
- capability resolution refs;
- capability execution refs;
- audit event refs;
- warnings;
- approval requirements;
- runtime_result_ref.

O TaskExecutionOutcome deve continuar preservando as referências principais.

Não alterar a responsabilidade da Task Queue.

## 10. Compatibilidade

O comportamento legado deve permanecer disponível:

- AgentOrchestrator sem pipeline completo deve continuar funcionando;
- Capability Resolver opcional continua compatível;
- Capability Executor opcional continua compatível;
- ModelSelector opcional continua compatível;
- EventLog ausente não deve quebrar consumidores legados;
- Context Router ausente não deve ser exigido fora do novo caminho integrado.

O novo caminho deve ser ativado explicitamente por configuração ou dependência.

Adicionar configuração equivalente a:

- execution_governance opcional;
- require_execution_governance desativado por padrão.

Quando require_execution_governance estiver ativo:

- ausência da dependência deve falhar antes do runtime;
- ausência de PolicySets pode usar conjunto vazio explícito;
- ausência de candidatos de contexto pode produzir ContextPackage vazio válido,
  desde que o contrato permita;
- ausência de catálogo de modelos deve falhar claramente quando Model Selection
  for obrigatório;
- falhas não devem cair silenciosamente para comportamento legado.

# Fronteiras Obrigatórias

## Task Queue

tasks/ não deve importar:

- policy;
- guardian;
- context;
- model_selection;
- audit;
- capabilities;
- skills;
- tools;
- providers;
- agents.

Task Queue controla apenas:

- estado;
- dependências;
- elegibilidade;
- tentativas;
- retries;
- resultado normalizado.

## Agent Orchestrator

AgentOrchestrator pode depender de contratos de alto nível, mas não deve:

- resolver PolicySets por lógica duplicada;
- montar ContextPackage manualmente;
- estimar tokens manualmente;
- escrever JSONL diretamente;
- conhecer adapters concretos;
- chamar rede;
- chamar banco;
- chamar MCP;
- chamar provider real;
- executar subprocesso;
- acessar OpenCode diretamente.

## Policy Engine

Não deve executar ações concretas.

## Context Router

Não deve escolher modelo ou executar runtime.

## Model Selection

Não deve chamar provider ou runtime.

## Audit/Event Log

Não deve alterar decisões nem controlar fluxo.

# Escopo Permitido

- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/policy/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/audit/
- src/vercosa_ai_framework/capabilities/
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/tasks/ somente para referências normalizadas,
  sem dependências novas para camadas inferiores
- src/vercosa_ai_framework/workflows/ apenas quando necessário para propagação
  de referências e composição
- src/vercosa_ai_framework/missions/ apenas quando necessário para o teste
  ponta a ponta do fluxo já existente
- tests/
- docs/
- README.md
- CHANGELOG.md

# Escopo Proibido

- provider real;
- rede;
- API externa;
- MCP real;
- OpenCode real;
- banco;
- PostgreSQL;
- pgvector;
- RAG;
- busca vetorial;
- crawling;
- subprocesso;
- nova persistência externa;
- ativação global de JSONL;
- internacionalização;
- tag;
- release;
- publicação de pacote;
- push automático;
- alteração destrutiva;
- implementação da missão 0108;
- reescrita ampla de Specs;
- mudanças não relacionadas.

# Testes Obrigatórios

Criar testes unitários e de integração que demonstrem:

1. PolicySets explícitos geram ResolvedPolicySet determinístico.
2. PolicyEvaluationContext preserva IDs do fluxo.
3. ResolvedPolicySet chega ao Context Router.
4. ResolvedPolicySet chega ao ModelSelector.
5. Context Router recebe candidatos explícitos.
6. Token Budget Manager omite item acima do orçamento.
7. ContextPackage preserva referências, orçamento e requisitos de modelo.
8. Guardian avalia ContextPackage antes do Model Selection ou runtime conforme
   a sequência arquitetural adotada e documentada.
9. Guardian BLOCK impede Capability Executor e Runtime Adapter.
10. Guardian REQUIRE_APPROVAL impede execução sem aprovação explícita.
11. Guardian WARN permite execução e preserva warning.
12. ModelSelector usa minimum_context_window do ContextPackage.
13. modelo incompatível com orçamento falha antes do runtime.
14. política DENY exclui modelo incompatível.
15. decisão que exige aprovação impede runtime.
16. Capability/Skill/Tool/Provider Gateway em dry-run continua funcionando.
17. Provider Gateway não chama adapter concreto em dry-run.
18. eventos de auditoria são registrados em ordem determinística.
19. eventos não contêm conteúdo integral do contexto nem campos sensíveis.
20. policy_resolution_id, context_package_id, selected_model_id e
    guardian_decision_refs chegam ao AgentExecutionResult.
21. TaskExecutionOutcome preserva referências principais.
22. runtime é chamado exatamente uma vez no fluxo de sucesso.
23. runtime não é chamado em falha de Policy, Context, Guardian ou Model.
24. comportamento legado sem pipeline completo permanece compatível.
25. tasks/ não importa módulos proibidos.
26. nenhum teste usa rede, banco, subprocesso ou provider externo.
27. fluxo completo Mission/Workflow/Task/Agent/Governance/Capability/
    Skill/Tool/Provider dry-run funciona com fakes locais.
28. suíte de regressão permanece verde.

# Documentação Obrigatória

Criar documentação arquitetural da integração 0107.

Criar exemplo mínimo mostrando:

Task
-> Policy
-> Context
-> Token Budget
-> Guardian
-> Model Selection
-> Capability
-> Skill
-> Tool
-> Provider Gateway dry-run
-> Runtime fake
-> Audit/Event Log

Atualizar somente documentos afetados, incluindo quando aplicável:

- README.md;
- CHANGELOG.md;
- docs/alignment/architecture-map.md;
- docs/alignment/current-state.md;
- docs/alignment/implementation-status.md;
- docs/alignment/roadmap.md;
- docs/alignment/open-questions.md;
- docs/architecture/module-index.md;
- docs/architecture/post-integration-architecture-review.md;
- docs/architecture/audit-event-architecture.md;
- docs/agent-orchestrator.md;
- docs/context-router-token-budget.md;
- docs/model-selection-engine.md;
- docs/policy-engine.md;
- docs/guardian-engine.md;
- docs/roadmap/mission-backlog.md.

Não declarar:

- provider real;
- rede;
- banco;
- RAG;
- MCP;
- API externa;
- produção;
- release alfa pronta.

Registrar divergências entre Specs e implementação para revisão na missão 0108.

Não reescrever Specs nesta missão.

Não criar links Markdown para logs locais ou arquivos ignorados pelo Git.

# Critérios De Aceite

A missão será aceita somente se:

- Policy, Guardian, Context Router, Token Budget, Model Selection e Audit
  participarem do mesmo fluxo mínimo;
- a integração for explícita e injetável;
- ResolvedPolicySet for propagado;
- ContextPackage for realmente construído;
- orçamento de tokens for realmente aplicado;
- requisitos de contexto influenciarem Model Selection;
- bloqueios ocorrerem antes do runtime;
- eventos auditáveis forem registrados;
- o fluxo 0106 continuar operando em dry-run;
- nenhum provider real ou adapter concreto for chamado;
- nenhuma rede, banco, MCP ou subprocesso for usado;
- compatibilidade legada for preservada;
- testes novos e regressões passarem;
- documentação refletir o estado real;
- Specs não forem reescritas;
- Git permanecer sem mudanças não relacionadas;
- a missão gerar um único commit próprio.

# Validações Obrigatórias

Executar:

- pytest;
- python3 -m compileall src;
- python3 -m vercosa_ai_framework.cli.main docs-links;
- python3 -m vercosa_ai_framework.cli.main doctor;
- git status --short;
- git diff --stat;
- revisão do diff completo;
- verificação estática de imports proibidos em tasks/;
- verificação de ausência de rede e subprocesso nos testes novos;
- verificação de ausência de conteúdo sensível nos eventos;
- verificação da ordem determinística dos eventos.

# Entrega Esperada

Entregar:

- integração transversal explícita e injetável;
- resultado estruturado de preparação governada;
- PolicyResolutionResult e ResolvedPolicySet propagados;
- ContextPackage governado por Token Budget;
- Guardian aplicado ao contexto e execução;
- Model Selection alimentado por políticas e orçamento;
- Audit/Event Log integrado;
- testes unitários, de integração e ponta a ponta;
- exemplo mínimo;
- documentação atualizada;
- commit exclusivo da missão 0107.

Ao concluir, mover este arquivo para missions/done conforme o runner seguro.

Não executar push.
Não criar missão 0108.
Não criar missão 0109.

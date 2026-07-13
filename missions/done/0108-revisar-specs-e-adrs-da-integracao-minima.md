---
id: "0108"
title: "Revisar Specs e ADRs da integração mínima"
base_contract: "v1"
roles:
  - specification-architect
  - architecture-reviewer
  - documentation-engineer
  - governance-reviewer
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

Revisar e alinhar as Specs e decisões arquiteturais afetadas pelas integrações
mínimas concluídas nas missões 0104, 0105, 0106 e 0107.

A missão deve reconciliar documentação normativa, arquitetura implementada,
testes e estado declarado do projeto.

A missão é documental e arquitetural.

Ela não deve criar novo comportamento de runtime.

# Estado De Partida

As missões anteriores validaram os seguintes caminhos:

## Missão 0104

Mission Runner
-> Workflow Engine
-> Task Queue
-> Task Scheduler
-> executor injetado
-> WorkflowResult
-> MissionResult

## Missão 0105

Task Scheduler
-> AgentTaskExecutor
-> AgentOrchestrator
-> CapabilityResolver
-> RuntimeAdapter
-> TaskExecutionOutcome

## Missão 0106

CapabilityResolutionResult
-> ResolvedCapabilityExecutor
-> SkillExecutor
-> ToolExecutor
-> ProviderGateway em dry-run
-> RuntimeAdapter fake ou injetado

## Missão 0107

Policy Engine
-> Context Router
-> Token Budget Manager
-> Guardian Engine
-> Model Selection
-> Capability Resolver
-> Capability Executor
-> Skill
-> Tool
-> Provider Gateway em dry-run
-> Runtime Adapter
-> Audit/Event Log
-> Task/Workflow/Mission results

O fluxo integrado continua:

- local;
- determinístico;
- injetável;
- sem provider real;
- sem rede;
- sem banco;
- sem MCP;
- sem API externa;
- sem RAG;
- sem PostgreSQL;
- sem pgvector.

# Problema A Resolver

As Specs existentes foram escritas antes de parte das integrações 0104-0107.

Algumas descrevem arquitetura futura mais ampla do que o código atual.

Outras podem não registrar decisões já comprovadas pela implementação e pelos
testes.

A missão deve distinguir claramente:

- arquitetura pretendida;
- comportamento implementado;
- fluxo integrado validado;
- compatibilidade legada;
- limitações atuais;
- decisões arquiteturais aceitas;
- decisões provisórias;
- perguntas ainda abertas.

# Fontes Obrigatórias

Revisar, no mínimo:

## Specs

- specs/framework/0001-framework-foundation.md
- specs/framework/0002-model-selection-engine.md
- specs/framework/0004-mission-runner.md
- specs/framework/0005-guardian-engine.md
- specs/framework/0006-workflow-engine.md
- specs/framework/0007-task-queue.md
- specs/framework/0008-agent-orchestrator.md
- specs/framework/0009-capabilities-skills-tools.md
- specs/framework/0010-provider-gateway.md
- specs/framework/0014-context-router-token-budget-memory.md

## Implementação

- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/workflows/
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/policy/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/capabilities/
- src/vercosa_ai_framework/skills/
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/audit/

## Testes

- tests/test_mission_workflow_task_integration.py
- tests/test_task_agent_capability_integration.py
- tests/test_capability_skill_tool_provider_dry_run.py
- tests/test_agent_execution_governance_0107.py
- demais testes diretamente relacionados aos módulos revisados

## Documentação

- docs/alignment/implementation-status.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/architecture/post-integration-architecture-review.md
- docs/architecture/execution-governance-0107.md
- docs/architecture/audit-event-architecture.md
- docs/architecture/module-index.md
- docs/agent-orchestrator.md
- docs/capabilities-skills-tools.md
- docs/context-router-token-budget.md
- docs/model-selection-engine.md
- docs/policy-engine.md
- docs/guardian-engine.md
- docs/roadmap/mission-backlog.md
- README.md
- CHANGELOG.md

# Auditoria Obrigatória

Criar:

- docs/audits/spec-adr-integration-review-0108.md

O relatório deve conter uma matriz com:

- documento normativo;
- responsabilidade declarada;
- implementação correspondente;
- evidência por teste;
- estado: planejado, implementado, integrado ou validado;
- divergência encontrada;
- ação adotada;
- decisão ainda pendente.

Não usar existência de documentação como prova de implementação.

Não usar teste unitário isolado como prova de integração completa.

# Specs Afetadas

Atualizar Specs somente quando a implementação e os testes fornecerem evidência.

Não alterar objetivos fundamentais do framework sem justificativa explícita.

## Mission Runner

Registrar claramente:

- Mission Runner controla ciclo da Mission;
- integração com Workflow é explícita e injetável;
- Mission Runner não deve absorver permanentemente Workflow Engine;
- existência de Mission Orchestrator separado continua decisão pendente quando
  ainda não comprovada.

## Workflow Engine

Registrar:

- execute_with_queue como caminho integrado mínimo;
- Workflow Engine constrói e acompanha Workflow;
- Task Queue controla execução operacional das Tasks;
- caminho legado execute pode permanecer por compatibilidade;
- decidir documentalmente se o caminho legado é suportado, transitório ou
  candidato a depreciação futura;
- não removê-lo nesta missão.

## Task Queue

Registrar:

- TaskScheduler é o loop operacional de Tasks no caminho integrado;
- Task Queue controla estado, dependências, tentativas e retries;
- Task Queue recebe executor injetado;
- Task Queue não conhece Agent, Capability, Skill, Tool ou Provider;
- retries permanecem responsabilidade da Task Queue.

## Agent Orchestrator

Registrar:

- AgentTaskExecutor é a ponte entre Task Scheduler e Agent Orchestrator;
- Agent Orchestrator seleciona Agent Profile;
- resolução de Capability ocorre antes do runtime quando configurada;
- execução de Capability ocorre antes do runtime quando configurada;
- Execution Governance é dependência explícita e opcional;
- comportamento legado permanece compatível;
- Agent Orchestrator não acessa provider, MCP, API, banco ou OpenCode
  diretamente.

## Capabilities, Skills E Tools

Registrar separação entre:

- CapabilityResolutionResult;
- resolução declarativa Capability -> Skill;
- execução da Capability resolvida;
- SkillExecutionRequest;
- ToolExecutionRequest;
- ProviderRequest;
- resultados de cada fronteira.

Registrar que:

- Capability Resolver não executa Skill;
- ResolvedCapabilityExecutor faz a ponte para SkillExecutor;
- SkillExecutor seleciona e chama ToolExecutor;
- ToolExecutor é a fronteira que chama ProviderGateway;
- cada camada preserva IDs e referências.

## Provider Gateway

Registrar:

- dry-run usa ProviderGateway real;
- dry-run não chama adapter concreto;
- Provider Gateway seleciona e valida ProviderProfile;
- Provider Gateway não é Model Selector;
- providers reais continuam fora do fluxo validado;
- rede não foi validada;
- fallback real externo não foi validado.

## Policy Engine E Guardian

Registrar decisão arquitetural:

- Policy Engine resolve políticas declarativas;
- Guardian faz enforcement operacional;
- Policy Engine não executa ações;
- Guardian não substitui resolução declarativa;
- ResolvedPolicySet é propagado aos consumidores;
- BLOCK impede execução;
- REQUIRE_APPROVAL impede execução automática sem aprovação representada;
- WARN preserva referência e permite continuidade quando o contrato permitir.

## Context Router E Token Budget

Registrar:

- candidatos de contexto são explícitos;
- Token Budget Manager é aplicado pelo Context Router;
- itens podem ser omitidos deterministicamente;
- ContextPackage produz requisitos mínimos para Model Selection;
- Context Router não implementa RAG;
- não existe busca vetorial integrada;
- não existe memória global automática.

## Model Selection

Registrar:

- catálogo em memória é injetado;
- seleção usa ModelSelectionPolicy;
- ResolvedPolicySet pode excluir modelos;
- requisitos do ContextPackage influenciam minimum_context_window;
- Model Selection não chama provider nem runtime;
- aprovação exigida bloqueia execução automática.

## Audit/Event Log

Registrar:

- EventLog é injetável;
- InMemoryEventLog é usado em testes;
- JsonlAuditEventLog continua opt-in;
- Audit/Event Log observa e registra;
- Audit/Event Log não decide nem controla fluxo;
- eventos não devem conter conteúdo sensível completo;
- ordem dos eventos é determinística no fluxo 0107.

# ADRs

Localizar primeiro o padrão existente de ADRs do projeto.

Não criar estrutura concorrente se já existir padrão canônico.

Caso não exista diretório canônico, criar:

- docs/architecture/decisions/README.md

E usar nomes claros, estáveis e numerados.

Criar ou atualizar ADRs somente para decisões já adotadas e comprovadas.

Decisões candidatas:

1. separação Mission Runner, Workflow Engine e Task Queue;
2. TaskScheduler como loop operacional de Tasks;
3. AgentTaskExecutor como ponte desacoplada;
4. separação entre resolução e execução de Capability;
5. ToolExecutor como única fronteira da cadeia que chama ProviderGateway;
6. ProviderGateway dry-run sem chamada a adapter;
7. Execution Governance como pipeline injetável;
8. Policy Engine resolve e Guardian aplica enforcement;
9. ContextPackage alimenta Model Selection por requisitos de tokens;
10. Audit/Event Log é observador, opcional e não controlador;
11. compatibilidade legada por configuração explícita.

Não criar ADR como aceita quando a decisão continuar aberta.

Usar estados claros, por exemplo:

- Aceita;
- Provisória;
- Substituída;
- Rejeitada;
- Em avaliação.

# Decisões Que Devem Permanecer Abertas

Não resolver sem evidência:

- criação de Mission Orchestrator como módulo separado;
- remoção do WorkflowEngine.execute legado;
- catálogo real de Agents e Capabilities;
- providers reais;
- múltiplos runtimes reais;
- formato definitivo de aprovação humana;
- persistência externa de auditoria;
- PostgreSQL;
- pgvector;
- RAG;
- modelo definitivo de memória;
- consumidor principal do produto;
- tag ou release alfa.

Registrar essas decisões em docs/alignment/open-questions.md quando necessário.

# Fonte Canônica De Estado

docs/alignment/implementation-status.md deve continuar sendo o checklist
canônico de implementação.

Os demais documentos devem:

- resumir;
- apontar para o checklist;
- evitar duplicação extensa;
- não apresentar estado contraditório.

Não executar ainda a consolidação documental ampla reservada à missão 0109.

# Escopo Permitido

- specs/framework/
- docs/
- README.md
- CHANGELOG.md
- missions/done/0108-... apenas pela movimentação feita pelo runner

# Escopo Proibido

- src/
- tests/
- scripts/
- .github/
- pyproject.toml
- configuração do OpenCode
- alteração de comportamento
- refatoração de código
- novos módulos Python
- novos testes
- provider real
- rede
- banco
- MCP
- API externa
- PostgreSQL
- pgvector
- RAG
- internacionalização
- tag
- release
- publicação de pacote
- push automático
- criação da missão 0109
- criação da missão 0110

# Regras De Precisão

Toda afirmação sobre implementação deve apontar para código ou teste.

Toda afirmação sobre integração deve apontar para teste de integração.

Toda afirmação sobre validação deve apontar para evidência executável.

Não declarar:

- produção pronta;
- release pronta;
- provider real validado;
- rede validada;
- banco integrado;
- RAG implementado;
- memória global implementada;
- sandbox técnico completo;
- segurança absoluta;
- arquitetura final imutável.

Usar linguagem como:

- MVP;
- integração mínima;
- local;
- determinístico;
- injetável;
- opcional;
- dry-run;
- validado por testes;
- ainda não implementado;
- decisão pendente.

# Validações Obrigatórias

Executar:

- pytest;
- python3 -m compileall src;
- python3 -m vercosa_ai_framework.cli.main docs-links;
- python3 -m vercosa_ai_framework.cli.main doctor;
- git diff --check;
- git status --short;
- git diff --stat;
- revisão completa do diff;
- verificação de links para arquivos ignorados;
- verificação de ausência de alterações em src/;
- verificação de ausência de alterações em tests/;
- verificação de ausência de afirmações de release ou provider real;
- verificação de consistência entre Specs e implementation-status.

# Critérios De Aceite

A missão será aceita somente se:

- o relatório de auditoria 0108 existir;
- Specs afetadas refletirem o fluxo realmente implementado;
- ADRs registrarem apenas decisões comprovadas;
- decisões abertas permanecerem abertas;
- implementação-status continuar sendo fonte canônica;
- documentação não prometer funcionalidades inexistentes;
- nenhuma mudança em src/ ocorrer;
- nenhuma mudança em tests/ ocorrer;
- nenhum comportamento de runtime mudar;
- todos os links Markdown forem válidos;
- testes e validações permanecerem verdes;
- a missão gerar um único commit próprio.

# Movimentação Da Missão

O agente não deve mover manualmente este arquivo de missions/running para
missions/done.

A movimentação final é responsabilidade exclusiva do runner seguro.

O agente deve apenas concluir alterações, validar e criar o commit da missão.

# Entrega Esperada

Entregar:

- relatório de auditoria 0108;
- Specs revisadas;
- ADRs criadas ou atualizadas;
- decisões pendentes registradas;
- documentos de alinhamento atualizados somente quando necessário;
- README e CHANGELOG atualizados somente quando necessário;
- nenhuma alteração de código;
- commit exclusivo da missão 0108.

Não executar push.
Não criar missão 0109.
Não criar missão 0110.
Não mover manualmente o arquivo da missão.

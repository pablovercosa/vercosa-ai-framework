---
id: "0106"
title: "Integrar Capability Skill Tool e Provider Gateway em dry-run governado"
base_contract: "v1"
roles:
  - integration-architect
  - capability-governance-engineer
  - skill-tool-engineer
  - provider-gateway-engineer
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

Integrar o caminho mínimo governado:

CapabilityResolutionResult
-> fronteira de execução de Capability
-> SkillExecutionRequest
-> SkillExecutor
-> ToolExecutionRequest
-> ToolExecutor
-> ProviderRequest
-> ProviderGateway
-> ProviderResult em dry-run
-> ToolExecutionResult
-> SkillExecutionResult
-> resultado rastreável da Capability
-> AgentExecutionResult
-> TaskExecutionOutcome

A missão deve comprovar que uma Capability previamente resolvida pode ser
executada por uma Skill compatível, por uma Tool governada e por um Provider
Gateway em dry-run, sem rede e sem chamar adapter concreto.

# Estado De Partida

A missão 0105 concluiu o fluxo:

TaskScheduler
-> AgentTaskExecutor
-> AgentOrchestrator
-> CapabilityResolver
-> RuntimeAdapter
-> TaskExecutionOutcome

O CapabilityResolver atualmente seleciona declarativamente uma SkillProfile,
mas não executa a Skill.

O projeto já possui:

- CapabilityResolutionResult;
- SkillExecutionRequest e SkillExecutionResult;
- SkillExecutor;
- ToolExecutionRequest e ToolExecutionResult;
- ToolExecutor;
- ProviderRequest e ProviderResult;
- ProviderGateway;
- registries de capabilities, skills, tools e providers;
- dry-run no Provider Gateway;
- Guardian opcional nas fronteiras já existentes;
- AgentOrchestrator integrado ao CapabilityResolver;
- AgentTaskExecutor integrado ao TaskScheduler.

A missão não deve reimplementar esses componentes.

# Fluxo Alvo

O caminho validado deve demonstrar:

Task
-> AgentTaskExecutor
-> AgentOrchestrator
-> CapabilityResolver
-> CapabilityResolutionResult
-> executor ou pipeline injetável de Capability
-> SkillExecutor
-> ToolExecutor
-> ProviderGateway
-> ProviderResult com status dry_run
-> resultado normalizado da Capability
-> RuntimeAdapter fake ou injetado
-> AgentExecutionResult
-> TaskExecutionOutcome

A execução de Capability deve ocorrer depois da resolução declarativa e antes
da chamada final ao RuntimeAdapter.

Uma falha na execução de qualquer Capability obrigatória deve impedir a chamada
ao RuntimeAdapter.

# Arquitetura Obrigatória

## 1. Fronteira Capability Para Skill

Criar uma fronteira pequena, explícita e testável que receba um
CapabilityResolutionResult e produza uma execução normalizada da Skill
selecionada.

O nome concreto deve seguir os padrões existentes. Exemplos aceitáveis:

- CapabilityExecutor;
- CapabilityExecutionPipeline;
- ResolvedCapabilityExecutor;
- CapabilitySkillExecutor.

Não criar abstrações duplicadas quando um contrato existente puder ser
estendido de forma compatível.

A fronteira deve:

- receber o CapabilityResolutionResult;
- preservar CapabilityRequest original;
- construir SkillExecutionRequest;
- usar exatamente a SkillProfile selecionada pelo CapabilityResolver;
- não selecionar outra Skill silenciosamente;
- chamar SkillExecutor;
- normalizar sucesso, avisos, erros e referências;
- manter ordem determinística;
- não acessar rede, banco, MCP ou provider concreto.

## 2. Integração Com Agent Orchestrator

O AgentOrchestrator não deve importar ou construir diretamente:

- ToolExecutor;
- ProviderGateway;
- ProviderRegistry;
- ProviderAdapter;
- adapters concretos;
- MCPs;
- APIs;
- clientes de rede.

A integração deve ocorrer por contrato injetável de alto nível.

Adicionar configuração explícita equivalente a:

- capability_executor opcional;
- require_capability_execution desativado por padrão.

O comportamento legado deve permanecer compatível.

Quando a execução de Capability for exigida:

- ausência do executor deve falhar claramente antes do RuntimeAdapter;
- todas as Capabilities obrigatórias devem ser executadas;
- a ordem deve acompanhar task.required_capabilities;
- execução parcial não deve ser tratada como sucesso;
- falha deve impedir o RuntimeAdapter;
- resultados devem ser preservados no AgentExecutionRequest e
  AgentExecutionResult de forma rastreável.

Não fazer a Task Queue conhecer Skill, Tool ou Provider.

## 3. Construção De SkillExecutionRequest

Cada SkillExecutionRequest deve preservar no mínimo:

- mission_id;
- workflow_id;
- task_id;
- agent_assignment_id;
- capability;
- skill;
- inputs;
- context_refs;
- granted_permissions;
- allowed_tools;
- limits;
- guardian_decision_refs;
- request_id;
- metadados de rastreabilidade.

Os dados devem vir do CapabilityResolutionResult e de sua CapabilityRequest.

Não inventar permissões amplas.

Não substituir inputs ausentes por comandos ou efeitos implícitos.

Quando allowed_tools for informado, a Tool selecionada deve estar nessa lista.

## 4. Skill Executor E Tool Executor

Reutilizar SkillExecutor e ToolExecutor existentes.

Não duplicar:

- seleção determinística de Tool;
- validação de permissões;
- validação de efeitos;
- bloqueio de Tool perigosa;
- fallback de Tool;
- construção de ProviderRequest;
- normalização de ToolExecutionResult.

SkillExecutor deve continuar sendo a camada que transforma SkillExecutionRequest
em ToolExecutionRequest.

ToolExecutor deve continuar sendo a única camada da cadeia que chama
ProviderGateway.

## 5. Provider Gateway Em Dry-Run

A integração obrigatória desta missão deve usar:

- ToolExecutionRequest.dry_run igual a True;
- ProviderRequest.dry_run igual a True;
- ProviderGateway real do projeto;
- ProviderRegistry declarativo;
- ProviderProfile fake ou local;
- nenhum adapter concreto necessário;
- nenhuma chamada de rede;
- nenhum subprocesso;
- nenhum provider externo.

O resultado esperado deve possuir:

- success igual a True;
- status igual a dry_run;
- provider_request_id;
- provider_result_id quando o contrato o gerar;
- provider_id;
- operation;
- outputs indicando dry_run;
- warnings informando que o adapter não foi executado;
- timeout aplicado quando configurado;
- guardian_decision_refs preservados;
- rastreabilidade até Tool e Skill.

O teste deve provar explicitamente que qualquer adapter injetado não foi
chamado durante o dry-run.

## 6. Governança

A cadeia deve respeitar:

- permissões da Capability;
- permissões da Skill;
- permissões da Tool;
- permissões do ProviderProfile;
- efeitos permitidos;
- data_sensitivity;
- network_policy;
- limits e timeout;
- Guardian quando configurado;
- bloqueio de elementos dangerous, blocked, disabled ou deprecated conforme
  os contratos existentes.

Não ampliar o escopo da missão 0107.

A missão 0106 pode reutilizar os pontos de Guardian já existentes, mas não deve
ainda integrar globalmente Policy Engine, Context Router, Token Budget,
Model Selection e Audit/Event Log ao fluxo inteiro.

## 7. Rastreabilidade

Preservar ou registrar referências para:

- mission_id;
- workflow_id;
- task_id;
- attempt_id;
- agent_assignment_id;
- capability request;
- capability resolution;
- skill request;
- skill result;
- tool request;
- tool result;
- provider request;
- provider result;
- runtime result;
- audit_log_ref quando existente;
- guardian_decision_refs;
- evidence_refs;
- warnings;
- errors.

IDs já existentes não devem ser recriados sem necessidade.

# Escopo Permitido

- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/capabilities/
- src/vercosa_ai_framework/skills/
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/tasks/ apenas para referências normalizadas e
  compatíveis, sem dependência das camadas inferiores
- tests/
- docs/
- README.md
- CHANGELOG.md

# Escopo Proibido

- provider real;
- chamada de rede;
- OpenCode real;
- MCP real;
- API externa;
- banco de dados;
- PostgreSQL;
- pgvector;
- RAG;
- internacionalização;
- criação de tag;
- criação de release;
- publicação de pacote;
- push automático;
- alteração destrutiva;
- reescrita ampla de Specs;
- implementação antecipada da missão 0107;
- implementação antecipada da missão 0108.

# Testes Obrigatórios

Criar testes dedicados para demonstrar:

1. CapabilityResolutionResult gera SkillExecutionRequest correto.
2. Skill selecionada pelo resolver é preservada.
3. SkillExecutor chama ToolExecutor.
4. ToolExecutor chama ProviderGateway.
5. ProviderGateway retorna dry_run sem chamar adapter.
6. mission_id, workflow_id, task_id e agent_assignment_id são preservados.
7. permissões ausentes bloqueiam antes do Provider Gateway.
8. Tool não permitida bloqueia a execução.
9. efeitos incompatíveis bloqueiam a execução.
10. ProviderProfile bloqueado, desabilitado, perigoso ou incompatível falha.
11. falha de uma Capability obrigatória impede RuntimeAdapter.
12. múltiplas Capabilities são executadas em ordem determinística.
13. execução parcial não produz sucesso.
14. caminho legado sem capability_executor permanece compatível.
15. tasks/ não importa skills, tools ou providers.
16. AgentOrchestrator não conhece adapters concretos.
17. fluxo completo Mission/Workflow/Task/Agent/Capability/Skill/Tool/Provider
    funciona com fakes locais e Provider Gateway em dry-run.
18. nenhum acesso de rede, banco ou subprocesso ocorre.

Usar fakes determinísticos e registries locais.

Não depender de credenciais, variáveis secretas ou serviços externos.

# Documentação

Criar documentação arquitetural específica para a integração 0106.

Criar exemplo mínimo executável ou testável mostrando:

Task
-> Agent
-> Capability
-> Skill
-> Tool
-> Provider Gateway dry-run

Atualizar somente documentos afetados, incluindo quando aplicável:

- README.md;
- CHANGELOG.md;
- docs/capabilities-skills-tools.md;
- docs/agent-orchestrator.md;
- docs/alignment/architecture-map.md;
- docs/alignment/current-state.md;
- docs/alignment/implementation-status.md;
- docs/alignment/roadmap.md;
- docs/alignment/open-questions.md;
- docs/architecture/module-index.md;
- docs/architecture/post-integration-architecture-review.md;
- docs/roadmap/mission-backlog.md.

Não declarar provider real implementado.

Não declarar rede, MCP ou API externa validada.

Registrar diferenças encontradas entre implementação e Specs para revisão
formal na missão 0108, sem reescrever Specs nesta missão.

Não criar links Markdown para logs locais ou arquivos ignorados pelo Git.

# Critérios De Aceite

A missão será aceita somente se:

- a cadeia Capability -> Skill -> Tool -> Provider Gateway estiver integrada;
- o caminho usar ProviderGateway real em dry-run;
- nenhum adapter concreto for chamado;
- nenhum acesso de rede ocorrer;
- AgentOrchestrator depender apenas de contrato injetável de alto nível;
- Task Queue continuar desacoplada;
- falhas bloquearem RuntimeAdapter;
- rastreabilidade for preservada;
- compatibilidade legada permanecer;
- testes novos e regressões passarem;
- documentação refletir precisamente o estado implementado;
- Specs não forem reescritas antecipadamente;
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
- verificação de ausência de chamadas de rede e subprocesso nos testes novos.

# Entrega Esperada

Entregar:

- ponte explícita CapabilityResolutionResult -> SkillExecutionRequest;
- integração injetável com AgentOrchestrator;
- cadeia SkillExecutor -> ToolExecutor -> ProviderGateway em dry-run;
- resultado rastreável da execução de Capability;
- testes unitários, de integração e regressão;
- exemplo mínimo;
- documentação atualizada;
- commit exclusivo da missão 0106.

Ao concluir, mover este arquivo para missions/done conforme o runner seguro.

Não executar push.
Não criar missão 0107.
Não criar missão 0108.

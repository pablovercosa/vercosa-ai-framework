# Status De Implementação

Links principais: [README principal](../../README.md) | [Auditoria de aderência](../audits/objective-and-scope-alignment-audit.md) | [Estado atual](current-state.md) | [Roadmap](roadmap.md) | [Perguntas em aberto](open-questions.md) | [Backlog estratégico](../roadmap/mission-backlog.md) | [CHANGELOG.md](../../CHANGELOG.md)

## Objetivo

Este documento é a fonte canônica do checklist factual de implementação do Vercosa AI Framework.

Ele diferencia planejado, implementado, integrado e validado. Existência de documentação não conta como implementação. Teste unitário isolado não conta como integração validada de fluxo.

Histórico de mudanças visíveis: [CHANGELOG.md](../../CHANGELOG.md). Planejamento futuro: [mission-backlog.md](../roadmap/mission-backlog.md).

## Definições

- Planejado: há intenção, Spec, roadmap ou pergunta em aberto, mas não há implementação operacional.
- Implementado: há código, documentação ou artefato local com testes ou evidência direta.
- Integrado: o item participa de um fluxo real com outros componentes.
- Validado: o fluxo integrado foi executado por teste, CLI, script ou relatório factual suficiente.

## Integrado E Validado

| Área | Item | Evidência | Observação |
| --- | --- | --- | --- |
| Fundação | Estrutura Python em `src/`, pacote importável e testes locais | `pyproject.toml`, `tests/`, `pytest` | Validado localmente; instalação limpa histórica ainda reprovada. |
| Runners | Runner shell individual e batch | `scripts/`, docs operacionais, logs de missões | Integração operacional real do projeto; não prova fluxo arquitetural completo. |
| Runners | Composição obrigatória de contexto de missão | `src/vercosa_ai_framework/missions/prompt_composer.py`, `scripts/vaf-run-one-mission.sh`, testes de composição | Validado por testes locais; não implementa sandbox técnico completo. |
| CLI | Comandos `status`, `missions`, `batch-summary`, `validate`, `doctor`, `docs-links`, `alpha-readiness` | `src/vercosa_ai_framework/cli/main.py`, testes CLI | CLI é leitura/diagnóstico; não executa missões. |
| Testes | Suíte pytest | `tests/` | Testes cobrem contratos e integrações parciais; não substituem fluxo ponta a ponta. |
| Empacotamento | Instalação editável local planejada com entrypoint `vaf` | `pyproject.toml`, `tests/test_python_packaging.py` | Validado por testes; reexecução limpa ainda pendente. |
| CI | Workflow mínimo localmente definido | `.github/workflows/ci.yml` | Existe; confirmação remota depende de push/execução GitHub. |
| Documentação | README, contribuição, segurança, conduta, release e arquitetura | `README.md`, `docs/`, `CHANGELOG.md` | Ampla e factual, mas volumosa. |
| Documentação | Comparação pública com OpenSpec e GitHub Spec Kit | `docs/comparacoes.md` | Documental; não implementa integração nem adapter. |
| Arquitetura | Mission Runner -> Workflow Engine -> Task Queue | `src/vercosa_ai_framework/missions/workflow_integration.py`, `src/vercosa_ai_framework/workflows/task_mapping.py`, `WorkflowEngine.execute_with_queue()`, `tests/test_mission_workflow_task_integration.py` | Validado localmente como fluxo mínimo; pode receber executor injetado para caminhos superiores. |
| Arquitetura | Task Queue -> Agent Orchestrator -> Capability Resolver | `src/vercosa_ai_framework/agents/task_executor.py`, `src/vercosa_ai_framework/agents/orchestrator.py`, `tests/test_task_agent_capability_integration.py` | Validado localmente com resolução declarativa de capabilities antes do runtime. |
| Arquitetura | Capability -> Skill -> Tool -> Provider Gateway em dry-run | `src/vercosa_ai_framework/capabilities/executor.py`, `src/vercosa_ai_framework/skills/executor.py`, `src/vercosa_ai_framework/tools/executor.py`, `src/vercosa_ai_framework/providers/gateway.py`, `tests/test_capability_skill_tool_provider_dry_run.py` | Validado localmente com ProviderGateway real em `dry_run=True`, sem provider real, adapter concreto, rede, banco, MCP ou API externa. |

## Implementado

| Área | Item | Evidência | Observação |
| --- | --- | --- | --- |
| Arquitetura | Specs canônicas `0001` a `0014` | `specs/framework/` | Mais amplas que o código atual. |
| Motores centrais | Mission Runner Python | `src/vercosa_ai_framework/missions/runner.py` | Implementado; caminho integrado opcional com Workflow/Task por injeção explícita. |
| Motores centrais | Contrato base de execução de missões `v1` | `missions/base/EXECUTION_CONTRACT.md` | Fonte normativa das regras comuns de execução; `AGENTS.md` permanece fonte global. |
| Motores centrais | Agente executor base operacional | `.opencode/agents/mission-executor-base.md` | Composto automaticamente; complementa o contrato sem substituí-lo. |
| Motores centrais | Formato compacto de missão | `missions/templates/COMPACT_MISSION_TEMPLATE.md`, `docs/operations/compact-mission-format.md` | Padrão para missões novas a partir de `0103`; legado continua compatível. |
| Motores centrais | Workflow Engine sequencial | `src/vercosa_ai_framework/workflows/engine.py` | Implementado; `execute_with_queue()` integra Task Queue no caminho Mission Runner configurado. |
| Motores centrais | Task Queue e scheduler | `src/vercosa_ai_framework/tasks/` | Implementado; integrado ao Workflow Engine e capaz de receber ponte injetada para Agent Orchestrator sem dependência direta. |
| Motores centrais | Agent Orchestrator | `src/vercosa_ai_framework/agents/` | Implementado com seleção de agente, runtime injetado, resolução declarativa opcional e execução opcional de capabilities obrigatórias por contrato injetável. |
| Motores centrais | Policy Engine | `src/vercosa_ai_framework/policy/` | Implementado; consumidores recebem `ResolvedPolicySet` opcional. |
| Motores centrais | Guardian Engine | `src/vercosa_ai_framework/guardian/` | Implementado e testado; aplicação obrigatória varia por fluxo. |
| Motores centrais | Context Router e Token Budget Manager | `src/vercosa_ai_framework/context/` | Implementados; ainda dependem de candidatos explícitos. |
| Motores centrais | Model Selection Engine | `src/vercosa_ai_framework/model_selection/` | Implementado com catálogo em memória; sem descoberta real. |
| Motores centrais | Knowledge Hub textual | `src/vercosa_ai_framework/knowledge/` | Implementado em memória; sem Semantic Index. |
| Motores centrais | Provider Gateway | `src/vercosa_ai_framework/providers/` | Implementado com adapters injetáveis e dry-run. |
| Motores centrais | Runtime Adapter OpenCode | `src/vercosa_ai_framework/runtime/` | Implementado como adapter inicial. |
| Motores centrais | Capabilities, Skills e Tools | `src/vercosa_ai_framework/capabilities/`, `skills/`, `tools/` | Implementados como cadeia MVP; o fluxo 0106 executa Skill/Tool/Provider Gateway em dry-run quando injetado explicitamente no Agent Orchestrator. |
| Auditoria | Audit/Event Log em memória | `src/vercosa_ai_framework/audit/` | Implementado; integração opcional. |
| Auditoria | Persistência JSONL opt-in | `src/vercosa_ai_framework/audit/jsonl.py` | Implementada; sem retenção, rotação ou uso global. |
| Segurança | Usage/API Limit Guard | `src/vercosa_ai_framework/guardian/usage_limits.py` | Implementado como classificação textual local. |
| Persistência | Filesystem repository | `src/vercosa_ai_framework/persistence/` | Implementado como adapter local genérico. |

## Implementado Parcialmente

| Área | Item | Evidência | Lacuna |
| --- | --- | --- | --- |
| Arquitetura | Task -> Agent | `AgentTaskExecutor` em `agents` depende de `tasks` | Existe como ponte explícita e testada; `tasks` permanece sem dependência de `agents`. |
| Arquitetura | Composição de prompt/contexto | `prompt_composer` e runner shell | Integrado ao fluxo shell; ainda não substitui Context Router arquitetural. |
| Arquitetura | Agent -> Capability -> Skill -> Tool -> Provider | módulos existem | Integrado em dry-run governado; ainda falta integração global de Policy/Context/Token/Model/Audit e providers reais continuam fora do escopo. |
| Auditoria | Eventos de decisões centrais | `audit/integrations.py` | Helpers opcionais; não obrigatórios em todos os fluxos. |
| Release | Preparação alfa | `docs/release/` | Diagnóstico `NÃO PRONTO`, checklist `REPROVADO`, tag não autorizada. |
| Segurança | Política pública inicial | `SECURITY.md` | Falta canal público definitivo e processo maduro. |
| Produção | CI mínimo | `.github/workflows/ci.yml` | Sem matriz ampla, lint, release workflow ou validação limpa automatizada. |

## Planejado

| Área | Item | Fonte | Observação |
| --- | --- | --- | --- |
| PostgreSQL | Adapter de persistência ou Knowledge/Code Intelligence | `AGENTS.md`, roadmap | Planejado como opção, não requisito. |
| pgvector | Vector store adapter | `AGENTS.md`, roadmap | Depende de contrato de Semantic Index. |
| RAG | Retrieval semântico governado | README, roadmap | Futuro; não implementado. |
| Providers | Providers reais múltiplos | Specs e docs | Devem passar por Provider Gateway. |
| Runtimes | Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI, API | `AGENTS.md` | Futuros adapters. |
| Internacionalização | Documentação pública, CLI e demais mensagens | roadmap | Em fases, após estabilização em pt-BR. |
| Observabilidade | Exportação externa, dashboard, retenção e rotação | docs arquitetura | Futuro; não confundir com Audit/Event Log atual. |
| Produção | Hardening, SLA, suporte, release estável | docs release/security | Fora do estágio atual. |

## Adiado

| Área | Item | Motivo |
| --- | --- | --- |
| PostgreSQL | Implementação real | Fluxo central ainda não integrado. |
| pgvector | Implementação real | Sem contrato final de vector store e retrieval. |
| RAG | Implementação real | Context Router e Knowledge Hub precisam de fluxo real primeiro. |
| Providers reais | Integração externa | Política, auditoria e limites ainda precisam de fluxo mínimo. |
| Múltiplos runtimes | Novos adapters | OpenCode adapter ainda precisa contrato de conformidade consolidado. |
| Internacionalização | READMEs multilíngues | Conteúdo canônico em português ainda está mudando. |
| Release alfa | Tag e publicação | Gates atuais reprovados ou pendentes. |

## Fora Do Escopo Atual

| Área | Item | Observação |
| --- | --- | --- |
| Produção | Uso crítico, SLA, hardening completo | Não prometido. |
| Release | Publicação de pacote, PyPI, GitHub Release | Exige missão e autorização explícita. |
| Infraestrutura | Tornar PostgreSQL, pgvector, Ollama, Docker, ARM64 ou systemd obrigatórios | Contraria agnosticismo do framework. |
| Segurança | Bug bounty, disclosure formal completo, sandbox garantido | Futuro. |

## Em Revisão

| Área | Item | Pergunta |
| --- | --- | --- |
| Produto | Consumidor principal | Mantenedor interno, contribuidor, usuário Python, operador CLI ou integrador? |
| Produto | Fluxo de valor principal | Qual problema concreto deve ser demonstrado primeiro? |
| Arquitetura | `SpecificationProvider` | Hipótese para integrar OpenSpec, Spec Kit ou Markdown nativo; não implementada. |
| Arquitetura | Mission Runner vs Mission Orchestrator | Separar módulo antes da próxima integração? |
| Arquitetura | Workflow Engine vs Task Queue | Handoff mínimo implementado por `execute_with_queue()`; missão 0108 deve revisar Specs/ADRs e decidir se o executor direto legado permanece. |
| Arquitetura | Agentes e capabilities | Catálogo mínimo de teste existe; catálogo aprovado para uso real ainda precisa decisão. |
| Release | Tag alfa | Deve ser adiada até fluxo de valor integrado? |
| Documentação | Volume e repetição | Quais documentos devem apontar para este checklist em vez de repetir estado? |

## Próximo Uso Deste Checklist

Atualize este documento quando uma missão alterar estado de implementação, integração, validação, release, segurança, arquitetura ou produção. Não use o `CHANGELOG.md` como checklist operacional.

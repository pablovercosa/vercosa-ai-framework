# Vercosa AI Framework

O Vercosa AI Framework é um framework open source de Harness Engineering para agentes de IA, desenvolvimento orientado por especificações e execução governada de software.

O projeto não trata o modelo de IA como o sistema inteiro. O modelo é apenas uma peça substituível dentro de uma camada operacional que organiza missões, runners, contexto, orçamento de tokens, políticas, guardrails, auditoria, seleção de modelos, providers, runtimes, validações e CLI operacional.

## Objetivo

Permitir que pessoas e agentes executem trabalho de engenharia de software de forma rastreável, segura e reproduzível, mantendo Specs, missões, workflows, tasks, agentes, capabilities, skills, tools, policies, Knowledge Hub, validações e adapters substituíveis sob uma arquitetura coerente.

O problema central que o VAF busca resolver é transformar desenvolvimento assistido por IA baseado em prompts improvisados em um processo controlado, reproduzível, auditável e orientado por especificações.

## O Problema Que O Projeto Resolve

Desenvolvimento com IA costuma falhar quando o trabalho fica concentrado em conversas soltas com modelos. Problemas recorrentes:

- dependência de prompts improvisados;
- repetição ou esquecimento de regras do projeto;
- ampliação silenciosa de escopo;
- seleção de modelos e providers sem política clara;
- crescimento de contexto sem controle;
- interrupções por quota, rate limit ou billing e estados inconsistentes após falha;
- falta de rastreabilidade entre objetivo, especificação, implementação, validação e commit;
- ações perigosas sem governança explícita;
- dificuldade de diferenciar planejado, implementado, integrado e validado.

## Como O VAF Pretende Resolver

O fluxo conceitual de valor pretendido é:

```text
objetivo
↓
especificação
↓
missão
↓
políticas e permissões
↓
composição de contexto
↓
agentes e skills
↓
seleção de modelo
↓
runtime e provider
↓
execução
↓
testes
↓
evidências
↓
auditoria
↓
commit
```

Parte desse fluxo já existe como operação local, contratos, MVPs determinísticos ou documentação. O fluxo público completo de ponta a ponta ainda não está integrado como produto único para usuário externo.

## O Produto Não É Somente O Mission Runner

O Mission Runner e o batch são infraestrutura operacional de suporte. Eles ajudam a executar missões locais com validações, parada segura e rastreabilidade, mas não são o produto inteiro.

O produto maior é a camada de Harness Engineering formada, conforme o estado aplicável de cada componente, por:

- Policy Engine, Guardian Engine e Usage/API Limit Guard;
- Context Router e Token Budget Manager;
- Model Selection Engine;
- Provider Gateway e Runtime Adapter;
- Agent Orchestrator, Capabilities, Skills e Tools;
- Knowledge Hub e Canonicalizer;
- persistência local inicial e futura persistência externa por adapters;
- Audit/Event Log;
- Mission Runner, scripts seguros, batch e CLI operacional.

Implementado hoje em MVP, contrato ou integração inicial: runners seguros, composição determinística de contexto de missão, integração mínima Mission Runner -> Workflow Engine -> Task Queue, integração Task Queue -> Agent Orchestrator -> Capability Resolver, integração Capability -> Skill -> Tool -> Provider Gateway em dry-run governado, Policy Engine, Guardian Engine, Usage/API Limit Guard, Context Router, Token Budget Manager, Knowledge Hub textual, Model Selection Engine, Runtime Adapter inicial para OpenCode, Provider Gateway, Capabilities, Skills, Tools, Agent Orchestrator, Audit/Event Log, persistência JSONL opt-in e CLI diagnóstica.

Parcialmente integrado: pontes entre políticas, Guardian, contexto, orçamento de tokens, seleção de modelo, eventos auditáveis e fluxo operacional local. Essas pontes dependem de chamada explícita ou de integração operacional específica.

Planejado ou adiado: providers reais múltiplos, persistência externa, Semantic Index, embeddings, pgvector, RAG semântico, múltiplos runtimes reais, observabilidade externa e internacionalização.

## Para Quem O Projeto É Útil

Consumidores principais plausíveis nesta fase:

- desenvolvedor individual que usa múltiplos agentes, modelos ou ferramentas e precisa reduzir improviso;
- equipe que executa desenvolvimento assistido por IA com regras, validações e auditoria;
- projeto que exige governança, segurança e rastreabilidade entre intenção, Spec, implementação e teste;
- ambiente com múltiplos modelos, providers ou runtimes que não devem ficar hardcoded no processo;
- projeto orientado por especificações que precisa transformar mudanças em missões verificáveis;
- pipeline de execução prolongada que precisa preservar contexto, estado, evidências e recuperação após falhas.

Essa lista descreve consumidores pretendidos ou plausíveis. O repositório ainda não declara adoção real por usuários externos.

## O Que O Framework Não Pretende Substituir

O VAF não pretende substituir:

- modelos de IA;
- Git;
- CI/CD;
- bancos de dados;
- OpenCode ou outros executores;
- ferramentas completas de Specification-Driven Development;
- controles do sistema operacional;
- revisão humana.

PostgreSQL, pgvector, RAG e internacionalização só devem avançar quando servirem ao fluxo principal de valor. No estado atual, eles permanecem futuros, opcionais ou adiados.

## Prompt Engineering, Agent Framework E Harness Engineering

- Prompt Engineering foca em instruções, exemplos e formato de entrada para melhorar a resposta de um modelo.
- Agent Framework foca em agentes, ferramentas, memória, planejamento e execução automatizada de tarefas.
- Harness Engineering foca na camada operacional ao redor dos agentes e modelos: execução governada, limites, políticas, auditoria, validação, rastreabilidade, orquestração, adaptação de runtimes e integração segura com providers.

O VAF se posiciona como Harness Engineering: ele organiza o ambiente em que agentes de IA trabalham, em vez de depender apenas de prompts ou de um agente monolítico.

## O Que O Framework É

- Um framework Specification First para desenvolvimento assistido por IA.
- Uma arquitetura AI Native para execução governada, rastreabilidade, segurança operacional, evolução por missões, separação de responsabilidades, testes e documentação progressiva.
- Um harness model agnostic, provider agnostic, runtime agnostic e storage agnostic como direção arquitetural.
- Um conjunto de contratos e MVPs em Python para Mission Runner, Workflow Engine, Task Queue, Agent Orchestrator, Policy Engine, Guardian Engine, Usage/API Limit Guard, Audit/Event Log, Context Router, Token Budget Manager, Knowledge Hub, Model Selection Engine, Runtime Adapter, Provider Gateway, CLI operacional e adapters iniciais.

## O Que O Framework Não É

- Não é um IDE.
- Não é um MCP server.
- Não é um único agente.
- Não é apenas um wrapper de OpenCode, Claude Code, Codex CLI, Cursor ou outro runtime.
- Não é dependente de PostgreSQL, pgvector, Ollama, ARM64, systemd ou SSH.
- Não é uma coleção de prompts sem Specs, validação e governança.

## Estado Atual

Status: MVP operacional inicial com fundação arquitetural e contratos em evolução.

As Specs em `specs/framework/` descrevem a arquitetura desejada. O código em `src/vercosa_ai_framework/` implementa MVPs determinísticos e integrações iniciais. O trecho Mission Runner -> Workflow Engine -> Task Queue já possui fluxo mínimo validado, o trecho Task Queue -> Agent Orchestrator -> Capability Resolver possui integração validada, o trecho Capability -> Skill -> Tool -> Provider Gateway possui integração em dry-run governado e o caminho mínimo 0107 integrou Policy/Context/Token/Guardian/Model/Audit antes de Capability/Runtime por dependências injetadas. Provider real, rede, banco, MCP, API externa, RAG, PostgreSQL, pgvector e múltiplos runtimes reais ainda não fazem parte desse fluxo.

A documentação pública inicial está sendo preparada para uma futura alfa pública, mas isso não significa release publicada, tag criada, pacote distribuído ou estabilidade de produção. A versão alfa planejada é documentada como `0.1.0-alpha.1`, sem publicação realizada. A política inicial está em [docs/release/versioning-policy.md](docs/release/versioning-policy.md), a política de release está em [docs/release/release-policy.md](docs/release/release-policy.md), o checklist pré-tag está em [docs/release/pre-release-checklist.md](docs/release/pre-release-checklist.md), o plano alfa está em [docs/release/alpha-version-plan.md](docs/release/alpha-version-plan.md), as notas alfa preliminares estão em [docs/release/release-notes-alpha.md](docs/release/release-notes-alpha.md), o checklist documental está em [docs/release/public-alpha-readiness.md](docs/release/public-alpha-readiness.md), o diagnóstico local de prontidão alfa está em [docs/release/alpha-readiness-diagnostic.md](docs/release/alpha-readiness-diagnostic.md), a consolidação local preparatória está em [docs/release/alpha-candidate-summary.md](docs/release/alpha-candidate-summary.md), a solicitação futura de decisão de tag está em [docs/release/tag-decision-request.md](docs/release/tag-decision-request.md) e o histórico inicial está em [CHANGELOG.md](CHANGELOG.md).

A revisão arquitetural pós-integrações está em [docs/architecture/post-integration-architecture-review.md](docs/architecture/post-integration-architecture-review.md) e consolida o estado após as integrações concluídas até a missão 0080.

O repositório possui empacotamento Python local mínimo em `pyproject.toml`, com versão PEP 440 `0.1.0a1` equivalente à alfa planejada `0.1.0-alpha.1`. Isso permite instalação editável em ambiente virtual para desenvolvimento, mas não significa pacote publicado, release alfa publicada, tag criada ou distribuição via PyPI.

O repositório também possui CI mínimo em GitHub Actions em `.github/workflows/ci.yml`. O workflow roda em pull requests e pushes para `main`, instala o projeto em modo desenvolvimento com o extra `dev`, executa `pytest`, valida links Markdown relativos com `python -m vercosa_ai_framework.cli.main docs-links`, executa `alpha-readiness` como diagnóstico não bloqueante e valida `python -m compileall src`. Esse CI não publica pacote, não cria release, não usa secrets, não executa missões, não chama providers e não substitui a validação local.

Implementado em estado MVP ou contrato inicial:

- Mission Runner local, fila em diretórios e integração opcional com eventos auditáveis em Python.
- Integração mínima Mission Runner -> Workflow Engine -> Task Queue por contratos injetáveis e execução queue-backed.
- Integração mínima Task Queue -> Agent Orchestrator -> Capability Resolver por executor injetado.
- Integração Capability -> Skill -> Tool -> Provider Gateway em dry-run governado por executor de capability injetável, sem provider real, rede, banco, MCP ou API externa.
- Runner seguro de uma missão e runner seguro em batch por scripts operacionais.
- Composição obrigatória de contexto de missão pelo runner, com `AGENTS.md`, contrato base versionado, agente executor base, agentes operacionais especializados declarados e missão específica.
- Formato compacto para missões novas a partir de `0103`, com frontmatter validável e negação por padrão para capacidades perigosas.
- Policy Engine declarativo e Guardian Engine determinístico.
- Usage/API Limit Guard para classificar sinais textuais de limite externo em logs já recebidos.
- Context Router, Token Budget Manager e `ContextPackage` determinísticos.
- Knowledge Hub com ingestão Markdown, store em memória, busca textual e adaptação para candidatos de contexto.
- Model Selection Engine com catálogo em memória, políticas resolvidas opcionais e requisitos opcionais de orçamento de tokens.
- Runtime Adapter inicial para OpenCode.
- Provider Gateway, Tools, Skills, Capabilities e Agent Orchestrator como cadeia MVP de contratos.
- Audit/Event Log em memória com persistência local JSONL opt-in e helpers opcionais para decisões e ciclo de vida de missão; a arquitetura dedicada está em [docs/architecture/audit-event-architecture.md](docs/architecture/audit-event-architecture.md).
- CLI operacional inicial com `status`, `missions`, `validate`, `doctor`, `batch-summary`, `docs-links` e `alpha-readiness`.

O que já funciona de forma factual e resumida:

- fila local de missões;
- execução segura individual;
- execução segura em batch;
- parada na primeira falha;
- recuperação operacional por estado de missão e restauração quando a composição falha;
- commit por missão quando o fluxo operacional configurado o exige;
- bloqueio de push automático por padrão;
- detecção textual de sinais de limite de uso/API em logs já recebidos;
- testes e validações locais;
- logs operacionais e eventos auditáveis opcionais;
- diagnósticos pela CLI;
- contrato base de execução;
- formato compacto para missões novas;
- composição determinística de contexto de missão.

Ainda são futuros ou lacunas:

- Fluxo público completo de ponta a ponta para usuário externo.
- CLI predominantemente diagnóstica, sem executar missões.
- Motores centrais ainda parcialmente integrados ou acionados por chamador explícito; Skill -> Tool -> Provider Gateway existe em dry-run e Policy/Context/Token/Model/Audit foram validados no caminho mínimo 0107, mas ainda não representam provider real, rede, banco, MCP, RAG, persistência externa ou fluxo público completo de produto.
- Providers reais adiados.
- Persistência externa adiada.
- PostgreSQL, pgvector e RAG adiados.
- Internacionalização adiada.
- Tag alfa bloqueada até demonstração do fluxo de valor e cumprimento dos gates documentados.
- RAG semântico.
- Embeddings.
- pgvector como adapter real.
- Semantic Index.
- Múltiplos providers reais.
- Persistência externa de eventos.
- Retenção e rotação de eventos auditáveis.
- Internacionalização dos READMEs.

Esses recursos não devem ser interpretados como implementados no estado atual.

## Comparação Com Outras Abordagens

OpenSpec e GitHub Spec Kit atuam principalmente na organização e execução de processos orientados por especificações para agentes de codificação. O VAF pretende concentrar sua diferenciação na execução governada, auditável e agnóstica de runtime/provider, sem tratar esses projetos como adversários.

A comparação factual, com fontes oficiais consultadas e separação entre VAF atual e VAF pretendido, está em [docs/comparacoes.md](docs/comparacoes.md).

## Runtime Inicial

OpenCode é o runtime e laboratório inicial. Ele permanece atrás de adapter em `runtime/` e não define o núcleo do framework. O VAF deve poder suportar outros runtimes e interfaces no futuro sem transformar nenhum deles no centro arquitetural.

## Arquitetura Resumida

Fluxo conceitual principal:

```text
Mission Runner
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Capabilities
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Runtime Adapter / Providers / MCPs / APIs
```

Eixo de governança:

- Policy Engine resolve políticas declarativas.
- Guardian Engine avalia ações concretas, riscos e pacotes de contexto.
- Usage/API Limit Guard classifica sinais textuais de limite externo.
- Audit/Event Log registra eventos estruturados quando um `EventLog` é fornecido.

Eixo de contexto e memória:

- Knowledge Hub organiza documentos textuais e busca textual MVP.
- Context Router monta `ContextPackage` a partir de candidatos explícitos.
- Token Budget Manager estima orçamento de tokens de forma determinística.
- `ContextPackage` preserva itens selecionados, omissões, citações, warnings, refs de política e requisitos mínimos para seleção de modelo.

Eixo operacional:

- Runner seguro de uma missão: `scripts/vaf-run-next-safe.sh`.
- Runner seguro em batch: `scripts/vaf-run-batch-safe.sh`.
- CLI operacional: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status|missions|batch-summary|validate|doctor|docs-links|alpha-readiness`.
- Listagem local de missões por estado: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions [--state queue|running|done|failed]`.
- Resumo pós-batch auxiliar: `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary`.
- Playbooks e checklists documentam execução, validação e revisão pós-batch.

## Fluxo Operacional Padrão

O fluxo operacional padrão do projeto é executar missões em batch quando o bloco em `missions/queue/` estiver bem especificado, revisado e seguro. O batch continua usando missões completas em Markdown, uma missão por arquivo, escopo claro, restrições explícitas, critérios de aceite verificáveis, commits separados, parada na primeira falha, validação pós-batch e push manual por padrão.

Antes da execução, o runner compõe determinísticamente o contexto com `AGENTS.md`, `missions/base/EXECUTION_CONTRACT.md`, `.opencode/agents/mission-executor-base.md`, agentes operacionais especializados declarados e a missão. Missões compactas usam `missions/templates/COMPACT_MISSION_TEMPLATE.md`; missões legadas continuam compatíveis.

Use `VAF_BATCH_SIZE=8` para blocos normais já revisados. Use `VAF_BATCH_SIZE=3` para testes, retomadas, blocos pequenos ou recuperação. Use `./scripts/vaf-run-next-safe.sh` para missões sensíveis, arquiteturais, incertas, de alto risco, investigação de erro ou recuperação após falha.

`VAF_AUTO_PUSH=1` continua sendo opt-in. A prática recomendada é validar o batch com o checklist operacional e fazer push manual somente depois de revisar estado das missões, testes, `compileall`, Git e commits.

## Mapa De Módulos

O mapa navegável oficial está em [docs/architecture/module-index.md](docs/architecture/module-index.md).

Módulos principais:

- [cli](src/vercosa_ai_framework/cli/README.md)
- [core](src/vercosa_ai_framework/core/README.md)
- [missions](src/vercosa_ai_framework/missions/README.md)
- [workflows](src/vercosa_ai_framework/workflows/README.md)
- [tasks](src/vercosa_ai_framework/tasks/README.md)
- [agents](src/vercosa_ai_framework/agents/README.md)
- [capabilities](src/vercosa_ai_framework/capabilities/README.md)
- [policy](src/vercosa_ai_framework/policy/README.md)
- [guardian](src/vercosa_ai_framework/guardian/README.md)
- [audit](src/vercosa_ai_framework/audit/README.md)
- [context](src/vercosa_ai_framework/context/README.md)
- [model_selection](src/vercosa_ai_framework/model_selection/README.md)
- [knowledge](src/vercosa_ai_framework/knowledge/README.md)
- [canonicalizer](src/vercosa_ai_framework/canonicalizer/README.md)
- [skills](src/vercosa_ai_framework/skills/README.md)
- [tools](src/vercosa_ai_framework/tools/README.md)
- [providers](src/vercosa_ai_framework/providers/README.md)
- [runtime](src/vercosa_ai_framework/runtime/README.md)
- [persistence](src/vercosa_ai_framework/persistence/README.md)

## Estrutura Do Repositório

- `AGENTS.md`: contexto central para agentes e regras de colaboração.
- `missions/base/EXECUTION_CONTRACT.md`: contrato base versionado das regras comuns de execução de missões.
- `missions/templates/COMPACT_MISSION_TEMPLATE.md`: template compacto para missões novas.
- `specs/framework/`: Specs do framework.
- `docs/`: documentação técnica, alinhamento, arquitetura, operações e exemplos.
- `src/vercosa_ai_framework/`: contratos e MVPs do framework.
- `knowledge/`: visão, princípios, arquitetura de referência e ADRs.
- `.opencode/`: integração inicial com OpenCode como laboratório/runtime.
- `.github/`: templates iniciais de issues e pull requests para colaboração futura.
- `.github/workflows/ci.yml`: CI mínimo com GitHub Actions para testes e `compileall`, sem release ou publicação de pacote.

## Operação Local

Guia inicial para preparar um checkout de desenvolvimento: [Instalação local para desenvolvimento](docs/getting-started/local-installation.md).

Instalação local editável em ambiente virtual:

```bash
python3 -m pip install -e ".[dev]"
```

Após essa instalação local, o atalho `vaf` pode ser usado dentro do ambiente virtual. A forma explícita `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main` continua suportada para diagnóstico de checkout.

Checklist manual para validar instalação limpa antes de uma futura alfa: [Checklist de instalação limpa](docs/getting-started/clean-install-checklist.md). Uma execução real foi registrada em [Registro de validação limpa](docs/release/clean-install-validation.md) com resultado `REPROVADO`; nova execução aprovada ainda é necessária antes de release.

Guia inicial para contribuir com segurança: [CONTRIBUTING.md](CONTRIBUTING.md).

Templates iniciais para issues e pull requests estão em [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) e [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md).

Conduta inicial para colaboração: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Segurança, Licença E Uso Responsável

A licença final do projeto ainda está pendente e deve ser definida antes de uma release pública. O estado atual da decisão está documentado em [Notas de licença](docs/legal/license-notes.md).

Use o projeto de forma conservadora conforme a [política inicial de uso responsável](docs/legal/usage-policy.md), a [política inicial de segurança](SECURITY.md) e o [código de conduta inicial](CODE_OF_CONDUCT.md). Esta documentação não substitui revisão jurídica formal, processo público maduro de segurança, governança comunitária madura ou validação humana antes de executar missões, comandos, tools, providers ou runtimes.

Scripts operacionais:

- `./scripts/vaf-run-next-safe.sh`: executa uma missão com validações antes e depois.
- `./scripts/vaf-run-batch-safe.sh`: executa um batch sequencial seguro e para na primeira falha.
- `./scripts/vaf-status.sh`: mostra estado operacional dos diretórios de missão.

CLI inicial:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main status
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main missions
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main batch-summary
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness
```

A CLI não substitui `pytest`, `python3 -m compileall src`, os scripts seguros ou revisão humana quando a política exigir. O comando `missions` apenas lista arquivos Markdown por estado e não executa, move ou edita missões. O comando `batch-summary` resume contagens pós-batch, último log local e lembretes de validação manual, sem executar testes, Git, scripts, missões, rede, banco ou providers. O comando `docs-links` valida links relativos em documentos Markdown locais e ignora links externos, sem acessar rede e sem validar âncoras de forma completa. O comando `alpha-readiness` verifica presença documental mínima, diretórios operacionais, contagens de missões e CI local para a futura alfa, mas não cria tag, não publica release, não publica pacote, não executa testes e não substitui o checklist pré-tag.

## Documentação Relevante

- [Guia inicial de contribuição](CONTRIBUTING.md)
- [Código de conduta inicial](CODE_OF_CONDUCT.md)
- [Changelog inicial](CHANGELOG.md)
- [Comparação com OpenSpec e GitHub Spec Kit](docs/comparacoes.md)
- [Política inicial de versionamento](docs/release/versioning-policy.md)
- [Política inicial de release](docs/release/release-policy.md)
- [Checklist pré-tag](docs/release/pre-release-checklist.md)
- [Plano da versão alfa inicial](docs/release/alpha-version-plan.md)
- [Notas preliminares da futura alfa](docs/release/release-notes-alpha.md)
- [Diagnóstico local de prontidão alfa](docs/release/alpha-readiness-diagnostic.md)
- [Consolidação local do candidato alfa](docs/release/alpha-candidate-summary.md)
- [Solicitação futura de decisão sobre tag alfa](docs/release/tag-decision-request.md)
- [Política inicial de segurança](SECURITY.md)
- [Política inicial de uso responsável](docs/legal/usage-policy.md)
- [Diretrizes de convivência e colaboração](docs/conduct/community-guidelines.md)
- [Notas de licença](docs/legal/license-notes.md)
- [Índice de contribuição](docs/contributing/README.md)
- [Instalação local para desenvolvimento](docs/getting-started/local-installation.md)
- [Checklist de instalação limpa](docs/getting-started/clean-install-checklist.md)
- [Índice de módulos](docs/architecture/module-index.md)
- [Integração Mission Runner, Workflow Engine e Task Queue](docs/architecture/mission-workflow-task-integration.md)
- [Integração Task, Agent e Capability](docs/architecture/task-agent-capability-integration.md)
- [Revisão arquitetural pós-integrações](docs/architecture/post-integration-architecture-review.md)
- [Arquitetura de Audit/Event Log](docs/architecture/audit-event-architecture.md)
- [Checklist de prontidão para alfa pública](docs/release/public-alpha-readiness.md)
- [Backlog estratégico de missões](docs/roadmap/mission-backlog.md)
- [Playbook de execução em batch](docs/operations/batch-execution-playbook.md)
- [Checklist de validação pós-batch](docs/operations/post-batch-validation-checklist.md)
- [Exemplos operacionais](docs/examples/README.md)
- [Estado atual](docs/alignment/current-state.md)
- [Roadmap](docs/alignment/roadmap.md)
- [Padrão de README](docs/documentation/readme-standard.md)
- [Padrão de idioma e commits](docs/documentation/language-and-commit-standard.md)
- [Política de atualização de documentação](docs/documentation/documentation-update-policy.md)

## Specs Principais

- [Spec 0001: Framework Foundation](specs/framework/0001-framework-foundation.md)
- [Spec 0002: Model Selection Engine](specs/framework/0002-model-selection-engine.md)
- [Spec 0003: OpenCode Runtime Adapter](specs/framework/0003-opencode-runtime-adapter.md)
- [Spec 0004: Mission Runner](specs/framework/0004-mission-runner.md)
- [Spec 0005: Guardian Engine](specs/framework/0005-guardian-engine.md)
- [Spec 0006: Workflow Engine](specs/framework/0006-workflow-engine.md)
- [Spec 0007: Task Queue](specs/framework/0007-task-queue.md)
- [Spec 0008: Agent Orchestrator](specs/framework/0008-agent-orchestrator.md)
- [Spec 0009: Capabilities, Skills e Tools](specs/framework/0009-capabilities-skills-tools.md)
- [Spec 0010: Provider Gateway](specs/framework/0010-provider-gateway.md)
- [Spec 0011: Knowledge Hub](specs/framework/0011-knowledge-hub.md)
- [Spec 0012: Canonicalizer](specs/framework/0012-canonicalizer.md)
- [Spec 0013: Persistence Layer](specs/framework/0013-persistence-layer.md)
- [Spec 0014: Context Router, Token Budget Manager e Memory Architecture](specs/framework/0014-context-router-token-budget-memory.md)

## Princípios

- Specification First
- AI Native
- Provider Agnostic
- Local First
- Extensible by Design
- Security by Design
- Token Efficiency
- Governance by Design

## Idioma E Commits

O idioma oficial da documentação do projeto é português do Brasil. Termos técnicos e nomes arquiteturais consolidados podem permanecer em inglês quando fizerem parte da API, arquitetura ou vocabulário do framework.

Mensagens de commit futuras devem usar português do Brasil. O histórico Git já publicado não deve ser reescrito apenas para traduzir mensagens antigas.

## Regras De Trabalho

- Nenhum código deve ser implementado sem Spec aprovada.
- Contribuições devem seguir o [guia inicial de contribuição](CONTRIBUTING.md).
- Documentação deve refletir o estado real do código e das Specs.
- Recursos futuros devem ser marcados como futuros, lacunas ou próximos passos.
- Agentes não devem chamar providers, MCPs, APIs, bancos ou filesystem diretamente; agentes solicitam capabilities.
- Links de documentação devem ser relativos.
- Mudanças arquiteturais materiais devem gerar ADR, Spec update ou pergunta registrada.

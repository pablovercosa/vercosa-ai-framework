# Estado Atual

## Objetivo

Registrar o estado arquitetural do Vercosa AI Framework após as integrações concluídas até a missão 0080 e antes da próxima onda de implementação.

Atualização da missão 0101: a auditoria estratégica de aderência ao objetivo e escopo está registrada em [docs/audits/objective-and-scope-alignment-audit.md](../audits/objective-and-scope-alignment-audit.md). O checklist canônico de implementação passa a ser [docs/alignment/implementation-status.md](implementation-status.md). Este documento deve resumir estado e apontar para o checklist, não duplicar todo o controle operacional.

Atualização da missão 0103: o README passou a explicitar o problema central, o fluxo de valor pretendido, consumidores plausíveis, limites do projeto e o estado real do VAF. A comparação factual com OpenSpec e GitHub Spec Kit está em [docs/comparacoes.md](../comparacoes.md).

Classificação geral da auditoria: `ALINHADO COM RESSALVAS`.

Ressalvas principais: o fluxo operacional interno por missões e batch existe, o fluxo mínimo Mission Runner -> Workflow Engine -> Task Queue foi integrado por contratos injetáveis, a ponte Task Queue -> Agent Orchestrator -> Capability Resolver foi validada e o caminho Capability -> Skill -> Tool -> Provider Gateway foi demonstrado em dry-run governado. Providers reais, rede, banco, MCP e API externa seguem fora do fluxo; vários motores seguem MVPs opcionais; a preparação alfa avançou antes de uma demonstração completa de valor integrado; `LICENSE` está ausente; instalação limpa e checklist pré-tag permanecem reprovados em registros locais.

Este checkpoint é apenas documental. Ele não aprova novo código, novo comportamento de runtime, alterações de configuração global, operações privilegiadas ou expansão de funcionalidades.

A revisão arquitetural pós-integrações está registrada em [docs/architecture/post-integration-architecture-review.md](../architecture/post-integration-architecture-review.md).

## O Que O Framework É

O Vercosa AI Framework é um framework open source de Harness Engineering para agentes de IA, desenvolvimento de software orientado por especificações e execução governada assistida por IA.

Seu objetivo central é organizar a camada operacional ao redor de modelos e agentes em torno de missões, Specs, workflows, políticas, agentes, capabilities, contexto, orçamento de tokens, conhecimento, validação, auditoria e adapters agnósticos de provider, runtime e storage.

O framework pretende ser:

- Specification First: Specs são fonte da verdade para implementação.
- AI Native: IA participa de planejamento, implementação, revisão, validação, documentação e aprendizado.
- Provider Agnostic: modelos, providers, runtimes, vector stores, IDEs, APIs, MCPs e bancos são adapters substituíveis.
- Local First: execução local deve ser possível quando houver capacidades disponíveis, sem tornar infraestrutura local obrigatória.
- Extensible by Design: mecanismos concretos devem ficar atrás de contratos ou adapters.
- Security by Design: Guardian Specs e decisões Guardian restringem execução.
- Token Efficient: contexto deve ser selecionado, comprimido, referenciado ou recuperado em vez de enviado de forma redundante.
- Governance by Design: decisões, critérios, políticas, validações, riscos e logs devem ser explícitos.

## O Que O Framework Não É

O framework não é:

- um IDE;
- um MCP server;
- um único agente;
- um wrapper de OpenCode;
- um wrapper de Claude Code;
- um wrapper de Codex CLI;
- uma distribuição de LangGraph, MetaGPT ou AutoGen;
- um produto dependente apenas de PostgreSQL;
- um produto dependente apenas de Ollama;
- um projeto específico para ARM64;
- uma coleção de prompts;
- um script de automação específico de runtime;
- substituto para Specs, validação, revisão de segurança ou aprovação humana quando política exigir.

OpenCode é atualmente runtime e laboratório inicial. Ele não é o centro arquitetural.

O VAF também não substitui ferramentas completas de Specification-Driven Development. Projetos como OpenSpec e GitHub Spec Kit podem ser complementares como fontes de artefatos ou processos de especificação, mas qualquer integração deve ser tratada como hipótese/adaptação futura até decisão e implementação específicas.

## Estado Do Repositório

O repositório está em transição de fundação/MVP para um MVP interno mais coerente. A base operacional já permite executar missões locais de forma controlada, validar batches seguros, diagnosticar estado básico pela CLI, registrar eventos auditáveis iniciais em Python quando o chamador injeta um `EventLog`, persistir eventos auditáveis em JSONL local quando o chamador opta explicitamente por `JsonlAuditEventLog` e consultar uma revisão arquitetural pós-integrações para orientar próximos blocos.

Ativos principais:

- `AGENTS.md`: contexto operacional central e regras arquiteturais para agentes.
- `README.md`: resumo público do projeto, identidade de Harness Engineering e limites do MVP atual.
- `CONTRIBUTING.md`: guia inicial de contribuição com fluxo por missões, validações, documentação, idioma, commits e limites operacionais.
- `CODE_OF_CONDUCT.md` e `docs/conduct/`: código de conduta inicial e diretrizes práticas de convivência, ainda sem canal público definitivo ou governança comunitária madura.
- `SECURITY.md` e `docs/security/`: política inicial de segurança e orientação conservadora para reporte responsável, ainda sem canal público definitivo de vulnerabilidades.
- `docs/legal/`: documentação legal inicial com política de uso responsável e notas sobre licença pendente.
- `docs/getting-started/local-installation.md`: guia inicial de instalação local para desenvolvimento, validações básicas e uso inicial da CLI.
- `docs/getting-started/clean-install-checklist.md`: checklist documental para validação manual de instalação limpa, executado uma vez em cópia temporária local com resultado `REPROVADO`.
- `docs/release/public-alpha-readiness.md`: checklist de prontidão documental para futura alfa pública, sem criar release, tag, pacote ou promessa de estabilidade.
- `docs/release/clean-install-validation.md`: registro factual da validação de instalação limpa de 2026-07-10, classificada como `REPROVADO`.
- `docs/release/versioning-policy.md` e `docs/release/alpha-version-plan.md`: política inicial de versionamento e plano da versão alfa `0.1.0-alpha.1`, sem release publicada.
- `docs/release/release-policy.md` e `docs/release/pre-release-checklist.md`: política inicial de release e checklist pré-tag, ambos manuais e sem criar tag, release ou pacote.
- `docs/release/release-notes-alpha.md`: release notes alfa preliminares para a futura `0.1.0-alpha.1`, sem declarar release publicada, tag criada ou pacote publicado.
- `docs/release/alpha-readiness-diagnostic.md`: diagnóstico local de prontidão alfa executado em 2026-07-11, classificado como `NÃO PRONTO`, sem criar tag, release ou pacote.
- `docs/release/pre-tag-checklist-execution.md`: execução local do checklist pré-tag alfa registrada em 2026-07-11, classificada como `REPROVADO`, sem criar tag, release, pacote ou confirmação de CI remoto.
- `docs/release/alpha-candidate-summary.md`: consolidação local preparatória do candidato alfa `0.1.0-alpha.1`, sem criar tag, publicar release, publicar pacote, fazer push ou confirmar CI remoto.
- `docs/release/tag-decision-request.md`: solicitação futura de decisão sobre tag alfa, sem autorização automática e dependente de validação final, push, CI remoto e autorização explícita.
- `CHANGELOG.md`: changelog inicial do estado não publicado, com versão alfa planejada documentada, sem tag, release publicada ou promessa de estabilidade de produção.
- `missions/base/EXECUTION_CONTRACT.md`: contrato base versionado `v1` para regras comuns de execução de missões.
- `missions/templates/COMPACT_MISSION_TEMPLATE.md`: template compacto para missões novas a partir de `0103`.
- `.opencode/agents/mission-executor-base.md`: agente executor base operacional composto automaticamente pelo runner.
- `pyproject.toml`: empacotamento Python local mínimo com `setuptools`, descoberta do pacote em `src`, versão PEP 440 `0.1.0a1`, extra opcional `dev` para `pytest` e console script local `vaf`, sem pacote publicado.
- `.github/workflows/ci.yml`: CI mínimo em GitHub Actions para pull requests e pushes em `main`, com instalação editável, `pytest`, validação local de links Markdown relativos, diagnóstico não bloqueante `alpha-readiness` e `python -m compileall src`, sem publicar pacote, criar release, executar missões, acessar banco, chamar providers ou usar secrets.
- `docs/architecture/post-integration-architecture-review.md`: revisão arquitetural pós-integrações, com estado real, limites, riscos e recomendações.
- `.github/ISSUE_TEMPLATE/` e `.github/PULL_REQUEST_TEMPLATE.md`: templates iniciais para colaboração pública futura, sem processo público maduro ou SLA.
- `knowledge/`: visão, princípios e notas de arquitetura central.
- `specs/framework/`: Specs do framework.
- `docs/`: documentação técnica e de alinhamento.
- `src/vercosa_ai_framework/`: componentes Python agnósticos de provider, runtime e storage, com contratos e MVPs determinísticos.

## Estado Das Specs

As Specs definem uma arquitetura mais ampla do que o código atual implementa.

Specs atuais:

- `0001-framework-foundation.md`: fundação conceitual do framework.
- `0002-model-selection-engine.md`: Model Selection Engine orientado por política e agnóstico de provider.
- `0003-opencode-runtime-adapter.md`: OpenCode como Runtime Adapter, não core.
- `0004-mission-runner.md`: ciclo de vida de missão, fila, ciclos, logs, validação e budgets.
- `0005-guardian-engine.md`: decisões de política, risco, limites e controles; a ADR de Policy Engine versus Guardian Engine separa resolução declarativa de enforcement operacional.
- `0006-workflow-engine.md`: workflows, decomposição de tasks, dependências, validação e replanejamento.
- `0007-task-queue.md`: estado de tasks, dependências, tentativas, retries e scheduler.
- `0008-agent-orchestrator.md`: seleção de agentes e subagentes sem acoplamento direto a providers/tools/MCPs.
- `0009-capabilities-skills-tools.md`: cadeia de capabilities para skills, tools e providers/MCPs/APIs.
- `0010-provider-gateway.md`: fronteira governada entre tools e providers concretos.
- `0011-knowledge-hub.md`: documentos canônicos, índices semânticos, fontes, retrieval e governança.
- `0012-canonicalizer.md`: conversão para Markdown canônico e normalização governada.
- `0013-persistence-layer.md`: portas de persistência, adapters, registros determinísticos, retenção e bancos futuros.
- `0014-context-router-token-budget-memory.md`: Context Router, Token Budget Manager e arquitetura de memória.

## Módulos MVP Implementados

O pacote `src/vercosa_ai_framework/` contém implementações MVP e contratos para:

- `core/`: primitivas de domínio e política.
- `cli/`: CLI operacional inicial para status local básico, listagem de missões por estado, resumo pós-batch auxiliar, validação estrutural local, validação local de links Markdown, diagnóstico de prontidão alfa, versão e diagnóstico simples; ela não substitui scripts shell nem executa missões nesta fase.
- `missions/`: tipos, fila em diretório e runner de missões.
- `workflows/`: tipos e engine sequencial de workflow.
- `tasks/`: tipos, fila, scheduler, tentativas e transições de estado.
- `policy/`: contratos e resolução determinística MVP de políticas declarativas, precedência simples e conflitos básicos.
- `guardian/`: Guardian Engine determinístico com decisões estruturadas e detecção inicial de sinais textuais de limite de uso/API sem chamadas externas.
- `audit/`: contratos iniciais de Audit/Event Log, tipos de evento, implementação em memória, persistência local JSONL opt-in, helpers opcionais para decisões centrais e eventos básicos de ciclo de vida de missão.
- `context/`: Context Router, Token Budget Manager e `ContextPackage` determinísticos.
- `model_selection/`: políticas, tipos e selector MVP.
- `runtime/`: contrato de Runtime Adapter e OpenCode Runtime Adapter MVP.
- `agents/`: perfis, registry, orchestrator MVP e ponte `AgentTaskExecutor` para scheduler.
- `capabilities/`: perfis, registry e resolver declarativo integrado ao caminho de agente quando configurado.
- `skills/`: perfis, registry e executor.
- `tools/`: perfis, registry e executor.
- `providers/`: perfis, registry, contrato de adapter e gateway.
- `knowledge/`: ingestão Markdown, documentos, store em memória e busca textual.
- `canonicalizer/`: canonicalização, hashes, warnings e conversão para Knowledge Hub.
- `persistence/`: tipos, contrato de repository e filesystem repository local.
- runners seguros: scripts operacionais para execução segura de uma missão e execução segura em batch, com validações locais. Batch é o fluxo operacional padrão para blocos revisados e seguros; execução individual continua válida para risco alto, investigação e recuperação.

Módulos centrais existentes no estado atual:

- `audit`.
- `cli`.
- `policy`.
- `guardian`.
- `context`.
- `model_selection`.
- `missions`.
- `providers`.
- `runtime`.
- `knowledge`.
- `persistence`.
- `workflows`.
- `tasks`.
- `agents`.
- `capabilities`.
- `skills`.
- `tools`.

## Integrações Centrais Atuais

Integrações já feitas em estado MVP ou integração inicial:

- Policy Engine integrado ao Guardian Engine por `ResolvedPolicySet` opcional fornecido pelo chamador.
- Policy Engine integrado ao Context Router por `ResolvedPolicySet` opcional fornecido pelo chamador.
- Policy Engine integrado ao Model Selection por políticas resolvidas opcionais.
- Token Budget Manager integrado ao Model Selection por requisitos mínimos derivados de orçamento.
- Knowledge Hub integrado ao Context Router por candidatos explícitos e busca textual MVP.
- Guardian Engine capaz de avaliar `ContextPackage` quando chamado explicitamente.
- Usage/API Limit Guard disponível para classificar sinais textuais de limite externo de API em logs já recebidos.
- Audit/Event Log inicial com helpers opcionais para eventos de Policy, Guardian, Context e ciclo de vida de missão/batch.
- `MissionRunner` Python capaz de registrar eventos de missão quando recebe `EventLog` opcional.
- `MissionRunner` Python capaz de executar caminho integrado opcional com `WorkflowEngine.execute_with_queue()` e `TaskQueue` quando recebe `MissionWorkflowProvider` e `MissionWorkflowExecutor`.
- `TaskScheduler` capaz de acionar `AgentOrchestrator` por `AgentTaskExecutor` injetado, com resolução declarativa de capabilities obrigatórias antes do runtime.
- `prompt_composer` em `src/vercosa_ai_framework/missions/` capaz de compor contexto efetivo de execução com `AGENTS.md`, contrato base, agente executor base, agentes operacionais especializados declarados, permissões e missão específica.
- Runner shell integrado ao compositor antes da chamada ao OpenCode, com restauração para `queue` quando a composição falha.
- CLI operacional inicial com comandos `status`, `missions`, `batch-summary`, `validate`, `doctor`, `docs-links` e `alpha-readiness`.
- Runner seguro individual e runner seguro em batch documentados como fluxo operacional local.

O projeto validou batch de 3 como fluxo de teste, retomada, bloco pequeno e recuperação. O projeto também executou batch de 10 como fluxo funcional histórico para blocos normais revisados e seguros, com ressalva operacional: limites externos de API, quota, rate limit ou billing podem interromper o batch e exigem parada segura antes de retomada. A recomendação operacional atual passa a ser batch normal de até 8 missões, blocos de 2 a 4 para missões estruturais ou pesadas e 1 a 3 para recuperação.

## Cadeia De Execução Atual

Arquitetura desejada:

```text
Mission
↓
Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Agents
↓
Subagents
↓
Capabilities
↓
Policy Engine / Guardian Engine
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Providers / MCPs / APIs / Runtimes
```

Cadeia MVP atual integrada para Mission/Workflow/Task:

```text
Chamador Python
↓
MissionRunner
↓
MissionWorkflowProvider
↓
WorkflowEngine.execute_with_queue()
↓
TaskQueue + TaskScheduler
↓
RuntimeAdapter.execute_task() ou executor injetado
```

Ponte mínima validada para Agent/Capability/Skill/Tool/Provider Gateway em dry-run:

```text
TaskScheduler
↓
AgentTaskExecutor
↓
AgentOrchestrator
↓
CapabilityResolver
↓
ResolvedCapabilityExecutor
↓
SkillExecutor
↓
ToolExecutor
↓
ProviderGateway em dry-run
↓
RuntimeAdapter fake ou injetado
```

O runner shell e o batch operacional continuam usando o fluxo de arquivos de missão e OpenCode como runtime/laboratório. A integração Python acima é local, determinística e validada por testes. Ela executa capabilities resolvidas por Skill, Tool e Provider Gateway em dry-run antes do runtime quando configurada explicitamente.

A cadeia capabilities/skills/tools/provider existe como contratos MVP e participa do caminho 0106 em dry-run. Provider real, rede, banco, MCP, API externa e integração global de Policy/Context/Token/Model/Audit continuam fora do escopo atual.

Fluxo operacional atual:

```text
missions/queue
↓
prompt_composer
↓
scripts/vaf-run-next-safe.sh ou scripts/vaf-run-batch-safe.sh
↓
worker local
↓
pytest + python3 -m compileall src
↓
missions/done ou missions/failed
```

Batch é o padrão operacional quando o bloco estiver bem especificado, revisado e seguro. Execução individual permanece necessária para missões críticas, sensíveis, arquiteturais, incertas, investigativas, de recuperação ou de alto risco.

## Lacunas Importantes

O projeto ainda precisa alinhar ou implementar:

- Mission Orchestrator como camada distinta de Mission Runner.
- Integração orquestrada e obrigatória entre Policy Engine, Guardian Engine, Context Router, Model Selection e Audit/Event Log nos fluxos completos, além das pontes opcionais já existentes.
- Integração global de Policy Engine, Guardian Engine, Context Router, Token Budget, Model Selection e Audit/Event Log ao fluxo Capability -> Skill -> Tool -> Provider Gateway.
- Integração completa do Context Router ao fluxo de missão, agente, modelo e recuperação governada.
- RAG semântico.
- Embeddings.
- Semantic Index com embeddings.
- Adapter PostgreSQL/pgvector para Knowledge Hub e Code Intelligence.
- Paridade de Runtime Adapter para Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.
- Persistência formal de Model Registry.
- Retenção, rotação e persistência externa de audit logs além da persistência local JSONL opt-in inicial.
- Provider real integrado como caminho obrigatório.
- Billing real.
- Observabilidade externa.
- Licença final publicada em `LICENSE`.
- Processo público maduro de segurança, incluindo canal definitivo de reporte de vulnerabilidades.
- Canal público definitivo para problemas de conduta e política de governança comunitária madura.
- Publicação de release alfa; o checklist de prontidão, o checklist de instalação limpa, a validação limpa reprovada e a versão planejada existem, mas não criam tag, pacote ou marco público por si só.
- Política pública madura de segurança. O CI público mínimo existe, mas ainda não há matriz de múltiplas versões, lint, validação limpa automatizada ou changelog de release versionado.
- Testes de contrato entre portas/adapters.
- ADRs para fronteiras ainda ambíguas.

## Risco De Continuar Sem Alinhamento

Continuar implementação sem alinhamento pode:

- transformar OpenCode no core acidental;
- permitir agentes chamando providers, MCPs, tools ou bancos diretamente;
- duplicar lógica de política em Guardian, runtime, CLI, tools e providers;
- misturar responsabilidades de Mission Runner, Mission Orchestrator, Workflow Engine e Task Queue;
- fundir memória, Knowledge Hub, índices semânticos e context routing em um subsistema sem fronteira;
- hardcodar PostgreSQL, Ollama, pgvector, ARM64 ou provider específico;
- adicionar LangGraph, MetaGPT, AutoGen ou MCPs como dependências centrais;
- perder rastreabilidade de Spec para Plan, Tasks, implementação, validação e commit;
- aumentar custo de tokens por carregamento amplo e repetido de contexto;
- criar lacunas de segurança em segredos, tools, providers externos e permissões de runtime.

## Estado De Versionamento E Release

A versão alfa inicial planejada é `0.1.0-alpha.1`, com tag futura planejada `v0.1.0-alpha.1`.

Esse estado é apenas documental:

- não há release alfa publicada;
- não há tag Git criada para alfa;
- não há GitHub Release publicada;
- não há pacote PyPI publicado;
- há apenas empacotamento local mínimo para instalação editável em ambiente de desenvolvimento;
- há CI mínimo com GitHub Actions para `pytest`, `python -m vercosa_ai_framework.cli.main docs-links`, diagnóstico não bloqueante `alpha-readiness` e `python -m compileall src`, sem publicação de pacote ou release;
- há política inicial de release e checklist pré-tag documentados;
- há release notes alfa preliminares, ainda pendentes de revisão final antes de publicação real;
- há diagnóstico local de prontidão alfa registrado com classificação `NÃO PRONTO`;
- há execução local do checklist pré-tag alfa registrada com classificação `REPROVADO`;
- há consolidação local do candidato alfa registrada como preparação, sem publicação;
- há solicitação futura de decisão de tag registrada, sem autorização automática;
- não há garantia de estabilidade de produção;
- não há promessa de compatibilidade de API.

Antes de qualquer publicação, ainda são necessárias correção ou decisão explícita sobre os bloqueios da validação limpa reprovada, resolução dos bloqueios do diagnóstico local de prontidão alfa, resolução dos bloqueios da execução local do checklist pré-tag, reexecução do checklist de instalação limpa, nova execução pré-tag quando houver candidato apto, testes, `compileall`, revisão do changelog, confirmação de CI remoto após push, decisão explícita de tag/release e resolução das pendências aplicáveis de licença e distribuição.

O candidato alfa local foi consolidado, mas a tag não foi criada, a release não foi publicada e nenhum pacote foi publicado. A próxima etapa depende de validação final pós-batch, push manual quando autorizado, confirmação do CI remoto e autorização explícita para uma missão futura de tag.

## Execução Local Do Checklist Pré-Tag Alfa

O checklist pré-tag local foi executado em 2026-07-11 no commit `45a8274339fa6fa31e49f1cb54c131450e8155c7` e registrado em [docs/release/pre-tag-checklist-execution.md](../release/pre-tag-checklist-execution.md).

Classificação real: `REPROVADO`.

Bloqueios principais registrados:

- `LICENSE` ausente.
- `missions/running` continha 1 missão.
- `alpha-readiness` retornou `NÃO PRONTO`.
- `validate` e `doctor` falharam pela forma local documentada com `PYTHONPATH=src` por `running > 0`.
- Git estava sujo durante a execução local.
- CI remoto permanece pendente de confirmação após push.

Resultados positivos registrados:

- `pytest` passou com `444` testes.
- `python3 -m compileall src` passou.
- `docs-links` passou pela forma local documentada com `PYTHONPATH=src`.

Esse checklist não declara release publicada, não cria tag, não publica release e não publica pacote.

## Diagnóstico Local De Prontidão Alfa

O diagnóstico local de prontidão alfa foi executado em 2026-07-11 no commit `7552ba140b5bd42db072a586cb49008ed02a64e1` e registrado em [docs/release/alpha-readiness-diagnostic.md](../release/alpha-readiness-diagnostic.md).

Classificação real: `NÃO PRONTO`.

Bloqueios principais registrados:

- `LICENSE` ausente.
- `missions/running` continha 1 missão.
- Git estava sujo durante o diagnóstico.
- A forma literal `python3 -m vercosa_ai_framework.cli.main ...` falhou sem instalação editável ou `PYTHONPATH=src`.
- A validação de instalação limpa anterior continuava `REPROVADO`.

Resultados positivos registrados:

- `pytest` passou com `444` testes.
- `python3 -m compileall src` passou.
- `docs-links` passou pela forma local documentada com `PYTHONPATH=src`.

Esse diagnóstico não declara release publicada, não cria tag e não publica pacote.

## Validação De Instalação Limpa

A validação de instalação limpa foi executada em 2026-07-10 no commit `365ea328399495434d3727fcf212f8aaf4ae25f4`, em cópia temporária local criada com `mktemp -d` e clone local com `git clone --no-hardlinks`, sem rede e sem publicar artefatos.

Classificação real: `REPROVADO`.

Limitações relevantes encontradas:

- instalação editável offline falhou por ausência local de `hatchling>=1.25` no commit validado; depois disso, o empacotamento local foi ajustado para `setuptools`, mas a validação limpa ainda precisa ser reexecutada;
- CLI `validate` e `doctor` falharam porque `missions/running` e `missions/failed` não existem no clone limpo;
- `scripts/vaf-status.sh` usa caminho absoluto para o checkout principal e não valida corretamente uma cópia temporária;
- `pytest` passou como evidência complementar, mas não comprova instalação de desenvolvimento isolada porque a instalação editável falhou;
- `compileall` passou;
- `LICENSE` continua pendente; o metadado de licença não deve inventar licença final antes de decisão explícita.

Esse resultado reduz a prontidão da alfa: o projeto ainda não deve criar tag, release ou pacote até nova validação aprovada ou decisão explícita de exceção com risco aceito.

## Recomendação De Alinhamento

Antes de novas implementações, congelar vocabulário arquitetural e escolher o próximo bloco deliberadamente.

Foco imediato recomendado:

- manter alterações de código bloqueadas sem Spec aprovada específica;
- integrar Policy Engine e Guardian Engine sem fundir resolução declarativa e enforcement operacional;
- definir Context Router e Semantic Index antes de implementar memória avançada;
- definir fronteiras de Mission Orchestrator antes de expandir Mission Runner;
- integrar MVPs existentes por contratos antes de adicionar frameworks externos;
- escrever ADRs para posicionamento de frameworks externos e arquitetura de memória quando necessário.

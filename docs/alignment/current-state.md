# Estado Atual

## Objetivo

Registrar o estado arquitetural do Vercosa AI Framework antes da próxima onda de implementação.

Este checkpoint é apenas documental. Ele não aprova novo código, novo comportamento de runtime, alterações de configuração global, operações privilegiadas ou expansão de funcionalidades.

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

## Estado Do Repositório

O repositório está em fase de fundação/MVP.

Ativos principais:

- `AGENTS.md`: contexto operacional central e regras arquiteturais para agentes.
- `README.md`: resumo público do projeto, identidade de Harness Engineering e limites do MVP atual.
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
- `cli/`: CLI operacional inicial para status local básico, validação estrutural local, versão e diagnóstico simples; ela não substitui scripts shell nem executa missões nesta fase.
- `missions/`: tipos, fila em diretório e runner de missões.
- `workflows/`: tipos e engine sequencial de workflow.
- `tasks/`: tipos, fila, scheduler, tentativas e transições de estado.
- `policy/`: contratos e resolução determinística MVP de políticas declarativas, precedência simples e conflitos básicos.
- `guardian/`: Guardian Engine determinístico com decisões estruturadas e detecção inicial de sinais textuais de limite de uso/API sem chamadas externas.
- `audit/`: contratos iniciais de Audit/Event Log, tipos de evento, implementação em memória, helpers opcionais para decisões centrais e eventos básicos de ciclo de vida de missão.
- `model_selection/`: políticas, tipos e selector MVP.
- `runtime/`: contrato de Runtime Adapter e OpenCode Runtime Adapter MVP.
- `agents/`: perfis, registry e orchestrator MVP.
- `capabilities/`: perfis, registry e resolver.
- `skills/`: perfis, registry e executor.
- `tools/`: perfis, registry e executor.
- `providers/`: perfis, registry, contrato de adapter e gateway.
- `knowledge/`: ingestão Markdown, documentos, store em memória e busca textual.
- `canonicalizer/`: canonicalização, hashes, warnings e conversão para Knowledge Hub.
- `persistence/`: tipos, contrato de repository e filesystem repository local.
- runners seguros: scripts operacionais para execução segura de uma missão e execução segura em batch, com validações locais. Batch é o fluxo operacional padrão para blocos revisados e seguros; execução individual continua válida para risco alto, investigação e recuperação.

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

Cadeia MVP atual:

```text
CLI, scripts shell or Python caller
↓
Mission Runner or Workflow Engine
↓
Guardian Engine
↓
Runtime Adapter
↓
OpenCode adapter in dry-run or controlled execution mode
```

A cadeia capabilities/skills/tools/provider existe como contratos MVP, mas ainda não está integrada de ponta a ponta no loop missão-agente.

## Lacunas Importantes

O projeto ainda precisa alinhar ou implementar:

- Mission Orchestrator como camada distinta de Mission Runner.
- Integração profunda entre Policy Engine e Guardian Engine após os contratos iniciais do Policy Engine.
- Fluxo ponta a ponta Mission -> Workflow -> Task Queue -> Agent Orchestrator -> Capability -> Skill -> Tool -> Provider.
- Integração completa do Context Router ao fluxo de missão, agente, modelo e recuperação governada.
- Semantic Index com embeddings.
- Adapter PostgreSQL/pgvector para Knowledge Hub e Code Intelligence.
- Paridade de Runtime Adapter para Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.
- Persistência formal de Model Registry.
- Persistência e retenção de audit logs além da implementação em memória inicial.
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

## Recomendação De Alinhamento

Antes de novas implementações, congelar vocabulário arquitetural e escolher o próximo bloco deliberadamente.

Foco imediato recomendado:

- manter alterações de código bloqueadas sem Spec aprovada específica;
- integrar Policy Engine e Guardian Engine sem fundir resolução declarativa e enforcement operacional;
- definir Context Router e Semantic Index antes de implementar memória avançada;
- definir fronteiras de Mission Orchestrator antes de expandir Mission Runner;
- integrar MVPs existentes por contratos antes de adicionar frameworks externos;
- escrever ADRs para posicionamento de frameworks externos e arquitetura de memória quando necessário.

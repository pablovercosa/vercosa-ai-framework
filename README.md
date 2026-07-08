# Vercosa AI Framework

Open source framework para desenvolvimento de software orientado por especificações e assistido por IA.

## Objetivo

O Vercosa AI Framework organiza engenharia de software em torno de Specs, missões, workflows, tarefas, agentes, capabilities, skills, tools, policies, Knowledge Hub, validação, auditoria e adapters substituíveis.

## O Que O Framework É

- Um framework Specification First para desenvolvimento assistido por IA.
- Uma arquitetura AI Native com governança, rastreabilidade e validação explícitas.
- Um núcleo provider agnostic para modelos, runtimes, bancos, vetores, IDEs, MCPs e APIs.
- Um conjunto de contratos e MVPs iniciais em Python para missão, workflow, task queue, agentes, Policy Engine, Guardian, detecção determinística de limites de uso/API, Audit/Event Log em memória com eventos opcionais de missão, runtime, knowledge, context routing, token budget, canonicalização, providers e persistência.

## O Que O Framework Não É

- Não é um IDE.
- Não é um MCP server.
- Não é um único agente.
- Não é um wrapper de OpenCode, Claude Code, Codex CLI ou Cursor.
- Não é dependente de PostgreSQL, pgvector, Ollama, ARM64, systemd ou SSH.
- Não é uma coleção de prompts sem Specs, validação e governança.

## Estado Atual

Status: fundação arquitetural com MVPs e contratos iniciais.

As Specs em `specs/framework/` descrevem a arquitetura desejada. O código em `src/vercosa_ai_framework/` implementa partes mínimas e ainda não representa o fluxo completo de ponta a ponta.

## Runtime Inicial

OpenCode é o runtime e laboratório inicial. Ele deve permanecer atrás de adapter em `runtime/` e não define o núcleo do framework.

## Worker Local

Os scripts em `scripts/` permitem processar missões locais em fila usando OpenCode no ambiente atual.

A CLI Python inicial em `src/vercosa_ai_framework/cli/` é uma camada de conveniência para leitura, diagnóstico básico e validação estrutural local com `validate`. Ela não substitui `scripts/vaf-status.sh`, `pytest` ou `python3 -m compileall src`, não executa missões nesta fase e não altera o fluxo `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.

Variáveis relevantes:

- `VAF_AUTO_COMMIT`: quando definido como `1`, o runner cria commit automático ao concluir uma missão com alterações staged.
- `VAF_COMMIT_MESSAGE`: quando definida e não vazia, substitui a mensagem automática do commit.
- Com `VAF_AUTO_COMMIT=1` e sem `VAF_COMMIT_MESSAGE`, a mensagem padrão é `missão: nome-da-missao`.

Exemplo:

```bash
VAF_AUTO_COMMIT=1 VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-worker.sh
```

### Runner Seguro De Próxima Missão

O script `scripts/vaf-run-next-safe.sh` executa a próxima missão da fila com validações locais antes e depois do worker. Ele aborta se o Git não estiver limpo antes de iniciar, verifica se não há worker em execução, roda apenas uma missão por padrão, executa `pytest`, executa `python3 -m compileall src` e só permite push automático quando solicitado explicitamente.

Guia operacional: [Uso do runner seguro](docs/operations/safe-runner-usage.md).

Uso básico:

```bash
./scripts/vaf-run-next-safe.sh
```

Uso com push automático opcional:

```bash
VAF_AUTO_PUSH=1 ./scripts/vaf-run-next-safe.sh
```

Uso com mensagem de commit customizada:

```bash
VAF_COMMIT_MESSAGE="implementação: exemplo" ./scripts/vaf-run-next-safe.sh
```

Por padrão, o runner define `VAF_MAX_CYCLES=1`, `VAF_AUTO_APPROVE=1` e `VAF_AUTO_COMMIT=1`. O push automático nunca é padrão; quando `VAF_AUTO_PUSH=1`, o script exige branch `main`, Git limpo, testes aprovados, `compileall` aprovado, worker parado, nenhuma missão em `missions/failed` e remoto `origin` configurado.

### Runner Seguro Em Batch

O script `scripts/vaf-run-batch-safe.sh` executa múltiplas missões em sequência controlada usando o runner seguro de próxima missão. O padrão é `VAF_BATCH_SIZE=3`; o limite máximo seguro inicial é `VAF_BATCH_SIZE=10`.

Uso básico:

```bash
./scripts/vaf-run-batch-safe.sh
```

Uso com tamanho explícito:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
```

O batch para na primeira falha, valida `pytest` e `python3 -m compileall src` por missão por reaproveitamento do runner seguro, exige Git limpo após cada missão e preserva commits separados por missão. Push automático é opt-in com `VAF_AUTO_PUSH=1` e ocorre somente ao final do batch se todas as missões executadas passarem.

Playbook operacional: [Execução em batch](docs/operations/batch-execution-playbook.md). Checklist pós-batch: [Validação pós-batch](docs/operations/post-batch-validation-checklist.md).

## Princípios

- Specification First
- AI Native
- Provider Agnostic
- Local First
- Extensible by Design
- Security by Design
- Token Efficiency
- Governance by Design

## Arquitetura Resumida

```text
Mission
↓
Mission Runner / Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Agents / Subagents
↓
Capabilities
↓
Policy / Guardian
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Providers / MCPs / APIs / Runtimes
```

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
- [skills](src/vercosa_ai_framework/skills/README.md)
- [tools](src/vercosa_ai_framework/tools/README.md)
- [providers](src/vercosa_ai_framework/providers/README.md)
- [runtime](src/vercosa_ai_framework/runtime/README.md)
- [model_selection](src/vercosa_ai_framework/model_selection/README.md)
- [context](src/vercosa_ai_framework/context/README.md)
- [knowledge](src/vercosa_ai_framework/knowledge/README.md)
- [canonicalizer](src/vercosa_ai_framework/canonicalizer/README.md)
- [persistence](src/vercosa_ai_framework/persistence/README.md)

## Estrutura Do Repositório

- `AGENTS.md`: contexto central para agentes e regras de colaboração.
- `specs/framework/`: Specs do framework.
- `docs/`: documentação técnica, alinhamento, arquitetura e guias.
- `docs/documentation/readme-standard.md`: padrão oficial de README.
- `docs/templates/readme-template.md`: template para novos READMEs.
- `src/vercosa_ai_framework/`: contratos e MVPs do framework.
- `knowledge/`: visão, princípios e arquitetura de referência.
- `.opencode/`: integração inicial com OpenCode.

## Idioma E Commits

O idioma oficial da documentação do projeto é português do Brasil. Termos técnicos e nomes arquiteturais consolidados podem permanecer em inglês quando fizerem parte da API, arquitetura ou vocabulário do framework.

Mensagens de commit futuras devem usar português do Brasil. O histórico Git já publicado não deve ser reescrito apenas para traduzir mensagens antigas.

Políticas detalhadas:

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

## Documentação Técnica

- [Mapa de arquitetura](docs/alignment/architecture-map.md)
- [Estado atual](docs/alignment/current-state.md)
- [Perguntas em aberto](docs/alignment/open-questions.md)
- [SDD Lifecycle](docs/alignment/sdd-lifecycle.md)
- [Roadmap](docs/alignment/roadmap.md)
- [Backlog estratégico de missões](docs/roadmap/mission-backlog.md)
- [Padrão de README](docs/documentation/readme-standard.md)
- [Padrão de idioma e commits](docs/documentation/language-and-commit-standard.md)
- [Política de atualização de documentação](docs/documentation/documentation-update-policy.md)
- [Uso do runner seguro](docs/operations/safe-runner-usage.md)
- [Playbook de execução em batch](docs/operations/batch-execution-playbook.md)
- [Checklist de validação pós-batch](docs/operations/post-batch-validation-checklist.md)
- [CLI operacional inicial](docs/cli.md)
- [Context Router e Token Budget](docs/context-router-token-budget.md)

## Regras De Trabalho

- Nenhum código deve ser implementado sem Spec aprovada.
- Documentação deve refletir o estado real do código e das Specs.
- Toda missão que criar, alterar ou expandir funcionalidade deve revisar e atualizar READMEs, docs, Specs e ADRs relacionados quando necessário.
- Mensagens de commit futuras devem usar português do Brasil.
- Mudanças arquiteturais materiais devem gerar ADR, Spec update ou pergunta registrada.
- Agentes não devem chamar providers, MCPs, APIs, bancos ou filesystem diretamente.
- Links de documentação devem ser relativos.

## Integração Policy E Guardian

O Policy Engine e o Guardian Engine permanecem separados. O Policy Engine resolve políticas declarativas em `ResolvedPolicySet`; o Guardian Engine avalia ações concretas e pode considerar esse conjunto opcional para elevar decisões operacionais como `warn`, `require_approval` ou `block`.

Essa integração é inicial, determinística e sem chamadas externas. Ela não implementa DSL, parser de políticas, carregamento remoto, RAG, embeddings, banco ou provider.

O Guardian também possui um `Usage/API Limit Guard` inicial para classificar sinais textuais de rate limit, quota, limite de uso e billing em erros/logs já recebidos de providers ou runtimes. Esse guard é determinístico, não consulta billing real, não chama providers externos e diferencia limitações externas temporárias de bugs do framework.

## Integração Policy E Context Router

O Context Router pode receber `ResolvedPolicySet` opcional já produzido pelo Policy Engine em `ContextRequest`. Ele apenas consome políticas resolvidas para registrar refs, gerar warnings, marcar aprovação requerida em metadados e omitir itens quando houver `deny` determinístico com alvo claro.

Essa integração é inicial, determinística e sem chamadas externas. Ela não implementa DSL, parser de políticas, RAG semântico, embeddings, pgvector, banco, provider externo ou chamada de LLM.

## Integração Policy E Model Selection

O Model Selection Engine pode receber `ResolvedPolicySet` opcional já produzido pelo Policy Engine. Ele apenas consome políticas resolvidas para registrar fontes, gerar notas, marcar revisão ou aprovação requerida e excluir candidatos quando houver `deny` determinístico com alvo claro.

Essa integração é inicial, determinística e sem chamadas externas. Ela não implementa precificação real, consulta de billing real, consulta de limites reais de API, roteamento avançado, ranking semântico, RAG, embeddings, banco, provider externo ou chamada de LLM.

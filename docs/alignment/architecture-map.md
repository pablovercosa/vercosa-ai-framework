# Mapa De Arquitetura

Links principais: [README principal](../../README.md) | [Índice de módulos](../architecture/module-index.md) | [Revisão pós-integrações](../architecture/post-integration-architecture-review.md) | [Estado atual](current-state.md) | [Roadmap](roadmap.md)

## Espinha Arquitetural

A arquitetura do framework é orientada por missões e governada por especificações.

Cadeia canônica:

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

Regra principal: camadas superiores expressam intenção; camadas inferiores fornecem mecanismos de execução substituíveis. A revisão consolidada após as integrações até a missão 0080 está em [Revisão arquitetural pós-integrações](../architecture/post-integration-architecture-review.md).

## Mapa De Camadas

| Camada | Objetivo | Estado atual | Não deve fazer |
| --- | --- | --- | --- |
| Mission | Intenção do usuário/sistema e entregáveis exigidos | Representada por `missions/types.py` e arquivos de fila | Codificar comandos específicos de runtime como arquitetura |
| Mission Runner | Ciclo operacional, fila, ciclos, validação e estado final | MVP em `missions/runner.py` e `missions/queue.py`, com ponte opcional para Workflow/Task por contratos injetáveis | Substituir Mission Orchestrator ou Workflow Engine permanentemente |
| Mission Orchestrator | Decidir qual workflow satisfaz uma missão | Conceitual, ainda sem módulo distinto claro | Virar runtime adapter ou comando CLI |
| Workflow Engine | Construir/executar plano de workflow e ordem de tasks | MVP sequencial em `workflows/engine.py`, com `execute_with_queue()` para Task Queue | Controlar ciclo de missão, registry de agentes ou execução de providers |
| Task Queue | Gerenciar estados, dependências, tentativas e retries | MVP em `tasks/`, usado como substrato operacional no fluxo integrado Mission/Workflow/Task | Executar providers concretos ou escolher agentes por conta própria |
| Agent Orchestrator | Selecionar perfil de agente, resolver capabilities declarativas e preparar execução | MVP em `agents/`, integrado ao Capability Resolver e a executor de capability injetável quando configurado | Chamar OpenCode, MCPs, APIs, bancos ou tools diretamente |
| Agents/Subagents | Executar responsabilidades por fronteiras do framework | Conceitual/MVP no nível de perfil | Conhecer providers ou infraestrutura concreta |
| Capabilities | Representar capacidades abstratas solicitadas | MVP em `capabilities/`, com resolver e executor de capability resolvida em dry-run governado | Codificar detalhes concretos de tool/provider |
| Policy/Guardian | Resolver políticas declarativas e aplicar enforcement operacional em ações concretas | Policy Engine MVP resolve políticas declarativas; Guardian MVP avalia ações e riscos; pontes opcionais já alcançam Context Router, Model Selection e Audit/Event Log por resultados explícitos | Executar comandos ou mutar estado diretamente |
| Audit/Event Log | Representar eventos internos auditáveis e rastreáveis | Contratos iniciais, implementação em memória, persistência local JSONL opt-in, helpers opcionais para decisões centrais e eventos de missão/batch; arquitetura dedicada em [Audit/Event Log](../architecture/audit-event-architecture.md) | Persistir globalmente por padrão, exportar observabilidade externa ou chamar módulos consumidores automaticamente |
| Skills | Procedimentos reutilizáveis que implementam capabilities | MVP em `skills/` | Contornar tools ou Provider Gateway para efeitos |
| Tools | Fronteira governada de ação concreta | MVP em `tools/` | Ocultar chamadas diretas a providers da governança |
| Provider Gateway | Normalizar acesso a providers após aprovação por tool | MVP em `providers/` | Virar seletor de modelo, runtime adapter ou camada de agente |
| Providers/MCPs/APIs/Runtimes | Mecanismos externos concretos | OpenCode runtime MVP; providers são contratos injetáveis | Vazar para o core ou abstrações de agentes |

## Fluxo Implementado Versus Futuro

Fluxo operacional implementado atualmente:

```text
CLI, scripts shell ou chamador Python
↓
Mission Runner, Workflow Engine ou runner operacional
↓
Guardian Engine quando configurado
↓
Runtime Adapter injetado
↓
OpenCode adapter inicial ou fake adapter em testes
↓
validações locais, status de missão e documentação de evidências
```

Fluxo transversal implementado como integração inicial por chamada explícita:

```text
Policy Engine
↓
ResolvedPolicySet
↓
Guardian Engine / Context Router / Model Selection Engine
↓
GuardianDecision / ContextPackage / SelectionDecision
↓
Audit/Event Log opcional quando EventLog é fornecido
```

Fluxo mínimo integrado por chamada explícita:

```text
MissionRunner
↓
MissionWorkflowProvider
↓
WorkflowEngine.execute_with_queue()
↓
TaskQueue
↓
TaskScheduler
↓
RuntimeAdapter.execute_task()
↓
WorkflowResult
↓
MissionResult
```

Esse fluxo foi validado localmente. Quando recebe `AgentTaskExecutor`, pode acionar o caminho mínimo Agent Orchestrator -> Capability Resolver antes do runtime.

Fluxo mínimo Task/Agent/Capability/Skill/Tool/Provider Gateway em dry-run validado:

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
↓
TaskExecutionOutcome
```

Esse fluxo executa SkillExecutor, ToolExecutor e Provider Gateway em `dry_run=True`. Ele não chama provider real, adapter concreto, MCP, API externa, rede, banco ou subprocesso.

Fluxo futuro ainda não integrado globalmente:

```text
Mission Runner
↓
Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Capability Resolver
↓
SkillExecutor
↓
ToolExecutor
↓
Provider Gateway
↓
ProviderAdapter / RuntimeAdapter / MCP adapter governado
↓
Audit/Event Log persistível e documentação de evidências
```

O fluxo futuro acima não deve ser tratado como implementado com provider real. Ele orienta fronteiras e próximas decisões para Policy/Context/Token/Model/Audit, adapters reais e auditoria persistível.

## Mapa De Módulos Fonte

- `src/vercosa_ai_framework/core/`: modelos de domínio compartilhados e primitivas de política.
- `src/vercosa_ai_framework/cli/`: interface CLI operacional inicial para leitura, listagem de missões e validação estrutural local; não é o núcleo de orquestração e não substitui os scripts shell.
- `src/vercosa_ai_framework/missions/`: registros, fila e runner de missão.
- `src/vercosa_ai_framework/workflows/`: workflow e execução sequencial de tasks.
- `src/vercosa_ai_framework/tasks/`: fila, scheduler, estado, elegibilidade e tentativas de tasks.
- `src/vercosa_ai_framework/policy/`: contratos e resolução determinística MVP de políticas declarativas.
- `src/vercosa_ai_framework/guardian/`: Guardian Engine MVP para decisões de política, risco e classificação determinística de sinais textuais de limite de uso/API.
- `src/vercosa_ai_framework/audit/`: contratos iniciais de Audit/Event Log, implementação em memória e persistência local JSONL opt-in, sem persistência externa. Ver [arquitetura de Audit/Event Log](../architecture/audit-event-architecture.md).
- `src/vercosa_ai_framework/model_selection/`: contratos e seleção de modelos por política.
- `src/vercosa_ai_framework/runtime/`: fronteira de Runtime Adapter, incluindo OpenCode como MVP inicial.
- `src/vercosa_ai_framework/agents/`: perfis de agentes, registry e orchestrator MVP.
- `src/vercosa_ai_framework/capabilities/`: registry e resolver de capabilities.
- `src/vercosa_ai_framework/skills/`: registry e executor de skills.
- `src/vercosa_ai_framework/tools/`: registry e executor governado de tools.
- `src/vercosa_ai_framework/providers/`: registry, contrato de adapter e Provider Gateway.
- `src/vercosa_ai_framework/knowledge/`: documentos, ingestão Markdown, store em memória e busca textual.
- `src/vercosa_ai_framework/canonicalizer/`: contratos e MVP de canonicalização de texto/Markdown.
- `src/vercosa_ai_framework/persistence/`: contratos de persistência e repository filesystem MVP.

## Caminhos De Integração Atuais

Caminho de Mission Runner:

```text
Mission file or queued Mission
↓
DirectoryMissionQueue
↓
MissionRunner
↓
GuardianEngine
↓
RuntimeAdapter
↓
OpenCodeRuntimeAdapter or injected fake adapter
↓
MissionResult
```

Caminho integrado Mission/Workflow/Task:

```text
MissionRunner
↓
MissionWorkflowProvider
↓
QueueBackedWorkflowExecutor
↓
WorkflowEngine.execute_with_queue()
↓
TaskQueue + TaskScheduler
↓
RuntimeAdapter.execute_task() por executor injetado
↓
WorkflowResult
↓
MissionResult
```

Caminho legado de Workflow:

```text
Workflow
↓
WorkflowEngine.execute()
↓
GuardianEngine por task
↓
RuntimeAdapter.execute_task()
↓
WorkflowResult
```

Caminho de Capability:

```text
CapabilityRequest
↓
CapabilityResolver
↓
SkillProfile declarativa
```

O caminho `SkillExecutor -> ToolExecutor -> ProviderGateway` existe como contratos/MVPs, mas não faz parte da integração 0105.

Caminho de Policy, Context, Model Selection, Guardian e Audit:

```text
PolicySet explícito
↓
Policy Engine
↓
ResolvedPolicySet
↓
Context Router / Token Budget Manager / Model Selection
↓
ContextPackage e ModelSelectionDecision
↓
Guardian Engine quando chamado explicitamente
↓
Audit/Event Log opcional quando EventLog é fornecido
```

Esse caminho representa integrações iniciais por estruturas explícitas. Ele não significa chamada automática de provider, billing real, RAG semântico, persistência externa de eventos ou observabilidade externa.

Relações atuais do Audit/Event Log:

- Policy Engine pode ter `PolicyResolutionResult` transformado em evento `policy.resolution` por helper opcional.
- Guardian Engine pode ter `GuardianDecision` transformada em evento `guardian.decision` por helper opcional.
- Context Router pode ter `ContextPackage` transformado em evento `context.package` por helper opcional.
- Mission Runner Python pode registrar eventos de missão quando recebe `EventLog` opcional.
- `JsonlAuditEventLog` pode persistir eventos em arquivo JSONL local quando fornecido explicitamente pelo chamador.
- Model Selection possui categoria reservada no contrato, mas emissão estruturada específica ainda é futura.
- Usage/API Limit Guard possui categoria reservada no contrato; no estado atual, a integração operacional usa classificação de logs textuais já existentes.

Relações atuais da CLI operacional:

- `status` lê contagens locais de `missions/queue`, `missions/running`, `missions/done` e `missions/failed`.
- `missions` lista nomes de arquivos `.md` por estado, com contagens gerais e filtro opcional.
- `validate` faz validação estrutural local mínima.
- `doctor` combina validação estrutural e diagnóstico local amigável.
- A CLI não executa missões, scripts shell, Git, testes, providers, banco, rede, OpenCode ou MCPs nesta fase.

## Pontes Ausentes

- Mission Orchestrator para Workflow Engine.
- Catálogo aprovado de Agent Profiles, Capabilities e Skills para uso real além dos testes.
- Caminho Capability/Skill/Tool para Provider Gateway como fluxo padrão de efeitos.
- Recuperação do Knowledge Hub para Context Router.
- Context Router para Mission Runner, Workflow Engine e Agent Orchestrator como parte do fluxo padrão.
- Persistence Layer para missões, workflows, tasks, decisões Guardian, decisões de modelo e documentos.
- Persistência externa, retenção, rotação e integração automática de eventos auditáveis aos fluxos operacionais.
- CLI para resumo pós-batch como comando próprio de leitura segura.

## Decisões De Fronteira Necessárias

- Policy Engine versus Guardian Engine: ADR aceita define camadas separadas; ainda falta integração profunda entre resolução declarativa e enforcement operacional.
- Mission Runner versus Mission Orchestrator: separar estado operacional de escolha de workflow e estratégia de orquestração.
- Workflow Engine versus Task Queue: separar semântica de workflow do estado, elegibilidade e tentativas de tasks.
- Runtime Adapter versus Provider Gateway: separar execução de sessões de runtime de acesso normalizado a providers atrás de tools.
- Knowledge Hub versus Context Router: separar armazenamento/recuperação de conhecimento da decisão do que entra no contexto.
- Semantic Index versus memória persistente: separar infraestrutura de recuperação semântica de registros duráveis.

## Guardrails Arquiteturais

- Agentes solicitam capabilities; não chamam MCPs, providers, APIs, bancos ou shell diretamente.
- Skills usam tools; tools usam adapters de providers/MCPs/APIs.
- OpenCode, Claude Code, Codex CLI, Cursor, IDEs, Web UI e API são runtime/interface adapters.
- LangGraph, MetaGPT e AutoGen podem ser adapters opcionais ou referências, não dependências centrais.
- PostgreSQL, pgvector, Ollama e tree-sitter são adapters local-first válidos, não premissas obrigatórias.
- Todo loop precisa de condição de parada.
- Toda implementação precisa de Spec aprovada.
- Todo efeito externo material precisa de avaliação Guardian/policy.
- Toda mudança material de fronteira arquitetural deve gerar atualização de Spec ou ADR.

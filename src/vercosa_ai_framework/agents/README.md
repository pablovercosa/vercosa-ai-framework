# Módulo agents

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0008](../../../specs/framework/0008-agent-orchestrator.md)

## Objetivo

Selecionar perfis de agentes e preparar execuções de agente sem acoplar agentes a providers, MCPs, tools ou runtime concreto.

## O Que Este Módulo Faz

- Define perfis, roles, modos, estados e resultados de agentes.
- Mantém registry de perfis de agentes.
- Seleciona agente compatível com role, capabilities e metadados.
- Resolve capabilities obrigatórias de forma declarativa quando o `CapabilityResolver` é configurado explicitamente.
- Executa capabilities obrigatórias por contrato injetável de alto nível quando `capability_executor` e `require_capability_execution=True` são configurados.
- Fornece `AgentTaskExecutor` como ponte para o executor injetado do `TaskScheduler`.
- Prepara requisição normalizada para RuntimeAdapter.

## O Que Este Módulo Não Faz

- Não executa tools, MCPs, APIs, bancos ou providers diretamente.
- Não implementa o loop final de agente como máquina de estados completa.
- Não importa nem constrói ToolExecutor, ProviderGateway, adapters concretos, MCPs, APIs ou clientes de rede.
- Não escolhe modelos sem Model Selection Engine.
- Não altera tasks ou workflows diretamente.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de agentes, perfis, requests e resultados. |
| `registry.py` | `AgentRegistry` para perfis. |
| `orchestrator.py` | `AgentOrchestrator` MVP. |
| `task_executor.py` | Ponte `TaskScheduler` -> `AgentOrchestrator`. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `AgentRole`: papéis de agente.
- `AgentMode`: modo operacional.
- `AgentState`: estados conceituais de agente.
- `AgentProfile`: perfil selecionável.
- `AgentCapabilityRequest`: capabilities solicitadas pelo agente.
- `AgentExecutionRequest`: pedido de execução.
- `AgentExecutionResult`: resultado normalizado.
- `AgentRegistry`: catálogo de perfis.
- `AgentOrchestrator`: seleção e preparação de execução.
- `AgentTaskExecutor`: executor injetável para o scheduler de tasks.

## Entradas E Saídas

Entradas:

- Pedido de execução com role, capabilities, contexto e limites.
- Perfis registrados em `AgentRegistry`.

Saídas:

- `AgentExecutionResult` e requisições normalizadas para runtime.

## Dependências Internas

- `../runtime/`: execução concreta por adapter.
- `../guardian/`: avaliação quando configurada.
- `../capabilities/`: resolução declarativa e execução opcional por contrato injetável de capabilities obrigatórias.

## Módulos Relacionados

- Acima: [tasks](../tasks/README.md).
- Abaixo: [capabilities](../capabilities/README.md).
- Transversal: [model_selection](../model_selection/README.md), [runtime](../runtime/README.md).

## Specs Correspondentes

- [Spec 0008: Agent Orchestrator](../../../specs/framework/0008-agent-orchestrator.md)
- [Spec 0009: Capabilities, Skills e Tools](../../../specs/framework/0009-capabilities-skills-tools.md)

## Docs Relacionadas

- [Agent Orchestrator](../../../docs/agent-orchestrator.md)
- [Integração Task, Agent e Capability](../../../docs/architecture/task-agent-capability-integration.md)
- [Capabilities, Skills, Tools](../../../docs/capabilities-skills-tools.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.agents import AgentProfile, AgentRegistry, AgentRole

registry = AgentRegistry()
registry.register(
    AgentProfile(
        role=AgentRole.DOCUMENTATION,
        domain="documentation",
        supported_task_types=("docs",),
        supported_capabilities=("write_docs",),
    )
)
```

## Status Atual

Status: `MVP`.

Há registry, orchestrator mínimo, ponte para Task Scheduler, resolução declarativa de capabilities obrigatórias e execução opcional por `capability_executor` antes do runtime. O fluxo 0106 valida Capability -> Skill -> Tool -> Provider Gateway em dry-run, sem provider real, rede, banco, MCP ou API externa.

## Próximos Passos

- Revisar Specs/ADRs afetadas pela integração mínima e integrar Policy, Context, Token Budget, Model Selection e Audit/Event Log em missão futura.

# Módulo agents

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0008](../../../specs/framework/0008-agent-orchestrator.md)

## Objetivo

Selecionar perfis de agentes e preparar execuções de agente sem acoplar agentes a providers, MCPs, tools ou runtime concreto.

## O Que Este Módulo Faz

- Define perfis, roles, modos, estados e resultados de agentes.
- Mantém registry de perfis de agentes.
- Seleciona agente compatível com role, capabilities e metadados.
- Prepara requisição normalizada para RuntimeAdapter.

## O Que Este Módulo Não Faz

- Não executa tools, MCPs, APIs, bancos ou providers diretamente.
- Não implementa o loop final de agente como máquina de estados completa.
- Não resolve capabilities por conta própria.
- Não escolhe modelos sem Model Selection Engine.
- Não altera tasks ou workflows diretamente.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de agentes, perfis, requests e resultados. |
| `registry.py` | `AgentRegistry` para perfis. |
| `orchestrator.py` | `AgentOrchestrator` MVP. |
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

## Entradas E Saídas

Entradas:

- Pedido de execução com role, capabilities, contexto e limites.
- Perfis registrados em `AgentRegistry`.

Saídas:

- `AgentExecutionResult` e requisições normalizadas para runtime.

## Dependências Internas

- `../runtime/`: execução concreta por adapter.
- `../guardian/`: avaliação quando configurada.

## Módulos Relacionados

- Acima: [tasks](../tasks/README.md).
- Abaixo: [capabilities](../capabilities/README.md).
- Transversal: [model_selection](../model_selection/README.md), [runtime](../runtime/README.md).

## Specs Correspondentes

- [Spec 0008: Agent Orchestrator](../../../specs/framework/0008-agent-orchestrator.md)
- [Spec 0009: Capabilities, Skills e Tools](../../../specs/framework/0009-capabilities-skills-tools.md)

## Docs Relacionadas

- [Agent Orchestrator](../../../docs/agent-orchestrator.md)
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

Há registry e orchestrator mínimos, mas o fluxo Task Queue -> Agent -> Capability ainda não está integrado de ponta a ponta.

## Próximos Passos

- Definir contrato Task Queue -> Agent Orchestrator.
- Conectar solicitações de capabilities ao `capabilities/` sem acoplamento a tools.

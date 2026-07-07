# Módulo audit

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0001](../../../specs/framework/0001-framework-foundation.md) | [Spec 0013](../../../specs/framework/0013-persistence-layer.md)

## Objetivo

Definir contratos iniciais para Audit/Event Log interno do Vercosa AI Framework, permitindo representar eventos relevantes de forma estruturada, determinística e testável.

## O Que Este Módulo Faz

- Define categorias, severidades e resultados de eventos internos.
- Define `AuditEvent` como estrutura mínima para eventos do framework.
- Gera `event_id` determinístico a partir dos dados normalizados do evento quando o identificador não é informado.
- Permite `created_at` controlável pelo chamador para testes determinísticos.
- Define a porta `EventLog`.
- Fornece `InMemoryEventLog`, uma implementação em memória para registrar, listar, filtrar e limpar eventos.

## O Que Este Módulo Não Faz

- Não implementa persistência em arquivo.
- Não implementa banco de dados.
- Não implementa SQLite.
- Não implementa PostgreSQL.
- Não implementa OpenTelemetry.
- Não exporta eventos para dashboards, serviços externos ou observabilidade distribuída.
- Não chama LLM, provider, runtime, MCP, rede ou API externa.
- Não integra automaticamente com Guardian Engine, Policy Engine, Context Router, Model Selection, Runtime Adapter, Mission Runner ou Provider Gateway nesta etapa.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Enums, `AuditEvent`, geração determinística de `event_id` e timestamp auxiliar. |
| `event_log.py` | Porta `EventLog` e implementação `InMemoryEventLog`. |
| `__init__.py` | Exportações públicas do módulo. |
| `README.md` | Documentação do módulo e limites arquiteturais. |

## Principais Tipos, Classes E Funções

- `EventCategory`: `mission`, `policy`, `guardian`, `context`, `model_selection`, `runtime`, `provider`, `usage_limit` e `system`.
- `EventSeverity`: `debug`, `info`, `warning`, `error` e `critical`.
- `EventResult`: `success`, `skipped`, `warning`, `failed`, `blocked` e `requires_approval`.
- `AuditEvent`: evento interno estruturado com `event_id`, categoria, nome, severidade, resultado, mensagem, origem, metadados e timestamp opcional.
- `EventLog`: contrato para registrar, listar, filtrar e limpar eventos.
- `InMemoryEventLog`: implementação em memória, determinística e sem persistência externa.

## Entradas E Saídas

Entradas:

- Eventos `AuditEvent` criados por chamadores autorizados.
- Filtros por categoria, severidade ou resultado.

Saídas:

- Tuplas de eventos em ordem determinística de inserção.
- Snapshots imutáveis da lista interna, sem expor a lista mutável usada pela implementação em memória.

## Dependências Internas

- Nenhuma dependência interna obrigatória além do próprio pacote `audit/`.
- O módulo não importa módulos de missão, política, Guardian, contexto, seleção de modelo, runtime, providers ou persistência.

## Módulos Relacionados

- Acima: [missions](../missions/README.md), [policy](../policy/README.md), [guardian](../guardian/README.md), [context](../context/README.md), [model_selection](../model_selection/README.md), [runtime](../runtime/README.md), [providers](../providers/README.md).
- Futuro: [persistence](../persistence/README.md) poderá persistir eventos quando houver contrato aprovado para durabilidade e retenção.

## Relações Futuras Previstas

- `missions/` poderá registrar início, conclusão, falha e validação de missões.
- `policy/` poderá registrar políticas resolvidas, conflitos e warnings.
- `guardian/` poderá registrar decisões, bloqueios, aprovações requeridas e sinais do `Usage/API Limit Guard`.
- `context/` poderá registrar montagem de `ContextPackage`, omissões, redactions e warnings.
- `model_selection/` poderá registrar seleção de modelo, fallback e restrições de orçamento.
- `runtime/` poderá registrar planos e resultados normalizados de execução.
- `providers/` e futuro Provider Gateway poderão registrar chamadas governadas sem expor segredos ou payload sensível bruto.

Essas relações são próximos passos possíveis. Elas não estão implementadas nesta missão.

## Specs Correspondentes

- [Spec 0001: Framework Foundation](../../../specs/framework/0001-framework-foundation.md)
- [Spec 0013: Persistence Layer](../../../specs/framework/0013-persistence-layer.md)

## Docs Relacionadas

- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)
- [Estado atual](../../../docs/alignment/current-state.md)
- [Roadmap](../../../docs/alignment/roadmap.md)
- [Backlog estratégico de missões](../../../docs/roadmap/mission-backlog.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.audit import AuditEvent, EventCategory, InMemoryEventLog

event = AuditEvent(
    category=EventCategory.SYSTEM,
    name="framework.started",
    message="Evento interno registrado em memória.",
    created_at="2026-07-07T00:00:00+00:00",
)

event_log = InMemoryEventLog()
event_log.record(event)
events = event_log.list_events()
```

O exemplo não grava arquivo, não acessa banco, não chama rede e não integra observabilidade externa.

## Status Atual

Status: `contracts`.

O módulo possui contratos iniciais e implementação em memória. Não há persistência externa, banco de dados, exportação, dashboards, OpenTelemetry ou integração automática com outros módulos.

## Próximos Passos

- Registrar decisões de Guardian.
- Registrar políticas resolvidas.
- Registrar montagem de `ContextPackage`.
- Registrar seleção de modelo.
- Registrar falhas de quota, rate limit e limites de uso.
- Definir persistência futura por contratos aprovados.
- Definir exportação futura sem acoplar observabilidade externa ao núcleo.

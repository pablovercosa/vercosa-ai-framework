# Módulo audit

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Arquitetura de Audit/Event Log](../../../docs/architecture/audit-event-architecture.md) | [Spec 0001](../../../specs/framework/0001-framework-foundation.md) | [Spec 0013](../../../specs/framework/0013-persistence-layer.md)

## Objetivo

Definir contratos iniciais para Audit/Event Log interno do Vercosa AI Framework, permitindo representar eventos relevantes de forma estruturada, determinística, testável e segura para composição futura.

## O Que Este Módulo Faz

- Define categorias, severidades e resultados de eventos internos.
- Define `AuditEvent` como estrutura mínima para eventos auditáveis do framework.
- Gera `event_id` determinístico a partir dos dados normalizados do evento quando o identificador não é informado.
- Permite `created_at` controlável pelo chamador para testes determinísticos.
- Define a porta `EventLog`.
- Fornece `InMemoryEventLog`, uma implementação em memória para registrar, listar, filtrar e limpar eventos.
- Fornece helpers opcionais para eventos derivados de Policy Engine, Guardian Engine e Context Router.
- Fornece helpers opcionais para eventos básicos de ciclo de vida de missão e batch.
- Permite que o `MissionRunner` Python registre eventos quando recebe um `EventLog` opcional.

## O Que Este Módulo Não Faz

- Não implementa persistência em arquivo.
- Não implementa JSONL.
- Não implementa banco de dados.
- Não implementa SQLite.
- Não implementa PostgreSQL.
- Não implementa OpenTelemetry.
- Não exporta eventos para dashboards, serviços externos ou observabilidade distribuída.
- Não chama LLM, provider, runtime, MCP, rede ou API externa.
- Não integra automaticamente com scripts shell.
- Não torna o Event Log obrigatório para Policy Engine, Guardian Engine, Context Router, Model Selection, Runtime Adapter ou Provider Gateway.
- Não captura conteúdo bruto, prompts completos, segredos, credenciais ou tokens de API por padrão.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Enums `EventCategory`, `EventSeverity`, `EventResult`, dataclass `AuditEvent`, geração determinística de `event_id` e timestamp auxiliar. |
| `event_log.py` | Porta `EventLog` e implementação `InMemoryEventLog`, com listagem, filtros e limpeza em memória. |
| `integrations.py` | Helpers opcionais para eventos derivados de decisões de Policy Engine, Guardian Engine e Context Router. |
| `mission_events.py` | Helpers opcionais para eventos de ciclo de vida de missão e batch. |
| `__init__.py` | Exportações públicas do módulo. |
| `README.md` | Visão de módulo, limites e links para documentação arquitetural. |

## Principais Tipos, Classes E Funções

- `EventCategory`: `mission`, `policy`, `guardian`, `context`, `model_selection`, `runtime`, `provider`, `usage_limit` e `system`.
- `EventSeverity`: `debug`, `info`, `warning`, `error` e `critical`.
- `EventResult`: `success`, `skipped`, `warning`, `failed`, `blocked` e `requires_approval`.
- `AuditEvent`: evento interno estruturado com `event_id`, categoria, nome, severidade, resultado, mensagem, origem, metadados e timestamp opcional.
- `EventLog`: contrato para registrar, listar, filtrar e limpar eventos.
- `InMemoryEventLog`: implementação em memória, determinística e sem persistência externa.
- `policy_resolution_event()` e `record_policy_resolution_event()`: criam ou registram evento de resolução de política.
- `guardian_decision_event()` e `record_guardian_decision_event()`: criam ou registram evento de decisão Guardian.
- `context_package_event()` e `record_context_package_event()`: criam ou registram evento de `ContextPackage`.
- `mission_queued_event()`, `mission_started_event()`, `mission_completed_event()`, `mission_failed_event()` e `mission_skipped_event()`: criam eventos de missão.
- `batch_started_event()`, `batch_completed_event()` e `batch_interrupted_event()`: criam eventos de batch.
- `record_mission_event()`: registra evento de missão somente quando um `EventLog` opcional é fornecido.

## Entradas E Saídas

Entradas:

- Eventos `AuditEvent` criados por chamadores autorizados.
- Resultados já produzidos por Policy Engine, Guardian Engine ou Context Router quando o chamador quiser criar evento auditável.
- Metadados seguros de missão ou batch informados explicitamente pelo chamador.
- Filtros por categoria, severidade ou resultado.

Saídas:

- Tuplas de eventos em ordem determinística de inserção.
- Snapshots imutáveis da lista interna, sem expor a lista mutável usada pela implementação em memória.
- Eventos estruturados com categorias, severidades, resultados e metadados mínimos.

## Dependências Internas

- `integrations.py` importa tipos de `policy/`, `guardian/` e `context/` para criar eventos a partir de resultados já existentes.
- `mission_events.py` depende apenas dos tipos e da porta de Audit/Event Log.
- `event_log.py` e `types.py` continuam sem dependência de módulos consumidores.
- O módulo não importa seleção de modelo, runtime, providers ou persistência.

## Módulos Relacionados

- Acima: [missions](../missions/README.md), [policy](../policy/README.md), [guardian](../guardian/README.md), [context](../context/README.md), [model_selection](../model_selection/README.md), [runtime](../runtime/README.md), [providers](../providers/README.md).
- Futuro: [persistence](../persistence/README.md) poderá persistir eventos quando houver contrato aprovado para durabilidade e retenção.

## Specs Correspondentes

- [Spec 0001: Framework Foundation](../../../specs/framework/0001-framework-foundation.md)
- [Spec 0013: Persistence Layer](../../../specs/framework/0013-persistence-layer.md)

## Docs Relacionadas

- [Arquitetura de Audit/Event Log](../../../docs/architecture/audit-event-architecture.md)
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

O módulo possui contratos iniciais, implementação em memória, helpers opcionais para eventos de Policy, Guardian, Context e missão, além de integração opcional inicial com o `MissionRunner` Python. Não há persistência externa, banco de dados, SQLite, PostgreSQL, exportação, dashboards, OpenTelemetry ou integração automática com scripts operacionais.

## Próximos Passos

- Persistir eventos em arquivo local controlado quando houver contrato aprovado.
- Registrar eventos estruturados durante scripts de runner e batch quando houver contrato seguro.
- Relacionar eventos com commits e artefatos alterados.
- Registrar seleção de modelo, fallback e restrições de orçamento.
- Registrar limites de quota, rate limit e uso/API como eventos estruturados quando o contrato estiver definido.
- Definir redaction de metadata e política de retenção.
- Integrar eventos futuros com Provider Gateway sem registrar payloads sensíveis.

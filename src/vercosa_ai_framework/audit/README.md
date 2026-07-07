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
- Fornece helpers opcionais para transformar resultados de Policy Engine, Guardian Engine e Context Router em eventos auditáveis estruturados.
- Fornece helpers opcionais para representar eventos auditáveis básicos de ciclo de vida de missão e batch.

## O Que Este Módulo Não Faz

- Não implementa persistência em arquivo.
- Não implementa banco de dados.
- Não implementa SQLite.
- Não implementa PostgreSQL.
- Não implementa OpenTelemetry.
- Não exporta eventos para dashboards, serviços externos ou observabilidade distribuída.
- Não chama LLM, provider, runtime, MCP, rede ou API externa.
- Não integra automaticamente com Guardian Engine, Policy Engine, Context Router, Model Selection, Runtime Adapter ou Provider Gateway nesta etapa.
- Não altera scripts shell nem o fluxo operacional `queue`, `running`, `done` e `failed` das missões.
- Não captura conteúdo bruto, prompts completos, segredos, credenciais ou tokens de API por padrão.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Enums, `AuditEvent`, geração determinística de `event_id` e timestamp auxiliar. |
| `event_log.py` | Porta `EventLog` e implementação `InMemoryEventLog`. |
| `integrations.py` | Helpers opcionais para eventos derivados de decisões de Policy, Guardian e Context. |
| `mission_events.py` | Helpers opcionais para eventos de ciclo de vida de missão e batch. |
| `__init__.py` | Exportações públicas do módulo. |
| `README.md` | Documentação do módulo e limites arquiteturais. |

## Principais Tipos, Classes E Funções

- `EventCategory`: `mission`, `policy`, `guardian`, `context`, `model_selection`, `runtime`, `provider`, `usage_limit` e `system`.
- `EventSeverity`: `debug`, `info`, `warning`, `error` e `critical`.
- `EventResult`: `success`, `skipped`, `warning`, `failed`, `blocked` e `requires_approval`.
- `AuditEvent`: evento interno estruturado com `event_id`, categoria, nome, severidade, resultado, mensagem, origem, metadados e timestamp opcional.
- `EventLog`: contrato para registrar, listar, filtrar e limpar eventos.
- `InMemoryEventLog`: implementação em memória, determinística e sem persistência externa.
- `policy_resolution_event()`: cria evento estruturado para `PolicyResolutionResult`.
- `guardian_decision_event()`: cria evento estruturado para `GuardianDecision`.
- `context_package_event()`: cria evento estruturado para `ContextPackage`.
- `record_policy_resolution_event()`, `record_guardian_decision_event()` e `record_context_package_event()`: gravam o evento somente quando um `EventLog` opcional é fornecido.
- `mission_queued_event()`, `mission_started_event()`, `mission_completed_event()`, `mission_failed_event()` e `mission_skipped_event()`: criam eventos estruturados de ciclo de vida de missão.
- `batch_started_event()`, `batch_completed_event()` e `batch_interrupted_event()`: criam eventos estruturados de ciclo de vida de batch.
- `record_mission_event()`: grava evento de missão somente quando um `EventLog` opcional é fornecido.

## Entradas E Saídas

Entradas:

- Eventos `AuditEvent` criados por chamadores autorizados.
- Resultados já produzidos por Policy Engine, Guardian Engine ou Context Router quando o chamador quiser criar evento auditável.
- Metadados seguros de missão ou batch informados explicitamente pelo chamador.
- Filtros por categoria, severidade ou resultado.

Saídas:

- Tuplas de eventos em ordem determinística de inserção.
- Snapshots imutáveis da lista interna, sem expor a lista mutável usada pela implementação em memória.
- Eventos estruturados com categoria `policy`, `guardian`, `context` ou `mission`, severidade, resultado e metadados mínimos.

## Dependências Internas

- `integrations.py` importa tipos de `policy/`, `guardian/` e `context/` para criar eventos a partir de resultados já existentes.
- `mission_events.py` depende apenas dos tipos e da porta de Audit/Event Log.
- `event_log.py` e `types.py` continuam sem dependência de módulos consumidores.
- O módulo não importa seleção de modelo, runtime, providers ou persistência.

## Módulos Relacionados

- Acima: [missions](../missions/README.md), [policy](../policy/README.md), [guardian](../guardian/README.md), [context](../context/README.md), [model_selection](../model_selection/README.md), [runtime](../runtime/README.md), [providers](../providers/README.md).
- Futuro: [persistence](../persistence/README.md) poderá persistir eventos quando houver contrato aprovado para durabilidade e retenção.

## Integração Inicial Com Decisões Centrais

O módulo possui integração inicial e opcional com decisões centrais por meio de helpers em `integrations.py`. Essa integração não altera o comportamento dos módulos consumidores e não exige que Policy Engine, Guardian Engine ou Context Router recebam um `EventLog`.

Os eventos atuais podem representar:

- políticas resolvidas, quantidade de políticas consideradas, políticas resolvidas, conflitos, warnings, `deny` e `require_approval`;
- conflitos de política por identificadores e contadores, sem registrar conteúdo bruto da regra além de refs estruturadas;
- decisões Guardian, ação operacional, warnings, bloqueios, aprovação requerida, origem da avaliação, risco e refs de políticas;
- montagem de `ContextPackage`, quantidade de candidatos quando informada, itens selecionados, itens omitidos, estimativa de tokens, warnings, motivos de omissão e sinal de aprovação requerida;
- omissões de contexto por motivo agregado e refs de itens omitidos, sem registrar o conteúdo integral dos itens.

A integração é explícita:

```python
from vercosa_ai_framework.audit import InMemoryEventLog, record_policy_resolution_event

event_log = InMemoryEventLog()
event = record_policy_resolution_event(policy_result, event_log=event_log)
```

Se `event_log` não for fornecido, os helpers `record_*` apenas retornam o evento criado. Isso mantém a integração opcional e evita dependência obrigatória de log nos módulos consumidores.

## Integração Inicial Com Missões

O módulo possui helpers explícitos para eventos de ciclo de vida de missões e batch. Esses helpers criam `AuditEvent` com categoria `mission`, nomes determinísticos e severidade/resultado coerentes com o estado representado.

Eventos de missão já representáveis:

- `mission.queued`: missão enfileirada, com severidade `info` e resultado `success`.
- `mission.started`: missão iniciada, com severidade `info` e resultado `success`.
- `mission.completed`: missão concluída, com severidade `info` e resultado `success`.
- `mission.failed`: missão com falha, com severidade `error` e resultado `failed`.
- `mission.skipped`: missão ignorada, com severidade `warning` e resultado `skipped`.

Eventos de batch já representáveis:

- `mission.batch.started`: batch iniciado, com severidade `info` e resultado `success`.
- `mission.batch.completed`: batch concluído, com severidade `info` e resultado `success`.
- `mission.batch.interrupted`: batch interrompido, com severidade `warning` e resultado `failed`.

O `MissionRunner` Python pode receber um `EventLog` opcional e registrar eventos de missão enfileirada, iniciada, concluída e com falha. Se `event_log` não for fornecido, o runner mantém o comportamento atual e não registra eventos estruturados.

Os scripts shell (`scripts/vaf-run-one-mission.sh`, `scripts/vaf-worker.sh`, `scripts/vaf-run-next-safe.sh` e `scripts/vaf-run-batch-safe.sh`) continuam usando logs textuais e movimentação de arquivos por `missions/queue`, `missions/running`, `missions/done` e `missions/failed`. Eles não emitem esses eventos automaticamente nesta etapa.

Metadados permitidos nos helpers de missão são restritos a dados seguros:

- `mission_id`.
- `mission_name`.
- `mission_path`.
- `batch_size`.
- `executed_count`.
- `queue_count`.
- `done_count`.
- `failed_count`.
- `commit_hash`.

Os helpers não exigem conteúdo integral da missão, não registram prompts completos por padrão, não registram secrets, não registram credenciais e não registram tokens de API.

## Logs Textuais, Eventos Auditáveis E Persistência

Log textual operacional é saída humana ou de terminal usada para diagnóstico imediato. Ele pode conter mensagens livres e não é, por si só, um registro estruturado.

Evento auditável estruturado é um `AuditEvent` com categoria, nome, severidade, resultado, origem e metadados normalizados. Ele deve carregar refs, contadores e sinais úteis sem capturar conteúdo sensível por padrão. Eventos de missão são uma base estruturada para rastreabilidade, mas não substituem os logs textuais dos scripts.

Persistência futura é a gravação durável desses eventos em arquivo, banco ou outro adapter aprovado. Ela ainda não existe neste módulo. O `InMemoryEventLog` mantém eventos somente em memória durante o processo.

## Relações Futuras Previstas

- `missions/` já pode registrar eventos básicos no `MissionRunner` Python quando recebe `EventLog` opcional; integração completa dos scripts operacionais continua futura.
- `policy/` já pode ter resultados transformados em eventos por helper opcional; integração automática continua futura.
- `guardian/` já pode ter decisões transformadas em eventos por helper opcional; sinais do `Usage/API Limit Guard` ainda são próximos passos.
- `context/` já pode ter `ContextPackage`, omissões e warnings transformados em eventos por helper opcional; redactions detalhadas continuam limitadas a contadores e refs.
- `model_selection/` poderá registrar seleção de modelo, fallback e restrições de orçamento.
- `runtime/` poderá registrar planos e resultados normalizados de execução.
- `providers/` e futuro Provider Gateway poderão registrar chamadas governadas sem expor segredos ou payload sensível bruto.

As integrações existentes são helpers explícitos e opcionais. Integração automática em fluxos orquestrados continua como próximo passo possível.

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

O módulo possui contratos iniciais, implementação em memória, helpers opcionais para eventos de Policy, Guardian, Context e missão, além de integração opcional inicial com o `MissionRunner` Python. Não há persistência externa, banco de dados, exportação, dashboards, OpenTelemetry ou integração automática com scripts operacionais.

## Próximos Passos

- Registrar eventos reais durante execução dos scripts de runner quando houver contrato seguro.
- Registrar eventos reais durante batch quando houver contrato seguro.
- Persistir eventos em arquivo controlado quando houver contrato aprovado.
- Exportar eventos quando houver contrato aprovado.
- Relacionar eventos com commits e artefatos alterados.
- Registrar seleção de modelo.
- Registrar falhas de quota, rate limit e limites de uso.
- Definir persistência futura por contratos aprovados.
- Definir exportação futura sem acoplar observabilidade externa ao núcleo.
- Integrar eventos futuros com Provider Gateway sem registrar payloads sensíveis.

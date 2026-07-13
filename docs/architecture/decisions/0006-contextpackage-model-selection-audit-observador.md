# ADR 0006: Propagar ContextPackage Para Model Selection E Audit/Event Log Observador

Estado: Aceita.

## Contexto

A missão 0107 validou Context Router e Token Budget Manager produzindo `ContextPackage`, requisitos mínimos para Model Selection e eventos auditáveis por `InMemoryEventLog`.

## Decisão

Usar `ContextPackage` como artefato rastreável para alimentar requisitos de contexto do Model Selection. Manter Audit/Event Log como observador injetável e opcional, sem decidir nem controlar fluxo.

## Evidências

- Código: `src/vercosa_ai_framework/context/router.py`.
- Código: `src/vercosa_ai_framework/context/budget.py`.
- Código: `src/vercosa_ai_framework/model_selection/selector.py`.
- Código: `src/vercosa_ai_framework/audit/event_log.py`.
- Teste: `tests/test_agent_execution_governance_0107.py`.
- Teste: `tests/test_token_budget_model_selection_integration.py`.
- Teste: `tests/test_audit_event_log_contracts.py`.

## Consequências

- Context Router trabalha com candidatos explícitos e não implementa RAG.
- Token Budget Manager pode omitir itens deterministicamente.
- Model Selection não chama provider nem runtime.
- EventLog registra eventos sem armazenar conteúdo sensível completo.
- `JsonlAuditEventLog` permanece opt-in.

## Decisões Ainda Pendentes

- Persistência externa de auditoria.
- Semantic Index, PostgreSQL, pgvector e RAG.
- Modelo definitivo de memória e retenção de conversas.

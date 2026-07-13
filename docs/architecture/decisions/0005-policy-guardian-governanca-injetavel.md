# ADR 0005: Separar Policy Engine, Guardian Engine E Governança Injetável

Estado: Aceita.

## Contexto

A missão 0107 validou um fluxo governado em que Policy Engine resolve políticas declarativas, Guardian Engine aplica enforcement operacional e `AgentExecutionGovernance` injeta a composição de governança no Agent Orchestrator.

## Decisão

Manter Policy Engine e Guardian Engine separados.

Policy Engine resolve políticas declarativas e produz `ResolvedPolicySet`. Guardian Engine aplica enforcement operacional e emite decisões `allow`, `warn`, `block` ou `require_approval`. Execution Governance é dependência explícita e opcional do Agent Orchestrator; quando exigida e ausente, a execução falha antes do runtime.

## Evidências

- Código: `src/vercosa_ai_framework/policy/engine.py`.
- Código: `src/vercosa_ai_framework/guardian/engine.py`.
- Código: `src/vercosa_ai_framework/agents/governance.py`.
- Teste: `tests/test_policy_guardian_integration.py`.
- Teste: `tests/test_agent_execution_governance_0107.py`.

## Consequências

- Policy Engine não executa ações.
- Guardian Engine não substitui resolução declarativa.
- `BLOCK` impede execução.
- `REQUIRE_APPROVAL` impede execução automática sem aprovação representada.
- `WARN` preserva referência e permite continuidade quando o contrato permite.

## Decisões Ainda Pendentes

- Formato definitivo de aprovação humana.
- Versionamento e migração de políticas declarativas.
- Modo Guardian padrão para automação ou daemon.

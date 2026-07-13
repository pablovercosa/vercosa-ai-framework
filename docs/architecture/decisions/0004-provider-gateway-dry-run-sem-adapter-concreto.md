# ADR 0004: Usar Provider Gateway Em Dry-Run Sem Adapter Concreto

Estado: Aceita.

## Contexto

A missão 0106 validou o uso de Provider Gateway real no modo `dry_run=True`. O fluxo preserva rastreabilidade sem chamar provider real, rede, banco, MCP, API externa ou adapter concreto.

## Decisão

Manter dry-run como execução real do contrato do Provider Gateway sem chamada a adapter concreto.

Provider Gateway seleciona e valida `ProviderProfile`, constrói `ProviderResult` rastreável e retorna status `dry_run`. Provider Gateway não é Model Selector.

## Evidências

- Código: `src/vercosa_ai_framework/providers/gateway.py`.
- Código: `src/vercosa_ai_framework/tools/executor.py`.
- Teste: `tests/test_provider_gateway.py`.
- Teste: `tests/test_tool_executor_provider_gateway.py`.
- Teste: `tests/test_capability_skill_tool_provider_dry_run.py`.

## Consequências

- Dry-run pode validar contratos e rastreabilidade sem efeitos externos.
- Adapter concreto não deve ser chamado em dry-run.
- Providers reais permanecem fora do fluxo validado atual.

## Decisões Ainda Pendentes

- Providers reais.
- Rede e fallback externo real.
- MCPs, bancos e APIs externas.

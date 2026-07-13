# Exemplo Mínimo Da Governança De Execução 0107

Este exemplo descreve o caminho mínimo validado localmente, sem provider real, rede, banco, MCP, API externa, RAG ou subprocesso.

```text
Task
-> PolicySet explícito
-> DeterministicPolicyEngine
-> ResolvedPolicySet
-> ContextRequest com ContextItems explícitos
-> DeterministicContextRouter
-> SimpleTokenBudgetManager
-> ContextPackage
-> GuardianEngine.evaluate_context_package()
-> ModelSelector com catálogo em memória
-> CapabilityResolver
-> ResolvedCapabilityExecutor em dry_run=True
-> SkillExecutor
-> ToolExecutor
-> ProviderGateway em dry-run
-> RuntimeAdapter fake
-> GuardianEngine de validação
-> InMemoryEventLog
```

## Contrato Mínimo

- `Task.metadata["policy_sets"]` recebe `PolicySet` explícitos.
- `Task.metadata["context_sources"]` e `Task.metadata["context_items"]` recebem candidatos locais explícitos.
- `Task.metadata["token_budget"]` define `max_input_tokens` e `reserved_output_tokens`.
- `ModelSelector` recebe catálogo em memória.
- `AgentExecutionGovernance` recebe `context_router`, `guardian_engine`, `model_selector` e `event_log` por injeção.
- `AgentOrchestrator` recebe `execution_governance` e pode exigir o pipeline com `require_execution_governance=True`.

## Garantias Do Exemplo

- Item que excede orçamento é omitido de forma determinística.
- `ContextPackage.model_requirements` influencia a seleção de modelo.
- `GuardianAction.BLOCK` e `GuardianAction.REQUIRE_APPROVAL` impedem capabilities e runtime.
- `GuardianAction.WARN` permite execução e preserva warnings.
- Provider Gateway permanece em dry-run e não chama adapter concreto.
- Eventos registram IDs, contagens, estados e refs, sem conteúdo integral do contexto.

Referência arquitetural: [Integração de Governança da Execução 0107](../architecture/execution-governance-0107.md).

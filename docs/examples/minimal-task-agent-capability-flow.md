# Exemplo Mínimo: Task Para Agent Com Capability Declarativa

Este exemplo descreve o fluxo mínimo validado na missão 0105. Ele é um exemplo de contrato em memória, não uma execução real de skill, tool, provider, MCP, API ou banco.

## Componentes

- `TaskQueue` com uma `Task` que declara `required_capabilities=("ReadContext",)`.
- `TaskScheduler` com executor injetado.
- `AgentTaskExecutor` como ponte para o `AgentOrchestrator`.
- `AgentRegistry` com `AgentProfile` compatível.
- `CapabilityRegistry` com `CapabilityProfile` ativa.
- `SkillRegistry` com `SkillProfile` declarativa e `required_tools=()`.
- `CapabilityResolver` configurado no `AgentOrchestrator`.
- `RuntimeAdapter` fake em teste.

## Fluxo

```text
TaskScheduler.run_until_idle(queue, AgentTaskExecutor(orchestrator))
↓
AgentOrchestrator.execute_task(task, attempt)
↓
CapabilityResolver.resolve(CapabilityRequest(...))
↓
RuntimeAdapter.execute_task(RuntimeExecutionRequest(...))
↓
AgentExecutionResult
↓
TaskExecutionOutcome(done)
```

## Evidências Esperadas

- O `agent_assignment_id` é o mesmo na capability request, no request de runtime, no resultado de agente e no outcome da task.
- A skill selecionada aparece como evidência declarativa em `capability_resolutions`.
- O runtime é chamado uma única vez quando a capability é resolvida com sucesso.
- Falha de capability ou permissão ausente bloqueia o runtime.

## Limites

Este exemplo não executa `SkillExecutor`, `ToolExecutor`, `ProviderGateway`, subprocessos, rede ou banco.

# Agent Orchestrator MVP

O Agent Orchestrator transforma uma `Task` elegivel em uma execucao de agente governada e rastreavel.

Ele fica entre Task Queue e Runtime Adapter:

```text
Task Queue
-> Agent Orchestrator
-> Runtime Adapter
-> normalized AgentExecutionResult
```

No caminho integrado da missão 0106, o orquestrador também pode receber um `CapabilityResolver` e um `capability_executor` configurados explicitamente para resolver e executar, em dry-run governado, todas as capabilities obrigatórias antes do runtime.

## Responsabilidades

- Receber uma `Task`.
- Selecionar um `AgentProfile` compativel por `role`, `domain`, `tags`, `task_type`, `required_capabilities`, `complexity` e `risk_level`.
- Consultar o Guardian Engine antes da execucao e antes de aceitar o resultado.
- Selecionar modelo via Model Selection Engine quando `model_catalog` e `model_policy` forem fornecidos.
- Montar um `AgentExecutionRequest` provider-neutral.
- Resolver capabilities obrigatórias por `CapabilityResolver` quando `require_capability_resolution=True`.
- Executar capabilities obrigatórias por contrato injetável de alto nível quando `capability_executor` e `require_capability_execution=True` forem configurados.
- Delegar a execucao concreta para um `RuntimeAdapter` abstrato.
- Normalizar o retorno como `AgentExecutionResult`.

## Fora do Escopo

- Chamar OpenCode diretamente.
- Chamar MCPs, providers, APIs, bancos ou subprocessos.
- Importar ou construir `ToolExecutor`, `ProviderGateway`, adapters concretos, MCPs, APIs ou clientes de rede.
- Executar subagents reais.
- Implementar paralelismo.
- Alterar Task Queue, dependencias ou criterios de aceite.

## Estado

O MVP usa o fluxo simples:

```text
idle -> planning -> executing -> validating -> done
idle -> planning -> failed
idle -> planning -> executing -> validating -> failed
```

As transicoes ficam em `AgentExecutionResult.metadata["state_transitions"]`.

## Guardian Engine

O orquestrador avalia dois pontos:

- `agent_assignment_planning`: antes de acionar o runtime.
- `agent_assignment_validation`: antes de marcar a assignment como concluida.

Decisoes `block` e `require_approval` impedem conclusao automatica.

## Model Selection

O orquestrador nao escolhe modelo por hardcode.

Quando existe catalogo de modelos e a Task declara `metadata["model_policy"]`, a politica e normalizada para `ModelSelectionPolicy` e enviada ao `ModelSelector`. A decisao e passada ao `RuntimeAdapter` dentro de `RuntimeExecutionRequest.selection_decision`.

## Runtime Adapter

O runtime recebe uma `RuntimeExecutionRequest` contendo:

- `selection_decision`, quando houver.
- `execution_limits`.
- politicas de log e aprovacao.
- contexto minimo com o `AgentExecutionRequest`.
- permissoes explicitas impedindo acesso direto a MCPs e providers.

Testes devem usar runtime fake ou dry-run. O MVP nao exige OpenCode real.

## Capability Resolver

Quando configurado com `capability_resolver` e `require_capability_resolution=True`, o Agent Orchestrator:

- cria uma `CapabilityRequest` por capability obrigatória;
- preserva `mission_id`, `workflow_id`, `task_id`, `attempt_id` em metadata e `agent_assignment_id`;
- usa permissões explícitas da task, como `metadata["granted_permissions"]` ou `metadata["inputs"]["granted_permissions"]`;
- registra `capability_resolutions` no `AgentExecutionRequest` e no `AgentExecutionResult`;
- impede chamada ao runtime quando uma capability obrigatória não existe, não tem permissão ou não possui skill declarativa compatível.

## Capability Executor

Quando configurado com `capability_executor` e `require_capability_execution=True`, o Agent Orchestrator:

- executa cada `CapabilityResolutionResult` em ordem de `task.required_capabilities`;
- preserva a skill selecionada pelo resolver;
- registra `capability_executions` no `AgentExecutionRequest` e no `AgentExecutionResult`;
- bloqueia o `RuntimeAdapter` quando uma capability obrigatória falha;
- mantém o acesso a Skill, Tool e Provider Gateway atrás do contrato injetado.

O fluxo validado pela missão 0106 usa `ProviderGateway` real em `dry_run=True`, `ProviderRegistry` declarativo e provider fake/local. Nenhum provider real, adapter concreto, rede, banco, MCP, API externa ou subprocesso é chamado.

## Erros

- `NoCompatibleAgentError`: nenhuma profile registrada atende a Task.
- `AgentOrchestratorError`: selecao de modelo ou outra etapa de preparacao falhou de forma segura.

Documento complementar: [Integração Task, Agent e Capability](architecture/task-agent-capability-integration.md).

Exemplo complementar: [Fluxo Capability, Skill, Tool e Provider Gateway em dry-run](examples/minimal-capability-skill-tool-provider-dry-run.md).

## Validacao

Comandos esperados:

```bash
pytest
python3 -m compileall src
```

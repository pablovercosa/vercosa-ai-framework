# Agent Orchestrator MVP

O Agent Orchestrator transforma uma `Task` elegivel em uma execucao de agente governada e rastreavel.

Ele fica entre Task Queue e Runtime Adapter:

```text
Task Queue
-> Agent Orchestrator
-> Runtime Adapter
-> normalized AgentExecutionResult
```

No caminho integrado da missão 0105, o orquestrador também pode receber um `CapabilityResolver` configurado explicitamente para resolver declarativamente todas as capabilities obrigatórias antes do runtime.

## Responsabilidades

- Receber uma `Task`.
- Selecionar um `AgentProfile` compativel por `role`, `domain`, `tags`, `task_type`, `required_capabilities`, `complexity` e `risk_level`.
- Consultar o Guardian Engine antes da execucao e antes de aceitar o resultado.
- Selecionar modelo via Model Selection Engine quando `model_catalog` e `model_policy` forem fornecidos.
- Montar um `AgentExecutionRequest` provider-neutral.
- Resolver capabilities obrigatórias por `CapabilityResolver` quando `require_capability_resolution=True`.
- Delegar a execucao concreta para um `RuntimeAdapter` abstrato.
- Normalizar o retorno como `AgentExecutionResult`.

## Fora do Escopo

- Chamar OpenCode diretamente.
- Chamar MCPs, providers, APIs, bancos ou subprocessos.
- Executar capabilities, skills ou tools.
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

A skill selecionada é apenas evidência declarativa de compatibilidade. Ela não é executada neste fluxo.

## Erros

- `NoCompatibleAgentError`: nenhuma profile registrada atende a Task.
- `AgentOrchestratorError`: selecao de modelo ou outra etapa de preparacao falhou de forma segura.

Documento complementar: [Integração Task, Agent e Capability](architecture/task-agent-capability-integration.md).

## Validacao

Comandos esperados:

```bash
pytest
python3 -m compileall src
```

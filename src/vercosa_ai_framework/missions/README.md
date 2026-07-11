# Módulo missions

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0004](../../../specs/framework/0004-mission-runner.md)

## Objetivo

Controlar o ciclo operacional de missões em uma implementação local inicial.

## O Que Este Módulo Faz

- Define tipos de missão e resultado.
- Mantém uma fila local baseada em diretório.
- Executa uma missão por meio de `MissionRunner` com avaliação Guardian e RuntimeAdapter injetado.
- Executa uma missão pelo caminho integrado opcional com Workflow Engine e Task Queue quando `workflow_provider` e `workflow_executor` são injetados.
- Compõe contexto efetivo de execução por `prompt_composer`, usado pelo runner shell antes do OpenCode.
- Controla estados básicos como fila, execução, conclusão, falha e cancelamento.
- Pode registrar eventos auditáveis estruturados de ciclo de vida quando um `EventLog` opcional é fornecido ao `MissionRunner`.

## O Que Este Módulo Não Faz

- Não substitui o Mission Orchestrator conceitual.
- Não decompõe missões em workflows completos por conta própria.
- Não escolhe modelos diretamente.
- Não chama providers, MCPs, tools ou bancos diretamente.
- Não altera configuração global nem usa `sudo`.
- Não substitui os logs textuais dos scripts operacionais.
- Não implementa persistência externa de eventos auditáveis.
- Não altera o fluxo operacional `queue`, `running`, `done` e `failed` usado pelos scripts shell.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | `Mission`, `MissionStatus` e `MissionResult`. |
| `queue.py` | `DirectoryMissionQueue` para fila local. |
| `runner.py` | `MissionRunner` e contratos auxiliares de execução. |
| `workflow_integration.py` | Contratos injetáveis para resolver e executar workflows a partir de missões. |
| `prompt_composer.py` | Composição determinística de `AGENTS.md`, contrato base, agentes operacionais e missão. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `Mission`: unidade auditável de intenção e execução.
- `MissionStatus`: estados operacionais da missão.
- `MissionResult`: resultado normalizado de execução.
- `DirectoryMissionQueue`: fila local de missões em filesystem.
- `MissionRunner`: executa uma missão com Guardian e RuntimeAdapter.
- `MissionWorkflowProvider`: protocolo para resolver uma missão em workflow sem catálogo persistente obrigatório.
- `MissionWorkflowExecutor`: protocolo para executar workflow e retornar `WorkflowResult` ao runner.
- `QueueBackedWorkflowExecutor`: adapter para usar `WorkflowEngine.execute_with_queue()` no Mission Runner.
- `compose_mission_prompt`: compõe o contexto efetivo de execução sem modificar os arquivos de origem.
- `validate_mission_prompt`: valida a composição sem persistir prompt composto.
- `AutoCommitter`: protocolo para commit automático quando política permitir.
- `GuardianEvaluator`: protocolo para avaliação de política.
- `event_log` opcional em `MissionRunner`: permite registrar eventos `mission.queued`, `mission.started`, `mission.completed` e `mission.failed` em memória ou outra porta compatível fornecida pelo chamador.

## Entradas E Saídas

Entradas:

- `Mission` carregada de arquivo, fila ou chamada Python.
- `GuardianEngine` ou avaliador compatível.
- `RuntimeAdapter` para execução concreta.
- `MissionWorkflowProvider` e `MissionWorkflowExecutor` quando o caminho integrado for usado.

Saídas:

- `MissionResult` com status, saída, erro e metadados.
- Arquivos de fila atualizados quando `DirectoryMissionQueue` é usado.
- Eventos auditáveis estruturados somente quando um `EventLog` opcional é injetado.
- Prompt composto em memória ou stdout quando solicitado explicitamente; o runner shell usa arquivo temporário removido ao final.

## Dependências Internas

- `../guardian/`: avaliação de políticas antes da execução.
- `../runtime/`: execução concreta por adapter.
- `../workflows/`: caminho integrado opcional Mission -> Workflow -> Task Queue.
- `../audit/`: contrato opcional de eventos auditáveis estruturados.

## Módulos Relacionados

- Acima: [core](../core/README.md).
- Abaixo: [workflows](../workflows/README.md).
- Transversal: [audit](../audit/README.md), [persistence](../persistence/README.md), [guardian](../guardian/README.md).

## Eventos Auditáveis De Missão

O `MissionRunner` pode receber um `EventLog` opcional. Quando fornecido, ele registra eventos estruturados básicos do ciclo de vida de missão sem mudar a decisão de execução, sem gravar arquivo, sem acessar banco e sem chamar provider externo.

Eventos emitidos pelo `MissionRunner` nesta etapa:

- `mission.queued`: missão registrada na fila Python.
- `mission.started`: missão iniciada pelo runner Python.
- `mission.completed`: missão concluída com sucesso.
- `mission.failed`: missão concluída com falha.

Eventos de batch e missão ignorada já possuem helpers em [audit](../audit/README.md), mas os scripts shell ainda não os emitem automaticamente.

Os eventos carregam metadados seguros como `mission_id`, `mission_name` e `commit_hash` quando disponível. Eles não registram por padrão o conteúdo integral da missão, prompts completos, segredos, credenciais ou tokens de API.

Logs textuais dos scripts continuam sendo saída operacional humana. Eventos auditáveis são registros estruturados criados por helpers Python. Persistência futura de eventos ainda depende de contrato aprovado e não faz parte deste módulo.

## Specs Correspondentes

- [Spec 0004: Mission Runner](../../../specs/framework/0004-mission-runner.md)
- [Spec 0001: Framework Foundation](../../../specs/framework/0001-framework-foundation.md)

## Docs Relacionadas

- [Mission Runner](../../../docs/mission-runner.md)
- [Integração Mission Runner, Workflow Engine e Task Queue](../../../docs/architecture/mission-workflow-task-integration.md)
- [Contrato de execução de missões](../../../docs/operations/mission-execution-contract.md)
- [Formato compacto de missão](../../../docs/operations/compact-mission-format.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)
- [SDD Lifecycle](../../../docs/alignment/sdd-lifecycle.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.missions import Mission

mission = Mission(title="Documentar módulo", goal="Criar README técnico")
```

## Status Atual

Status: `MVP`.

Existe execução local mínima com eventos auditáveis opcionais em Python, composição obrigatória de contexto no runner shell e integração opcional Mission Runner -> Workflow Engine -> Task Queue por contratos injetáveis. A separação final entre Mission Runner e Mission Orchestrator ainda está em aberto.

## Próximos Passos

- Resolver a fronteira Mission Runner versus Mission Orchestrator.
- Revisar Specs/ADRs da integração Mission Runner -> Workflow Engine -> Task Queue na missão 0108.
- Integrar, em missão futura, os scripts operacionais aos eventos auditáveis sem substituir logs textuais nem alterar o fluxo `queue`, `running`, `done` e `failed`.

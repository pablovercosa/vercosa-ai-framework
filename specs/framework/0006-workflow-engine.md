# Spec 0006 — Workflow Engine

## Status

Proposta.

## Objetivo

Definir o Workflow Engine do Vercosa AI Framework como o componente responsável por transformar uma Mission aprovada para execução em um Workflow Plan composto por Tasks rastreáveis, ordenadas, validáveis e governadas por políticas.

O Workflow Engine deve permitir execução sequencial inicial e preparar a arquitetura para execução paralela futura, sem acoplar o núcleo do framework a agentes, runtimes, providers, modelos, banco de dados, sistema operacional ou ferramentas específicas.

## Contexto

O Vercosa AI Framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design.

As Specs 0001, 0002, 0003, 0004 e 0005 estabelecem que:

- o usuário fornece missões, não prompts gigantes;
- missões devem ser decompostas em workflows, tarefas, agentes, loops, validações e entregáveis;
- nenhum código deve ser implementado sem Spec aprovada;
- Guardian Specs prevalecem sobre políticas locais;
- modelos devem ser escolhidos pelo Model Selection Engine, não hardcoded;
- runtimes concretos, como OpenCode, devem ser acessados por adapters;
- o Mission Runner controla fila, estados, limites globais, orçamento, logs e encerramento de missão;
- o Guardian Engine avalia missões, planos e ações antes e durante execução;
- todo loop precisa de condição de parada.

O Workflow Engine é a camada que converte intenção em plano executável. Ele não executa comandos, não escolhe modelos diretamente, não chama providers, não substitui o Mission Runner, não executa agentes e não ignora decisões do Guardian Engine.

## Escopo

Esta Spec cobre:

- relação `Mission -> Workflow -> Task`;
- decomposição de missão em tarefas;
- estados de workflow;
- estados de task;
- dependências entre tarefas;
- execução sequencial inicial;
- preparação para execução paralela futura;
- integração com Guardian Engine;
- integração com Model Selection Engine;
- integração com Mission Runner;
- critérios de aceite por task;
- logs;
- rastreabilidade;
- retries;
- limites de custo, tokens e ciclos;
- encerramento seguro;
- relação futura com Agent Orchestrator;
- riscos, mitigações, decisões e critérios de aceite.

Esta Spec não cobre:

- implementação concreta em código;
- criação de CLI, daemon, serviço `systemd` ou API real;
- alteração de configurações globais;
- uso de `sudo`;
- schema final de banco de dados;
- implementação final da Task Queue;
- implementação final do Agent Orchestrator;
- seleção concreta de modelos;
- execução direta de agentes, tools, MCPs, comandos ou providers;
- engine final de paralelismo distribuído.

## Princípios

1. Workflows são planos auditáveis derivados de missões.
2. Tasks são as menores unidades planejáveis, rastreáveis, validáveis e reexecutáveis.
3. Toda task deve ter objetivo, entrada, saída esperada, critérios de aceite e limites.
4. O Workflow Engine planeja e replaneja; execução pertence às camadas abaixo.
5. Execução inicial deve ser sequencial para reduzir risco operacional.
6. Paralelismo futuro deve depender de análise explícita de dependências, isolamento e política.
7. Políticas de segurança, custo, tokens, qualidade e arquitetura prevalecem sobre conveniência.
8. Replanejamento não deve apagar histórico nem resetar limites.
9. Falhas devem preservar estado suficiente para retry, revisão manual ou encerramento seguro.
10. O Workflow Engine deve ser provider agnostic, runtime agnostic e agent agnostic.

## Posição arquitetural

O Workflow Engine fica entre Mission Orchestrator ou Mission Runner e Task Queue.

Fluxo conceitual:

```text
Mission Runner
↓
Mission Orchestrator
↓
Workflow Engine
↓
Workflow Plan
↓
Task Queue
↓
Agent Orchestrator
↓
Agents / Subagents
↓
Capabilities
↓
Policy Engine / Guardian Engine
↓
Model Selection Engine
↓
Runtime Adapter
```

Enquanto o Mission Orchestrator e a Task Queue ainda forem parciais, o Mission Runner pode acionar diretamente um fluxo mínimo do Workflow Engine, desde que registre a limitação e preserve a separação de responsabilidades.

## Definições

### Mission

Uma Mission é uma intenção de alto nível fornecida por usuário, sistema, API ou outro componente autorizado.

A Mission define o objetivo, contexto, restrições, políticas, entregáveis esperados, critérios de aceite, orçamento, limites e rastreabilidade global.

### Workflow

Um Workflow é a representação planejada da execução de uma Mission.

Ele contém Tasks, dependências, ordem de execução, limites, políticas aplicadas, critérios de encerramento, validações e metadados de rastreabilidade.

Campos mínimos desejados:

- `workflow_id`;
- `mission_id`;
- `title`;
- `goal`;
- `status`;
- `spec_refs`;
- `guardian_refs`;
- `policy_refs`;
- `tasks`;
- `dependency_graph`;
- `execution_mode`;
- `execution_limits`;
- `budget_policy`;
- `validation_policy`;
- `retry_policy`;
- `created_at`;
- `started_at`;
- `finished_at`;
- `audit_log_ref`.

### Task

Uma Task é uma unidade de trabalho derivada de um Workflow.

Ela deve ser pequena o suficiente para execução controlada, validação objetiva, retry seguro e rastreabilidade de artefatos.

Campos mínimos desejados:

- `task_id`;
- `workflow_id`;
- `mission_id`;
- `title`;
- `goal`;
- `task_type`;
- `status`;
- `inputs`;
- `expected_outputs`;
- `acceptance_criteria`;
- `dependencies`;
- `blocked_by`;
- `priority`;
- `risk_level`;
- `required_capabilities`;
- `model_policy`;
- `execution_limits`;
- `retry_policy`;
- `validation_policy`;
- `assigned_agent_ref` quando houver;
- `artifacts`;
- `attempt_count`;
- `last_error`;
- `audit_log_ref`.

### Workflow Engine

Componente responsável por planejar, validar, atualizar e encerrar workflows.

Responsabilidades:

- receber missão normalizada e políticas aplicáveis;
- decompor missão em workflow e tasks;
- definir dependências entre tasks;
- definir ordem inicial de execução;
- declarar capacidades necessárias por task;
- declarar políticas de modelo por task sem escolher modelo concreto;
- definir critérios de aceite por task;
- definir limites por workflow e por task;
- solicitar avaliação do Guardian Engine para plano e replanejamentos;
- preparar tasks para a Task Queue;
- acompanhar resultados retornados pela execução;
- replanejar quando permitido;
- encerrar workflow com estado seguro e auditável.

Não responsabilidades:

- executar comandos;
- editar arquivos;
- chamar tools, MCPs, providers ou bancos diretamente;
- escolher modelo concreto sem Model Selection Engine;
- executar agentes diretamente;
- aprovar Specs;
- ignorar Guardian Engine;
- alterar configuração global;
- usar `sudo`;
- fazer rollback destrutivo.

## Relação Mission -> Workflow -> Task

A relação conceitual deve ser:

```text
Mission
↓ decomposição
Workflow
↓ quebra operacional
Tasks
↓ enfileiramento e execução governada
Task Queue / Agent Orchestrator
```

Regras:

1. Uma Mission pode gerar um ou mais Workflows, mas a execução inicial deve preferir um Workflow por Mission.
2. Um Workflow pertence a uma Mission.
3. Uma Task pertence a um Workflow e a uma Mission.
4. Toda Task deve ser rastreável ao objetivo da Mission.
5. Um Workflow não deve conter Task que não contribua para os entregáveis ou validações da Mission.
6. Alteração relevante de escopo deve gerar replanejamento registrado ou nova Mission, conforme política.
7. A conclusão da Mission depende da conclusão validada do Workflow aplicável e dos critérios globais do Mission Runner.

## Decomposição de missão em tarefas

O Workflow Engine deve decompor uma Mission em Tasks usando escopo, Specs, critérios de aceite, riscos, dependências e limites.

Etapas conceituais:

```text
load mission
↓
resolve applicable specs and policies
↓
classify mission type and risk
↓
identify deliverables
↓
identify required validations
↓
split deliverables into tasks
↓
define dependencies and order
↓
assign acceptance criteria per task
↓
estimate cost, tokens and cycles
↓
request Guardian Engine evaluation
↓
emit Workflow Plan
```

Regras:

1. Decomposição deve preferir Tasks pequenas e verificáveis.
2. Tasks devem separar planejamento, mudança, validação e documentação quando isso reduzir risco.
3. Tasks de implementação devem referenciar Spec aprovada.
4. Tasks de validação devem ser explícitas quando a Mission alterar código, configuração, segurança, dados ou documentação governada.
5. Tarefas ambíguas devem ser refinadas antes da execução ou bloqueadas para revisão manual.
6. O Workflow Engine deve evitar criar Tasks redundantes ou que aumentem contexto sem necessidade.
7. Cada Task deve declarar entradas necessárias por referência sempre que possível, não por cópia extensa de contexto.
8. A decomposição deve respeitar limites globais recebidos do Mission Runner e limites adicionais do Guardian Engine.

## Estados de workflow

Estados mínimos obrigatórios:

- `draft`: workflow planejado, ainda não autorizado para execução;
- `ready`: workflow validado por política e pronto para enfileirar tasks;
- `running`: workflow com uma ou mais tasks em execução ou aguardando resultado;
- `paused`: workflow parado aguardando aprovação, recurso, decisão ou intervenção manual;
- `replanning`: workflow em ajuste controlado após mudança, falha ou nova informação;
- `done`: workflow concluído e validado conforme critérios aplicáveis;
- `failed`: workflow encerrado por erro, política bloqueante, validação reprovada ou limite excedido;
- `cancelled`: workflow cancelado por usuário, sistema ou política.

Transições permitidas:

```text
draft -> ready
draft -> failed
draft -> cancelled
ready -> running
ready -> paused
ready -> cancelled
running -> paused
running -> replanning
running -> done
running -> failed
running -> cancelled
paused -> running
paused -> replanning
paused -> failed
paused -> cancelled
replanning -> ready
replanning -> running
replanning -> failed
replanning -> cancelled
failed -> replanning
cancelled -> replanning
```

Regras:

1. `done` é terminal para a execução atual do workflow.
2. `failed` e `cancelled` só podem voltar via `replanning` quando política permitir.
3. `replanning` não deve apagar tasks anteriores, logs ou tentativas.
4. Toda transição deve ser registrada em log.
5. Um workflow não deve entrar em `running` sem decisão compatível do Guardian Engine.
6. Um workflow não deve entrar em `done` sem validação das tasks obrigatórias e dos critérios globais aplicáveis.

## Estados de task

Estados mínimos obrigatórios:

- `pending`: task criada e ainda não elegível ou não iniciada;
- `ready`: task elegível para execução porque dependências obrigatórias foram satisfeitas;
- `running`: task em execução por camada inferior;
- `blocked`: task impedida por dependência, política, aprovação, recurso ou erro externo;
- `validating`: task aguardando validação de resultado;
- `done`: task concluída e validada conforme critérios de aceite;
- `failed`: task falhou por erro, validação reprovada ou limite excedido;
- `skipped`: task não executada por replanejamento ou decisão registrada;
- `cancelled`: task cancelada por usuário, sistema, política ou encerramento do workflow.

Transições permitidas:

```text
pending -> ready
pending -> blocked
pending -> skipped
pending -> cancelled
ready -> running
ready -> blocked
ready -> skipped
ready -> cancelled
running -> validating
running -> failed
running -> blocked
running -> cancelled
validating -> done
validating -> failed
validating -> blocked
failed -> ready
failed -> skipped
blocked -> ready
blocked -> failed
blocked -> cancelled
```

Regras:

1. `done`, `skipped` e `cancelled` são terminais para a tentativa atual.
2. Retry de task falhada deve criar nova tentativa ou reabrir como `ready` com contador incrementado.
3. `skipped` exige justificativa e não pode ocultar critério de aceite obrigatório.
4. Uma Task só pode virar `ready` quando dependências obrigatórias estiverem satisfeitas.
5. Uma Task só pode virar `done` quando seus critérios de aceite forem avaliados.
6. Toda falha deve registrar causa, tentativa, limites consumidos e próxima ação segura.

## Dependências entre tarefas

O Workflow Engine deve representar dependências como grafo direcionado acíclico sempre que possível.

Tipos mínimos de dependência:

- `requires_completion`: a task depende da conclusão de outra task;
- `requires_artifact`: a task depende de artefato produzido por outra task;
- `requires_validation`: a task depende de validação aprovada;
- `requires_approval`: a task depende de aprovação humana ou política;
- `blocks`: a task bloqueia outra até ser resolvida;
- `optional_after`: a task pode executar após outra, mas não é obrigatória para conclusão.

Regras:

1. Dependências obrigatórias devem ser explícitas.
2. Ciclos de dependência devem ser bloqueados ou convertidos em replanejamento.
3. Dependências devem apontar para `task_id` ou artefato rastreável.
4. Dependência de aprovação deve registrar o que precisa ser aprovado.
5. Uma Task não deve consumir artefato de outra Task sem referência rastreável.
6. O grafo deve permitir identificar tasks elegíveis para execução sequencial inicial e paralelismo futuro.

## Execução sequencial inicial

A execução inicial do Workflow Engine deve ser sequencial por padrão.

Características:

- uma task executável por vez;
- ordem determinada por dependências, prioridade e risco;
- validação incremental após cada task quando aplicável;
- logs por transição e tentativa;
- reavaliação de política antes de tasks sensíveis;
- parada segura ao encontrar bloqueio, falha crítica ou limite excedido.

Regras:

1. Paralelismo deve ser desabilitado por padrão nesta fase.
2. A próxima Task deve ser selecionada apenas entre tasks `ready`.
3. Tasks de maior risco podem exigir validação ou aprovação antes de continuar.
4. Falha de Task obrigatória deve pausar, replanejar, tentar retry permitido ou falhar o Workflow.
5. Conclusão sequencial deve priorizar menor blast radius, menor contexto e validação mais rápida.

## Execução paralela futura

O Workflow Engine deve ser desenhado para suportar paralelismo futuro, mas esta Spec não autoriza implementação concreta de paralelismo.

Pré-condições futuras para paralelismo:

- grafo de dependências válido;
- tasks independentes identificadas;
- isolamento de artefatos ou paths;
- política explícita de concorrência;
- limites de custo, tokens, ciclos e runtime por grupo paralelo;
- controle de conflitos de escrita;
- logs correlacionáveis por task e tentativa;
- avaliação do Guardian Engine para execução concorrente;
- estratégia de merge, validação e encerramento seguro.

Regras arquiteturais:

1. Paralelismo só pode executar Tasks sem dependência obrigatória entre si.
2. Tasks paralelas não devem escrever nos mesmos artefatos sem política de lock ou merge.
3. Orçamento total do Workflow deve limitar a soma das execuções paralelas.
4. Falha de uma Task paralela deve ter política explícita para continuar, pausar ou cancelar o grupo.
5. Execução paralela futura deve preservar a mesma rastreabilidade da execução sequencial.
6. Paralelismo distribuído, multi-runtime ou multi-agente exigirá Spec ou ADR futura.

## Integração com Guardian Engine

O Workflow Engine deve consultar o Guardian Engine nos pontos mínimos:

- após criar o plano inicial em `draft`;
- antes de transicionar workflow para `ready`;
- antes de enfileirar Task sensível;
- antes de replanejar por mudança de escopo;
- antes de ampliar limites, contexto, custo, tokens ou ciclos;
- antes de permitir retry que possa repetir ação sensível;
- antes de marcar workflow como `done` quando houver validação crítica;
- quando política, risco ou contexto mudarem.

Contrato conceitual:

```text
Workflow Engine
↓ workflow or task evaluation request
Guardian Engine
↓ policy decision
Workflow Engine
↓ continue, pause, replan, fail or require approval
```

Regras:

1. Decisão `block` deve impedir avanço do Workflow ou da Task afetada.
2. Decisão `require_approval` deve colocar Workflow ou Task em `paused` ou `blocked`.
3. Decisão `warn` deve registrar aviso e permitir avanço conforme política.
4. Decisão `allow` não elimina validações posteriores.
5. Todas as decisões devem ser anexadas aos logs do Workflow e da Task.
6. O Workflow Engine não deve tentar contornar bloqueios reduzindo informação enviada ao Guardian Engine.

## Integração com Model Selection Engine

O Workflow Engine não escolhe modelos concretos.

Ele deve produzir intenção e política de modelo por Task para que o Model Selection Engine selecione o modelo adequado quando a Task for executada.

Campos mínimos desejados por Task:

- `task_type`;
- `role`;
- `complexity`;
- `quality`;
- `reasoning`;
- `memory`;
- `context_size_estimate`;
- `security`;
- `privacy`;
- `review`;
- `cost`;
- `small_model`;
- `fallback`;
- `budget`;
- `latency`;
- `constraints`.

Regras:

1. O Workflow Engine deve declarar requisitos, não IDs fixos de modelo.
2. Modelo fixo só pode aparecer quando política explícita aprovada exigir, e ainda deve passar pelo Model Selection Engine.
3. Tasks simples devem permitir `small_model: auto` quando compatível com qualidade e risco.
4. Tasks críticas devem declarar revisão obrigatória ou qualidade elevada conforme Guardian Specs.
5. Estimativas de contexto, tokens e custo devem ser atualizadas quando houver replanejamento.
6. Falha de seleção de modelo deve bloquear ou replanejar a Task, não escolher fallback silencioso.

## Integração com Mission Runner

O Mission Runner controla o ciclo de vida operacional da Mission. O Workflow Engine controla o plano de execução da Mission.

Contrato conceitual:

```text
Mission Runner
↓ mission, limits, policies, acceptance criteria
Workflow Engine
↓ workflow plan and task graph
Mission Runner / Task Queue
↓ execution results
Workflow Engine
↓ updated workflow state and closure recommendation
Mission Runner
```

Regras:

1. O Mission Runner deve fornecer Mission normalizada, limites globais, orçamento, políticas e critérios de aceite.
2. O Workflow Engine deve retornar Workflow Plan, Tasks, dependências, limites por Task e critérios de aceite por Task.
3. O Mission Runner mantém responsabilidade por estado global da Mission, orçamento global, logs globais e encerramento final.
4. O Workflow Engine deve reportar progresso, bloqueios, falhas, retries, replanejamentos e recomendação de encerramento.
5. O Workflow Engine não deve marcar Mission como `done`; ele pode recomendar encerramento após Workflow `done`.
6. Cancelamento da Mission deve propagar cancelamento seguro para Workflow e Tasks não concluídas.

## Critérios de aceite por task

Toda Task deve possuir critérios de aceite proporcionais a seu risco e objetivo.

Campos mínimos desejados:

- resultado esperado;
- artefatos esperados;
- validações obrigatórias;
- restrições de segurança;
- restrições de documentação;
- limites de custo, tokens e ciclos;
- condição de pronto;
- condição de falha;
- evidências exigidas.

Uma Task pode ser marcada como `done` somente quando:

1. resultados esperados foram produzidos ou a ausência foi aprovada por política;
2. artefatos esperados existem ou estão referenciados;
3. validações obrigatórias passaram ou foram justificadamente dispensadas por política;
4. limites de custo, tokens, ciclos e tentativas não foram violados;
5. decisões do Guardian Engine foram respeitadas;
6. logs e evidências foram registrados;
7. revisão manual ou cross-review foi concluída quando exigida.

## Logs

O Workflow Engine deve registrar eventos suficientes para auditoria e retomada.

Eventos mínimos de Workflow:

- workflow criado;
- workflow avaliado por política;
- transição de estado;
- plano emitido;
- replanejamento iniciado e concluído;
- task adicionada, alterada, pulada ou cancelada;
- dependência criada ou removida;
- limite aplicado ou excedido;
- orçamento estimado e consumido;
- decisão do Guardian Engine;
- recomendação de encerramento;
- falha, warning ou bloqueio.

Eventos mínimos de Task:

- task criada;
- task ficou `ready`;
- task enfileirada;
- task iniciada;
- task bloqueada;
- task enviada para validação;
- task concluída;
- task falhou;
- retry solicitado;
- retry executado;
- critérios de aceite avaliados;
- artefatos produzidos;
- modelo solicitado ou decisão de modelo referenciada quando disponível.

Regras:

1. Logs não podem conter segredos.
2. Logs devem preferir referências, hashes, caminhos, IDs e metadados.
3. Prompts completos só podem ser registrados quando política permitir.
4. Logs devem ser vinculáveis a `mission_id`, `workflow_id`, `task_id`, `attempt_id`, `cycle_number` e `evaluation_id` quando aplicável.
5. Falha de log deve bloquear encerramento automático de workflows de alto risco.

## Rastreabilidade

O Workflow Engine deve preservar rastreabilidade ponta a ponta.

Relações mínimas:

- Mission para Workflow;
- Workflow para Tasks;
- Task para dependências;
- Task para Specs e Guardian Specs aplicáveis;
- Task para critérios de aceite;
- Task para decisões do Guardian Engine;
- Task para Selection Request e Selection Decision quando disponíveis;
- Task para agente ou capability futura;
- Task para artefatos produzidos;
- Task para validações e resultados;
- Task para logs e tentativas.

Regras:

1. Todo artefato produzido por uma Task deve ser atribuído à Task quando possível.
2. Replanejamento deve manter vínculo com versão anterior do plano.
3. Tasks removidas por replanejamento devem virar `skipped` ou `cancelled`, não desaparecer silenciosamente.
4. IDs devem ser estáveis dentro da execução atual.
5. Rastreabilidade deve funcionar sem depender da memória de agentes.

## Retries

Retries devem ser finitos, explicáveis e governados por política.

Campos mínimos desejados:

- `attempt_count`;
- `max_attempts`;
- `retry_reason`;
- `retryable_error_types`;
- `non_retryable_error_types`;
- `backoff_policy` quando aplicável;
- `requires_revalidation`;
- `requires_guardian_evaluation`;
- `retry_budget`.

Regras:

1. Retry não pode ser infinito.
2. Retry deve consumir limite de ciclos, tentativas, tokens e custo conforme política.
3. Retry de ação sensível deve exigir nova avaliação do Guardian Engine quando risco ou contexto mudar.
4. Retry não deve repetir operação destrutiva sem aprovação explícita.
5. Falha determinística deve preferir replanejamento ou revisão manual em vez de repetição cega.
6. Após exceder `max_attempts`, a Task deve virar `failed` ou `blocked` para revisão manual.
7. Retry bem-sucedido deve preservar logs das tentativas anteriores.

## Limites de custo, tokens e ciclos

O Workflow Engine deve aplicar limites recebidos do Mission Runner e refiná-los por Workflow e Task.

Limites mínimos desejados:

- `max_cycles_per_workflow`;
- `max_cycles_per_task`;
- `max_replans_per_workflow`;
- `max_retries_per_task`;
- `max_validation_failures_per_task`;
- `max_tokens_per_workflow`;
- `max_tokens_per_task`;
- `max_cost_per_workflow`;
- `max_cost_per_task`;
- `max_wall_clock_time_per_workflow`;
- `max_wall_clock_time_per_task`;
- `max_context_size_per_task`;
- `max_parallel_tasks` futuro, default `1`.

Regras:

1. Workflow não deve iniciar sem limites explícitos ou defaults seguros.
2. Limites por Task não podem exceder limites globais da Mission sem aprovação.
3. Soma estimada das Tasks deve caber no orçamento do Workflow e da Mission.
4. Replanejamento não deve resetar orçamento, ciclos ou tentativas consumidas.
5. Ao exceder limite, Workflow deve pausar, falhar ou exigir aprovação conforme política.
6. Otimização de contexto e divisão de escopo devem ser preferidas antes de aumentar orçamento.
7. Limites mais restritivos definidos por Guardian Specs prevalecem.

## Encerramento seguro

O Workflow Engine deve encerrar workflows de forma segura, auditável e recuperável.

Condições para `done`:

- todas as Tasks obrigatórias estão `done` ou foram dispensadas por política registrada;
- critérios de aceite por Task foram avaliados;
- critérios do Workflow foram satisfeitos;
- validações obrigatórias foram executadas ou justificadamente dispensadas;
- decisões do Guardian Engine foram respeitadas;
- limites não foram violados;
- logs e rastreabilidade estão completos o suficiente;
- revisão manual foi concluída quando exigida.

Condições para `failed`:

- Task obrigatória falhou sem retry restante;
- limite crítico foi excedido;
- Guardian Engine emitiu `block` sem alternativa segura;
- validação obrigatória falhou;
- dependência obrigatória ficou irresolúvel;
- logs ou rastreabilidade críticos ficaram indisponíveis em contexto de alto risco.

Condições para `cancelled`:

- Mission foi cancelada;
- usuário ou sistema autorizado cancelou workflow;
- política exigiu encerramento antes da conclusão;
- condição externa tornou execução insegura ou irrelevante.

Regras:

1. Encerramento deve preservar estado de Tasks, tentativas, artefatos, logs e decisões.
2. Encerramento não deve executar rollback destrutivo automaticamente.
3. Tasks `running` devem receber solicitação de parada segura via camada apropriada.
4. Tasks `pending`, `ready` ou `blocked` devem ser canceladas ou marcadas conforme causa.
5. O Workflow Engine deve retornar recomendação clara ao Mission Runner: concluir, falhar, cancelar, pausar ou revisar manualmente.

## Relação futura com Agent Orchestrator

O Workflow Engine deve preparar Tasks para execução por um Agent Orchestrator futuro, sem assumir agentes concretos.

Contrato conceitual futuro:

```text
Workflow Engine
↓ task with required capabilities
Task Queue
↓ eligible task
Agent Orchestrator
↓ agent assignment
Agent / Subagent
↓ execution result
Workflow Engine
```

Campos que devem apoiar o Agent Orchestrator:

- `required_capabilities`;
- `task_type`;
- `risk_level`;
- `model_policy`;
- `context_refs`;
- `allowed_paths`;
- `denied_paths`;
- `validation_policy`;
- `expected_outputs`;
- `acceptance_criteria`;
- `execution_limits`;
- `approval_requirements`.

Regras:

1. Workflow Engine não deve escolher agente concreto quando Agent Orchestrator existir.
2. Workflow Engine deve declarar capabilities e restrições necessárias.
3. Agent Orchestrator deve respeitar dependências, estado e limites definidos pelo Workflow Engine.
4. Agentes não devem conhecer providers, MCPs ou bancos diretamente.
5. Resultado de agente deve voltar como evidência associada à Task.
6. Divergências futuras entre Workflow Engine, Task Queue e Agent Orchestrator devem gerar ADR.

## Integração com Task Queue

A Task Queue é a camada responsável por organizar Tasks elegíveis para execução.

Contrato conceitual:

```text
Workflow Engine
↓ tasks and dependency graph
Task Queue
↓ status and execution results
Workflow Engine
```

Regras:

1. Workflow Engine define dependências, elegibilidade e limites.
2. Task Queue controla enfileiramento, locks, prioridade e estado operacional da fila.
3. Task Queue não deve alterar critérios de aceite ou dependências sem replanejamento registrado.
4. Execução concorrente deve permanecer desabilitada por padrão até política futura.
5. Falha de persistência da fila deve impedir execução de workflows de alto risco.

## Validação do Workflow Plan

Antes de um Workflow sair de `draft`, o plano deve ser validado.

Validações mínimas:

- Mission vinculada existe e está autorizada para planejamento;
- Tasks possuem objetivo, entrada, saída e critérios de aceite;
- dependências obrigatórias são resolvíveis;
- grafo não possui ciclos não controlados;
- limites existem por Workflow e Task;
- orçamento estimado cabe nos limites da Mission;
- Tasks de implementação referenciam Spec aprovada;
- Tasks sensíveis possuem política de aprovação;
- contexto necessário está referenciado, não duplicado indevidamente;
- Guardian Engine emitiu decisão compatível.

Regras:

1. Plano inválido deve permanecer `draft`, virar `failed` ou exigir revisão manual.
2. Plano parcialmente válido não deve executar Tasks obrigatórias ambíguas.
3. Validação deve gerar logs explicáveis.
4. Falha de validação deve sugerir alternativa segura quando possível.

## Erros e degradação segura

O Workflow Engine deve produzir erros claros para:

- Mission inválida ou ambígua;
- Spec ausente ou não aprovada para implementação;
- critérios de aceite ausentes;
- dependência cíclica;
- dependência irresolúvel;
- orçamento insuficiente;
- limite de ciclos excedido;
- limite de tokens excedido;
- limite de custo excedido;
- Guardian Engine bloqueou plano ou Task;
- Model Selection Engine não encontrou modelo compatível;
- Task falhou sem retry restante;
- validação obrigatória reprovada;
- conflito de artefatos ou paths;
- contexto sensível sem política adequada;
- replanejamento excedeu limite;
- Task Queue indisponível;
- Agent Orchestrator futuro indisponível quando obrigatório.

Quando possível, o erro deve sugerir alternativa segura, como dividir a missão, reduzir escopo, adicionar critério de aceite, corrigir dependência, solicitar aprovação, reduzir contexto, ajustar orçamento, replanejar ou encaminhar para revisão manual.

## Relação com Guardian Specs

### Security by Design

O Workflow Engine deve identificar tasks sensíveis, restringir contexto, evitar vazamento de segredos em logs, exigir aprovação para ações arriscadas e bloquear planos que dependam de `sudo`, alteração global ou operação destrutiva não autorizada.

### Token Efficiency

O Workflow Engine deve decompor missões para reduzir contexto, referenciar artefatos em vez de copiar conteúdo extenso, limitar ciclos e evitar tasks redundantes.

### AI Quality Assurance

O Workflow Engine deve exigir critérios de aceite por task, validação proporcional ao risco, revisão manual ou cross-review quando política exigir e condição de parada explícita.

### Cost Optimization

O Workflow Engine deve estimar custo por Workflow e Task, respeitar orçamento, preferir decomposição incremental e impedir paralelismo futuro sem orçamento agregado.

### Architecture Governance

O Workflow Engine deve preservar fronteiras entre Mission Runner, Guardian Engine, Model Selection Engine, Task Queue, Agent Orchestrator e Runtime Adapters.

### Documentation Governance

Replanejamentos relevantes, mudanças de escopo, decisões arquiteturais e falhas recorrentes devem gerar logs, decision notes, Specs ou ADRs conforme impacto.

### Testing Governance

Tasks que alterem código devem incluir validação aplicável ou justificativa registrada. Falha de validação deve impedir conclusão automática.

### Compliance Governance

Tasks que tratem dados sensíveis, providers externos, retenção de logs ou requisitos regulatórios devem herdar políticas de compliance aplicáveis.

### Observability Governance

O Workflow Engine deve emitir eventos estruturados de planejamento, estado, dependência, task, retry, replanejamento, custo, tokens, validação, erro e encerramento.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Decomposição gerar tasks grandes demais | Exigir objetivo, saída e critérios de aceite por task. |
| Decomposição gerar tasks excessivas | Aplicar Token Efficiency e evitar redundância. |
| Loops infinitos de replanejamento | Limitar ciclos, retries e `max_replans`. |
| Paralelismo causar conflitos | Desabilitar paralelismo por padrão e exigir Spec ou ADR futura. |
| Task sem validação virar concluída | Exigir critérios de aceite avaliados antes de `done`. |
| Bypass do Guardian Engine | Tornar avaliação obrigatória para plano, tasks sensíveis e replanejamentos. |
| Modelo hardcoded no workflow | Workflow declara política; Model Selection Engine decide modelo. |
| Perda de rastreabilidade após replanejamento | Preservar versões, tasks antigas, logs e vínculos. |
| Custo inesperado por muitas tasks | Estimar orçamento agregado e verificar limites por task e workflow. |
| Acoplamento ao OpenCode ou agentes concretos | Usar Runtime Adapter, capabilities e Agent Orchestrator futuro. |
| Cancelamento deixar execução inconsistente | Encerramento seguro com parada de tasks e preservação de estado. |

## Decisões aprovadas por esta Spec

1. Workflow Engine é componente arquitetural próprio do framework.
2. Workflow Engine transforma Mission em Workflow Plan composto por Tasks.
3. Workflow Engine não executa comandos, agentes, tools, MCPs, providers ou bancos diretamente.
4. Workflow Engine deve definir estados explícitos de Workflow e Task.
5. Tasks devem ter critérios de aceite próprios.
6. Dependências entre Tasks devem ser explícitas e rastreáveis.
7. Execução inicial deve ser sequencial por padrão.
8. Paralelismo futuro deve depender de dependências, isolamento, política, orçamento e avaliação do Guardian Engine.
9. Workflow Engine deve consultar Guardian Engine para plano, tasks sensíveis e replanejamentos.
10. Workflow Engine deve produzir políticas de seleção por Task, mas não escolher modelo concreto.
11. Workflow Engine deve integrar Mission Runner sem assumir seu papel de encerramento global da Mission.
12. Replanejamento não reseta histórico, ciclos, orçamento ou tentativas.
13. Retries devem ser finitos, auditáveis e governados por política.
14. Logs e rastreabilidade são obrigatórios por Mission, Workflow, Task, tentativa e decisão.
15. Encerramento seguro deve preservar estado, logs, artefatos e evidências.
16. Relação futura com Agent Orchestrator deve ser baseada em capabilities, não em agentes hardcoded.

## Estado implementado e validado em 0108

O caminho integrado mínimo é `WorkflowEngine.execute_with_queue()`, implementado em `src/vercosa_ai_framework/workflows/engine.py`. Esse caminho constrói e acompanha o Workflow, mapeia `WorkflowTask` para Task Queue por `src/vercosa_ai_framework/workflows/task_mapping.py` e delega execução operacional ao Task Scheduler.

Evidências:

- `tests/test_mission_workflow_task_integration.py` valida execução de tasks dependentes, retry de task obrigatória e bloqueio de dependente.
- `tests/test_task_agent_capability_integration.py` valida o uso de executor de task injetado para alcançar Agent Orchestrator.
- `tests/test_agent_execution_governance_0107.py` valida `execute_with_queue()` no fluxo governado 0107.

O método legado `WorkflowEngine.execute()` permanece suportado como compatibilidade transitória no estado atual e não deve ser removido nesta missão. A remoção ou promoção de `execute_with_queue()` como caminho canônico exclusivo permanece decisão pendente em `docs/alignment/open-questions.md`.

## Critérios de aceite

- Existe uma Spec própria para o Workflow Engine em `specs/framework/0006-workflow-engine.md`.
- A Spec define a relação `Mission -> Workflow -> Task`.
- A Spec define decomposição de missão em tarefas.
- A Spec define estados de workflow.
- A Spec define estados de task.
- A Spec define dependências entre tarefas.
- A Spec define execução sequencial inicial.
- A Spec contempla execução paralela futura.
- A Spec define integração com Guardian Engine.
- A Spec define integração com Model Selection Engine.
- A Spec define integração com Mission Runner.
- A Spec define critérios de aceite por task.
- A Spec define logs.
- A Spec define rastreabilidade.
- A Spec define retries.
- A Spec define limites de custo, tokens e ciclos.
- A Spec define encerramento seguro.
- A Spec define relação futura com Agent Orchestrator.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir schema persistente final de Workflow, Task, tentativa e dependência.
- Definir formato final do `Workflow Plan`.
- Definir contrato formal entre Mission Orchestrator e Workflow Engine.
- Definir contrato formal entre Workflow Engine e Task Queue.
- Definir contrato formal entre Workflow Engine e Agent Orchestrator.
- Definir política padrão de granularidade de tasks por tipo de missão.
- Definir defaults numéricos para custo, tokens, ciclos, retries e replanejamentos.
- Definir estratégia de versionamento de workflows após replanejamento.
- Definir formato de logs estruturados por workflow e task.
- Definir política de paralelismo futuro e locks de artefatos.
- Definir matriz de capabilities por tipo de task.
- Definir ADR se a fronteira entre Workflow Engine, Mission Orchestrator e Task Queue mudar.

# Spec 0007 — Task Queue

## Status

Proposta.

## Objetivo

Definir a Task Queue interna do Vercosa AI Framework como o componente operacional do Workflow Engine responsável por organizar, priorizar, persistir e despachar Tasks de um Workflow de forma determinística, rastreável, governada por políticas e preparada para execução sequencial inicial e paralelismo futuro.

A Task Queue deve preservar a separação arquitetural entre Mission Queue, Workflow Engine, Guardian Engine, Runtime Adapter e futuro Agent Orchestrator, sem acoplar o núcleo do framework a runtime, provider, modelo, sistema operacional, banco de dados, agente ou ferramenta específica.

## Contexto

O Vercosa AI Framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design.

As Specs 0001, 0003, 0004, 0005 e 0006 estabelecem que:

- missões são intenções de alto nível fornecidas por usuário, sistema, API ou outro componente autorizado;
- o Mission Runner controla fila de missões, estado global, limites globais, orçamento, logs e encerramento de missões;
- o Workflow Engine transforma uma Mission em Workflow Plan composto por Tasks rastreáveis;
- a Task Queue organiza Tasks, dependências, prioridade, paralelismo e estado operacional;
- o Guardian Engine avalia missões, planos, tasks e ações sensíveis antes e durante execução;
- Runtime Adapters executam intenções já governadas em runtimes concretos;
- execução inicial deve ser sequencial;
- paralelismo futuro deve ser explícito, governado, auditável e seguro;
- agentes não devem conhecer providers, MCPs, APIs ou bancos diretamente.

A Task Queue existe para tornar a execução de Tasks controlável e recuperável. Ela não substitui o Workflow Engine, não substitui o Mission Runner, não aprova políticas, não decide modelos, não executa comandos por conta própria e não escolhe agentes concretos.

## Escopo

Esta Spec cobre:

- diferença entre Mission Queue e Task Queue;
- Task Queue como componente interno do Workflow Engine;
- estados de task: `queued`, `running`, `done`, `failed`, `blocked`, `skipped`, `cancelled`;
- prioridade;
- dependências;
- retries;
- backoff;
- limite de tentativas;
- ordenação determinística;
- execução sequencial inicial;
- execução paralela futura;
- integração com Guardian Engine;
- integração com Runtime Adapter;
- integração futura com Agent Orchestrator;
- logs;
- rastreabilidade;
- persistência local inicial;
- provider agnostic;
- segurança e limites;
- riscos, mitigações, decisões e critérios de aceite.

Esta Spec não cobre:

- implementação concreta em código;
- criação de CLI, API, daemon, worker, serviço `systemd` ou scheduler real;
- alteração de configurações globais;
- uso de `sudo`;
- schema final de banco de dados;
- engine final de paralelismo distribuído;
- implementação final do Agent Orchestrator;
- seleção concreta de modelos;
- execução direta de agents, tools, MCPs, comandos, providers ou bancos;
- política final de locks distribuídos.

## Princípios

1. A Task Queue é uma fila operacional de Tasks, não uma fila de Missions.
2. A Task Queue pertence ao ciclo interno do Workflow Engine.
3. Uma Task só pode ser enfileirada quando pertencer a um Workflow validado ou a um replanejamento autorizado.
4. Ordem de execução deve ser determinística para reprodutibilidade e auditoria.
5. Execução inicial deve ser sequencial por padrão, com `max_parallel_tasks: 1`.
6. Paralelismo futuro deve depender de dependências, locks, isolamento, orçamento, política e avaliação do Guardian Engine.
7. Estados, tentativas, decisões e artefatos não podem depender da memória de agentes.
8. Retries devem ser finitos, explicáveis e governados por política.
9. Logs devem ser suficientes para auditoria e retomada, sem expor segredos.
10. A Task Queue deve ser provider agnostic, runtime agnostic e agent agnostic.

## Posição arquitetural

A Task Queue fica dentro da fronteira operacional do Workflow Engine, entre o Workflow Plan e a execução por Runtime Adapter ou futuro Agent Orchestrator.

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
Runtime Adapter inicial
↓
runtime concreto
```

Fluxo futuro com Agent Orchestrator:

```text
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Agents / Subagents
↓
Capabilities
↓
Skills
↓
Tools
↓
Providers / MCPs / APIs
```

Regras:

1. O Workflow Engine pode possuir uma Task Queue interna no MVP.
2. A Task Queue pode evoluir para módulo próprio, desde que preserve o contrato com o Workflow Engine.
3. A Task Queue não deve chamar providers diretamente.
4. A Task Queue não deve conhecer detalhes internos do OpenCode ou de outro runtime.
5. A Task Queue não deve assumir sistema operacional, arquitetura, banco, modelo ou provider específico.

## Mission Queue vs Task Queue

### Mission Queue

A Mission Queue é a fila de missões controlada pelo Mission Runner.

Responsabilidades:

- receber missões de alto nível;
- preservar ordem, prioridade e estado de missões;
- aplicar limites globais da missão;
- controlar orçamento global, ciclos e encerramento;
- decidir quando uma missão pode ser planejada ou executada;
- registrar logs globais da missão;
- sobreviver a falhas do processo quando possível;
- impedir execução concorrente de missões quando política não permitir.

Exemplos de estados de Mission pertencem ao Mission Runner, não à Task Queue.

### Task Queue

A Task Queue é a fila de Tasks pertencentes a um Workflow.

Responsabilidades:

- receber Tasks emitidas pelo Workflow Engine;
- persistir estado operacional das Tasks;
- calcular elegibilidade por dependências;
- ordenar Tasks elegíveis por prioridade e critérios determinísticos;
- controlar transições operacionais de Task;
- controlar tentativas, retries, backoff e limites por Task;
- despachar uma Task por vez na execução sequencial inicial;
- registrar logs e eventos por Task, tentativa e decisão;
- reportar resultados ao Workflow Engine;
- preparar metadados para Runtime Adapter inicial ou Agent Orchestrator futuro.

### Diferenças obrigatórias

| Aspecto | Mission Queue | Task Queue |
| --- | --- | --- |
| Dono | Mission Runner | Workflow Engine |
| Unidade | Mission | Task |
| Escopo | Global da missão | Interno ao Workflow |
| Responsabilidade | Orquestrar ciclo de vida da missão | Organizar execução de Tasks |
| Estado final | Conclusão, falha ou cancelamento da missão | Resultado operacional de cada Task |
| Planejamento | Delegado ao Workflow Engine | Não planeja, apenas agenda Tasks planejadas |
| Políticas | Limites globais e decisão de execução | Limites por Task e elegibilidade |
| Persistência inicial | Fila local de missões | Estado local de Tasks do Workflow |
| Paralelismo | Entre missões, futuro e governado | Entre Tasks independentes, futuro e governado |

Regras:

1. Uma Mission Queue pode conter várias Missions; uma Task Queue deve operar dentro de um Workflow específico ou de um conjunto claramente vinculado a um `workflow_id`.
2. A Task Queue não deve marcar Mission como `done`, `failed` ou `cancelled`.
3. A Mission Queue não deve manipular diretamente dependências internas de Tasks sem passar pelo Workflow Engine.
4. Cancelamento de Mission deve propagar cancelamento seguro para Task Queue via Workflow Engine.
5. Repriorização global de Mission não deve alterar ordem interna de Tasks sem replanejamento ou política registrada.

## Definições

### Task Queue

Componente interno do Workflow Engine responsável pelo estado operacional de Tasks planejadas.

Campos mínimos desejados:

- `queue_id`;
- `workflow_id`;
- `mission_id`;
- `status`;
- `execution_mode`;
- `max_parallel_tasks`;
- `ordering_policy`;
- `retry_policy`;
- `backoff_policy`;
- `persistence_ref`;
- `audit_log_ref`;
- `created_at`;
- `updated_at`.

### Queue Item

Representação operacional de uma Task dentro da Task Queue.

Campos mínimos desejados:

- `queue_item_id`;
- `task_id`;
- `workflow_id`;
- `mission_id`;
- `status`;
- `priority`;
- `dependencies`;
- `blocked_by`;
- `attempt_count`;
- `max_attempts`;
- `next_attempt_at`;
- `backoff_policy`;
- `last_error`;
- `lock_ref` quando houver;
- `guardian_decision_refs`;
- `runtime_request_ref` quando houver;
- `agent_assignment_ref` futuro;
- `created_at`;
- `queued_at`;
- `started_at`;
- `finished_at`;
- `updated_at`;
- `audit_log_ref`.

### Attempt

Uma Attempt é uma tentativa rastreável de executar uma Task.

Campos mínimos desejados:

- `attempt_id`;
- `task_id`;
- `workflow_id`;
- `mission_id`;
- `attempt_number`;
- `status`;
- `started_at`;
- `finished_at`;
- `guardian_decision_ref`;
- `runtime_request_ref`;
- `runtime_result_ref`;
- `error_type`;
- `error_message`;
- `retry_decision`;
- `cost_used` quando disponível;
- `tokens_used` quando disponível;
- `audit_log_ref`.

## Estados de task na Task Queue

Estados mínimos obrigatórios da Task Queue:

- `queued`: task aceita pela fila e aguardando elegibilidade, prioridade ou slot de execução;
- `running`: task despachada para execução e ainda sem resultado final;
- `done`: task concluída e aceita conforme resultado e validação aplicável;
- `failed`: task falhou por erro, validação reprovada, limite excedido ou ausência de retry permitido;
- `blocked`: task impedida por dependência, política, aprovação, recurso, lock ou decisão externa;
- `skipped`: task não executada por replanejamento, dependência dispensada ou decisão registrada;
- `cancelled`: task cancelada por usuário, sistema, política ou encerramento do Workflow/Mission.

Mapeamento com estados de `WorkflowTask` da Spec 0006:

| Task Queue | WorkflowTask |
| --- | --- |
| `queued` | `pending` ou `ready` |
| `running` | `running` ou `validating` |
| `done` | `done` |
| `failed` | `failed` |
| `blocked` | `blocked` |
| `skipped` | `skipped` |
| `cancelled` | `cancelled` |

Transições permitidas:

```text
queued -> running
queued -> blocked
queued -> skipped
queued -> cancelled
running -> done
running -> failed
running -> blocked
running -> cancelled
failed -> queued
failed -> blocked
blocked -> queued
blocked -> failed
blocked -> skipped
blocked -> cancelled
```

Regras:

1. `done`, `skipped` e `cancelled` são terminais para o Queue Item atual.
2. Retry deve criar nova Attempt e pode recolocar o item em `queued` se houver tentativa restante.
3. `failed -> queued` só é permitido quando a política de retry autorizar.
4. `blocked -> queued` exige que a causa do bloqueio tenha sido resolvida ou dispensada por política.
5. `skipped` exige justificativa e referência ao replanejamento, política ou decisão que dispensou a Task.
6. `cancelled` deve preservar motivo, autor, timestamp e escopo do cancelamento quando disponível.
7. Toda transição deve gerar evento estruturado.

## Prioridade

A Task Queue deve usar prioridade como um dos critérios de ordenação, não como substituto de dependências ou política.

Campos mínimos desejados:

- `priority`: número inteiro estável;
- `priority_reason`: justificativa opcional;
- `priority_source`: `workflow_plan`, `guardian_policy`, `manual_override` ou `replan`;
- `priority_updated_at`.

Regras:

1. Menor valor numérico deve representar maior prioridade, salvo política explícita diferente.
2. Dependências obrigatórias sempre prevalecem sobre prioridade.
3. Tasks bloqueadas não devem ser selecionadas por prioridade.
4. Repriorização deve ser registrada em log.
5. Repriorização manual deve exigir autorização quando afetar Task sensível, ordem de validação ou risco.
6. A prioridade não deve ser usada para contornar Guardian Engine.
7. Empates devem ser resolvidos por ordenação determinística.

## Dependências

A Task Queue deve respeitar dependências definidas pelo Workflow Engine. Ela pode calcular elegibilidade operacional, mas não deve alterar o grafo de dependências sem replanejamento.

Tipos mínimos herdados da Spec 0006:

- `requires_completion`;
- `requires_artifact`;
- `requires_validation`;
- `requires_approval`;
- `blocks`;
- `optional_after`.

Regras:

1. Tasks com dependência obrigatória não satisfeita permanecem `queued` ou `blocked`, conforme política.
2. Dependência falhada deve bloquear, pular ou falhar Tasks descendentes conforme política do Workflow.
3. Dependência opcional pode influenciar ordenação, mas não deve impedir execução obrigatória.
4. Ciclos detectados pela Task Queue devem bloquear execução e reportar erro ao Workflow Engine.
5. Dependências devem apontar para `task_id`, `artifact_ref`, `approval_ref` ou referência rastreável.
6. A Task Queue deve permitir identificar o conjunto futuro de Tasks independentes para paralelismo.
7. Dependência de artefato deve registrar o artefato esperado e a Task produtora.

## Ordenação determinística

A seleção da próxima Task deve ser reproduzível com o mesmo estado de fila, política e relógio lógico.

Ordem mínima recomendada para execução sequencial:

1. Filtrar Tasks em `queued`.
2. Remover Tasks com dependências obrigatórias não satisfeitas.
3. Remover Tasks com `next_attempt_at` futuro.
4. Remover Tasks bloqueadas por Guardian Engine, aprovação, lock ou limite.
5. Ordenar por `priority` ascendente.
6. Ordenar por profundidade/topologia do grafo de dependências.
7. Ordenar por `created_at` ascendente.
8. Ordenar por `task_id` lexicográfico.

Regras:

1. O algoritmo de ordenação deve ser documentado e versionado.
2. Empates não devem depender da ordem nativa de dicionários, filesystem ou runtime.
3. Mudanças de política de ordenação devem gerar log e podem exigir ADR se afetarem reprodutibilidade.
4. Ordenação deve ser estável dentro de uma execução, exceto quando houver replanejamento registrado.
5. Tasks sensíveis podem exigir avaliação do Guardian Engine antes de serem selecionadas, mesmo se forem as próximas pela ordem.

## Execução sequencial inicial

A Task Queue deve executar sequencialmente por padrão.

Características:

- `execution_mode: sequential`;
- `max_parallel_tasks: 1`;
- uma Task `running` por Workflow;
- validação incremental quando aplicável;
- persistência de estado antes e depois de cada transição;
- avaliação do Guardian Engine antes de Task sensível ou retry sensível;
- parada segura em bloqueio, falha crítica, limite excedido ou decisão `block`.

Regras:

1. Nenhuma Task deve ser despachada se já existir Task `running` no mesmo Workflow, salvo política futura explícita.
2. A próxima Task deve ser selecionada apenas entre Tasks elegíveis.
3. A fila deve persistir a transição para `running` antes de chamar a camada de execução.
4. Resultado de execução deve ser persistido antes de selecionar a próxima Task.
5. Falha de persistência deve impedir execução automática de Workflows de alto risco.
6. Cancelamento deve impedir novo despacho e solicitar parada segura para Task `running` via camada apropriada.

## Execução paralela futura

A arquitetura da Task Queue deve permitir paralelismo futuro, mas esta Spec não autoriza implementação concreta de paralelismo.

Pré-condições futuras:

- grafo de dependências válido e acíclico ou ciclos controlados por replanejamento;
- Tasks independentes identificadas;
- `max_parallel_tasks` maior que `1` por política explícita;
- isolamento de artefatos, paths e recursos;
- locks ou estratégia de merge para artefatos compartilhados;
- orçamento agregado suficiente;
- limites de tokens, custo, tempo e ciclos por grupo paralelo;
- avaliação do Guardian Engine para concorrência;
- logs correlacionáveis por Task, Attempt e worker;
- estratégia de cancelamento e encerramento seguro.

Regras futuras:

1. Tasks paralelas não podem ter dependência obrigatória entre si.
2. Tasks paralelas não devem escrever nos mesmos artefatos sem lock ou política de merge.
3. Falha de uma Task paralela deve ter política explícita: continuar, pausar grupo, cancelar grupo ou replanejar.
4. Orçamento do Workflow deve limitar a soma das execuções paralelas.
5. Paralelismo não deve reduzir rastreabilidade, validação ou logging.
6. Paralelismo distribuído, multi-runtime ou multi-agent exige Spec ou ADR futura.

## Retries

Retries devem ser finitos, auditáveis e governados por política.

Campos mínimos desejados:

- `attempt_count`;
- `max_attempts`;
- `retry_reason`;
- `retryable_error_types`;
- `non_retryable_error_types`;
- `requires_guardian_evaluation`;
- `requires_revalidation`;
- `retry_budget`;
- `next_attempt_at`;
- `backoff_policy`.

Regras:

1. `max_attempts` deve ter default seguro, inicialmente `1` quando política não definir outro valor.
2. Retry não pode ser infinito.
3. Retry deve consumir limites de tentativas, ciclos, tempo, tokens e custo conforme aplicável.
4. Retry de erro determinístico deve preferir bloqueio, replanejamento ou revisão manual em vez de repetição cega.
5. Retry de operação sensível deve exigir nova avaliação do Guardian Engine quando risco, contexto, alvo ou tentativa mudar.
6. Retry não deve repetir operação destrutiva sem aprovação explícita.
7. Ao exceder `max_attempts`, a Task deve virar `failed` ou `blocked` para revisão manual conforme política.
8. Todas as Attempts anteriores devem permanecer preservadas.

## Backoff

Backoff define quando uma Task falhada pode tentar novamente.

Políticas mínimas suportadas conceitualmente:

- `none`: retry imediato quando seguro;
- `fixed`: atraso fixo entre tentativas;
- `exponential`: atraso crescente por tentativa;
- `manual`: retry depende de intervenção ou aprovação;
- `policy_defined`: Guardian Engine ou política específica define atraso.

Campos mínimos desejados:

- `backoff_type`;
- `initial_delay_seconds`;
- `max_delay_seconds`;
- `multiplier`;
- `jitter_enabled` futuro;
- `next_attempt_at`;
- `backoff_reason`.

Regras:

1. Backoff não deve ser usado para contornar `max_attempts`.
2. Backoff deve ser calculado de forma determinística quando `jitter_enabled` for falso.
3. Jitter futuro deve ser registrado porque reduz reprodutibilidade exata.
4. Backoff manual deve colocar a Task em `blocked` ou mantê-la inelegível até aprovação.
5. Backoff deve respeitar limites globais de tempo do Workflow e da Mission.
6. Se `next_attempt_at` exceder o limite do Workflow, a Task deve bloquear, falhar ou exigir revisão.

## Integração com Guardian Engine

A Task Queue deve consultar ou receber decisões do Guardian Engine por meio do Workflow Engine ou contrato aprovado. Ela não deve contornar política.

Pontos mínimos de avaliação:

- antes de aceitar Tasks de um Workflow Plan avaliado como pronto;
- antes de despachar Task sensível;
- antes de retry de Task sensível;
- antes de pular Task obrigatória;
- antes de cancelar grupo de Tasks quando houver impacto relevante;
- antes de paralelismo futuro;
- quando contexto, alvo, limite, risco ou política mudar.

Contrato conceitual:

```text
Task Queue
↓ task execution eligibility context
Guardian Engine
↓ allow, warn, require_approval or block
Task Queue
↓ queue, run, block, fail, skip or require review
```

Regras:

1. Decisão `block` deve impedir despacho da Task afetada.
2. Decisão `require_approval` deve colocar a Task em `blocked` ou manter inelegível até aprovação.
3. Decisão `warn` deve gerar log e permitir continuidade apenas se a política permitir.
4. Decisão `allow` não dispensa validação posterior.
5. Decisões devem ser anexadas ao Queue Item e à Attempt quando aplicável.
6. A Task Queue não deve reduzir contexto enviado ao Guardian Engine para obter aprovação.
7. Falha de avaliação do Guardian Engine deve bloquear execução automática quando a Task for sensível ou o Workflow for de alto risco.

## Integração com Runtime Adapter

Na fase inicial, a Task Queue pode despachar Tasks para execução por Runtime Adapter por meio do Workflow Engine ou contrato interno equivalente.

Contrato conceitual inicial:

```text
Task Queue
↓ eligible task with limits, context refs and policies
Runtime Adapter
↓ execution result, artifacts, logs, errors and metadata
Task Queue
↓ update state and report to Workflow Engine
```

Regras:

1. Runtime Adapter executa uma intenção governada; ele não deve planejar Tasks.
2. Task Queue deve enviar somente contexto necessário por referência sempre que possível.
3. Task Queue deve enviar `mission_id`, `workflow_id`, `task_id` e `attempt_id` quando disponível.
4. Task Queue deve enviar limites, políticas de log e restrições de paths aplicáveis.
5. Runtime Adapter deve retornar resultado normalizado, artefatos, validações, erros e referência de log.
6. Falha do Runtime Adapter deve virar erro de Attempt, não perda de estado da fila.
7. A Task Queue não deve chamar OpenCode diretamente; deve falar com o contrato de Runtime Adapter.
8. Fallback entre runtimes deve preservar política, decisões, limites, logs e rastreabilidade.

## Integração futura com Agent Orchestrator

Quando o Agent Orchestrator existir, a Task Queue deve despachar Tasks elegíveis para ele em vez de escolher agentes diretamente.

Contrato conceitual futuro:

```text
Task Queue
↓ eligible task with required capabilities
Agent Orchestrator
↓ agent assignment and execution coordination
Agent / Subagent
↓ result and evidence
Task Queue
↓ state update and traceability
```

Campos que devem apoiar o Agent Orchestrator:

- `required_capabilities`;
- `task_type`;
- `risk_level`;
- `model_policy`;
- `context_refs`;
- `allowed_paths`;
- `denied_paths`;
- `execution_limits`;
- `validation_policy`;
- `approval_requirements`;
- `attempt_id`;
- `audit_log_ref`.

Regras:

1. Task Queue não deve escolher agente concreto.
2. Agent Orchestrator deve respeitar estado, dependências, prioridade e limites da Task Queue.
3. Agentes não devem conhecer providers, MCPs, APIs ou bancos diretamente.
4. Resultado de agente deve voltar como evidência associada à Task e Attempt.
5. Agent Orchestrator indisponível deve bloquear Tasks que dependam dele, não acionar provider alternativo diretamente.
6. Divergências de fronteira entre Task Queue e Agent Orchestrator devem gerar ADR.

## Logs

A Task Queue deve registrar eventos estruturados suficientes para auditoria, diagnóstico, retomada e reprodução.

Eventos mínimos:

- Queue criada;
- Queue carregada de persistência;
- Task enfileirada;
- Task tornou-se elegível;
- Task bloqueada;
- Task desbloqueada;
- Task selecionada para execução;
- Attempt criada;
- Attempt iniciada;
- decisão do Guardian Engine recebida;
- Runtime Adapter acionado;
- resultado recebido;
- Task concluída;
- Task falhou;
- retry agendado;
- backoff calculado;
- limite excedido;
- Task pulada;
- Task cancelada;
- dependência satisfeita;
- dependência falhou;
- erro de persistência;
- encerramento da Queue.

Campos mínimos por evento:

- `event_id`;
- `event_type`;
- `mission_id`;
- `workflow_id`;
- `queue_id`;
- `task_id` quando aplicável;
- `attempt_id` quando aplicável;
- `previous_status` quando aplicável;
- `new_status` quando aplicável;
- `timestamp`;
- `reason`;
- `policy_refs`;
- `guardian_decision_ref` quando aplicável;
- `runtime_result_ref` quando aplicável;
- `artifact_refs` quando aplicável.

Regras:

1. Logs não podem conter segredos.
2. Logs devem preferir referências, hashes, paths, IDs e metadados.
3. Prompts completos só podem ser registrados quando política permitir.
4. Logs devem ser append-only quando possível.
5. Falha de log deve impedir encerramento automático de Workflows de alto risco.
6. Logs devem permitir reconstruir a sequência de seleção e execução de Tasks.

## Rastreabilidade

A Task Queue deve preservar rastreabilidade ponta a ponta entre Mission, Workflow, Task, Attempt, decisão, execução, artefato e validação.

Relações mínimas:

- Mission para Workflow;
- Workflow para Task Queue;
- Task Queue para Queue Items;
- Queue Item para Task planejada;
- Queue Item para dependências;
- Queue Item para Attempts;
- Attempt para decisão do Guardian Engine;
- Attempt para Runtime Request e Runtime Result;
- Attempt para Agent Assignment futuro;
- Task para artefatos produzidos;
- Task para validações;
- Task para logs;
- Task para retries e backoff.

Regras:

1. IDs devem ser estáveis dentro da execução atual.
2. Replanejamento deve versionar ou preservar vínculo com Queue Items anteriores.
3. Tasks removidas por replanejamento devem virar `skipped` ou `cancelled`, não desaparecer silenciosamente.
4. Artefatos devem ser referenciados por path, hash, ID ou outro identificador rastreável.
5. Rastreabilidade deve funcionar sem depender de memória de agentes ou logs de runtime externo.
6. Estado persistido deve ser suficiente para diagnóstico pós-falha.

## Persistência local inicial

A persistência inicial da Task Queue deve ser local, simples, auditável e provider agnostic.

Opções aceitáveis conceitualmente:

- arquivos estruturados em workspace controlado;
- SQLite local;
- outro storage local simples aprovado por Spec futura.

Requisitos mínimos:

- persistir Queue, Queue Items, Attempts e eventos essenciais;
- sobreviver a reinício do processo quando possível;
- evitar segredos em texto claro;
- usar escrita atômica ou estratégia equivalente quando possível;
- permitir leitura humana ou exportação para auditoria;
- preservar timestamps e IDs;
- não depender de PostgreSQL, pgvector, Ollama, OpenCode, Docker, systemd ou arquitetura específica.

Regras:

1. O formato persistente final não é definido por esta Spec.
2. Persistência local inicial não deve exigir serviço externo.
3. Falha de persistência deve bloquear execução automática de Tasks de alto risco.
4. Dados sensíveis devem ser omitidos, mascarados ou referenciados conforme política.
5. Migração futura para banco local ou remoto deve preservar contrato lógico e rastreabilidade.
6. Arquivos de persistência devem respeitar políticas de paths permitidos do projeto.

## Provider Agnostic

A Task Queue deve depender de contratos do framework, não de implementações concretas.

Regras:

1. Não deve haver dependência arquitetural de OpenCode.
2. Não deve haver dependência arquitetural de OpenAI, Anthropic, Ollama ou qualquer modelo específico.
3. Não deve haver dependência obrigatória de PostgreSQL, pgvector, SQLite, Redis, Docker, systemd ou cloud provider.
4. Não deve haver dependência obrigatória de Linux, ARM64, x86_64, macOS ou Windows.
5. Runtime concreto deve ser acessado via Runtime Adapter.
6. Agent execução futura deve passar pelo Agent Orchestrator.
7. Capabilities devem ser declaradas por abstração, não por tool concreta.

## Segurança e limites

A Task Queue deve aplicar limites operacionais antes de despachar qualquer Task.

Limites mínimos desejados:

- `max_attempts_per_task`;
- `max_retries_per_task`;
- `max_running_tasks_per_workflow`, inicial `1`;
- `max_wall_clock_time_per_task`;
- `max_wall_clock_time_per_workflow`;
- `max_tokens_per_task` quando disponível;
- `max_cost_per_task` quando disponível;
- `max_context_size_per_task`;
- `max_queue_items_per_workflow`;
- `max_backoff_delay_seconds`;
- `allowed_paths`;
- `denied_paths`;
- `allow_network`;
- `allow_external_provider`;
- `allow_destructive_operations`.

Regras:

1. Execução sem limites explícitos ou defaults seguros deve ser bloqueada.
2. `sudo` deve ser bloqueado por padrão.
3. Operações destrutivas devem exigir política explícita e aprovação quando aplicável.
4. Acesso a `.env`, secrets, credenciais e arquivos sensíveis deve ser bloqueado ou exigir aprovação conforme política.
5. Providers externos não devem receber dados sensíveis sem política permissiva explícita.
6. Logs devem mascarar segredos e evitar prompts completos por padrão.
7. Cancelamento deve ser seguro e não deve executar rollback destrutivo automaticamente.
8. Limites mais restritivos vindos de Guardian Specs prevalecem.
9. Task Queue não deve alterar configurações globais.
10. Task Queue não deve usar permissões elevadas.

## Encerramento da Queue

A Task Queue pode ser considerada encerrada quando todas as Tasks obrigatórias estão em estado terminal compatível com o Workflow.

Condições para sucesso operacional:

- todas as Tasks obrigatórias estão `done` ou foram dispensadas por política registrada;
- nenhuma Task obrigatória está `queued`, `running` ou `blocked` sem decisão de encerramento;
- Attempts e logs essenciais foram persistidos;
- decisões do Guardian Engine foram respeitadas;
- limites não foram violados;
- resultados foram reportados ao Workflow Engine.

Condições para falha operacional:

- Task obrigatória falhou sem retry restante;
- dependência obrigatória ficou irresolúvel;
- Guardian Engine bloqueou sem alternativa segura;
- limite crítico foi excedido;
- persistência ou logs críticos ficaram indisponíveis em Workflow de alto risco;
- Runtime Adapter ou Agent Orchestrator obrigatório ficou indisponível sem fallback permitido.

Regras:

1. A Task Queue não encerra Mission.
2. A Task Queue deve reportar recomendação operacional ao Workflow Engine.
3. Encerramento deve preservar Queue Items, Attempts, logs, artefatos e decisões.
4. Tasks não executadas por encerramento devem virar `skipped` ou `cancelled` com motivo.

## Relação com Guardian Specs

### Security by Design

A Task Queue deve bloquear execução sem limites, mascarar logs, impedir `sudo` por padrão, restringir paths, exigir aprovação para ações sensíveis e tratar runtimes, providers, plugins, MCPs e APIs como superfície de ataque indireta.

### Token Efficiency

A Task Queue deve enviar contexto por referência, evitar retries cegos, impedir loops infinitos e registrar consumo quando disponível.

### AI Quality Assurance

A Task Queue deve preservar critérios de aceite, validações, Attempts, resultados e evidências antes de aceitar uma Task como `done`.

### Cost Optimization

A Task Queue deve respeitar orçamento por Task e Workflow, limitar retries e bloquear paralelismo futuro sem orçamento agregado.

### Architecture Governance

A Task Queue deve preservar fronteiras entre Mission Runner, Workflow Engine, Guardian Engine, Runtime Adapter e Agent Orchestrator.

### Documentation Governance

Mudanças relevantes de política de fila, paralelismo, retry, persistência ou fronteira arquitetural devem gerar Spec, decision note ou ADR conforme impacto.

### Testing Governance

Tasks que alterem código devem preservar vínculo com validações exigidas. Falha de validação deve impedir conclusão automática.

### Compliance Governance

Dados sensíveis, retenção de logs, auditoria, providers externos e políticas de privacidade devem seguir requisitos aplicáveis.

### Observability Governance

A Task Queue deve emitir eventos estruturados de enfileiramento, elegibilidade, seleção, estado, tentativa, retry, backoff, limite, política, erro e encerramento.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Confundir Mission Queue com Task Queue | Definir donos, escopos e unidades diferentes nesta Spec. |
| Execução não determinística | Ordenação por prioridade, topologia, criação e `task_id`. |
| Retry infinito | Exigir `max_attempts` e limites de ciclos, custo e tempo. |
| Backoff mascarar falha determinística | Classificar erros e preferir bloqueio ou replanejamento. |
| Paralelismo causar conflito de artefatos | Desabilitar por padrão e exigir locks, isolamento e ADR/Spec futura. |
| Bypass do Guardian Engine | Tornar avaliação obrigatória para Tasks sensíveis, retries e paralelismo. |
| Vazamento de segredos em logs | Registrar referências e mascarar dados sensíveis. |
| Perda de estado após falha | Persistência local inicial e eventos append-only quando possível. |
| Acoplamento ao OpenCode | Usar contrato de Runtime Adapter. |
| Acoplamento a agentes concretos | Usar Agent Orchestrator futuro e capabilities. |
| Fila alterar plano sem governança | Exigir replanejamento para mudanças de dependência ou critério de aceite. |
| Cancelamento inconsistente | Propagar parada segura e preservar estado terminal com motivo. |

## Decisões aprovadas por esta Spec

1. Task Queue é componente operacional interno do Workflow Engine.
2. Task Queue é diferente da Mission Queue do Mission Runner.
3. Task Queue trabalha com Tasks de Workflow, não com Missions.
4. Estados mínimos da Task Queue são `queued`, `running`, `done`, `failed`, `blocked`, `skipped` e `cancelled`.
5. Execução inicial da Task Queue deve ser sequencial, com `max_parallel_tasks: 1`.
6. Ordenação deve ser determinística e auditável.
7. Dependências obrigatórias prevalecem sobre prioridade.
8. Retries devem ser finitos e registrados por Attempt.
9. Backoff deve ser governado por política e respeitar limites.
10. Task Queue deve integrar Guardian Engine antes de Tasks sensíveis, retries sensíveis e paralelismo futuro.
11. Task Queue deve integrar Runtime Adapter sem conhecer OpenCode ou outro runtime concreto.
12. Task Queue deve preparar integração futura com Agent Orchestrator sem escolher agentes concretos.
13. Persistência inicial deve ser local, simples, auditável e provider agnostic.
14. Logs e rastreabilidade são obrigatórios por Mission, Workflow, Queue, Task e Attempt.
15. Task Queue não deve executar tools, MCPs, providers, bancos ou comandos diretamente.
16. Task Queue não deve alterar configurações globais nem usar `sudo`.

## Critérios de aceite

- Existe uma Spec própria para Task Queue em `specs/framework/0007-task-queue.md`.
- A Spec diferencia Mission Queue e Task Queue.
- A Spec define Task Queue como componente interno do Workflow Engine.
- A Spec cobre os estados `queued`, `running`, `done`, `failed`, `blocked`, `skipped` e `cancelled`.
- A Spec define prioridade.
- A Spec define dependências.
- A Spec define retries.
- A Spec define backoff.
- A Spec define limite de tentativas.
- A Spec define ordenação determinística.
- A Spec define execução sequencial inicial.
- A Spec prepara execução paralela futura sem autorizá-la como implementação concreta.
- A Spec define integração com Guardian Engine.
- A Spec define integração com Runtime Adapter.
- A Spec define integração futura com Agent Orchestrator.
- A Spec define logs.
- A Spec define rastreabilidade.
- A Spec define persistência local inicial.
- A Spec preserva provider agnostic.
- A Spec define segurança e limites.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir schema persistente final de Queue, Queue Item, Attempt e Event.
- Definir formato final de arquivos locais ou storage local inicial.
- Definir contrato formal entre Workflow Engine e Task Queue em código ou IDL.
- Definir política numérica padrão de `max_attempts`, backoff e timeouts por tipo de Task.
- Definir política de locks e isolamento para paralelismo futuro.
- Definir estratégia de recuperação após crash com Task `running`.
- Definir como replanejamento versiona Queue Items já existentes.
- Definir formato estruturado final dos eventos de observabilidade.
- Definir ADR se a Task Queue deixar de ser interna ao Workflow Engine.

# Spec 0008 — Agent Orchestrator

## Status

Proposta.

## Objetivo

Definir o Agent Orchestrator do Vercosa AI Framework como o componente responsável por selecionar, configurar e coordenar Agents e Subagents para executar Tasks elegíveis recebidas da Task Queue, respeitando capabilities, políticas, limites, rastreabilidade e decisões do Guardian Engine.

O Agent Orchestrator deve preservar a arquitetura Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design. Ele não deve acoplar o núcleo do framework a OpenCode, MCPs, providers, modelos, sistema operacional, banco de dados, IDE ou ferramenta de agente específica.

## Contexto

As Specs 0001, 0006 e 0007 estabelecem que:

- missões são decompostas em workflows e tasks;
- a execução inicial deve ser sequencial;
- paralelismo futuro deve ser explícito, governado e rastreável;
- a Task Queue organiza prioridade, dependências, tentativas e estado operacional;
- Tasks declaram `required_capabilities`, `risk_level`, `model_policy`, limites, contexto e critérios de aceite;
- agentes não devem conhecer providers, MCPs, APIs ou bancos diretamente;
- capabilities são a fronteira entre agentes e implementação concreta;
- OpenCode é runtime inicial, não núcleo do framework;
- Model Selection Engine seleciona modelos por política, não por hardcode;
- Guardian Engine governa planos, tasks e ações sensíveis;
- todo loop precisa de condição de parada.

O Agent Orchestrator é a camada que transforma uma Task elegível em uma execução de agente controlada. Ele não planeja workflows, não altera dependências da Task Queue, não escolhe modelos diretamente, não chama MCPs diretamente e não substitui Runtime Adapter, Guardian Engine, Model Selection Engine, Capabilities, Skills ou Tools.

## Escopo

Esta Spec cobre:

- papel do Agent Orchestrator na arquitetura;
- relação `Task Queue -> Agent Orchestrator -> Agents -> Subagents`;
- agentes como state machines;
- estados `idle`, `planning`, `executing`, `reflecting`, `validating`, `replanning`, `done` e `failed`;
- separação entre Agent, Capability, Skill, Tool, Provider e MCP;
- regra de que agente não conhece MCP diretamente;
- seleção de agente por role, domínio, complexidade e risco;
- integração com Model Selection Engine;
- integração com Guardian Engine;
- integração com Runtime Adapter;
- execução inicial sequencial;
- execução paralela futura;
- delegação para subagents;
- critérios de parada;
- limites de custo, tokens, ciclos e tentativas;
- logs e rastreabilidade;
- segurança contra prompt injection;
- provider agnostic;
- OpenCode como runtime inicial, não núcleo;
- riscos, mitigações, decisões e critérios de aceite.

Esta Spec não cobre:

- implementação concreta em código;
- criação de CLI, API, daemon, worker, serviço `systemd` ou scheduler real;
- alteração de configurações globais;
- uso de `sudo`;
- schema final de banco de dados;
- implementação final de registry de agentes;
- implementação final de Capabilities, Skills, Tools ou MCPs;
- engine final de paralelismo multi-agente;
- seleção concreta de modelos;
- criação de agentes OpenCode específicos;
- execução real de comandos, tools, MCPs, providers, bancos ou APIs.

## Princípios

1. Agent Orchestrator coordena agentes; ele não é agente.
2. Agentes executam responsabilidades específicas por meio de capabilities abstratas.
3. Agentes não conhecem MCPs, providers, bancos, APIs ou ferramentas concretas diretamente.
4. Capabilities são solicitadas por agentes e resolvidas pelo framework por meio de políticas, skills e tools.
5. Skills implementam capabilities de forma reutilizável.
6. Tools acessam providers, MCPs, APIs, bancos ou filesystem conforme política.
7. O modelo de IA usado por um agente deve ser selecionado pelo Model Selection Engine.
8. Toda execução de agente deve ser governada pelo Guardian Engine quando houver risco, ação sensível ou mudança de contexto.
9. Execução inicial deve ser sequencial, com uma Task e um agente ativo por Workflow.
10. Paralelismo futuro deve preservar isolamento, orçamento, logs, validação e política.
11. Loops de agentes devem ter estados explícitos e condições de parada.
12. OpenCode é o runtime inicial via Runtime Adapter, não dependência central do framework.

## Posição arquitetural

O Agent Orchestrator fica entre a Task Queue e Agents/Subagents.

Fluxo conceitual:

```text
Mission Runner
↓
Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Agents
↓
Subagents
↓
Capabilities
↓
Policy Engine / Guardian Engine
↓
Skills
↓
Tools
↓
Providers / MCPs / APIs
```

Fluxo operacional inicial:

```text
Task Queue
↓ eligible task with required capabilities, limits and context refs
Agent Orchestrator
↓ agent assignment and execution request
Runtime Adapter
↓ runtime-specific agent execution
Agent / Subagent loop
↓ normalized result and evidence
Agent Orchestrator
↓ assignment result
Task Queue
```

Regras:

1. A Task Queue despacha Tasks elegíveis para o Agent Orchestrator quando execução por agente for necessária.
2. O Agent Orchestrator seleciona perfil de agente e coordena execução, mas não altera dependências, prioridade ou critérios de aceite da Task.
3. Runtime Adapter traduz uma execução governada para runtime concreto, como OpenCode.
4. O Agent Orchestrator deve tratar OpenCode como adapter inicial, não como modelo arquitetural obrigatório.
5. Resultado de agente deve voltar como evidência vinculada a `mission_id`, `workflow_id`, `task_id`, `attempt_id` e `agent_assignment_id`.

## Definições

### Agent Orchestrator

Componente responsável por receber uma Task elegível, selecionar um Agent Profile compatível, criar uma Agent Assignment, coordenar o loop de execução do agente, delegar subtrabalhos quando permitido, coletar evidências e devolver resultado normalizado à Task Queue.

Responsabilidades:

- validar que a Task possui capabilities, limites, contexto e política suficientes;
- solicitar decisão do Guardian Engine quando necessário;
- solicitar seleção de modelo ao Model Selection Engine;
- selecionar Agent Profile por role, domínio, complexidade, risco e capabilities;
- criar Agent Assignment rastreável;
- coordenar ciclo de vida de Agent e Subagents;
- aplicar limites de custo, tokens, ciclos, tempo e delegação;
- impedir acesso direto de agentes a MCPs e providers;
- acionar Runtime Adapter para execução concreta;
- normalizar resultado, evidências, validações, warnings e erros;
- reportar estado e resultado à Task Queue.

Não responsabilidades:

- decompor Mission em Workflow;
- criar ou alterar grafo de dependências;
- alterar critérios de aceite da Task;
- persistir fila como fonte primária;
- escolher modelo concreto sem Model Selection Engine;
- chamar MCP, provider, API, banco ou tool diretamente;
- implementar Skills ou Tools;
- aprovar Specs;
- ignorar Guardian Engine;
- alterar configuração global;
- usar `sudo`;
- executar rollback destrutivo automático.

### Agent

Agent é uma entidade executora orientada por role, objetivo, contexto, políticas e capabilities.

Campos mínimos desejados de um Agent Profile:

- `agent_profile_id`;
- `role`;
- `domain`;
- `supported_task_types`;
- `supported_capabilities`;
- `complexity_range`;
- `risk_range`;
- `default_model_policy`;
- `default_execution_limits`;
- `allowed_delegations`;
- `validation_requirements`;
- `security_profile`;
- `runtime_constraints`;
- `audit_log_ref`.

Regras:

1. Agent Profile descreve capacidade e política, não provider concreto.
2. Agente deve operar como state machine com estado externo rastreável.
3. Agente deve pedir capabilities, não tools, MCPs ou providers.
4. Agente não deve receber segredos, dados sensíveis ou contexto excessivo sem política explícita.
5. Agente deve produzir resultado validável ou falha explicável.

### Subagent

Subagent é uma execução especializada, limitada e subordinada a uma Agent Assignment principal.

Uso esperado:

- pesquisa limitada;
- revisão focada;
- validação específica;
- análise de impacto;
- geração de artefato auxiliar;
- investigação de erro;
- decomposição interna não persistida como Workflow Task quando política permitir.

Regras:

1. Subagent deve herdar limites, políticas, contexto permitido e rastreabilidade da Agent Assignment principal.
2. Subagent não pode ampliar escopo, paths, providers, modelo, orçamento ou permissões sem autorização.
3. Delegação deve ter objetivo, entrada, saída esperada, limite e condição de parada.
4. Resultado de Subagent deve voltar como evidência da Agent Assignment principal.
5. Subagent não deve conhecer MCPs diretamente.

### Capability

Capability é uma capacidade abstrata solicitada por agentes.

Exemplos:

- `SearchSpecification`;
- `SearchCode`;
- `ReadContext`;
- `GenerateADR`;
- `ValidateSecurity`;
- `ReviewArchitecture`;
- `OptimizeTokens`;
- `RunValidation`.

Regras:

1. Capabilities devem ser nomeadas por intenção, não por implementação.
2. Capability deve ser autorizada por política antes de resolver Skills ou Tools sensíveis.
3. Agente deve receber somente o contrato da capability e os resultados permitidos.
4. A resolução de Capability para Skill/Tool pertence ao framework, não ao agente.

### Skill

Skill implementa uma ou mais capabilities de forma reutilizável, governada e testável.

Regras:

1. Skill pode usar Tools conforme política.
2. Skill deve declarar entradas, saídas, riscos, limites e ferramentas necessárias.
3. Skill não deve expor detalhes de MCP ou provider ao agente quando isso não for necessário.
4. Skill deve retornar resultado normalizado para a capability solicitada.

### Tool

Tool é a integração concreta usada por uma Skill.

Regras:

1. Tool pode acessar MCP, provider, banco, API, filesystem ou runtime conforme política.
2. Tool é camada de implementação externa, não abstração de agente.
3. Tool deve ser governada por Guardian Engine quando ação for sensível.
4. Tool deve registrar evidência, erros e consumo quando disponível.

### Provider e MCP

Provider e MCP pertencem à camada externa do framework.

Regras:

1. Provider ou MCP não deve ser dependência direta de Agent ou Subagent.
2. Acesso a Provider ou MCP deve ocorrer por Tool, chamada por Skill, autorizada por Capability e política.
3. Provider externo não deve receber dados sensíveis sem política permissiva explícita.
4. Troca de Provider ou MCP não deve exigir mudança de Agent Profile.

## Agent Assignment

Agent Assignment é a unidade rastreável de execução de uma Task por um agente selecionado.

Campos mínimos desejados:

- `agent_assignment_id`;
- `mission_id`;
- `workflow_id`;
- `task_id`;
- `attempt_id`;
- `agent_profile_id`;
- `role`;
- `domain`;
- `status`;
- `state`;
- `required_capabilities`;
- `resolved_capability_refs`;
- `model_selection_request_ref`;
- `model_selection_decision_ref`;
- `guardian_decision_refs`;
- `runtime_request_ref`;
- `runtime_result_ref`;
- `subagent_assignment_refs`;
- `context_refs`;
- `artifact_refs`;
- `cost_used`;
- `tokens_used`;
- `cycle_count`;
- `started_at`;
- `finished_at`;
- `last_error`;
- `audit_log_ref`.

Regras:

1. Toda execução de agente deve possuir Agent Assignment.
2. Assignment deve ser criada antes de acionar Runtime Adapter.
3. Assignment deve preservar decisões de Guardian e Model Selection.
4. Assignment não deve depender da memória interna do runtime para rastreabilidade.
5. Assignment deve terminar em `done` ou `failed`, ou retornar bloqueio/revisão conforme contrato da Task Queue.

## State machine de agentes

Estados mínimos obrigatórios de Agent Assignment:

- `idle`: agente selecionado ou disponível, ainda sem planejamento da execução;
- `planning`: agente está montando plano interno limitado para a Task;
- `executing`: agente está executando ações permitidas via capabilities;
- `reflecting`: agente está avaliando resultado parcial, erros, evidências e próximos passos;
- `validating`: agente está validando saída contra critérios de aceite e políticas;
- `replanning`: agente está ajustando plano interno dentro dos limites permitidos;
- `done`: agente concluiu com resultado aceito para a Assignment;
- `failed`: agente falhou por erro, bloqueio, validação reprovada ou limite excedido.

Transições permitidas:

```text
idle -> planning
idle -> failed
planning -> executing
planning -> failed
executing -> reflecting
executing -> validating
executing -> failed
reflecting -> executing
reflecting -> validating
reflecting -> replanning
reflecting -> failed
validating -> done
validating -> replanning
validating -> failed
replanning -> executing
replanning -> failed
```

Regras:

1. `done` e `failed` são terminais para a Assignment atual.
2. `replanning` é interno à execução do agente e não pode alterar o Workflow Plan ou dependências da Task Queue.
3. Replanejamento que exigir mudança de escopo, critério de aceite, dependência ou limite deve retornar bloqueio ao Workflow Engine/Task Queue.
4. Toda transição deve gerar log estruturado.
5. Todo loop deve incrementar `cycle_count` ou métrica equivalente.
6. Assignment deve falhar ou bloquear quando `max_cycles`, `max_tokens`, `max_cost`, `max_wall_clock_time` ou `max_delegations` forem excedidos.
7. O estado real deve ser persistível ou reconstruível sem depender de conversa do agente.

## Seleção de agente

O Agent Orchestrator deve selecionar agente por compatibilidade, risco e política.

Entradas mínimas:

- `task_type`;
- `required_capabilities`;
- `role` quando declarado na Task ou `model_policy`;
- `domain` quando inferível por Spec, path, artefato ou metadata;
- `complexity`;
- `risk_level`;
- `acceptance_criteria`;
- `validation_policy`;
- `execution_limits`;
- `context_refs`;
- `allowed_paths` e `denied_paths` quando disponíveis;
- decisões do Guardian Engine;
- políticas globais e Guardian Specs.

Ordem conceitual de seleção:

1. Filtrar Agent Profiles por capabilities obrigatórias.
2. Filtrar por role compatível.
3. Filtrar por domínio compatível.
4. Filtrar por suporte a tipo de Task.
5. Filtrar por complexidade suportada.
6. Filtrar por risco permitido.
7. Aplicar restrições de segurança, privacidade e compliance.
8. Aplicar disponibilidade de runtime.
9. Aplicar política de custo, tokens e latência.
10. Escolher perfil determinístico ou registrar motivo de empate.

Regras:

1. Falta de agente compatível deve bloquear a Task, não escolher agente genérico inseguro silenciosamente.
2. Task de alto risco deve preferir agente com perfil de revisão, validação ou segurança compatível.
3. Agente especializado deve ser preferido quando reduzir risco e contexto.
4. Agente genérico só deve executar Task sensível com política explícita e validação adequada.
5. Seleção deve ser auditável e reproduzível com os mesmos inputs e registry.
6. Overrides manuais devem ser registrados e podem exigir Guardian Engine.

## Integração com Model Selection Engine

O Agent Orchestrator não escolhe modelos concretos.

Contrato conceitual:

```text
Agent Orchestrator
↓ model selection request with task, agent role, complexity, risk and policy
Model Selection Engine
↓ model selection decision
Agent Orchestrator
↓ Runtime Adapter request with selected model reference
```

Campos mínimos da solicitação:

- `mission_id`;
- `workflow_id`;
- `task_id`;
- `agent_assignment_id`;
- `role`;
- `domain`;
- `task_type`;
- `complexity`;
- `risk_level`;
- `quality`;
- `reasoning`;
- `memory`;
- `context_size_estimate`;
- `security`;
- `privacy`;
- `cost`;
- `budget`;
- `latency`;
- `fallback`;
- `runtime_constraints`;
- `available_provider_policy`.

Regras:

1. Agent Orchestrator deve enviar requisitos e políticas, não IDs hardcoded de modelo.
2. Decisão de modelo deve ser registrada na Assignment.
3. Falha de seleção deve bloquear ou falhar a Assignment conforme política.
4. Fallback de modelo deve ser decidido pelo Model Selection Engine e respeitar Guardian Engine.
5. Troca de modelo durante replanning interno exige nova decisão se risco, contexto, custo ou capacidade mudar.

## Integração com Guardian Engine

O Agent Orchestrator deve consultar ou receber decisões do Guardian Engine antes e durante execuções relevantes.

Pontos mínimos de avaliação:

- antes de criar Assignment para Task sensível;
- antes de selecionar agente para risco alto;
- antes de permitir capability sensível;
- antes de acionar Tool que possa alterar arquivos, executar comandos, usar rede, provider externo, banco ou MCP;
- antes de delegar para Subagent quando houver aumento de escopo, contexto ou risco;
- antes de ampliar limites de custo, tokens, ciclos, tempo ou contexto;
- antes de retry de execução sensível;
- antes de aceitar resultado de alto risco como `done`.

Decisões esperadas:

- `allow`: execução pode continuar conforme limites;
- `warn`: execução pode continuar se política permitir e warning for registrado;
- `require_approval`: Assignment deve bloquear ou exigir revisão;
- `block`: Assignment deve falhar ou bloquear sem executar a ação.

Regras:

1. Agent Orchestrator não deve reduzir contexto enviado ao Guardian Engine para obter aprovação.
2. Decisão `block` deve impedir a ação afetada.
3. Decisão `require_approval` deve retornar estado bloqueado ou requerer revisão manual.
4. Decisão `allow` não elimina validação posterior.
5. Decisões devem ser vinculadas à Assignment, capability, subagent ou ação avaliada.
6. Falha do Guardian Engine deve bloquear execução automática de alto risco.

## Integração com Runtime Adapter

O Agent Orchestrator deve acionar runtimes concretos apenas por Runtime Adapter.

Contrato conceitual:

```text
Agent Orchestrator
↓ normalized agent execution request
Runtime Adapter
↓ concrete runtime execution, initially OpenCode
Runtime Adapter
↓ normalized result, artifacts, logs, usage and errors
Agent Orchestrator
```

Campos mínimos da execução:

- `mission_id`;
- `workflow_id`;
- `task_id`;
- `attempt_id`;
- `agent_assignment_id`;
- `agent_profile_ref`;
- `model_selection_decision_ref`;
- `required_capabilities`;
- `context_refs`;
- `expected_outputs`;
- `acceptance_criteria`;
- `execution_limits`;
- `logging_policy`;
- `security_policy`;
- `approval_policy`;
- `allowed_paths`;
- `denied_paths`.

Regras:

1. Runtime Adapter executa intenção governada; ele não planeja Workflow nem escolhe agente.
2. Agent Orchestrator não deve chamar OpenCode diretamente.
3. OpenCode deve ser tratado como runtime inicial, substituível por Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI ou API futura.
4. Resultado do Runtime Adapter deve ser normalizado antes de retornar à Task Queue.
5. Falha de Runtime Adapter deve virar erro rastreável da Assignment, não perda de estado.
6. Runtime específico não pode ampliar permissões, providers, tools ou contexto sem autorização do framework.

## Execução sequencial inicial

A execução inicial do Agent Orchestrator deve ser sequencial.

Características:

- uma Task ativa por Workflow;
- uma Agent Assignment principal ativa por Task;
- Subagents desabilitados por padrão ou limitados por política explícita;
- `max_parallel_agents: 1`;
- `max_parallel_subagents: 0` ou `1` quando política permitir;
- validação incremental após cada Assignment;
- logs por estado, ciclo, capability, decisão e resultado;
- parada segura em bloqueio, falha crítica, limite excedido ou decisão `block`.

Regras:

1. Agent Orchestrator não deve iniciar nova Assignment se já houver Assignment principal `executing`, `reflecting`, `validating` ou `replanning` para a mesma Task.
2. Uma Task só deve receber Assignment quando estiver elegível pela Task Queue.
3. Assignment deve terminar antes de a Task Queue selecionar a próxima Task no modo sequencial.
4. Falha de Assignment obrigatória deve reportar erro à Task Queue para retry, bloqueio, falha ou replanejamento conforme política.
5. Execução sequencial deve priorizar baixo blast radius, rastreabilidade e depuração simples.

## Execução paralela futura

O Agent Orchestrator deve ser desenhado para suportar paralelismo futuro, mas esta Spec não autoriza implementação concreta de paralelismo.

Pré-condições futuras:

- Task Queue com `max_parallel_tasks` maior que `1` por política explícita;
- Tasks independentes sem dependência obrigatória entre si;
- isolamento de artefatos, paths e recursos;
- locks ou estratégia de merge para escrita concorrente;
- orçamento agregado suficiente;
- limites por agente, subagent, Task, Workflow e grupo paralelo;
- avaliação do Guardian Engine para concorrência;
- runtime capaz de executar concorrência com isolamento;
- logs correlacionáveis por Assignment, Subagent e Attempt;
- estratégia de cancelamento e encerramento seguro.

Regras futuras:

1. Agentes paralelos não devem escrever nos mesmos artefatos sem lock ou política de merge.
2. Orçamento do Workflow deve limitar a soma das execuções paralelas.
3. Falha de um agente paralelo deve ter política explícita: continuar, pausar grupo, cancelar grupo ou replanejar.
4. Paralelismo não deve reduzir validação, logging, segurança ou rastreabilidade.
5. Execução paralela multi-runtime, multi-agent ou distribuída exige Spec ou ADR futura.

## Delegação para Subagents

Delegação deve ser explícita, limitada e rastreável.

Campos mínimos de uma Subagent Assignment:

- `subagent_assignment_id`;
- `parent_agent_assignment_id`;
- `mission_id`;
- `workflow_id`;
- `task_id`;
- `role`;
- `domain`;
- `goal`;
- `required_capabilities`;
- `context_refs`;
- `expected_outputs`;
- `execution_limits`;
- `status`;
- `state`;
- `artifact_refs`;
- `cost_used`;
- `tokens_used`;
- `cycle_count`;
- `audit_log_ref`.

Regras:

1. Delegação deve ser permitida pelo Agent Profile e pela política da Task.
2. Delegação não deve criar Task Queue Item oculto quando o trabalho deveria ser uma Task rastreável do Workflow.
3. Subagent deve receber contexto mínimo necessário por referência.
4. Subagent deve ter limite próprio menor ou igual ao limite restante da Assignment principal.
5. Subagent não pode delegar novamente salvo política explícita futura.
6. Resultado de Subagent deve ser resumido, validado e anexado à Assignment principal.
7. Falha de Subagent deve ser classificada como recuperável, bloqueante ou irrelevante conforme política.

## Critérios de parada

Cada Agent Assignment deve ter condições de parada explícitas.

Condições de sucesso:

- objetivo da Task atendido;
- expected outputs produzidos ou justificadamente dispensados;
- critérios de aceite avaliados;
- validações obrigatórias concluídas;
- decisões do Guardian Engine respeitadas;
- limites não violados;
- evidências e logs registrados;
- revisão manual concluída quando exigida.

Condições de falha:

- erro não recuperável;
- capability obrigatória indisponível;
- agente compatível indisponível;
- Model Selection Engine sem modelo compatível;
- Guardian Engine bloqueou ação necessária;
- prompt injection ou contexto não confiável sem mitigação suficiente;
- validação obrigatória reprovada;
- limite de ciclos, tokens, custo, tempo, tentativas ou delegações excedido;
- runtime indisponível sem fallback permitido;
- evidência crítica ausente em Task de alto risco.

Regras:

1. Loops não podem ser infinitos.
2. Replanning interno não pode resetar limites consumidos.
3. Repetição de falha determinística deve preferir bloqueio ou revisão manual em vez de retry cego.
4. Assignment deve retornar resultado parcial quando isso ajudar diagnóstico sem violar segurança.
5. Encerramento deve preservar estado, logs, decisões, artefatos e erros.

## Limites de custo, tokens e ciclos

Limites mínimos desejados:

- `max_cycles_per_assignment`;
- `max_replans_per_assignment`;
- `max_tool_calls_per_assignment` futuro;
- `max_capability_calls_per_assignment`;
- `max_subagents_per_assignment`;
- `max_delegation_depth`;
- `max_tokens_per_assignment`;
- `max_cost_per_assignment`;
- `max_wall_clock_time_per_assignment`;
- `max_context_size_per_assignment`;
- `max_model_selection_attempts`;
- `max_runtime_attempts`;
- `max_parallel_agents` futuro, default `1`;
- `max_parallel_subagents` futuro, default `0` ou política explícita.

Regras:

1. Assignment não deve iniciar sem limites explícitos ou defaults seguros.
2. Limites da Assignment não podem exceder limites da Task, Workflow ou Mission sem aprovação.
3. Subagents consomem orçamento da Assignment principal.
4. Tokens e custo devem ser registrados quando runtime ou provider disponibilizar.
5. Estimativas devem ser atualizadas quando houver replanning interno relevante.
6. Ao exceder limite, Assignment deve falhar, bloquear ou exigir aprovação conforme política.
7. Limites mais restritivos vindos de Guardian Specs prevalecem.

## Logs

O Agent Orchestrator deve registrar eventos estruturados suficientes para auditoria, diagnóstico, reprodução e retomada.

Eventos mínimos:

- Assignment criada;
- agente selecionado;
- seleção de modelo solicitada;
- decisão de modelo recebida;
- decisão do Guardian Engine recebida;
- transição de estado do agente;
- capability solicitada;
- capability autorizada, bloqueada ou falhada;
- Runtime Adapter acionado;
- resultado de runtime recebido;
- Subagent delegado;
- Subagent concluído ou falhado;
- ciclo iniciado e concluído;
- replanning interno iniciado e concluído;
- limite aplicado ou excedido;
- prompt injection detectado ou mitigado;
- validação executada;
- Assignment concluída;
- Assignment falhou;
- resultado reportado à Task Queue.

Campos mínimos por evento:

- `event_id`;
- `event_type`;
- `mission_id`;
- `workflow_id`;
- `task_id`;
- `attempt_id`;
- `agent_assignment_id`;
- `subagent_assignment_id` quando aplicável;
- `agent_profile_id` quando aplicável;
- `previous_state` quando aplicável;
- `new_state` quando aplicável;
- `cycle_number` quando aplicável;
- `capability_ref` quando aplicável;
- `guardian_decision_ref` quando aplicável;
- `model_selection_decision_ref` quando aplicável;
- `runtime_request_ref` quando aplicável;
- `runtime_result_ref` quando aplicável;
- `artifact_refs` quando aplicável;
- `timestamp`;
- `reason`.

Regras:

1. Logs não podem conter segredos.
2. Logs devem preferir referências, hashes, paths, IDs e metadados.
3. Prompts completos só podem ser registrados quando política permitir.
4. Dados de contexto não confiável devem ser marcados como não confiáveis quando registrados.
5. Falha de log deve bloquear conclusão automática de Tasks de alto risco.

## Rastreabilidade

Relações mínimas:

- Mission para Workflow;
- Workflow para Task;
- Task para Attempt;
- Attempt para Agent Assignment;
- Agent Assignment para Agent Profile;
- Agent Assignment para Model Selection Request e Decision;
- Agent Assignment para decisões do Guardian Engine;
- Agent Assignment para Runtime Request e Result;
- Agent Assignment para Subagent Assignments;
- Agent Assignment para capabilities solicitadas;
- Capability para Skill e Tool quando resolvidas;
- Tool para Provider, MCP, API ou banco quando acionados;
- Assignment para artefatos, validações, logs, custo e tokens.

Regras:

1. Rastreabilidade deve funcionar sem depender da memória do agente ou do runtime.
2. Artefatos devem ser referenciados por path, hash, ID ou referência estável.
3. Decisões de modelo e política devem ser preservadas mesmo quando a execução falhar.
4. Subagents devem ser rastreáveis ao agente pai.
5. Reexecução ou retry deve criar nova Assignment ou nova Attempt conforme contrato da Task Queue.

## Segurança contra prompt injection

O Agent Orchestrator deve tratar entradas externas, documentos, código, resultados de busca, logs e respostas de ferramentas como potencialmente não confiáveis.

Regras:

1. Contexto não confiável deve ser marcado e separado de instruções do sistema, políticas e Specs.
2. Conteúdo recuperado de arquivos, web, banco, provider, MCP ou ferramenta não deve sobrescrever políticas do framework.
3. Agente deve receber instrução explícita para não obedecer comandos contidos em dados analisados.
4. Capabilities sensíveis devem exigir Guardian Engine quando contexto não confiável influenciar ação.
5. Dados sensíveis devem ser minimizados, mascarados ou omitidos conforme política.
6. Prompt injection detectado deve gerar log, warning e bloqueio quando houver risco de ação indevida.
7. Ação que modifique arquivos, execute comando, use rede, acesse provider externo ou leia segredo deve ser separada de leitura de contexto não confiável por validação ou política.
8. O Agent Orchestrator deve preferir referências a contexto extenso para reduzir superfície de ataque e consumo de tokens.

## Provider agnostic

O Agent Orchestrator deve depender de contratos do framework.

Regras:

1. Não deve depender arquiteturalmente de OpenCode.
2. Não deve depender de OpenAI, Anthropic, Ollama ou modelo específico.
3. Não deve depender obrigatoriamente de PostgreSQL, pgvector, SQLite, Redis, Docker, systemd ou cloud provider.
4. Não deve depender obrigatoriamente de Linux, ARM64, x86_64, macOS ou Windows.
5. Runtime concreto deve ser acessado via Runtime Adapter.
6. Provider externo deve ser acessado por Tool governada, nunca diretamente por agente.
7. MCP deve ser detalhe de Tool ou Provider, não dependência do agente.
8. Agent Profiles devem declarar capacidades e restrições, não integrações concretas.

## Relação com Guardian Specs

### Security by Design

O Agent Orchestrator deve aplicar mínimo privilégio, bloquear acesso direto a MCPs e providers, isolar contexto não confiável, impedir `sudo` por padrão, restringir paths, exigir aprovação para ações sensíveis e tratar runtimes, tools, providers, MCPs e APIs como superfície de ataque.

### Token Efficiency

O Agent Orchestrator deve enviar contexto por referência, selecionar agentes especializados quando reduzir contexto, limitar ciclos, evitar loops redundantes, resumir resultados de Subagents e impedir retries cegos.

### AI Quality Assurance

Agentes devem operar com estados explícitos, critérios de aceite, validação, reflexão controlada, evidências e revisão quando política exigir.

### Cost Optimization

O Agent Orchestrator deve respeitar orçamento por Assignment, Task, Workflow e Mission, registrar consumo quando disponível, limitar delegações e bloquear paralelismo futuro sem orçamento agregado.

### Architecture Governance

O Agent Orchestrator deve preservar fronteiras entre Task Queue, Agents, Capabilities, Skills, Tools, Guardian Engine, Model Selection Engine e Runtime Adapter.

### Documentation Governance

Mudanças relevantes em seleção de agente, registry, paralelismo, delegação ou fronteira arquitetural devem gerar Spec, decision note ou ADR conforme impacto.

### Testing Governance

Tasks que alterem código devem retornar evidências de validação ou justificativa registrada. Falha de validação deve impedir conclusão automática.

### Compliance Governance

Dados sensíveis, retenção de logs, uso de providers externos, transferência de contexto e auditoria devem seguir políticas aplicáveis.

### Observability Governance

O Agent Orchestrator deve emitir eventos estruturados de seleção, estado, capability, modelo, Guardian, runtime, subagent, limite, erro, validação e encerramento.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Agente acessar MCP diretamente | Exigir cadeia Agent -> Capability -> Skill -> Tool -> MCP. |
| Acoplamento ao OpenCode | Usar Runtime Adapter e tratar OpenCode como runtime inicial. |
| Modelo hardcoded em Agent Profile | Enviar política ao Model Selection Engine. |
| Loop infinito de agente | Estados explícitos, `max_cycles` e condições de parada. |
| Subagents criarem trabalho oculto | Delegação limitada, rastreável e subordinada à Assignment. |
| Prompt injection influenciar ações | Separar contexto não confiável, aplicar Guardian Engine e mínimo privilégio. |
| Paralelismo causar conflito | Desabilitar por padrão e exigir locks, isolamento e Spec/ADR futura. |
| Seleção insegura de agente genérico | Filtrar por role, domínio, complexidade, risco e capabilities. |
| Vazamento de segredos em logs | Registrar referências e mascarar dados sensíveis. |
| Bypass do Guardian Engine | Tornar avaliação obrigatória para ações e capabilities sensíveis. |
| Perda de rastreabilidade no runtime | Agent Assignment e eventos estruturados independentes do runtime. |
| Custo inesperado por delegação | Limites por Assignment e Subagent, com orçamento agregado. |

## Decisões aprovadas por esta Spec

1. Agent Orchestrator é componente arquitetural próprio entre Task Queue e Agents.
2. Task Queue não escolhe agente concreto; ela despacha Task elegível ao Agent Orchestrator.
3. Agent Orchestrator seleciona agente por role, domínio, tipo de Task, capabilities, complexidade e risco.
4. Agentes e Subagents operam como state machines.
5. Estados mínimos de Agent Assignment são `idle`, `planning`, `executing`, `reflecting`, `validating`, `replanning`, `done` e `failed`.
6. Agentes solicitam capabilities e não conhecem MCPs, providers, bancos, APIs ou tools diretamente.
7. A cadeia arquitetural obrigatória é Agent -> Capability -> Skill -> Tool -> Provider/MCP/API.
8. Agent Orchestrator integra Model Selection Engine e não escolhe modelos concretos por hardcode.
9. Agent Orchestrator integra Guardian Engine para seleção, capabilities, ações sensíveis, delegação, retries e validações críticas.
10. Agent Orchestrator integra Runtime Adapter e não chama OpenCode diretamente.
11. OpenCode é runtime inicial, não núcleo do Agent Orchestrator.
12. Execução inicial deve ser sequencial, com um agente principal ativo por Task.
13. Paralelismo futuro requer política explícita, isolamento, orçamento, logs, Guardian Engine e Spec ou ADR quando necessário.
14. Delegação para Subagents deve ser limitada, rastreável e subordinada à Agent Assignment principal.
15. Critérios de parada, limites de custo, tokens, ciclos, tempo e delegações são obrigatórios.
16. Logs e rastreabilidade são obrigatórios por Mission, Workflow, Task, Attempt, Agent Assignment e Subagent Assignment.
17. Segurança contra prompt injection é requisito central do Agent Orchestrator.
18. Agent Orchestrator deve ser provider agnostic, runtime agnostic e model agnostic.
19. Agent Orchestrator não deve alterar configurações globais nem usar `sudo`.

## Estado implementado e validado em 0108

`AgentTaskExecutor`, em `src/vercosa_ai_framework/agents/task_executor.py`, é a ponte desacoplada entre Task Scheduler e Agent Orchestrator. O Agent Orchestrator seleciona `AgentProfile`, pode resolver Capabilities antes do runtime e pode executar Capabilities resolvidas antes do runtime quando configurado.

Evidências:

- `tests/test_task_agent_capability_integration.py` valida seleção de perfil, resolução declarativa de Capability antes do runtime e compatibilidade do caminho legado.
- `tests/test_capability_skill_tool_provider_dry_run.py` valida execução obrigatória de Capability resolvida antes do runtime quando `capability_executor` é injetado.
- `tests/test_agent_execution_governance_0107.py` valida `AgentExecutionGovernance` como dependência explícita e opcional, incluindo falha quando governança é exigida e não configurada.

O comportamento legado permanece compatível quando resolução, execução de Capability ou governança não são exigidas. O Agent Orchestrator não acessa provider, MCP, API, banco ou OpenCode diretamente; chamadas concretas passam por Runtime Adapter ou pela cadeia Capability -> Skill -> Tool -> Provider Gateway.

## Critérios de aceite

- Existe uma Spec própria para Agent Orchestrator em `specs/framework/0008-agent-orchestrator.md`.
- A Spec define o papel do Agent Orchestrator na arquitetura.
- A Spec define a relação `Task Queue -> Agent Orchestrator -> Agents -> Subagents`.
- A Spec define agentes como state machines.
- A Spec cobre os estados `idle`, `planning`, `executing`, `reflecting`, `validating`, `replanning`, `done` e `failed`.
- A Spec define separação entre Agent, Capability, Skill, Tool, Provider e MCP.
- A Spec estabelece que agente não conhece MCP diretamente.
- A Spec define seleção de agente por role, domínio, complexidade e risco.
- A Spec define integração com Model Selection Engine.
- A Spec define integração com Guardian Engine.
- A Spec define integração com Runtime Adapter.
- A Spec define execução inicial sequencial.
- A Spec prepara execução paralela futura sem autorizá-la como implementação concreta.
- A Spec define delegação para Subagents.
- A Spec define critérios de parada.
- A Spec define limites de custo, tokens, ciclos, tempo e delegações.
- A Spec define logs e rastreabilidade.
- A Spec cobre segurança contra prompt injection.
- A Spec preserva provider agnostic.
- A Spec define OpenCode como runtime inicial, não núcleo.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir schema persistente final de Agent Profile, Agent Assignment e Subagent Assignment.
- Definir formato final do Agent Registry.
- Definir matriz inicial de roles, domínios, complexities e risk levels.
- Definir contrato formal entre Task Queue e Agent Orchestrator.
- Definir contrato formal entre Agent Orchestrator e Runtime Adapter para execução de agentes.
- Definir contrato formal entre Agent Orchestrator e Capability Resolver.
- Definir política numérica padrão de ciclos, tokens, custo, tempo e delegações.
- Definir como capabilities serão registradas, versionadas e autorizadas.
- Definir estratégia de recuperação após crash com Assignment em execução.
- Definir política futura de paralelismo multi-agent e locks de artefatos.
- Definir ADR se Agent Orchestrator assumir responsabilidades hoje atribuídas ao Runtime Adapter ou Task Queue.

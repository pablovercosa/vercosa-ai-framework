# Spec 0004 — Mission Runner

## Status

Proposta.

## Objetivo

Definir o Mission Runner do Vercosa AI Framework como o componente responsável por receber, registrar, controlar e executar missões em ciclos governados por políticas, limites, validações, orçamento, logs e estados explícitos.

O Mission Runner deve permitir execução local inicial e preparar a arquitetura para execução futura via `systemd`, API ou outros runtimes, sem acoplar o núcleo do framework a uma ferramenta específica.

## Contexto

O Vercosa AI Framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design.

As Specs 0001, 0002 e 0003 estabelecem que:

- o usuário fornece missões, não apenas prompts;
- missões devem ser decompostas em workflows, tarefas, agentes, loops, validações e entregáveis;
- todo loop precisa de condição de parada;
- Guardian Specs prevalecem sobre políticas locais;
- modelos devem ser escolhidos pelo Model Selection Engine;
- runtimes concretos, como OpenCode, devem ser acessados por adapters;
- execução automática deve respeitar limites, permissões, orçamento, logs e validação.

O Mission Runner é a primeira camada operacional que transforma uma missão registrada em execução controlada. Ele não substitui o Mission Orchestrator, o Workflow Engine, o Policy Engine, o Model Selection Engine ou os Runtime Adapters.

## Escopo

Esta Spec cobre:

- conceito de Mission;
- fila de missões;
- estados `queued`, `running`, `done`, `failed` e `cancelled`;
- execução em ciclos;
- limite de ciclos;
- logs e auditoria;
- política de `auto_commit`;
- validação;
- critérios de aceite;
- rollback ou revisão manual;
- orçamento de tokens e custo;
- políticas de segurança;
- execução local;
- execução futura via `systemd`;
- execução futura via API;
- integração com Guardian Specs;
- integração futura com Workflow Engine.

Esta Spec não cobre:

- implementação concreta em código;
- criação de CLI, daemon, serviço `systemd` ou API real;
- alteração de configurações globais;
- uso de `sudo`;
- schema final de banco de dados;
- implementação final do Workflow Engine;
- implementação final de rollback automático;
- seleção concreta de modelos;
- execução direta de tools, MCPs ou providers.

## Princípios

1. Missões são unidades auditáveis de intenção e execução.
2. Toda missão deve ter estado explícito e transições controladas.
3. Execução deve ocorrer em ciclos finitos, observáveis e validáveis.
4. Todo ciclo precisa de condição de parada.
5. O menor escopo executável deve ser preferido para reduzir risco, custo e tokens.
6. Políticas de segurança, privacidade, custo e qualidade prevalecem sobre conveniência.
7. Execução local é o modo inicial, mas não deve virar dependência arquitetural única.
8. `auto_commit` deve ser seguro por padrão e depender de validação.
9. Falhas devem preservar estado, logs e evidências suficientes para revisão manual.
10. O Mission Runner coordena execução; ele não decide arquitetura, modelo ou permissões sozinho.

## Posição arquitetural

O Mission Runner fica na camada operacional entre entrada de missão e orquestração detalhada.

Fluxo conceitual inicial:

```text
Mission Request
↓
Mission Runner
↓
Mission Queue
↓
Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Policy Engine
↓
Model Selection Engine
↓
Runtime Adapter
```

Enquanto o Workflow Engine ainda não existir completamente, o Mission Runner pode executar um fluxo mínimo governado por Spec, desde que não viole a hierarquia conceitual e registre limitações operacionais.

## Definições

### Mission

Uma Mission é uma intenção de alto nível fornecida por usuário, sistema, API ou outro componente autorizado.

Exemplos:

- criar uma Spec;
- implementar uma funcionalidade aprovada;
- revisar segurança;
- analisar impacto de mudança;
- gerar documentação;
- validar critérios de aceite;
- executar manutenção local.

Uma Mission deve ser representada como unidade rastreável, com objetivo, contexto, restrições, políticas, entregáveis esperados, orçamento, estado e histórico de execução.

Campos mínimos desejados:

- `mission_id`;
- `title`;
- `goal`;
- `requested_by`;
- `created_at`;
- `workspace`;
- `spec_refs`;
- `guardian_refs`;
- `constraints`;
- `acceptance_criteria`;
- `validation_policy`;
- `security_policy`;
- `budget_policy`;
- `commit_policy`;
- `rollback_policy`;
- `execution_limits`;
- `status`;
- `audit_log_ref`.

### Mission Runner

Componente que controla o ciclo de vida operacional de missões.

Responsabilidades:

- registrar missões;
- colocar missões em fila;
- controlar estados;
- aplicar limites de execução antes de iniciar ciclos;
- acionar Mission Orchestrator ou fluxo mínimo aprovado;
- executar ciclos finitos;
- coletar logs;
- acionar validação;
- aplicar política de `auto_commit` quando permitida;
- encerrar missão como `done`, `failed` ou `cancelled`;
- preservar evidências para revisão manual.

Não responsabilidades:

- aprovar Specs;
- escolher modelos diretamente;
- ignorar Policy Engine;
- executar tools ou providers diretamente;
- alterar configuração global;
- decidir sozinho uso pago ou externo;
- fazer rollback destrutivo sem política explícita;
- substituir revisão humana quando exigida.

### Mission Queue

Fila lógica de missões aguardando execução.

A fila deve preservar ordem, prioridade, estado e metadados suficientes para retomada ou auditoria.

Campos mínimos desejados por item:

- `mission_id`;
- `priority`;
- `status`;
- `queued_at`;
- `started_at`;
- `finished_at`;
- `attempt_count`;
- `max_attempts`;
- `cycle_count`;
- `max_cycles`;
- `locked_by` quando aplicável;
- `last_error`;
- `budget_remaining` quando aplicável.

## Estados da missão

Estados mínimos obrigatórios:

- `queued`: missão registrada e aguardando execução;
- `running`: missão em execução ativa;
- `done`: missão concluída e validada conforme critérios aplicáveis;
- `failed`: missão encerrada por erro, limite excedido, validação reprovada ou política bloqueante;
- `cancelled`: missão cancelada por usuário, sistema ou política antes da conclusão.

Transições permitidas:

```text
queued -> running
queued -> cancelled
running -> done
running -> failed
running -> cancelled
failed -> queued
cancelled -> queued
```

Regras:

1. `done` deve ser terminal para a execução atual.
2. `failed` pode ser reenfileirado somente por nova decisão explícita ou política de retry.
3. `cancelled` pode ser reenfileirado somente quando a causa do cancelamento permitir.
4. Transições devem ser registradas em log.
5. Uma missão não deve voltar de `done` para outro estado; uma nova execução deve criar novo registro ou tentativa vinculada.

## Fila de missões

A Mission Queue deve suportar, no mínimo:

- enfileirar missão;
- listar missões por estado;
- selecionar próxima missão elegível;
- bloquear missão durante execução;
- liberar ou finalizar missão;
- cancelar missão pendente ou em execução;
- reenfileirar missão falhada quando permitido;
- registrar prioridade;
- impedir execução concorrente da mesma missão.

Regras:

1. A fila inicial pode ser local e baseada em arquivos ou storage simples, desde que seja auditável.
2. O formato persistente final fica pendente para Spec futura.
3. Execução concorrente deve ser desabilitada por padrão até existir política explícita de paralelismo.
4. Missões devem ser selecionadas respeitando prioridade, elegibilidade, dependências e políticas.
5. A fila não deve conter segredos em texto claro.
6. O estado da fila deve sobreviver a falha do processo quando possível.

## Execução em ciclos

O Mission Runner deve executar missões como ciclos controlados.

Ciclo conceitual:

```text
load mission
↓
resolve policy
↓
prepare context
↓
plan or update workflow
↓
execute next step
↓
collect artifacts and logs
↓
validate partial result
↓
decide continue, replan, finish, fail or cancel
```

Cada ciclo deve produzir um registro mínimo:

- `mission_id`;
- `cycle_number`;
- `started_at`;
- `finished_at`;
- `action_taken`;
- `policy_decisions`;
- `model_decisions` quando aplicável;
- `runtime_used` quando aplicável;
- `artifacts_changed`;
- `validation_result`;
- `token_usage` quando disponível;
- `cost_usage` quando disponível;
- `warnings`;
- `errors`;
- próxima decisão.

## Limite de ciclos

Toda missão deve ter limite explícito de ciclos.

Limites mínimos desejados:

- `max_cycles_per_mission`;
- `max_cycles_per_task` quando houver tasks;
- `max_replans`;
- `max_validation_failures`;
- `max_retries`;
- `max_runtime_failures`;
- `max_token_budget`;
- `max_cost_budget`;
- `max_wall_clock_time`.

Regras:

1. O Mission Runner deve recusar execução sem limite de ciclos ou default seguro.
2. Ao atingir `max_cycles_per_mission`, a missão deve parar como `failed` ou exigir revisão manual.
3. Replanejamento não pode resetar contador de ciclos.
4. Retry deve consumir ciclo ou tentativa, conforme política registrada.
5. Limites podem ser reduzidos por Guardian Specs, projeto, missão ou workflow.

## Logs e auditoria

O Mission Runner deve registrar eventos suficientes para explicar o ciclo de vida da missão.

Eventos mínimos:

- missão criada;
- missão enfileirada;
- missão iniciada;
- transição de estado;
- início e fim de ciclo;
- políticas aplicadas;
- orçamento estimado e consumido;
- decisão de modelo quando aplicável;
- runtime acionado quando aplicável;
- arquivos ou artefatos alterados;
- validações executadas;
- falhas, warnings e bloqueios;
- decisões de revisão manual;
- decisão de `auto_commit`;
- resultado final.

Regras:

1. Logs não podem conter segredos.
2. Logs não devem incluir contexto sensível desnecessário.
3. Prompts completos só podem ser registrados quando a política permitir.
4. Tokens, chaves, credenciais e conteúdo de `.env` devem ser mascarados ou omitidos.
5. Logs devem priorizar metadados, hashes, caminhos e referências a artefatos.
6. Logs devem permitir auditoria posterior sem depender da memória do agente.

## Auto-commit

`auto_commit` é a política que permite ao Mission Runner criar commit automaticamente ao fim de uma missão validada.

Estados mínimos:

- `disabled`;
- `after_validation`;
- `manual_approval_required`.

Regras:

1. `auto_commit` deve ser `disabled` por padrão.
2. `auto_commit` só pode ocorrer quando a missão terminar como candidata a `done`.
3. `auto_commit` exige validação mínima bem-sucedida.
4. `auto_commit` só pode incluir arquivos alterados pela missão atual.
5. `auto_commit` não pode incluir segredos, `.env`, credenciais, arquivos gerados sensíveis ou mudanças não relacionadas.
6. Worktree com mudanças externas deve bloquear commit automático ou exigir revisão manual.
7. Mensagem de commit deve referenciar `mission_id` e resumo dos entregáveis.
8. Push automático está fora do escopo desta Spec.

## Validação

A validação deve confirmar se a missão produziu os entregáveis esperados e respeitou políticas.

Fontes de validação possíveis:

- critérios de aceite da Spec;
- testes automatizados;
- lint ou validação estática;
- revisão arquitetural;
- revisão de segurança;
- comparação de artefatos esperados;
- validação manual;
- cross-review por outro agente ou modelo quando exigido.

Regras:

1. Missão não deve ser marcada como `done` sem validação aplicável.
2. Se validação não puder ser executada, o motivo deve ser registrado.
3. Falha de validação deve produzir `failed` ou exigir revisão manual, conforme política.
4. Validação crítica não deve depender apenas do mesmo agente que executou a mudança.
5. Critérios de aceite devem ser avaliados explicitamente quando existirem.

## Critérios de aceite da missão

Cada Mission deve possuir critérios de aceite proporcionais ao risco e ao tipo de entrega.

Campos mínimos desejados:

- entregáveis obrigatórios;
- arquivos ou artefatos esperados;
- validações obrigatórias;
- restrições de segurança;
- orçamento máximo;
- limite de ciclos;
- requisitos de revisão;
- definição de pronto;
- definição de falha.

Uma missão pode ser concluída como `done` somente quando:

1. entregáveis obrigatórios foram produzidos;
2. critérios de aceite foram satisfeitos ou exceções foram aprovadas;
3. validações obrigatórias passaram ou foram justificadamente dispensadas por política;
4. orçamento e limites não foram violados;
5. logs e estado final foram registrados;
6. revisão manual foi concluída quando exigida.

## Rollback ou revisão manual

O Mission Runner deve tratar rollback como política sensível.

Modos mínimos:

- `none`: não executar rollback automático;
- `manual_review_required`: preservar estado e solicitar revisão humana;
- `safe_revert_only`: permitir reversão apenas de artefatos claramente produzidos pela missão;
- `custom_policy`: seguir política específica aprovada por Spec ou ADR.

Regras:

1. Rollback automático deve ser desabilitado por padrão.
2. Operações destrutivas de rollback devem exigir política explícita e logs.
3. O Mission Runner não deve reverter mudanças que não consiga atribuir à missão atual.
4. Falha parcial deve preservar evidências, diff e logs para revisão manual.
5. Quando houver risco de perda de trabalho do usuário, exigir revisão manual.
6. Rollback de banco de dados, migração, infraestrutura ou estado externo exige Spec própria.

## Orçamento de tokens e custo

O Mission Runner deve aplicar orçamento como restrição de primeira classe.

Campos mínimos desejados:

- `token_budget_total`;
- `token_budget_per_cycle`;
- `cost_budget_total`;
- `cost_budget_per_cycle`;
- `pricing_policy`;
- `provider_policy`;
- `fallback_budget_policy`;
- `budget_exhaustion_action`.

Regras:

1. Orçamento deve ser verificado antes de iniciar a missão e antes de cada ciclo.
2. Quando o custo real não estiver disponível, registrar estimativa e limitação.
3. Ao exceder orçamento, a missão deve parar como `failed` ou exigir aprovação humana para continuar.
4. Fallback para modelo pago não pode ocorrer sem política permissiva.
5. Fallback para provider externo não pode ocorrer quando privacidade exigir execução local.
6. O Mission Runner deve solicitar seleção de modelos conforme Spec 0002, não escolher modelo por conta própria.
7. Otimizações de contexto devem ser preferidas antes de aumentar orçamento.

## Políticas de segurança

O Mission Runner deve aplicar Security by Design antes de execução.

Controles mínimos:

- paths permitidos e negados;
- bloqueio de segredos em logs;
- bloqueio de alteração global por padrão;
- bloqueio de `sudo` por padrão;
- bloqueio de comandos destrutivos sem aprovação explícita;
- controle de acesso a rede;
- controle de provider externo;
- controle de leitura de `.env` e credenciais;
- validação de plugins, MCPs e tools;
- registro de permissões efetivas.

Regras:

1. O Mission Runner não deve usar `sudo`.
2. Configurações globais não devem ser alteradas automaticamente.
3. Segredos não devem ser enviados a providers externos.
4. Dados sensíveis devem respeitar política de privacidade local ou do projeto.
5. Permissões devem ser derivadas do Policy Engine.
6. Em caso de conflito, a política mais restritiva prevalece.
7. Se uma ação exigir permissão ausente, a missão deve parar ou solicitar revisão manual.

## Execução local

Execução local é o modo inicial do Mission Runner.

Características:

- opera no workspace atual;
- usa arquivos locais para Specs, Knowledge Hub e artefatos;
- aciona Runtime Adapters locais quando necessário;
- respeita permissões do usuário atual;
- não presume arquitetura, sistema operacional, banco, modelo ou provider específico;
- detecta capacidades antes de executar.

Regras:

1. O Mission Runner deve ser Local First, mas não local-only.
2. Execução local não deve exigir interface gráfica.
3. Execução local não deve exigir `sudo`.
4. Execução local deve funcionar em ambientes SSH-first quando capacidades necessárias existirem.
5. Recursos específicos do ambiente atual devem ser tratados como capabilities detectadas, não pressupostos globais.

## Execução futura via systemd

O Mission Runner deve permitir futura execução como serviço gerenciado por `systemd`, sem depender disso no desenho inicial.

Uso futuro possível:

- processar fila em background;
- reiniciar após falha;
- executar timers;
- emitir logs para journal;
- controlar concorrência;
- isolar ambiente por usuário ou projeto.

Regras arquiteturais:

1. `systemd` deve ser adapter ou modo de hospedagem, não núcleo do Mission Runner.
2. A Spec atual não autoriza criação de serviço `systemd`.
3. Execução via `systemd` deve respeitar os mesmos estados, limites, logs, orçamento e políticas.
4. Configuração de serviço deve ser local ao projeto ou explicitamente aprovada.
5. Instalação global ou uso de `sudo` exigirá decisão futura separada.

## Execução futura via API

O Mission Runner deve permitir futura exposição por API.

Operações conceituais possíveis:

- criar missão;
- consultar missão;
- listar fila;
- cancelar missão;
- reenfileirar missão;
- consultar logs;
- aprovar revisão manual;
- consultar orçamento;
- receber eventos de execução.

Regras arquiteturais:

1. API deve ser interface, não núcleo.
2. API deve exigir autenticação, autorização e auditoria.
3. API não deve permitir bypass de Guardian Specs.
4. API não deve expor segredos em respostas ou logs.
5. API deve preservar idempotência em operações críticas quando possível.
6. API deve suportar execução assíncrona, pois missões podem ser longas.

## Integração com Guardian Specs

### Security by Design

O Mission Runner deve bloquear segredos em logs, impedir `sudo` por padrão, restringir paths, exigir aprovação para ações sensíveis e tratar providers, plugins, MCPs e APIs como superfície de ataque.

### Token Efficiency

O Mission Runner deve limitar ciclos, reduzir contexto enviado, preferir execução incremental, registrar uso de tokens quando possível e interromper missões ineficientes conforme política.

### AI Quality Assurance

O Mission Runner deve exigir validação, revisão ou cross-review quando a missão for crítica, quando a confiança for insuficiente ou quando a política determinar.

### Cost Optimization

O Mission Runner deve verificar orçamento antes e durante a execução, respeitar perfis de custo, bloquear uso pago não autorizado e registrar estimativas ou medições.

### Architecture Governance

O Mission Runner deve preservar separação entre missão, orquestração, workflow, política, seleção de modelo e runtime. Qualquer acoplamento direto a OpenCode, `systemd`, API ou provider deve ser tratado como risco arquitetural.

### Documentation Governance

Decisões relevantes de execução, limites, falhas, validação, revisão e rollback devem gerar logs, decision notes, Specs ou ADRs conforme impacto.

### Testing Governance

Missões que alterem código devem executar validações aplicáveis ou registrar motivo de impossibilidade. Falha de teste deve impedir conclusão automática como `done`.

### Compliance Governance

Dados sensíveis, uso externo de providers, retenção de logs, auditoria e permissões devem respeitar políticas do projeto e requisitos legais aplicáveis.

### Observability Governance

O Mission Runner deve emitir eventos estruturados de fila, ciclo, estado, custo, tokens, validação, erro, cancelamento, revisão e conclusão.

## Integração futura com Workflow Engine

O Mission Runner deve ser compatível com o Workflow Engine como componente responsável por decompor missão em fluxo de trabalho.

Contrato conceitual futuro:

```text
Mission Runner
↓
Workflow Engine
↓
Workflow Plan
↓
Task Queue
↓
Execution Results
↓
Mission Runner validation and closure
```

Regras:

1. O Mission Runner não deve embutir lógica complexa de decomposição de workflow.
2. Enquanto o Workflow Engine for parcial, o Mission Runner pode usar fluxo mínimo documentado.
3. Quando o Workflow Engine existir, o Mission Runner deve delegar planejamento e replanejamento a ele.
4. O Mission Runner mantém responsabilidade por fila, estado, limites globais, orçamento, logs e encerramento.
5. O Workflow Engine deve receber limites, políticas e critérios de aceite já resolvidos ou referenciados.

## Erros e degradação segura

O Mission Runner deve produzir erros claros para:

- Spec ausente ou não aprovada quando implementação for solicitada;
- política conflitante;
- orçamento insuficiente;
- limite de ciclos excedido;
- missão cancelada;
- validação reprovada;
- runtime indisponível;
- modelo indisponível conforme decisão do Model Selection Engine;
- permissão negada;
- path não autorizado;
- uso pago não autorizado;
- uso externo proibido;
- worktree inseguro para `auto_commit`;
- falha de log ou persistência de estado;
- tentativa de operação destrutiva sem aprovação.

Quando possível, o erro deve sugerir alternativa segura, como reduzir escopo, aumentar limite com aprovação, executar revisão manual, dividir a missão, ajustar Spec, usar fallback aprovado ou reenfileirar após correção.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Loops infinitos | Exigir `max_cycles`, retries finitos e condição de parada. |
| Execução automática insegura | Aplicar Policy Engine, bloquear ações sensíveis e exigir revisão manual. |
| Custo inesperado | Verificar orçamento por missão e ciclo, registrar estimativas e bloquear uso pago não autorizado. |
| Vazamento de segredos | Mascarar logs, restringir contexto e bloquear envio externo de dados sensíveis. |
| Auto-commit incluir mudanças externas | Limitar a arquivos da missão e bloquear worktree ambíguo. |
| Rollback apagar trabalho do usuário | Desabilitar rollback automático por padrão e exigir revisão manual. |
| Acoplamento a OpenCode | Usar Runtime Adapter conforme Spec 0003. |
| Acoplamento a systemd ou API | Tratar como modos futuros de hospedagem ou interface. |
| Workflow Engine ainda incompleto | Permitir fluxo mínimo documentado e migrar para Workflow Engine quando disponível. |
| Logs insuficientes para auditoria | Registrar estados, ciclos, decisões, validações, erros e orçamento. |

## Decisões aprovadas por esta Spec

1. Mission Runner é componente arquitetural próprio do framework.
2. Mission é unidade rastreável de intenção, execução, validação e auditoria.
3. Toda missão deve usar estados explícitos: `queued`, `running`, `done`, `failed` e `cancelled`.
4. Toda missão deve executar em ciclos finitos com limite explícito.
5. Toda missão deve ter logs auditáveis sem exposição de segredos.
6. `auto_commit` deve ser desabilitado por padrão e só permitido após validação.
7. Rollback automático deve ser desabilitado por padrão ou restrito a política explícita segura.
8. Orçamento de tokens e custo deve ser verificado antes e durante a execução.
9. Execução local é o modo inicial, mas o Mission Runner deve permitir hospedagem futura via `systemd` e interface futura via API.
10. Mission Runner deve respeitar Guardian Specs, Policy Engine, Model Selection Engine e Runtime Adapters.
11. Mission Runner deve se integrar futuramente ao Workflow Engine sem substituir sua responsabilidade.

## Critérios de aceite

- Existe uma Spec própria para o Mission Runner.
- A Spec define conceito de Mission.
- A Spec define fila de missões.
- A Spec define estados `queued`, `running`, `done`, `failed` e `cancelled`.
- A Spec define execução em ciclos.
- A Spec define limite de ciclos e condições de parada.
- A Spec define logs e auditoria.
- A Spec define política de `auto_commit`.
- A Spec define validação antes de conclusão.
- A Spec define critérios de aceite de missão.
- A Spec define rollback ou revisão manual.
- A Spec define orçamento de tokens e custo.
- A Spec define políticas de segurança.
- A Spec define execução local.
- A Spec contempla execução futura via `systemd`.
- A Spec contempla execução futura via API.
- A Spec integra Guardian Specs.
- A Spec contempla integração futura com Workflow Engine.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir schema persistente final de Mission.
- Definir storage inicial da Mission Queue.
- Definir formato de audit log estruturado.
- Definir política padrão de prioridade e concorrência.
- Definir contrato formal entre Mission Runner e Workflow Engine.
- Definir contrato formal entre Mission Runner e Runtime Adapters.
- Definir matriz padrão de `max_cycles` por tipo de missão.
- Definir política padrão de `auto_commit` por projeto.
- Definir formato de aprovação para revisão manual.
- Definir estratégia segura para rollback de arquivos, banco de dados e infraestrutura.
- Definir futura API pública do Mission Runner.
- Definir futura unidade `systemd` apenas após ADR ou Spec específica.

# Spec 0003 — OpenCode Runtime Adapter

## Status

Proposta.

## Objetivo

Definir o OpenCode Runtime Adapter como o adapter inicial de execução do Vercosa AI Framework, permitindo executar missões em OpenCode sem acoplar o núcleo do framework ao OpenCode, seus plugins, sua configuração global, seus providers ou suas APIs internas.

O OpenCode deve ser tratado como runtime inicial e laboratório operacional, não como núcleo arquitetural do framework.

## Contexto

O Vercosa AI Framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design.

As Specs 0001 e 0002 já estabelecem que:

- OpenCode será o runtime inicial, mas não o núcleo;
- agentes não devem conhecer MCPs, providers ou bancos diretamente;
- modelos não devem ser hardcoded;
- seleção de modelo deve passar pelo Model Selection Engine;
- Guardian Specs prevalecem sobre políticas locais;
- plugins externos devem ser avaliados antes do uso;
- execução automática deve respeitar políticas de segurança.

Existem decision notes aprovando OpenAI como provider principal inicial dentro do OpenCode e mantendo plugins externos desativados até validação individual. Essas decisões descrevem o estado inicial do ambiente, mas não devem virar dependência arquitetural obrigatória.

## Escopo

Esta Spec cobre:

- papel do OpenCode como runtime inicial;
- contrato conceitual de Runtime Adapter;
- execução de missões via OpenCode;
- entrada e saída esperadas;
- logs, auditoria e rastreabilidade;
- permissões e comandos sensíveis;
- integração com Model Selection Engine;
- uso de `small_model`;
- limites de execução;
- políticas para `auto_approve` e `auto_commit`;
- isolamento de plugins;
- fallback futuro para outros runtimes e interfaces;
- relação com Guardian Specs;
- riscos, mitigações e pendências.

Esta Spec não cobre:

- implementação concreta em código;
- alteração de configurações globais do OpenCode;
- uso de `sudo`;
- criação de plugins, MCPs ou agentes concretos;
- formato persistente final de logs;
- API interna definitiva do OpenCode;
- contrato detalhado de adapters para todos os runtimes futuros.

## Princípios

1. O Runtime Adapter traduz intenção do framework para um runtime concreto.
2. O Runtime Adapter não decide política arquitetural, segurança, custo ou modelo por conta própria.
3. OpenCode é substituível por outros runtimes.
4. Configuração global do usuário não deve ser alterada automaticamente.
5. Execução automática deve ser segura por padrão.
6. Plugins externos devem ser isolados e opt-in.
7. Logs devem ser úteis para auditoria sem expor segredos.
8. Falhas devem ser explícitas, recuperáveis quando possível e seguras por padrão.
9. O adapter deve respeitar limites de execução, orçamento, tokens e permissões.
10. O adapter deve preservar rastreabilidade entre missão, workflow, tarefas, agentes, modelo e entregáveis.

## Posição arquitetural

O OpenCode Runtime Adapter fica na camada externa de execução.

Fluxo conceitual:

```text
Mission
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
↓
OpenCode
↓
Providers / Tools / Filesystem / Shell
```

Agentes e subagentes não devem chamar OpenCode diretamente. Eles devem solicitar capacidades ao framework. O adapter recebe decisões já governadas por Policy Engine e Model Selection Engine e as traduz para execução no runtime.

## Definições

### Runtime Adapter

Componente que expõe um runtime concreto ao framework por meio de contrato normalizado.

Responsabilidades:

- descobrir capacidades do runtime;
- preparar contexto de execução;
- aplicar restrições recebidas do Policy Engine;
- executar tarefas ou missões no runtime;
- encaminhar decisão de modelo recebida do Model Selection Engine;
- capturar saída, logs, erros e metadados;
- reportar status de execução;
- preservar rastreabilidade.

Não responsabilidades:

- aprovar Specs;
- decidir arquitetura;
- escolher modelo sem Model Selection Engine;
- ignorar Guardian Specs;
- alterar configuração global sem aprovação explícita;
- habilitar plugins externos por conveniência;
- executar comandos destrutivos sem permissão adequada.

### OpenCode Runtime Adapter

Implementação inicial do contrato de Runtime Adapter para o OpenCode.

O adapter pode usar recursos públicos, documentados ou operacionalmente estáveis do OpenCode, mas deve encapsular detalhes específicos para que o núcleo do framework não dependa deles.

### Runtime Capability

Capacidade detectada ou declarada por um runtime.

Exemplos:

- execução de comandos de shell;
- leitura e edição de arquivos;
- uso de subagentes;
- uso de tools;
- providers de LLM disponíveis;
- modelos disponíveis;
- suporte a `small_model`;
- permissões configuradas;
- plugins ativos;
- modo interativo ou não interativo;
- suporte a logs estruturados;
- suporte a execução headless.

## Contrato de Runtime Adapter

O contrato conceitual mínimo deve conter as seguintes operações:

### `detect_runtime()`

Detecta presença, versão e capacidades básicas do runtime.

Entrada mínima:

- workspace;
- ambiente de execução;
- restrições de política.

Saída mínima:

- `runtime_id`;
- `runtime_name`;
- `runtime_version` quando disponível;
- `available`;
- `capabilities`;
- `limitations`;
- `security_warnings`.

### `list_models()`

Lista modelos e providers expostos pelo runtime quando possível.

Esta operação alimenta o Model Registry definido pela Spec 0002, mas não substitui o Model Selection Engine.

Saída mínima:

- provider;
- model;
- availability;
- pricing class quando disponível;
- context window quando disponível;
- suporte a tool use quando disponível;
- indicação de modelo leve quando disponível;
- limitações conhecidas.

### `prepare_execution()`

Prepara uma execução governada por política.

Entrada mínima:

- `mission_id`;
- `workflow_id`;
- `task_id` quando aplicável;
- workspace;
- contexto permitido;
- permissões efetivas;
- decisão de modelo;
- limites de execução;
- política de logs;
- política de plugins;
- política de aprovação.

Saída mínima:

- plano de execução normalizado;
- contexto efetivamente incluído;
- permissões concedidas;
- plugins permitidos;
- modelo selecionado;
- limites aplicados;
- bloqueios ou aprovações exigidas.

### `execute_mission()`

Executa uma missão ou etapa de missão no runtime.

Entrada mínima:

- missão normalizada;
- estado do workflow;
- tarefas autorizadas;
- decisão de modelo;
- contexto autorizado;
- permissões;
- limites;
- estratégia de fallback.

Saída mínima:

- status;
- artefatos produzidos;
- arquivos alterados quando aplicável;
- comandos executados quando permitido registrar;
- modelo usado;
- fallback usado;
- logs normalizados;
- erros;
- recomendações de revisão.

### `execute_task()`

Executa uma tarefa específica derivada de uma missão.

Deve seguir o mesmo modelo de entrada e saída de `execute_mission()`, mas com escopo menor, limite mais restrito e rastreabilidade para `task_id`.

### `collect_logs()`

Coleta logs estruturados e metadados úteis sem expor segredos.

Saída mínima:

- `mission_id`;
- `workflow_id`;
- `task_id`;
- runtime;
- provider;
- model;
- timestamps;
- duração;
- status;
- eventos;
- warnings;
- erros;
- estimativa ou medição de tokens quando disponível;
- estimativa ou medição de custo quando disponível;
- decisões de aprovação;
- fallback aplicado.

### `stop_execution()`

Solicita parada segura de uma execução em andamento.

Deve preservar logs parciais e estado recuperável quando possível.

### `validate_artifacts()`

Valida se os artefatos esperados foram produzidos.

Não substitui testes, revisão humana ou Guardian Specs. Apenas confirma entregáveis esperados e estado operacional.

## Execução de missões

O OpenCode Runtime Adapter deve executar missões somente depois que o framework tiver:

1. identificado a missão;
2. localizado ou criado a Spec aplicável quando necessário;
3. decomposto a missão em workflow e tarefas;
4. aplicado Policy Engine e Guardian Specs;
5. solicitado decisão ao Model Selection Engine;
6. definido permissões e limites;
7. preparado contexto mínimo necessário;
8. registrado condições de parada.

Execução conceitual:

```text
Mission Request
↓
Policy Resolution
↓
Model Selection Decision
↓
Runtime Preparation
↓
OpenCode Execution
↓
Artifact Collection
↓
Validation
↓
Audit Log
```

O adapter deve preferir execução incremental por tarefa quando isso reduzir risco, custo, tokens ou blast radius.

## Entrada esperada

Uma entrada normalizada para o OpenCode Runtime Adapter deve conter, no mínimo:

- `mission_id`;
- `mission_title`;
- `mission_goal`;
- `spec_refs`;
- `guardian_refs`;
- `workflow_id`;
- `task_ids`;
- `workspace`;
- `allowed_paths`;
- `denied_paths`;
- `context_bundle`;
- `selection_request`;
- `selection_decision`;
- `permissions_policy`;
- `approval_policy`;
- `commit_policy`;
- `plugin_policy`;
- `execution_limits`;
- `logging_policy`;
- `fallback_policy`;
- `stop_conditions`.

## Saída esperada

Uma saída normalizada do OpenCode Runtime Adapter deve conter, no mínimo:

- `mission_id`;
- `workflow_id`;
- `task_id` quando aplicável;
- `runtime_id`;
- `runtime_status`;
- `started_at`;
- `finished_at`;
- `duration_ms`;
- `selected_model`;
- `selected_provider`;
- `small_model_used`;
- `fallback_used`;
- `artifacts`;
- `changed_files`;
- `commands_executed` quando permitido;
- `tests_executed` quando aplicável;
- `validation_results`;
- `approval_events`;
- `commit_result` quando aplicável;
- `token_usage` quando disponível;
- `cost_estimate` ou `cost_actual` quando disponível;
- `warnings`;
- `errors`;
- `requires_review`;
- `audit_log_ref`.

## Logs e auditoria

O adapter deve registrar eventos suficientes para rastrear o que foi executado, por qual decisão e com quais limites.

Eventos mínimos desejados:

- início e fim da execução;
- runtime detectado;
- versão do runtime quando disponível;
- decisão do Model Selection Engine;
- modelo efetivamente usado;
- fallback aplicado;
- permissões concedidas;
- comandos sensíveis bloqueados ou aprovados;
- arquivos alterados;
- testes ou validações executadas;
- erros e warnings;
- uso estimado ou real de tokens;
- custo estimado ou real;
- plugins carregados ou bloqueados;
- decisões de `auto_approve` e `auto_commit`.

Regras:

1. Logs não podem conter segredos.
2. Logs não devem conter conteúdo sensível desnecessário.
3. Prompts completos só devem ser registrados quando a política permitir.
4. `.env`, chaves, tokens e credenciais devem ser mascarados ou omitidos.
5. Logs devem referenciar artefatos por caminho ou hash quando possível.
6. Falhas devem conter causa explicável e próxima ação segura.

## Permissões

Permissões devem ser explícitas e derivadas do Policy Engine.

Categorias mínimas:

- leitura de arquivos;
- escrita de arquivos;
- execução de comandos;
- acesso à rede;
- acesso a providers externos;
- leitura de arquivos sensíveis;
- uso de MCPs;
- uso de plugins;
- alteração de configuração local;
- alteração de configuração global;
- operações Git;
- operações destrutivas.

Regras:

1. Alteração de configuração global deve ser bloqueada por padrão.
2. Leitura de `.env` deve exigir confirmação explícita.
3. Comandos destrutivos devem exigir confirmação explícita.
4. Uso de provider externo em contexto sensível deve exigir política permissiva ou aprovação humana.
5. Acesso à rede deve ser registrável e restrito quando a missão exigir privacidade local.
6. MCPs devem passar por safety review antes de uso.
7. Plugins externos devem ser desativados por padrão até validação.
8. Permissões concedidas ao OpenCode não podem exceder as permissões aprovadas para a missão.

## Seleção de modelo

O OpenCode Runtime Adapter não escolhe modelos diretamente.

Fluxo obrigatório:

1. O framework cria um `Selection Request` conforme a Spec 0002.
2. O Model Selection Engine consulta Model Registry e adapters disponíveis.
3. O OpenCode Runtime Adapter pode fornecer inventário de modelos ao registry.
4. O Model Selection Engine emite uma `Selection Decision`.
5. O OpenCode Runtime Adapter executa usando o modelo e provider aprovados quando suportado pelo runtime.
6. Se o runtime não conseguir usar a decisão, o adapter reporta falha ou solicita fallback ao framework.

O adapter não deve substituir a decisão de modelo silenciosamente.

## Uso de `small_model`

O adapter deve suportar a política `small_model` definida na Spec 0002.

Usos permitidos:

- classificação simples;
- roteamento de intenção;
- sumarização curta;
- extração estruturada simples;
- validação mecânica;
- geração de metadados;
- pré-análise antes de escalar para modelo superior.

Regras:

1. `small_model` só deve ser usado quando autorizado pela decisão do Model Selection Engine.
2. `small_model` não deve aprovar entregas críticas sozinho.
3. Resultado de `small_model` deve escalar para modelo superior quando houver baixa confiança.
4. O adapter deve registrar quando `small_model` foi usado.
5. Se o OpenCode não expuser um modelo leve compatível, o adapter deve reportar limitação em vez de escolher outro modelo por conta própria.

## Limites de execução

Toda execução deve ter limites explícitos.

Limites mínimos desejados:

- tempo máximo por missão;
- tempo máximo por tarefa;
- número máximo de iterações;
- número máximo de chamadas a modelo;
- limite de tokens por tarefa;
- limite de custo por missão;
- número máximo de comandos de shell;
- número máximo de arquivos alterados;
- tamanho máximo de diff;
- paths permitidos e negados;
- limite de tentativas de fallback;
- limite de retries;
- condição de parada do loop.

Regras:

1. Todo loop precisa de condição de parada.
2. Retries devem ter limite e motivo registrado.
3. Fallback não pode ser infinito.
4. Ao atingir limite, o adapter deve parar com erro explicável e preservar estado.
5. Limites podem ser mais restritivos por tarefa do que por missão.

## Auto-approve

`auto_approve` é a política que permite ao runtime prosseguir sem confirmação humana para ações de baixo risco previamente autorizadas.

Estados mínimos:

- `disabled`;
- `safe_actions_only`;
- `policy_controlled`.

Regras:

1. `auto_approve` deve ser desabilitado por padrão para ações sensíveis.
2. `auto_approve` nunca deve autorizar leitura de segredos, alteração global, comando destrutivo, uso pago não autorizado ou envio externo de dados sensíveis.
3. Ações permitidas por `auto_approve` devem estar listadas na política da missão.
4. Toda aprovação automática deve ser registrada.
5. Se houver dúvida de classificação de risco, exigir aprovação humana.

## Auto-commit

`auto_commit` é a política que permite criar commits automaticamente após validação.

Estados mínimos:

- `disabled`;
- `after_validation`;
- `manual_approval_required`.

Regras:

1. `auto_commit` deve ser desabilitado por padrão.
2. `auto_commit` só pode operar em arquivos alterados pela missão atual.
3. Commits automáticos devem exigir validação mínima definida pela Spec ou workflow.
4. Commits automáticos não podem incluir segredos, arquivos `.env`, credenciais ou mudanças não relacionadas.
5. O adapter deve registrar arquivos incluídos, mensagem de commit e validações executadas.
6. Se o worktree tiver mudanças não relacionadas, o adapter deve evitar incluí-las e registrar o risco.
7. Push automático está fora do escopo desta Spec e deve exigir decisão própria.

## Isolamento de plugins

Plugins do OpenCode devem ser tratados como superfície de ataque e fonte de variabilidade operacional.

Política inicial:

- plugins externos desativados por padrão;
- plugins globais não devem ser assumidos como parte do framework;
- plugins necessários devem ser declarados por missão, projeto ou ADR;
- cada plugin deve passar por review de segurança, permissões e supply chain;
- plugins aprovados devem ter versão, origem e finalidade registradas;
- falha causada por plugin deve ser isolada do núcleo do framework.

Regras:

1. O adapter deve detectar e registrar plugins ativos quando possível.
2. Plugins desconhecidos devem gerar warning ou bloqueio conforme política.
3. Plugins não podem ampliar permissões aprovadas para a missão.
4. Plugins não devem acessar segredos sem autorização explícita.
5. Recursos inspirados no ECC podem ser reaproveitados futuramente, mas devem ser adaptados e validados, não copiados cegamente.

## Fallback para runtimes futuros

O contrato de Runtime Adapter deve permitir implementação futura para:

- Claude Code;
- Codex CLI;
- Cursor;
- VS Code;
- JetBrains;
- Web UI;
- API.

Regras:

1. Nenhum workflow deve depender de comportamento exclusivo do OpenCode sem abstração.
2. Capacidades específicas do OpenCode devem ser declaradas como capability opcional.
3. O núcleo deve falar com `Runtime Adapter`, não com OpenCode.
4. Fallback entre runtimes deve preservar política, segurança, logs, limites e decisão de modelo.
5. Se um runtime futuro não suportar determinada capability, o framework deve degradar com erro explicável ou escolher workflow alternativo.

## Relação com Guardian Specs

### Security by Design

O adapter deve bloquear segredos em logs, exigir confirmação para `.env`, tratar MCPs e plugins como superfície de ataque, exigir confirmação para comandos destrutivos e documentar decisões de risco.

### Token Efficiency

O adapter deve receber contexto mínimo necessário, evitar envio redundante, favorecer execução incremental e registrar tokens quando disponível.

### AI Quality Assurance

O adapter deve preservar validação, revisão, condições de parada e auditabilidade. Tarefas críticas devem exigir revisão ou cross-review quando a política determinar.

### Cost Optimization

O adapter deve respeitar orçamento, registrar uso quando possível, evitar chamadas repetidas e usar modelos gratuitos, locais ou leves quando a política e o Model Selection Engine determinarem.

### Architecture Governance

O adapter deve manter separação entre núcleo, políticas, seleção de modelo e runtime. Qualquer acoplamento direto ao OpenCode fora do adapter deve ser tratado como risco arquitetural.

### Documentation Governance

Mudanças relevantes de runtime, provider, plugin, permissão ou fallback devem ser documentadas em Spec, ADR ou decision note conforme impacto.

### Testing Governance

Execuções que alterem código devem reportar testes ou validações executadas. Quando testes não forem possíveis, o motivo deve ser registrado.

### Compliance Governance

Dados sensíveis, privacidade local obrigatória, uso externo de providers e logs devem respeitar políticas de compliance do projeto.

### Observability Governance

O adapter deve emitir eventos de execução, erro, fallback, custo, tokens e aprovações de forma auditável sem expor dados sensíveis.

## Erros e degradação segura

O adapter deve produzir erros claros para:

- OpenCode indisponível;
- versão incompatível;
- modelo selecionado indisponível no runtime;
- provider indisponível;
- política conflitante;
- permissão negada;
- plugin não aprovado;
- limite excedido;
- comando bloqueado;
- path não autorizado;
- uso pago não autorizado;
- uso externo proibido;
- contexto maior que limite permitido;
- falha de validação;
- worktree inseguro para auto-commit.

Quando possível, a resposta deve sugerir alternativa segura, como reduzir contexto, solicitar aprovação humana, usar fallback aprovado, desabilitar plugin, dividir a missão ou executar validação manual.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Acoplamento do framework ao OpenCode | Manter contrato de Runtime Adapter e encapsular APIs específicas. |
| Plugins globais alterarem comportamento | Desativar por padrão, detectar plugins ativos e exigir review. |
| Modelo ser escolhido fora do Model Selection Engine | Exigir `Selection Decision` e registrar modelo efetivo. |
| Vazamento de segredos em logs ou prompts | Mascarar, omitir dados sensíveis e exigir confirmação para `.env`. |
| Auto-approve executar ação sensível | Bloquear ações sensíveis por padrão e registrar aprovações. |
| Auto-commit incluir mudanças não relacionadas | Limitar a arquivos da missão, validar diff e bloquear worktree ambíguo. |
| Custos inesperados com modelos pagos | Respeitar orçamento, usar Model Selection Engine e registrar estimativas. |
| Loops sem fim | Exigir limites, retries finitos e condições de parada. |
| Fallback violar privacidade | Aplicar Policy Engine antes de qualquer fallback. |
| Runtime futuro não suportar capability | Declarar capabilities opcionais e degradar com erro explicável. |
| Comportamento diferente entre ambientes | Detectar ambiente, runtime e capacidades antes da execução. |
| Dependência de configuração global do usuário | Preferir configuração de projeto e não alterar global sem aprovação. |

## Decisões aprovadas por esta Spec

1. OpenCode é o Runtime Adapter inicial, não o núcleo do framework.
2. Runtime Adapter é contrato arquitetural próprio do framework.
3. OpenCode Runtime Adapter deve executar decisões governadas pelo Policy Engine e Model Selection Engine.
4. O adapter não escolhe modelo diretamente e não substitui decisão silenciosamente.
5. `small_model` só deve ser usado quando autorizado pelo Model Selection Engine.
6. Execuções devem ter limites explícitos e condições de parada.
7. `auto_approve` deve ser restrito e seguro por padrão.
8. `auto_commit` deve ser desabilitado por padrão e só permitido após validação e política explícita.
9. Plugins externos devem ser isolados, desativados por padrão e validados antes do uso.
10. Configurações globais não devem ser alteradas automaticamente.
11. O contrato deve permitir futuros adapters para Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.
12. Logs devem ser auditáveis sem expor segredos.

## Critérios de aceite

- Existe uma Spec própria para o OpenCode Runtime Adapter.
- A Spec define OpenCode como runtime inicial, não como núcleo.
- A Spec define contrato conceitual de Runtime Adapter.
- A Spec define execução de missões via runtime.
- A Spec define entrada e saída esperadas.
- A Spec define logs, auditoria e rastreabilidade.
- A Spec define permissões e ações sensíveis.
- A Spec integra seleção de modelo via Model Selection Engine.
- A Spec contempla uso de `small_model`.
- A Spec define limites de execução e condições de parada.
- A Spec define política de `auto_approve`.
- A Spec define política de `auto_commit`.
- A Spec define isolamento de plugins.
- A Spec contempla fallback futuro para Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.
- A Spec relaciona o adapter com Guardian Specs.
- A Spec documenta riscos e mitigações.
- A Spec registra pendências quando decisões ainda não existem.

## Pendências

- Definir schema final de `Runtime Adapter` em código ou IDL.
- Definir formato persistente de logs e audit trail.
- Definir onde o Model Registry será armazenado.
- Definir mecanismo concreto de descoberta de modelos no OpenCode.
- Definir como configurar modelo principal e `small_model` sem alterar configuração global.
- Definir matriz formal de permissões por tipo de missão.
- Definir política padrão de `auto_approve` por ambiente.
- Definir política padrão de `auto_commit` por projeto.
- Definir formato de isolamento de plugins por workspace.
- Definir processo de review para plugins derivados do ECC.
- Definir ADR para fronteira entre Mission Orchestrator, Runtime Adapter e Agent Orchestrator se houver divergência futura.
- Definir contrato mínimo comum para adapters futuros de Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.

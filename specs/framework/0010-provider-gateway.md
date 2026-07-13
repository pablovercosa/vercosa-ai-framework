# Spec 0010 — Provider / MCP / API Gateway

## Status

Proposta.

## Objetivo

Definir o Provider Gateway do Vercosa AI Framework como a camada de isolamento entre Tools e infraestrutura externa, incluindo Providers, MCPs, APIs HTTP, CLIs locais, bancos, filesystem, serviços locais e runtimes.

Esta Spec estabelece que Tools não devem conhecer detalhes internos de providers concretos. Tools devem emitir requisições normalizadas ao Provider Gateway, e o Gateway deve resolver, validar, governar, executar ou simular a chamada por meio de Provider Adapters autorizados.

## Contexto

As Specs 0001 e 0009 e a arquitetura central definem que:

- o framework é Specification First, Provider Agnostic, Local First, Security by Design, Extensible by Design e Governance by Design;
- OpenCode é runtime inicial, não núcleo;
- agentes não devem conhecer MCPs, APIs, bancos, filesystem ou providers diretamente;
- Agents e Subagents solicitam Capabilities;
- Capabilities são implementadas por Skills;
- Skills usam Tools;
- Tools acessam infraestrutura externa;
- Providers, MCPs e APIs ficam na camada externa;
- Guardian Engine governa ações sensíveis, permissões, segredos, risco e bloqueios;
- Tool Executor é a fronteira de execução governada de Tools.

A Spec 0009 define que Tool é a unidade concreta de execução usada por Skill. Esta Spec detalha a camada imediatamente abaixo da Tool: o Provider Gateway.

## Escopo

Esta Spec cobre:

- diferença entre Tool, Provider, MCP e API;
- regra de que Tool não deve conhecer detalhes internos de provider;
- Provider Gateway como camada de isolamento;
- MCP como uma forma de provider, não como núcleo;
- suporte futuro a APIs HTTP, CLIs locais, MCPs, bancos, filesystem e serviços locais;
- Provider Registry;
- Provider Adapter;
- ProviderRequest;
- ProviderResult;
- permissões;
- integração com Guardian Engine;
- integração com Tool Executor;
- logs e rastreabilidade;
- bloqueio de providers perigosos;
- redaction de segredos;
- `dry_run`;
- timeout;
- retries;
- fallback entre providers;
- provider agnostic;
- OpenCode como runtime inicial, não núcleo;
- riscos, mitigações, decisões e critérios de aceite.

Esta Spec não cobre:

- implementação concreta em código;
- schema persistente final;
- criação de adapters específicos;
- criação de MCPs;
- criação de cliente HTTP, subprocess runner, driver de banco ou filesystem real;
- alteração de configurações globais;
- uso de `sudo`;
- execução real de comandos, providers, MCPs, APIs, bancos, filesystem ou serviços locais;
- catálogo final de providers suportados.

## Princípios

1. Tool declara intenção técnica limitada; Provider Gateway resolve provider concreto.
2. Tool não conhece endpoint, comando, driver, protocolo, segredo ou detalhe interno do provider.
3. Provider Gateway isola providers concretos atrás de contrato normalizado.
4. MCP é um tipo de provider adapter, não a arquitetura central.
5. Provider Registry descreve providers de forma declarativa e auditável.
6. Provider Adapter encapsula protocolo e mecanismo concreto.
7. Toda chamada sensível deve passar por permissões, Guardian Engine e logs.
8. Segredos nunca devem aparecer em logs, erros, traces ou resultados entregues ao agente.
9. Fallback entre providers não pode ampliar permissões, custo, rede, escopo ou exposição de dados sem nova avaliação.
10. OpenCode pode hospedar adapters iniciais, mas não define contratos centrais.

## Posição arquitetural

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
Agents / Subagents
↓
Capabilities
↓
Skills
↓
Tool Executor
↓
Tools
↓
Provider Gateway
↓
Provider Registry / Provider Adapter
↓
Providers / MCPs / APIs / bancos / filesystem / CLIs / serviços locais / runtimes
```

Regras:

1. Agent, Subagent, Capability e Skill não devem chamar Provider Gateway diretamente.
2. Tool Executor valida e governa Tool antes de qualquer chamada ao Provider Gateway.
3. Tool envia ao Provider Gateway uma `ProviderRequest` normalizada, sem detalhes secretos ou específicos de protocolo.
4. Provider Gateway seleciona Provider Adapter compatível conforme Provider Registry, permissões, ambiente, política e Guardian Engine.
5. Provider Adapter executa ou simula a chamada concreta e retorna `ProviderResult` normalizado.
6. Tool transforma `ProviderResult` em `ToolExecutionResult` sem expor detalhes internos desnecessários ao agente.

## Definições

### Tool

Tool é a unidade concreta de execução usada por uma Skill para solicitar uma operação autorizada.

Uma Tool responde à pergunta: `qual operação técnica a Skill precisa executar?`

Exemplos:

- buscar texto em documentos;
- consultar índice semântico;
- ler arquivo permitido;
- enviar requisição de issue;
- gerar embedding;
- executar validação local permitida.

Regras:

1. Tool deve depender de contrato de provider, não de implementação específica.
2. Tool não deve conter URL final, comando shell bruto, DSN, token, segredo, driver específico ou detalhes internos de MCP.
3. Tool pode declarar `provider_ref`, `provider_type`, efeitos, permissões, timeout, retry e fallback desejados em seu perfil.
4. Tool deve validar entrada antes de solicitar Provider Gateway.
5. Tool deve tratar `ProviderResult` como dado não confiável até normalização e validação.
6. Tool não deve escolher provider perigoso, deprecated ou externo sem autorização.

### Provider

Provider é qualquer mecanismo externo ou local capaz de cumprir uma operação solicitada por Tool por meio do Provider Gateway.

Uma Provider responde à pergunta: `qual capacidade de infraestrutura existe e pode ser acionada?`

Tipos previstos:

- `http_api`;
- `local_cli`;
- `mcp_server`;
- `database`;
- `vector_database`;
- `filesystem`;
- `local_service`;
- `runtime_tool`;
- `llm_provider`;
- `embedding_provider`;
- `message_queue`;
- `custom_adapter`.

Regras:

1. Provider é infraestrutura, não Capability, Skill ou Agent.
2. Provider deve ser registrado antes de uso automático.
3. Provider deve declarar efeitos, permissões, sensibilidade de dados, rede, custo e limites.
4. Provider pode ser local, remoto, pago, gratuito, offline, experimental, deprecated ou perigoso.
5. Provider perigoso deve ser bloqueado por padrão.
6. Provider externo só pode receber dados sensíveis quando política permitir explicitamente.

### MCP

MCP é uma forma padronizada de expor ferramentas ou contexto por um servidor compatível com Model Context Protocol.

No Vercosa AI Framework, MCP responde à pergunta: `este provider usa o protocolo MCP?`

Regras:

1. MCP é um tipo de provider, não o núcleo do framework.
2. MCP não deve ser conhecido diretamente por Agent ou Skill.
3. MCP deve ser acessado por Provider Adapter governado.
4. MCP específico do OpenCode deve ser tratado como provider do Runtime Adapter ou Provider Adapter, não como contrato central.
5. Trocar MCP por API HTTP, CLI local, banco ou serviço local não deve mudar Capability nem Agent quando o contrato funcional for preservado.

### API

API é uma interface externa ou local com contrato de chamada definido, normalmente HTTP, mas não limitada a HTTP.

Regras:

1. API é provider quando acionada pelo Provider Gateway.
2. Tool não deve hardcodar endpoint, autenticação, headers sensíveis ou formato interno da API.
3. Provider Adapter deve encapsular autenticação, serialização, desserialização, paginação, rate limit e erros específicos.
4. API com rede externa deve exigir permissão `network_access` e, quando aplicável, `provider_external_access` e `cost_incur`.

## Provider Gateway

Provider Gateway é a camada responsável por receber `ProviderRequest`, selecionar Provider Adapter autorizado, aplicar governança e retornar `ProviderResult` normalizado.

Responsabilidades:

- isolar Tools de detalhes concretos de providers;
- consultar Provider Registry;
- validar permissões, efeitos, limites e disponibilidade;
- consultar Guardian Engine quando houver risco;
- aplicar redaction de segredos antes de logs;
- honrar `dry_run`;
- aplicar timeout;
- aplicar retries conforme política;
- avaliar fallback entre providers;
- bloquear providers perigosos, deprecated, indisponíveis ou não autorizados;
- emitir logs estruturados;
- preservar rastreabilidade Tool -> Provider Gateway -> Provider Adapter -> Provider.

Não responsabilidades:

- resolver Capability para Skill;
- escolher Skill;
- substituir Tool Executor;
- expor provider diretamente a agentes;
- guardar segredos em claro;
- modificar configurações globais;
- executar ações privilegiadas por padrão.

Regras:

1. Provider Gateway deve falhar de forma segura quando não houver provider autorizado.
2. Provider Gateway não deve degradar silenciosamente para provider mais permissivo.
3. Provider Gateway deve registrar motivo de seleção, bloqueio, retry e fallback.
4. Provider Gateway deve retornar erros estruturados, sem stack traces sensíveis ao agente.
5. Provider Gateway deve permitir execução determinística e auditável sempre que possível.

## Provider Registry

Provider Registry é o catálogo governado de providers disponíveis.

Responsabilidades:

- registrar providers com IDs estáveis e versões;
- declarar tipo de provider;
- declarar capabilities técnicas suportadas;
- declarar operações suportadas;
- declarar efeitos possíveis;
- declarar permissões mínimas;
- declarar limites de rede, custo, timeout e retry;
- declarar sensibilidade de dados permitida;
- declarar se provider é local ou externo;
- declarar disponibilidade por ambiente;
- declarar status: estável, experimental, deprecated, perigoso ou bloqueado;
- declarar adapters compatíveis;
- declarar providers de fallback permitidos.

Não responsabilidades:

- executar providers;
- resolver Skills;
- acessar segredos diretamente;
- aprovar ações sensíveis sozinho;
- substituir Guardian Engine.

Campos mínimos desejados:

- `provider_id`;
- `name`;
- `version`;
- `provider_type`;
- `description`;
- `adapter_ref`;
- `supported_operations`;
- `supported_domains`;
- `effects`;
- `required_permissions`;
- `network_policy`;
- `data_sensitivity_allowed`;
- `secret_refs`;
- `default_timeout`;
- `retry_policy`;
- `fallback_providers`;
- `cost_policy`;
- `rate_limit_policy`;
- `locality`;
- `availability`;
- `dangerous`;
- `experimental`;
- `deprecated`;
- `blocked`;
- `guardian_policy_refs`;
- `audit_log_ref`.

Regras:

1. Provider Registry deve separar metadados públicos de segredos.
2. `secret_refs` devem apontar para mecanismo seguro de resolução de segredos, nunca conter valores secretos.
3. Provider bloqueado não pode ser selecionado automaticamente.
4. Provider perigoso exige decisão explícita de Guardian Engine e aprovação quando política exigir.
5. Provider experimental não deve ser usado em tarefas críticas sem política explícita.
6. Provider deprecated não deve ser preferido quando houver alternativa estável compatível.
7. Registro ou alteração incompatível de provider crítico deve exigir Spec, ADR ou decisão rastreável conforme impacto.

## Provider Adapter

Provider Adapter é o componente que encapsula o mecanismo concreto de comunicação com um provider.

Responsabilidades:

- traduzir `ProviderRequest` para chamada concreta;
- executar ou simular chamada conforme `dry_run`;
- aplicar autenticação sem expor segredos;
- tratar protocolo, endpoint, driver, comando, cliente, MCP ou SDK específico;
- normalizar resposta em `ProviderResult`;
- mapear erros específicos para erros estruturados;
- respeitar timeout e cancelamento;
- cooperar com retries definidos pelo Gateway;
- redigir segredos em mensagens, logs e erros.

Não responsabilidades:

- conceder permissões;
- decidir política de alto nível;
- escolher Skill ou Tool;
- alterar escopo de dados enviado;
- executar fallback sem Provider Gateway;
- vazar detalhes internos ao agente.

Tipos iniciais previstos de adapter:

- `HttpApiProviderAdapter`;
- `LocalCliProviderAdapter`;
- `McpProviderAdapter`;
- `DatabaseProviderAdapter`;
- `FilesystemProviderAdapter`;
- `LocalServiceProviderAdapter`;
- `RuntimeProviderAdapter`;
- `LlmProviderAdapter`;
- `EmbeddingProviderAdapter`.

Regras:

1. Adapter deve ser injetável e testável por contrato.
2. Adapter não deve ler segredos sem `secret_read` ou mecanismo autorizado equivalente.
3. Adapter não deve executar comando shell livre derivado de contexto não confiável.
4. Adapter de CLI local deve usar argumentos estruturados, não interpolação insegura.
5. Adapter de filesystem deve respeitar `allowed_paths` e bloquear path traversal.
6. Adapter HTTP deve respeitar allowlist, rate limit, timeout, TLS e política de rede quando definidos.
7. Adapter MCP deve mapear tools MCP para operações de provider sem expor MCP diretamente ao agente.

## ProviderRequest

ProviderRequest é a requisição normalizada emitida por Tool para o Provider Gateway.

Campos mínimos desejados:

- `provider_request_id`;
- `tool_execution_request_id`;
- `mission_id`;
- `workflow_id`;
- `task_id`;
- `attempt_id`;
- `agent_assignment_id`;
- `skill_id`;
- `tool_id`;
- `provider_ref` opcional;
- `provider_type` opcional;
- `operation`;
- `inputs`;
- `input_schema_ref`;
- `expected_output_schema_ref`;
- `granted_permissions`;
- `allowed_effects`;
- `allowed_paths`;
- `data_sensitivity`;
- `network_policy`;
- `budget_policy`;
- `timeout`;
- `retry_policy`;
- `fallback_allowed`;
- `dry_run`;
- `guardian_decision_refs`;
- `metadata`.

Regras:

1. ProviderRequest deve carregar contexto suficiente para auditoria e Guardian Engine.
2. ProviderRequest não deve conter segredos em claro.
3. ProviderRequest deve declarar permissões concedidas, não permissões desejadas sem autorização.
4. ProviderRequest deve declarar `dry_run` explicitamente.
5. ProviderRequest deve declarar limites de timeout e retry.
6. ProviderRequest deve distinguir `provider_ref` obrigatório de seleção automática por `provider_type`.
7. Inputs vindos de contexto não confiável devem ser marcados ou encapsulados como dados, não instruções.

## ProviderResult

ProviderResult é o retorno normalizado do Provider Gateway para Tool.

Campos mínimos desejados:

- `provider_request_id`;
- `provider_result_id`;
- `provider_id`;
- `adapter_ref`;
- `operation`;
- `success`;
- `status`;
- `outputs`;
- `normalized_output_schema_ref`;
- `evidence_refs`;
- `artifact_refs`;
- `warnings`;
- `errors`;
- `blocked_reason`;
- `fallback_from`;
- `fallback_to`;
- `retry_count`;
- `timeout_applied`;
- `cost_used`;
- `rate_limit_state`;
- `guardian_decision_refs`;
- `redactions_applied`;
- `audit_log_ref`;
- `started_at`;
- `finished_at`;
- `metadata`.

Regras:

1. ProviderResult deve ser normalizado antes de retornar à Tool.
2. ProviderResult não deve conter segredos.
3. ProviderResult deve diferenciar falha, bloqueio, timeout, retry esgotado e fallback aplicado.
4. ProviderResult deve preservar referências auditáveis de evidências e artefatos.
5. ProviderResult deve permitir que Tool construa `ToolExecutionResult` sem expor detalhes internos do provider ao agente.

## Permissões

Permissões devem ser herdadas da Assignment e propagadas por Capability, Skill, Tool e ProviderRequest.

Categorias mínimas aplicáveis ao Provider Gateway:

- `network_access`;
- `provider_external_access`;
- `local_service_access`;
- `mcp_access`;
- `database_read`;
- `database_write`;
- `filesystem_read`;
- `filesystem_write`;
- `execute_command`;
- `secret_read`;
- `cost_incur`;
- `modify_global_config`;
- `privileged_execution`.

Regras:

1. Permissão não declarada deve ser tratada como negada.
2. Provider Gateway não pode conceder permissão ausente na ProviderRequest.
3. Provider Adapter não pode ampliar permissões recebidas do Gateway.
4. `modify_global_config` e `privileged_execution` devem ser bloqueadas por padrão.
5. `sudo` deve ser bloqueado por padrão.
6. Acesso a segredo deve usar referência, mínimo privilégio e redaction obrigatória.
7. Fallback não pode adicionar permissões sem nova avaliação do Guardian Engine.
8. Retry não pode repetir ação destrutiva sem política explícita de idempotência.

## Integração com Guardian Engine

Guardian Engine deve avaliar chamadas de provider quando houver risco, rede, segredo, custo, escrita, comando, banco, filesystem, MCP, provider externo, fallback, retry sensível ou provider perigoso.

Pontos mínimos de avaliação:

- antes de selecionar provider externo;
- antes de usar provider perigoso, experimental ou deprecated em tarefa sensível;
- antes de resolver segredo;
- antes de enviar dados sensíveis para provider externo;
- antes de executar CLI local;
- antes de escrever em banco ou filesystem;
- antes de acessar MCP;
- antes de fallback que mude provider, localidade, custo, rede ou exposição de dados;
- antes de retry de operação não idempotente ou sensível;
- antes de aceitar output de provider não confiável para ação sensível subsequente.

Contexto mínimo enviado ao Guardian Engine:

- `mission_id`;
- `evaluation_type` como `provider_request` ou equivalente;
- `tool_id`;
- `provider_id` ou critérios de seleção;
- `provider_type`;
- `operation`;
- `effects`;
- `required_permissions`;
- `granted_permissions`;
- `data_sensitivity`;
- `network_policy`;
- `budget_policy`;
- `target_paths` quando aplicável;
- `planned_command` quando aplicável;
- `dry_run`;
- `fallback_context` quando aplicável;
- `prior_decision_refs`.

Decisões esperadas:

- `allow`: continuar conforme limites;
- `warn`: continuar se política permitir e registrar warning;
- `require_approval`: bloquear execução automática até aprovação;
- `block`: impedir seleção ou execução.

Regras:

1. Decisão `block` deve impedir chamada ao adapter.
2. Decisão `require_approval` deve impedir execução automática.
3. Falha do Guardian Engine deve bloquear execução automática de alto risco.
4. Redactions determinadas pelo Guardian Engine devem ser aplicadas antes de logs e resultados.
5. Provider Gateway deve registrar `guardian_decision_ref` em ProviderResult.

## Integração com Tool Executor

Tool Executor continua sendo a camada responsável por validar e governar execução de Tool.

Contrato conceitual:

```text
Tool Executor
↓ valida ToolExecutionRequest e ToolProfile
Tool
↓ cria ProviderRequest normalizada
Provider Gateway
↓ seleciona e aciona Provider Adapter autorizado
ProviderResult
↓
Tool
↓ normaliza para ToolExecutionResult
Tool Executor
```

Regras:

1. Tool Executor não deve chamar provider diretamente.
2. Tool não deve contornar Provider Gateway para acessar provider concreto.
3. Provider Gateway não substitui validações do Tool Executor; ele adiciona governança no nível de provider.
4. `dry_run` recebido em ToolExecutionRequest deve ser propagado para ProviderRequest.
5. Bloqueio no Provider Gateway deve resultar em ToolExecutionResult falho, rastreável e sem efeito externo.
6. Logs devem permitir reconstruir `ToolExecutionRequest -> ProviderRequest -> ProviderResult -> ToolExecutionResult`.

## Logs

Eventos mínimos:

- ProviderRequest criada;
- Provider Registry consultado;
- provider candidato selecionado;
- provider candidato bloqueado;
- Guardian Engine consultado;
- segredo solicitado por referência;
- redaction aplicada;
- dry-run executado;
- adapter iniciado;
- adapter concluído;
- adapter falhado;
- timeout aplicado;
- retry avaliado;
- retry executado;
- fallback avaliado;
- fallback aplicado;
- fallback bloqueado;
- ProviderResult produzido.

Campos mínimos por evento:

- `event_id`;
- `event_type`;
- `mission_id`;
- `workflow_id`;
- `task_id`;
- `attempt_id`;
- `agent_assignment_id`;
- `skill_id`;
- `tool_id`;
- `tool_execution_request_id`;
- `provider_request_id`;
- `provider_result_id` quando aplicável;
- `provider_id` quando aplicável;
- `provider_type`;
- `adapter_ref` quando aplicável;
- `operation`;
- `effects`;
- `guardian_decision_ref` quando aplicável;
- `permission_set_ref`;
- `redactions_applied`;
- `timestamp`;
- `status`;
- `reason`.

Regras:

1. Logs não podem conter segredos.
2. Logs devem preferir IDs, hashes, referências, paths permitidos e metadados.
3. Payload completo só pode ser registrado quando política permitir explicitamente.
4. Falha de log deve bloquear conclusão automática de operação de alto risco.
5. Logs devem distinguir seleção automática de provider de provider explicitamente solicitado.

## Rastreabilidade

Relações mínimas:

- Mission para Workflow;
- Workflow para Task;
- Task para Attempt;
- Attempt para Agent Assignment;
- Agent Assignment para Capability Request;
- Capability Request para Skill;
- Skill para ToolExecutionRequest;
- ToolExecutionRequest para ProviderRequest;
- ProviderRequest para Provider Registry entry;
- ProviderRequest para Guardian Decision;
- ProviderRequest para Provider Adapter;
- Provider Adapter para provider concreto;
- ProviderResult para ToolExecutionResult;
- fallback para provider original, provider substituto, motivo e decisão de Guardian/Policy.

Regras:

1. Rastreabilidade não pode depender da memória do agente, do adapter ou do runtime.
2. Cada chamada deve registrar versões de Tool, Provider e Adapter.
3. Retry deve ser distinguível de nova ProviderRequest.
4. Fallback deve preservar referência da tentativa original.
5. Dry-run deve ser rastreável como simulação, não como execução real.

## Bloqueio de providers perigosos

Provider perigoso é qualquer provider capaz de causar dano relevante, vazamento, custo inesperado, execução privilegiada, alteração global ou impacto fora do escopo.

Exemplos:

- provider de comando shell livre;
- provider com acesso amplo ao filesystem;
- provider com escrita em banco de produção;
- provider que usa rede externa sem allowlist;
- provider que pode publicar, apagar ou transferir dados;
- provider que modifica configuração global;
- provider que exige privilégio elevado;
- provider experimental sem isolamento.

Regras:

1. Provider perigoso deve ser bloqueado por padrão.
2. Uso de provider perigoso deve exigir política explícita, Guardian Engine e aprovação quando aplicável.
3. Provider perigoso não pode ser fallback automático.
4. Provider perigoso deve declarar efeitos, riscos, limites e alternativas seguras.
5. Provider marcado como `blocked` nunca deve executar enquanto permanecer bloqueado.

## Redaction de segredos

Segredos incluem tokens, chaves, senhas, certificados privados, connection strings, cookies, credenciais cloud, headers de autenticação e qualquer valor marcado como sensível por política.

Regras:

1. Segredos devem ser referenciados por `secret_refs`, não incluídos em ProviderRequest.
2. Provider Adapter pode resolver segredo apenas quando autorizado.
3. Segredos devem ser redigidos em logs, warnings, erros, traces, outputs e metadados.
4. Redaction deve acontecer antes de persistência de logs.
5. Resposta de provider deve ser varrida para padrões prováveis de segredo antes de ser retornada.
6. Detecção de segredo não autorizado deve bloquear ou falhar de forma segura.
7. Provider externo não deve receber segredo sem política explícita e escopo mínimo.

## Dry Run

`dry_run` é execução simulada sem efeito externo real.

Regras:

1. ProviderRequest deve declarar `dry_run` explicitamente.
2. Quando `dry_run` for verdadeiro, Provider Adapter não deve executar chamada com efeito externo.
3. Dry-run deve retornar plano, provider selecionado, operação pretendida, efeitos declarados e limites aplicáveis quando possível.
4. Dry-run não deve resolver segredos reais salvo política explícita e necessidade justificada.
5. Operações sensíveis devem suportar dry-run quando tecnicamente possível.
6. Operação sem suporte a dry-run deve declarar essa limitação e exigir avaliação antes de execução real.

## Timeout

Timeout limita duração máxima de uma chamada ao provider.

Regras:

1. Provider deve declarar timeout padrão.
2. ProviderRequest pode declarar timeout menor ou igual ao permitido por política.
3. Provider Gateway deve aplicar timeout antes de acionar adapter.
4. Timeout excedido deve gerar ProviderResult estruturado.
5. Timeout não deve ser ampliado automaticamente por fallback ou retry sem nova avaliação quando houver risco, custo ou rede.
6. Adapter deve cooperar com cancelamento quando tecnicamente possível.

## Retries

Retry é repetição controlada de chamada falha ao mesmo provider.

Regras:

1. Retry deve ser declarado por política de provider, tool ou request.
2. Retry deve distinguir erro transitório de erro permanente quando possível.
3. Retry não deve repetir operação destrutiva ou não idempotente sem política explícita.
4. Retry deve respeitar timeout total, orçamento, rate limit e Guardian Engine.
5. Retry de operação sensível deve registrar cada tentativa.
6. Retry esgotado deve retornar falha estruturada com contagem de tentativas.

## Fallback entre providers

Fallback entre providers é a substituição controlada de um provider por outro capaz de cumprir a mesma operação.

Regras:

1. Fallback deve ser declarado previamente no Provider Registry, Tool Profile ou política aplicável.
2. Fallback deve preservar contrato de entrada e saída esperado pela Tool.
3. Fallback não pode ampliar permissões, efeitos, rede, custo, retenção, região, localidade ou sensibilidade de dados sem nova avaliação.
4. Fallback de provider local para provider externo deve exigir política explícita quando houver dados sensíveis.
5. Fallback para MCP não deve ser preferido apenas por conveniência se API local ou provider local governado cumprir o contrato.
6. Fallback deve registrar provider original, provider substituto, motivo, decisões de Guardian/Policy e diferenças de risco.
7. Ausência de fallback permitido deve retornar falha segura.

## Provider Agnostic

Regras:

1. Capability não deve nomear provider, MCP, API, banco, modelo, filesystem ou runtime concreto.
2. Skill não deve depender de provider concreto quando houver contrato abstrato viável.
3. Tool deve declarar necessidade técnica e contrato, não detalhes internos do provider.
4. Provider Gateway deve permitir múltiplos adapters para a mesma operação.
5. Trocar OpenAI por Ollama, GitHub API por GitHub MCP, PostgreSQL por outro banco, ou OpenCode por outro runtime não deve exigir mudança em Agent quando contratos forem preservados.
6. O framework não deve depender obrigatoriamente de OpenCode, MCP, Ollama, PostgreSQL, pgvector, Docker, GitHub, Linux ou ARM64.
7. Ambiente atual pode fornecer providers iniciais, mas seleção deve considerar detecção de capacidades e política.

## OpenCode como runtime inicial

OpenCode pode ser usado inicialmente para hospedar execução, ferramentas nativas, adapters ou MCPs durante o desenvolvimento do framework.

Regras:

1. OpenCode não é núcleo do Provider Gateway.
2. Tool nativa do OpenCode deve ser tratada como provider de runtime via adapter governado.
3. MCP configurado no OpenCode deve ser tratado como provider MCP, não como dependência direta de Agent.
4. Configurações do OpenCode não devem definir contratos centrais de ProviderRequest, ProviderResult, Provider Registry ou Provider Adapter.
5. Runtime específico não pode ampliar permissões concedidas pela Assignment, Tool ou ProviderRequest.
6. O mesmo modelo deve permitir runtimes futuros como Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI ou API.

## Relação com Guardian Specs

### Security by Design

Provider Gateway deve aplicar mínimo privilégio, bloquear providers perigosos por padrão, impedir `sudo`, proteger segredos, validar paths, controlar rede e exigir Guardian Engine para ações sensíveis.

### Token Efficiency

ProviderResult deve retornar dados normalizados, paginados, resumidos ou referenciados quando apropriado, evitando despejar payloads grandes no agente.

### AI Quality Assurance

Provider Adapter deve produzir erros estruturados, evidências e resultados normalizados. ProviderResult não deve ser ambíguo.

### Cost Optimization

Providers com custo devem declarar custo estimado, orçamento, rate limit, retries e fallback. Fallback não pode aumentar custo sem autorização.

### Architecture Governance

Provider Gateway preserva fronteira entre Tools e infraestrutura, mantendo MCP, API, banco, filesystem e runtimes fora do núcleo de agentes.

### Documentation Governance

Providers, adapters e contratos relevantes devem ser documentados, versionados e rastreáveis.

### Testing Governance

Provider Gateway e Provider Adapters devem ser testáveis por contrato quando implementados, incluindo dry-run, bloqueios, redaction, timeout, retry e fallback.

### Compliance Governance

Envio de dados a providers externos, retenção de logs, segredos, localização, auditoria e transferência de contexto devem seguir políticas aplicáveis.

### Observability Governance

Provider Gateway deve emitir eventos estruturados suficientes para auditoria, diagnóstico, replay e investigação.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Tool acoplar a provider específico | Exigir ProviderRequest normalizada e Provider Gateway como fronteira obrigatória. |
| MCP virar núcleo do framework | Definir MCP como tipo de provider adapter. |
| Provider perigoso executar automaticamente | Bloqueio por padrão, Guardian Engine e aprovação explícita. |
| Segredo vazar em logs ou erros | `secret_refs`, redaction antes de persistência e varredura de outputs. |
| Fallback expor dados a provider externo | Política explícita, Guardian Engine e registro de diferenças de risco. |
| Retry repetir ação destrutiva | Exigir idempotência ou política explícita antes de retry. |
| Adapter executar comando inseguro | Argumentos estruturados, validação e bloqueio de shell livre. |
| Acoplamento ao OpenCode | Tratar OpenCode como runtime provider inicial por adapter. |
| Perda de rastreabilidade | IDs estáveis e logs da cadeia ToolExecutionRequest -> ProviderRequest -> ProviderResult. |
| Provider indisponível causar degradação insegura | Falha segura ou fallback previamente autorizado. |

## Decisões aprovadas por esta Spec

1. Provider Gateway é a camada de isolamento entre Tools e Providers/MCPs/APIs.
2. Tool não deve conhecer detalhes internos de provider.
3. MCP é uma forma de provider, não o núcleo do framework.
4. API HTTP, CLI local, MCP, banco, filesystem, serviço local e runtime devem ser tratados como providers por adapters.
5. Provider Registry é o catálogo governado de providers disponíveis.
6. Provider Adapter encapsula protocolo, autenticação e mecanismo concreto.
7. ProviderRequest é o contrato normalizado de chamada de provider.
8. ProviderResult é o contrato normalizado de resultado de provider.
9. Provider Gateway deve integrar com Guardian Engine para ações sensíveis.
10. Provider Gateway deve integrar com Tool Executor sem substituí-lo.
11. Providers perigosos devem ser bloqueados por padrão.
12. Segredos devem usar referências e redaction obrigatória.
13. `dry_run`, timeout, retries e fallback devem ser governados e rastreáveis.
14. Fallback entre providers não pode ampliar risco sem nova avaliação.
15. O framework deve permanecer provider agnostic e runtime agnostic.
16. OpenCode é runtime inicial, não núcleo.
17. Esta Spec não autoriza implementação de código, alteração de configurações globais ou uso de `sudo`.

## Estado implementado e validado em 0108

O Provider Gateway implementado em `src/vercosa_ai_framework/providers/gateway.py` seleciona e valida `ProviderProfile` a partir de registry injetado. No fluxo validado, o Tool Executor chama um Provider Gateway real com `dry_run=True`; o Gateway produz `ProviderRequest` e `ProviderResult`, mas não chama adapter concreto.

Evidências:

- `tests/test_provider_gateway.py` cobre validação de provider, bloqueios e dry-run.
- `tests/test_tool_executor_provider_gateway.py` cobre a fronteira Tool Executor -> Provider Gateway.
- `tests/test_capability_skill_tool_provider_dry_run.py` valida que `adapter.calls == 0`, preservando IDs e status `dry_run`.
- `tests/test_agent_execution_governance_0107.py` valida o mesmo comportamento no fluxo governado integrado.

O Provider Gateway não é Model Selector. Providers reais, rede, fallback externo real, banco, MCP e API externa continuam fora do fluxo validado atual.

## Critérios de aceite

- Existe uma Spec própria em `specs/framework/0010-provider-gateway.md`.
- A Spec diferencia Tool, Provider, MCP e API.
- A Spec estabelece que Tool não conhece detalhes internos de provider.
- A Spec define Provider Gateway como camada de isolamento.
- A Spec define MCP como uma forma de provider, não como núcleo.
- A Spec cobre suporte futuro a APIs HTTP, CLIs locais, MCPs, bancos, filesystem e serviços locais.
- A Spec define Provider Registry.
- A Spec define Provider Adapter.
- A Spec define ProviderRequest.
- A Spec define ProviderResult.
- A Spec cobre permissões.
- A Spec define integração com Guardian Engine.
- A Spec define integração com Tool Executor.
- A Spec cobre logs e rastreabilidade.
- A Spec cobre bloqueio de providers perigosos.
- A Spec cobre redaction de segredos.
- A Spec cobre `dry_run`.
- A Spec cobre timeout.
- A Spec cobre retries.
- A Spec cobre fallback entre providers.
- A Spec preserva provider agnostic.
- A Spec define OpenCode como runtime inicial, não núcleo.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir schema persistente final de Provider Registry.
- Definir formato final de ProviderRequest e ProviderResult.
- Definir catálogo inicial de provider types e operações suportadas.
- Definir contrato formal de Provider Gateway.
- Definir contrato formal de Provider Adapter.
- Definir estratégia de resolução segura de `secret_refs`.
- Definir política numérica padrão de timeout, retries, rate limit e orçamento.
- Definir integração persistente com logs e audit trail.
- Definir adapters iniciais permitidos para ambiente local.
- Definir ADR se Provider Gateway assumir responsabilidades hoje atribuídas ao ToolAdapter MVP.

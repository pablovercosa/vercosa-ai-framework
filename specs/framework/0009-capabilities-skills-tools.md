# Spec 0009 — Capabilities, Skills e Tools

## Status

Proposta.

## Objetivo

Definir a camada de Capabilities, Skills e Tools do Vercosa AI Framework como a fronteira arquitetural entre Agents/Subagents e a infraestrutura concreta usada para executar ações.

Esta Spec estabelece que agentes expressam intenções funcionais por meio de Capabilities, o framework resolve essas intenções para Skills reutilizáveis e Skills usam Tools concretas para acessar Providers, MCPs, APIs, bancos, filesystem ou runtimes conforme política.

## Contexto

As Specs 0001 e 0008 e a arquitetura central definem que:

- o framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design;
- OpenCode é runtime inicial, não núcleo do framework;
- agentes não devem conhecer MCPs, providers, APIs, bancos, filesystem ou tools concretas diretamente;
- Agents e Subagents solicitam Capabilities;
- Capabilities são resolvidas pelo framework;
- Skills implementam Capabilities de forma reutilizável;
- Tools executam integrações concretas;
- Providers, MCPs e APIs pertencem à camada externa;
- Guardian Engine governa ações sensíveis, permissões, riscos e validações;
- Policy Engine será a camada futura de decisão centralizada entre Capabilities e Skills.

## Escopo

Esta Spec cobre:

- diferença entre Capability, Skill e Tool;
- regra central de que agente não conhece MCP diretamente;
- Capability como intenção funcional;
- Skill como procedimento reutilizável;
- Tool como execução concreta;
- Provider, MCP e API como infraestrutura externa;
- Capability Registry;
- Skill Registry;
- Tool Registry;
- permissões;
- integração com Guardian Engine;
- integração com Agent Orchestrator;
- integração futura com Policy Engine;
- segurança contra tool misuse;
- segurança contra prompt injection;
- rastreabilidade;
- logs;
- fallback de tools;
- provider agnostic;
- OpenCode como runtime inicial, não núcleo;
- riscos, mitigações, decisões e critérios de aceite.

Esta Spec não cobre:

- implementação concreta em código;
- schema persistente final;
- criação de CLI, API, daemon, worker, serviço `systemd` ou scheduler real;
- criação de MCPs concretos;
- criação de adapters específicos de providers;
- alteração de configurações globais;
- uso de `sudo`;
- execução real de comandos, tools, MCPs, providers, bancos ou APIs;
- catálogo final de todas as capabilities, skills e tools do framework.

## Princípios

1. Agente declara intenção; framework resolve execução.
2. Capability é contrato funcional, não implementação.
3. Skill é procedimento reutilizável, governado e testável.
4. Tool é integração concreta e restrita por política.
5. Provider, MCP, API, banco, filesystem e runtime são infraestrutura externa.
6. Agentes e Subagents nunca acessam MCPs diretamente.
7. A cadeia obrigatória é `Agent -> Capability -> Policy/Guardian -> Skill -> Tool -> Provider/MCP/API`.
8. Toda resolução sensível deve aplicar mínimo privilégio.
9. Toda chamada de Tool deve ser rastreável quando produzir efeito, custo, rede, leitura sensível ou escrita.
10. Prompt injection em contexto não confiável não pode alterar políticas, permissões ou cadeia de execução.
11. OpenCode pode hospedar ou acionar execução inicial via adapter, mas não define o modelo arquitetural.

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
Capability Request
↓
Capability Registry / Resolver
↓
Guardian Engine / Policy Engine futuro
↓
Skill Registry / Skill Execution
↓
Tool Registry / Tool Execution
↓
Providers / MCPs / APIs / bancos / filesystem / runtimes
```

Regras:

1. Agent Orchestrator entrega ao runtime uma execução com `required_capabilities`, limites, contexto e políticas.
2. Agent ou Subagent só pode solicitar Capability declarada e autorizada para a Assignment.
3. O framework resolve a Capability para Skill compatível.
4. Skill solicita Tools necessárias conforme seu contrato e permissões.
5. Tool acessa infraestrutura externa apenas dentro dos limites autorizados.
6. Provider, MCP ou API não deve aparecer como dependência direta de Agent Profile.

## Definições

### Capability

Capability é uma intenção funcional abstrata solicitada por um Agent ou Subagent.

Exemplos:

- `SearchSpecification`;
- `SearchCode`;
- `ReadContext`;
- `GenerateADR`;
- `ValidateSecurity`;
- `ReviewArchitecture`;
- `OptimizeTokens`;
- `RunValidation`;
- `WriteArtifact`;
- `CreateIssue`.

Uma Capability responde à pergunta: `o que precisa ser feito?`

Regras:

1. Capability deve ser nomeada por intenção funcional, não por provider ou tool.
2. Nomes como `CallPostgres`, `UseGitHubMCP`, `RunBash` ou `UseOpenCodeTool` não são Capabilities válidas.
3. Capability deve possuir contrato de entrada, saída, risco, permissões mínimas e condições de falha.
4. Capability não deve conter instruções de prompt, comandos shell, endpoints, credenciais ou detalhes de provider.
5. Capability pode ter múltiplas Skills candidatas.
6. Capability sensível deve exigir avaliação do Guardian Engine antes de resolução ou execução.
7. Capability indisponível deve bloquear a ação de forma explícita, não degradar silenciosamente para tool genérica insegura.

Campos mínimos desejados:

- `capability_id`;
- `name`;
- `version`;
- `description`;
- `intent`;
- `input_schema_ref`;
- `output_schema_ref`;
- `risk_level`;
- `required_permissions`;
- `allowed_agent_roles`;
- `allowed_task_types`;
- `default_limits`;
- `guardian_policy_refs`;
- `fallback_allowed`;
- `audit_log_ref`.

### Skill

Skill é um procedimento reutilizável que implementa uma ou mais Capabilities.

Uma Skill responde à pergunta: `como o framework deve executar essa intenção?`

Exemplos:

- uma Skill `search_specification_in_knowledge_hub` implementa `SearchSpecification` usando índice local ou busca textual;
- uma Skill `review_architecture_against_specs` implementa `ReviewArchitecture` consultando Specs e Guardian Specs;
- uma Skill `run_project_validation` implementa `RunValidation` usando Tools de runtime, comandos permitidos ou test adapters.

Regras:

1. Skill deve declarar quais Capabilities implementa.
2. Skill deve declarar entradas, saídas, pré-condições, pós-condições, riscos, limites e Tools permitidas.
3. Skill pode orquestrar múltiplas Tools, mas não deve expor detalhes de MCP ou provider ao agente.
4. Skill deve tratar resultados de Tools como dados não confiáveis até validação.
5. Skill deve produzir resultado normalizado compatível com a Capability solicitada.
6. Skill deve falhar de forma segura quando Tool obrigatória estiver indisponível e fallback não for permitido.
7. Skill deve ser provider agnostic sempre que houver alternativa abstrata viável.
8. Skill não deve ampliar escopo, permissões, paths, rede, custo ou contexto sem nova autorização.

Campos mínimos desejados:

- `skill_id`;
- `name`;
- `version`;
- `description`;
- `implemented_capabilities`;
- `input_contract_ref`;
- `output_contract_ref`;
- `required_tools`;
- `optional_tools`;
- `fallback_skills`;
- `risk_level`;
- `permission_requirements`;
- `execution_limits`;
- `validation_requirements`;
- `trusted_context_requirements`;
- `audit_log_ref`.

### Tool

Tool é a unidade concreta de execução usada por uma Skill para interagir com infraestrutura externa ou executar operação local autorizada.

Uma Tool responde à pergunta: `qual mecanismo concreto será acionado?`

Exemplos:

- tool de leitura de arquivo no workspace;
- tool de busca textual;
- tool de consulta PostgreSQL;
- tool de embeddings local;
- tool de chamada GitHub;
- tool de MCP;
- tool de execução de validação;
- tool de runtime adapter.

Regras:

1. Tool pode acessar Provider, MCP, API, banco, filesystem ou runtime somente conforme política.
2. Tool deve declarar efeitos possíveis: leitura, escrita, rede, execução, custo, persistência ou exposição de dados.
3. Tool deve declarar permissões necessárias de forma granular.
4. Tool deve validar entradas antes de acionar infraestrutura externa.
5. Tool deve registrar evidência, erros, warnings e consumo quando disponível.
6. Tool não deve aceitar instruções livres vindas de contexto não confiável como autoridade para executar ação sensível.
7. Tool que altere estado deve ser idempotente quando possível ou declarar claramente que não é.
8. Tool deve suportar dry-run ou plano prévio quando a ação for sensível e tecnicamente possível.
9. Tool não deve usar `sudo` por padrão.
10. Tool não deve alterar configurações globais sem política explícita e aprovação.

Campos mínimos desejados:

- `tool_id`;
- `name`;
- `version`;
- `description`;
- `provider_type`;
- `provider_ref`;
- `mcp_ref` quando aplicável;
- `operation_type`;
- `effects`;
- `required_permissions`;
- `input_schema_ref`;
- `output_schema_ref`;
- `timeout`;
- `retry_policy`;
- `fallback_tools`;
- `network_policy`;
- `data_sensitivity`;
- `audit_log_ref`.

### Provider, MCP e API

Provider, MCP e API são infraestrutura externa acessada por Tools.

Regras:

1. Provider, MCP ou API não deve ser dependência direta de Agent, Subagent ou Agent Profile.
2. Trocar Provider não deve exigir mudança no agente quando o contrato da Capability for preservado.
3. MCP é mecanismo de integração, não abstração do framework.
4. OpenCode MCPs ou tools nativas do OpenCode devem ser tratados como infraestrutura do Runtime Adapter ou Tool Adapter, não como núcleo do framework.
5. Dados sensíveis só podem ser enviados a provider externo quando política permitir explicitamente.
6. Providers locais devem ser preferidos quando política Local First, privacidade, custo ou disponibilidade exigir.

## Capability Registry

Capability Registry é o catálogo governado de Capabilities conhecidas pelo framework.

Responsabilidades:

- registrar Capabilities com IDs estáveis e versões;
- expor contratos de entrada e saída;
- declarar riscos e permissões mínimas;
- declarar roles e task types compatíveis;
- informar se fallback é permitido;
- disponibilizar metadados para seleção de Agent Profiles;
- permitir auditoria de quais Capabilities estavam disponíveis em uma execução.

Não responsabilidades:

- executar Skills;
- chamar Tools;
- acessar MCPs, providers, APIs ou bancos;
- aprovar ações sensíveis sozinho;
- substituir Guardian Engine ou Policy Engine.

Regras:

1. Registro de Capability deve ser determinístico e versionado.
2. Remoção ou alteração incompatível de contrato deve exigir Spec, decisão ou migração conforme impacto.
3. Capability experimental deve ser marcada explicitamente.
4. Capability depreciada não deve ser escolhida automaticamente quando houver alternativa estável.
5. Capability Registry deve permitir consulta por `capability_id`, nome, versão, risco, permissões e roles compatíveis.

## Skill Registry

Skill Registry é o catálogo de Skills capazes de implementar Capabilities.

Responsabilidades:

- registrar Skills com IDs estáveis e versões;
- mapear Capabilities para Skills candidatas;
- declarar Tools necessárias e opcionais;
- declarar limites, riscos, validações e fallback;
- permitir seleção determinística quando múltiplas Skills forem compatíveis;
- preservar auditabilidade da resolução Capability -> Skill.

Não responsabilidades:

- executar Tools diretamente fora de uma Skill Execution;
- contornar permissões;
- escolher provider por preferência hardcoded sem política;
- substituir Guardian Engine.

Ordem conceitual de seleção de Skill:

1. Filtrar Skills que implementam a Capability solicitada.
2. Filtrar por versão compatível do contrato.
3. Filtrar por permissões concedidas à Assignment.
4. Filtrar por risco permitido.
5. Filtrar por contexto, dados sensíveis, rede, custo e ambiente disponível.
6. Filtrar por Tools disponíveis.
7. Aplicar Guardian Engine e, futuramente, Policy Engine.
8. Escolher de forma determinística e registrar motivo.

Regras:

1. Falta de Skill compatível deve bloquear a Capability.
2. Skill de menor privilégio deve ser preferida quando cumprir o contrato.
3. Skill local deve ser preferida quando preservar qualidade e reduzir exposição externa conforme política.
4. Skill com provider externo deve justificar envio de dados e registrar escopo.
5. Empates devem ser resolvidos por prioridade declarada e registrados.

## Tool Registry

Tool Registry é o catálogo de Tools concretas disponíveis para Skills.

Responsabilidades:

- registrar Tools com IDs estáveis e versões;
- declarar provider, MCP, API ou mecanismo externo usado;
- declarar efeitos, permissões, limites, timeouts e retries;
- declarar fallback tools compatíveis;
- informar disponibilidade por ambiente;
- preservar auditabilidade da resolução Skill -> Tool.

Não responsabilidades:

- permitir acesso direto por agentes;
- executar Tools sem Skill e autorização;
- guardar segredos em claro;
- decidir política de alto nível sem Guardian Engine ou Policy Engine.

Regras:

1. Tool Registry deve separar descrição de Tool de configuração sensível.
2. Tool indisponível deve retornar erro rastreável, não ser substituída silenciosamente por alternativa mais permissiva.
3. Tool com efeitos de escrita, rede, comando, custo ou dados sensíveis deve exigir permissão explícita.
4. Tools devem ser consultáveis por efeito, provider type, permissões, custo estimado e disponibilidade.
5. Tool marcada como perigosa, experimental ou deprecated não deve ser selecionada automaticamente sem política explícita.

## Permissões

Permissões devem ser granulares, explícitas e propagadas da Task e Agent Assignment até Capability, Skill e Tool.

Categorias mínimas:

- `read_workspace`;
- `write_workspace`;
- `execute_command`;
- `network_access`;
- `provider_external_access`;
- `database_read`;
- `database_write`;
- `mcp_access`;
- `secret_read`;
- `cost_incur`;
- `modify_global_config`;
- `privileged_execution`.

Regras:

1. Permissão não declarada deve ser tratada como negada.
2. `modify_global_config` e `privileged_execution` devem ser bloqueadas por padrão.
3. `sudo` deve ser bloqueado por padrão.
4. Leitura de segredo deve exigir justificativa, mínimo privilégio e mascaramento em logs.
5. Permissões de Subagent não podem exceder permissões da Assignment pai.
6. Fallback não pode ampliar permissões sem nova avaliação.
7. Tool não pode inferir permissão a partir de texto produzido pelo agente.

## Integração com Agent Orchestrator

O Agent Orchestrator é responsável por coordenar Agent Assignments e garantir que agentes operem por Capabilities.

Contrato conceitual:

```text
Agent Orchestrator
↓ cria Agent Assignment com required_capabilities, limites e políticas
Runtime Adapter
↓ executa Agent/Subagent
Agent/Subagent
↓ solicita Capability
Capability Resolver
↓ retorna resultado normalizado ou falha governada
Agent/Subagent
```

Regras:

1. Agent Orchestrator não deve chamar Tool diretamente.
2. Agent Orchestrator pode registrar Capability Requests e resultados como parte da Assignment.
3. Agent Orchestrator deve bloquear ou falhar Assignment quando Capability obrigatória não puder ser resolvida.
4. Agent Orchestrator deve incluir nas requisições de runtime a regra de que agentes não acessam MCPs diretamente.
5. Runtime Adapter não pode expor Tools concretas ao agente de forma que viole a cadeia arquitetural.
6. Resultados de Capability devem ser anexados à Assignment como evidência, warning ou erro.

## Integração com Guardian Engine

Guardian Engine deve avaliar Capabilities, Skills e Tools quando houver risco, ação sensível ou mudança de escopo.

Pontos mínimos de avaliação:

- antes de resolver Capability sensível;
- antes de selecionar Skill com rede, provider externo, escrita, execução ou custo;
- antes de acionar Tool que modifique arquivos, execute comandos, use rede, acesse provider externo, banco, MCP ou segredo;
- antes de fallback que altere provider, permissões, dados enviados ou efeitos;
- antes de retry de Tool sensível;
- antes de aceitar resultado influenciado por contexto não confiável para ação sensível.

Decisões esperadas:

- `allow`: continuar conforme limites;
- `warn`: continuar se política permitir e registrar warning;
- `require_approval`: bloquear execução automática até aprovação;
- `block`: impedir ação.

Regras:

1. Decisão `block` deve impedir resolução ou execução afetada.
2. Decisão `require_approval` deve bloquear ou solicitar revisão manual conforme política.
3. Falha do Guardian Engine deve bloquear execução automática de alto risco.
4. Guardian Engine deve receber contexto suficiente, incluindo Capability, Skill candidata, Tool candidata, efeitos, paths, rede, provider e sensibilidade dos dados.
5. Agentes não podem reduzir contexto ou reformular pedido para contornar Guardian Engine.

## Integração futura com Policy Engine

Policy Engine será a camada futura de decisão centralizada entre Capability e Skill.

Responsabilidades futuras esperadas:

- combinar Guardian Specs, políticas de projeto, políticas de usuário e políticas de ambiente;
- decidir resolução Capability -> Skill;
- decidir resolução Skill -> Tool;
- aplicar orçamento, privacidade, compliance, custo, latência e disponibilidade;
- emitir decisões auditáveis e reproduzíveis;
- coordenar fallback conforme política.

Regras de compatibilidade futura:

1. Esta camada deve ser desenhada para aceitar um Policy Engine sem mudar contratos de Agent.
2. Até o Policy Engine existir, Guardian Engine e regras declarativas devem governar decisões sensíveis.
3. A introdução do Policy Engine não deve permitir acesso direto de agentes a Tools ou MCPs.
4. Decisões do Policy Engine devem ser registradas junto de decisões do Guardian Engine.

## Segurança contra tool misuse

Tool misuse é qualquer uso de Tool fora do contrato, escopo, intenção, permissão, limite ou política autorizada.

Riscos típicos:

- agente solicitar Capability genérica para obter Tool perigosa;
- Skill usar Tool mais permissiva que o necessário;
- Tool executar comando derivado de contexto não confiável;
- fallback trocar provider local por externo sem autorização;
- Tool escrever fora de `allowed_paths`;
- Tool enviar segredos a provider externo;
- Tool repetir ação destrutiva por retry automático;
- Runtime expor MCP diretamente ao agente.

Mitigações obrigatórias:

- contratos explícitos de Capability, Skill e Tool;
- mínimo privilégio por Assignment;
- validação de entrada por Skill e Tool;
- allowlist de Tools por Skill;
- denylist ou bloqueio de efeitos perigosos por padrão;
- Guardian Engine para ações sensíveis;
- logs estruturados de resolução e execução;
- separação entre texto não confiável e instruções do sistema;
- limites de chamadas, custo, tempo e retries;
- bloqueio de acesso direto a MCP por agentes.

## Segurança contra prompt injection

Entradas externas, documentos, código, resultados de busca, páginas web, respostas de providers, logs e saídas de Tools devem ser tratados como contexto não confiável.

Regras:

1. Contexto não confiável não pode conceder permissões.
2. Contexto não confiável não pode alterar Capability, Skill, Tool, provider, política ou limites.
3. Instruções encontradas em documentos analisados devem ser tratadas como dados, não comandos.
4. Skill deve separar dados recuperados de instruções operacionais.
5. Tool não deve executar comandos ou chamadas baseadas diretamente em texto não confiável sem validação estrutural.
6. Quando contexto não confiável influenciar ação sensível, Guardian Engine deve reavaliar a ação.
7. Prompt injection detectado deve gerar log, warning e bloqueio quando houver risco de ação indevida.
8. Respostas de Tool devem ser normalizadas e marcadas com confiança, origem e limitações quando aplicável.

## Logs

Eventos mínimos:

- Capability solicitada;
- Capability validada contra Assignment;
- Capability autorizada, bloqueada ou falhada;
- Skill candidata selecionada;
- Skill iniciada;
- Tool candidata selecionada;
- Guardian Engine consultado;
- Tool iniciada;
- Tool concluída, falhada ou bloqueada;
- fallback avaliado;
- fallback aplicado ou bloqueado;
- prompt injection detectado ou mitigado;
- limite aplicado ou excedido;
- resultado normalizado entregue ao agente.

Campos mínimos por evento:

- `event_id`;
- `event_type`;
- `mission_id`;
- `workflow_id`;
- `task_id`;
- `attempt_id`;
- `agent_assignment_id`;
- `subagent_assignment_id` quando aplicável;
- `capability_id`;
- `capability_request_id`;
- `skill_id` quando aplicável;
- `tool_id` quando aplicável;
- `provider_ref` quando aplicável;
- `guardian_decision_ref` quando aplicável;
- `policy_decision_ref` futuro quando aplicável;
- `permission_set_ref`;
- `artifact_refs`;
- `timestamp`;
- `status`;
- `reason`.

Regras:

1. Logs não podem conter segredos.
2. Logs devem preferir referências, hashes, IDs, paths e metadados.
3. Entradas e saídas completas só devem ser registradas quando política permitir.
4. Falha de log deve bloquear conclusão automática de ação de alto risco.
5. Logs devem permitir reconstruir a cadeia Capability -> Skill -> Tool -> Provider.

## Rastreabilidade

Relações mínimas:

- Mission para Workflow;
- Workflow para Task;
- Task para Attempt;
- Attempt para Agent Assignment;
- Agent Assignment para Capability Request;
- Capability Request para Capability Registry entry;
- Capability Request para Guardian Decision;
- Capability para Skill selecionada;
- Skill para Tools selecionadas;
- Tool para Provider, MCP, API, banco, filesystem ou runtime;
- Tool Execution para artefatos, erros, warnings, custo, tokens e logs;
- fallback para motivo, alternativa escolhida e decisão de política.

Regras:

1. Rastreabilidade não pode depender da memória interna do agente ou do runtime.
2. Cada resolução deve registrar versões de Capability, Skill e Tool.
3. Retry deve ser distinguível de nova solicitação.
4. Fallback deve preservar referência da tentativa original.
5. Resultado retornado ao agente deve possuir referência auditável quando houver ação sensível.

## Fallback de Tools

Fallback é a substituição controlada de uma Tool indisponível, falha ou inadequada por outra Tool compatível com o mesmo contrato de Skill.

Regras:

1. Fallback deve ser declarado previamente em Tool ou Skill Registry.
2. Fallback não pode ampliar permissões, efeitos, escopo, rede, custo ou exposição de dados sem nova avaliação.
3. Fallback para provider externo a partir de provider local deve exigir política explícita quando houver dados sensíveis.
4. Fallback deve preservar contrato de saída esperado pela Skill.
5. Fallback deve registrar motivo, Tool original, Tool substituta e decisões de Guardian/Policy.
6. Fallback não deve ocultar falha relevante do agente, Task Queue ou auditoria.
7. Ausência de fallback permitido deve retornar falha segura.

## Provider Agnostic

Regras:

1. Capability não deve nomear provider, MCP, API, banco, modelo ou runtime concreto.
2. Skill deve preferir contratos abstratos e permitir múltiplas Tools quando viável.
3. Tool encapsula o detalhe do provider concreto.
4. Agent Profile deve declarar Capabilities suportadas, não Tools concretas.
5. O framework não deve depender obrigatoriamente de OpenAI, Anthropic, Ollama, PostgreSQL, pgvector, Docker, GitHub, Linux, ARM64, OpenCode ou MCP específico.
6. Ambiente atual pode fornecer Tools iniciais, mas a arquitetura deve detectar capacidades disponíveis e escolher conforme política.

## OpenCode como runtime inicial

OpenCode pode ser usado inicialmente para executar agentes, acionar adapters e servir como laboratório do framework.

Regras:

1. OpenCode não é núcleo da camada de Capabilities, Skills e Tools.
2. Tools nativas do OpenCode devem ser acessadas por adapters governados, não diretamente por agentes.
3. Configurações do OpenCode não devem definir contratos centrais do framework.
4. O mesmo contrato deve permitir runtimes futuros como Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI ou API.
5. Runtime específico não pode ampliar permissões concedidas pela Capability, Skill ou Tool.

## Relação com Guardian Specs

### Security by Design

A camada deve aplicar mínimo privilégio, impedir acesso direto a MCPs, validar entradas, bloquear `sudo` por padrão, proteger segredos, restringir paths e exigir Guardian Engine para ações sensíveis.

### Token Efficiency

Capabilities devem trabalhar por contratos e referências. Skills devem recuperar apenas contexto necessário e Tools devem retornar resultados normalizados, resumidos ou paginados quando apropriado.

### AI Quality Assurance

Skills devem ser testáveis, produzir evidências e validar saídas. Tools devem retornar erros estruturados e não resultados ambíguos.

### Cost Optimization

Tools com custo devem declarar custo estimado quando possível, limites e política de retry. Fallback não pode aumentar custo sem autorização.

### Architecture Governance

A camada deve preservar fronteiras entre Agents, Capabilities, Skills, Tools, Guardian Engine, Policy Engine futuro, Runtime Adapter e Providers.

### Documentation Governance

Capabilities, Skills e Tools relevantes devem possuir contratos documentados, versionados e rastreáveis.

### Testing Governance

Skills e Tools devem ser validáveis por contrato. Mudanças que alterem comportamento devem exigir testes ou justificativa quando houver implementação futura.

### Compliance Governance

Uso de providers externos, dados sensíveis, retenção de logs, transferência de contexto e auditoria devem seguir políticas aplicáveis.

### Observability Governance

Resolução e execução devem emitir eventos estruturados suficientes para auditoria, diagnóstico, replay e investigação.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Agente acessar MCP diretamente | Exigir cadeia Agent -> Capability -> Skill -> Tool -> MCP e bloquear exposição direta no runtime. |
| Capability virar nome de tool | Exigir nomeação por intenção funcional e revisão de registry. |
| Skill usar Tool excessivamente permissiva | Allowlist de Tools, mínimo privilégio e Guardian Engine. |
| Prompt injection alterar permissões | Separar contexto não confiável de política e bloquear autoridade de dados externos. |
| Fallback expor dados a provider externo | Exigir política explícita, Guardian Engine e logs. |
| Tool executar comando perigoso | Validação estrutural, denylist, dry-run quando possível e bloqueio por padrão. |
| Vazamento de segredos em logs | Mascaramento, referências e proibição de registrar payload sensível. |
| Acoplamento ao OpenCode | Tratar OpenCode como runtime adapter inicial. |
| Perda de rastreabilidade | Eventos estruturados e IDs estáveis por Capability, Skill, Tool e Provider. |
| Provider indisponível causar ação insegura | Falha segura ou fallback previamente autorizado. |

## Decisões aprovadas por esta Spec

1. Capability é intenção funcional abstrata solicitada por Agents e Subagents.
2. Skill é procedimento reutilizável que implementa Capabilities.
3. Tool é execução concreta que acessa infraestrutura externa ou operação local autorizada.
4. Provider, MCP e API são infraestrutura externa, nunca dependência direta de agente.
5. Agentes não conhecem MCPs diretamente.
6. A cadeia obrigatória é `Agent -> Capability -> Guardian/Policy -> Skill -> Tool -> Provider/MCP/API`.
7. Capability Registry, Skill Registry e Tool Registry são componentes conceituais distintos.
8. Permissões devem ser granulares e negadas por padrão.
9. Guardian Engine deve avaliar Capabilities, Skills e Tools sensíveis.
10. Policy Engine futuro deve poder assumir decisões de resolução sem alterar contratos de Agent.
11. Segurança contra tool misuse e prompt injection é requisito central desta camada.
12. Logs e rastreabilidade devem cobrir Capability -> Skill -> Tool -> Provider.
13. Fallback de Tools deve ser declarado, governado e auditável.
14. A camada deve ser provider agnostic e runtime agnostic.
15. OpenCode é runtime inicial, não núcleo.
16. Esta Spec não autoriza implementação de código, alteração de configurações globais ou uso de `sudo`.

## Estado implementado e validado em 0108

O fluxo atual separa resolução e execução de Capability. `CapabilityResolver` produz `CapabilityResolutionResult` e não executa Skill. `ResolvedCapabilityExecutor`, em `src/vercosa_ai_framework/capabilities/executor.py`, faz a ponte para `SkillExecutor`. `SkillExecutor` seleciona e chama `ToolExecutor`. `ToolExecutor` é a fronteira da cadeia que chama `ProviderGateway`.

Evidências:

- `tests/test_capability_resolution.py` cobre resolução declarativa.
- `tests/test_skill_executor.py`, `tests/test_tool_executor.py` e `tests/test_tool_executor_provider_gateway.py` cobrem execução por fronteiras separadas.
- `tests/test_capability_skill_tool_provider_dry_run.py` valida a cadeia Capability -> Skill -> Tool -> Provider Gateway em dry-run preservando IDs de mission, workflow, task, agent assignment, request e result.

Cada camada preserva IDs e referências. O fluxo validado é local, injetável e sem provider real, rede, banco, MCP ou API externa.

## Critérios de aceite

- Existe uma Spec própria em `specs/framework/0009-capabilities-skills-tools.md`.
- A Spec diferencia Capability, Skill e Tool.
- A Spec estabelece que agente não conhece MCP diretamente.
- A Spec define Capability como intenção funcional.
- A Spec define Skill como procedimento reutilizável.
- A Spec define Tool como execução concreta.
- A Spec define Provider, MCP e API como infraestrutura externa.
- A Spec define Capability Registry.
- A Spec define Skill Registry.
- A Spec define Tool Registry.
- A Spec cobre permissões.
- A Spec define integração com Guardian Engine.
- A Spec define integração com Agent Orchestrator.
- A Spec prepara integração futura com Policy Engine.
- A Spec cobre segurança contra tool misuse.
- A Spec cobre segurança contra prompt injection.
- A Spec cobre rastreabilidade.
- A Spec cobre logs.
- A Spec cobre fallback de tools.
- A Spec preserva provider agnostic.
- A Spec define OpenCode como runtime inicial, não núcleo.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir schema persistente final de Capability Registry, Skill Registry e Tool Registry.
- Definir formato final dos contratos de entrada e saída.
- Definir catálogo inicial de Capabilities do framework.
- Definir catálogo inicial de Skills essenciais.
- Definir catálogo inicial de Tools locais e adapters permitidos.
- Definir contrato formal do Capability Resolver.
- Definir contrato formal de Skill Execution.
- Definir contrato formal de Tool Execution.
- Definir política numérica padrão de limites, timeouts, retries e custo por Tool.
- Definir integração persistente com logs e audit trail.
- Definir ADR se Policy Engine assumir responsabilidades hoje atribuídas ao Guardian Engine durante resolução.

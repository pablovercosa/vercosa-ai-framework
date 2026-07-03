# Spec 0013 — Persistence Layer

## Status

Proposta.

## Objetivo

Definir a Persistence Layer do Vercosa AI Framework como a camada de portas e adaptadores responsável por persistir, recuperar, versionar, auditar e rastrear estado e conhecimento do framework sem acoplar o núcleo a filesystem, banco relacional, banco vetorial, runtime, provider, sistema operacional ou infraestrutura específica.

A Persistence Layer deve começar com armazenamento em memória e filesystem local, por Local First e simplicidade operacional, e preparar a arquitetura para adapters futuros de SQLite, PostgreSQL e PostgreSQL com pgvector, preservando contratos, segurança, rastreabilidade, determinismo e governança.

## Contexto

As Specs 0001, 0004, 0006, 0011 e 0012 definem que:

- o framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design;
- Mission Runner controla missões, fila, estados, ciclos, limites, validação, logs e auditoria;
- Workflow Engine transforma missões em workflows e tasks rastreáveis;
- Knowledge Hub organiza Canonical Documents e Semantic Indexes;
- Canonicalizer produz Markdown canônico antes de indexação ou uso por agentes;
- Guardian Engine governa segurança, privacidade, segredos, custo, tokens e ações sensíveis;
- Model Selection Engine produz decisões auditáveis de modelo e provider;
- Provider Gateway isola acesso a providers concretos;
- agentes não devem conhecer bancos, filesystem, MCPs, APIs ou providers diretamente.

O código inicial já possui contratos e implementações simples para fila local de missões e Knowledge Store em memória. Esta Spec formaliza a Persistence Layer para evitar que esses mecanismos iniciais virem acoplamentos arquiteturais.

## Escopo

Esta Spec cobre:

- persistência como porta/adaptador;
- storage agnostic;
- armazenamento inicial em memória;
- armazenamento inicial em filesystem;
- suporte futuro a SQLite;
- suporte futuro a PostgreSQL;
- suporte futuro a PostgreSQL com pgvector;
- persistência de Missions;
- persistência de Workflows;
- persistência de Tasks;
- persistência de Knowledge Documents;
- persistência de Canonical Documents;
- persistência de Guardian Decisions;
- persistência de Model Decisions;
- logs e audit trail;
- serialização determinística;
- versionamento de schema;
- migrations futuras;
- segurança de segredos;
- redaction;
- backup;
- rastreabilidade;
- limites de dados;
- integração com Provider Gateway;
- integração com Guardian Engine;
- provider agnostic.

Esta Spec não cobre:

- implementação concreta em código;
- criação de tabelas, migrações, índices, arquivos ou diretórios reais;
- escolha definitiva de banco de dados;
- criação de adapter SQLite, PostgreSQL, pgvector ou filesystem final;
- criação de MCPs;
- alteração de configurações globais;
- uso de `sudo`;
- instalação ou configuração de serviços locais;
- schema físico final de produção;
- estratégia final de replicação, alta disponibilidade ou disaster recovery.

## Princípios

1. Persistência é uma capacidade do framework, não detalhe embutido nos componentes de domínio.
2. Componentes centrais dependem de portas abstratas, não de storage concreto.
3. Adapters de storage podem variar sem alterar contratos de Mission, Workflow, Task, Knowledge Hub, Guardian Engine ou Model Selection Engine.
4. Memória e filesystem são adapters iniciais, não arquitetura final obrigatória.
5. SQLite, PostgreSQL e PostgreSQL com pgvector são opções futuras, não dependências universais.
6. Dados persistidos devem ser determinísticos, versionados, rastreáveis e auditáveis.
7. Logs e audit trail devem explicar decisões e transições sem vazar segredos.
8. Segredos não devem ser persistidos em claro.
9. Redaction deve ocorrer antes de logs, índices, backups, caches ou entrega a providers externos quando política exigir.
10. Schema deve evoluir por versões e migrations governadas.
11. Dados derivados, como índices semânticos e caches, devem ser reconstruíveis quando possível.
12. Falha de persistência deve causar degradação segura, não execução silenciosa sem auditoria.

## Posição arquitetural

Fluxo conceitual:

```text
Mission Runner / Workflow Engine / Task Queue / Knowledge Hub / Guardian Engine / Model Selection Engine
↓
Persistence Ports
↓
Persistence Service
↓
Persistence Adapters
↓
In-Memory / Filesystem / SQLite / PostgreSQL / PostgreSQL + pgvector / Future Stores
```

Quando uma operação de persistência depender de infraestrutura concreta, acesso externo, banco, filesystem governado, segredo, rede ou provider selecionável, ela deve passar pelo Provider Gateway ou por adapter registrado compatível com as políticas do framework.

Regras:

1. Mission Runner não deve escrever diretamente em banco ou filesystem sem porta de persistência.
2. Workflow Engine não deve embutir schema de storage.
3. Task Queue não deve assumir que fila é arquivo, tabela ou memória.
4. Knowledge Hub não deve hardcodar PostgreSQL, pgvector, filesystem ou embeddings.
5. Guardian Engine e Model Selection Engine devem produzir decisões persistíveis sem conhecer storage concreto.
6. Provider Gateway deve isolar adapters concretos quando houver provider técnico ou infraestrutura substituível.

## Definições

### Persistence Layer

Persistence Layer é a camada lógica responsável por oferecer contratos de leitura, escrita, listagem, busca, transação lógica, audit trail, versionamento, backup e recuperação para dados do framework.

Responsabilidades:

- definir portas de persistência por domínio;
- normalizar registros antes de persistir;
- aplicar serialização determinística;
- associar registros a versões de schema;
- preservar rastreabilidade entre entidades;
- registrar eventos e audit trail;
- aplicar redaction e políticas de retenção antes de persistência sensível;
- suportar adapters substituíveis;
- declarar capacidades, limites e garantias de cada adapter;
- permitir backup e restore conforme política;
- preparar migrations futuras.

Não responsabilidades:

- decidir política de segurança sozinha;
- executar providers ignorando Provider Gateway;
- escolher modelos de IA;
- canonicalizar documentos;
- indexar semanticamente por conta própria;
- substituir Knowledge Hub;
- substituir Guardian Engine;
- esconder falhas de persistência;
- armazenar segredos em claro;
- exigir banco específico.

### Persistence Port

Persistence Port é uma interface conceitual exposta ao núcleo para persistir e recuperar entidades de domínio.

Portas previstas:

- `MissionStore`;
- `WorkflowStore`;
- `TaskStore`;
- `KnowledgeDocumentStore`;
- `CanonicalDocumentStore`;
- `GuardianDecisionStore`;
- `ModelDecisionStore`;
- `AuditLogStore`;
- `SchemaMetadataStore`;
- `BackupStore`.

Regras:

1. Porta deve declarar operações funcionais, não tecnologia de storage.
2. Porta deve retornar erros normalizados e auditáveis.
3. Porta deve aceitar metadados de política, schema e rastreabilidade quando aplicável.
4. Porta não deve expor detalhes como SQL, path local, extensão de arquivo ou driver ao domínio.

### Persistence Adapter

Persistence Adapter é uma implementação concreta de uma ou mais portas usando um storage específico.

Adapters previstos:

- `in_memory` inicial;
- `filesystem` inicial;
- `sqlite` futuro;
- `postgresql` futuro;
- `postgresql_pgvector` futuro;
- adapters futuros para object storage, KV store, search engine ou banco vetorial alternativo.

Regras:

1. Adapter deve declarar capacidades suportadas.
2. Adapter deve declarar limites conhecidos.
3. Adapter deve declarar se suporta transações, locks, consultas, busca textual, busca vetorial, migrations e backup.
4. Adapter deve ser substituível sem alterar entidades de domínio.
5. Adapter deve passar por Guardian Engine quando operação, conteúdo ou destino forem sensíveis.

### Persistence Record

Persistence Record é a forma serializada e versionada de uma entidade persistida.

Campos mínimos desejados:

- `record_id`;
- `record_type`;
- `schema_version`;
- `entity_id`;
- `parent_refs`;
- `content_hash`;
- `created_at`;
- `updated_at`;
- `created_by`;
- `updated_by`;
- `sensitivity`;
- `redactions_applied`;
- `guardian_decision_refs`;
- `audit_log_refs`;
- `payload`.

Regras:

1. `payload` deve seguir schema versionado do tipo de registro.
2. `content_hash` deve ser calculado sobre representação canônica determinística.
3. Metadados sensíveis devem ser redigidos ou omitidos conforme política.
4. Registro persistido deve permitir reconstrução suficiente do estado auditável.

## Dados Persistidos

### Missions

Missions devem ser persistidas como unidades rastreáveis de intenção, estado, execução e encerramento.

Dados mínimos:

- `mission_id`;
- `title`;
- `goal`;
- `requested_by`;
- `workspace`;
- `status`;
- `priority`;
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
- `attempt_count`;
- `cycle_count`;
- `timestamps`;
- `last_error`;
- `audit_log_ref`.

Regras:

1. Transições de estado devem gerar audit events.
2. Requeue deve preservar histórico anterior.
3. `done` não deve ser sobrescrito para outro estado na mesma execução.
4. Conteúdo sensível em objetivo, constraints ou erros deve ser redigido antes de logs ou backup.

### Workflows

Workflows devem ser persistidos como planos derivados de Missions.

Dados mínimos:

- `workflow_id`;
- `mission_id`;
- `title`;
- `goal`;
- `status`;
- `spec_refs`;
- `guardian_refs`;
- `policy_refs`;
- `tasks` ou referências a tasks;
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

Regras:

1. Replanejamento deve criar nova versão lógica ou evento de mudança, não apagar plano anterior.
2. Workflows devem permanecer vinculados à Mission original.
3. Dependências devem ser persistidas de forma rastreável e determinística.
4. Tasks removidas por replanejamento devem permanecer auditáveis como `skipped` ou `cancelled` quando aplicável.

### Tasks

Tasks devem ser persistidas tanto como unidades planejadas do Workflow quanto como itens operacionais de fila quando a Task Queue as materializar.

Dados mínimos:

- `task_id`;
- `queue_item_id` quando aplicável;
- `workflow_id`;
- `mission_id`;
- `title`;
- `goal`;
- `task_type`;
- `status` ou `state`;
- `priority`;
- `dependencies`;
- `blocked_by`;
- `required_capabilities`;
- `context_refs`;
- `artifact_refs`;
- `guardian_decision_refs`;
- `model_decision_refs` quando disponíveis;
- `attempt_count`;
- `max_attempts`;
- `last_error`;
- `timestamps`;
- `audit_log_ref`.

Regras:

1. Tentativas de task devem ser persistidas separadamente ou como histórico append-only.
2. Retry não deve sobrescrever evidências da tentativa anterior.
3. Locks, quando existirem, devem ter dono, timestamp e expiração ou política de recuperação.
4. Falha de persistência de task de alto risco deve bloquear execução automática.

### Knowledge Documents

Knowledge Documents devem ser persistidos como conhecimento canônico ou metadados de conhecimento consumidos pelo Knowledge Hub.

Dados mínimos:

- `document_id`;
- `domain`;
- `title`;
- `content` ou `content_ref`;
- `canonical_uri`;
- `source_uri`;
- `source_type`;
- `version`;
- `canonical_format`;
- `language`;
- `sensitivity`;
- `trust_level`;
- `frontmatter`;
- `metadata`;
- `provenance`;
- `tags`;
- `redactions_applied`;
- `guardian_decision_refs`;
- `content_hash`;
- `created_at`;
- `updated_at`;
- `ingested_at`.

Regras:

1. Documento canônico deve ser fonte da verdade para índices derivados.
2. Índices, embeddings e caches devem ser tratados como derivados reconstruíveis.
3. Documentos sensíveis devem respeitar políticas de retenção, redaction, backup e provider externo.
4. Conteúdo de documentos deve ser tratado como dado não confiável, mesmo quando persistido.

### Canonical Documents

Canonical Documents produzidos pelo Canonicalizer devem ser persistidos de forma compatível com Knowledge Hub.

Regras:

1. `content_hash` deve refletir Markdown canônico normalizado.
2. `source_hash` deve ser preservado quando disponível e permitido.
3. `conversion_confidence`, warnings, prompt injection warnings e redactions devem ser persistidos.
4. Atualização de Canonical Document deve invalidar índices, caches e embeddings derivados.
5. Documento bloqueado por política não deve ser persistido como utilizável para RAG.

### Guardian Decisions

Guardian Decisions devem ser persistidas como decisões auditáveis de governança.

Dados mínimos:

- `evaluation_id`;
- `mission_id`;
- `decision`;
- `risk_level`;
- `guardian_mode`;
- `matched_policies`;
- `violations`;
- `reasons`;
- `required_actions`;
- `approval_requirements`;
- `blocked_items`;
- `warnings`;
- `safe_alternatives`;
- `limits_applied`;
- `redactions_applied`;
- `created_at`;
- `expires_at`;
- `metadata`.

Regras:

1. Decisão Guardian deve ser referenciável por Mission, Workflow, Task, Knowledge Document, Canonical Document, Provider Request e audit event.
2. Decisões expiradas devem permanecer auditáveis, mas não devem autorizar novas ações automaticamente.
3. Evidências sensíveis de violações devem ser redigidas.
4. Falha ao persistir decisão Guardian deve bloquear operação automática sensível.

### Model Decisions

Model Decisions devem ser persistidas como evidências de seleção de modelo e provider.

Dados mínimos:

- `decision_id` ou referência equivalente;
- `mission_id` quando houver;
- `workflow_id` quando houver;
- `task_id` quando houver;
- `selected_model_ref`;
- `selected_provider_ref`;
- `selected_runtime`;
- `small_model_ref` quando houver;
- `fallback_chain_refs`;
- `reason`;
- `policy_sources`;
- `estimated_cost`;
- `quality_expectation`;
- `requires_review`;
- `requires_user_approval`;
- `security_notes`;
- `created_at`.

Regras:

1. Persistência deve armazenar referências e metadados suficientes, não credenciais de provider.
2. Decisão de modelo deve ser vinculada ao contexto de missão, workflow ou task que a consumiu.
3. Uso pago, externo ou sensível deve ser rastreável.
4. Fallback deve preservar cadeia de decisão e motivo.

## Logs e Audit Trail

Audit trail deve ser append-only sempre que possível.

Eventos mínimos:

- entidade criada;
- entidade atualizada;
- transição de estado;
- tentativa iniciada e finalizada;
- decisão Guardian persistida;
- decisão de modelo persistida;
- documento canonicalizado;
- documento ingerido;
- índice ou cache invalidado;
- redaction aplicada;
- backup iniciado e finalizado;
- migration planejada, iniciada, concluída ou falhada;
- erro de persistência;
- operação bloqueada por política.

Campos mínimos de evento:

- `event_id`;
- `event_type`;
- `schema_version`;
- `occurred_at`;
- `actor_ref`;
- `mission_id` quando aplicável;
- `workflow_id` quando aplicável;
- `task_id` quando aplicável;
- `entity_type`;
- `entity_id`;
- `operation`;
- `before_hash` quando aplicável;
- `after_hash` quando aplicável;
- `guardian_decision_refs`;
- `model_decision_refs`;
- `redactions_applied`;
- `metadata`.

Regras:

1. Audit logs não devem conter segredos em claro.
2. Payload completo só pode ser registrado quando política permitir explicitamente.
3. Logs devem preferir IDs, hashes, referências, diffs resumidos e metadados.
4. Eventos críticos devem ser persistidos antes de marcar operação como concluída quando possível.
5. Falha de audit trail deve bloquear encerramento automático de missões ou workflows de alto risco.

## Serialização Determinística

Persistência deve usar serialização determinística para permitir hashes estáveis, diffs legíveis, backups verificáveis e testes de contrato.

Regras:

1. Campos devem ter ordem estável quando serializados em texto.
2. Objetos devem ser normalizados antes do cálculo de hash.
3. Timestamps devem usar formato UTC ISO 8601 quando aplicável.
4. Coleções semânticas devem ter ordenação definida quando a ordem não representar significado.
5. Valores ausentes devem ter política explícita entre omitir e serializar como `null`.
6. JSON determinístico é permitido para registros estruturados iniciais.
7. Markdown canônico permanece formato de conteúdo para documentos quando aplicável.
8. Serialização deve incluir `schema_version`.
9. Mudança de serialização canônica deve ser versionada e migrável.

## Versionamento de Schema

Todo registro persistido deve declarar versão de schema.

Regras:

1. Schema deve ter versão por tipo de registro.
2. Versão de schema deve ser independente da versão do package quando possível.
3. Leitura deve validar compatibilidade antes de hidratar entidade de domínio.
4. Schema desconhecido deve falhar de forma segura ou exigir migration.
5. Adapters devem declarar quais versões conseguem ler e escrever.
6. Backups devem registrar versões de schema incluídas.
7. Alterações incompatíveis devem exigir migration planejada e auditável.

## Migrations Futuras

Migrations devem permitir evolução de schemas e adapters sem perda de rastreabilidade.

Tipos previstos:

- migration de schema lógico;
- migration de layout filesystem;
- migration de memória ou cache para filesystem;
- migration de filesystem para SQLite;
- migration de SQLite para PostgreSQL;
- migration de PostgreSQL para PostgreSQL com pgvector;
- reindexação de documentos e embeddings;
- migration de versão de hash ou serialização.

Regras:

1. Migration deve ter plano, preflight, execução, validação e rollback ou estratégia de recuperação.
2. Migration não deve apagar dados antigos sem backup ou política explícita.
3. Migration deve preservar IDs, hashes, proveniência, timestamps relevantes e audit trail.
4. Migration que envolva dados sensíveis deve passar pelo Guardian Engine.
5. Migration de embeddings deve registrar modelo, provider, dimensão e índice afetado.
6. Migration deve ser idempotente quando possível.
7. Migration falhada deve deixar estado diagnosticável e seguro.

## Segurança de Segredos

Segredos incluem tokens, chaves, senhas, certificados privados, connection strings, cookies, credenciais cloud, headers de autenticação, dados pessoais sensíveis e qualquer valor marcado como sensível por política.

Regras:

1. Segredos não devem ser persistidos em claro por padrão.
2. Persistence Layer deve aceitar referências a segredos, não valores, quando componentes precisarem rastrear dependências.
3. Connection strings e credenciais de storage devem permanecer fora de registros auditáveis.
4. Erros de storage devem ser sanitizados antes de persistência ou exibição.
5. Backups não devem ampliar exposição de segredos.
6. Segredos detectados em payload devem acionar redaction, bloqueio ou aprovação conforme política.
7. Conteúdo com segredo não redigido não deve ser enviado a provider externo de storage, backup, busca ou embedding sem autorização explícita.

## Redaction

Redaction é obrigatória antes de persistir dados sensíveis em logs, audit trail, caches, índices, backups ou providers externos quando política exigir.

Regras:

1. Redaction deve preservar utilidade auditável sem revelar valor sensível.
2. Redaction deve registrar tipo de dado redigido, localização aproximada e política aplicada.
3. Redaction não deve destruir o documento original quando política exigir retenção segura separada.
4. Redaction aplicada deve ser rastreável por `redactions_applied`.
5. Falha de redaction obrigatória deve bloquear persistência automática.
6. Reprocessamento de redaction deve invalidar índices, caches e backups derivados quando necessário.

## Backup e Restore

Backup deve permitir recuperação de estado, auditoria e continuidade sem violar privacidade ou segurança.

Escopo mínimo de backup:

- Missions;
- Workflows;
- Tasks;
- Task attempts;
- Knowledge Documents;
- Canonical Documents;
- Guardian Decisions;
- Model Decisions;
- audit logs;
- schema metadata;
- referências de índices derivados quando aplicável.

Regras:

1. Backup deve ser explícito, auditável e governado por política.
2. Backup inicial em filesystem deve produzir artefatos determinísticos quando possível.
3. Backup deve registrar origem, horário, adapter, schema versions, hashes e escopo.
4. Restore deve validar hashes, versões e compatibilidade de schema.
5. Backups sensíveis devem ser protegidos, redigidos ou criptografados conforme política futura.
6. Backup não deve incluir segredos em claro.
7. Índices derivados podem ser omitidos quando reconstruíveis, desde que isso seja registrado.
8. Restore não deve sobrescrever estado ativo sem preflight, confirmação ou política explícita.

## Rastreabilidade

Relações mínimas:

- Mission para Workflow;
- Mission para audit events;
- Workflow para Tasks;
- Task para Attempts;
- Task para Guardian Decisions;
- Task para Model Decisions;
- Task para artefatos;
- Knowledge Source para Canonical Document;
- Canonical Document para Knowledge Document;
- Canonical Document para chunks e índices derivados;
- Guardian Decision para entidade avaliada;
- Model Decision para task, capability ou provider request;
- Provider Request para Provider Result quando persistido;
- Backup para registros incluídos;
- Migration para registros afetados.

Regras:

1. Rastreabilidade não pode depender da memória do agente.
2. IDs devem ser estáveis dentro do ciclo de vida da entidade.
3. Referências devem usar IDs, hashes ou URIs canônicas, não caminhos frágeis quando houver alternativa.
4. Entidade derivada deve apontar para fonte e versão usada.
5. Exclusão lógica deve preservar rastreabilidade quando auditoria exigir.

## Limites de Dados

Persistence Layer deve declarar e aplicar limites para evitar consumo excessivo, vazamento de contexto, degradação de performance e custos inesperados.

Limites mínimos previstos:

- tamanho máximo por registro;
- tamanho máximo por payload textual;
- tamanho máximo por documento canônico;
- quantidade máxima de eventos por missão antes de compactação governada;
- retenção de logs;
- retenção de caches;
- quantidade máxima de resultados por query persistida;
- tamanho máximo de backup;
- quantidade máxima de backups locais;
- limite de documentos por domínio em adapters simples;
- limite de embeddings por índice futuro.

Regras:

1. Exceder limite deve gerar erro claro, truncamento governado ou exigência de revisão, nunca perda silenciosa.
2. Truncamento não deve ocorrer em dados obrigatórios para auditoria sem registrar evento.
3. Conteúdo grande deve preferir `content_ref`, chunking ou storage especializado.
4. Adapters simples devem declarar limites menores e falhar com alternativa segura.
5. Limites podem ser reduzidos por Guardian Specs, projeto ou missão.

## Storage Inicial em Memória

Storage em memória é permitido para testes de contrato, protótipos, execução efêmera e ambientes sem persistência durável.

Regras:

1. Adapter em memória deve ser determinístico.
2. Adapter em memória deve deixar claro que não oferece durabilidade.
3. Adapter em memória não deve ser usado para missões de alto risco que exijam audit trail durável.
4. Adapter em memória pode ser usado em testes, validações, dry-run e workflows descartáveis.
5. Export para backup ou filesystem deve ser possível em futuro contrato quando durabilidade for necessária.

## Storage Inicial em Filesystem

Storage em filesystem é permitido como adapter inicial Local First, auditável e legível por humanos.

Características desejadas:

- um registro por arquivo quando isso simplificar auditoria;
- JSON determinístico para metadados estruturados;
- Markdown para conteúdo canônico;
- escrita atômica por arquivo quando possível;
- nomes derivados de IDs seguros;
- diretório local ao workspace ou path autorizado;
- separação entre fonte da verdade, logs, caches e índices derivados.

Regras:

1. Paths devem ser validados contra path traversal.
2. Filesystem adapter não deve alterar configurações globais.
3. Filesystem adapter não deve exigir `sudo`.
4. Escritas devem preferir arquivo temporário e rename atômico quando possível.
5. Arquivos de cache e índices derivados devem ser identificáveis como derivados.
6. Layout físico inicial não deve virar contrato arquitetural imutável.
7. Concorrência deve ser conservadora; locks devem ser explícitos se necessários.
8. Falha parcial deve preservar diagnóstico e evitar corrupção silenciosa.

## Suporte Futuro a SQLite

SQLite é opção futura para persistência local durável, transacional e de baixa operação.

Uso previsto:

- Missions;
- Workflows;
- Tasks;
- audit logs;
- Guardian Decisions;
- Model Decisions;
- metadados de Knowledge Documents;
- cache local governado.

Regras:

1. SQLite deve ser adapter, não dependência do núcleo.
2. Schema SQLite deve ser definido por Spec ou ADR antes de implementação.
3. Migrations SQLite devem ser versionadas e auditáveis.
4. SQLite não deve ser assumido como adequado para todos os cenários de concorrência.
5. Conteúdo grande pode permanecer em arquivos com metadados no banco, conforme política futura.

## Suporte Futuro a PostgreSQL

PostgreSQL é opção futura para persistência robusta, multiusuário, transacional e com consultas avançadas.

Uso previsto:

- estado de missões e filas;
- workflows e tasks;
- tentativas e locks;
- audit trail estruturado;
- Guardian Decisions;
- Model Decisions;
- metadados de documentos;
- permissões e retenção futuras;
- consultas operacionais e observabilidade.

Regras:

1. PostgreSQL deve ser acessado por adapter governado.
2. O framework não deve assumir PostgreSQL instalado.
3. Configuração, credenciais e connection strings devem ser tratadas como segredos.
4. Schema final deve ser definido em Spec ou ADR antes de implementação.
5. Migrations devem preservar rastreabilidade, logs e compatibilidade quando possível.
6. PostgreSQL não deve ser acessado diretamente por agentes, skills ou componentes de domínio.

## Suporte Futuro a PostgreSQL + pgvector

PostgreSQL com pgvector é opção futura para combinar persistência estruturada e índices vetoriais, especialmente para Knowledge Hub e Code Intelligence.

Uso previsto:

- chunks de Canonical Documents;
- embeddings;
- metadados de índices;
- busca vetorial;
- busca híbrida;
- invalidação e reindexação;
- rastreabilidade entre embedding, documento, chunk, modelo e provider.

Regras:

1. pgvector deve ser adapter ou capacidade do adapter PostgreSQL, não contrato central.
2. Dimensão de embedding deve vir do índice e do modelo selecionado, não ser hardcoded no núcleo.
3. No ambiente atual, `nomic-embed-text` com dimensão 768 pode ser provider inicial, mas não regra universal.
4. Troca de modelo de embedding deve criar novo índice, nova versão ou reindexação governada.
5. Embeddings de conteúdo sensível exigem redaction e avaliação Guardian antes de persistência.
6. Índices vetoriais são derivados e devem ser reconstruíveis a partir de Canonical Documents quando possível.

## Integração com Provider Gateway

Persistence Layer deve integrar Provider Gateway quando storage concreto for tratado como provider ou depender de adapter substituível.

Operações conceituais de provider:

- `persist_record`;
- `load_record`;
- `list_records`;
- `query_records`;
- `append_audit_event`;
- `create_backup`;
- `restore_backup`;
- `run_migration`;
- `upsert_vector_chunk` futuro;
- `query_vector_index` futuro.

Regras:

1. Provider Gateway deve selecionar adapter conforme capabilities, política, ambiente e Guardian Engine.
2. Persistence Layer não deve contornar Provider Gateway para providers externos ou infraestrutura concreta governada.
3. Fallback entre storages deve exigir avaliação quando alterar durabilidade, privacidade, custo, rede ou retenção.
4. ProviderResult de persistência deve ser registrado como evidência quando operação for crítica.
5. Falha de provider deve retornar erro normalizado e seguro.

## Integração com Guardian Engine

Guardian Engine deve avaliar operações de persistência quando houver risco.

Pontos mínimos de avaliação:

- persistência de dados sensíveis;
- detecção de segredo;
- redaction obrigatória;
- envio de dados para storage externo;
- backup de dados sensíveis;
- restore que sobrescreva estado;
- migration destrutiva ou incompatível;
- mudança de adapter;
- reindexação em massa;
- persistência de embeddings;
- retenção ou exclusão de audit logs;
- exportação de dados.

Contexto mínimo enviado ao Guardian Engine:

- `mission_id` quando houver;
- `workflow_id` quando houver;
- `task_id` quando houver;
- `evaluation_type` como `persistence_operation`;
- `operation`;
- `record_type`;
- `adapter_ref`;
- `data_sensitivity`;
- `redaction_policy`;
- `retention_policy`;
- `backup_policy`;
- `provider_policy`;
- `network_policy`;
- `schema_version`;
- `prior_decision_refs`.

Regras:

1. Decisão `block` deve impedir a operação de persistência afetada.
2. Decisão `require_approval` deve impedir execução automática até aprovação.
3. Falha do Guardian Engine deve bloquear operações automáticas de alto risco.
4. Decisões Guardian devem ser persistidas ou referenciadas quando a operação avançar.
5. Guardian Engine pode reduzir retenção, exigir redaction, exigir local-only ou proibir backup externo.

## Provider Agnostic e Storage Agnostic

Regras:

1. O núcleo do framework não deve depender obrigatoriamente de filesystem, SQLite, PostgreSQL, pgvector, object storage, cloud, MCP ou provider específico.
2. Contratos devem descrever operações e garantias, não drivers ou comandos.
3. Capabilities, Skills e Agents não devem nomear banco ou storage concreto.
4. Storage deve ser selecionado por adapter disponível, política, risco, escala, privacidade e ambiente detectado.
5. Ambientes locais, CI, servidores SSH-first e futuras APIs devem poder escolher adapters diferentes.
6. Trocar adapter não deve alterar o significado das entidades persistidas.

## Erros e Degradação Segura

Erros mínimos:

- schema incompatível;
- registro inexistente;
- conflito de versão;
- lock expirado ou inválido;
- escrita parcial;
- falha de serialização;
- hash divergente;
- redaction obrigatória falhou;
- segredo detectado;
- Guardian Engine bloqueou operação;
- adapter indisponível;
- limite de dados excedido;
- backup inválido;
- migration falhou;
- permissão negada;
- path não autorizado;
- provider externo não autorizado.

Regras:

1. Erro deve explicar causa e alternativa segura quando possível.
2. Erro não deve vazar segredo, path sensível ou credencial.
3. Persistência ambígua deve preferir bloquear conclusão automática.
4. Operações idempotentes devem permitir retry seguro quando possível.
5. Falha em dados derivados deve permitir reconstrução; falha em fonte da verdade deve bloquear operação crítica.

## Relação com Guardian Specs

### Security by Design

Persistence Layer deve proteger segredos, validar paths, controlar storage externo, aplicar redaction, evitar logs sensíveis e bloquear operações destrutivas sem política explícita.

### Token Efficiency

Persistence Layer deve armazenar referências, hashes, chunks e metadados em vez de duplicar payloads extensos desnecessariamente.

### AI Quality Assurance

Decisões, artefatos, validações e evidências devem ser persistidos de forma rastreável para revisão, replay e auditoria.

### Cost Optimization

Storage, backup, cache e índices derivados devem evitar duplicação, permitir deduplicação e declarar custo ou limites quando provider pago ou externo for usado.

### Architecture Governance

Persistence Layer deve preservar fronteiras entre núcleo, Provider Gateway, Guardian Engine, Knowledge Hub, Mission Runner, Workflow Engine e adapters.

### Documentation Governance

Schemas, migrations, backups, decisões de storage e mudanças de adapter devem ser documentados por Specs, ADRs ou audit events conforme impacto.

### Testing Governance

Implementações futuras devem ter testes de contrato para serialização determinística, redaction, schema versioning, migrations, audit trail, backup, restore e compatibilidade entre adapters.

### Compliance Governance

Persistência deve respeitar retenção, privacidade, jurisdição, consentimento, exportação, exclusão e auditoria conforme políticas aplicáveis.

### Observability Governance

Persistence Layer deve emitir eventos estruturados de leitura, escrita, erro, backup, restore, migration, redaction, bloqueio e degradação segura.

## Riscos e Mitigações

| Risco | Mitigação |
| --- | --- |
| Acoplamento ao filesystem inicial | Definir filesystem como adapter substituível e preservar portas abstratas. |
| Acoplamento a PostgreSQL ou pgvector | Tratar como adapters futuros e não contratos centrais. |
| Perda de audit trail | Exigir eventos mínimos e bloquear encerramento automático em contextos críticos. |
| Vazamento de segredos | Redaction, referências a segredos, logs sanitizados e avaliação Guardian. |
| Schema evoluir sem controle | Versionamento por record type e migrations auditáveis. |
| Backup ampliar exposição | Política de backup, redaction, hashes, escopo explícito e proteção futura. |
| Índice derivado virar fonte da verdade | Declarar índices, caches e embeddings como reconstruíveis. |
| Corrupção por escrita parcial | Escrita atômica quando possível, hashes e validação de leitura. |
| Dados grandes degradarem storage simples | Limites, chunking, content refs e adapters especializados futuros. |
| Migration destrutiva | Preflight, backup, validação e aprovação quando sensível. |

## Decisões aprovadas por esta Spec

1. Persistence Layer é uma camada arquitetural própria do Vercosa AI Framework.
2. Persistência deve ser exposta por portas e implementada por adapters.
3. O framework deve permanecer storage agnostic e provider agnostic.
4. Armazenamento inicial permitido inclui memória e filesystem local.
5. SQLite, PostgreSQL e PostgreSQL com pgvector são suportes futuros previstos, não dependências obrigatórias.
6. Missions, Workflows, Tasks, Knowledge Documents, Canonical Documents, Guardian Decisions e Model Decisions devem possuir persistência rastreável.
7. Logs e audit trail são parte obrigatória da persistência governada.
8. Serialização determinística é obrigatória para registros persistidos sempre que aplicável.
9. Todo registro persistido deve declarar schema version.
10. Migrations futuras devem ser planejadas, auditáveis e seguras.
11. Segredos não devem ser persistidos em claro.
12. Redaction deve ser aplicada antes de logs, backups, caches, índices ou providers externos quando política exigir.
13. Backups devem ser explícitos, verificáveis e governados por política.
14. Rastreabilidade entre entidades, decisões, eventos e artefatos é obrigatória.
15. Limites de dados devem ser declarados e aplicados.
16. Provider Gateway deve isolar providers concretos de storage quando aplicável.
17. Guardian Engine deve avaliar operações de persistência sensíveis.
18. Esta Spec não autoriza implementação de código, alteração de configurações globais ou uso de `sudo`.

## Critérios de aceite

- Existe uma Spec própria em `specs/framework/0013-persistence-layer.md`.
- A Spec define persistência como porta/adaptador.
- A Spec preserva storage agnostic.
- A Spec cobre armazenamento inicial em memória.
- A Spec cobre armazenamento inicial em filesystem.
- A Spec prevê suporte futuro a SQLite.
- A Spec prevê suporte futuro a PostgreSQL.
- A Spec prevê suporte futuro a PostgreSQL com pgvector.
- A Spec cobre persistência de Missions.
- A Spec cobre persistência de Workflows.
- A Spec cobre persistência de Tasks.
- A Spec cobre persistência de Knowledge Documents.
- A Spec cobre persistência de Canonical Documents.
- A Spec cobre persistência de Guardian Decisions.
- A Spec cobre persistência de Model Decisions.
- A Spec cobre logs e audit trail.
- A Spec define serialização determinística.
- A Spec define versionamento de schema.
- A Spec cobre migrations futuras.
- A Spec cobre segurança de segredos.
- A Spec cobre redaction.
- A Spec cobre backup.
- A Spec cobre rastreabilidade.
- A Spec cobre limites de dados.
- A Spec define integração com Provider Gateway.
- A Spec define integração com Guardian Engine.
- A Spec preserva provider agnostic.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não altera configurações globais.
- A Spec não exige nem usa `sudo`.

## Pendências

- Definir contratos formais das portas `MissionStore`, `WorkflowStore`, `TaskStore`, `KnowledgeDocumentStore`, `CanonicalDocumentStore`, `GuardianDecisionStore`, `ModelDecisionStore` e `AuditLogStore`.
- Definir schemas lógicos versionados por tipo de registro.
- Definir normalização exata para serialização determinística e hash.
- Definir layout filesystem inicial governado.
- Definir política padrão de retenção de audit logs.
- Definir política padrão de backup local.
- Definir catálogo de limites de dados por adapter.
- Definir Spec ou ADR para adapter SQLite.
- Definir Spec ou ADR para adapter PostgreSQL.
- Definir Spec ou ADR para uso de pgvector em Knowledge Hub e Code Intelligence.
- Definir formato de migration plan e migration log.
- Definir testes de contrato de persistência entre adapters.
- Definir política de criptografia futura para backups e dados sensíveis em repouso.

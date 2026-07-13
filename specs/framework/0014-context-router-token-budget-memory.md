# Spec 0014 — Context Router, Token Budget Manager e Memory Architecture

## Status

Proposta.

Esta Spec e conceitual e nao autoriza implementacao de codigo, alteracao em `src/`, testes, dependencias, configuracoes globais, banco, embeddings, pgvector ou RAG funcional.

## Visao geral

Esta Spec define a arquitetura de contexto, memoria e eficiencia de tokens do Vercosa AI Framework.

O objetivo e criar contratos conceituais para Context Router, Token Budget Manager, Context Package e camadas de memoria antes de qualquer implementacao funcional. O framework deve evitar prometer memoria infinita e deve tratar memoria como arquitetura em camadas: persistencia duravel, documentos canonicos, Knowledge Hub, indices derivados, roteamento de contexto, budgets e pacotes rastreaveis.

## Objetivos

- Definir Context Router como componente que seleciona, compoe e justifica contexto.
- Definir Token Budget Manager como componente que estima, reserva e limita tokens.
- Definir Context Package como artefato citavel, rastreavel e governado.
- Definir Context Source, Context Item, Context Citation, Context Redaction, Context Omission Reason, Context Policy Reference e Memory Layer.
- Separar memoria persistente, Knowledge Hub, Semantic Index futuro, Context Router e pacotes finais.
- Definir fluxo entre Policy Engine, Context Router, Knowledge Hub, Canonicalizer, Persistence, Token Budget Manager, Guardian Engine, Model Selection Engine e Runtime Adapter.
- Preservar provider agnostic, storage agnostic, runtime agnostic e model agnostic.
- Preparar Semantic Index, embeddings e pgvector como futuros adapters derivados, nao requisitos centrais.

## Nao objetivos

- Nao implementar codigo.
- Nao criar novo modulo em `src/`.
- Nao alterar testes.
- Nao adicionar dependencias.
- Nao criar banco, tabela, migracao, indice vetorial ou schema fisico.
- Nao escolher pgvector, PostgreSQL, Ollama, OpenCode, Claude Code ou qualquer provider como default obrigatorio.
- Nao implementar embeddings, RAG, reranking, semantic chunking ou cache executavel.
- Nao prometer memoria infinita.
- Nao definir comportamento estavel para algo ainda futuro.

## Componentes

### Context Router

Componente responsavel por receber uma necessidade de contexto e produzir um Context Package.

Responsabilidades:

- interpretar objetivo, task, agente, role, dominio e risco;
- consumir politicas resolvidas;
- obter candidatos de contexto por Knowledge Hub, Canonicalizer, Persistence Layer e Semantic Index futuro;
- selecionar, ordenar, deduplicar, reduzir e justificar itens;
- separar instrucoes confiaveis de dados recuperados;
- preservar citacoes;
- registrar redactions e omissoes;
- produzir Context Package rastreavel;
- solicitar avaliacao Guardian quando necessario;
- expor requisitos de contexto ao Model Selection Engine.

Nao responsabilidades:

- persistir diretamente;
- executar providers, tools, MCPs, bancos, APIs, shell ou runtimes;
- escolher modelo concreto;
- resolver politica global;
- fazer enforcement operacional;
- gerar embeddings;
- substituir Knowledge Hub ou Canonicalizer.

### Token Budget Manager

Componente responsavel por estimar, reservar, alocar, limitar e reportar tokens.

Responsabilidades:

- estimar tokens por item, pacote, instrucao, historico e output esperado;
- reservar margem de resposta;
- aplicar limites por missao, workflow, task, assignment e ciclo;
- indicar excedentes;
- sugerir reducao, omissao, resumo ou escalonamento;
- registrar consumo estimado e real quando disponivel;
- fornecer `context_size` e janela minima ao Model Selection Engine.

Nao responsabilidades:

- selecionar fontes;
- escolher modelo;
- decidir seguranca;
- redigir conteudo;
- executar sumarizacao com modelo sem fluxo governado;
- persistir diretamente.

### Context Package

Artefato produzido pelo Context Router para uma solicitacao especifica.

Campos conceituais minimos:

- `context_package_id`;
- `mission_id`, `workflow_id`, `task_id`, `attempt_id`, `agent_assignment_id` quando aplicaveis;
- `request_goal`;
- `scope`;
- `items`;
- `sources`;
- `citations`;
- `token_estimate`;
- `output_token_reservation`;
- `redactions`;
- `omission_reasons`;
- `policy_refs`;
- `guardian_decision_refs`;
- `model_requirements`;
- `content_hash`;
- `cache_key` quando aplicavel;
- `warnings`;
- `created_at`;
- `metadata`.

### Context Source

Origem de contexto candidata ou selecionada.

Exemplos:

- Spec;
- ADR;
- README;
- documento canonico;
- resultado de busca textual;
- resultado de Semantic Index futuro;
- task record;
- decision record;
- validation result;
- artifact persistido;
- conversa autorizada.

Campos conceituais:

- `source_id`;
- `source_type`;
- `domain`;
- `uri`;
- `content_hash`;
- `trust_level`;
- `sensitivity`;
- `canonical_ref`;
- `policy_refs`;
- `metadata`.

### Context Item

Trecho, resumo, referencia ou metadado incluido no Context Package.

Campos conceituais:

- `context_item_id`;
- `source_ref`;
- `content` ou `content_ref`;
- `item_type` como `excerpt`, `summary`, `reference`, `instruction`, `metadata` ou `evidence`;
- `rank`;
- `reason_selected`;
- `token_estimate`;
- `citations`;
- `redactions`;
- `trust_level`;
- `sensitivity`;
- `is_untrusted_data`;
- `metadata`.

### Context Citation

Referencia auditavel de origem.

Campos conceituais:

- `citation_id`;
- `source_ref`;
- `document_id`;
- `canonical_uri`;
- `source_uri`;
- `path`;
- `heading`;
- `line_range`;
- `chunk_id`;
- `content_hash`;
- `retrieved_at`;
- `metadata`.

### Context Redaction

Registro de conteudo removido ou mascarado.

Campos conceituais:

- `redaction_id`;
- `redaction_type`;
- `target_ref`;
- `policy_ref`;
- `reason`;
- `approximate_location`;
- `replacement` quando seguro;
- `guardian_decision_ref`;
- `metadata`.

Redaction nao deve expor o valor original.

### Context Omission Reason

Motivo registrado para contexto candidato nao incluido.

Valores conceituais iniciais:

- `token_budget_exceeded`;
- `policy_denied`;
- `sensitivity_denied`;
- `low_relevance`;
- `duplicate`;
- `stale_index`;
- `missing_citation`;
- `uncanonicalized_source`;
- `guardian_blocked`;
- `requires_approval`;
- `prompt_injection_risk`;
- `untrusted_source`;
- `cache_invalid`;
- `outside_scope`.

### Context Policy Reference

Referencia a politica que influenciou selecao, omissao, redaction, limite ou entrega.

Campos conceituais:

- `policy_ref_id`;
- `policy_source`;
- `policy_name`;
- `scope`;
- `decision_effect`;
- `resolved_policy_ref`;
- `metadata`.

### Memory Layer

Camada de memoria na arquitetura.

Camadas conceituais:

- `ephemeral_context`: contexto temporario de uma execucao ou ciclo;
- `working_memory`: estado de task, agent assignment e plano em andamento;
- `persistent_memory`: registros duraveis de missoes, workflows, tasks, decisoes, validacoes e artefatos;
- `canonical_knowledge`: documentos canonicos e metadados governados;
- `derived_indexes`: busca textual, caches, chunks e Semantic Index futuro;
- `context_packages`: pacotes finais entregues ou reutilizados;
- `audit_memory`: decisoes, logs e evidencias de validacao.

## Fluxo esperado

Fluxo conceitual:

```text
Mission / Task / Agent Request
↓
Policy Engine
↓
Context Router
↓
Knowledge Hub / Canonicalizer / Persistence / future Semantic Index
↓
Token Budget Manager
↓
Guardian Engine
↓
Model Selection Engine
↓
Runtime Adapter
```

Regras do fluxo:

1. Policy Engine resolve politicas antes da selecao final de contexto.
2. Context Router coleta candidatos e monta pacote proposto.
3. Token Budget Manager estima e limita o pacote.
4. Context Router reduz ou omite itens quando o orcamento exigir.
5. Guardian Engine avalia risco operacional do pacote quando houver sensibilidade, provider externo, prompt injection, redaction, cross-domain ou excedente.
6. Model Selection Engine escolhe modelo compativel com pacote aprovado, janela necessaria, privacidade e custo.
7. Runtime Adapter recebe apenas contexto aprovado, referencias e limites.

## Contratos conceituais

### Context Request

Entrada minima:

- `request_id`;
- `mission_id`;
- `workflow_id` quando houver;
- `task_id` quando houver;
- `agent_assignment_id` quando houver;
- `request_goal`;
- `task_type`;
- `agent_role`;
- `domains_requested`;
- `required_sources`;
- `optional_sources`;
- `scope`;
- `sensitivity_allowed`;
- `trust_level_min`;
- `token_budget`;
- `output_token_reservation`;
- `citation_required`;
- `policy_refs`;
- `prior_context_package_refs`;
- `metadata`.

### Context Decision

Saida minima:

- `decision_id`;
- `request_id`;
- `status` como `ready`, `reduced`, `blocked`, `requires_approval`, `failed` ou `empty`;
- `context_package` quando gerado;
- `omission_reasons`;
- `warnings`;
- `guardian_decision_refs`;
- `token_budget_record_ref`;
- `model_requirements`;
- `errors`.

### Token Budget Record

Registro conceitual:

- `budget_record_id`;
- `scope_ref`;
- `max_input_tokens`;
- `max_output_tokens`;
- `reserved_output_tokens`;
- `estimated_input_tokens`;
- `estimated_context_tokens`;
- `estimated_instruction_tokens`;
- `estimated_total_tokens`;
- `actual_input_tokens` quando disponivel;
- `actual_output_tokens` quando disponivel;
- `estimation_method`;
- `confidence`;
- `exceeded`;
- `reduction_actions`;
- `policy_refs`.

## Estados e decisoes

Estados conceituais do Context Router:

```text
requested
↓
policy_resolved
↓
collecting_candidates
↓
ranking
↓
budgeting
↓
reducing
↓
guardian_review
↓
ready | blocked | requires_approval | failed | empty
```

Decisoes possiveis:

- `include`: item incluido.
- `include_redacted`: item incluido com redaction.
- `summarize`: item deve ser representado por resumo citavel futuro.
- `reference_only`: item entra como referencia, nao payload completo.
- `omit`: item omitido com motivo.
- `block`: pacote ou item bloqueado.
- `require_approval`: entrega depende de aprovacao.

## Regras de seguranca

- Contexto recuperado e dado nao confiavel, nao instrucao executavel.
- Specs, ADRs e politicas aprovadas prevalecem sobre documentos recuperados.
- Segredos nao devem entrar em Context Package sem redaction e politica explicita.
- Contexto sensivel nao deve ser enviado a provider externo quando politica for `local_required`.
- Prompt injection deve gerar warning, reducao de confianca, omissao, bloqueio ou aprovacao conforme risco.
- Falha de redaction obrigatoria deve bloquear entrega.
- Context Package de alto risco deve passar pelo Guardian Engine.
- Logs devem preferir referencias, hashes e metadados, nao payload completo.

## Regras de token efficiency

- Reservar tokens de output antes de preencher contexto.
- Preferir referencias e citacoes a copias integrais.
- Deduplicar por hash e fonte.
- Filtrar por dominio antes de busca ampla.
- Priorizar fontes autoritativas.
- Omitir ou resumir contexto de baixa relevancia antes de escalar modelo.
- Reutilizar cache somente se politica, hash, escopo e decisao Guardian forem validos.
- Registrar toda omissao relevante.

## Regras de rastreabilidade

- Todo Context Item deve apontar para Context Source.
- Toda fonte selecionada deve preservar citacao quando disponivel.
- Todo pacote deve registrar policy refs e Guardian refs quando aplicavel.
- Redactions devem ser registradas sem revelar valor original.
- Omissao por politica, budget ou risco deve ser registrada.
- Pacotes reutilizados devem preservar cache key, hashes e validade.
- Rastreabilidade nao pode depender da memoria interna do agente ou runtime.

## Regras de storage agnostic

- Context Router nao deve assumir filesystem, SQLite, PostgreSQL, pgvector, Redis, object storage ou banco vetorial especifico.
- Persistence Layer deve expor portas para registros futuros.
- Semantic Index deve ser derivado e reconstruivel.
- Storage concreto deve ser adapter substituivel.
- Troca de storage nao deve alterar significado de Context Package.

## Regras contra acoplamento a tecnologias especificas

O nucleo desta Spec nao deve acoplar a:

- pgvector;
- PostgreSQL;
- Ollama;
- OpenCode;
- Claude Code;
- LangGraph;
- AutoGen;
- MetaGPT;
- ECC;
- Hermes.

Essas tecnologias podem ser referencias, adapters ou ambientes futuros quando aprovadas por Spec/ADR propria. Nenhuma deve aparecer como requisito central do Context Router, Token Budget Manager ou Memory Architecture.

## Criterios de aceitacao para futura implementacao

Uma implementacao futura so deve ser aceita se:

- possuir Spec aprovada para o escopo de codigo;
- implementar contratos sem acoplar storage, provider, runtime ou banco vetorial especifico;
- produzir Context Package com itens, fontes, citacoes, estimativas de tokens, redactions, omission reasons e policy refs;
- integrar Policy Engine ou substituto provisoriamente documentado;
- consultar Guardian Engine para pacotes sensiveis ou arriscados;
- fornecer requisitos de contexto ao Model Selection Engine;
- nao permitir agentes acessarem Knowledge Store, banco, provider, MCP ou filesystem diretamente;
- preservar citacoes e hashes;
- registrar redactions e omissoes;
- falhar de forma segura quando politica, budget, redaction ou citacao obrigatoria nao puderem ser satisfeitos;
- ter testes de contrato para seguranca, tokens, rastreabilidade e storage agnostic.

## Testes esperados para futura implementacao

Testes futuros devem cobrir:

- selecao de contexto por dominio;
- priorizacao de Specs e ADRs sobre conversas;
- omissao por token budget;
- redaction sem vazamento;
- bloqueio por Guardian;
- `require_approval` em contexto sensivel;
- citacoes preservadas;
- deduplicacao por hash;
- cache invalidado por mudanca de hash;
- cache invalidado por mudanca de politica;
- pacote sem citacao obrigatoria falhando;
- contexto nao confiavel separado de instrucoes;
- Model Selection recebendo janela minima;
- ausencia de pgvector ou embeddings nao quebrando fluxo textual;
- storage adapter substituivel;
- logs sem segredos.

## Estado implementado e validado em 0108

O MVP implementado em `src/vercosa_ai_framework/context/` possui Context Router determinístico e Token Budget Manager aplicados sobre candidatos explícitos de contexto. O Context Router não implementa RAG, não executa busca vetorial, não cria memória global automática e não acessa banco ou provider externo.

Evidências:

- `tests/test_context_router_mvp.py` cobre seleção, omissão determinística e pacote de contexto.
- `tests/test_context_contracts.py` cobre contratos do pacote de contexto.
- `tests/test_policy_context_router_integration.py` cobre uso de políticas resolvidas no roteamento de contexto.
- `tests/test_token_budget_model_selection_integration.py` cobre produção de requisitos mínimos para Model Selection.
- `tests/test_agent_execution_governance_0107.py` valida Context Router e Token Budget Manager no fluxo integrado governado, incluindo omissão determinística de item grande e propagação do `context_package_id`.

O `ContextPackage` atual produz requisitos mínimos de janela de contexto para Model Selection. Semantic Index, embeddings, pgvector, PostgreSQL, RAG e modelo definitivo de memória permanecem decisões futuras.

## Pendencias

- Definir Spec de implementacao do Context Router.
- Definir Spec de implementacao do Token Budget Manager.
- Definir schemas persistiveis de Context Package e Token Budget Record.
- Definir contrato formal entre Policy Engine e Context Router.
- Definir contrato formal entre Guardian Engine e Context Package.
- Definir adapter futuro de Semantic Index.
- Definir estrategia de chunking por dominio.
- Definir politica de retencao de conversas e pacotes de contexto.
- Definir ADR propria para pgvector se ele for escolhido como primeiro vector store adapter.
- Atualizar documentacao navegavel apos aprovacao desta Spec.

# Spec 0011 — Knowledge Hub

## Status

Proposta.

## Objetivo

Definir o Knowledge Hub do Vercosa AI Framework como a base de conhecimento governada, rastreável, text-only e provider agnostic usada para armazenar, canonicalizar, indexar, recuperar e entregar contexto relevante ao ciclo de desenvolvimento orientado por especificações.

O Knowledge Hub deve permitir que missões, workflows, agentes, skills e tools recuperem conhecimento com precisão, segurança e eficiência de tokens, sem acoplar o framework a um banco, provedor de embeddings, formato original de documento, IDE, runtime ou mecanismo vetorial específico.

## Contexto

As Specs 0001, 0002, 0005, 0009 e 0010 e a arquitetura central definem que:

- o framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design;
- Markdown canônico é o formato interno padrão de troca, versionamento, leitura humana e uso por agentes;
- arquivos binários devem ser convertidos para Markdown canônico antes de uso por agentes ou indexação;
- agentes não devem conhecer diretamente bancos, MCPs, APIs, filesystem ou providers;
- agentes solicitam Capabilities;
- Capabilities são implementadas por Skills;
- Skills usam Tools;
- Tools acessam providers por meio do Provider Gateway;
- o Model Selection Engine seleciona modelos e provedores adequados por política;
- o Guardian Engine governa segurança, tokens, custos, segredos, contexto e ações sensíveis;
- o ambiente atual pode usar PostgreSQL, pgvector, Ollama e embeddings locais, mas o framework não deve depender obrigatoriamente dessas escolhas.

O Knowledge Hub é a camada conceitual que organiza conhecimento do framework e de projetos. Ele não substitui o Canonicalizer, Provider Gateway, Model Selection Engine, Guardian Engine, Capabilities, Skills ou Tools.

## Escopo

Esta Spec cobre:

- Knowledge Hub como base de conhecimento do framework;
- Canonical Documents;
- Semantic Indexes;
- RAG por domínio;
- fontes de conhecimento;
- ingestão de Markdown;
- conversão futura de formatos não Markdown para Markdown canônico;
- uso de frontmatter YAML;
- relação com Canonicalizer;
- relação com Provider Gateway;
- relação com Model Selection Engine;
- relação com Guardian Engine;
- text-only como regra de eficiência de tokens;
- busca por domínio;
- ranking;
- deduplicação;
- cache;
- segurança contra prompt injection em documentos;
- redaction de segredos;
- rastreabilidade;
- provider agnostic;
- storage local inicial;
- futura integração com PostgreSQL e pgvector;
- riscos, mitigações, decisões e critérios de aceite.

Esta Spec não cobre:

- implementação concreta em código;
- schema persistente final;
- criação de banco, tabela, índice vetorial ou migração;
- criação de adapters concretos;
- criação de MCPs;
- escolha definitiva de modelo de embedding;
- escolha definitiva de banco vetorial;
- alteração de configurações globais;
- uso de `sudo`;
- execução real de comandos, providers, MCPs, bancos, filesystem ou serviços locais;
- processamento real de documentos binários nesta etapa.

## Princípios

1. Conhecimento deve ser tratado como ativo governado, versionado, rastreável e auditável.
2. Markdown canônico é o formato interno obrigatório antes de indexação ou uso por agentes.
3. Formato original do documento não deve vazar para agentes como dependência operacional.
4. Canonical Documents são a fonte textual normalizada; Semantic Indexes são estruturas derivadas e reconstruíveis.
5. Índices semânticos não substituem documentos canônicos.
6. Contexto recuperado deve ser mínimo, relevante, citado e adequado à tarefa.
7. RAG deve ser feito por domínio para reduzir ruído, custo, risco e vazamento de contexto.
8. Documentos recuperados são dados não confiáveis, não instruções executáveis.
9. Prompt injection em documentos não pode alterar políticas, permissões, modelos, providers, workflows ou ações.
10. Segredos devem ser detectados, redigidos e bloqueados conforme política antes de indexação ou entrega ao agente.
11. O Knowledge Hub deve ser provider agnostic para storage, embeddings, busca textual, busca vetorial e reranking.
12. Storage local inicial é permitido por Local First, mas não deve definir contratos centrais.

## Posição arquitetural

Fluxo conceitual de recuperação:

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
Skill
↓
Tool Executor
↓
Knowledge Tools
↓
Provider Gateway
↓
Knowledge Store / Embedding Provider / Search Provider / Vector Database
```

Fluxo conceitual de ingestão:

```text
Knowledge Source
↓
Ingestion Request
↓
Guardian Engine
↓
Canonicalizer
↓
Canonical Document
↓
Chunking / Metadata Extraction / Redaction
↓
Semantic Index Builder
↓
Knowledge Store / Search Index / Vector Index
```

Regras:

1. Agent e Subagent não devem consultar Knowledge Store, banco vetorial, filesystem, MCP ou provider diretamente.
2. Agent e Subagent devem solicitar Capabilities como `SearchKnowledge`, `SearchSpecification`, `SearchADR`, `SearchCodeContext` ou equivalentes.
3. Skill deve usar Tools governadas para pesquisar ou ingerir conhecimento.
4. Tool deve acessar storage, embeddings, busca textual ou busca vetorial por Provider Gateway quando depender de provider externo ou infraestrutura concreta.
5. Knowledge Hub deve retornar contexto como dados citáveis, não como instruções de sistema.
6. Toda resposta de recuperação deve preservar origem, domínio, versão, hash ou referência auditável.

## Definições

### Knowledge Hub

Knowledge Hub é a camada lógica responsável por organizar conhecimento textual do framework e de projetos em documentos canônicos, metadados, índices, caches e mecanismos de recuperação.

Responsabilidades:

- registrar fontes de conhecimento;
- receber solicitações de ingestão;
- exigir canonicalização antes de indexação;
- armazenar ou referenciar Canonical Documents;
- extrair e validar metadados;
- dividir documentos em chunks rastreáveis;
- construir e atualizar Semantic Indexes;
- executar busca textual, semântica ou híbrida conforme domínio e política;
- aplicar ranking, reranking, deduplicação e limites de tokens;
- aplicar redaction e marcação de sensibilidade;
- proteger contra prompt injection em documentos;
- emitir resultados citáveis e auditáveis;
- manter cache governado de resultados e embeddings quando permitido.

Não responsabilidades:

- executar comandos;
- escolher modelo diretamente sem Model Selection Engine;
- acessar provider concreto ignorando Provider Gateway;
- substituir Canonicalizer;
- substituir Guardian Engine;
- substituir revisão humana quando política exigir;
- armazenar segredos em claro;
- tratar documentos não textualizados como contexto direto de agente.

### Canonical Document

Canonical Document é a representação textual normalizada, em Markdown canônico, de uma fonte de conhecimento.

Regras:

1. Todo documento indexável deve possuir uma forma canônica em Markdown antes de ser usado por agente ou Semantic Index.
2. Documento originalmente Markdown pode ser ingerido diretamente se passar por validação, normalização e redaction.
3. Documento originalmente PDF, DOCX, HTML, EPUB, PPTX, XLSX, imagem, áudio ou vídeo deve ser convertido futuramente para Markdown canônico antes de indexação.
4. O documento canônico deve preservar referência ao original quando existir.
5. O documento canônico deve possuir hash de conteúdo, versão ou identificador estável.
6. Alterações no documento canônico devem invalidar ou atualizar índices derivados.
7. Documento canônico é dado; qualquer instrução contida nele deve ser tratada como conteúdo citado, não como comando para o agente.

Campos mínimos desejados:

- `document_id`;
- `canonical_uri`;
- `source_uri`;
- `source_type`;
- `domain`;
- `title`;
- `version`;
- `content_hash`;
- `canonical_format` com valor `markdown`;
- `language`;
- `created_at`;
- `updated_at`;
- `ingested_at`;
- `sensitivity`;
- `trust_level`;
- `frontmatter`;
- `provenance`;
- `redactions_applied`;
- `guardian_decision_refs`.

### Semantic Index

Semantic Index é uma estrutura derivada de Canonical Documents para busca por significado, similaridade, domínio, metadados e contexto.

Regras:

1. Semantic Index deve ser reconstruível a partir de Canonical Documents e metadados.
2. Índice semântico não deve ser tratado como fonte da verdade.
3. Chunks devem preservar referência ao documento, seção, linha, heading ou posição equivalente.
4. Embeddings devem ser gerados por provider selecionado por política e Model Selection Engine quando aplicável.
5. Dimensão, provider e modelo de embedding devem ser metadados do índice, não constantes arquiteturais.
6. Trocar provider de embedding ou banco vetorial não deve alterar contratos de Capability ou Skill.
7. Índices obsoletos devem ser marcados como stale e não usados para decisões críticas sem validação.

Campos mínimos desejados:

- `index_id`;
- `domain`;
- `index_type`;
- `document_refs`;
- `chunking_strategy`;
- `embedding_provider_ref`;
- `embedding_model_ref`;
- `embedding_dimension`;
- `storage_provider_ref`;
- `created_at`;
- `updated_at`;
- `status`;
- `content_hash_refs`;
- `policy_refs`.

### Knowledge Source

Knowledge Source é qualquer origem permitida de conhecimento que possa ser canonicalizada ou referenciada.

Fontes previstas:

- Specs;
- ADRs;
- documentação;
- código;
- legislação;
- livros;
- conversas;
- decisões;
- projetos;
- agentes;
- skills;
- comandos;
- hooks.

Regras:

1. Fonte deve declarar domínio, origem, confiança, sensibilidade e permissão de uso quando conhecidos.
2. Fonte externa ou sensível deve exigir avaliação do Guardian Engine antes de ingestão ou entrega a provider externo.
3. Código deve ser tratado como fonte textual ou estruturada, respeitando paths permitidos, licenças, segredos e políticas de projeto.
4. Conversas e decisões devem preservar autoria, data, contexto e nível de confiança quando disponível.
5. Legislação e livros podem exigir metadados de jurisdição, edição, licença, trecho e data de vigência.

### Domain

Domain é uma partição lógica de conhecimento usada para reduzir ruído, controlar acesso e orientar RAG.

Domínios iniciais previstos:

- `specs`;
- `adrs`;
- `docs`;
- `code`;
- `legal`;
- `books`;
- `conversations`;
- `decisions`;
- `projects`;
- `agents`;
- `skills`;
- `commands`;
- `hooks`;
- `guardian`;
- `architecture`.

Regras:

1. Busca deve declarar domínio ou permitir seleção automática justificada.
2. Domínio sensível pode exigir permissão específica.
3. RAG cross-domain deve ser explícito, rastreável e limitado por política.
4. Domínios não devem ser usados para esconder falta de metadados; documentos sem domínio confiável devem ser classificados como `unknown` ou bloqueados para uso crítico.

## Frontmatter YAML

Canonical Documents podem possuir frontmatter YAML para metadados e políticas locais.

Exemplo conceitual:

```yaml
---
document_id: spec-framework-0011
domain: specs
source_type: markdown
title: Knowledge Hub
version: 1
status: proposta
language: pt-BR
sensitivity: internal
trust_level: authoritative
provider: auto
model: auto
embedding_provider: auto
embedding_model: auto
security: strict
privacy: local_preferred
rag_allowed: true
indexing_allowed: true
redaction_required: true
---
```

Campos mínimos recomendados:

- `document_id`;
- `domain`;
- `source_type`;
- `title`;
- `version`;
- `status`;
- `language`;
- `sensitivity`;
- `trust_level`;
- `security`;
- `privacy`;
- `rag_allowed`;
- `indexing_allowed`;
- `redaction_required`.

Regras:

1. Frontmatter YAML pode orientar políticas locais, mas não pode sobrescrever Guardian Specs.
2. Campos de provider e modelo devem usar `auto` por padrão, salvo política aprovada em contrário.
3. Frontmatter não deve conter segredos.
4. Frontmatter inválido deve gerar warning ou bloqueio conforme criticidade do domínio.
5. Política declarada no frontmatter deve ser registrada como fonte de decisão quando influenciar ingestão, indexação ou recuperação.

## Ingestão de Markdown

A ingestão inicial deve aceitar Markdown como formato primário.

Etapas conceituais:

1. Receber `Ingestion Request` com fonte, domínio, permissões e objetivo.
2. Consultar Guardian Engine quando houver fonte sensível, externa, segredo, licença, compliance ou risco.
3. Validar path, origem, tamanho, encoding e tipo de fonte.
4. Ler Markdown permitido por Tool governada.
5. Normalizar para Markdown canônico.
6. Extrair e validar frontmatter YAML.
7. Detectar prompt injection, segredos e conteúdo sensível.
8. Aplicar redaction quando permitido e necessário.
9. Gerar `document_id`, hash e metadados.
10. Armazenar ou atualizar Canonical Document.
11. Criar chunks rastreáveis.
12. Atualizar Semantic Indexes e caches derivados conforme política.

Regras:

1. Markdown ingerido não deve ser presumido confiável apenas por estar no repositório.
2. Arquivos grandes devem ser chunkados antes de uso por agente.
3. Conteúdo duplicado deve ser detectado antes de gerar embeddings redundantes.
4. Falha de redaction obrigatória deve bloquear indexação quando houver risco de segredo.
5. Ingestão deve registrar logs suficientes para auditoria sem persistir segredo.

## Conversão futura para Markdown canônico

Formatos futuros previstos:

- PDF;
- DOCX;
- HTML;
- EPUB;
- PPTX;
- XLSX;
- imagens com OCR;
- áudio com transcrição;
- vídeo com transcrição e metadados temporais.

Regras:

1. Nenhum desses formatos deve ser entregue diretamente a agentes como contexto primário.
2. Conversão deve produzir Markdown canônico e metadados de proveniência.
3. Conversão deve preservar referências úteis como página, seção, slide, célula, timestamp ou bounding box quando aplicável.
4. OCR e transcrição devem declarar confiança, idioma, modelo ou ferramenta usada.
5. Baixa confiança de conversão deve reduzir ranking ou exigir validação humana em tarefas críticas.
6. Documento convertido deve manter vínculo com artefato original quando política permitir.
7. Conversores são providers ou tools governadas, não dependências diretas de agentes.

## Relação com Canonicalizer

Canonicalizer é o componente responsável por transformar fontes em Markdown canônico e normalizar estrutura textual.

Regras:

1. Knowledge Hub deve solicitar canonicalização; não deve embutir lógica final de conversão de formatos.
2. Canonicalizer deve receber fonte, formato, metadados e política aplicável.
3. Canonicalizer deve retornar Markdown canônico, metadados, warnings, confiança e referências de proveniência.
4. Knowledge Hub deve validar o resultado do Canonicalizer antes de indexar.
5. Falha de canonicalização deve bloquear indexação e RAG daquele artefato, salvo política explícita de uso parcial.
6. Canonicalizer deve tratar conteúdo convertido como dado não confiável e não como instrução.

## Relação com Provider Gateway

Knowledge Hub deve usar Provider Gateway para acessar providers concretos quando houver storage externo, banco, embeddings, busca vetorial, filesystem governado, OCR, transcrição, conversão ou serviços locais.

Regras:

1. Knowledge Tools devem emitir `ProviderRequest` normalizada para operações concretas.
2. Provider Gateway deve selecionar Provider Adapter conforme Provider Registry, permissões, ambiente, política e Guardian Engine.
3. Knowledge Hub não deve hardcodar PostgreSQL, pgvector, Ollama, filesystem, MCP ou API.
4. Provider externo não deve receber documento sensível sem política explícita.
5. Fallback de provider local para externo deve exigir nova avaliação quando houver dados sensíveis, custo, rede ou retenção.
6. Resultados de providers de busca, embedding, OCR ou conversão devem ser tratados como dados não confiáveis até validação.

Operações de provider previstas:

- `read_canonical_document`;
- `write_canonical_document`;
- `list_knowledge_sources`;
- `generate_embedding`;
- `upsert_semantic_chunk`;
- `query_text_index`;
- `query_vector_index`;
- `query_hybrid_index`;
- `convert_to_markdown`;
- `redact_sensitive_content`.

## Relação com Model Selection Engine

Model Selection Engine deve selecionar modelos para tarefas de embeddings, sumarização, extração, reranking, classificação, OCR/transcrição assistida por IA e compressão de contexto quando modelos forem necessários.

Regras:

1. Knowledge Hub não deve escolher modelo concreto diretamente quando a escolha envolver política, custo, qualidade, privacidade ou disponibilidade.
2. Seleção de modelo para embeddings deve considerar dimensão, idioma, domínio, custo, privacidade, localidade e compatibilidade com índice existente.
3. Troca de modelo de embedding deve criar novo índice, versão de índice ou processo de reindexação governado.
4. Modelos menores devem ser preferidos para classificação simples, deduplicação e extração leve quando cumprirem qualidade mínima.
5. Modelos locais devem ser preferidos quando política exigir `local_required` ou `local_preferred` e houver capacidade disponível.
6. Modelo pago ou externo só deve receber conteúdo sensível quando política permitir explicitamente.
7. Decisões de modelo que afetem índice ou RAG devem ser rastreáveis.

## Relação com Guardian Engine

Guardian Engine deve avaliar ingestão, indexação, recuperação e entrega de contexto quando houver risco.

Pontos mínimos de avaliação:

- ingestão de fonte externa;
- ingestão de domínio sensível;
- detecção de segredo;
- redaction obrigatória;
- envio de documento para provider externo;
- uso de modelo pago ou externo;
- RAG cross-domain;
- recuperação de contexto sensível;
- entrega de trechos grandes ao agente;
- uso de documento com baixa confiança;
- conversão de formatos com OCR, transcrição ou extração incerta;
- atualização ou exclusão de Canonical Documents;
- reindexação em massa;
- fallback que altere localidade, custo, rede, retenção ou exposição de dados.

Contexto mínimo enviado ao Guardian Engine:

- `mission_id` quando houver;
- `evaluation_type` como `knowledge_ingestion`, `knowledge_indexing`, `knowledge_retrieval` ou equivalente;
- `source_uri`;
- `document_id` quando houver;
- `domain`;
- `source_type`;
- `operation`;
- `data_sensitivity`;
- `trust_level`;
- `provider_policy`;
- `network_policy`;
- `privacy_policy`;
- `budget_policy`;
- `target_domains`;
- `requested_token_budget`;
- `prior_decision_refs`.

Regras:

1. Decisão `block` deve impedir ingestão, indexação, recuperação ou entrega conforme escopo da decisão.
2. Decisão `require_approval` deve bloquear execução automática.
3. Falha do Guardian Engine deve bloquear operação automática de alto risco.
4. Redactions determinadas pelo Guardian Engine devem ser aplicadas antes de indexação, cache, logs e entrega ao agente.
5. Knowledge Hub deve registrar `guardian_decision_ref` nos artefatos e resultados afetados.

## Text-only e eficiência de tokens

O Knowledge Hub deve operar internamente sobre texto estruturado, preferencialmente Markdown canônico.

Regras:

1. Conteúdo binário não deve ser enviado a agentes como contexto bruto.
2. Contexto recuperado deve ser menor que o documento original sempre que a tarefa não exigir documento completo.
3. Resultados devem priorizar trechos relevantes, citações e referências em vez de despejar documentos inteiros.
4. Chunks devem ter tamanho adequado ao domínio, modelo, tarefa e orçamento de tokens.
5. Busca deve aplicar filtros de domínio e metadados antes de expandir contexto.
6. Resumos e compressões devem preservar citações para trechos originais.
7. Conteúdo repetido deve ser deduplicado antes de ser enviado ao agente.
8. Cache pode ser usado para evitar recomputar embeddings, rankings e resultados recorrentes quando política permitir.

## RAG por domínio

RAG por domínio é a recuperação aumentada por geração limitada a domínios relevantes, com ranking e entrega de contexto governados.

Fluxo conceitual:

```text
Retrieval Request
↓
Domain Selection
↓
Policy / Guardian Evaluation
↓
Text Search + Semantic Search + Metadata Filters
↓
Ranking / Reranking
↓
Deduplication
↓
Token Budgeting
↓
Context Package
```

Regras:

1. Retrieval Request deve declarar objetivo, domínios desejados, sensibilidade e orçamento de tokens.
2. Se domínio não for declarado, seleção automática deve ser justificada e rastreável.
3. RAG de `specs` deve preferir Specs aprovadas ou mais autoritativas.
4. RAG de `adrs` deve considerar status da decisão e data.
5. RAG de `code` deve preservar path, símbolo, trecho e versão.
6. RAG de `legal` deve preservar jurisdição, vigência e referência oficial quando disponível.
7. RAG de `conversations` deve considerar confiança menor que Specs e ADRs, salvo decisão explicitamente promovida.
8. Cross-domain RAG deve limitar resultados por domínio para evitar domínio ruidoso dominar o contexto.
9. Context Package entregue ao agente deve separar instruções do sistema, pedido do usuário e documentos recuperados.

## Busca por domínio

Busca por domínio deve combinar filtros explícitos, metadados, busca textual, busca semântica e ranking.

Campos mínimos de `KnowledgeQuery`:

- `query_id`;
- `mission_id` quando houver;
- `task_id` quando houver;
- `query_text`;
- `domains`;
- `source_types`;
- `filters`;
- `top_k`;
- `token_budget`;
- `ranking_policy`;
- `sensitivity_allowed`;
- `trust_level_min`;
- `include_citations`;
- `guardian_decision_refs`.

Campos mínimos de `KnowledgeResult`:

- `query_id`;
- `result_id`;
- `domain`;
- `document_id`;
- `chunk_id`;
- `title`;
- `snippet`;
- `score`;
- `rank`;
- `citations`;
- `source_uri`;
- `content_hash`;
- `sensitivity`;
- `trust_level`;
- `warnings`;
- `redactions_applied`.

Regras:

1. Resultado sem citação ou referência deve ter menor confiança.
2. Busca deve falhar de forma segura quando domínio autorizado não estiver disponível.
3. Busca não deve ampliar domínios automaticamente quando a política restringir o escopo.
4. Busca deve distinguir ausência de resultado, índice indisponível, índice stale e bloqueio por política.

## Ranking e reranking

Ranking deve ordenar resultados por relevância, autoridade, atualidade, domínio, confiança, proximidade semântica, correspondência textual e adequação à tarefa.

Sinais mínimos de ranking:

- similaridade semântica;
- correspondência textual;
- domínio solicitado;
- autoridade da fonte;
- status do documento;
- atualidade;
- proximidade estrutural com heading, seção ou símbolo;
- confiança de conversão;
- sensibilidade permitida;
- histórico de uso validado quando permitido;
- penalização por duplicidade ou stale index.

Regras:

1. Ranking deve ser explicável em nível suficiente para auditoria.
2. Reranking por modelo deve passar pelo Model Selection Engine quando envolver escolha de modelo.
3. Resultado sensível não deve subir no ranking apenas por similaridade se política não permitir sua entrega.
4. Fontes autoritativas como Specs aprovadas devem prevalecer sobre conversas quando houver conflito.
5. Resultados obsoletos devem indicar status e ser penalizados ou bloqueados conforme criticidade.

## Deduplicação

Deduplicação deve reduzir redundância em documentos, chunks, embeddings e Context Packages.

Estratégias previstas:

- hash exato de conteúdo;
- normalização textual;
- similaridade semântica;
- comparação de source URI;
- comparação de headings e trechos;
- identificação de versões do mesmo documento;
- preferência por fonte mais autoritativa.

Regras:

1. Duplicata exata não deve gerar embeddings redundantes sem necessidade.
2. Duplicata semântica deve ser agrupada ou penalizada no ranking.
3. Quando duas fontes conflitarem, Knowledge Hub deve preservar ambas e marcar conflito em vez de apagar evidência.
4. Deduplicação não deve remover informação de proveniência.
5. Deduplicação aplicada deve ser rastreável.

## Cache

Cache pode ser usado para reduzir custo, latência e tokens.

Tipos de cache previstos:

- cache de Canonical Document normalizado;
- cache de chunks;
- cache de embeddings;
- cache de resultados de busca;
- cache de reranking;
- cache de Context Packages;
- cache de conversões futuras para Markdown.

Regras:

1. Cache deve ser invalidado por mudança de conteúdo, política, domínio, modelo, provider ou permissão relevante.
2. Cache de conteúdo sensível deve respeitar política de retenção e redaction.
3. Cache não deve conter segredos em claro.
4. Cache deve preservar referência à versão de documento e índice usados.
5. Resultado de cache não deve ignorar avaliação atual do Guardian Engine quando contexto ou política mudou.
6. Cache pode ser desabilitado por política de privacidade, segurança ou compliance.

## Segurança contra prompt injection em documentos

Documentos ingeridos ou recuperados podem conter instruções maliciosas, enganosas ou fora de escopo.

Exemplos de risco:

- documento instruir agente a ignorar Specs ou políticas;
- documento pedir execução de comando;
- documento solicitar exfiltração de segredo;
- documento simular mensagem de sistema;
- documento tentar alterar modelo, provider, orçamento ou permissões;
- documento inserir dados falsos para manipular ranking ou decisão.

Regras:

1. Conteúdo de documento recuperado deve ser encapsulado como dado citado.
2. Context Package deve separar claramente instruções confiáveis de trechos recuperados.
3. Trechos recuperados não podem conceder permissões, alterar políticas ou redefinir objetivo da missão.
4. Instruções conflitantes dentro de documentos devem ser ignoradas como instrução e tratadas apenas como conteúdo analisável.
5. Detecção de prompt injection deve gerar warning, reduzir confiança ou bloquear uso conforme risco.
6. Documentos não confiáveis não devem ser usados para ações sensíveis sem validação adicional.
7. Skills que usam Knowledge Hub devem tratar resultados como dados não confiáveis até validação.

## Redaction de segredos

Segredos incluem tokens, chaves, senhas, certificados privados, connection strings, cookies, credenciais cloud, headers de autenticação e qualquer valor marcado como sensível por política.

Regras:

1. Ingestão deve detectar padrões prováveis de segredo antes de indexação.
2. Segredo detectado deve ser redigido, bloqueado ou exigir aprovação conforme política.
3. Segredos não devem ser enviados a provider externo de embeddings, OCR, transcrição, busca ou reranking sem autorização explícita.
4. Embeddings de conteúdo com segredo não redigido devem ser tratados como vazamento potencial e bloqueados por padrão.
5. Logs, erros, warnings, cache, metadados e resultados não devem conter segredo em claro.
6. Redaction deve preservar rastreabilidade suficiente sem revelar valor sensível.
7. Detecção posterior de segredo deve invalidar caches e índices afetados.

## Rastreabilidade

Relações mínimas:

- Mission para KnowledgeQuery;
- Task para KnowledgeQuery;
- Capability Request para Skill;
- Skill para ToolExecutionRequest;
- ToolExecutionRequest para ProviderRequest;
- Knowledge Source para Canonical Document;
- Canonical Document para chunks;
- chunks para Semantic Index;
- Semantic Index para provider, modelo e dimensão de embedding;
- KnowledgeQuery para resultados;
- resultados para documentos, chunks, hashes e citações;
- Guardian Decision para ingestão, indexação ou recuperação;
- Model Selection Decision para embeddings, reranking ou sumarização;
- cache entry para documento, índice, política e query original.

Eventos mínimos:

- fonte registrada;
- ingestão solicitada;
- Guardian Engine consultado;
- canonicalização iniciada;
- canonicalização concluída;
- segredo detectado;
- redaction aplicada;
- documento canônico criado ou atualizado;
- chunk criado;
- embedding solicitado;
- índice atualizado;
- cache criado ou invalidado;
- query recebida;
- domínio selecionado;
- busca executada;
- ranking aplicado;
- deduplicação aplicada;
- Context Package produzido;
- operação bloqueada.

Regras:

1. Rastreabilidade não pode depender da memória do agente.
2. Logs devem preferir IDs, hashes, referências e metadados em vez de payload completo.
3. Payload completo só pode ser registrado quando política permitir explicitamente.
4. Toda entrega de contexto a agente deve ser reconstruível por referências.
5. Alterações em Canonical Documents devem permitir identificar índices e caches afetados.

## Provider agnostic

Regras:

1. Knowledge Hub não deve depender obrigatoriamente de PostgreSQL, pgvector, Ollama, OpenAI, Anthropic, GitHub, MCP, OpenCode, Linux ou ARM64.
2. Storage, busca textual, busca vetorial, embeddings, OCR, transcrição, conversão e reranking devem ser providers ou adapters substituíveis.
3. Capability não deve nomear banco, provider, MCP ou modelo concreto.
4. Skill deve depender de contrato funcional de busca ou ingestão, não de implementação.
5. Tool deve emitir operação técnica normalizada e usar Provider Gateway para providers concretos.
6. Ambiente atual pode fornecer providers iniciais, mas seleção deve considerar capacidade detectada e política.
7. Fallback entre providers não pode ampliar risco sem nova avaliação.

## Storage local inicial

O storage local inicial deve priorizar simplicidade, auditabilidade e versionamento humano.

Estrutura conceitual permitida:

- documentos canônicos em Markdown no repositório ou workspace autorizado;
- metadados em arquivos estruturados ou índice local;
- cache local governado;
- índices derivados reconstruíveis.

Regras:

1. Storage local inicial não deve exigir serviço privilegiado.
2. Storage local inicial não deve alterar configurações globais.
3. Paths devem ser permitidos por política e validação contra path traversal.
4. Arquivos derivados devem ser identificáveis como cache ou índice, não fonte da verdade.
5. Layout físico inicial não deve virar contrato arquitetural imutável.
6. Uso local deve continuar compatível com futura migração para storage especializado.

## Integração futura com PostgreSQL e pgvector

PostgreSQL com pgvector é uma opção futura importante para Knowledge Store e Semantic Indexes, especialmente no ambiente atual, mas não deve ser obrigatório.

Uso futuro previsto:

- persistir Canonical Document metadata;
- persistir chunks;
- persistir embeddings;
- executar busca vetorial;
- combinar filtros estruturados com similaridade;
- registrar audit trail;
- suportar reindexação e invalidação.

Regras:

1. PostgreSQL e pgvector devem ser acessados por Provider Adapter governado.
2. Schema final deve ser definido em Spec ou ADR próprio antes de implementação.
3. Dimensão de embedding deve vir do modelo selecionado e do índice, não ser hardcoded no contrato central.
4. No ambiente atual, `nomic-embed-text` com dimensão 768 pode ser provider inicial, mas não regra universal.
5. Migração de storage local para PostgreSQL deve preservar IDs, hashes, proveniência e rastreabilidade.
6. Banco vetorial alternativo deve poder substituir pgvector quando contrato funcional for preservado.
7. Operações de escrita em banco devem passar por permissões e Guardian Engine quando sensíveis.

## Relação com Guardian Specs

### Security by Design

Knowledge Hub deve proteger segredos, controlar acesso por domínio, tratar documentos como dados não confiáveis, mitigar prompt injection, validar paths e bloquear envio de dados sensíveis a providers externos sem política explícita.

### Token Efficiency

Knowledge Hub deve usar Markdown canônico, chunking, busca por domínio, ranking, deduplicação, cache e Context Packages compactos para evitar envio redundante ou excessivo de contexto.

### AI Quality Assurance

Resultados devem ser citáveis, ranqueados, explicáveis e acompanhados de domínio, confiança, status, hash e warnings quando aplicável.

### Cost Optimization

Embeddings, reranking, conversões e buscas devem usar cache, modelos adequados e providers locais ou baratos quando cumprirem qualidade e política.

### Architecture Governance

Knowledge Hub deve preservar fronteiras entre Agents, Capabilities, Skills, Tools, Provider Gateway, Canonicalizer, Model Selection Engine e Guardian Engine.

### Documentation Governance

Canonical Documents devem ser versionáveis, legíveis por humanos, rastreáveis e documentados por metadados consistentes.

### Testing Governance

Implementações futuras devem ser testáveis por contrato, incluindo ingestão, redaction, ranking, deduplicação, cache, bloqueios, prompt injection e reconstrução de índices.

### Compliance Governance

Legislação, livros, conversas, dados sensíveis e fontes externas devem respeitar licença, retenção, privacidade, jurisdição, auditoria e política de uso.

### Observability Governance

Knowledge Hub deve emitir eventos estruturados suficientes para auditoria, diagnóstico, replay, investigação e análise de impacto.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Documento malicioso alterar comportamento do agente | Encapsular documentos como dados, detectar prompt injection e impedir que contexto recuperado altere políticas. |
| Vazamento de segredo por embeddings | Redaction antes de indexação, bloqueio de segredo não redigido e proibição de provider externo sem política. |
| Acoplamento a PostgreSQL ou pgvector | Definir storage e busca como providers substituíveis via Provider Gateway. |
| Índice semântico virar fonte da verdade | Declarar Semantic Index como derivado e reconstruível a partir de Canonical Documents. |
| RAG trazer contexto irrelevante | Busca por domínio, filtros, ranking, reranking e token budget. |
| Conversão de PDF/OCR gerar erro factual | Registrar confiança, proveniência e exigir validação em tarefas críticas. |
| Cache entregar contexto obsoleto | Invalidar por hash, política, provider, modelo, permissão e versão de índice. |
| Duplicação aumentar custo e ruído | Deduplicação por hash, URI, versão e similaridade semântica. |
| Fonte não confiável superar Spec aprovada | Ranking por autoridade e prevalência de Specs/ADRs aprovadas. |
| Provider externo receber dado sensível | Guardian Engine, política de privacidade, local preferred/required e redaction obrigatória. |
| Perda de rastreabilidade | IDs estáveis, hashes, citações, logs e relações entre fonte, documento, chunk, índice e query. |

## Decisões aprovadas por esta Spec

1. Knowledge Hub é a base de conhecimento governada do Vercosa AI Framework.
2. Knowledge Hub possui duas camadas principais: Canonical Documents e Semantic Indexes.
3. Markdown canônico é obrigatório antes de uso por agente ou indexação.
4. Semantic Indexes são derivados e reconstruíveis, não fonte da verdade.
5. RAG deve ser organizado por domínio.
6. Fontes previstas incluem Specs, ADRs, docs, código, legislação, livros, conversas, decisões, projetos, agentes, skills, comandos e hooks.
7. Ingestão inicial deve focar Markdown.
8. PDF, DOCX, HTML, EPUB, PPTX, XLSX, imagens/OCR, áudio e vídeo devem ser convertidos futuramente para Markdown canônico antes de uso.
9. Frontmatter YAML pode declarar metadados e políticas locais, sem sobrescrever Guardian Specs.
10. Canonicalizer é responsável pela canonicalização; Knowledge Hub valida e indexa o resultado.
11. Provider Gateway isola Knowledge Hub de storage, embeddings, busca, OCR, transcrição, conversão e providers concretos.
12. Model Selection Engine seleciona modelos para embeddings, reranking, sumarização, classificação e tarefas similares quando necessário.
13. Guardian Engine governa ingestão, indexação, recuperação, redaction, provedores externos e contexto sensível.
14. Text-only é regra central de eficiência de tokens.
15. Busca deve suportar domínio, ranking, deduplicação e cache.
16. Documentos recuperados devem ser tratados como dados não confiáveis para mitigar prompt injection.
17. Segredos devem ser redigidos antes de indexação, cache, logs e entrega ao agente.
18. Toda recuperação relevante deve ser rastreável por fontes, documentos, chunks, índices, hashes e citações.
19. Knowledge Hub deve permanecer provider agnostic.
20. Storage local inicial é permitido e deve ser simples, auditável e substituível.
21. PostgreSQL com pgvector é integração futura prevista, não dependência obrigatória.
22. Esta Spec não autoriza implementação de código, alteração de configurações globais ou uso de `sudo`.

## Critérios de aceite

- Existe uma Spec própria em `specs/framework/0011-knowledge-hub.md`.
- A Spec define Knowledge Hub como base de conhecimento do framework.
- A Spec define Canonical Documents.
- A Spec define Semantic Indexes.
- A Spec cobre RAG por domínio.
- A Spec cobre fontes: specs, ADRs, docs, código, legislação, livros, conversas, decisões, agentes, skills, comandos e hooks.
- A Spec cobre ingestão de Markdown.
- A Spec cobre conversão futura de PDF, DOCX, HTML, EPUB, PPTX, XLSX, imagens/OCR, áudio e vídeo para Markdown.
- A Spec cobre frontmatter YAML.
- A Spec define relação com Canonicalizer.
- A Spec define relação com Provider Gateway.
- A Spec define relação com Model Selection Engine.
- A Spec define relação com Guardian Engine.
- A Spec define text-only como regra de eficiência de tokens.
- A Spec cobre busca por domínio.
- A Spec cobre ranking.
- A Spec cobre deduplicação.
- A Spec cobre cache.
- A Spec cobre segurança contra prompt injection em documentos.
- A Spec cobre redaction de segredos.
- A Spec cobre rastreabilidade.
- A Spec preserva provider agnostic.
- A Spec define storage local inicial.
- A Spec prevê futura integração com PostgreSQL e pgvector.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir Spec própria do Canonicalizer.
- Definir schema persistente final de Canonical Documents.
- Definir schema persistente final de chunks e Semantic Indexes.
- Definir contrato formal de `KnowledgeQuery` e `KnowledgeResult`.
- Definir catálogo inicial de domains e permissões associadas.
- Definir estratégia padrão de chunking por domínio.
- Definir estratégia padrão de ranking e reranking.
- Definir política numérica de cache, TTL e invalidação.
- Definir adapters iniciais de storage local.
- Definir integração concreta futura com PostgreSQL e pgvector.
- Definir política de licenças e compliance para livros, legislação e fontes externas.
- Definir testes de contrato para prompt injection, redaction, deduplicação e rastreabilidade.

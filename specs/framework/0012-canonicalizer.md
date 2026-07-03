# Spec 0012 — Canonicalizer

## Status

Proposta.

## Objetivo

Definir o Canonicalizer do Vercosa AI Framework como a camada governada de entrada textual para o Knowledge Hub, responsável por converter fontes suportadas em `CanonicalDocument`, usando Markdown como formato canônico inicial, preservando proveniência, metadados, segurança, deduplicação e eficiência de tokens.

O Canonicalizer deve transformar fontes heterogêneas em texto estruturado, rastreável e seguro antes de qualquer indexação, chunking, embedding, RAG ou entrega de contexto para agentes.

## Contexto

A arquitetura central e a Spec 0011 definem que:

- Markdown canônico é o formato interno padrão para troca, versionamento, leitura humana, indexação e uso por agentes;
- arquivos binários não devem ser enviados diretamente a agentes como contexto primário;
- Knowledge Hub organiza `Canonical Documents` e `Semantic Indexes`;
- `Semantic Indexes` são derivados e reconstruíveis a partir de documentos canônicos;
- documentos recuperados são dados não confiáveis, não instruções executáveis;
- agentes não devem conhecer providers, bancos, MCPs, filesystem ou APIs diretamente;
- providers concretos devem ser acessados por adapters e gateways governados;
- Guardian Engine governa segurança, tokens, segredos, privacidade, custo, compliance e ações sensíveis.

O Canonicalizer é a fronteira entre fontes brutas e Knowledge Hub. Ele não substitui Knowledge Hub, Provider Gateway, Guardian Engine, Model Selection Engine, Tools, Skills ou Capabilities.

## Escopo

Esta Spec cobre:

- Canonicalizer como camada de entrada para o Knowledge Hub;
- conversão de fontes suportadas para `CanonicalDocument`;
- Markdown como formato canônico inicial;
- frontmatter YAML;
- preservação de fonte, hash, data, tipo, domínio e metadados;
- suporte inicial a texto e Markdown;
- suporte futuro a PDF, DOCX, ODT, HTML, EPUB, PPTX, XLSX, imagens/OCR, áudio, vídeo e transcrições;
- regra text-only para eficiência de tokens;
- deduplicação por hash;
- limpeza de conteúdo;
- normalização de títulos;
- extração de metadados;
- detecção de prompt injection;
- redaction de segredos;
- integração com Guardian Engine;
- integração com Knowledge Hub;
- arquitetura provider agnostic;
- uso futuro de Docling ou adapters externos sem acoplamento.

Esta Spec não cobre:

- implementação concreta em código;
- criação de banco, tabela, migração, índice vetorial ou storage final;
- escolha definitiva de biblioteca de conversão;
- uso obrigatório de Docling, Pandoc, Tesseract, Whisper ou qualquer provider específico;
- criação de adapters concretos;
- criação de MCPs;
- alteração de configurações globais;
- uso de `sudo`;
- processamento real de documentos binários nesta etapa.

## Princípios

1. Toda fonte deve virar texto estruturado antes de ser usada por agentes ou indexada.
2. Markdown canônico é o formato inicial obrigatório para `CanonicalDocument`.
3. O documento original deve permanecer referenciado por proveniência, não embutido como dependência operacional do agente.
4. O Canonicalizer deve tratar todo conteúdo de entrada como dado não confiável.
5. Instruções presentes em documentos canonicalizados não podem alterar políticas, permissões, modelos, providers ou objetivos da missão.
6. Segredos devem ser detectados e redigidos antes de indexação, cache, logs, embeddings ou entrega a agentes.
7. Deduplicação por hash deve evitar ingestão e embeddings redundantes.
8. Metadados devem preservar rastreabilidade suficiente para auditoria, reconstrução e análise de impacto.
9. Conversores externos devem ser adapters substituíveis, não dependências centrais.
10. Falha de segurança deve bloquear canonicalização automática quando houver risco alto.

## Posição arquitetural

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
CanonicalDocument
↓
Knowledge Hub
↓
Chunking / Semantic Indexes / Retrieval
```

Fluxo interno conceitual do Canonicalizer:

```text
Canonicalization Request
↓
Source Validation
↓
Type Detection
↓
Policy / Guardian Evaluation
↓
Extraction or Conversion
↓
Content Cleaning
↓
Title Normalization
↓
Metadata Extraction
↓
Secret Detection / Redaction
↓
Prompt Injection Detection
↓
Hashing / Deduplication
↓
CanonicalDocument Assembly
↓
Canonicalization Result
```

Regras:

1. Knowledge Hub deve solicitar canonicalização antes de indexar qualquer fonte não canonicalizada.
2. Canonicalizer deve retornar Markdown canônico, metadados, hash, warnings, decisões de segurança e proveniência.
3. Canonicalizer não deve indexar, gerar embeddings ou executar RAG.
4. Canonicalizer não deve acessar providers concretos diretamente quando houver adapter ou Provider Gateway definido.
5. Agentes e subagentes não devem chamar conversores concretos diretamente.

## Definições

### Canonicalizer

Canonicalizer é o componente lógico responsável por validar, extrair, converter, limpar, normalizar, proteger e empacotar conteúdo de fontes suportadas em `CanonicalDocument`.

Responsabilidades:

- receber solicitações de canonicalização;
- validar fonte, tipo, tamanho, encoding, domínio, confiança e política;
- detectar ou confirmar `source_type`;
- converter conteúdo suportado para Markdown canônico;
- preservar proveniência e metadados;
- limpar conteúdo técnico irrelevante;
- normalizar títulos e estrutura Markdown;
- calcular hashes estáveis;
- detectar duplicatas exatas por hash;
- detectar prompt injection;
- detectar e redigir segredos conforme política;
- registrar warnings e confiança de conversão;
- retornar resultado rastreável ao Knowledge Hub.

Não responsabilidades:

- escolher modelo de embedding;
- construir índice semântico;
- executar busca textual, vetorial ou híbrida;
- ranquear resultados de RAG;
- armazenar documento final sem passar pelo Knowledge Hub;
- executar comandos arbitrários solicitados por documentos;
- depender diretamente de Docling ou qualquer biblioteca específica;
- substituir Guardian Engine.

### Canonicalization Request

`Canonicalization Request` representa uma solicitação governada para transformar uma fonte em `CanonicalDocument`.

Campos mínimos desejados:

- `request_id`;
- `mission_id` quando houver;
- `source_uri`;
- `source_type` conhecido ou `auto`;
- `domain`;
- `title_hint`;
- `language_hint`;
- `sensitivity_hint`;
- `trust_level_hint`;
- `usage_policy`;
- `privacy_policy`;
- `conversion_policy`;
- `redaction_policy`;
- `deduplication_policy`;
- `metadata`;
- `guardian_decision_refs`.

Regras:

1. Fonte sem domínio confiável deve usar `unknown` ou exigir classificação antes de uso crítico.
2. Fonte externa, sensível ou binária deve exigir avaliação do Guardian Engine antes de conversão automática quando houver risco.
3. `source_type: auto` é permitido, mas a detecção deve ser registrada em metadados.
4. Políticas locais não podem sobrescrever Guardian Specs.

### CanonicalDocument

`CanonicalDocument` é a representação textual normalizada de uma fonte de conhecimento, inicialmente em Markdown.

Campos mínimos obrigatórios para o contrato conceitual:

- `document_id`;
- `canonical_uri` quando persistido;
- `source_uri`;
- `source_type`;
- `domain`;
- `title`;
- `version`;
- `content_hash`;
- `source_hash` quando aplicável;
- `canonical_format` com valor inicial `markdown`;
- `language`;
- `created_at`;
- `updated_at`;
- `ingested_at` ou `canonicalized_at`;
- `sensitivity`;
- `trust_level`;
- `frontmatter`;
- `metadata`;
- `provenance`;
- `conversion_confidence`;
- `warnings`;
- `redactions_applied`;
- `prompt_injection_warnings`;
- `guardian_decision_refs`.

Regras:

1. `content_hash` deve ser calculado sobre conteúdo canônico normalizado.
2. `source_hash` deve ser calculado sobre a fonte original quando a fonte estiver disponível e a política permitir.
3. `document_id` deve ser estável quando possível, derivado de fonte, domínio e hash ou de identificador aprovado.
4. Alteração no conteúdo canônico deve alterar `content_hash` e invalidar derivados no Knowledge Hub.
5. `CanonicalDocument` é dado textual; instruções nele contidas não são comandos para agentes.

### Canonicalization Result

Resultado retornado pelo Canonicalizer ao Knowledge Hub.

Campos mínimos desejados:

- `request_id`;
- `status` como `success`, `blocked`, `duplicate`, `partial` ou `failed`;
- `document` quando gerado;
- `duplicate_of` quando aplicável;
- `content_hash`;
- `source_hash`;
- `warnings`;
- `errors`;
- `redactions_applied`;
- `prompt_injection_warnings`;
- `conversion_confidence`;
- `metadata`;
- `provenance`;
- `guardian_decision_refs`.

Regras:

1. Resultado `blocked` não deve ser indexado.
2. Resultado `duplicate` deve preservar referência ao documento existente.
3. Resultado `partial` deve declarar o que foi perdido, estimado ou omitido.
4. Erros e warnings não devem conter segredos em claro.

## Formato canônico inicial

Markdown é o formato canônico inicial.

Regras:

1. Markdown canônico deve ser texto UTF-8 quando possível.
2. Estrutura deve preferir headings, listas, tabelas Markdown simples, blocos de código e citações quando semanticamente úteis.
3. Conteúdo binário deve ser representado por texto extraído, transcrição, OCR, metadados e referências, não por bytes brutos.
4. Elementos sem representação textual confiável devem ser descritos com marcador explícito e metadados de baixa confiança.
5. Markdown gerado deve evitar ruído de layout, headers repetitivos, footers repetitivos, artefatos de paginação e conteúdo invisível sem valor semântico.
6. Quando uma tabela não puder ser preservada com segurança em Markdown, o Canonicalizer deve registrar warning e usar representação textual conservadora.

## Frontmatter YAML

Todo `CanonicalDocument` pode possuir frontmatter YAML com metadados e políticas locais.

Exemplo conceitual:

```yaml
---
document_id: spec-framework-0012
domain: specs
source_type: markdown
title: Canonicalizer
version: 1
canonical_format: markdown
language: pt-BR
sensitivity: internal
trust_level: authoritative
source_uri: specs/framework/0012-canonicalizer.md
content_hash: auto
source_hash: auto
canonicalized_at: auto
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
- `canonical_format`;
- `language`;
- `sensitivity`;
- `trust_level`;
- `source_uri`;
- `content_hash`;
- `source_hash` quando aplicável;
- `canonicalized_at`;
- `security`;
- `privacy`;
- `rag_allowed`;
- `indexing_allowed`;
- `redaction_required`.

Regras:

1. Frontmatter YAML deve ser validado antes de uso.
2. Frontmatter inválido deve gerar warning ou bloqueio conforme domínio e risco.
3. Frontmatter não deve conter segredos.
4. Políticas do frontmatter podem restringir uso, mas não podem ampliar permissões além das Guardian Specs.
5. Campos calculados como hashes e datas podem ser preenchidos pelo processo de canonicalização ou storage, conforme contrato futuro.

## Fontes suportadas

### Suporte inicial

O suporte inicial deve cobrir:

- texto puro;
- Markdown.

Regras para texto puro:

1. Texto puro deve ser convertido para Markdown com estrutura mínima.
2. Se não houver título confiável, o título deve ser extraído da primeira linha útil ou marcado como desconhecido.
3. Encoding deve ser validado e normalizado para texto seguro.

Regras para Markdown:

1. Markdown existente deve ser validado, limpo e normalizado, não aceito cegamente.
2. Frontmatter existente deve ser extraído, validado e combinado com metadados da solicitação.
3. Headings devem ser normalizados quando houver quebras óbvias ou título duplicado.
4. Prompt injection e segredos devem ser verificados mesmo em arquivos do repositório.

### Suporte futuro

Formatos futuros previstos:

- PDF;
- DOCX;
- ODT;
- HTML;
- EPUB;
- PPTX;
- XLSX;
- imagens com OCR;
- áudio com transcrição;
- vídeo com transcrição;
- transcrições externas.

Regras para formatos futuros:

1. Nenhum formato binário deve ser entregue diretamente a agentes como contexto primário.
2. Conversão deve produzir Markdown canônico e metadados de proveniência.
3. PDF deve preservar página, seção, título, notas, tabelas e confiança de extração quando possível.
4. DOCX e ODT devem preservar títulos, estilos relevantes, listas, tabelas, notas e comentários permitidos.
5. HTML deve remover scripts, estilos, navegação e boilerplate quando não forem semanticamente relevantes.
6. EPUB deve preservar capítulo, seção, autoria, edição e ordem de leitura.
7. PPTX deve preservar slide, notas do apresentador, título e ordem visual aproximada.
8. XLSX deve converter planilhas em tabelas ou descrições textuais com nome da aba, intervalo e limites de tamanho.
9. OCR deve registrar idioma, ferramenta ou provider, confiança, páginas ou regiões e limitações.
10. Áudio e vídeo devem preservar timestamps, idioma, speaker labels quando disponíveis e confiança de transcrição.
11. Transcrições externas devem preservar origem, ferramenta, data, idioma e relação com mídia original.

## Limpeza de conteúdo

Limpeza de conteúdo deve reduzir ruído sem apagar evidência relevante.

Operações permitidas:

- normalizar quebras de linha;
- remover bytes nulos e caracteres de controle inseguros;
- normalizar espaços repetidos quando não afetar blocos de código;
- remover headers e footers repetitivos quando detectados com confiança;
- remover navegação, menus, anúncios e boilerplate em HTML convertido;
- preservar blocos de código, tabelas e citações quando relevantes;
- marcar conteúdo omitido quando a remoção puder afetar interpretação.

Regras:

1. Limpeza não deve alterar significado intencional.
2. Limpeza agressiva deve registrar warning.
3. Conteúdo removido por segurança deve ser registrado como redaction, não como limpeza comum.
4. Conteúdo sensível não deve aparecer em logs de limpeza.

## Normalização de títulos

O Canonicalizer deve determinar um título auditável para cada `CanonicalDocument`.

Ordem de preferência:

1. Título explícito aprovado no request.
2. `title` do frontmatter.
3. Título extraído de metadados da fonte.
4. Primeiro heading H1 confiável.
5. Primeira linha textual útil.
6. Nome de arquivo ou identificador de origem permitido.
7. `Untitled` ou equivalente localizado quando nada for confiável.

Regras:

1. Título deve ser texto simples, sem Markdown complexo.
2. Título deve remover excesso de espaço, quebras de linha e caracteres de controle.
3. Título extraído automaticamente deve registrar origem no metadado.
4. Título não deve conter segredo; se contiver, deve ser redigido.

## Extração de metadados

Metadados devem ser extraídos da fonte, do frontmatter, da solicitação e do processo de conversão.

Metadados mínimos:

- origem;
- tipo de fonte;
- domínio;
- título;
- idioma;
- data de criação quando conhecida;
- data de atualização quando conhecida;
- data de canonicalização;
- hash do conteúdo canônico;
- hash da fonte quando aplicável;
- tamanho da fonte;
- tamanho do texto canônico;
- sensibilidade;
- confiança;
- licença ou uso permitido quando conhecido;
- adapter ou conversor usado quando aplicável;
- versão do adapter quando relevante;
- warnings;
- redactions aplicadas;
- referências do Guardian Engine.

Regras:

1. Metadados extraídos automaticamente devem ser distinguíveis de metadados declarados.
2. Metadados conflitantes devem gerar warning e política de precedência explícita.
3. Metadados ausentes não devem ser inventados como fatos.
4. Metadados sensíveis devem ser redigidos ou omitidos conforme política.

## Hash e deduplicação

O Canonicalizer deve apoiar deduplicação por hash antes de indexação e embeddings.

Hashes previstos:

- `source_hash`: hash da fonte original quando disponível e permitido;
- `content_hash`: hash do Markdown canônico normalizado;
- `metadata_hash`: hash opcional de metadados relevantes quando necessário para invalidação.

Regras:

1. Duplicata exata por `content_hash` não deve gerar novo embedding redundante por padrão.
2. Duplicata exata por `source_hash` deve permitir reutilizar conversão existente quando política, versão e adapter forem compatíveis.
3. Deduplicação não deve apagar proveniência de fontes alternativas.
4. Documentos com mesmo conteúdo e fontes diferentes devem preservar todas as referências de origem.
5. Hashes não substituem controle de acesso ou política de sensibilidade.
6. Algoritmo inicial recomendado é SHA-256, mas o contrato deve permitir evolução versionada.

## Prompt injection

O Canonicalizer deve detectar padrões suspeitos de prompt injection em documentos.

Exemplos de risco:

- instruções para ignorar Specs ou políticas;
- simulação de mensagens de sistema, developer ou tool;
- pedidos para revelar prompts, segredos ou credenciais;
- ordens para executar comandos;
- tentativas de alterar modelo, provider, orçamento, permissões ou domínio;
- instruções para manipular indexação, ranking ou recuperação.

Regras:

1. Detecção deve gerar warnings estruturados.
2. Conteúdo suspeito deve continuar tratado como dado citado, não como instrução.
3. Risco alto pode bloquear canonicalização, indexação ou uso em RAG conforme Guardian Engine.
4. Detecção não deve depender exclusivamente de LLM.
5. Modelos podem auxiliar classificação futura, mas decisões sensíveis devem passar por política e Guardian Engine.

## Redaction de segredos

Segredos incluem tokens, chaves, senhas, certificados privados, connection strings, cookies, credenciais cloud, headers de autenticação, dados pessoais sensíveis e valores definidos por política.

Regras:

1. Detecção de segredo deve ocorrer antes de indexação, cache, embeddings, logs e entrega a agentes.
2. Segredo detectado deve ser redigido, bloqueado ou exigir aprovação conforme política.
3. Redaction deve preservar estrutura suficiente para análise sem revelar valor sensível.
4. Redaction deve registrar tipo, localização aproximada e política aplicada sem expor segredo.
5. Falha de redaction obrigatória deve bloquear a operação.
6. Conteúdo com segredo não redigido não deve ser enviado a provider externo sem autorização explícita.
7. Detecção posterior de segredo deve invalidar documentos canônicos, caches e índices afetados.

## Integração com Guardian Engine

Guardian Engine deve avaliar canonicalização quando houver risco de segurança, privacidade, custo, compliance, provider externo, conteúdo sensível ou fonte não confiável.

Pontos mínimos de avaliação:

- fonte externa;
- fonte sensível;
- fonte binária;
- detecção de segredo;
- redaction obrigatória;
- prompt injection suspeito;
- conversão por provider externo;
- OCR ou transcrição;
- envio de conteúdo para modelo ou serviço externo;
- documento com baixa confiança;
- deduplicação ou substituição de documento existente;
- alteração de domínio ou sensibilidade.

Contexto mínimo enviado ao Guardian Engine:

- `mission_id` quando houver;
- `evaluation_type` como `canonicalization`;
- `source_uri`;
- `source_type`;
- `domain`;
- `operation`;
- `data_sensitivity`;
- `trust_level`;
- `conversion_provider_policy`;
- `network_policy`;
- `privacy_policy`;
- `redaction_policy`;
- `detected_secret_types`;
- `prompt_injection_warnings`;
- `prior_decision_refs`.

Regras:

1. Decisão `block` deve impedir canonicalização automática ou entrega ao Knowledge Hub.
2. Decisão `require_approval` deve bloquear execução automática até aprovação.
3. Falha do Guardian Engine deve bloquear operações automáticas de alto risco.
4. Decisões devem ser registradas em `guardian_decision_refs`.
5. Guardian Engine pode reduzir permissões, exigir local-only, exigir redaction ou proibir provider externo.

## Integração com Knowledge Hub

Knowledge Hub deve consumir o resultado do Canonicalizer e decidir armazenamento, atualização, chunking, indexação e cache.

Regras:

1. Knowledge Hub deve validar `Canonicalization Result` antes de armazenar ou indexar.
2. Knowledge Hub deve rejeitar resultado bloqueado, sem conteúdo canônico ou sem metadados mínimos.
3. Knowledge Hub deve usar `content_hash` para deduplicação e invalidação de derivados.
4. Knowledge Hub deve preservar `source_uri`, `source_type`, domínio, datas, hashes, redactions, warnings e decisões Guardian.
5. Knowledge Hub não deve embutir lógica final de conversão de formatos.
6. Knowledge Hub pode solicitar recanonicalização quando política, adapter, fonte ou documento mudar.

## Provider agnostic e adapters externos

Canonicalizer deve ser provider agnostic.

Regras:

1. Conversores devem ser adapters substituíveis.
2. Docling pode ser usado futuramente como adapter externo, mas não deve ser dependência arquitetural obrigatória.
3. Pandoc, Tesseract, Whisper, serviços cloud, bibliotecas locais ou MCPs podem ser providers futuros quando aprovados por Spec/ADR e política.
4. O contrato central deve falar em capacidade, como `convert_to_markdown`, `extract_text`, `ocr_image` ou `transcribe_audio`, não em ferramenta concreta.
5. Provider externo não deve receber conteúdo sensível sem avaliação e autorização explícita.
6. Fallback entre adapters não pode alterar privacidade, custo, rede ou retenção sem nova avaliação.
7. Resultado de adapter externo deve ser tratado como dado não confiável até validação.

## Text-only e eficiência de tokens

O Canonicalizer deve aplicar text-only como regra central de eficiência de tokens.

Regras:

1. Conteúdo binário não deve ser usado como contexto bruto de agente.
2. Conversão deve extrair texto útil e metadados, não preservar ruído visual sem utilidade.
3. Markdown canônico deve ser menor e mais estruturado que a fonte bruta quando possível.
4. Conteúdo repetitivo deve ser reduzido antes de chunking e embeddings.
5. Partes omitidas devem ser marcadas quando a omissão puder afetar compreensão.
6. Extração completa deve ser evitada quando a política ou missão permitir extração seletiva com rastreabilidade.
7. Canonicalização não deve gerar sumarizações destrutivas como substituto do documento canônico sem política explícita.

## Rastreabilidade e observabilidade

Eventos mínimos:

- canonicalização solicitada;
- fonte validada;
- tipo detectado;
- Guardian Engine consultado;
- conversão iniciada;
- conversão concluída;
- limpeza aplicada;
- título normalizado;
- metadados extraídos;
- segredo detectado;
- redaction aplicada;
- prompt injection suspeito;
- hash calculado;
- duplicata detectada;
- documento canônico gerado;
- operação bloqueada;
- falha registrada.

Regras:

1. Logs devem preferir IDs, hashes, tipos e referências em vez de payload completo.
2. Logs não devem conter segredos em claro.
3. Todo `CanonicalDocument` deve ser rastreável até a fonte quando política permitir.
4. Toda conversão futura deve registrar adapter, versão, confiança e limitações relevantes.
5. Rastreabilidade não pode depender da memória do agente.

## Relação com Guardian Specs

### Security by Design

Canonicalizer deve validar fontes, detectar prompt injection, redigir segredos, tratar conteúdo como não confiável e bloquear envio indevido a providers externos.

### Token Efficiency

Canonicalizer deve produzir Markdown limpo, estruturado, deduplicável e adequado para chunking, evitando contexto binário ou redundante.

### AI Quality Assurance

Canonicalizer deve preservar metadados, proveniência, confiança de conversão, warnings e limitações para que agentes possam avaliar qualidade do contexto.

### Cost Optimization

Canonicalizer deve deduplicar por hash, reutilizar conversões compatíveis e evitar conversões externas ou caras quando texto local confiável estiver disponível.

### Architecture Governance

Canonicalizer deve respeitar fronteiras entre Knowledge Hub, Guardian Engine, Provider Gateway, adapters, Skills, Tools e Agents.

### Documentation Governance

CanonicalDocument deve ser legível, versionável, auditável e acompanhado de frontmatter e metadados consistentes.

### Testing Governance

Implementações futuras devem possuir testes de contrato para texto, Markdown, hash, deduplicação, frontmatter, prompt injection, redaction, metadados, bloqueios e falhas.

### Compliance Governance

Canonicalizer deve preservar licença, origem, jurisdição, autoria, datas, permissões de uso e retenção quando aplicável.

### Observability Governance

Canonicalizer deve emitir eventos estruturados suficientes para auditoria, replay, diagnóstico e análise de impacto sem vazar conteúdo sensível.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Documento malicioso tentar controlar agente | Tratar conteúdo como dado, detectar prompt injection e registrar warnings governados. |
| Vazamento de segredo em índice ou embedding | Detectar e redigir antes de Knowledge Hub, cache, logs e providers externos. |
| Acoplamento a Docling ou ferramenta específica | Definir conversores como adapters provider agnostic. |
| Conversão binária perder informação importante | Registrar proveniência, confiança, warnings e permitir validação humana. |
| Deduplicação apagar evidência de origem | Deduplicar conteúdo sem remover proveniência alternativa. |
| Limpeza alterar significado | Usar limpeza conservadora, warnings e marcação de omissões. |
| Hash instável por normalização inconsistente | Definir normalização canônica versionada antes do hash. |
| Provider externo receber dado sensível | Guardian Engine, política local-only, redaction e autorização explícita. |
| Frontmatter malicioso ampliar permissões | Validar frontmatter e impedir sobrescrita de Guardian Specs. |
| Logs vazarem conteúdo sensível | Registrar IDs, hashes e metadados seguros em vez de payload completo. |

## Decisões aprovadas por esta Spec

1. Canonicalizer é a camada governada de entrada para o Knowledge Hub.
2. Toda fonte suportada deve ser convertida para `CanonicalDocument` antes de indexação ou uso por agente.
3. Markdown é o formato canônico inicial.
4. Frontmatter YAML é o mecanismo inicial para metadados e políticas locais.
5. `CanonicalDocument` deve preservar fonte, hash, data, tipo, domínio, metadados, proveniência, redactions e decisões Guardian.
6. Suporte inicial deve cobrir texto puro e Markdown.
7. Suporte futuro deve cobrir PDF, DOCX, ODT, HTML, EPUB, PPTX, XLSX, imagens/OCR, áudio, vídeo e transcrições.
8. Text-only é regra obrigatória de eficiência de tokens.
9. Deduplicação inicial deve usar hash de conteúdo canônico e, quando possível, hash da fonte.
10. Canonicalizer deve limpar conteúdo, normalizar títulos e extrair metadados.
11. Canonicalizer deve detectar prompt injection e tratar documentos como dados não confiáveis.
12. Canonicalizer deve detectar e redigir segredos antes de indexação, cache, logs, embeddings ou entrega a agentes.
13. Operações sensíveis devem integrar Guardian Engine.
14. Knowledge Hub deve consumir e validar resultados do Canonicalizer, não embutir conversão final de formatos.
15. Canonicalizer deve permanecer provider agnostic.
16. Docling e outros conversores podem ser usados futuramente como adapters externos sem acoplamento arquitetural.
17. Esta Spec não autoriza implementação de código, alteração de configurações globais ou uso de `sudo`.

## Critérios de aceite

- Existe uma Spec própria em `specs/framework/0012-canonicalizer.md`.
- A Spec define Canonicalizer como camada de entrada para Knowledge Hub.
- A Spec define conversão de fonte suportada para `CanonicalDocument`.
- A Spec define Markdown como formato canônico inicial.
- A Spec cobre frontmatter YAML.
- A Spec cobre preservação de fonte, hash, data, tipo, domínio e metadados.
- A Spec cobre suporte inicial a texto e Markdown.
- A Spec prevê suporte futuro a PDF, DOCX, ODT, HTML, EPUB, PPTX, XLSX, imagens/OCR, áudio, vídeo e transcrições.
- A Spec define text-only como regra de eficiência de tokens.
- A Spec cobre deduplicação por hash.
- A Spec cobre limpeza de conteúdo.
- A Spec cobre normalização de títulos.
- A Spec cobre extração de metadados.
- A Spec cobre detecção de prompt injection.
- A Spec cobre redaction de segredos.
- A Spec define integração com Guardian Engine.
- A Spec define integração com Knowledge Hub.
- A Spec preserva provider agnostic.
- A Spec permite uso futuro de Docling ou adapters externos sem acoplamento.
- A Spec respeita Guardian Specs.
- A Spec não implementa código.
- A Spec não altera configurações globais.
- A Spec não exige nem usa `sudo`.

## Pendências

- Definir contrato formal versionado de `Canonicalization Request` e `Canonicalization Result`.
- Definir normalização canônica exata antes do cálculo de `content_hash`.
- Definir catálogo inicial de warnings e códigos de erro.
- Definir política de redaction por tipo de segredo.
- Definir política de classificação automática de domínio.
- Definir adapters iniciais para texto e Markdown.
- Definir Specs ou ADRs para adapters futuros de PDF, DOCX, ODT, HTML, EPUB, PPTX, XLSX, OCR, áudio e vídeo.
- Definir testes de contrato para canonicalização, deduplicação, redaction, prompt injection e Guardian Engine.

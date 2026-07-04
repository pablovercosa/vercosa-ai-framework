# ADR: Context Router, Token Budget Manager e arquitetura de memoria

## Status da decisao

Aceita em 2026-07-04.

Esta ADR define a arquitetura conceitual de contexto, memoria e eficiencia de tokens do Vercosa AI Framework antes de qualquer implementacao funcional de Context Router, Token Budget Manager, Semantic Index, embeddings, pgvector ou RAG.

## Contexto

O Vercosa AI Framework ja possui Specs e MVPs parciais para Knowledge Hub, Canonicalizer, Persistence Layer, Guardian Engine, Model Selection Engine e Agent Orchestrator.

O estado atual registrado em `docs/alignment/current-state.md`, `docs/alignment/architecture-map.md` e `docs/alignment/alignment-review-2026-07-03.md` declara lacunas importantes:

- nao existe Context Router como modulo ou contrato formal;
- nao existe Token Budget Manager como contrato formal;
- Knowledge Hub atual executa ingestao Markdown e busca textual deterministica em memoria, mas nao implementa Semantic Index, embeddings, pgvector, PostgreSQL ou RAG governado;
- Canonicalizer atual canonicaliza texto e Markdown, mas nao processa binarios nem integra completamente politicas;
- Persistence Layer atual possui porta generica e adapter filesystem inicial, mas nao define schemas finais de memoria, contexto ou indices;
- Model Selection considera `context_size`, mas nao recebe ainda Context Packages formais;
- Guardian Engine avalia riscos e limites, mas nao deve montar contexto nem gerenciar orcamento detalhado;
- a ADR `2026-07-04-policy-engine-vs-guardian-engine.md` separa Policy Engine como resolucao declarativa de politicas e Guardian Engine como enforcement operacional.

A arquitetura precisa definir memoria e contexto antes de expandir busca semantica, embeddings, pgvector, RAG ou claims de memoria longa.

## Problema

Sem uma fronteira clara, ha risco de transformar busca semantica em despejo de texto em prompts, confundir memoria persistente com Knowledge Hub, tratar pgvector como dependencia central, duplicar politicas em varios componentes e prometer memoria infinita sem limites reais de custo, privacidade, relevancia, retencao e janela de contexto.

O framework precisa decidir:

- o que seleciona contexto;
- o que estima e limita tokens;
- o que armazena conhecimento;
- o que canonicaliza fontes;
- o que persiste artefatos e decisoes;
- o que avalia risco operacional;
- o que escolhe modelo compativel com o contexto final;
- como tudo isso preserva rastreabilidade e independencia de storage, provider, runtime e banco vetorial.

## Decisao

O Vercosa AI Framework adotara tres conceitos arquiteturais distintos:

1. Context Router como componente que seleciona, compoe, reduz, ordena e justifica o contexto entregue a agentes, modelos, skills, validacoes ou runtimes.
2. Token Budget Manager como componente que estima, reserva, aloca, limita, reduz e reporta orcamento de tokens por missao, workflow, task, agent assignment, Context Package, modelo e ciclo.
3. Memory Architecture como arquitetura em camadas, composta por memoria persistente, Knowledge Hub, documentos canonicos, indices derivados, caches, pacotes de contexto e registros auditaveis.

O framework nao deve prometer memoria infinita. Deve oferecer memoria persistente, recuperacao governada, contexto seletivo, sumarizacao rastreavel, caches controlados e indices derivados reconstruiveis.

Semantic Index, embeddings e pgvector permanecem futuros adapters ou indices derivados. Eles nao sao requisito para o contrato inicial de Context Router e nao sao fonte da verdade.

## Justificativa

Separar esses componentes preserva os principios centrais do framework:

- Specification First: contexto deve ser rastreavel a Specs, ADRs e fontes aprovadas.
- Provider Agnostic: nenhum modelo, runtime, banco vetorial ou provider deve ser necessario para a arquitetura central.
- Local First: pgvector, PostgreSQL e Ollama podem ser adapters locais futuros, nao defaults universais.
- Security by Design: contexto sensivel deve ser redigido, omitido ou bloqueado antes de entrega.
- Token Efficiency: contexto deve ser selecionado, deduplicado, comprimido e citado em vez de reenviado integralmente.
- Governance by Design: cada pacote de contexto deve explicar fontes, omissoes, redactions, estimativas, politicas e decisoes.

## Definicao de Context Router

Context Router e o componente responsavel por transformar uma necessidade de contexto em um `Context Package` governado.

Ele recebe objetivo de missao, task, papel de agente, contexto ja conhecido, politicas resolvidas, limites, dominios permitidos, necessidades de evidencia e requisitos do modelo. Em seguida consulta Knowledge Hub, Canonicalizer, Persistence Layer e, futuramente, Semantic Index para obter candidatos de contexto. Por fim, seleciona itens, aplica redactions/omissoes, solicita ou usa estimativas de token, preserva citacoes e produz um pacote justificavel.

Context Router nao e banco de dados, indice vetorial, RAG engine, runtime, agent, skill, tool, provider, Guardian Engine ou Policy Engine.

## Definicao de Token Budget Manager

Token Budget Manager e o componente responsavel por governar orcamento de tokens.

Ele estima tokens de input, contexto, instrucao, output esperado, tool/result payloads, validacao, sumarizacao e retries. Tambem reserva limites por escopo, calcula margem para resposta do modelo, sugere reducao de contexto, registra consumo estimado ou real e informa Model Selection Engine quando a janela necessaria excede modelos candidatos.

Ele nao escolhe modelo, nao recupera conhecimento, nao executa redaction, nao decide seguranca e nao executa runtime.

## Definicao de Context Package

Context Package e o artefato rastreavel produzido pelo Context Router para uma execucao especifica.

Campos conceituais minimos:

- `context_package_id`;
- `mission_id`, `workflow_id`, `task_id`, `attempt_id` e `agent_assignment_id` quando aplicaveis;
- objetivo e escopo da solicitacao;
- itens de contexto selecionados;
- fontes e citacoes;
- estimativas de tokens por item e totais;
- reserva de output;
- redactions aplicadas;
- motivos de omissao;
- referencias de politica;
- referencias de decisoes Guardian;
- hashes de conteudo e cache;
- warnings de confianca, stale index, sensibilidade ou prompt injection;
- metadados para reproducao e auditoria.

## Definicao de Memory Architecture

Memory Architecture e a organizacao em camadas da memoria do framework:

```text
Persistent Memory
↓
Persistence Layer
↓
Canonical Documents / Knowledge Records
↓
Knowledge Hub
↓
Derived Indexes, Text Search, Future Semantic Index
↓
Context Router
↓
Context Package
↓
Agent / Model / Runtime
```

Essa arquitetura separa durabilidade, canonicalizacao, recuperacao, selecao de contexto e entrega ao runtime.

## Diferencas conceituais

Memoria infinita nao e componente arquitetural. E uma promessa imprecisa que o framework deve evitar. Sistemas reais possuem limites de armazenamento, retencao, custo, privacidade, latencia, relevancia, janela de contexto e politica.

Memoria persistente e qualquer informacao duravel que sobrevive a sessoes, processos e runtimes. Inclui Specs, ADRs, documentos, missoes, workflows, tasks, decisoes, logs, validacoes, conversas autorizadas e pacotes de contexto persistidos.

Memoria semantica e capacidade de recuperar informacao por significado, normalmente usando embeddings, reranking ou representacoes semanticas. Ela depende de indices derivados e nao substitui a memoria persistente.

Knowledge Hub e o subsistema governado que organiza fontes, documentos canonicos, dominios, metadados, recuperacao, citacoes, redactions e indices derivados.

Semantic Index e um indice derivado para recuperacao semantica. Pode usar embeddings e bancos vetoriais, mas sempre aponta de volta para documentos canonicos. Nao e fonte da verdade.

Context Router e o decisor de contexto. Ele escolhe o que entra no pacote final, o que fica fora e por que, sob politicas, risco e orcamento.

## Responsabilidades do Context Router

O Context Router deve:

- receber requests de contexto de Mission/Task/Agent/Skill/Validation;
- consumir politicas resolvidas pelo Policy Engine;
- consultar Knowledge Hub para candidatos de contexto;
- solicitar canonicalizacao quando uma fonte ainda nao possuir forma canonica aprovada;
- consultar Persistence Layer para artefatos, decisoes e pacotes anteriores quando permitido;
- consultar Semantic Index futuro somente como mecanismo derivado;
- selecionar dominios relevantes;
- ordenar fontes por autoridade, atualidade, confianca, relevancia e escopo;
- deduplicar contexto;
- separar instrucoes confiaveis de dados recuperados;
- tratar documentos recuperados como dados nao confiaveis;
- aplicar ou registrar redactions conforme politica;
- registrar motivos de omissao;
- preservar citacoes e hashes;
- produzir Context Package com estimativas e policy refs;
- solicitar avaliacao Guardian quando pacote envolver risco;
- fornecer requisitos de contexto ao Model Selection Engine.

## Responsabilidades que nao pertencem ao Context Router

O Context Router nao deve:

- persistir diretamente ignorando Persistence Layer;
- escolher modelo concreto substituindo Model Selection Engine;
- resolver precedencia de politicas substituindo Policy Engine;
- fazer enforcement operacional substituindo Guardian Engine;
- executar tools, skills, providers, MCPs, bancos, APIs, shell ou runtimes;
- gerar embeddings ou gerenciar banco vetorial diretamente;
- canonicalizar binarios substituindo Canonicalizer;
- tratar Semantic Index como fonte da verdade;
- ampliar escopo ou permissao de contexto por conveniencia;
- remover citacoes para economizar tokens em tarefas que exigem rastreabilidade;
- prometer memoria infinita.

## Responsabilidades do Token Budget Manager

O Token Budget Manager deve:

- receber limites resolvidos de tokens por missao, workflow, task, agent assignment, ciclo e modelo;
- estimar tokens de itens de contexto, instrucoes, historico, ferramentas, validacao e output esperado;
- reservar margem minima para resposta do modelo;
- calcular orcamento restante;
- indicar contexto excedente;
- recomendar reducao, sumarizacao, priorizacao, chunking, omissao ou escalonamento de modelo;
- registrar estimativa, incerteza e consumo real quando disponivel;
- expor requisitos de janela de contexto para Model Selection Engine;
- impedir reenvio redundante quando cache e referencias forem suficientes;
- produzir razoes de omissao por limite de token.

## Responsabilidades que nao pertencem ao Token Budget Manager

O Token Budget Manager nao deve:

- selecionar fontes de conhecimento sozinho;
- escolher modelo concreto;
- decidir seguranca, privacidade ou aprovacao humana;
- executar redaction;
- armazenar registros diretamente;
- consultar providers de LLM diretamente;
- gerar embeddings;
- compactar semanticamente usando modelo sem passar por Model Selection e politica;
- sobrescrever limites definidos por Policy Engine ou Guardian Specs.

## Relacao com Policy Engine

Policy Engine resolve declarativamente politicas de contexto, privacidade, sensibilidade, dominios permitidos, retencao, cache, redaction, token budget, providers, modelos, storage, citacoes obrigatorias e approvals.

Context Router e Token Budget Manager consomem `Resolved Policy Set` ou referencias equivalentes. Eles nao definem politica global nem resolvem precedencia sozinhos.

## Relacao com Guardian Engine

Guardian Engine avalia risco operacional de Context Packages, ampliacao de contexto, redaction insuficiente, contexto sensivel, prompt injection, envio para provider externo, RAG cross-domain, uso de cache sensivel, excedente de token/custo e reuso de contexto.

Decisoes `block` impedem entrega do pacote afetado. Decisoes `require_approval` pausam a execucao ate aprovacao escopada. Decisoes `warn` devem ser registradas no Context Package.

## Relacao com Knowledge Hub

Knowledge Hub armazena e recupera conhecimento canonico, resultados citaveis, dominios, metadados, chunks e indices derivados.

Context Router usa Knowledge Hub como fonte governada de candidatos. Knowledge Hub nao decide sozinho o pacote final para o modelo.

## Relacao com Canonicalizer

Canonicalizer transforma fontes suportadas em Markdown canonico, com hashes, metadados, warnings, redactions e proveniencia.

Context Router nao deve usar fonte bruta nao canonicalizada como contexto primario quando a politica exigir forma canonica. Se faltar canonicalizacao, deve solicitar o fluxo apropriado ou omitir a fonte com motivo registrado.

## Relacao com Persistence Layer

Persistence Layer persiste registros, decisoes, documentos, pacotes, caches e audit trail por portas/adapters.

Context Router e Token Budget Manager devem produzir artefatos persistiveis, mas nao escrever diretamente em storage concreto. Caches de contexto devem referenciar hashes, politicas e fontes para invalidez segura.

## Relacao com Model Selection Engine

Model Selection Engine usa requisitos de contexto e tokens para escolher modelo compativel.

Context Router e Token Budget Manager fornecem:

- tamanho estimado de input;
- reserva de output;
- janela minima requerida;
- sensibilidade e privacidade do contexto;
- necessidade de citacoes;
- necessidade de raciocinio ou structured output;
- possibilidade de reduzir contexto;
- risco de provider externo.

Model Selection nao deve selecionar modelo que nao comporte o pacote aprovado, salvo se o Context Router conseguir reduzir contexto com justificativa.

## Relacao com Agent Orchestrator, Capabilities, Skills, Tools e Providers

Agent Orchestrator solicita contexto para uma Agent Assignment e recebe referencias de Context Package, nao acesso direto a bancos, stores, MCPs ou providers.

Agents consomem o contexto permitido e pedem capabilities quando precisam de mais informacao.

Capabilities expressam intencao de recuperar, ler, resumir ou validar contexto.

Skills implementam procedimentos de busca ou preparacao por Tools governadas.

Tools acessam Knowledge Hub, storage, providers, MCPs ou APIs por adapters aprovados.

Providers continuam abaixo de Tools/Provider Gateway e nao sao conhecidos diretamente por agentes.

## Relacao com SDD

No ciclo Spec -> Plan -> Tasks -> Implement -> Validate -> Commit:

- Spec define escopo, fontes autoritativas, politicas de contexto, privacidade, token e criterios de aceite.
- Plan usa Context Router para obter contexto de planejamento e identificar lacunas.
- Tasks recebem context refs, dominios permitidos, limites e omissoes relevantes.
- Implement usa Context Package aprovado para Agent Assignment ou Runtime Adapter.
- Validate usa pacotes com citacoes, evidencias e fontes autoritativas para checar resultado.
- Commit deve referenciar Spec, Task, Validation Result e, quando aplicavel, Context Package refs sem incluir segredos.

## Estrategia de token efficiency

A estrategia sera:

- preferir referencias, hashes e citacoes a documentos inteiros;
- filtrar por dominio antes de busca ampla;
- priorizar Specs, ADRs e documentos autoritativos;
- deduplicar por hash e similaridade futura;
- limitar resultados por tarefa e risco;
- reservar output antes de preencher contexto;
- resumir apenas quando politica permitir e com citacoes preservadas;
- reutilizar Context Packages por cache quando fonte, politica e escopo nao mudarem;
- escalar modelo somente depois de tentar reducao segura de contexto.

## Estrategia de redaction e contexto sensivel

Contexto sensivel deve ser classificado antes de entrega. Redaction deve ocorrer antes de logs, cache, embeddings, envio a provider externo ou persistencia quando politica exigir.

O Context Package deve registrar tipo de redaction, localizacao aproximada, politica aplicada e impacto. Falha de redaction obrigatoria deve bloquear entrega automatica.

Segredos nao devem ser enviados a modelos externos. Dados marcados como `local_required` devem permanecer em runtime/provider local ou ser omitidos.

## Estrategia de citacoes e rastreabilidade

Todo Context Item deve preservar citacoes para documento, path, URI, heading, linha, chunk, hash ou registro persistido quando disponivel.

Contexto sem citacao pode ser usado apenas como contexto de baixa confianca e deve ser marcado. Tarefas de arquitetura, seguranca, compliance e validacao devem exigir fontes citaveis.

## Estrategia de cache, hash e reutilizacao de contexto

Caches de contexto devem ser derivados e invalidaveis por:

- hash de conteudo;
- versao de documento;
- politica resolvida;
- permissoes;
- redactions;
- modelo ou janela de contexto;
- dominio;
- query ou objetivo;
- status de indice;
- sensibilidade;
- decisao Guardian expirada.

Cache nao deve permitir bypass de Policy Engine ou Guardian Engine. Reuso de pacote deve registrar motivo e validade.

## Estrategia futura para Semantic Index, embeddings e pgvector

Semantic Index sera adapter/indice derivado do Knowledge Hub. Embeddings serao gerados por provider selecionado por politica e Model Selection quando aplicavel. pgvector podera ser adapter futuro de vector store, especialmente no ambiente atual, mas nao sera default obrigatorio.

Regras futuras:

- chunks devem apontar para Canonical Documents;
- dimensao de embedding vem do modelo e do indice;
- troca de embedding model exige novo indice, versao ou reindexacao;
- embeddings de conteudo sensivel exigem redaction e avaliacao Guardian;
- busca semantica retorna candidatos citaveis, nao Context Package final;
- Context Router aprova, reduz e justifica a entrega.

## O que nao deve ser implementado ainda

Nao deve ser implementado nesta fase:

- codigo de Context Router;
- codigo de Token Budget Manager;
- nova pasta em `src/`;
- testes ou contratos executaveis novos;
- Semantic Index funcional;
- embeddings;
- pgvector;
- schema PostgreSQL;
- RAG runtime;
- adapters para LangGraph, AutoGen, MetaGPT, ECC ou Hermes;
- integracao direta com OpenCode, Claude Code ou Codex CLI;
- promessa de memoria infinita;
- dependencia obrigatoria de PostgreSQL, pgvector, Ollama ou modelo especifico.

## Consequencias positivas

- Define fronteira clara entre memoria, conhecimento, indice, contexto e tokens.
- Evita acoplamento prematuro a pgvector, PostgreSQL, Ollama ou OpenCode.
- Prepara RAG governado e rastreavel.
- Reduz risco de vazamento de contexto sensivel.
- Da insumos concretos para Model Selection.
- Transforma Token Efficiency em contrato operacional futuro.
- Mantem Semantic Index como derivado, nao fonte da verdade.

## Consequencias negativas

- Adiciona novos componentes conceituais antes de implementacao.
- Exige contratos entre varios modulos existentes.
- Pode aumentar quantidade de registros auditaveis.
- Exige disciplina para nao duplicar politicas em Context Router e Token Budget Manager.
- Pode atrasar implementacao de embeddings e pgvector ate contratos estarem estaveis.

## Riscos

- Context Router virar Knowledge Hub ou RAG engine monolitico.
- Token Budget Manager virar Model Selection ou Guardian parcial.
- Semantic Index futuro ser usado diretamente por agentes.
- Cache reutilizar contexto sob politica expirada.
- Citacoes serem descartadas por economia de tokens.
- Redaction incompleta gerar vazamento em embeddings, logs ou providers externos.
- pgvector virar default acidental por ser o ambiente atual.
- Conversas serem persistidas como memoria sem politica de retencao.

## Checklist para proximas missoes

- [ ] Atualizar mapas de arquitetura e README principal para referenciar Spec 0014 quando apropriado.
- [ ] Definir modulo futuro de Context Router somente apos aprovacao da Spec.
- [ ] Definir contratos formais de `ContextRequest`, `ContextPackage`, `ContextItem` e `TokenBudget`.
- [ ] Definir como Policy Engine entrega `Resolved Policy Set` para contexto e tokens.
- [ ] Definir como Guardian Engine avalia Context Packages.
- [ ] Definir persistencia futura de Context Packages e Token Budget Records.
- [ ] Definir criterios de invalidacao de cache por hash e politica.
- [ ] Definir contrato minimo de Semantic Index antes de embeddings.
- [ ] Definir ADR separada para pgvector somente quando adapter for implementado.
- [ ] Manter memoria infinita fora da linguagem tecnica do framework.

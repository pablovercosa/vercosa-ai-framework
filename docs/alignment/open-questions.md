# Perguntas Em Aberto

## Objetivo

Este documento lista perguntas arquiteturais que devem ser respondidas antes da próxima onda significativa de implementação.

As perguntas são agrupadas por área de decisão. Cada item não resolvido deve gerar uma ADR, uma atualização de Spec ou uma decisão explícita do projeto quando afetar implementação.

## Fronteiras Centrais

1. Guardian Engine é o Policy Engine concreto da fase atual ou Policy Engine deve ser um componente separado que delega ao Guardian Engine?
2. Onde a precedência de políticas é resolvida: Guardian Engine, Policy Engine, Mission Runner ou um resolvedor dedicado?
3. Mission Orchestrator deve ser implementado como módulo separado antes de expandir Mission Runner?
4. Qual é a fronteira exata entre Mission Runner e Mission Orchestrator?
5. Qual é a fronteira exata entre Workflow Engine e Task Queue?
6. Workflow Engine deve sempre usar Task Queue ou pode manter um executor sequencial direto para workflows locais simples?
7. Qual componente é responsável por replanejamento após falha de validação?
8. Qual componente é responsável pelo encerramento final da missão e pela agregação de evidências de validação?

## Ciclo De Vida SDD

1. O que conta como Spec aprovada para implementação?
2. Onde a aprovação de Spec é registrada?
3. Missões apenas documentais podem prosseguir sem uma Spec de funcionalidade aprovada?
4. Qual artefato mínimo de Plan é obrigatório antes da criação de Tasks?
5. Qual artefato mínimo de Task é obrigatório antes do início da implementação?
6. Quais validações são obrigatórias antes de uma task ser marcada como concluída?
7. Quais validações são obrigatórias antes de uma missão ser marcada como concluída?
8. Quais metadados devem ser incluídos em um commit criado pelo framework?
9. Auto-commit deve permanecer desabilitado globalmente salvo quando explicitamente habilitado por missão?
10. Como uma validação com falha deve retornar para Plan ou Tasks?

## Memória E Contexto

1. Qual é a diferença formal entre memória persistente, Knowledge Hub, Semantic Index e Context Router?
2. Context Router deve ser um novo módulo de primeiro nível?
3. Qual é o contrato mínimo de request e response do Context Router?
4. Quais políticas podem excluir contexto de um prompt?
5. Como redaction de contexto deve ser representada em logs de auditoria?
6. Como citações devem ser preservadas da recuperação até a saída final do agente?
7. O que deve ser armazenado permanentemente versus recomputado a partir de documentos canônicos?
8. Qual política de retenção se aplica a conversas, prompts, logs e decisões?
9. Histórico de conversa deve fazer parte do Knowledge Hub por padrão ou por opt-in?
10. Como conhecimento sensível deve ser indexado sem expor segredos?

## Knowledge Hub E Semantic Index

1. Quais são os primeiros tipos de documento canônico além de Markdown?
2. O suporte a PDF/DOCX/PPTX deve aguardar Specs separadas de adapter?
3. Qual estratégia de chunking deve ser usada para índices semânticos?
4. Quais metadados são obrigatórios para cada chunk indexado?
5. Qual é o primeiro contrato de adapter para embedding provider?
6. `nomic-embed-text` é o padrão local inicial apenas quando detectado ou um adapter recomendado documentado?
7. pgvector é o primeiro vector store adapter ou apenas o alvo do ambiente atual?
8. Como índices semânticos devem ser invalidados quando documentos canônicos mudam?
9. Qual é o fallback quando embeddings não estão disponíveis?
10. Como Code Intelligence deve compartilhar ou separar índices do Knowledge Hub?

## Agentes E Capabilities

1. Qual é o schema mínimo de perfil de agente para uso real?
2. Como perfis de agentes são aprovados, versionados e armazenados?
3. Agentes podem solicitar várias capabilities em uma task ou capabilities devem ser resolvidas uma por vez?
4. Qual componente decide se deve delegar para subagentes?
5. Qual é a profundidade máxima de delegação?
6. Qual é a condição de parada padrão para loops de agente?
7. Quais capabilities são essenciais para o primeiro caminho de implementação ponta a ponta?
8. Quais capabilities exigem aprovação humana?
9. Como saídas de agentes são validadas antes de se tornarem saídas de task?
10. Como a confiança do agente é representada sem permitir que o modelo autocertifique conclusão?

## Skills, Tools, Providers E MCPs

1. Qual é o primeiro catálogo aprovado de capabilities?
2. Qual é o primeiro catálogo aprovado de skills?
3. Quais tools locais são permitidas no perfil seguro inicial?
4. Quais efeitos toda tool deve declarar?
5. Como permissões de tools devem mapear para decisões Guardian?
6. Onde adapters MCP ficam: tools, providers, runtime ou um pacote distinto de adapters?
7. Qual é o processo de revisão de segurança para um MCP server?
8. Uma tool pode chamar um runtime adapter ou runtimes devem permanecer separados da execução de providers/tools?
9. Quais operações de provider são permitidas apenas em dry-run?
10. Como fallback de provider deve ser auditado?

## Runtime Adapters

1. Qual é o contrato formal de conformidade de RuntimeAdapter?
2. Quais capabilities todo runtime adapter deve reportar?
3. O que model discovery significa em OpenCode, Claude Code, Codex CLI, IDEs, Web UI e API?
4. Como funcionalidades específicas de runtime devem ser representadas sem vazar para o core?
5. Claude Code e Codex CLI devem ser tratados de forma idêntica ao OpenCode no nível de adapter?
6. Como runtimes sem execução headless devem ser suportados?
7. Como aprovação interativa deve ser representada em CLI, Web UI e IDEs?
8. Como logs de runtime devem ser normalizados?
9. Quais falhas de runtime podem ser retentadas?
10. Uma missão pode trocar de runtime durante a execução?

## Frameworks Externos

1. LangGraph deve ser usado como backend de workflow, referência ou não deve ser usado?
2. MetaGPT deve ser usado como referência de organização de agentes, adapter ou não deve ser usado?
3. AutoGen deve ser usado como backend de conversa multiagente, adapter ou não deve ser usado?
4. Qual footprint de dependências é aceitável para adapters opcionais de frameworks?
5. Frameworks externos conseguem cumprir requisitos de auditoria e política do Vercosa sem wrappers invasivos?
6. Como estados de frameworks externos são mapeados para estados de missão/workflow/task do Vercosa?
7. Como chamadas de tools de frameworks externos são forçadas a passar por capabilities/skills/tools do Vercosa?
8. Quais recursos de frameworks externos devem influenciar o design do Vercosa sem serem copiados?
9. O que desqualifica um framework externo para uso no core?
10. Adapters de frameworks externos devem viver fora do pacote core?

## Persistência E Auditoria

1. Quais stores são obrigatórios para o primeiro MVP integrado?
2. Quais dados devem ser persistidos para recuperação de missão após crash?
3. Quais dados nunca devem ser persistidos em texto claro?
4. Qual é o schema de audit log?
5. Qual é a política de retenção para audit logs?
6. Persistência em filesystem deve permanecer padrão até adapters de banco amadurecerem?
7. Qual é o primeiro adapter de banco: SQLite, PostgreSQL ou ambos?
8. Como migrations são representadas e validadas?
9. Como hashes de registros são calculados entre adapters?
10. Como backups e restores são tratados sem vazar segredos?

## Segurança E Governança

1. Qual é o modo Guardian padrão para desenvolvimento local?
2. Qual é o modo Guardian padrão para automação ou execução daemon?
3. Quais comandos são bloqueados em todos os sistemas operacionais?
4. Quais comandos exigem aprovação em todos os sistemas operacionais?
5. Como detecções falso-positivas de segredos são aprovadas sem expor valores?
6. Qual política controla acesso à rede?
7. Qual política controla acesso a providers pagos?
8. Qual política controla acesso de provider externo com contexto do projeto?
9. Como exceções de política são aprovadas, escopadas e expiradas?
10. Quais registros de governança são obrigatórios antes de alterar arquitetura?

## Model Selection

1. Onde o Model Registry é persistido?
2. Qual é o schema mínimo de Model Profile para a próxima fase?
3. Como modelos descobertos pelo OpenCode são mesclados com modelos de providers configurados?
4. Como custo de modelo deve ser representado quando providers não expõem custo preciso?
5. O que qualifica um `small_model`?
6. Como fallback de modelo deve ser auditado?
7. Uma decisão de modelo pode expirar?
8. Quando cross-review é obrigatório?
9. Como Model Selection consome estimativas do Context Router?
10. Como políticas de privacidade local-only são aplicadas em model selection e execução de runtime?

## ADRs Recomendadas

Crie ADRs para estas decisões antes de novo código quando possível:

- Fronteira entre Policy Engine e Guardian Engine.
- Fronteira entre Mission Runner e Mission Orchestrator.
- Context Router e arquitetura de memória.
- Fronteira entre Knowledge Hub e Semantic Index.
- Modelo de conformidade de Runtime Adapter.
- Posicionamento de frameworks externos para LangGraph, MetaGPT e AutoGen.
- Local de adapters MCP e processo de revisão de segurança.
- Ordem de adapters de persistência: filesystem, SQLite, PostgreSQL.

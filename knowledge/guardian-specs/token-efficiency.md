# Guardian Spec 002 — Token Efficiency

## Objetivo

Economizar tokens sem reduzir a qualidade do produto final.

## Escopo

Aplica-se a prompts, missões, specs, agentes, subagentes, RAG, MCPs, Knowledge Hub e seleção de modelos.

## Regras

1. Nunca enviar contexto redundante.
2. Preferir texto puro a formatos binários.
3. Converter arquivos binários para Markdown canônico antes do uso.
4. Usar recuperação seletiva de contexto.
5. Separar bases de conhecimento por domínio.
6. Usar chunks adaptativos.
7. Utilizar cache semântico quando possível.
8. Preferir modelos locais ou gratuitos para tarefas simples.
9. Usar modelos pagos somente quando a complexidade justificar ou a política permitir.
10. Registrar custo, tokens e justificativa de uso quando possível.

## Estratégias

- Smart Retrieval
- Context Router
- Semantic Compression
- Prompt Deduplication
- Incremental Context
- Multi-level Context
- Adaptive Chunking
- Model Selection Engine
- Cost-aware Routing

## Bases recomendadas

- Specification RAG
- Code RAG
- Documentation RAG
- Legal RAG
- Book RAG
- Conversation RAG

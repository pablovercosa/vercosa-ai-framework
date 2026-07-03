Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0011-knowledge-hub.md
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar MVP do Knowledge Hub com ingestão Markdown local.

Entregáveis esperados:
- src/vercosa_ai_framework/knowledge/markdown.py
- src/vercosa_ai_framework/knowledge/search.py
- tests/test_knowledge_markdown.py
- tests/test_knowledge_search.py
- docs/knowledge-hub.md

Requisitos:
- ler Markdown local;
- extrair frontmatter YAML simples sem dependência pesada;
- criar KnowledgeDocument;
- indexar em InMemoryKnowledgeStore;
- busca textual simples determinística;
- filtro por domínio e tags;
- detectar conteúdo suspeito de prompt injection de forma básica e marcar warning metadata;
- não implementar embeddings ainda;
- não acessar PostgreSQL;
- não chamar APIs externas;
- não usar sudo;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

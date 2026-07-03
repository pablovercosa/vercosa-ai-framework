Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0011-knowledge-hub.md
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais do Knowledge Hub.

Entregáveis esperados:
- src/vercosa_ai_framework/knowledge/__init__.py
- src/vercosa_ai_framework/knowledge/types.py
- src/vercosa_ai_framework/knowledge/store.py
- tests/test_knowledge_contracts.py
- tests/test_knowledge_store.py

Requisitos:
- criar KnowledgeDocument;
- criar KnowledgeSource;
- criar KnowledgeDomain;
- criar KnowledgeQuery;
- criar KnowledgeSearchResult;
- criar KnowledgeStore abstrato;
- criar InMemoryKnowledgeStore;
- suportar adicionar documento;
- suportar buscar por domínio, tags e texto simples;
- suportar frontmatter metadata;
- não implementar embeddings ainda;
- não chamar APIs externas;
- não acessar banco real;
- não usar subprocess;
- manter provider agnostic.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

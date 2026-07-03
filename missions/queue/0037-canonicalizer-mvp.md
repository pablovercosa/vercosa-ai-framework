Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0012-canonicalizer.md
- src/vercosa_ai_framework/canonicalizer/
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar MVP do Canonicalizer para texto e Markdown.

Entregáveis esperados:
- src/vercosa_ai_framework/canonicalizer/engine.py
- src/vercosa_ai_framework/canonicalizer/markdown.py
- tests/test_canonicalizer_engine.py
- tests/test_canonicalizer_markdown.py
- docs/canonicalizer.md

Requisitos:
- canonicalizar texto puro;
- canonicalizar Markdown com frontmatter YAML simples;
- calcular hash determinístico do conteúdo;
- gerar CanonicalDocument;
- normalizar título quando possível;
- preservar metadados;
- detectar prompt injection básico e marcar warning;
- detectar provável segredo e marcar warning/redaction metadata sem expor segredo em logs;
- integrar com KnowledgeDocument, se fizer sentido;
- não converter PDF/DOCX ainda;
- não chamar APIs externas;
- não usar dependência pesada;
- não usar sudo.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

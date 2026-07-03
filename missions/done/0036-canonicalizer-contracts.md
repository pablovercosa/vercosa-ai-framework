Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0012-canonicalizer.md
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais do Canonicalizer.

Entregáveis esperados:
- src/vercosa_ai_framework/canonicalizer/__init__.py
- src/vercosa_ai_framework/canonicalizer/types.py
- src/vercosa_ai_framework/canonicalizer/adapter.py
- tests/test_canonicalizer_contracts.py

Requisitos:
- criar CanonicalDocument;
- criar CanonicalSource;
- criar CanonicalMetadata;
- criar CanonicalizationRequest;
- criar CanonicalizationResult;
- criar CanonicalizerAdapter abstrato;
- suportar source_type: text, markdown, pdf, docx, html, image, audio, video, unknown;
- não implementar conversores externos ainda;
- não chamar APIs externas;
- não usar subprocess;
- não usar sudo;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

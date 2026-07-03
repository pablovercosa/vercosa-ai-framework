Leia obrigatoriamente:
- AGENTS.md
- knowledge/principles/framework-principles.md
- knowledge/architecture/core-architecture.md
- specs/framework/0011-knowledge-hub.md
- src/vercosa_ai_framework/knowledge/

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Canonicalizer do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0012-canonicalizer.md

A Spec deve cobrir:
- Canonicalizer como camada de entrada para Knowledge Hub;
- conversão de qualquer fonte suportada para CanonicalDocument;
- Markdown como formato canônico inicial;
- frontmatter YAML;
- preservação de fonte, hash, data, tipo, domínio e metadados;
- suporte inicial a texto e Markdown;
- suporte futuro a PDF, DOCX, ODT, HTML, EPUB, PPTX, XLSX, imagens/OCR, áudio, vídeo e transcrições;
- text-only como regra de eficiência de tokens;
- deduplicação por hash;
- limpeza de conteúdo;
- normalização de títulos;
- extração de metadados;
- detecção de prompt injection;
- redaction de segredos;
- integração com Guardian Engine;
- integração com Knowledge Hub;
- provider agnostic;
- uso futuro de Docling ou adapters externos sem acoplamento.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

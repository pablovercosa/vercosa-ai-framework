Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- knowledge/principles/framework-principles.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0010-provider-gateway.md

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Knowledge Hub do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0011-knowledge-hub.md

A Spec deve cobrir:
- Knowledge Hub como base de conhecimento do framework;
- Canonical Documents;
- Semantic Indexes;
- RAG por domínio;
- fontes: specs, ADRs, docs, código, legislação, livros, conversas, decisões, agentes, skills, comandos e hooks;
- ingestão de Markdown;
- conversão futura de PDF, DOCX, HTML, EPUB, PPTX, XLSX, imagens/OCR, áudio e vídeo para Markdown;
- frontmatter YAML;
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
- futura integração com PostgreSQL + pgvector.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

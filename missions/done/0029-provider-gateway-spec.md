Leia obrigatoriamente:
- AGENTS.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0009-capabilities-skills-tools.md
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/guardian/

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Provider / MCP / API Gateway do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0010-provider-gateway.md

A Spec deve cobrir:
- diferença entre Tool, Provider, MCP e API;
- Tool não deve conhecer detalhes internos de provider;
- Provider Gateway como camada de isolamento;
- MCP como uma forma de provider, não como núcleo;
- suporte futuro a APIs HTTP, CLIs locais, MCPs, bancos, filesystem e serviços locais;
- Provider Registry;
- Provider Adapter;
- ProviderRequest;
- ProviderResult;
- permissões;
- integração com Guardian Engine;
- integração com Tool Executor;
- logs e rastreabilidade;
- bloqueio de providers perigosos;
- redaction de segredos;
- dry_run;
- timeout;
- retries;
- fallback entre providers;
- provider agnostic;
- OpenCode como runtime inicial, não núcleo.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

Leia obrigatoriamente:
- AGENTS.md
- knowledge/vision.md
- knowledge/architecture/core-architecture.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0002-model-selection-engine.md

Assuma o papel de framework-architect.

Missão:
Criar a Spec do OpenCode Runtime Adapter.

Entregável obrigatório:
- specs/framework/0003-opencode-runtime-adapter.md

A Spec deve definir:
- OpenCode como runtime inicial, não como núcleo;
- contrato de Runtime Adapter;
- execução de missões;
- entrada/saída esperada;
- logs;
- permissões;
- seleção de modelo via Model Selection Engine;
- uso de small_model;
- limites de execução;
- auto-approve;
- auto-commit;
- isolamento de plugins;
- fallback futuro para Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API;
- relação com Guardian Specs;
- riscos e mitigações.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo;
- registrar pendências se faltar decisão.

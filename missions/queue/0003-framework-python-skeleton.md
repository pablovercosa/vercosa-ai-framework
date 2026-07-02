Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0002-model-selection-engine.md, se existir.

Assuma o papel de implementation-architect.

Missão:
Criar o esqueleto inicial Python do Vercosa AI Framework.

Entregáveis obrigatórios:
- pyproject.toml
- src/vercosa_ai_framework/__init__.py
- src/vercosa_ai_framework/cli.py
- src/vercosa_ai_framework/core/__init__.py
- src/vercosa_ai_framework/core/models.py
- src/vercosa_ai_framework/core/policies.py
- tests/test_cli.py
- docs/development.md

Requisitos:
- CLI inicial deve expor comando básico de versão ou diagnóstico.
- Não implementar lógica complexa ainda.
- Estrutura deve favorecer Clean Architecture.
- Não acoplar a OpenCode.
- Não acoplar a OpenAI.
- Não acoplar a PostgreSQL.
- Não usar segredos.
- Não usar sudo.
- Não alterar configs globais.

Critérios de aceite:
- python -m compileall src deve passar.
- pytest deve ser configurável, mesmo que os testes sejam mínimos.
- pyproject.toml deve conter metadados básicos do projeto.

Leia obrigatoriamente:
- AGENTS.md
- src/vercosa_ai_framework/cli.py
- src/vercosa_ai_framework/workflows/
- src/vercosa_ai_framework/missions/

Assuma o papel de implementation-architect.

Missão:
Adicionar comandos CLI iniciais para Workflow Engine.

Entregáveis esperados:
- atualizar src/vercosa_ai_framework/cli.py
- atualizar tests/test_cli.py
- criar ou atualizar docs/cli.md

Comandos desejados:
- vaf workflow-status
- vaf workflow-run
- vaf workflow-validate

Requisitos:
- não executar OpenCode real nos testes;
- permitir dry_run;
- aceitar arquivo de workflow simples;
- manter comandos existentes funcionando;
- não usar dependência pesada;
- não acessar configs globais.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

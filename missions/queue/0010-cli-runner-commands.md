Leia obrigatoriamente:
- AGENTS.md
- src/vercosa_ai_framework/cli.py
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/runtime/

Assuma o papel de implementation-architect.

Missão:
Adicionar comandos CLI iniciais para o Mission Runner.

Entregáveis esperados:
- atualizar src/vercosa_ai_framework/cli.py
- atualizar tests/test_cli.py
- docs/cli.md

Comandos desejados:
- vaf version
- vaf status
- vaf run-one
- vaf run-worker

Requisitos:
- usar argparse ou implementação simples sem dependência pesada;
- não executar OpenCode real nos testes;
- permitir dry_run;
- manter compatibilidade com testes existentes;
- não usar sudo;
- não acessar configs globais do OpenCode.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

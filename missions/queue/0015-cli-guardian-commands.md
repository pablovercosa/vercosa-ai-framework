Leia obrigatoriamente:
- AGENTS.md
- src/vercosa_ai_framework/cli.py
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/missions/

Assuma o papel de implementation-architect.

Missão:
Adicionar comandos CLI para validação Guardian e execução segura.

Entregáveis esperados:
- atualizar src/vercosa_ai_framework/cli.py
- atualizar tests/test_cli.py
- criar ou atualizar docs/cli.md

Comandos desejados:
- vaf check-mission <arquivo>
- vaf run-one --guardian-mode strict
- vaf run-worker --guardian-mode strict
- vaf status

Requisitos:
- check-mission deve imprimir decisão Guardian;
- não executar OpenCode real nos testes;
- permitir dry_run;
- manter comandos existentes funcionando;
- não usar dependência pesada;
- não acessar configs globais.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

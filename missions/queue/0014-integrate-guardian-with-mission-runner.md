Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0004-mission-runner.md
- specs/framework/0005-guardian-engine.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/runtime/

Assuma o papel de implementation-architect.

Missão:
Integrar o Guardian Engine ao Mission Runner.

Entregáveis esperados:
- atualizar src/vercosa_ai_framework/missions/runner.py
- atualizar src/vercosa_ai_framework/missions/types.py, se necessário
- atualizar tests/test_mission_runner.py
- criar tests/test_mission_runner_guardian.py
- atualizar docs/mission-runner.md

Requisitos:
- Mission Runner deve validar a missão antes de executar RuntimeAdapter;
- decisão allow: executa normalmente;
- decisão warn: executa, mas registra warnings no resultado;
- decisão require_approval: não executa em modo não interativo;
- decisão block: não executa e marca como failed ou blocked;
- permitir guardian_mode: permissive, standard, strict;
- não executar OpenCode real nos testes;
- não usar sudo;
- manter RuntimeAdapter abstrato.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

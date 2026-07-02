Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0004-mission-runner.md
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/runtime/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP do Mission Runner em Python.

Entregáveis esperados:
- src/vercosa_ai_framework/missions/runner.py
- tests/test_mission_runner.py
- docs/mission-runner.md

Requisitos:
- executar uma missão por vez;
- mover queued -> running -> done/failed;
- usar RuntimeAdapter abstrato;
- registrar MissionResult;
- suportar auto_commit como interface, mas sem executar git real nos testes;
- suportar limite de ciclos;
- não chamar OpenCode real nos testes;
- não usar sudo;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

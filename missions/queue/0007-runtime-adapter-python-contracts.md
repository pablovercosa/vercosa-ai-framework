Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0003-opencode-runtime-adapter.md, se existir.
- specs/framework/0004-mission-runner.md, se existir.
- src/vercosa_ai_framework/model_selection/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais para Runtime Adapter e Mission Runner.

Entregáveis esperados:
- src/vercosa_ai_framework/runtime/__init__.py
- src/vercosa_ai_framework/runtime/types.py
- src/vercosa_ai_framework/runtime/adapter.py
- src/vercosa_ai_framework/missions/__init__.py
- src/vercosa_ai_framework/missions/types.py
- src/vercosa_ai_framework/missions/queue.py
- tests/test_runtime_contracts.py
- tests/test_mission_queue.py

Requisitos:
- não executar OpenCode ainda;
- não chamar APIs externas;
- não usar subprocess nesta missão;
- criar contratos/interfaces puras;
- criar Mission, MissionStatus, MissionResult;
- criar RuntimeAdapter abstrato;
- criar fila local baseada em diretório temporário para testes;
- manter provider agnostic;
- manter OpenCode fora do núcleo.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0003-opencode-runtime-adapter.md
- specs/framework/0004-mission-runner.md
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/missions/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP do OpenCode Runtime Adapter.

Entregáveis esperados:
- src/vercosa_ai_framework/runtime/opencode.py
- tests/test_opencode_runtime_adapter.py
- docs/opencode-runtime-adapter.md

Requisitos:
- criar adapter que monta comando para OpenCode;
- não executar OpenCode real nos testes;
- usar subprocess apenas atrás de interface testável;
- permitir dry_run;
- permitir model e small_model;
- permitir auto_approve;
- permitir cwd;
- capturar exit_code, stdout, stderr;
- não depender de configs globais;
- não expor segredos;
- não usar sudo.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

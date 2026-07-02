Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0005-guardian-engine.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/missions/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP do Guardian Engine.

Entregáveis esperados:
- src/vercosa_ai_framework/guardian/engine.py
- tests/test_guardian_engine.py
- docs/guardian-engine.md

Requisitos:
- validar texto da missão antes da execução;
- detectar comandos perigosos como rm -rf /, mkfs, dd destrutivo, shutdown, reboot;
- detectar presença provável de segredos;
- detectar sudo;
- detectar alteração de configs globais;
- retornar allow/warn/block/require_approval;
- modo strict deve bloquear sudo e configs globais;
- modo standard deve exigir aprovação para sudo;
- modo permissive deve gerar warning;
- não executar comandos;
- não usar APIs externas;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

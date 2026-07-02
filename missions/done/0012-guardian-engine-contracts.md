Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0005-guardian-engine.md
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/runtime/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais do Guardian Engine.

Entregáveis esperados:
- src/vercosa_ai_framework/guardian/__init__.py
- src/vercosa_ai_framework/guardian/types.py
- src/vercosa_ai_framework/guardian/policies.py
- tests/test_guardian_contracts.py

Requisitos:
- criar GuardianDecision;
- criar GuardianSeverity;
- criar GuardianAction: allow, warn, block, require_approval;
- criar GuardianPolicy;
- criar estruturas para violations;
- não executar comandos;
- não chamar APIs externas;
- não usar OpenCode real;
- manter código testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

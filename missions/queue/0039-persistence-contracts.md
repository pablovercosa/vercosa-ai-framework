Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0013-persistence-layer.md
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/workflows/
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/canonicalizer/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais da Persistence Layer.

Entregáveis esperados:
- src/vercosa_ai_framework/persistence/__init__.py
- src/vercosa_ai_framework/persistence/types.py
- src/vercosa_ai_framework/persistence/repository.py
- tests/test_persistence_contracts.py

Requisitos:
- criar Repository abstrato genérico;
- criar EntityRef;
- criar PersistedRecord;
- criar PersistenceResult;
- criar QueryFilter simples;
- suportar save/get/list/delete em contrato;
- não implementar banco real;
- não chamar APIs externas;
- não usar subprocess;
- não usar sudo;
- manter storage agnostic;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

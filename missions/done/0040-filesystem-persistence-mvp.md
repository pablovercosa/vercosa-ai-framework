Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0013-persistence-layer.md
- src/vercosa_ai_framework/persistence/
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/canonicalizer/

Assuma o papel de implementation-architect.

Missão:
Implementar MVP de persistência em filesystem com JSON.

Entregáveis esperados:
- src/vercosa_ai_framework/persistence/filesystem.py
- tests/test_filesystem_persistence.py
- docs/persistence-layer.md

Requisitos:
- salvar registros em JSON;
- listar registros;
- recuperar por id;
- excluir por id;
- usar diretório configurável;
- serialização determinística;
- não persistir segredos em claro se metadata indicar secret_warning;
- suportar namespaces/collections;
- não usar banco real;
- não chamar APIs externas;
- não usar sudo;
- manter testável com tmp_path.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

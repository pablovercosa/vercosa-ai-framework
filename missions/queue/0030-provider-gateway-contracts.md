Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0010-provider-gateway.md
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar contratos Python iniciais do Provider Gateway.

Entregáveis esperados:
- src/vercosa_ai_framework/providers/__init__.py
- src/vercosa_ai_framework/providers/types.py
- src/vercosa_ai_framework/providers/registry.py
- src/vercosa_ai_framework/providers/adapter.py
- tests/test_provider_contracts.py
- tests/test_provider_registry.py

Requisitos:
- criar ProviderProfile;
- criar ProviderKind: mcp, api, cli, filesystem, database, local_service, mock;
- criar ProviderRequest;
- criar ProviderResult;
- criar ProviderAdapter abstrato;
- criar ProviderRegistry em memória;
- suportar busca por nome, kind, tags e domínio;
- suportar enabled/disabled;
- não executar provider real;
- não chamar APIs externas;
- não usar subprocess;
- não usar sudo;
- manter testável.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

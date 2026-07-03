Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0010-provider-gateway.md
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/guardian/

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP do Provider Gateway e integrar com Tool Executor.

Entregáveis esperados:
- src/vercosa_ai_framework/providers/gateway.py
- atualizar src/vercosa_ai_framework/tools/executor.py, se necessário
- tests/test_provider_gateway.py
- tests/test_tool_executor_provider_gateway.py
- docs/provider-gateway.md

Requisitos:
- ProviderGateway deve receber ProviderRequest;
- validar request com Guardian Engine antes de executar provider;
- executar ProviderAdapter abstrato ou callable injetável;
- suportar dry_run;
- suportar timeout como campo de configuração, sem necessidade de timeout real se não houver execução real;
- suportar fallback simples entre providers compatíveis;
- bloquear provider disabled;
- retornar ProviderResult;
- ToolExecutor deve conseguir delegar para ProviderGateway quando configurado;
- não executar MCP real;
- não chamar APIs externas;
- não usar subprocess real nos testes;
- não usar sudo;
- manter provider agnostic.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar.

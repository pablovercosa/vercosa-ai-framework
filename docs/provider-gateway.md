# Provider Gateway MVP

O Provider Gateway é a fronteira entre Tools e providers concretos no Vercosa AI Framework.

Neste MVP, ele é deliberadamente side-effect-free por padrão: não cria providers reais, não chama MCP, não chama APIs externas, não usa subprocess e não executa comandos. A execução real só ocorre por adapter ou callable injetado pelo runtime ou pelos testes.

## Fluxo

```text
ToolExecutor
↓
ProviderRequest
↓
ProviderGateway
↓
Guardian Engine
↓
ProviderAdapter ou callable injetável
↓
ProviderResult
↓
ToolExecutionResult
```

## Contratos

`ProviderRequest` carrega operação, contexto auditável, permissões concedidas, efeitos permitidos, `dry_run`, timeout, política de fallback e metadados sem segredos em claro.

`ProviderResult` normaliza sucesso, bloqueio, falha, dry-run, fallback, timeout aplicado, erros, avisos e referências de decisão do Guardian.

`ProviderProfile` é o registro declarativo do provider. Ele declara operações, permissões, efeitos, `adapter_ref`, status, timeout padrão e fallbacks permitidos.

## Comportamento MVP

- Valida provider antes de executar adapter.
- Bloqueia provider `disabled`, `blocked`, `dangerous` ou `deprecated`.
- Valida permissões concedidas contra permissões requeridas.
- Valida efeitos permitidos contra efeitos declarados.
- Consulta Guardian Engine antes de qualquer execução de adapter.
- Bloqueia decisões `block` e `require_approval`.
- Em `dry_run`, retorna plano normalizado e não chama adapter.
- Registra timeout como valor aplicado, sem enforcement real neste MVP.
- Executa `ProviderAdapter` ou callable injetável quando `dry_run=False`.
- Aplica fallback simples apenas quando `fallback_allowed=True`, o provider original declara `fallback_providers`, e o fallback é compatível.

## Integração Com ToolExecutor

`ToolExecutor` continua validando Tool e consultando Guardian no nível de Tool.

Quando configurado com `provider_gateway`, o executor monta um `ProviderRequest` a partir do `ToolExecutionRequest` e do `ToolProfile`, delega ao gateway e converte `ProviderResult` para `ToolExecutionResult`.

Sem `provider_gateway`, o comportamento legado com `ToolAdapter` injetável permanece disponível.

## Limitações Intencionais

- Sem execução real de MCP, HTTP, CLI, banco ou filesystem.
- Sem retry real.
- Sem enforcement real de timeout.
- Sem persistência de audit logs.
- Sem resolução de segredos.
- Sem seleção dinâmica avançada de providers.

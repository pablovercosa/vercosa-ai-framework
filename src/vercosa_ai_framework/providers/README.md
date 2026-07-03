# Providers Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0010](../../../specs/framework/0010-provider-gateway.md)

## Objetivo

Isolar providers, MCPs, APIs e outros mecanismos externos atrás de contratos normalizados.

## O Que Este Módulo Faz

- Define perfis, requests e resultados de provider.
- Mantém `ProviderRegistry`.
- Define contrato `ProviderAdapter`.
- Implementa `ProviderGateway` com validação, dry-run e adapter injetado.

## O Que Este Módulo Não Faz

- Não é uma capability, skill ou agent layer.
- Não deve ser chamado diretamente por agentes.
- Não embute credenciais ou endpoints finais no núcleo.
- Não torna MCP arquitetura central.
- Não escolhe modelo sem Model Selection Engine.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de provider, request e resultado. |
| `registry.py` | `ProviderRegistry`. |
| `adapter.py` | Contrato abstrato `ProviderAdapter`. |
| `gateway.py` | `ProviderGateway` e adapter callable. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `ProviderKind`: categorias de provider.
- `ProviderProfile`: metadados e permissões de provider.
- `ProviderRequest`: chamada normalizada.
- `ProviderResult`: resultado normalizado.
- `ProviderRegistry`: catálogo de providers.
- `ProviderAdapter`: contrato de adapter.
- `CallableProviderAdapter`: adapter baseado em callable injetado.
- `ProviderGateway`: fronteira de acesso a providers.

## Entradas E Saídas

Entradas:

- `ProviderRequest` vindo de ToolExecutor ou adapter autorizado.
- Provider registrado e adapter compatível.

Saídas:

- `ProviderResult` com payload, status, warnings e metadados.

## Dependências Internas

- `../guardian/`: avaliação de risco quando configurada.

## Módulos Relacionados

- Acima: [tools](../tools/README.md).
- Abaixo: providers externos, MCPs, APIs, bancos, CLIs e serviços locais.
- Paralelo: [runtime](../runtime/README.md).

## Specs Correspondentes

- [Spec 0010: Provider Gateway](../../../specs/framework/0010-provider-gateway.md)
- [Spec 0009: Capabilities, Skills e Tools](../../../specs/framework/0009-capabilities-skills-tools.md)

## Docs Relacionadas

- [Provider Gateway](../../../docs/provider-gateway.md)
- [External Framework Positioning](../../../docs/alignment/external-framework-positioning.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.providers import ProviderKind, ProviderProfile, ProviderRegistry

registry = ProviderRegistry()
registry.register(
    ProviderProfile(
        name="Local search",
        version="0.1.0",
        description="Local search provider",
        kind=ProviderKind.MOCK,
        adapter_ref="mock.local_search",
        provider_id="local_search",
    )
)
```

## Status Atual

Status: `MVP`.

O gateway e registry existem, mas adapters concretos e política de provider ainda precisam de catálogo e testes de contrato.

## Próximos Passos

- Definir catálogo inicial de providers seguros.
- Formalizar tratamento de MCP como provider adapter revisado.

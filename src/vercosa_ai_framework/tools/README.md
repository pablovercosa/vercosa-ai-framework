# Módulo tools

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0009](../../../specs/framework/0009-capabilities-skills-tools.md)

## Objetivo

Executar operações técnicas governadas, com permissões, efeitos e adapters explícitos.

## O Que Este Módulo Faz

- Define perfis, requests e resultados de tool.
- Mantém `ToolRegistry`.
- Valida permissões e efeitos declarados.
- Consulta Guardian quando configurado.
- Executa adapter injetado ou delega para ProviderGateway quando configurado.

## O Que Este Módulo Não Faz

- Não permite que agentes chamem providers diretamente.
- Não deve conter detalhes secretos de provider.
- Não substitui ProviderGateway.
- Não decide política arquitetural por conta própria.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de tool, request e resultado. |
| `registry.py` | `ToolRegistry`. |
| `executor.py` | `ToolExecutor`, adapters e callable adapter. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `ToolProfile`: operação técnica declarada.
- `ToolExecutionRequest`: pedido de execução.
- `ToolExecutionResult`: resultado normalizado.
- `ToolRegistry`: catálogo de tools.
- `ToolAdapter`: contrato abstrato de adapter.
- `CallableToolAdapter`: adapter baseado em callable injetado.
- `ToolExecutor`: executor governado.

## Entradas E Saídas

Entradas:

- `ToolExecutionRequest` com tool, permissões, efeitos e payload.
- Tool registrada e adapter autorizado.

Saídas:

- `ToolExecutionResult` com payload, status, warnings e metadados.

## Dependências Internas

- `../guardian/`: avaliação antes de ações sensíveis.
- `../providers/`: delegação opcional para ProviderGateway.

## Módulos Relacionados

- Acima: [skills](../skills/README.md).
- Abaixo: [providers](../providers/README.md).
- Transversal: [guardian](../guardian/README.md).

## Specs Correspondentes

- [Spec 0009: Capabilities, Skills e Tools](../../../specs/framework/0009-capabilities-skills-tools.md)
- [Spec 0010: Provider Gateway](../../../specs/framework/0010-provider-gateway.md)

## Docs Relacionadas

- [Capabilities, Skills, Tools](../../../docs/capabilities-skills-tools.md)
- [Provider Gateway](../../../docs/provider-gateway.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.tools import ToolProfile, ToolRegistry

registry = ToolRegistry()
registry.register(
    ToolProfile(
        name="Read context",
        version="0.1.0",
        description="Read approved context",
        provider_type="filesystem",
        operation_type="read",
        domain="documentation",
        tool_id="read_context",
    )
)
```

## Status Atual

Status: `MVP`.

Há registry e executor governado mínimos, mas permissões e catálogo de tools ainda precisam ser formalizados.

## Próximos Passos

- Definir matriz inicial de permissões e efeitos.
- Garantir que todos os efeitos concretos passem por ProviderGateway ou adapter governado.

# Módulo core

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0001](../../../specs/framework/0001-framework-foundation.md)

## Objetivo

Fornecer primitivas compartilhadas de identidade e política para os demais módulos do framework.

## O Que Este Módulo Faz

- Define identidade básica do framework.
- Define níveis de política usados como vocabulário comum.
- Mantém conceitos centrais livres de runtime, provider, banco, IDE ou sistema operacional.

## O Que Este Módulo Não Faz

- Não executa missões, workflows ou tarefas.
- Não avalia Guardian Specs.
- Não seleciona modelos.
- Não acessa providers, tools, runtime ou persistência.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `models.py` | Identidade do framework. |
| `policies.py` | Enum de níveis de política. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `FrameworkIdentity`: metadados básicos do framework.
- `PolicyLevel`: vocabulário comum para níveis de política.

## Entradas E Saídas

Entradas:

- Configuração ou chamada Python que precise de identidade ou nível de política.

Saídas:

- Objetos e enums compartilhados por outros módulos.

## Dependências Internas

- Não depende de outros módulos internos relevantes.

## Módulos Relacionados

- Acima: [README principal](../../../README.md).
- Abaixo: [missions](../missions/README.md), [guardian](../guardian/README.md), [model_selection](../model_selection/README.md).

## Specs Correspondentes

- [Spec 0001: Framework Foundation](../../../specs/framework/0001-framework-foundation.md)

## Docs Relacionadas

- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)
- [Estado atual](../../../docs/alignment/current-state.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.core import FrameworkIdentity

identity = FrameworkIdentity()
```

## Status Atual

Status: `MVP`.

O módulo possui primitivas mínimas e estáveis o suficiente para uso interno, mas ainda não representa uma camada completa de domínio.

## Próximos Passos

- Consolidar vocabulário comum quando as fronteiras de Policy Engine, Guardian Engine e Mission Orchestrator forem decididas.

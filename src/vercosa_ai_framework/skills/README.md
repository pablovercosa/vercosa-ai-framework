# Skills Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0009](../../../specs/framework/0009-capabilities-skills-tools.md)

## Objetivo

Representar procedimentos reutilizáveis que implementam capabilities usando tools governadas.

## O Que Este Módulo Faz

- Define perfis, requests e resultados de skill.
- Mantém `SkillRegistry`.
- Seleciona tools compatíveis para uma execução de skill.
- Delega execução concreta ao `ToolExecutor`.

## O Que Este Módulo Não Faz

- Não acessa providers, MCPs, APIs ou bancos diretamente.
- Não transforma provider em capability.
- Não ignora permissões de tools.
- Não substitui CapabilityResolver ou ToolExecutor.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de skill, request e resultado. |
| `registry.py` | `SkillRegistry`. |
| `executor.py` | `SkillExecutor`. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `SkillProfile`: procedimento reutilizável implementando capabilities.
- `SkillExecutionRequest`: pedido de execução de skill.
- `SkillExecutionResult`: resultado normalizado.
- `SkillRegistry`: catálogo de skills.
- `SkillExecutor`: executor que usa tools.
- `SkillToolSelection`: seleção de tool para skill.

## Entradas E Saídas

Entradas:

- `SkillExecutionRequest` e skill registrada.
- Tools disponíveis e permissões declaradas.

Saídas:

- `SkillExecutionResult` com resultado agregado ou erro.

## Dependências Internas

- `../tools/`: execução concreta governada.

## Módulos Relacionados

- Acima: [capabilities](../capabilities/README.md).
- Abaixo: [tools](../tools/README.md).
- Transversal: [guardian](../guardian/README.md).

## Specs Correspondentes

- [Spec 0009: Capabilities, Skills e Tools](../../../specs/framework/0009-capabilities-skills-tools.md)

## Docs Relacionadas

- [Capabilities, Skills, Tools](../../../docs/capabilities-skills-tools.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.skills import SkillProfile, SkillRegistry

registry = SkillRegistry()
registry.register(
    SkillProfile(
        name="Search docs",
        version="0.1.0",
        description="Search documentation through approved tools",
        implemented_capabilities=("search_docs",),
        domain="documentation",
        skill_id="search_docs",
    )
)
```

## Status Atual

Status: `MVP`.

O módulo tem contratos e executor mínimos, mas ainda precisa de catálogo aprovado de skills.

## Próximos Passos

- Definir catálogo inicial de skills.
- Integrar CapabilityResolver -> SkillExecutor como fluxo padrão.

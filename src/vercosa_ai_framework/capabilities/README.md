# Módulo capabilities

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0009](../../../specs/framework/0009-capabilities-skills-tools.md)

## Objetivo

Resolver intenções funcionais abstratas para skills compatíveis e autorizáveis.

## O Que Este Módulo Faz

- Define `CapabilityProfile` e `CapabilityRequest`.
- Mantém registry de capabilities declarativas.
- Resolve capabilities por domínio, permissões, roles e skills candidatas.
- Retorna resultado de resolução com `SkillProfile` declarativa sem executar skills ou tools.
- Oferece `ResolvedCapabilityExecutor` para transformar `CapabilityResolutionResult` em `SkillExecutionRequest` e executar a skill selecionada quando o chamador injeta `SkillExecutor`.

## O Que Este Módulo Não Faz

- Não seleciona outra skill após a resolução.
- Não chama providers, MCPs, APIs, bancos ou runtime.
- Não representa comandos concretos como capabilities.
- Não substitui Guardian ou Policy Engine.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de capability e request. |
| `registry.py` | `CapabilityRegistry`. |
| `resolver.py` | `CapabilityResolver`. |
| `executor.py` | Fronteira `CapabilityExecutor` e implementação `ResolvedCapabilityExecutor`. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `CapabilityProfile`: contrato funcional abstrato.
- `CapabilityRequest`: intenção solicitada por agente ou sistema.
- `CapabilityRegistry`: catálogo declarativo.
- `CapabilityResolver`: resolução para skill compatível.
- `CapabilityResolutionResult`: saída da resolução.
- `CapabilityExecutor`: contrato injetável de alto nível.
- `ResolvedCapabilityExecutor`: ponte Capability resolvida -> SkillExecutionRequest -> SkillExecutor.
- `CapabilityExecutionResult`: saída rastreável da execução de capability.

## Entradas E Saídas

Entradas:

- `CapabilityRequest` com capability, role, domínio e permissões.
- Capabilities registradas e skills disponíveis.

Saídas:

- `CapabilityResolutionResult` com skill selecionada ou erro explícito.
- `CapabilityExecutionResult` quando a execução opcional é acionada pelo chamador.

## Dependências Internas

- Não depende diretamente de providers ou runtime.

## Módulos Relacionados

- Acima: [agents](../agents/README.md).
- Abaixo: [skills](../skills/README.md).
- Transversal: [guardian](../guardian/README.md).

## Specs Correspondentes

- [Spec 0009: Capabilities, Skills e Tools](../../../specs/framework/0009-capabilities-skills-tools.md)

## Docs Relacionadas

- [Capabilities, Skills, Tools](../../../docs/capabilities-skills-tools.md)
- [Integração Task, Agent e Capability](../../../docs/architecture/task-agent-capability-integration.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.capabilities import CapabilityProfile, CapabilityRegistry

registry = CapabilityRegistry()
registry.register(
    CapabilityProfile(
        name="SearchDocs",
        version="0.1.0",
        description="Search approved documentation",
        intent="search documentation",
        domain="documentation",
        capability_id="search_docs",
    )
)
```

## Status Atual

Status: `MVP`.

O módulo tem registry, resolver mínimo e executor de capability resolvida. Participa do caminho integrado Task -> Agent -> Capability -> Skill -> Tool -> Provider Gateway em dry-run quando o Agent Orchestrator recebe `capability_executor` explicitamente. Ele ainda depende de catálogo aprovado para uso real amplo e não chama providers reais.

## Próximos Passos

- Definir catálogo inicial de capabilities.
- Revisar Specs e ADRs afetadas pela integração mínima na missão 0108.

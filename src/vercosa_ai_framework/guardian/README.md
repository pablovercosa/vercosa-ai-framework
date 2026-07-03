# Guardian Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0005](../../../specs/framework/0005-guardian-engine.md)

## Objetivo

Avaliar missões, tasks, comandos e ações sensíveis contra políticas de segurança, risco e governança.

## O Que Este Módulo Faz

- Define ações, severidades, modos, riscos, violações e decisões Guardian.
- Implementa políticas estáticas e contexto de avaliação.
- Fornece `GuardianEngine` determinístico MVP.
- Detecta padrões perigosos como `sudo`, comandos destrutivos, segredos prováveis e alterações globais.

## O Que Este Módulo Não Faz

- Não executa comandos.
- Não edita arquivos.
- Não escolhe modelos.
- Não substitui revisão humana quando política exigir.
- Não resolve completamente a fronteira futura de Policy Engine.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de decisão, risco, modo e violação. |
| `policies.py` | Contratos e políticas estáticas. |
| `engine.py` | `GuardianEngine` MVP. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `GuardianAction`: `allow`, `warn`, `block`, `require_approval`.
- `GuardianSeverity`: severidade de achados.
- `GuardianMode`: modo permissivo, padrão ou estrito.
- `GuardianRiskLevel`: risco agregado.
- `GuardianViolation`: violação detectada.
- `GuardianDecision`: decisão estruturada.
- `GuardianEvaluationContext`: contexto de avaliação.
- `GuardianPolicy`: contrato de política.
- `StaticGuardianPolicy`: política declarativa.
- `GuardianEngine`: avaliador principal.

## Entradas E Saídas

Entradas:

- Contexto de missão, workflow, task, comando, permissões ou metadados.

Saídas:

- `GuardianDecision` com ação, violações, riscos e justificativa.

## Dependências Internas

- `../core/`: vocabulário de política quando aplicável.

## Módulos Relacionados

- Acima: [core](../core/README.md).
- Abaixo: [missions](../missions/README.md), [workflows](../workflows/README.md), [tools](../tools/README.md).
- Transversal: [model_selection](../model_selection/README.md), [runtime](../runtime/README.md).

## Specs Correspondentes

- [Spec 0005: Guardian Engine](../../../specs/framework/0005-guardian-engine.md)
- [Spec 0001: Framework Foundation](../../../specs/framework/0001-framework-foundation.md)

## Docs Relacionadas

- [Guardian Engine](../../../docs/guardian-engine.md)
- [Open Questions](../../../docs/alignment/open-questions.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.guardian import GuardianEngine

guardian = GuardianEngine()
decision = guardian.validate_mission_text("Atualizar documentação")
```

## Status Atual

Status: `MVP`.

O módulo possui avaliação determinística inicial, mas a relação com um Policy Engine mais amplo ainda precisa de ADR ou Spec update.

## Próximos Passos

- Resolver Guardian Engine versus Policy Engine.
- Definir persistência de decisões Guardian.

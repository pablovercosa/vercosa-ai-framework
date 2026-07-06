# Módulo guardian

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0005](../../../specs/framework/0005-guardian-engine.md)

## Objetivo

Avaliar missões, tasks, comandos, ações sensíveis e Context Packages contra políticas de segurança, risco e governança.

## O Que Este Módulo Faz

- Define ações, severidades, modos, riscos, violações e decisões Guardian.
- Implementa políticas estáticas e contexto de avaliação.
- Fornece `GuardianEngine` determinístico MVP.
- Detecta padrões perigosos como `sudo`, comandos destrutivos, segredos prováveis e alterações globais.
- Avalia riscos básicos de `ContextPackage` já produzido pelo Context Router, incluindo rastreabilidade, fonte, warnings, redactions, orçamento, sensibilidade e omissões críticas.

## O Que Este Módulo Não Faz

- Não executa comandos.
- Não edita arquivos.
- Não escolhe modelos.
- Não escolhe, monta, ordena ou reduz contexto.
- Não faz RAG, busca semântica, embeddings, chamadas a LLM, providers, MCPs, APIs ou rede.
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
- `GuardianEngine.evaluate_context_package()`: avaliação determinística inicial de `ContextPackage` sem efeitos externos.

## Entradas E Saídas

Entradas:

- Contexto de missão, workflow, task, comando, permissões ou metadados.
- `ContextPackage` já montado por `context/`, quando o chamador quiser avaliar risco antes de entrega.

Saídas:

- `GuardianDecision` com ação, violações, riscos, limites aplicados, metadados de pacote e justificativa.

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
- [Context Router e Token Budget](../../../docs/context-router-token-budget.md)
- [Perguntas em aberto](../../../docs/alignment/open-questions.md)
- [Mapa de arquitetura](../../../docs/alignment/architecture-map.md)

## Exemplo Mínimo

```python
from vercosa_ai_framework.guardian import GuardianEngine

guardian = GuardianEngine()
decision = guardian.validate_mission_text("Atualizar documentação")
```

Avaliação determinística de pacote de contexto:

```python
from vercosa_ai_framework.guardian import GuardianEngine

decision = GuardianEngine().evaluate_context_package(context_package)
```

O Guardian avalia o pacote recebido. Ele não recupera documentos, não escolhe itens e não chama LLM.

## Status Atual

Status: `MVP`.

O módulo possui avaliação determinística inicial de missões, comandos, ações sensíveis e Context Packages. A avaliação de Context Package é local, testável e não altera o fluxo principal de execução.

## Próximos Passos

- Integrar decisões Guardian ao fluxo de Context Router quando houver chamada governada explícita.
- Definir persistência de decisões Guardian.
- Evoluir políticas declarativas quando o Policy Engine formal existir, sem mover seleção de contexto para o Guardian.

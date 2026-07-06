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
- Recebe opcionalmente um `ResolvedPolicySet` produzido pelo Policy Engine e pode elevar a decisão operacional conforme efeitos resolvidos.

## O Que Este Módulo Não Faz

- Não executa comandos.
- Não edita arquivos.
- Não escolhe modelos.
- Não escolhe, monta, ordena ou reduz contexto.
- Não faz RAG, busca semântica, embeddings, chamadas a LLM, providers, MCPs, APIs ou rede.
- Não substitui revisão humana quando política exigir.
- Não resolve políticas declarativas no lugar do Policy Engine.
- Não chama o Policy Engine e não altera políticas declarativas.

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
- `GuardianEvaluationContext.resolved_policy_set`: entrada opcional para políticas já resolvidas pelo Policy Engine.

## Entradas E Saídas

Entradas:

- Contexto de missão, workflow, task, comando, permissões ou metadados.
- `ContextPackage` já montado por `context/`, quando o chamador quiser avaliar risco antes de entrega.
- `ResolvedPolicySet` opcional, quando o chamador já tiver resolvido políticas declarativas.

Saídas:

- `GuardianDecision` com ação, violações, riscos, limites aplicados, metadados de pacote e justificativa.

Quando recebe `ResolvedPolicySet`, o Guardian continua avaliando ação concreta e risco operacional. A política resolvida apenas participa da decisão como fator de elevação: `allow` não bloqueia por si só, `warn` pode gerar `warn`, `require_approval` pode exigir aprovação, `deny` pode bloquear, e conflitos podem gerar aviso ou aprovação obrigatória conforme severidade.

## Dependências Internas

- `../core/`: vocabulário de política quando aplicável.
- `../policy/`: tipos declarativos para receber `ResolvedPolicySet` opcional, sem chamada reversa ao Policy Engine.

## Módulos Relacionados

- Acima: [core](../core/README.md).
- Abaixo: [missions](../missions/README.md), [workflows](../workflows/README.md), [tools](../tools/README.md).
- Transversal: [model_selection](../model_selection/README.md), [runtime](../runtime/README.md).
- Complementar: [policy](../policy/README.md).

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

Integração inicial com política resolvida:

```python
from vercosa_ai_framework.guardian import GuardianEngine, GuardianEvaluationContext

context = GuardianEvaluationContext(
    mission_id="mission",
    evaluation_type="mission_pre_execution",
    mission_goal="Atualizar documentação com entregáveis e critérios de aceite.",
    resolved_policy_set=resolved_policy_set,
)
decision = GuardianEngine().evaluate(context)
```

O `resolved_policy_set` deve ser produzido fora do Guardian. O Guardian não resolve, carrega ou busca políticas.

## Status Atual

Status: `MVP`.

O módulo possui avaliação determinística inicial de missões, comandos, ações sensíveis, Context Packages e políticas resolvidas recebidas como entrada opcional. A avaliação é local, testável e não altera o fluxo principal de execução.

## Próximos Passos

- Integrar decisões Guardian ao fluxo de Context Router quando houver chamada governada explícita.
- Definir persistência de decisões Guardian.
- Evoluir a interpretação operacional de `ResolvedPolicySet` sem mover resolução declarativa para o Guardian.

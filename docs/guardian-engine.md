# Guardian Engine MVP

O Guardian Engine avalia missões e ações planejadas antes da execução e retorna uma decisão estruturada: `allow`, `warn`, `block` ou `require_approval`.

## Escopo do MVP

- Valida texto de missão antes da execução.
- Detecta comandos perigosos como `rm -rf /`, `mkfs`, `dd` destrutivo, `shutdown` e `reboot`.
- Detecta presença provável de segredos em texto fornecido.
- Detecta uso de `sudo`.
- Detecta alteração provável de configurações globais.
- Aplica modos `strict`, `standard` e `permissive`.
- Não executa comandos.
- Não usa APIs externas.

## Modos

- `strict`: bloqueia `sudo` e alterações de configuração global.
- `standard`: exige aprovação para `sudo` e alterações de configuração global.
- `permissive`: gera warning para `sudo` e alterações de configuração global.

Comandos destrutivos e segredos prováveis são bloqueados em todos os modos.

## Uso

```python
from vercosa_ai_framework.guardian import GuardianEngine, GuardianEvaluationContext, GuardianMode

engine = GuardianEngine()
decision = engine.evaluate(
    GuardianEvaluationContext(
        mission_id="m-1",
        evaluation_type="command_pre_execution",
        guardian_mode=GuardianMode.STANDARD,
        mission_goal="Entregaveis: teste. Criterios de aceite: decisao estruturada.",
        planned_command="sudo apt update",
        spec_refs=("specs/framework/0005-guardian-engine.md",),
    )
)
```

O resultado é um `GuardianDecision` com políticas aplicadas, razões, ações exigidas, avisos, itens bloqueados e alternativas seguras.

## Limites

Este MVP usa regras locais determinísticas. Ele não substitui um scanner de segredos completo, não executa comandos e não integra Runtime Adapters diretamente.

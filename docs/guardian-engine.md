# Guardian Engine MVP

O Guardian Engine avalia missões e ações planejadas antes da execução e retorna uma decisão estruturada: `allow`, `warn`, `block` ou `require_approval`.

## Escopo do MVP

- Valida texto de missão antes da execução.
- Detecta comandos perigosos como `rm -rf /`, `mkfs`, `dd` destrutivo, `shutdown` e `reboot`.
- Detecta presença provável de segredos em texto fornecido.
- Detecta uso de `sudo`.
- Detecta alteração provável de configurações globais.
- Classifica sinais textuais de limite de uso/API, quota, rate limit e billing em mensagens já recebidas de providers ou runtimes.
- Aplica modos `strict`, `standard` e `permissive`.
- Não executa comandos.
- Não usa APIs externas.
- Não consulta billing real e não chama provider externo.

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

## Usage/API Limit Guard

O `Usage/API Limit Guard` inicial classifica mensagens de erro ou log já produzidas por providers e runtimes. Ele é determinístico, case-insensitive e preserva a mensagem original no resultado.

Classificações iniciais:

- `rate_limit`: sinais como `rate limit`, `too many requests`, `requests per minute`, `tokens per minute` ou `429`.
- `quota_exceeded`: sinais como `quota exceeded`, `insufficient quota` ou `daily limit`.
- `billing_limit`: sinais como `billing hard limit`.
- `unknown_usage_limit`: sinais genéricos como `usage limit` ou `usage limit has been reached`.
- `not_usage_limit`: mensagens que não parecem relacionadas a limite de uso/API.

Exemplo:

```python
from vercosa_ai_framework.guardian import detect_usage_limit

detection = detect_usage_limit("HTTP 429: too many requests", origin="runtime")
```

O resultado indica severidade, origem, provider/runtime opcional, ação recomendada, se o worker deve parar com segurança e se uma nova tentativa pode fazer sentido futuramente. Limitações externas de uso, quota, rate limit ou crédito não devem ser confundidas com bug de implementação do framework.

Este guard não consulta billing real, não chama OpenAI, Gemini, Ollama, Claude, OpenCode, MCPs, APIs, rede ou qualquer provider externo. Ele não mascara erros não relacionados; mensagens sem padrão conhecido retornam `not_usage_limit`.

## Limites

Este MVP usa regras locais determinísticas. Ele não substitui um scanner de segredos completo, não executa comandos, não integra Runtime Adapters diretamente e não implementa billing real.

Próximos passos: integrar a detecção a Mission Runner, Task Queue ou scripts de worker somente para diagnóstico e parada segura simples, com testes para garantir que erros não relacionados continuem visíveis como falhas comuns.

# Decisão — OpenCode com OpenAI como runtime inicial

## Data

2026-07-02

## Contexto

O OpenCode estava tentando usar modelos Anthropic como padrão, mas a conta Anthropic estava sem crédito. Também houve tentativa inicial de OpenAI com erro de quota. Após autenticação/conexão via browser, o OpenCode passou a executar com OpenAI corretamente.

## Decisão

Usar OpenAI como provider principal inicial do Vercosa AI Framework dentro do OpenCode.

## Política

- OpenAI será o provider principal para tarefas robustas.
- O modelo leve deve ser explicitamente configurado para evitar chamadas involuntárias ao Anthropic.
- Modelos gratuitos via OpenRouter/GitHub Copilot ficam como fallback.
- Plugins externos continuam desativados até validação individual.
- Toda mudança futura de provider/modelo deve ser registrada em ADR ou decision note.

## Justificativa

O OpenAI ficou funcional no OpenCode após autenticação via browser, enquanto Anthropic falhou por falta de crédito e OpenRouter free apresentou rate limit temporário.

## Estado

Aprovado para runtime inicial.

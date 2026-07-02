# Decisão — Isolar ECC Global do OpenCode

## Data

2026-07-02

## Contexto

O OpenCode falhou com o erro:

default agent "build" is a subagent

A investigação mostrou que o arquivo global ~/.opencode/opencode.json definia default_agent como build, mas o próprio agente build estava configurado como mode: subagent. Também havia plugins globais do oh-my-openagent ativos.

## Decisão

Isolar temporariamente a instalação global ECC em ~/.opencode e manter o runtime do Vercosa AI Framework mínimo, limpo e previsível.

## Justificativa

O framework precisa primeiro funcionar com OpenCode estável antes de reativar agentes, comandos, hooks e plugins externos.

## Política

- Não apagar ECC.
- Mover ECC global para pasta desabilitada com timestamp.
- Desativar plugins globais.
- Usar OpenAI como runtime inicial.
- Reativar recursos ECC futuramente de forma seletiva, testada e registrada em ADR.

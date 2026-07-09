---
name: Relato de bug
about: Relate um problema reproduzível sem expor dados sensíveis.
title: "bug: "
labels: bug
assignees: ""
---

## Antes de relatar

Não inclua secrets, tokens, credenciais, chaves de API, dados pessoais sensíveis, logs não sanitizados ou detalhes exploráveis de vulnerabilidades.

Se o problema envolver vulnerabilidade, bypass de segurança, exposição de credenciais, execução destrutiva ou detalhe explorável, siga [SECURITY.md](../../SECURITY.md) e [docs/security/vulnerability-reporting.md](../../docs/security/vulnerability-reporting.md) em vez de publicar detalhes em issue pública.

## Descrição do problema

Descreva o problema de forma objetiva.

## Comportamento esperado

O que deveria acontecer?

## Comportamento observado

O que aconteceu de fato?

## Passos para reproduzir

1. 
2. 
3. 

## Ambiente

- Sistema operacional:
- Arquitetura:
- Versão do Python:
- Forma de instalação:
- Branch ou commit, se aplicável:

## Logs sanitizados

Inclua apenas trechos mínimos e sanitizados. Use placeholders como `TOKEN_REMOVIDO`, `CREDENCIAL_REMOVIDA` ou `VALOR_SENSIVEL_REMOVIDO`.

```text

```

## Impacto percebido

Explique o impacto para uso local, testes, documentação, missão, batch ou operação.

## Validações já executadas

- [ ] `pytest`
- [ ] `python3 -m compileall src`
- [ ] Outro comando relevante:

## Checklist

- [ ] Li `README.md`.
- [ ] Verifiquei issues existentes, se aplicável.
- [ ] Removi dados sensíveis.
- [ ] Rodei `pytest` quando aplicável.
- [ ] Rodei `python3 -m compileall src` quando aplicável.
- [ ] Anexei apenas logs sanitizados.

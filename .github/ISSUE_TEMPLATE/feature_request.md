---
name: Proposta de melhoria
about: Proponha uma melhoria com escopo, riscos e impacto claros.
title: "melhoria: "
labels: enhancement
assignees: ""
---

## Contexto

Proposta de melhoria não é garantia de implementação. Mudanças relevantes podem exigir missão específica, atualização de Spec, ADR ou decisão explícita.

Novas integrações com providers, runtimes, bancos, RAG, embeddings ou pgvector exigem missão específica e análise de arquitetura, segurança, dados, custos, logs e validações.

## Problema que a melhoria resolve

Qual problema real esta melhoria resolve?

## Solução proposta

Descreva a solução em termos práticos.

## Alternativas consideradas

Liste alternativas avaliadas e por que não são suficientes.

## Impacto arquitetural

Indique módulos, Specs, ADRs, fronteiras ou decisões afetadas.

## Impacto em documentação

Quais READMEs, guias, mapas, docs operacionais ou roadmap precisariam ser atualizados?

## Impacto em testes

Quais testes seriam esperados? `pytest` e `python3 -m compileall src` continuam obrigatórios quando aplicável.

## Riscos

Liste riscos de segurança, governança, manutenção, compatibilidade, portabilidade, custo ou acoplamento.

## Escopo fora da proposta

Declare explicitamente o que esta proposta não pretende fazer.

## Checklist de segurança

- [ ] Não exige secrets em texto claro.
- [ ] Não exige `sudo` sem justificativa.
- [ ] Não reduz validações.
- [ ] Não contorna Policy Engine.
- [ ] Não contorna Guardian Engine.
- [ ] Não executa automação destrutiva sem aprovação.

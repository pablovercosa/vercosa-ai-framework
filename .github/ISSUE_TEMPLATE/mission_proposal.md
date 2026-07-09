---
name: Proposta de missão
about: Proponha uma missão em Markdown para avaliação, sem tratá-la como fila executável.
title: "missão: "
labels: mission
assignees: ""
---

## Aviso inicial

Esta issue é uma proposta de missão, não uma fila executável. Nem toda proposta será enfileirada. Missões executáveis devem ser revisadas, pequenas, uma missão por arquivo e adicionadas a `missions/queue/` somente quando houver decisão apropriada.

## Título da missão

Informe um título curto e rastreável.

## Objetivo

Qual resultado a missão deve entregar?

## Contexto

Explique por que a missão é necessária agora.

## Arquivos obrigatórios para leitura

Liste documentos, Specs, ADRs, módulos, scripts ou guias que devem ser lidos antes da execução.

## Entregáveis

Liste arquivos ou resultados esperados.

## Requisitos

Liste requisitos verificáveis.

## Restrições

Declare o que não pode ser feito, incluindo limites de código, scripts, rede, providers, banco, dependências e Git quando aplicável.

## Critérios de aceite

Liste critérios objetivos e verificáveis.

## Riscos

Indique riscos de segurança, arquitetura, documentação, testes, dados sensíveis, dependências ou operação.

## Testes esperados

- [ ] `pytest`
- [ ] `python3 -m compileall src`
- [ ] Outros testes ou validações:

## Documentação afetada

Liste READMEs, docs de arquitetura, operações, roadmap, Specs ou ADRs que podem precisar de atualização.

## Padrão esperado para missões

- [ ] Escopo claro.
- [ ] Uma missão por arquivo.
- [ ] Restrições explícitas.
- [ ] Critérios de aceite verificáveis.
- [ ] Atualização documental quando aplicável.
- [ ] Testes e `compileall` definidos.
- [ ] Commits em português do Brasil.

## Cuidados operacionais

- [ ] Não usar `git add .`.
- [ ] Não fazer force push.
- [ ] Não acessar rede sem necessidade.
- [ ] Não chamar providers sem missão específica.
- [ ] Não alterar scripts críticos sem testes.

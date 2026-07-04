# Política De Atualização De Documentação

## Objetivo

Definir quando READMEs, docs, Specs e ADRs devem ser revisados durante uma missão.

## Regra Obrigatória

Toda missão que criar, alterar ou expandir funcionalidade deve verificar e, quando necessário, atualizar a documentação relacionada.

Essa revisão é obrigatória mesmo quando a mudança de código for pequena.

## Documentos Que Devem Ser Verificados

- `README.md` principal.
- `README.md` do módulo afetado.
- `docs/architecture/module-index.md`.
- Documentos em `docs/` relacionados ao módulo ou fluxo alterado.
- Specs em `specs/framework/` relacionadas.
- ADRs em `knowledge/decisions/` relacionadas.
- Links relativos entre documentos.

## Quando Atualizar

Atualize a documentação quando a missão:

- criar novo módulo, contrato, adapter, comando, fluxo ou política;
- alterar responsabilidade de módulo existente;
- alterar entrada, saída, status, dependência ou limite conhecido;
- expandir comportamento MVP;
- alterar relação arquitetural entre módulos;
- resolver pergunta em aberto;
- criar ou alterar decisão arquitetural;
- mudar comandos, validações ou exemplos documentados.

## Quando Não Atualizar Conteúdo Funcional

Não documente comportamento como existente quando ele ainda for apenas plano, lacuna ou próximo passo.

Use linguagem explícita:

- `futuro`;
- `pendente`;
- `lacuna`;
- `próximo passo`;
- `decisão em aberto`.

## Checklist De Encerramento De Missão

- O README principal foi revisado quando a mudança afeta visão geral, arquitetura, comandos ou mapa de módulos.
- O README do módulo afetado reflete responsabilidades, limites, arquivos, tipos, entradas, saídas, status e próximos passos.
- O índice de módulos continua navegável e com status correto.
- Docs relacionados não contradizem a Spec ou o código.
- Specs relacionadas foram atualizadas ou a necessidade de atualização foi registrada.
- ADRs relacionadas foram atualizadas ou uma nova ADR foi proposta quando houve decisão arquitetural material.
- Links relativos continuam corretos.
- O texto explicativo está em português do Brasil.

## Pendências

Se houver inconsistência relevante entre Spec, documentação e código, registre em `docs/alignment/open-questions.md` antes de expandir implementação.

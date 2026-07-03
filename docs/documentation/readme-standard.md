# README Standard

## Objetivo

Definir o padrão oficial de `README.md` para o Vercosa AI Framework.

Este padrão existe para tornar cada módulo navegável, rastreável até Specs e claro sobre responsabilidades, limites e estado atual.

## Escopo

Este padrão se aplica a:

- `README.md` principal do repositório;
- `README.md` de módulos em `src/vercosa_ai_framework/`;
- novos módulos documentados em `docs/architecture/module-index.md`.

## Regras Gerais

- Use links relativos.
- Todo README de módulo deve linkar para o [README principal](../../README.md).
- Todo README de módulo deve linkar para a Spec relacionada.
- Todo README de módulo deve linkar para módulos imediatamente acima e abaixo na arquitetura quando existirem.
- Documente o estado real do módulo: `spec`, `contracts`, `MVP`, `experimental` ou `stable`.
- Separe explicitamente o que o módulo faz do que ele não faz.
- Não apresente contratos propostos como implementação estável.
- Não use linguagem de marketing quando uma descrição técnica direta bastar.
- Não duplique Specs completas; referencie-as e resuma apenas o necessário para orientar navegação.
- Se houver inconsistência entre código, Spec e arquitetura, registre em [open-questions](../alignment/open-questions.md).

## Estrutura Obrigatória Para README De Módulo

Cada README de módulo deve conter, nesta ordem:

1. Título com o nome do módulo.
2. Links principais.
3. Objetivo.
4. O que este módulo faz.
5. O que este módulo não faz.
6. Principais arquivos.
7. Principais tipos, classes e funções.
8. Entradas e saídas.
9. Dependências internas.
10. Módulos relacionados.
11. Specs correspondentes.
12. Docs relacionadas.
13. Exemplo mínimo de uso quando fizer sentido.
14. Status atual.
15. Próximos passos.

## Estados Permitidos

| Status | Uso |
| --- | --- |
| `spec` | Existe definição conceitual ou Spec, mas não há contrato implementado suficiente. |
| `contracts` | Existem tipos, portas, adapters abstratos ou registros, mas a integração ainda é parcial. |
| `MVP` | Existe implementação mínima funcional, com limites conhecidos. |
| `experimental` | Existe implementação exploratória sujeita a mudança forte. |
| `stable` | Contrato e comportamento estão consolidados e validados. |

## Regras Para README Principal

O `README.md` principal deve conter:

- identidade do projeto;
- objetivo;
- o que o framework é;
- o que o framework não é;
- princípios centrais;
- estado atual;
- arquitetura resumida;
- mapa de módulos;
- links para Specs, docs e índice de módulos;
- regras de contribuição e documentação;
- aviso explícito de que OpenCode é runtime inicial, não núcleo.

## Regras Para Índice De Módulos

`docs/architecture/module-index.md` deve funcionar como mapa navegável do framework.

Ele deve listar:

- cadeia arquitetural;
- módulo fonte correspondente;
- status;
- Spec relacionada;
- documentação relacionada;
- links para README de cada módulo;
- lacunas arquiteturais relevantes.

## Checklist De Revisão

Antes de concluir documentação de módulo, verifique:

- O README linka para o README principal.
- O README linka para pelo menos uma Spec.
- O README declara o que faz e o que não faz.
- O README não promete comportamento inexistente.
- Os principais arquivos citados existem.
- Os tipos/classes/funções citados existem ou estão marcados como conceituais.
- O status é compatível com o código atual.
- Links relativos resolvem corretamente a partir do arquivo.

# Exemplos Operacionais

Links principais: [README principal](../../README.md) | [Mapa de arquitetura](../alignment/architecture-map.md) | [Arquitetura de Audit/Event Log](../architecture/audit-event-architecture.md) | [Playbook de execução em batch](../operations/batch-execution-playbook.md) | [Checklist pós-batch](../operations/post-batch-validation-checklist.md)

## Objetivo

Este diretório reúne exemplos operacionais iniciais do Vercosa AI Framework. O objetivo é mostrar, com fluxos reais e copiáveis quando possível, como módulos centrais se conectam no estado atual do projeto.

Os exemplos não substituem Specs, testes, README principal, mapas de arquitetura ou playbooks operacionais. Eles ajudam a entender o uso prático do MVP sem prometer integração ainda não implementada.

## Como Ler Os Exemplos

Um exemplo pode misturar quatro tipos de informação:

- Comportamento implementado: existe no código ou nos scripts atuais.
- Contrato existente: existe como tipo, porta, helper ou documentação de módulo, mas pode depender de chamada explícita do consumidor.
- Fluxo operacional atual: existe como procedimento local documentado, geralmente por scripts e diretórios de missão.
- Próximo passo documentado: ainda não existe como comportamento integrado e deve ser tratado como futuro.

## Tipos De Exemplo

- Exemplo executável: contém comandos que podem ser rodados localmente quando os pré-requisitos forem atendidos.
- Exemplo conceitual: descreve a sequência entre módulos sem exigir execução real.
- Exemplo de arquitetura: explica responsabilidades e fronteiras entre componentes.
- Exemplo futuro: registra uma evolução possível, marcada explicitamente como futura ou fora do escopo atual.

## Exemplos Disponíveis

- [Fluxo operacional de missões em batch](mission-batch-operational-flow.md)
- [Fluxo mínimo Mission, Workflow e Task](minimal-mission-workflow-task-flow.md)
- [Fluxo Policy, Context e Guardian](policy-context-guardian-flow.md)
- [Fluxo de diagnóstico da CLI operacional](cli-diagnostics-flow.md)

## Não Substitui

Estes exemplos não substituem:

- [README principal](../../README.md)
- [Mapa de arquitetura](../alignment/architecture-map.md)
- [Índice de módulos](../architecture/module-index.md)
- [Arquitetura de Audit/Event Log](../architecture/audit-event-architecture.md)
- Specs em [specs/framework](../../specs/framework/)
- Testes em [tests](../../tests/)
- [Uso do runner seguro](../operations/safe-runner-usage.md)
- [Playbook de execução em batch](../operations/batch-execution-playbook.md)
- [Checklist de validação pós-batch](../operations/post-batch-validation-checklist.md)

## Regras Para Novos Exemplos

- Escrever em português do Brasil.
- Usar links relativos.
- Declarar claramente o que é implementado, contrato, MVP, integração inicial, futuro ou fora do escopo.
- Não prometer integração ainda não implementada.
- Não transformar exemplo em roadmap completo.
- Não substituir Spec, teste, playbook ou decisão arquitetural.

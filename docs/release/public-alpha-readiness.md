# Checklist De Prontidão Para Alfa Pública

Links principais: [README principal](../../README.md) | [Roadmap](../alignment/roadmap.md) | [Estado atual](../alignment/current-state.md) | [Backlog estratégico](../roadmap/mission-backlog.md) | [Documentação legal](../legal/README.md)

## Objetivo

Este documento é um checklist de preparação documental para uma futura alfa pública do Vercosa AI Framework.

Alfa pública não significa estabilidade de produção, suporte completo, release publicada, pacote distribuído ou adequação para uso crítico. O projeto ainda está em desenvolvimento e possui contratos, MVPs e documentação inicial em evolução.

Este documento não é release notes, não cria versão, não cria tag, não publica pacote e não promete data de alfa.

## Estado Da Documentação Pública

A documentação pública inicial está parcialmente preparada para leitura externa conservadora. O README, guia de instalação, guia de contribuição, documentação legal inicial, arquitetura, operação em batch, exemplos e backlog já existem, mas ainda há pendências relevantes antes de uma release alfa.

O estado atual deve ser lido assim:

- documentação pública preparada: guias e mapas iniciais existem e indicam limites do MVP;
- alfa pública futura: ainda depende de decisões, validações e artefatos de release;
- release publicada: ainda não ocorreu;
- produção: fora do escopo atual;
- recursos futuros: RAG semântico, embeddings, pgvector como adapter real, provider real obrigatório, persistência externa de eventos e internacionalização ainda não devem ser tratados como implementados.

## Checklist De Documentação Mínima

| Item | Status | Observação |
| --- | --- | --- |
| [README.md](../../README.md) | existe | Precisa permanecer enxuto e distinguir MVP, lacunas e futuro. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | existe | Precisa continuar sem prometer processo público maduro de contribuição. |
| `LICENSE` | pendente | Não existe no repositório; a pendência está documentada em [license-notes.md](../legal/license-notes.md). |
| [docs/legal/usage-policy.md](../legal/usage-policy.md) | existe | Precisa continuar explícita sobre ausência de segurança absoluta. |
| [docs/legal/license-notes.md](../legal/license-notes.md) | existe | Registra licença pendente e não substitui revisão jurídica. |
| [docs/getting-started/local-installation.md](../getting-started/local-installation.md) | existe | Não promete PyPI, Docker, banco, provider real ou ambiente único. |
| [docs/architecture/module-index.md](../architecture/module-index.md) | existe | Precisa continuar alinhado aos módulos realmente existentes. |
| [docs/operations/batch-execution-playbook.md](../operations/batch-execution-playbook.md) | existe | Não recomenda execução cega; batch depende de revisão e validação. |
| [docs/operations/post-batch-validation-checklist.md](../operations/post-batch-validation-checklist.md) | existe | Define bloqueios antes de push, novo batch ou retomada. |
| [docs/examples/README.md](../examples/README.md) | existe | Precisa manter exemplos marcados como implementados, conceituais ou futuros. |
| [docs/roadmap/mission-backlog.md](../roadmap/mission-backlog.md) | existe | Deve continuar separado da fila executável `missions/queue/`. |

Legenda de status usada neste checklist: `existe`, `precisa de revisão`, `pendente` e `fora do escopo da alfa atual`.

## Checklist De Consistência

| Verificação | Status | Observação |
| --- | --- | --- |
| O README explica o que é o projeto. | existe | Define VAF como framework de Harness Engineering. |
| O README diferencia implementado e futuro. | existe | Lista lacunas como RAG, embeddings, pgvector, providers reais e persistência externa de eventos. |
| O README aponta para guias principais. | existe | Inclui instalação, contribuição, arquitetura, exemplos, roadmap e este checklist. |
| O guia de instalação não promete PyPI inexistente. | existe | Documenta instalação local em modo desenvolvimento. |
| O guia de contribuição não promete processo público maduro. | existe | Declara processo inicial e conservador. |
| A política de uso não promete segurança absoluta. | existe | Afirma explicitamente que não substitui revisão humana. |
| A documentação legal não faz aconselhamento jurídico. | existe | Mantém licença pendente e necessidade de revisão formal. |
| A documentação operacional não recomenda execução cega. | existe | Batch exige fila revisada, parada na primeira falha e validação. |
| O roadmap não promete funcionalidades futuras como implementadas. | existe | Mantém próximos passos conservadores e lacunas explícitas. |

## Riscos Antes Da Alfa Pública

| Risco ou ausência | Status | Impacto |
| --- | --- | --- |
| Ausência de CI público. | pendente | Validação depende de execução local manual. |
| Ausência de `SECURITY.md`. | pendente | Política pública de reporte de vulnerabilidades ainda não está publicada. |
| Ausência de `CODE_OF_CONDUCT.md`. | pendente | Regras comunitárias públicas ainda não foram definidas. |
| Ausência de templates de issue. | pendente | Reportes públicos podem chegar sem estrutura mínima. |
| Ausência de templates de pull request. | pendente | Revisões públicas podem chegar sem checklist mínimo. |
| Ausência de release/tag. | pendente | Não há marco alfa publicado. |
| Ausência de documentação internacionalizada. | pendente | `README.md` permanece canônico em português do Brasil; `README.en.md` e `README.es.md` são futuros. |
| Ausência de provider real configurado. | pendente | O estado atual não deve ser apresentado como integração real com provider externo. |
| Ausência de RAG semântico. | pendente | Busca semântica e recuperação avançada continuam futuras. |
| Ausência de persistência externa de eventos. | pendente | Audit/Event Log atual é em memória. |
| Ausência de testes de instalação limpa em ambiente novo. | pendente | O guia local ainda precisa ser validado fora do ambiente principal do mantenedor. |

## Decisões Já Tomadas

- Documentação em português do Brasil.
- `README.md` canônico em português do Brasil.
- Internacionalização no final, depois de estabilizar o conteúdo canônico.
- Batch como fluxo operacional padrão quando seguro.
- Execução individual para missões sensíveis, críticas, arquiteturais, incertas, investigativas ou de recuperação.
- OpenCode como runtime/laboratório atual, não núcleo do framework.
- Sem banco por enquanto no fluxo alfa atual.
- Sem RAG por enquanto.
- Sem pgvector por enquanto.
- Sem provider real obrigatório por enquanto.
- Sem persistência externa de eventos por enquanto.

## Pendências Antes De Release Alfa

- Revisar licença final e criar `LICENSE`, se a decisão estiver aprovada.
- Criar `SECURITY.md`.
- Criar `CODE_OF_CONDUCT.md`, se desejado para abertura pública.
- Criar templates de issue.
- Criar template de pull request.
- Criar changelog inicial, quando houver decisão de release.
- Definir versão inicial.
- Testar instalação do zero em ambiente novo.
- Revisar README final de alfa.
- Decidir se `README.en.md` e `README.es.md` serão criados apenas no final.
- Definir modelo de release alfa sem prometer estabilidade de produção.

## Critérios Mínimos Para Considerar Alfa Pública Pronta

Uma alfa pública só deve ser considerada pronta quando todos os critérios mínimos abaixo forem atendidos ou quando uma decisão explícita registrar exceção e risco aceito:

- `README.md` revisado para alfa, sem prometer produção, provider real obrigatório, RAG, embeddings, pgvector, Docker, PyPI ou CI inexistentes.
- Guia de instalação validado em ambiente limpo e documentado como instalação local de desenvolvimento.
- Guia de contribuição revisado para processo público inicial, sem prometer maturidade inexistente.
- Licença final decidida e publicada em `LICENSE` ou pendência tratada antes de distribuição pública.
- Política de uso responsável revisada e alinhada ao estado real do projeto.
- Política pública de segurança criada ou pendência aceita explicitamente antes da abertura.
- Templates de issue e pull request criados ou decisão explícita de adiar registrada.
- Changelog inicial e versão inicial definidos somente quando houver decisão de release.
- Testes locais passam com `pytest`.
- Compilação dos módulos passa com `python3 -m compileall src`.
- Roadmap, backlog e estado atual diferenciam documentação preparada, alfa futura, release publicada e produção.
- Recursos futuros permanecem marcados como futuros, lacunas, próximos passos ou fora do escopo atual.

## Fora Do Escopo Deste Documento

- Criar release.
- Criar tag.
- Publicar pacote.
- Criar changelog de release sem decisão.
- Criar `SECURITY.md`.
- Criar `CODE_OF_CONDUCT.md`.
- Criar templates de issue ou pull request.
- Internacionalizar READMEs.
- Implementar funcionalidades.
- Adicionar dependências.

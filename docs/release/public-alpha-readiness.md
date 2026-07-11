# Checklist De Prontidão Para Alfa Pública

Links principais: [README principal](../../README.md) | [Política de versionamento](versioning-policy.md) | [Política de release](release-policy.md) | [Checklist pré-tag](pre-release-checklist.md) | [Execução local do checklist pré-tag](pre-tag-checklist-execution.md) | [Consolidação local do candidato alfa](alpha-candidate-summary.md) | [Solicitação futura de decisão de tag](tag-decision-request.md) | [Plano da versão alfa](alpha-version-plan.md) | [Notas preliminares da futura alfa](release-notes-alpha.md) | [Diagnóstico local de prontidão alfa](alpha-readiness-diagnostic.md) | [Checklist de instalação limpa](../getting-started/clean-install-checklist.md) | [Registro de validação limpa](clean-install-validation.md) | [Roadmap](../alignment/roadmap.md) | [Estado atual](../alignment/current-state.md) | [Revisão pós-integrações](../architecture/post-integration-architecture-review.md) | [Backlog estratégico](../roadmap/mission-backlog.md) | [Documentação legal](../legal/README.md) | [Política de segurança](../../SECURITY.md) | [Código de conduta](../../CODE_OF_CONDUCT.md)

## Objetivo

Este documento é um checklist de preparação documental para uma futura alfa pública do Vercosa AI Framework.

Alfa pública não significa estabilidade de produção, suporte completo, release publicada, pacote distribuído ou adequação para uso crítico. O projeto ainda está em desenvolvimento e possui contratos, MVPs e documentação inicial em evolução.

Este documento não é release notes, não cria versão, não cria tag, não publica pacote e não promete data de alfa.

A versão alfa planejada está documentada como `0.1.0-alpha.1`, com tag futura planejada `v0.1.0-alpha.1`. Essa definição é apenas documental: a alfa ainda não foi publicada e a tag ainda não foi criada.

## Estado Da Documentação Pública

A documentação pública inicial está parcialmente preparada para leitura externa conservadora. O README, guia de instalação, guia de contribuição, documentação legal inicial, arquitetura, operação em batch, exemplos e backlog já existem, mas ainda há pendências relevantes antes de uma release alfa.

O estado atual deve ser lido assim:

- documentação pública preparada: guias e mapas iniciais existem e indicam limites do MVP;
- alfa pública futura: ainda depende de decisões, validações e artefatos de release;
- release publicada: ainda não ocorreu;
- produção: fora do escopo atual;
- recursos futuros: RAG semântico, embeddings, pgvector como adapter real, provider real obrigatório, persistência externa de eventos, retenção/rotação de eventos e internacionalização ainda não devem ser tratados como implementados.

Diagnóstico local de prontidão alfa executado em 2026-07-11: [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md). Classificação real registrada: `NÃO PRONTO`. Esse diagnóstico não criou tag, não publicou release, não publicou pacote e não substitui revisão humana.

Execução local do checklist pré-tag alfa registrada em 2026-07-11: [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md). Classificação real registrada: `REPROVADO`. A execução local não criou tag, não publicou release, não publicou pacote, não confirmou CI remoto e não substitui autorização humana.

Consolidação local do candidato alfa registrada em [alpha-candidate-summary.md](alpha-candidate-summary.md), com solicitação futura de decisão em [tag-decision-request.md](tag-decision-request.md). Esses documentos são preparatórios: não declaram alfa publicada, não criam tag, não publicam release, não publicam pacote e não substituem autorização explícita.

## Checklist De Documentação Mínima

| Item | Status | Observação |
| --- | --- | --- |
| [README.md](../../README.md) | existe | Precisa permanecer enxuto e distinguir MVP, lacunas e futuro. |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | existe | Precisa continuar sem prometer processo público maduro de contribuição. |
| [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md) | existe | Código de conduta inicial e conservador; canal público para problemas de conduta ainda precisa ser definido antes de abertura pública ampla. |
| [CHANGELOG.md](../../CHANGELOG.md) | existe | Changelog inicial criado com versão alfa planejada documentada, sem tag, release publicada ou promessa de estabilidade. |
| [versioning-policy.md](versioning-policy.md) | existe | Política inicial e conservadora de versionamento. |
| [release-policy.md](release-policy.md) | existe | Política inicial de release manual e explícita, sem tag, release ou pacote automático. |
| [pre-release-checklist.md](pre-release-checklist.md) | existe | Checklist operacional pré-tag; não autoriza release por si só. |
| [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md) | existe | Execução local do checklist pré-tag classificada como `REPROVADO`; bloqueada por `LICENSE` ausente, missão em `running`, Git sujo, `alpha-readiness` `NÃO PRONTO` e CI remoto pendente. |
| [alpha-candidate-summary.md](alpha-candidate-summary.md) | existe | Consolidação local preparatória do candidato alfa; mantém bloqueios e pendências antes da tag. |
| [tag-decision-request.md](tag-decision-request.md) | existe | Solicitação futura de decisão; não autoriza tag por si só. |
| [alpha-version-plan.md](alpha-version-plan.md) | existe | Plano documental para `0.1.0-alpha.1`, sem tag ou release publicada. |
| [release-notes-alpha.md](release-notes-alpha.md) | existe | Release notes alfa preliminares criadas como artefato preparatório; ainda exigem revisão final antes de publicação real. |
| [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md) | existe | Diagnóstico local executado com classificação `NÃO PRONTO`; bloqueado por `LICENSE` ausente, missão em `running`, Git sujo e validação limpa anterior reprovada. |
| [SECURITY.md](../../SECURITY.md) | existe | Política inicial e conservadora; canal público de vulnerabilidades ainda precisa ser definido antes da alfa pública. |
| `LICENSE` | pendente | Não existe no repositório; a pendência está documentada em [license-notes.md](../legal/license-notes.md). |
| [docs/legal/usage-policy.md](../legal/usage-policy.md) | existe | Precisa continuar explícita sobre ausência de segurança absoluta. |
| [docs/legal/license-notes.md](../legal/license-notes.md) | existe | Registra licença pendente e não substitui revisão jurídica. |
| [docs/getting-started/local-installation.md](../getting-started/local-installation.md) | existe | Não promete PyPI, Docker, banco, provider real ou ambiente único. |
| `pyproject.toml` | existe | Empacotamento Python local mínimo para instalação editável, sem pacote publicado e sem promessa de PyPI. |
| [docs/getting-started/clean-install-checklist.md](../getting-started/clean-install-checklist.md) | existe | Checklist documental criado e executado uma vez em cópia temporária local; resultado atual reprovado. |
| [docs/release/clean-install-validation.md](clean-install-validation.md) | existe | Registro factual da validação limpa de 2026-07-10, classificada como `REPROVADO`. |
| [docs/architecture/module-index.md](../architecture/module-index.md) | existe | Precisa continuar alinhado aos módulos realmente existentes. |
| [docs/architecture/post-integration-architecture-review.md](../architecture/post-integration-architecture-review.md) | existe | Consolida arquitetura pós-integrações sem publicar alfa. |
| [docs/operations/batch-execution-playbook.md](../operations/batch-execution-playbook.md) | existe | Não recomenda execução cega; batch depende de revisão e validação. |
| [docs/operations/post-batch-validation-checklist.md](../operations/post-batch-validation-checklist.md) | existe | Define bloqueios antes de push, novo batch ou retomada. |
| [docs/examples/README.md](../examples/README.md) | existe | Precisa manter exemplos marcados como implementados, conceituais ou futuros. |
| [docs/roadmap/mission-backlog.md](../roadmap/mission-backlog.md) | existe | Deve continuar separado da fila executável `missions/queue/`. |
| [.github/ISSUE_TEMPLATE/](../../.github/ISSUE_TEMPLATE/) | existe | Templates iniciais para bug, melhoria, documentação e proposta de missão. |
| [.github/PULL_REQUEST_TEMPLATE.md](../../.github/PULL_REQUEST_TEMPLATE.md) | existe | Template inicial de pull request com escopo, segurança, testes e documentação. |
| [.github/workflows/ci.yml](../../.github/workflows/ci.yml) | existe | CI público mínimo com instalação editável, `pytest`, `docs-links`, diagnóstico não bloqueante `alpha-readiness` e `python -m compileall src`, sem secrets, providers, release ou publicação de pacote. |

Legenda de status usada neste checklist: `existe`, `precisa de revisão`, `pendente` e `fora do escopo da alfa atual`.

## Checklist De Consistência

| Verificação | Status | Observação |
| --- | --- | --- |
| O README explica o que é o projeto. | existe | Define VAF como framework de Harness Engineering. |
| O README diferencia implementado e futuro. | existe | Lista lacunas como RAG, embeddings, pgvector, providers reais e persistência externa de eventos. |
| O README aponta para guias principais. | existe | Inclui instalação, contribuição, arquitetura, exemplos, roadmap e este checklist. |
| O guia de instalação não promete PyPI inexistente. | existe | Documenta instalação local em modo desenvolvimento. |
| O empacotamento local mínimo existe. | existe | `pyproject.toml` usa `setuptools`, pacote em `src/vercosa_ai_framework`, versão PEP 440 `0.1.0a1`, sem dependências runtime e entrypoint local `vaf`. |
| O checklist de instalação limpa foi criado. | existe | Diferencia procedimento documental, execução real do checklist e release alfa. |
| O checklist de instalação limpa foi executado. | precisa de revisão | Execução real em 2026-07-10 foi classificada como `REPROVADO`; a alfa não está pronta. |
| O guia de contribuição não promete processo público maduro. | existe | Declara processo inicial e conservador. |
| A política de uso não promete segurança absoluta. | existe | Afirma explicitamente que não substitui revisão humana. |
| A política inicial de segurança não promete SLA, bug bounty, conformidade regulatória ou segurança absoluta. | existe | Registra limites atuais e pendência de canal público de reporte. |
| A documentação legal não faz aconselhamento jurídico. | existe | Mantém licença pendente e necessidade de revisão formal. |
| A documentação operacional não recomenda execução cega. | existe | Batch exige fila revisada, parada na primeira falha e validação. |
| A CLI operacional diferencia leitura e execução. | existe | `missions` lista arquivos por estado e `batch-summary` resume pós-batch sem mover, executar ou substituir scripts seguros. |
| O roadmap não promete funcionalidades futuras como implementadas. | existe | Mantém próximos passos conservadores e lacunas explícitas. |
| A revisão pós-integrações diferencia implementado, MVP, integração inicial, futuro e fora do escopo. | existe | Ajuda a evitar promessa pública acima do estado real. |
| A estratégia inicial de versionamento está documentada. | existe | Define `0.1.0-alpha.1` como versão planejada, sem publicar release. |
| A política inicial de release está documentada. | existe | Define critérios, bloqueios e etapas manuais sem criar tag, release ou pacote. |
| O checklist pré-tag está documentado. | existe | Define validações mínimas como pré-condição, não como autorização automática. |
| A versão alfa planejada está documentada. | existe | Diferencia versão planejada, tag futura, release GitHub e pacote publicado. |
| Release notes alfa preliminares foram criadas. | existe | Documento preparatório criado, sem declarar alfa publicada e ainda pendente de revisão final. |
| Diagnóstico CLI de prontidão alfa existe. | existe | `python3 -m vercosa_ai_framework.cli.main alpha-readiness` consolida verificações locais mínimas, sem criar tag, release ou pacote e sem substituir revisão humana. |
| Diagnóstico local de prontidão alfa foi executado. | precisa de revisão | Execução registrada em [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md) com classificação `NÃO PRONTO`. |
| Checklist pré-tag local foi executado. | precisa de revisão | Execução registrada em [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md) com classificação `REPROVADO`; não autoriza tag. |
| Validador local de links Markdown existe. | existe | `docs-links` valida links relativos locais, ignora URLs externas sem acessar rede e não promete parser Markdown completo ou validação perfeita de âncoras. |
| CI público mínimo existe. | existe | Valida `pytest`, `python -m vercosa_ai_framework.cli.main docs-links`, executa `alpha-readiness` como diagnóstico não bloqueante e valida `python -m compileall src` em pull requests e pushes para `main`, sem executar missões ou providers. |

## Riscos Antes Da Alfa Pública

| Risco ou ausência | Status | Impacto |
| --- | --- | --- |
| CI público mínimo ainda sem matriz ampla. | precisa de revisão | Existe workflow mínimo com Python 3.11, `pytest` e `compileall`; matriz de múltiplas versões, lint e validação limpa automatizada continuam futuros. |
| Canal público definitivo para reporte de vulnerabilidades. | pendente | `SECURITY.md` existe, mas o canal e o processo público maduro ainda precisam ser definidos antes da alfa pública. |
| Canal público definitivo para problemas de conduta. | pendente | `CODE_OF_CONDUCT.md` existe como política inicial, mas canal público e governança comunitária madura ainda precisam ser definidos antes de abertura pública ampla. |
| Templates de issue iniciais. | existe | Estruturam reportes públicos sem prometer triagem madura ou suporte formal. |
| Template de pull request inicial. | existe | Registra checklist mínimo de escopo, segurança, testes e documentação sem prometer merge ou SLA. |
| Ausência de release/tag. | pendente | Não há marco alfa publicado. |
| Ausência de decisão explícita de release. | pendente | A versão planejada existe documentalmente, mas não autoriza publicação. |
| Ausência de documentação internacionalizada. | pendente | `README.md` permanece canônico em português do Brasil; `README.en.md` e `README.es.md` são futuros. |
| Ausência de provider real configurado. | pendente | O estado atual não deve ser apresentado como integração real com provider externo. |
| Ausência de RAG semântico. | pendente | Busca semântica e recuperação avançada continuam futuras. |
| Ausência de persistência externa de eventos. | pendente | Audit/Event Log atual possui memória e JSONL local opt-in, mas não possui banco, exportador remoto, retenção, rotação ou observabilidade externa. |
| Validação de instalação limpa reprovada. | pendente | A execução real de 2026-07-10 falhou no commit validado. O empacotamento local foi ajustado depois, mas diretórios operacionais vazios ausentes no clone, script de status acoplado ao checkout principal, licença pendente e reexecução aprovada ainda permanecem. |
| Diagnóstico local de prontidão alfa reprovado. | pendente | A execução de 2026-07-11 foi classificada como `NÃO PRONTO` por bloqueios documentados em [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md). |
| Checklist pré-tag local reprovado. | pendente | A execução de 2026-07-11 foi classificada como `REPROVADO` por bloqueios documentados em [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md). |

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
- Persistência local JSONL de eventos auditáveis é opt-in e não substitui retenção, rotação ou observabilidade externa.
- Versão alfa inicial planejada como `0.1.0-alpha.1`, sem release publicada.
- Forma PEP 440 local da alfa planejada como `0.1.0a1` em `pyproject.toml`, sem release publicada e sem pacote publicado.
- Tag futura planejada como `v0.1.0-alpha.1`, sem tag criada nesta fase.
- Política inicial de release criada em [release-policy.md](release-policy.md), sem automatizar publicação.
- Checklist pré-tag criado em [pre-release-checklist.md](pre-release-checklist.md), sem autorização automática.
- Checklist pré-tag local executado e registrado em [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md), com classificação `REPROVADO` e sem autorização automática.
- Release notes alfa preliminares criadas em [release-notes-alpha.md](release-notes-alpha.md), sem publicação de release.
- CI público mínimo com GitHub Actions, sem release, sem publicação de pacote, sem secrets, sem providers externos e sem execução de missões.

## Pendências Antes De Release Alfa

- Revisar licença final e criar `LICENSE`, se a decisão estiver aprovada.
- Definir canal público de reporte de vulnerabilidades e política de disclosure antes da alfa pública.
- Revisar `CODE_OF_CONDUCT.md` e definir canal público para problemas de conduta antes de abertura pública ampla.
- Revisar templates de issue e pull request conforme o processo público amadurecer.
- Manter `CHANGELOG.md` inicial atualizado sem criar release, tag ou versão enquanto não houver decisão explícita.
- Revisar as release notes alfa preliminares antes de qualquer publicação real.
- Corrigir os bloqueios encontrados na validação de instalação limpa e reexecutar o checklist antes da alfa.
- Corrigir ou aceitar explicitamente os bloqueios do diagnóstico local de prontidão alfa registrado em [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md).
- Corrigir ou aceitar explicitamente os bloqueios da execução local do checklist pré-tag registrada em [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md).
- Revisar a consolidação local do candidato alfa em [alpha-candidate-summary.md](alpha-candidate-summary.md).
- Revisar a solicitação futura de decisão de tag em [tag-decision-request.md](tag-decision-request.md) apenas após validação final.
- Reexecutar o checklist pré-tag antes de qualquer tag quando houver novo candidato local.
- Executar `python3 -m vercosa_ai_framework.cli.main alpha-readiness` como diagnóstico auxiliar antes da revisão final, sem tratar resultado como autorização automática.
- Obter autorização explícita para tag e release.
- Executar validação final pós-batch.
- Fazer push manual quando autorizado operacionalmente.
- Confirmar CI remoto após push.
- Manter CI público mínimo passando antes da tag alfa.
- Decidir futuramente se haverá matriz de múltiplas versões de Python, lint e validação limpa automatizada no CI.
- Revisar README final de alfa.
- Decidir explicitamente se e quando criar a tag `v0.1.0-alpha.1`.
- Decidir explicitamente se e quando publicar a release alfa.
- Definir se a alfa terá pacote publicado ou apenas código-fonte.
- Decidir se `README.en.md` e `README.es.md` serão criados apenas no final.
- Definir modelo de release alfa sem prometer estabilidade de produção.

## Critérios Mínimos Para Considerar Alfa Pública Pronta

Uma alfa pública só deve ser considerada pronta quando todos os critérios mínimos abaixo forem atendidos ou quando uma decisão explícita registrar exceção e risco aceito:

- `README.md` revisado para alfa, sem prometer produção, provider real obrigatório, RAG, embeddings, pgvector, Docker, PyPI, matriz ampla de CI ou release inexistente.
- Checklist de instalação limpa criado e executado em ambiente novo, com resultado aprovado ou exceção explicitamente aceita; o resultado atual é `REPROVADO`.
- Links relativos Markdown validados localmente com `python3 -m vercosa_ai_framework.cli.main docs-links`, sem validar URLs externas.
- Prontidão alfa diagnosticada localmente com `python3 -m vercosa_ai_framework.cli.main alpha-readiness`, sabendo que `PRONTO COM RESSALVAS` retorna código `0` e ainda exige revisão humana.
- Guia de contribuição revisado para processo público inicial, sem prometer maturidade inexistente.
- Código de conduta inicial criado e revisado sem prometer governança comunitária madura inexistente.
- Licença final decidida e publicada em `LICENSE` ou pendência tratada antes de distribuição pública.
- Política de uso responsável revisada e alinhada ao estado real do projeto.
- Política pública de segurança criada ou pendência aceita explicitamente antes da abertura.
- Templates de issue e pull request criados e revisados conforme o processo público amadurecer.
- Changelog inicial criado e política inicial de versionamento documentada.
- Versão alfa planejada documentada sem declarar release publicada.
- CI mínimo passando em pull requests ou no commit candidato da branch `main`.
- Testes locais passam com `pytest`.
- Compilação dos módulos passa com `python3 -m compileall src`.
- `git status` limpo no momento da release.
- Decisão explícita de tag e release registrada antes de publicar.
- Roadmap, backlog e estado atual diferenciam documentação preparada, alfa futura, release publicada e produção.
- Recursos futuros permanecem marcados como futuros, lacunas, próximos passos ou fora do escopo atual.

## Fora Do Escopo Deste Documento

- Criar release.
- Criar tag.
- Publicar pacote.
- Criar changelog de release versionado sem decisão.
- Definir canal público de reporte de vulnerabilidades e processo público maduro de segurança.
- Internacionalizar READMEs.
- Implementar funcionalidades.
- Adicionar dependências.

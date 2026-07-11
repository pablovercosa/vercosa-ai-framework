# Consolidação Local Do Candidato Alfa

Este documento consolida localmente o candidato alfa planejado do Vercosa AI Framework. Ele é preparatório e factual.

Este documento não é release, não cria tag, não publica pacote, não confirma CI remoto, não substitui autorização humana e não declara a alfa como publicada.

## Identificação

| Campo | Estado |
| --- | --- |
| Versão planejada | `0.1.0-alpha.1` |
| Tag planejada | `v0.1.0-alpha.1` |
| Estado | planejado, não publicado |
| Release GitHub | não publicada |
| Tag Git | não criada |
| Pacote | não publicado |

## Artefatos De Release Existentes

- Política de versionamento: [versioning-policy.md](versioning-policy.md).
- Plano da alfa: [alpha-version-plan.md](alpha-version-plan.md).
- Política de release: [release-policy.md](release-policy.md).
- Checklist pré-tag: [pre-release-checklist.md](pre-release-checklist.md).
- Release notes alfa preliminares: [release-notes-alpha.md](release-notes-alpha.md).
- Validação de instalação limpa: [clean-install-validation.md](clean-install-validation.md).
- Diagnóstico local de prontidão alfa: [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md).
- Execução local do checklist pré-tag: [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md).

## Artefatos Técnicos Existentes

- Empacotamento Python mínimo em [`../../pyproject.toml`](../../pyproject.toml), com versão PEP 440 `0.1.0a1` para instalação local editável.
- CLI operacional inicial documentada em [`../../src/vercosa_ai_framework/cli/README.md`](../../src/vercosa_ai_framework/cli/README.md).
- Comando `docs-links` para validação local de links Markdown relativos.
- Comando `alpha-readiness` para diagnóstico local de prontidão alfa.
- Persistência local JSONL opt-in de eventos auditáveis.
- CI mínimo em [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml).
- Documentação pública mínima em [README.md](../../README.md), [CONTRIBUTING.md](../../CONTRIBUTING.md), [SECURITY.md](../../SECURITY.md), [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md) e documentos em [`../`](../).

## Classificação Consolidada

| Evidência | Classificação | Efeito conservador |
| --- | --- | --- |
| [clean-install-validation.md](clean-install-validation.md) | `REPROVADO` | Bloqueia aprovação plena da alfa até nova validação aprovada ou exceção explícita com risco aceito. |
| [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md) | `NÃO PRONTO` | Bloqueia avanço direto para tag enquanto os bloqueios persistirem ou não houver exceção explícita. |
| [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md) | `REPROVADO` | Não autoriza tag; exige resolução, nova execução ou decisão explícita proporcional ao risco. |

Essas classificações não foram suavizadas. O candidato alfa local permanece planejado e não publicado.

## Estado Esperado Após O Batch 0091-0100

Após o batch 0091-0100 encerrar fora desta missão, os estados esperados precisam ser confirmados novamente:

- `queue=0`.
- `running=0`.
- `failed=0`.
- `pytest` passando.
- `python3 -m compileall src` passando.
- `git status --short` limpo.
- Push ainda precisará ser feito manualmente.
- CI remoto ainda precisará ser confirmado após o push.

Como esta consolidação ocorre dentro do próprio ciclo de batch, a presença temporária desta missão em `running` não deve ser tratada como bloqueio permanente. Ela continua sendo bloqueio para tag enquanto existir no momento de decisão final.

## Bloqueios

- [clean-install-validation.md](clean-install-validation.md) permanece `REPROVADO`.
- [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md) permanece `NÃO PRONTO`.
- [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md) permanece `REPROVADO`.
- `LICENSE` não existe no repositório atual e a licença final permanece pendente.
- Push do bloco local ainda não foi feito por esta missão.
- CI remoto ainda não foi confirmado após push do bloco.
- Autorização explícita para tag ainda não foi concedida.
- Autorização explícita para release ainda não foi concedida.

## Ressalvas

- As release notes em [release-notes-alpha.md](release-notes-alpha.md) permanecem preliminares.
- A alfa não é adequada para produção e não promete estabilidade, SLA, suporte formal ou compatibilidade de API.
- A publicação em PyPI ainda não foi decidida.
- A internacionalização dos READMEs permanece futura.
- A verificação de secrets registrada anteriormente foi textual e conservadora, não scanner especializado.
- O CI local existe como workflow mínimo, mas a confirmação remota depende de push e execução no GitHub.

## Pendências Antes Da Tag

- Concluir o batch 0091-0100.
- Executar validação final pós-batch.
- Confirmar `queue=0`, `running=0` e `failed=0` após o batch.
- Executar `pytest` e confirmar sucesso.
- Executar `python3 -m compileall src` e confirmar sucesso.
- Executar `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links` e confirmar sucesso.
- Executar `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness` e tratar bloqueios.
- Confirmar `git status --short` limpo.
- Fazer push manual do bloco, se autorizado operacionalmente.
- Confirmar CI remoto após o push.
- Revisar release notes finais.
- Revisar [CHANGELOG.md](../../CHANGELOG.md).
- Confirmar licença e resolver a ausência de `LICENSE` ou registrar exceção explícita compatível com o risco.
- Obter autorização explícita para tag.
- Criar tag em missão específica, somente se autorizada.
- Publicar release em missão específica, somente se autorizada.
- Decidir se haverá pacote publicado ou apenas código-fonte.

## Não Realizado Nesta Etapa

- Nenhuma tag criada.
- Nenhuma release publicada.
- Nenhum pacote publicado.
- Nenhum push feito por esta missão.
- Nenhum deploy.
- Nenhum upload para PyPI.
- Nenhuma internacionalização dos READMEs.
- Nenhuma confirmação de CI remoto.

## Próxima Decisão

A próxima decisão deve ser objetiva: autorizar ou não uma futura missão para criar a tag alfa `v0.1.0-alpha.1`, adiar por bloqueios, resolver ressalvas antes da tag e confirmar CI remoto antes de qualquer tag.

Documento complementar para essa decisão futura: [tag-decision-request.md](tag-decision-request.md).

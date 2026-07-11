# Solicitação Futura De Decisão Sobre Tag Alfa

Este documento prepara uma decisão futura sobre a tag alfa do Vercosa AI Framework.

Este documento não autoriza tag por si só. A tag ainda não foi criada, a release ainda não foi publicada e a decisão depende de autorização explícita do usuário após validação final.

## Identificação

| Campo | Valor |
| --- | --- |
| Versão planejada | `0.1.0-alpha.1` |
| Tag planejada | `v0.1.0-alpha.1` |
| Estado atual | planejado, não publicado |

## Evidências Disponíveis

- Validação de instalação limpa: [clean-install-validation.md](clean-install-validation.md), classificada como `REPROVADO`.
- Diagnóstico local de prontidão alfa: [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md), classificado como `NÃO PRONTO`.
- Checklist pré-tag local: [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md), classificado como `REPROVADO`.
- Release notes preliminares: [release-notes-alpha.md](release-notes-alpha.md).
- Política de release: [release-policy.md](release-policy.md).
- CI mínimo criado em [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml).
- Consolidação local do candidato alfa: [alpha-candidate-summary.md](alpha-candidate-summary.md).

## Condições Mínimas Para Pedir Autorização

- Batch 0091-0100 concluído.
- `queue=0`.
- `running=0`.
- `failed=0`.
- `pytest` passando.
- `python3 -m compileall src` passando.
- `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main docs-links` passando.
- `PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main alpha-readiness` sem bloqueios ou com exceção explícita registrada.
- `git status --short` limpo.
- Push concluído.
- CI remoto confirmado.
- Release notes revisadas.
- [CHANGELOG.md](../../CHANGELOG.md) revisado.
- Ausência de secrets confirmada por revisão proporcional ao risco.
- Licença confirmada, com `LICENSE` resolvido ou exceção explícita registrada antes da publicação pública.

## Perguntas De Decisão

- Autorizar criação da tag `v0.1.0-alpha.1`?
- Publicar release no GitHub após tag?
- Publicar pacote ou manter apenas código-fonte?
- Revisar release notes antes da publicação?
- Internacionalizar READMEs antes ou depois da alfa?

## Opções Possíveis

- Prosseguir para missão de tag, somente após gates finais atendidos e autorização explícita.
- Prosseguir para revisão final de release notes.
- Adiar tag até resolver ressalvas.
- Adiar release e continuar desenvolvimento.
- Publicar apenas código-fonte no GitHub quando autorizado.

## Riscos

- API ainda instável.
- Alfa não pronta para produção.
- CI remoto ainda depende de confirmação após push.
- Release notes ainda preliminares.
- Pacote PyPI ainda não decidido.
- Internacionalização ainda futura.
- `LICENSE` ainda ausente no repositório atual.
- Evidências anteriores registram `REPROVADO` e `NÃO PRONTO`, não aprovação plena.

## Recomendação Conservadora

- Não criar tag antes de push e confirmação do CI remoto.
- Não publicar release sem autorização explícita.
- Não publicar pacote sem missão própria.
- Não tratar este documento, o checklist pré-tag ou a consolidação local como autorização automática.
- Se houver comando futuro de tag, ele deve pertencer a uma missão futura específica e autorizada; não é instrução operacional ativa deste documento.

## Documentos De Apoio

- [alpha-candidate-summary.md](alpha-candidate-summary.md).
- [release-policy.md](release-policy.md).
- [pre-release-checklist.md](pre-release-checklist.md).
- [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md).
- [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md).
- [clean-install-validation.md](clean-install-validation.md).
- [release-notes-alpha.md](release-notes-alpha.md).
- [CHANGELOG.md](../../CHANGELOG.md).

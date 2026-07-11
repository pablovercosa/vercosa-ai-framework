# Política Inicial De Release

Links principais: [CHANGELOG.md](../../CHANGELOG.md) | [Plano da versão alfa](alpha-version-plan.md) | [Notas preliminares da futura alfa](release-notes-alpha.md) | [Prontidão para alfa pública](public-alpha-readiness.md) | [Checklist pré-tag](pre-release-checklist.md) | [Execução local do checklist pré-tag](pre-tag-checklist-execution.md) | [Validação de instalação limpa](clean-install-validation.md) | [SECURITY.md](../../SECURITY.md) | [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Objetivo

Definir uma política inicial, manual e conservadora para decidir quando o Vercosa AI Framework pode preparar uma tag e uma release futura.

Esta política não cria tag, não publica release, não publica pacote, não declara alfa publicada e não promete estabilidade.

## Estado Atual

O projeto ainda não possui release estável. A primeira release prevista é uma alfa, planejada como `0.1.0-alpha.1`, com tag futura planejada `v0.1.0-alpha.1`.

Execução local do checklist pré-tag alfa foi registrada em [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md) com classificação `REPROVADO`. Essa execução local não substitui autorização explícita, não cria tag, não publica release, não publica pacote e não confirma CI remoto. Quando houver push aplicável do bloco atual, o CI remoto deve ser confirmado antes de qualquer missão de tag.

Uma release alfa não significa estabilidade de produção, compatibilidade de API, suporte formal, SLA, hardening completo ou adequação a uso crítico. Ela deve ser tratada como marco inicial para experimentação controlada e revisão pública conservadora.

## Conceitos Que Não Devem Ser Confundidos

| Conceito | Significado nesta fase |
| --- | --- |
| Versão planejada | Intenção documentada, como `0.1.0-alpha.1`; não significa publicação. |
| Tag Git | Referência Git criada explicitamente para marcar um commit; ainda não existe para a alfa. |
| Release GitHub | Página de release publicada no GitHub, normalmente associada a uma tag; ainda não existe para a alfa. |
| Pacote publicado | Distribuição enviada a registry como PyPI; ainda não existe. |
| Changelog | Registro contínuo de mudanças em [CHANGELOG.md](../../CHANGELOG.md); não cria release por si só. |
| Release notes | Texto de publicação de uma release; notas preliminares podem existir como preparação, mas precisam de revisão final antes da publicação real. |
| Branch `main` | Linha de desenvolvimento ativa; estar em `main` não significa release publicada. |
| Produção | Uso operacional estável; está fora do escopo da alfa inicial. |

## Regras De Publicação

- Release é um processo manual e explícito nesta fase.
- Nenhuma tag deve ser criada sem autorização explícita.
- Nenhuma release deve ser publicada sem autorização explícita.
- Nenhum pacote deve ser publicado sem missão específica.
- `VAF_AUTO_PUSH=1` não equivale a release.
- `git push` comum não equivale a release.
- A tag planejada `v0.1.0-alpha.1` não deve ser criada nesta missão.
- Publicação em PyPI é futura e depende de decisão própria.
- Internacionalização dos READMEs continua futura.

## Critérios Mínimos Para Release Alfa

Uma release alfa só deve ser considerada quando todos os critérios abaixo estiverem atendidos ou quando uma exceção for registrada explicitamente com risco aceito:

- `queue=0`.
- `running=0`.
- `failed=0`.
- `git status` limpo.
- `origin/main` sincronizado com `main` local.
- `pytest` passando.
- `python3 -m compileall src` passando.
- CI mínimo passando.
- Links Markdown relativos validados localmente com `python3 -m vercosa_ai_framework.cli.main docs-links`, sem validação de URLs externas.
- Prontidão alfa diagnosticada localmente com `python3 -m vercosa_ai_framework.cli.main alpha-readiness`, sem tratar o comando como autorização automática.
- Validação de instalação limpa executada e aprovada ou aprovada com ressalvas aceitáveis.
- [CHANGELOG.md](../../CHANGELOG.md) atualizado.
- Documentação pública mínima presente.
- [SECURITY.md](../../SECURITY.md) presente.
- [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md) presente.
- Templates de issue e pull request presentes.
- Licença definida ou pendência documentada de forma aceitável.
- Versão planejada documentada em [alpha-version-plan.md](alpha-version-plan.md).
- Riscos conhecidos documentados em [public-alpha-readiness.md](public-alpha-readiness.md), [clean-install-validation.md](clean-install-validation.md) ou documentação equivalente.

## Bloqueios Para Release

Qualquer item abaixo bloqueia tag ou release até correção ou decisão explícita de exceção compatível com o risco:

- Testes falhando.
- `compileall` falhando.
- `failed > 0`.
- Missão presa em `running`.
- Git sujo.
- CI falhando.
- Documentação prometendo recurso inexistente.
- Ausência de [SECURITY.md](../../SECURITY.md).
- Ausência de [CHANGELOG.md](../../CHANGELOG.md).
- Ausência de política de uso.
- Problema de licença não resolvido ou não documentado de forma aceitável.
- Instalação limpa reprovada.
- Secrets expostos.
- Tag ou release sem aprovação explícita.

## Etapas Manuais Recomendadas

1. Revisar status das missões.
2. Validar Git, branch, commits e sincronização com `origin/main`.
3. Rodar `pytest`.
4. Rodar `python3 -m vercosa_ai_framework.cli.main docs-links`.
5. Rodar `python3 -m vercosa_ai_framework.cli.main alpha-readiness` como diagnóstico auxiliar.
6. Rodar `python3 -m compileall src`.
7. Rodar comandos principais da CLI.
8. Revisar [CHANGELOG.md](../../CHANGELOG.md).
9. Revisar esta política, o [checklist pré-tag](pre-release-checklist.md), o [plano alfa](alpha-version-plan.md), as [notas preliminares da futura alfa](release-notes-alpha.md), a [prontidão alfa](public-alpha-readiness.md) e a [validação limpa](clean-install-validation.md).
10. Revisar [SECURITY.md](../../SECURITY.md) e a política de uso.
11. Confirmar CI mínimo passando.
12. Confirmar versão planejada.
13. Obter autorização explícita.
14. Criar tag somente em missão própria autorizada.
15. Publicar release somente em missão própria autorizada, se aprovado.

## Convenção De Tag Planejada

A tag futura planejada para a primeira alfa é:

```text
v0.1.0-alpha.1
```

Esta política apenas documenta a convenção. A tag não deve ser criada nesta missão.

## Release Notes E Pacotes

As [release notes alfa preliminares](release-notes-alpha.md) são artefato preparatório e não publicam a alfa. Release notes finais devem ser revisadas em missão específica antes de qualquer publicação. O [CHANGELOG.md](../../CHANGELOG.md) continua registrando mudanças em `Não publicado` até uma decisão explícita de release.

Publicação em PyPI ou qualquer registry é decisão futura separada. Nenhuma etapa desta política autoriza `twine`, publicação automática, workflow de release ou pacote distribuído.

## Diagnóstico `alpha-readiness`

O comando `python3 -m vercosa_ai_framework.cli.main alpha-readiness` verifica presença documental mínima, diretórios operacionais, contagens de missões e workflow de CI em modo local e somente leitura. Ele pode classificar o estado como `PRONTO`, `PRONTO COM RESSALVAS` ou `NÃO PRONTO`.

Esse comando não autoriza release sozinho. `PRONTO` não cria tag, não publica release, não publica pacote e não dispensa checklist pré-tag, validação limpa, `pytest`, `compileall`, revisão de segurança, revisão humana ou autorização explícita. `PRONTO COM RESSALVAS` retorna código `0` por decisão de uso diagnóstico, mas as ressalvas continuam exigindo avaliação antes de qualquer tag.

# Plano Da Versão Alfa Inicial

Links principais: [README principal](../../README.md) | [Política de versionamento](versioning-policy.md) | [Política de release](release-policy.md) | [Checklist pré-tag](pre-release-checklist.md) | [Checklist de alfa pública](public-alpha-readiness.md) | [Notas preliminares da futura alfa](release-notes-alpha.md) | [Checklist de instalação limpa](../getting-started/clean-install-checklist.md) | [Registro de validação limpa](clean-install-validation.md) | [CHANGELOG.md](../../CHANGELOG.md)

## Objetivo

Registrar a proposta documental da primeira versão alfa planejada do Vercosa AI Framework.

Este plano organiza uma futura release alfa, mas não publica release, não cria tag, não publica pacote, não cria release notes finais e não promete data ou estabilidade.

As notas preliminares da futura alfa estão em [release-notes-alpha.md](release-notes-alpha.md). Elas são artefato preparatório e ainda precisam de revisão final antes de qualquer publicação real.

A política inicial de release está em [release-policy.md](release-policy.md). O checklist operacional pré-tag está em [pre-release-checklist.md](pre-release-checklist.md). Ambos são preparação manual, não publicação.

## Proposta De Versão

| Campo | Valor |
| --- | --- |
| Versão planejada | `0.1.0-alpha.1` |
| Versão PEP 440 para pacote local | `0.1.0a1` |
| Tag futura planejada | `v0.1.0-alpha.1` |
| Status atual | planejada e não publicada |
| Release GitHub | não publicada |
| Tag Git | não criada |
| Pacote PyPI | não publicado |
| Garantia de estabilidade | inexistente nesta fase |

`0.1.0-alpha.1` é uma versão planejada para organizar uma entrega pública inicial. Ela não deve ser tratada como release feita, marco estável, pacote distribuído ou promessa de compatibilidade de API.

O metadado local em `pyproject.toml` usa `0.1.0a1`, forma PEP 440 equivalente para ferramentas Python. Esse metadado prepara instalação editável local e não publica a alfa.

## O Que Já Apoia A Alfa

O projeto já possui artefatos que apoiam a preparação de uma futura alfa pública:

- README principal;
- documentação de Harness Engineering;
- guia de instalação local;
- guia de contribuição;
- política de uso responsável;
- `SECURITY.md`;
- `CODE_OF_CONDUCT.md`;
- templates de issue e pull request;
- `CHANGELOG.md`;
- playbooks operacionais;
- documentação de arquitetura;
- checklist de alfa pública;
- política inicial de release;
- checklist pré-tag;
- release notes alfa preliminares, ainda não finais;
- checklist documental de instalação limpa;
- empacotamento Python local mínimo em `pyproject.toml`, com `setuptools`, descoberta em `src`, versão `0.1.0a1` e entrypoint local `vaf`;
- CI mínimo em GitHub Actions com instalação editável, `pytest` e `python -m compileall src`, sem publicar pacote, criar release, usar secrets, executar missões ou chamar providers;
- registro factual de uma execução de instalação limpa em cópia temporária local, atualmente classificada como `REPROVADO`.

Esses artefatos reduzem risco documental, mas não substituem validação final de release.

## Pendências Antes Da Publicação

Antes de publicar a alfa, ainda é necessário:

- corrigir ou decidir explicitamente os bloqueios encontrados na validação de instalação limpa registrada em [docs/release/clean-install-validation.md](clean-install-validation.md);
- reexecutar o checklist de instalação limpa criado em [docs/getting-started/clean-install-checklist.md](../getting-started/clean-install-checklist.md) com resultado aprovado ou exceção aceita;
- fazer revisão final do README;
- validar links Markdown relativos com `python3 -m vercosa_ai_framework.cli.main docs-links`, sem validar URLs externas;
- manter o CI mínimo passando no commit candidato;
- executar `pytest`;
- executar `python3 -m compileall src`;
- revisar o `CHANGELOG.md`;
- revisar as release notes alfa preliminares;
- executar o checklist pré-tag;
- decidir explicitamente criar a tag;
- decidir explicitamente publicar a release;
- definir se haverá pacote ou apenas código-fonte;
- confirmar licença final se a pendência continuar aplicável;
- garantir `git status` limpo no momento de release.

## Critérios Mínimos De Publicação

A alfa só deve ser considerada publicável quando todos os critérios mínimos abaixo forem atendidos ou quando uma exceção for registrada explicitamente com risco aceito:

- `queue=0`;
- `running=0`;
- `failed=0`;
- `git status` limpo;
- CI mínimo passando;
- `pytest` passando;
- `python3 -m vercosa_ai_framework.cli.main docs-links` passando;
- `python3 -m compileall src` passando;
- documentação mínima presente;
- segurança básica documentada;
- changelog atualizado;
- versão planejada documentada;
- autorização explícita para tag/release.

## Estado Da Validação De Instalação Limpa

A validação real executada em 2026-07-10 no commit `365ea328399495434d3727fcf212f8aaf4ae25f4` foi classificada como `REPROVADO`.

Bloqueios registrados:

- instalação editável offline falhou por ausência local de `hatchling>=1.25` no commit validado; o backend foi ajustado posteriormente para `setuptools`, mas ainda exige nova validação limpa;
- `validate` e `doctor` falharam porque `missions/running` e `missions/failed` não existem no clone limpo;
- `scripts/vaf-status.sh` usa caminho absoluto para o checkout principal e não representa corretamente uma cópia temporária;
- `LICENSE` permanece ausente; o metadado local não deve inventar licença antes da decisão final.

Esse resultado não altera a versão planejada `0.1.0-alpha.1`, não cria tag, não publica release e bloqueia a aprovação da alfa até nova validação ou decisão explícita de exceção.

## Fora Do Escopo Deste Plano

Este plano não cria:

- changelog de release definitivo;
- release notes finais;
- tag Git;
- GitHub Release;
- pacote PyPI;
- promessa de data;
- promessa de estabilidade;
- promessa de compatibilidade de API.

## Próxima Decisão Necessária

A próxima decisão de release deve ocorrer em missão própria, depois de validação local, revisão documental e confirmação explícita sobre tag, release GitHub e forma de distribuição.

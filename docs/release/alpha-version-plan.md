# Plano Da Versão Alfa Inicial

Links principais: [README principal](../../README.md) | [Política de versionamento](versioning-policy.md) | [Checklist de alfa pública](public-alpha-readiness.md) | [Checklist de instalação limpa](../getting-started/clean-install-checklist.md) | [Registro de validação limpa](clean-install-validation.md) | [CHANGELOG.md](../../CHANGELOG.md)

## Objetivo

Registrar a proposta documental da primeira versão alfa planejada do Vercosa AI Framework.

Este plano organiza uma futura release alfa, mas não publica release, não cria tag, não publica pacote, não cria release notes finais e não promete data ou estabilidade.

## Proposta De Versão

| Campo | Valor |
| --- | --- |
| Versão planejada | `0.1.0-alpha.1` |
| Tag futura planejada | `v0.1.0-alpha.1` |
| Status atual | planejada e não publicada |
| Release GitHub | não publicada |
| Tag Git | não criada |
| Pacote PyPI | não publicado |
| Garantia de estabilidade | inexistente nesta fase |

`0.1.0-alpha.1` é uma versão planejada para organizar uma entrega pública inicial. Ela não deve ser tratada como release feita, marco estável, pacote distribuído ou promessa de compatibilidade de API.

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
- checklist documental de instalação limpa.

Esses artefatos reduzem risco documental, mas não substituem validação final de release.

## Pendências Antes Da Publicação

Antes de publicar a alfa, ainda é necessário:

- executar o checklist de instalação limpa criado em [docs/getting-started/clean-install-checklist.md](../getting-started/clean-install-checklist.md);
- registrar o resultado real em [docs/release/clean-install-validation.md](clean-install-validation.md);
- fazer revisão final do README;
- validar links;
- executar `pytest`;
- executar `python3 -m compileall src`;
- revisar o `CHANGELOG.md`;
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
- `pytest` passando;
- `python3 -m compileall src` passando;
- documentação mínima presente;
- segurança básica documentada;
- changelog atualizado;
- versão planejada documentada;
- autorização explícita para tag/release.

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

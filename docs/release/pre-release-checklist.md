# Checklist Pré-Tag

Links principais: [Política de release](release-policy.md) | [Plano da versão alfa](alpha-version-plan.md) | [Notas preliminares da futura alfa](release-notes-alpha.md) | [Prontidão para alfa pública](public-alpha-readiness.md) | [Diagnóstico local de prontidão alfa](alpha-readiness-diagnostic.md) | [Execução local do checklist pré-tag](pre-tag-checklist-execution.md) | [Validação de instalação limpa](clean-install-validation.md) | [CHANGELOG.md](../../CHANGELOG.md) | [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Objetivo

Definir um checklist operacional pré-tag para a futura alfa do Vercosa AI Framework.

Executar este checklist não cria release, não cria tag, não publica pacote e não concede autorização automática. Ele é pré-condição para uma decisão explícita posterior.

Este documento permanece como checklist reutilizável. Uma execução local real foi registrada separadamente em [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md), com classificação `REPROVADO`; esse relatório não transforma este checklist em documento único de execução e não autoriza tag.

## Estado Git

- [ ] Branch atual é `main`.
- [ ] `git status --short` está limpo.
- [ ] `HEAD` local está sincronizado com `origin/main`.
- [ ] Último commit foi revisado.
- [ ] Não há alterações locais pendentes.

## Missões

- [ ] `queue=0`.
- [ ] `running=0`.
- [ ] `failed=0`.
- [ ] `done` está consistente com as missões esperadas.
- [ ] Worker está parado.
- [ ] Logs foram revisados quando aplicável.

## Testes

- [ ] `pytest` passa.
- [ ] `python3 -m vercosa_ai_framework.cli.main docs-links` passa, validando links Markdown relativos locais sem acessar URLs externas.
- [ ] `python3 -m vercosa_ai_framework.cli.main alpha-readiness` executado como diagnóstico auxiliar, com pendências e ressalvas revisadas manualmente.
- [ ] Diagnóstico local de prontidão alfa registrado em [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md) revisado como evidência, sem tratar o relatório como autorização automática.
- [ ] Execução local do checklist pré-tag registrada em [pre-tag-checklist-execution.md](pre-tag-checklist-execution.md) revisada como evidência, sem tratar o relatório como autorização automática.
- [ ] `python3 -m compileall src` passa.
- [ ] Comandos principais da CLI passam.
- [ ] CI GitHub Actions mínimo passa no commit candidato.

## Documentação

- [ ] `README.md` revisado.
- [ ] `CONTRIBUTING.md` revisado.
- [ ] `CHANGELOG.md` atualizado em `Não publicado` ou preparado para missão de release específica.
- [ ] `docs/release/release-notes-alpha.md` revisado como notas preliminares e, se aprovado, preparado para release notes finais em missão específica.
- [ ] `SECURITY.md` presente e atualizado.
- [ ] `CODE_OF_CONDUCT.md` presente.
- [ ] `LICENSE` definido ou pendência explicitamente aceita e documentada.
- [ ] `docs/legal/usage-policy.md` presente.
- [ ] `docs/release/versioning-policy.md` alinhado.
- [ ] `docs/release/alpha-version-plan.md` alinhado.
- [ ] `docs/release/public-alpha-readiness.md` alinhado.
- [ ] `docs/release/alpha-readiness-diagnostic.md` revisado quando existir execução local aplicável.
- [ ] `docs/release/clean-install-validation.md` atualizado com execução real aplicável.
- [ ] Links relativos Markdown validados localmente com `python3 -m vercosa_ai_framework.cli.main docs-links`.

## Segurança

- [ ] Sem secrets em arquivos versionados.
- [ ] Sem tokens em documentação, exemplos, logs ou fixtures.
- [ ] Sem credenciais expostas.
- [ ] Logs revisados e sanitizados quando aplicável.
- [ ] `SECURITY.md` atualizado.
- [ ] Vulnerabilidades conhecidas avaliadas.
- [ ] Política de uso atualizada.

## Empacotamento

- [ ] `pyproject.toml` existe.
- [ ] Instalação local em modo desenvolvimento está documentada.
- [ ] Versão está coerente com o plano alfa.
- [ ] Nenhum pacote foi publicado.

## Validação De Instalação Limpa

- [ ] Checklist de instalação limpa foi criado.
- [ ] Execução real foi registrada.
- [ ] Resultado foi classificado.
- [ ] Ressalvas foram avaliadas.
- [ ] Bloqueios foram resolvidos ou aceitos explicitamente.

## Autorização

- [ ] Há autorização explícita para criar tag.
- [ ] Há autorização explícita para publicar release.
- [ ] Há autorização explícita para publicar pacote, se um dia houver essa decisão.

Sem autorização explícita, pare. Checklist aprovado não equivale a autorização.

## Evidências Recomendadas Antes Da Tag

O diagnóstico local de prontidão alfa em [alpha-readiness-diagnostic.md](alpha-readiness-diagnostic.md) deve ser revisado antes da tag quando existir execução recente. Esse relatório é evidência auxiliar, não gate automático e não autorização de publicação.

Se o relatório estiver classificado como `NÃO PRONTO`, a tag deve permanecer bloqueada até correção dos bloqueios ou decisão explícita de exceção compatível com o risco. Se estiver classificado como `PRONTO COM RESSALVAS`, as ressalvas devem ser avaliadas manualmente antes de qualquer autorização.

## Comandos Sugeridos

Os comandos abaixo são sugestões para execução manual. Eles não devem ser automatizados por este checklist.

```bash
./scripts/vaf-status.sh
git status --short
git log --oneline --decorate -10
pytest
python3 -m vercosa_ai_framework.cli.main docs-links
python3 -m compileall src
python3 -m vercosa_ai_framework.cli.main --help
python3 -m vercosa_ai_framework.cli.main validate
python3 -m vercosa_ai_framework.cli.main doctor
python3 -m vercosa_ai_framework.cli.main missions
python3 -m vercosa_ai_framework.cli.main batch-summary
python3 -m vercosa_ai_framework.cli.main alpha-readiness
```

Use o entrypoint `vaf` somente se o projeto estiver instalado em modo desenvolvimento e esse entrypoint estiver documentado e disponível no ambiente ativo.

## Comandos Fora Deste Checklist

Comandos de tag podem existir em missão futura específica e autorizada, mas não fazem parte da operação desta missão.

Este checklist não inclui `git push --tags`, `gh release create`, `twine upload`, publicação PyPI, criação de release GitHub ou publicação de pacote.

`alpha-readiness` também não inclui essas operações. Ele é somente leitura, retorna `0` para `PRONTO COM RESSALVAS` por ser diagnóstico auxiliar e não substitui os itens manuais deste checklist.

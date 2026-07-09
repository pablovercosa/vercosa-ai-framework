# Política Inicial De Versionamento

Links principais: [CHANGELOG.md](../../CHANGELOG.md) | [Checklist de alfa pública](public-alpha-readiness.md) | [Plano de versão alfa](alpha-version-plan.md) | [Backlog estratégico](../roadmap/mission-backlog.md)

## Objetivo

Definir uma política inicial, conservadora e documental de versionamento para o Vercosa AI Framework.

Esta política prepara o caminho para uma futura alfa pública. Ela não cria release, não cria tag Git, não publica pacote, não define estabilidade de produção e não substitui uma missão específica de release.

## Estado Atual

O projeto ainda não possui release estável publicada. Também não há release alfa publicada, tag de release criada, GitHub Release publicada ou pacote PyPI publicado.

A primeira versão alfa será usada para organizar uma entrega pública inicial e rastreável. Ela não deve ser interpretada como promessa de estabilidade de produção, compatibilidade de API, suporte formal, SLA ou maturidade operacional completa.

Qualquer metadado de versão já existente em arquivo de empacotamento local deve ser tratado com cautela enquanto não houver decisão explícita de release, tag publicada e changelog versionado correspondente.

## Estratégia Conservadora

SemVer pode ser usado como referência prática para nomes de versão, porque oferece uma convenção conhecida e previsível. Nesta fase, porém, a política formal de estabilidade ainda não está madura.

Para versões `0.x` do projeto:

- APIs podem mudar;
- comportamento público pode mudar;
- compatibilidade retroativa ainda não é garantida;
- contratos podem ser ajustados conforme Specs, ADRs, testes e uso real;
- estabilidade de produção não é prometida.

A política formal de estabilidade deve ser amadurecida depois das primeiras alfas, quando os contratos públicos, empacotamento, processo de release e critérios de suporte estiverem mais claros.

## Categorias De Versão

| Categoria | Significado | Exemplo |
| --- | --- | --- |
| Desenvolvimento não publicado | Estado local ou branch sem release formal. Pode conter mudanças ainda não publicadas. | `main` sem tag de release |
| Alfa | Marco público inicial para experimentação controlada, sem promessa de estabilidade. | `0.1.0-alpha.1` |
| Beta futura | Marco futuro para validar APIs e fluxos mais próximos de estabilização. | a definir |
| Estável futura | Linha futura com política explícita de compatibilidade e suporte. | a definir |

## Conceitos Que Não Devem Ser Confundidos

| Conceito | Definição |
| --- | --- |
| Versão planejada | Versão documentada como intenção futura. Não significa publicação. |
| Versão publicada | Versão efetivamente disponibilizada após decisão explícita de release. |
| Tag Git | Referência Git imutável recomendada para apontar um commit de release, como `v0.1.0-alpha.1`. |
| Release GitHub | Página/artefato de release publicado no GitHub, normalmente associada a uma tag. |
| Pacote publicado | Distribuição publicada em registry como PyPI. Não existe nesta fase. |

## Convenção Recomendada Para A Alfa Inicial

A convenção recomendada para a primeira alfa planejada é:

```text
0.1.0-alpha.1
```

A tag futura correspondente deve seguir o padrão previsível:

```text
v0.1.0-alpha.1
```

Esta missão não cria a tag. A tag futura só deve ser criada em uma missão específica de release, depois de validações, revisão documental e autorização explícita.

## Condições Antes Da Publicação Da Alfa

A versão alfa inicial só deve ser publicada depois de:

- documentação pública mínima revisada;
- `SECURITY.md` criado e revisado;
- `CODE_OF_CONDUCT.md` criado e revisado;
- templates de issue e pull request criados;
- `CHANGELOG.md` criado e atualizado;
- checklist de instalação limpa executado;
- `pytest` passando;
- `python3 -m compileall src` passando;
- `git status` limpo;
- decisão explícita de release;
- decisão explícita de criação da tag;
- decisão explícita sobre publicar pacote ou apenas código-fonte;
- licença final resolvida quando a pendência for aplicável.

## Uso Do CHANGELOG

O [CHANGELOG.md](../../CHANGELOG.md) deve continuar registrando mudanças relevantes em `Não publicado` enquanto não houver release formal.

Em futuras versões, mudanças relevantes devem ser agrupadas de forma simples:

- Adicionado;
- Alterado;
- Corrigido;
- Removido;
- Segurança;
- Documentação;
- Operacional.

Uma mudança deve afetar a avaliação de versão quando envolver:

- mudança pública de comportamento;
- mudança de API;
- alteração operacional relevante;
- alteração de segurança;
- alteração em documentação pública de release.

Quando uma release for preparada de fato, o changelog pode receber uma seção versionada e datada somente após decisão explícita. Antes disso, o conteúdo deve permanecer em `Não publicado` para evitar falsa indicação de release concluída.

## Limites Desta Política

Esta política é inicial e intencionalmente simples. Ela não promete compatibilidade que o projeto ainda não sustenta, não cria suporte formal a múltiplas linhas de versão e não define estabilidade para produção.

Regras mais detalhadas devem ser criadas apenas quando houver necessidade concreta, como pacote publicado, usuários externos, APIs públicas estabilizadas, contratos de suporte ou releases recorrentes.

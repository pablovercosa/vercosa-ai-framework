## Resumo

Descreva a mudança de forma objetiva.

## Missão relacionada

Informe a missão, issue, Spec, ADR ou decisão relacionada.

## Tipo de alteração

- [ ] Documentação.
- [ ] Correção.
- [ ] Teste.
- [ ] Implementação com Spec aprovada.
- [ ] Refatoração.
- [ ] Operação ou processo.
- [ ] Outro:

## Arquivos principais alterados

Liste os arquivos mais relevantes.

## Documentação atualizada

Indique o que foi atualizado ou justifique por que não foi necessário.

Documentos a revisar quando aplicável:

- [ ] `README.md`.
- [ ] README do módulo afetado.
- [ ] `docs/architecture/module-index.md`.
- [ ] `docs/alignment/current-state.md`.
- [ ] `docs/roadmap/mission-backlog.md`.
- [ ] `docs/operations/` quando aplicável.

## Testes executados

```text
pytest
```

Resultado:

## Compileall executado

```text
python3 -m compileall src
```

Resultado:

## Impacto arquitetural

Explique impacto em módulos, Specs, ADRs, Policy Engine, Guardian Engine, providers, runtimes, capabilities, skills, tools, contexto, auditoria ou persistência.

## Segurança

- Secrets, tokens e credenciais não foram incluídos.
- Logs foram sanitizados antes de anexar ou citar.
- A mudança não contorna Policy Engine.
- A mudança não contorna Guardian Engine.
- Providers, runtimes, tools, rede, banco ou MCPs não foram acionados sem missão específica.
- Automações destrutivas não foram adicionadas nem executadas sem aprovação explícita.

Observações de segurança:

## Riscos

Liste riscos conhecidos e mitigação, se houver.

## Limitações

Declare limitações, lacunas e comportamento futuro que não está sendo entregue neste PR.

## Próximos passos

Liste próximos passos somente se forem necessários e não fizerem parte deste PR.

## Checklist obrigatório

- [ ] Li `AGENTS.md`.
- [ ] Respeitei o escopo da missão.
- [ ] Não usei `git add .`.
- [ ] Não adicionei dependências sem justificativa.
- [ ] Não alterei scripts críticos sem necessidade.
- [ ] Não expus secrets.
- [ ] Atualizei documentação quando necessário.
- [ ] Rodei `pytest`.
- [ ] Rodei `python3 -m compileall src`.
- [ ] Verifiquei `git status --short`.
- [ ] Mantive documentação e commits em português do Brasil.

PR sem testes executados ou sem justificativa pode precisar de revisão adicional. Este template não promete merge automático nem SLA de revisão.

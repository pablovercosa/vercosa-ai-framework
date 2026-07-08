# Guia Inicial De Contribuição

O Vercosa AI Framework ainda está em desenvolvimento. Este guia descreve um fluxo inicial e conservador para contribuir com segurança, sem prometer um processo público completo ou maduro.

O projeto evolui por missões em Markdown, com escopo claro, referências rastreáveis, validações locais, documentação coerente e commits em português do Brasil.

## Estado Do Projeto

O repositório possui contratos e MVPs iniciais, runners operacionais locais, documentação de instalação, playbooks de batch e validações básicas. Ainda não há release alfa pública, processo público completo de pull requests, templates de issue, templates de pull request, `CODE_OF_CONDUCT.md` ou `SECURITY.md` neste momento.

Recursos como RAG semântico, embeddings, pgvector como adapter real, providers reais obrigatórios, múltiplos runtimes reais e publicação de pacote continuam futuros ou fora do escopo atual, salvo missão específica aprovada.

## Princípios Para Contribuir

- Trabalhe com escopo claro e pequeno.
- Use missão em Markdown para mudanças planejadas.
- Inclua referências obrigatórias a Specs, docs, ADRs, scripts ou módulos relevantes.
- Rode testes e `compileall` antes de considerar a entrega pronta.
- Atualize documentação quando a mudança afetar comportamento, fluxo, arquitetura, comandos, módulos ou roadmap.
- Use commits em português do Brasil.
- Não use `git add .`; faça staging explícito dos arquivos pretendidos.
- Não faça force push.
- Não adicione dependências sem justificativa e sem atualizar os arquivos de configuração aplicáveis.
- Siga a [política inicial de uso responsável](docs/legal/usage-policy.md).

## Fluxo Recomendado

1. Leia o [README principal](README.md).
2. Leia a [instalação local para desenvolvimento](docs/getting-started/local-installation.md).
3. Prepare o ambiente local.
4. Rode as validações iniciais.
5. Escolha uma missão existente ou proponha uma missão pequena.
6. Crie ou revise a missão em Markdown com objetivo, escopo, restrições, referências e critérios de aceite.
7. Execute a missão pelo runner apropriado.
8. Valide testes, `compileall`, documentação e Git.
9. Revise se README, docs, backlog ou roadmap precisam de atualização.
10. Abra pull request futuramente se o fluxo público for adotado.

Comandos mínimos para validar o checkout local:

```bash
pytest
python3 -m compileall src
```

Comandos úteis antes de executar missões:

```bash
./scripts/vaf-status.sh
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main validate
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main doctor
git status --short
```

## Missões Em Markdown

Mudanças relevantes devem partir de uma missão em Markdown. A missão deve declarar:

- objetivo;
- contexto;
- escopo permitido;
- escopo proibido;
- arquivos e documentos de referência;
- entregáveis;
- validações obrigatórias;
- critérios de aceite.

O backlog estratégico em [docs/roadmap/mission-backlog.md](docs/roadmap/mission-backlog.md) orienta planejamento, mas não é fila executável automática. A fila executável deve conter arquivos `.md` pequenos e revisados em `missions/queue/`.

## Execução Individual E Batch

O fluxo operacional padrão interno é batch quando seguro. Mesmo assim, contribuidores devem entender primeiro o runner de uma missão antes de usar batch.

Runner de uma missão:

```bash
./scripts/vaf-run-next-safe.sh
```

Runner em batch:

```bash
VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
```

O batch deve parar na primeira falha. Se uma missão falhar, preserve logs, revise `missions/failed/`, verifique Git, rode validações e não adicione novas missões à fila antes de diagnosticar.

## Quando Usar Execução Individual

Use execução individual quando houver:

- mudança arquitetural sensível;
- alteração em scripts críticos;
- alteração em Guardian, Policy, Context Router, Runtime ou Providers com impacto amplo;
- missão com dependências incertas;
- recuperação após falha;
- investigação de erro;
- limite externo de API, quota, rate limit ou billing recém-ocorrido;
- critérios de aceite fracos ou escopo ainda ambíguo.

## Quando Usar Batch

Use batch somente quando houver:

- bloco revisado;
- missões bem especificadas;
- dependências claras;
- risco baixo ou médio;
- testes estáveis;
- quota disponível quando houver runtime/provider envolvido;
- nenhuma falha recente sem diagnóstico;
- aceitação de revisar commits e documentação depois da execução.

Use `VAF_BATCH_SIZE=3` para validação, retomada, recuperação ou blocos pequenos. Use `VAF_BATCH_SIZE=10` apenas para blocos normais já revisados e seguros.

## Push E Publicação

`VAF_AUTO_PUSH=1` não é padrão. O push automático é opt-in e deve ser usado apenas com decisão explícita.

A prática preferida é fazer push manual depois de validar:

```bash
pytest
python3 -m compileall src
git status --short
git log --oneline --decorate -12
```

Não faça push se houver missão em `running`, missão em `failed`, testes falhando, `compileall` falhando, Git sujo, dúvida sobre a entrega ou documentação incoerente.

## Padrão De Idioma

Use português do Brasil em:

- documentação;
- READMEs;
- missões;
- mensagens de commit;
- textos explicativos de Specs e ADRs.

Termos técnicos arquiteturais podem permanecer em inglês quando forem nomes do projeto ou nomes consolidados, como Context Router, Token Budget Manager, Policy Engine, Guardian Engine, Provider Gateway, Runtime Adapter, Knowledge Hub, Mission Runner, Workflow Engine e Task Queue.

Consulte [docs/documentation/language-and-commit-standard.md](docs/documentation/language-and-commit-standard.md).

## Mensagens De Commit

Mensagens de commit futuras devem usar português do Brasil. Use descrições curtas, rastreáveis e compatíveis com o escopo da missão.

Exemplos:

```text
missão: enfileirar exemplo
implementação: adiciona contrato inicial
docs: atualiza guia operacional
correção: ajusta validação do runner
teste: cobre integração inicial
```

Regras importantes:

- não reescreva histórico publicado;
- não faça force push;
- não misture mudanças fora do escopo da missão;
- não use mensagens em inglês para texto comum;
- mantenha nomes técnicos em inglês apenas quando forem nomes consolidados.

## Testes Obrigatórios

Antes de entregar uma mudança, execute:

```bash
pytest
python3 -m compileall src
```

Falha em qualquer um desses comandos bloqueia entrega, push ou continuação de batch até diagnóstico.

## Documentação Obrigatória

Revise e atualize documentação quando a mudança afetar comportamento, arquitetura, comando, módulo, fluxo operacional, estado do projeto ou planejamento.

Verifique:

- `README.md` principal quando a visão geral, comandos, links ou estado mudarem;
- README do módulo afetado quando responsabilidades, entradas, saídas, status ou limites mudarem;
- `docs/architecture/module-index.md` quando um módulo novo surgir ou o status de módulo mudar;
- roadmap/backlog quando o escopo estratégico mudar;
- docs operacionais quando o fluxo operacional mudar.

Consulte [docs/documentation/documentation-update-policy.md](docs/documentation/documentation-update-policy.md) e [docs/documentation/readme-standard.md](docs/documentation/readme-standard.md).

## Segurança E Limites

- Não registre secrets.
- Não exponha tokens.
- Não inclua credenciais em código, documentação, logs, exemplos ou fixtures.
- Não altere configurações globais.
- Não use `sudo` sem decisão explícita.
- Não acesse rede sem necessidade e sem escopo aprovado.
- Não adicione provider externo sem missão específica.
- Não adicione dependências sem justificativa explícita.
- Não introduza automações destrutivas sem aprovação explícita.
- Não prometa conformidade regulatória, adequação a produção ou segurança absoluta.
- Não implemente RAG, embeddings ou pgvector sem missão específica.
- Não chame providers, MCPs, bancos ou APIs fora do fluxo governado.
- Não transforme ambiente local específico em requisito obrigatório do framework.

## Licença E Uso Responsável

O projeto ainda não possui `LICENSE` final. A decisão de licença está registrada como pendente em [docs/legal/license-notes.md](docs/legal/license-notes.md) e deve ser resolvida antes de uma release pública.

Contribuições devem respeitar a [política inicial de uso responsável](docs/legal/usage-policy.md). Não inclua secrets, credenciais, providers externos, dependências novas ou automações com efeitos destrutivos sem missão específica, justificativa e revisão proporcional ao risco.

## Dependências

- Não adicione dependências sem justificativa.
- Prefira a biblioteca padrão quando possível.
- Documente impacto de dependência nova.
- Atualize arquivos de configuração quando existirem e forem afetados.
- Explique riscos de segurança, manutenção, compatibilidade e portabilidade.

Dependências novas exigem missão específica, critérios de aceite e revisão proporcional ao impacto.

## Pull Requests Futuros

O projeto caminha para uma futura alfa pública, mas este guia não promete um processo público completo de contribuição.

Quando pull requests forem usados, a expectativa inicial será:

- escopo pequeno e rastreável;
- referência à missão ou decisão relacionada;
- testes e `compileall` executados;
- documentação atualizada;
- commits em português do Brasil;
- ausência de secrets, dependências desnecessárias e automações novas sem aprovação.

Templates, regras formais de revisão pública e políticas adicionais podem ser criados em missões futuras.

## Como Reportar Problemas

Enquanto o processo público ainda não estiver maduro, reporte problemas de forma conservadora e objetiva:

- descreva o comportamento observado;
- informe o comportamento esperado;
- inclua comandos executados;
- inclua erro ou trecho relevante de log sem secrets;
- informe sistema operacional, versão do Python e forma de instalação quando relevante;
- indique se há missão em `running` ou `failed`;
- indique se `pytest` e `python3 -m compileall src` passam.

Não publique tokens, chaves, credenciais, logs completos com dados sensíveis ou conteúdo privado de prompts.

## Documentos Relevantes

- [Instalação local para desenvolvimento](docs/getting-started/local-installation.md)
- [Política inicial de uso responsável](docs/legal/usage-policy.md)
- [Notas de licença](docs/legal/license-notes.md)
- [Playbook de execução em batch](docs/operations/batch-execution-playbook.md)
- [Checklist de validação pós-batch](docs/operations/post-batch-validation-checklist.md)
- [Padrão de idioma e commits](docs/documentation/language-and-commit-standard.md)
- [Política de atualização de documentação](docs/documentation/documentation-update-policy.md)
- [Índice de módulos](docs/architecture/module-index.md)
- [Backlog estratégico de missões](docs/roadmap/mission-backlog.md)

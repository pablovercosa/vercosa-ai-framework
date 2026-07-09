# Diretrizes De Convivência E Colaboração

Links principais: [README de conduta](README.md) | [Código de conduta](../../CODE_OF_CONDUCT.md) | [Guia de contribuição](../../CONTRIBUTING.md) | [Política de segurança](../../SECURITY.md) | [Política de uso responsável](../legal/usage-policy.md)

## Objetivo

Oferecer diretrizes práticas para colaboração no Vercosa AI Framework enquanto o projeto ainda está em desenvolvimento e caminha para uma futura alfa pública.

Estas diretrizes complementam o [código de conduta inicial](../../CODE_OF_CONDUCT.md). Elas não criam processo público formal, comitê de moderação, SLA ou governança comunitária madura.

## Prioridades Do Projeto

O projeto prioriza:

- segurança operacional;
- rastreabilidade;
- documentação;
- testes;
- clareza;
- responsabilidade humana sobre automações.

## Discussões Técnicas

Ao abrir uma discussão técnica:

- descreva o problema ou proposta com escopo claro;
- diferencie fato observado, hipótese e sugestão;
- inclua referências a Specs, ADRs, docs, código ou logs sanitizados quando útil;
- evite generalizações sem evidência;
- mantenha foco no comportamento técnico, não em pessoas.

## Propostas De Missão

Ao propor uma missão:

- declare objetivo, contexto, escopo permitido, escopo proibido e critérios de aceite;
- indique validações esperadas, como `pytest` e `python3 -m compileall src` quando aplicável;
- preserve o princípio Specification First para mudanças de código;
- não inclua automações destrutivas, providers externos, rede, banco ou dependências novas sem justificativa explícita;
- mantenha a missão pequena o suficiente para revisão.

## Revisão De Documentação

Ao revisar documentação:

- verifique se o texto está em português do Brasil;
- confirme se links relativos funcionam;
- diferencie implementado, MVP, experimental, futuro, lacuna e decisão pendente;
- evite prometer recursos acima do estado real;
- confira se decisões sensíveis foram registradas no documento adequado.

## Reporte De Bugs

Ao reportar bugs:

- descreva comportamento observado e comportamento esperado;
- informe comandos executados;
- informe ambiente relevante sem expor dados privados;
- inclua trecho de erro ou log sanitizado;
- indique se `pytest` e `python3 -m compileall src` passam quando isso for relevante;
- não publique tokens, credenciais, prompts privados ou logs completos com dados sensíveis.

Vulnerabilidades devem seguir [SECURITY.md](../../SECURITY.md) e [docs/security/vulnerability-reporting.md](../security/vulnerability-reporting.md).

## Discordâncias

Discordâncias devem ser tratadas com:

- argumentos verificáveis;
- testes quando aplicável;
- documentação;
- escopo claro;
- respeito ao padrão do projeto.

Quando uma decisão afetar segurança, arquitetura, governança, release, licença, dados sensíveis ou automações, registre a decisão em Spec, ADR, documentação de alinhamento ou pergunta em aberto antes de tratá-la como padrão.

## Limitações De IA

Contribuições assistidas por IA devem considerar que modelos podem errar, omitir contexto, inventar detalhes ou sugerir comandos perigosos.

Boas práticas:

- revisar saídas antes de aplicar;
- validar alterações com testes e leitura de diff;
- não executar comandos destrutivos sem autorização explícita;
- não tratar resposta de modelo como aprovação de segurança;
- manter responsabilidade humana sobre decisões, automações e publicação de resultados.

## Proteção De Dados Sensíveis

- Não publique secrets, tokens, chaves, credenciais ou dados pessoais.
- Sanitize logs antes de compartilhar.
- Use placeholders como `TOKEN_REMOVIDO` ou `CREDENCIAL_REMOVIDA` em exemplos.
- Evite publicar prompts privados, contexto sensível ou dados de terceiros.
- Não exponha evidências sensíveis em issues públicas.

## Limites Operacionais

Contribuições devem evitar:

- pressa sem validação;
- automação cega;
- promessas acima do implementado;
- exposição de credenciais;
- alterações fora de escopo;
- mudanças destrutivas sem autorização;
- redução de validações sem justificativa;
- bypass de Policy Engine, Guardian Engine ou mecanismos de segurança;
- uso de `git add .` contra o padrão do projeto.

## Relação Com Outras Políticas

- Contribuições devem seguir [CONTRIBUTING.md](../../CONTRIBUTING.md).
- Segurança deve seguir [SECURITY.md](../../SECURITY.md).
- Uso responsável deve seguir [docs/legal/usage-policy.md](../legal/usage-policy.md).
- Problemas de conduta devem seguir [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md), respeitando a pendência de canal público definitivo.

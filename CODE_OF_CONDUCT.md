# Código De Conduta Inicial

O Vercosa AI Framework ainda está em desenvolvimento. Este código de conduta é uma política inicial, simples e conservadora para orientar convivência, contribuição e uso responsável antes de uma abertura pública mais ampla.

Este documento será amadurecido conforme o projeto evoluir. Ele não cria comitê formal, não promete SLA de resposta, não define processo disciplinar maduro e não substitui as políticas de contribuição, segurança ou uso responsável já existentes.

## Documentos Relacionados

- [Guia inicial de contribuição](CONTRIBUTING.md)
- [Política inicial de segurança](SECURITY.md)
- [Política inicial de uso responsável](docs/legal/usage-policy.md)
- [Reporte responsável de vulnerabilidades](docs/security/vulnerability-reporting.md)

## Expectativas De Conduta

Espera-se que participantes, usuários, contribuidores e mantenedores atuem com:

- respeito;
- colaboração;
- boa-fé;
- clareza técnica;
- abertura a revisão;
- responsabilidade com automações;
- cuidado com segurança;
- cuidado com dados sensíveis;
- comunicação objetiva e respeitosa.

Discordâncias técnicas são esperadas em um projeto em desenvolvimento. Elas devem ser tratadas com argumentos verificáveis, testes quando aplicável, documentação adequada, escopo claro e respeito ao padrão do projeto.

## Comportamentos Esperados

- Revisar comandos, missões, automações e efeitos esperados antes de executar.
- Documentar decisões relevantes em Specs, ADRs, documentação de alinhamento ou notas adequadas.
- Aceitar revisão técnica como parte normal do trabalho.
- Reportar problemas com contexto suficiente, comandos executados, resultado observado e resultado esperado.
- Evitar exposição de dados sensíveis, prompts privados, logs não sanitizados, tokens, chaves ou credenciais.
- Respeitar o escopo da missão em andamento.
- Manter commits, documentação, missões e textos explicativos em português do Brasil, conforme o padrão do projeto.
- Preservar rastreabilidade entre missão, decisão, documentação, validação e commit.
- Não reduzir validações, testes, checagens de segurança ou guardrails sem justificativa explícita e revisão proporcional ao risco.

## Comportamentos Não Aceitos

Não são aceitos:

- ataques pessoais;
- assédio;
- discriminação;
- humilhação pública;
- exposição de dados privados;
- publicação de secrets;
- publicação de credenciais;
- uso malicioso do projeto;
- execução destrutiva sem autorização explícita;
- tentativa de burlar Policy Engine, Guardian Engine ou mecanismos de segurança;
- introdução intencional de código perigoso;
- ocultação de riscos relevantes;
- alteração de histórico Git sem autorização;
- force push indevido;
- uso de `git add .` contra o padrão do projeto.

## Segurança, Dados Sensíveis E Automações

O Vercosa AI Framework organiza execução assistida por IA, missões, políticas, validações e automações. Por isso, responsabilidade humana continua necessária antes de executar comandos, aplicar mudanças, chamar ferramentas, acionar providers, processar dados sensíveis ou publicar resultados.

Vulnerabilidades devem seguir a [política inicial de segurança](SECURITY.md) e o guia de [reporte responsável de vulnerabilidades](docs/security/vulnerability-reporting.md). Não publique exploits, tokens, credenciais, dados sensíveis ou detalhes exploráveis em issues públicas antes de análise.

Uso responsável deve seguir a [política inicial de uso responsável](docs/legal/usage-policy.md). O projeto não deve ser usado para automação destrutiva, bypass de políticas, exposição de dados privados ou execução sem revisão humana quando houver risco relevante.

## Decisões Sensíveis

Decisões sensíveis devem ser registradas em documentação adequada antes de serem tratadas como padrão do projeto.

Exemplos de decisões sensíveis incluem mudanças em segurança, governança, licença, release pública, canais de reporte, automações destrutivas, redução de validações, uso de dados sensíveis, providers externos, dependências novas, Policy Engine, Guardian Engine, Runtime Adapter, Provider Gateway, tools ou scripts operacionais.

## Reporte De Problemas De Conduta

O projeto ainda não possui canal público definitivo para problemas de conduta. Esse canal deve ser definido antes de uma abertura pública mais ampla.

Até que esse canal exista:

- trate problemas de conduta com cautela e objetividade;
- não publique dados privados, evidências sensíveis, mensagens privadas, credenciais, tokens ou logs não sanitizados em issues públicas;
- preserve contexto suficiente para revisão futura sem expor pessoas ou dados sensíveis desnecessariamente;
- use documentação pública apenas para relatos que não exponham informações privadas ou riscos de segurança.

Este documento não promete prazo de resposta, comitê formal, mediação formal ou processo disciplinar maduro nesta fase. Esses mecanismos podem ser definidos futuramente, em documentação própria, antes de uma abertura pública mais ampla.

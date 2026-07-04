# Padrão De Idioma E Commits

## Objetivo

Definir o idioma oficial da documentação do Vercosa AI Framework e o padrão obrigatório para mensagens de commit futuras.

## Idioma Oficial

O idioma oficial da documentação do Vercosa AI Framework é português do Brasil.

Esta regra se aplica a:

- `README.md` principal;
- READMEs de módulos;
- documentos em `docs/`;
- textos explicativos de Specs;
- textos explicativos de ADRs;
- missões documentadas;
- políticas, guias, mapas navegáveis e registros de alinhamento.

## Termos Que Podem Permanecer Em Inglês

Podem permanecer em inglês quando forem nomes técnicos, arquiteturais ou de API:

- Context Router;
- Token Budget Manager;
- Policy Engine;
- Guardian Engine;
- Provider Gateway;
- Runtime Adapter;
- Knowledge Hub;
- Model Selection Engine;
- Mission Runner;
- Workflow Engine;
- Task Queue;
- Agent Orchestrator;
- nomes de arquivos, pacotes, classes, funções, enums, comandos e módulos.

## Regras De Tradução

- Traduza texto explicativo, títulos genéricos, descrições e instruções para português do Brasil.
- Não traduza nomes públicos de APIs, classes, funções, enums, pacotes ou arquivos apenas por idioma.
- Não renomeie arquivos existentes sem necessidade forte e decisão explícita.
- Não altere contratos públicos para traduzir nomes técnicos.
- Evite misturar português e inglês na mesma frase, salvo quando o termo em inglês for nome técnico consolidado.

## Mensagens De Commit

A partir da missão que criou este padrão, mensagens de commit futuras devem usar português do Brasil.

O histórico Git já publicado não deve ser reescrito apenas para traduzir mensagens antigas.

## Prefixos Recomendados

- `missão:` para registros ou entregas de missão.
- `docs:` para documentação.
- `arquitetura:` para decisões, mapas e ADRs.
- `implementação:` para código de funcionalidade.
- `teste:` para testes.
- `correção:` para correções.
- `refatoração:` para refatorações.
- `chore:` para manutenção sem impacto funcional direto.

## Exemplos

- `docs: padroniza idioma da documentação`
- `arquitetura: registra decisão sobre Guardian Engine`
- `correção: ajusta validação de missão sem alterar API`

## Restrições

- Não reescrever histórico Git já publicado.
- Não fazer force push para corrigir idioma de commits antigos.
- Não incluir mudanças fora do escopo da missão no commit.
- Não prometer comportamento ainda não implementado na mensagem de commit.

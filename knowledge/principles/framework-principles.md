# Princípios do Vercosa AI Framework

## 1. Specification First

A especificação é a fonte da verdade, independentemente da ferramenta em que foi criada.

A Spec pode vir de:

- Markdown;
- Obsidian;
- OpenSpec;
- GitHub Issues;
- Jira;
- Notion;
- documentos convertidos;
- APIs;
- banco de dados;
- arquivos locais.

Todo formato binário deve ser convertido para Markdown canônico antes do uso.

## 2. AI Native

A IA participa do processo inteiro, não apenas da geração de código.

O usuário escolhe os modelos que deseja usar, mas o framework deve possuir um AI Orchestrator capaz de selecionar, combinar, revisar e alternar modelos conforme tarefa, custo, qualidade e disponibilidade.

## 3. Provider Agnostic

O framework não depende de nenhum provedor.

Tudo deve ser adapter:

- LLM Provider;
- Embedding Provider;
- Knowledge Store;
- Specification Provider;
- IDE Adapter;
- MCP Adapter;
- Execution Provider.

## 4. Local First

O framework deve suportar execução local sempre que possível.

Isso não significa obrigar uso local.

Significa que a arquitetura deve permitir alternativas locais para:

- LLM;
- embeddings;
- banco;
- indexação;
- execução;
- documentação.

## 5. Extensible by Design

Tudo deve ser substituível.

Nenhum provider, modelo, banco, IDE ou sistema operacional deve ser hardcoded.

## 6. Security by Design

Segurança é política global.

Nenhuma entrega pode violar a Guardian Spec de segurança.

## 7. Token Efficiency

O framework deve economizar tokens sem perder qualidade.

Contexto deve ser recuperado com precisão, comprimido semanticamente quando necessário e nunca enviado de forma redundante.

## 8. Governance by Design

O framework deve ter critérios claros de aceite, revisão, qualidade, rastreabilidade e conformidade.

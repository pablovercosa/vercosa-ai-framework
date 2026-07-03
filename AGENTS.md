# Vercosa AI Framework

## Identidade do projeto

O Vercosa AI Framework é um framework open source para desenvolvimento de software orientado por especificações e assistido por IA.

O projeto não é um IDE, não é um MCP, não é um agente e não é apenas uma plataforma. É um framework de engenharia de software que organiza o uso de IA em todo o ciclo de desenvolvimento.

## Objetivo

Permitir que qualquer pessoa desenvolva software orientado por especificações utilizando IA de forma reproduzível, extensível, independente de fornecedor e com liberdade para escolher modelos, IDEs, bancos de dados, mecanismos de busca vetorial, infraestrutura e provedores.

## Princípios centrais

1. Specification First
2. AI Native
3. Provider Agnostic
4. Local First
5. Extensible by Design
6. Security by Design
7. Token Efficiency
8. Governance by Design

## Regra principal

Nenhum código deve ser implementado sem uma Spec aprovada.

## Ambiente atual do usuário

O ambiente principal do usuário atualmente é:

- VPS Oracle
- Ubuntu Server 26.04
- ARM64
- Sem interface gráfica
- Administração via terminal/SSH
- OpenCode instalado
- Ollama instalado
- PostgreSQL 18 instalado
- pgvector habilitado
- Docker instalado
- Bun instalado
- Node instalado
- Python instalado

Apesar disso, o framework deve ser genérico e não pode assumir que todos os usuários usarão a mesma arquitetura.

## Importante

ARM64, PostgreSQL, pgvector, Ollama, systemd e SSH-first são escolhas do ambiente atual do Pablo, mas o framework deve detectar ambiente, arquitetura, sistema operacional e capacidades disponíveis antes de decidir como executar.

## Filosofia

O framework deve ser agnóstico de:

- modelo de IA;
- provedor de IA;
- banco vetorial;
- sistema operacional;
- arquitetura de processador;
- IDE;
- ferramenta de agentes;
- mecanismo de execução;
- formato original de documentos.

## Texto puro como padrão

O framework trabalha internamente com texto estruturado.

Arquivos binários como PDF, DOCX, PPTX, imagens, áudio ou vídeo devem ser convertidos para Markdown canônico antes de serem usados por agentes ou indexados.

Markdown é o formato padrão de troca, versionamento e leitura humana.

## OpenCode

O OpenCode será usado inicialmente como runtime/laboratório de desenvolvimento do framework.

O OpenCode não é o centro do framework. Ele é um adapter/interface.

O framework deve poder suportar futuramente:

- OpenCode
- Claude Code
- Codex CLI
- Cursor
- VS Code
- JetBrains
- Web UI
- API

## Decisão importante

Os agentes não devem conhecer diretamente MCPs, APIs ou bancos.

Agentes devem solicitar capabilities.

Capabilities usam skills.

Skills usam tools.

Tools usam MCPs, providers, bancos ou APIs.

## Hierarquia conceitual

Mission
↓
Mission Orchestrator
↓
Workflow Engine
↓
Task Queue
↓
Agent Orchestrator
↓
Agents
↓
Subagents
↓
Capabilities
↓
Policy Engine
↓
Skills
↓
Tools
↓
Providers / MCPs / APIs

## Missões em vez de prompts

O framework deve evitar depender de prompts gigantes.

O usuário fornece missões.

A missão é decomposta em workflow, tarefas, agentes, loops, validações e entregáveis.

## Loops

Sempre que possível, prompts devem ser substituídos por loops controlados.

Um agente deve operar como máquina de estados:

IDLE
PLANNING
EXECUTING
REFLECTING
VALIDATING
REPLANNING
DONE

Todo loop precisa ter condição de parada.

## Guardian Specs

Existem Specs globais chamadas Guardian Specs.

Elas governam todos os projetos.

Principais Guardian Specs:

1. Security by Design
2. Token Efficiency
3. AI Quality Assurance
4. Cost Optimization
5. Architecture Governance
6. Documentation Governance
7. Testing Governance
8. Compliance Governance
9. Observability Governance

Nenhuma implementação deve violar Guardian Specs.

## Model Selection

O modelo usado em cada tarefa não deve ser hardcoded.

Arquivos podem ter cabeçalhos YAML com políticas de execução.

As Specs definem políticas.

O framework define estratégias.

Os modelos apenas executam.

Exemplo:

---
role: architect
complexity: high
quality: maximum
cost: balanced
reasoning: adaptive
memory: adaptive
provider: auto
model: auto
fallback: true
review: mandatory
security: strict
---

O Model Selection Engine deve consultar os modelos disponíveis no OpenCode e escolher o melhor modelo disponível conforme função, custo, qualidade, raciocínio, contexto, memória e disponibilidade.

Se houver modelo pago adequado, pode usar conforme política.

Se não houver modelo pago, deve usar o melhor modelo gratuito disponível.

## Knowledge Hub

O framework deve possuir um Knowledge Hub.

Camadas:

1. Canonical Documents
2. Semantic Indexes

Tipos de conhecimento:

- Specs
- ADRs
- código
- documentação
- livros
- legislação
- decisões
- conversas
- projetos
- agentes
- skills
- comandos
- hooks

## Code Intelligence

O CodeGraph foi descartado no ambiente atual porque não possui suporte adequado a Linux ARM64.

Será substituído por uma solução própria baseada em:

- PostgreSQL
- pgvector
- Ollama
- nomic-embed-text
- tree-sitter
- MCP próprio

Ferramentas futuras:

- search_code()
- find_usage()
- get_file_context()
- find_similar_code()
- impact_analysis()

## Banco atual

O ambiente atual usa:

- PostgreSQL 18
- pgvector 0.8.1
- modelo de embedding: nomic-embed-text
- dimensão: 768

A tabela code_embeddings precisa usar VECTOR(768).

O script index_code.py atual é protótipo e deve evoluir.

## Repositório ECC

Existe um repositório baixado em:

/home/projetos/ECC

Ele contém agentes, comandos, skills e documentação inspirados no setup vencedor do hackathon da Anthropic.

Esse conteúdo deve ser aproveitado como referência, mas não copiado cegamente.

O framework deve absorver boas ideias e adaptar ao OpenCode e ao Vercosa AI Framework.

## Diretriz para o OpenCode

Ao trabalhar neste projeto:

1. Leia este AGENTS.md primeiro.
2. Leia knowledge/vision.md.
3. Leia knowledge/principles/framework-principles.md.
4. Leia knowledge/architecture/core-architecture.md.
5. Leia as Guardian Specs antes de sugerir implementação.
6. Nunca implemente sem Spec.
7. Se faltar decisão, gere uma pergunta objetiva.
8. Se houver risco arquitetural, proponha ADR.

## Regras de documentação

Toda documentação do framework deve seguir estas regras:

1. Use o padrão oficial em docs/documentation/readme-standard.md para README.md principal, READMEs de módulos e novos mapas navegáveis.
2. Use docs/templates/readme-template.md como base para novos README.md de módulos.
3. Todo README.md de módulo deve linkar para o README.md principal.
4. Todo README.md de módulo deve linkar para a Spec relacionada em specs/framework/.
5. Todo README.md de módulo deve linkar para módulos imediatamente acima e abaixo na arquitetura quando existirem.
6. docs/architecture/module-index.md deve ser mantido como mapa navegável dos módulos do framework.
7. Links devem ser relativos.
8. Documentação deve separar explicitamente objetivo, responsabilidades, não responsabilidades, entradas, saídas, dependências, status e próximos passos.
9. Status permitido para módulos: spec, contracts, MVP, experimental ou stable.
10. Não documente comportamento inexistente como estável.
11. Não use linguagem genérica ou marketing quando houver responsabilidade técnica específica.
12. Se houver inconsistência entre Spec, documentação e código, registre em docs/alignment/open-questions.md antes de expandir implementação.

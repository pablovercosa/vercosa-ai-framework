# Arquitetura Central

## Hierarquia de execução

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

## Conceitos

### Mission

Uma missão é uma intenção de alto nível fornecida pelo usuário ou por outro sistema.

Exemplo:

- criar uma API;
- revisar segurança;
- implementar módulo NF-e;
- criar uma Spec;
- analisar impacto de mudança;
- gerar documentação.

### Mission Orchestrator

Recebe a missão e decide qual workflow deve ser acionado.

### Workflow Engine

Transforma missão em fluxo de trabalho.

### Task Queue

Organiza tarefas, dependências, prioridade, paralelismo e estado.

### Agent Orchestrator

Seleciona agentes adequados para executar tarefas.

### Agents

Executam responsabilidades específicas.

Agentes não devem conhecer MCPs diretamente.

### Subagents

Executam tarefas especializadas e limitadas.

### Capabilities

Representam capacidades abstratas.

Exemplos:

- SearchSpecification
- SearchCode
- GenerateADR
- ValidateSecurity
- OptimizeTokens
- ReviewArchitecture

### Policy Engine

Consulta Guardian Specs e decide se uma ação pode ser executada.

### Skills

Implementam capacidades de forma reutilizável.

### Tools

Ferramentas concretas usadas pelas skills.

### Providers / MCPs / APIs

Camada externa.

Inclui:

- OpenCode;
- PostgreSQL;
- pgvector;
- Ollama;
- GitHub;
- Docker;
- filesystem;
- LLMs;
- embeddings;
- bancos vetoriais;
- navegadores;
- APIs.

## Regra de ouro

Agentes dependem de abstrações, não de implementações.

Isso aplica SOLID ao ecossistema de agentes.

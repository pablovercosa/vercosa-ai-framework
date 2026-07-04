# Posicionamento De Frameworks Externos

## Objetivo

Posicionar frameworks de orquestração externos, runtimes e MCPs em relação ao Vercosa AI Framework.

Regra central: o Vercosa é dono da arquitetura. Frameworks e runtimes externos podem fornecer mecanismos de execução, mas devem permanecer atrás de contratos do Vercosa.

## Resumo

| Tecnologia | Papel no Vercosa | Dependência do core? |
| --- | --- | --- |
| LangGraph | Backend opcional de Workflow Engine ou referência de máquina de estados | Não |
| MetaGPT | Referência opcional de organização de agentes ou adapter | Não |
| AutoGen | Adapter opcional para conversas multiagente | Não |
| OpenCode | Runtime Adapter inicial e laboratório de desenvolvimento | Não |
| Claude Code | Runtime Adapter futuro | Não |
| Codex CLI | Runtime Adapter futuro | Não |
| MCPs | Mecanismos externos de tools/providers atrás de tools e políticas | Não |

## LangGraph

LangGraph pode ser útil para execução em grafo, máquinas de estado, loops controlados e composição de workflows.

Uso aceitável:

- backend opcional atrás de Workflow Engine;
- referência para design explícito de grafo/estado;
- adapter para workflows complexos após estabilização dos contratos de task/workflow do Vercosa.

Uso não aceitável:

- substituir contratos de Mission, Workflow, Task, Policy, Agent, Capability, Skill, Tool ou Provider do Vercosa;
- permitir que nós do grafo chamem tools/providers fora da governança do Vercosa;
- tornar LangGraph dependência obrigatória do core.

Recomendação: não adotar LangGraph no core na próxima onda de implementação. Reavaliar após estabilização de Workflow Engine, Task Queue e contratos de auditoria.

## MetaGPT

MetaGPT pode ser útil como inspiração para equipes de software baseadas em papéis e entregáveis multiagente.

Uso aceitável:

- referência para decomposição por papéis;
- adapter opcional para experimentos com equipes estruturadas de agentes;
- fonte de ideias para perfis de agentes e handoffs de revisão.

Uso não aceitável:

- substituir Agent Orchestrator;
- permitir que agentes MetaGPT chamem tools, MCPs, APIs, providers ou filesystems diretamente;
- contornar Specs, decisões Guardian, validação ou estado de task do Vercosa.

Recomendação: usar MetaGPT apenas como referência até perfis, assignments, capabilities e registros de validação de agentes serem formalizados.

## AutoGen

AutoGen pode ser útil para padrões de conversa multiagente.

Uso aceitável:

- backend opcional para conversas limitadas de subagentes;
- referência para padrões de turnos e colaboração;
- adapter após o Vercosa controlar limites de loop, roteamento de contexto e governança de tools.

Uso não aceitável:

- chats de agentes sem limite;
- chamadas diretas de tools fora de ToolExecutor ou ProviderGateway;
- memória de conversa sem governança;
- seleção de modelo/provider fora do Model Selection Engine.

Recomendação: não adotar AutoGen no core. Considerar depois como adapter se sua execução puder ser restringida por políticas do Vercosa.

## OpenCode

OpenCode é o runtime e ambiente de laboratório inicial.

Uso aceitável:

- implementação de RuntimeAdapter;
- backend de execução local;
- fonte de descoberta de capacidades de runtime/modelos quando encapsulada por adapter;
- laboratório de desenvolvimento para evolução do framework.

Uso não aceitável:

- core do framework;
- policy engine;
- model selection engine;
- Knowledge Hub;
- persistence layer;
- dependência direta de agentes;
- fonte da verdade arquitetural.

Recomendação: continuar usando OpenCode como primeiro RuntimeAdapter, mantendo comportamento específico do OpenCode dentro de `runtime/` ou pacotes de adapter.

## Claude Code E Codex CLI

Claude Code e Codex CLI devem ser tratados como Runtime Adapters futuros.

Eles devem expor as mesmas operações conceituais de outros runtime adapters:

- detectar runtime;
- reportar capabilities;
- preparar execução;
- executar missão ou task;
- coletar logs;
- validar artefatos quando aplicável.

Recomendação: não implementar antes de existirem testes de conformidade de RuntimeAdapter.

## MCPs

MCPs pertencem abaixo de tools/providers, não dentro de agentes.

Posicionamento correto:

```text
Agent
↓
Capability Request
↓
Capability Resolver
↓
Skill Executor
↓
Tool Executor
↓
MCP Tool Adapter or Provider Gateway
↓
MCP Server
```

Regras:

- Agentes não devem conhecer MCP servers diretamente.
- MCPs exigem permissões explícitas.
- Chamadas MCP devem ser auditáveis.
- Saídas de MCP podem conter prompt injection e devem ser tratadas como conteúdo externo.
- MCP servers devem passar por revisão de segurança antes de serem habilitados.

## Critérios De Admissão Para Integrações Externas

Um framework ou runtime externo só deve ser considerado quando:

- couber atrás de contrato de adapter controlado pelo Vercosa;
- suportar mapeamento explícito de estados;
- puder ser auditado;
- puder ser restringido por decisões Guardian;
- respeitar políticas de seleção de modelo e privacidade;
- executar com loops limitados;
- puder ser desabilitado ou substituído;
- não obrigar provedor, modelo, IDE, sistema operacional, vector store ou banco específico.

## Recomendação

Para a próxima onda de implementação, priorizar contratos próprios do Vercosa antes de integrar frameworks externos de orquestração.

OpenCode permanece o único alvo ativo de runtime adapter porque já possui uma fronteira MVP. LangGraph, MetaGPT, AutoGen, Claude Code, Codex CLI e expansão MCP devem aguardar conformidade de adapters, políticas, Context Router e contratos de auditoria.

# Roadmap

## Objetivo Do Roadmap

Recomendar os próximos blocos arquiteturais após o checkpoint de alinhamento atual. Este documento não autoriza implementação por si só.

Nenhum código fonte deve ser implementado apenas com base neste documento. Cada bloco de implementação ainda precisa de Spec aprovada ou atualização explícita de Spec existente.

Backlog operacional detalhado de missões futuras: [Backlog estratégico de missões](../roadmap/mission-backlog.md).

Execução em batch entrou no fluxo operacional como mecanismo controlado para rodar missões já revisadas em `missions/queue/`; o uso seguro está documentado no [playbook de execução em batch](../operations/batch-execution-playbook.md).

A identidade pública do projeto como framework de Harness Engineering para agentes de IA foi incorporada ao `README.md` principal. A internacionalização dos READMEs permanece tarefa futura e não faz parte deste bloco de alinhamento.

## Princípio Orientador

Prefira integrar contratos MVP existentes antes de adicionar novos frameworks, providers, bancos ou comportamentos de agentes.

A próxima fase deve reduzir ambiguidade, não aumentar superfície funcional.

## Bloco 0: Congelamento De Alinhamento

Objetivo: tornar explícita a arquitetura atual antes de nova implementação.

Ações recomendadas:

- Revisar documentos em `docs/alignment/`.
- Confirmar vocabulário de Mission Runner, Mission Orchestrator, Workflow Engine, Task Queue, Agent Orchestrator, Policy Engine, Guardian Engine, Knowledge Hub, Context Router e Semantic Index.
- Identificar conflitos entre código atual, docs MVP e Specs.
- Converter decisões arquiteturais não resolvidas em ADRs.

Critério de saída: a equipe concorda sobre quais componentes são core, adapters e integrações opcionais futuras.

## Bloco 1: Fronteira De Política

Objetivo: resolver Policy Engine versus Guardian Engine.

Saídas recomendadas:

- ADR sobre a fronteira Policy Engine e Guardian Engine.
- Atualização de Specs afetadas quando a decisão alterar terminologia.
- Definição de onde a precedência de políticas é resolvida.

Esta decisão vem primeiro porque afeta missões, tools, providers, runtimes, context routing, seleção de modelos, logs, aprovações e validação.

## Bloco 2: Arquitetura De Contexto

Objetivo: separar memória persistente, Knowledge Hub, Semantic Index e Context Router.

Ações recomendadas:

- Definir Context Router como componente de primeira classe.
- Definir entradas: missão, refs de Spec, task, papel de agente, risco, token budget, decisão de modelo e necessidades de retrieval.
- Definir saídas: pacote de contexto, citações, redactions, warnings e motivos de omissão.
- Definir como Knowledge Hub serve documentos canônicos e resultados de retrieval.
- Definir como Semantic Index apoia retrieval sem virar memória.

Saída recomendada: Spec ou ADR para Context Router e contrato mínimo de retrieval antes de embeddings.

## Bloco 3: Integração Mission-To-Task

Objetivo: conectar MVPs de missão, workflow e task por contratos explícitos.

Ações recomendadas:

- Definir Mission Orchestrator como distinto de Mission Runner.
- Definir saída de Mission Orchestrator como Workflow Plan ou decisão de seleção de workflow.
- Definir handoff de Workflow Engine para Task Queue.
- Definir retorno de estado de Task Queue para Workflow Engine e Mission Runner.

Implementação deve permanecer sequencial até existirem políticas de paralelismo e locks.

## Bloco 4: Integração Task-To-Agent

Objetivo: conectar execução de tasks ao Agent Orchestrator sem dar acesso de infraestrutura a agentes.

Ações recomendadas:

- Definir executor padrão de Task Queue para Agent Orchestrator.
- Definir ciclo de vida de Agent Assignment.
- Definir como agente solicita capabilities.
- Definir como saída de agente vira saída de task, evidência de validação e registro de auditoria.

Guardrail: agentes não devem chamar tools, providers, MCPs, runtime adapters, shell ou bancos diretamente.

## Bloco 5: Integração Capability-To-Provider

Objetivo: tornar o caminho Capabilities -> Skills -> Tools -> Provider Gateway o padrão para efeitos concretos.

Ações recomendadas:

- Definir catálogo essencial de capabilities.
- Definir catálogo essencial de skills.
- Definir tools locais permitidas e modelo de permissões/efeitos.
- Definir eventos de auditoria do Provider Gateway.
- Definir formato de adapter MCP abaixo de tools/providers, não abaixo de agentes.

## Bloco 6: Integração De Persistência

Objetivo: persistir registros críticos por portas antes de adapters específicos de banco.

Ações recomendadas:

- Definir stores para missões, workflows, tasks, decisões Guardian, decisões de modelo, audit logs, documentos canônicos e documentos de conhecimento.
- Usar filesystem adapter como primeira implementação governada.
- Definir registros JSON determinísticos e semântica de hash.
- Definir política de retenção de logs.

Guardrail: não tornar PostgreSQL obrigatório antes de estabilizar portas de persistência.

## Bloco 7: Semantic Index MVP

Objetivo: adicionar retrieval semântico apenas após estabilização dos contratos de Context Router e Knowledge Hub.

Ações recomendadas:

- Definir estratégia de chunking.
- Definir contrato de embedding provider adapter.
- Definir contrato de vector store adapter.
- Definir pgvector como uma implementação possível, não a única.
- Definir embedding local padrão como detecção de capability, não premissa.

Guardrail: busca semântica deve retornar contexto citável e filtrado por política; não deve despejar texto bruto em prompts sem aprovação do Context Router.

## Bloco 8: Expansão De Runtime Adapters

Objetivo: manter OpenCode como runtime inicial enquanto prepara paridade para outros runtimes.

Ações recomendadas:

- Formalizar operações comuns de RuntimeAdapter.
- Definir schema de detecção de capabilities.
- Definir schema de descoberta de modelos.
- Definir schema de resultado de execução.
- Definir testes de conformidade de adapter.

Adapters futuros candidatos: Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.

## Bloco 9: Avaliação De Frameworks Externos

Objetivo: decidir se LangGraph, MetaGPT ou AutoGen devem ser usados como adapters opcionais, referências ou não usados.

Ações recomendadas:

- Avaliar cada framework contra agnosticismo de provider, suporte local-first, máquinas de estado, auditabilidade, footprint de dependências e viabilidade de adapter.
- Mapear cada framework para papéis possíveis: backend de workflow, backend de agent runtime, simulação/referência ou adapter externo.
- Evitar adotar frameworks externos como core antes da estabilização dos contratos do Vercosa.

## Bloco 10: Validação E Governança De Commit

Objetivo: tornar Spec -> Plan -> Tasks -> Implement -> Validate -> Commit aplicável.

Ações recomendadas:

- Definir registros de resultado de validação.
- Definir como testes, checks estáticos, revisão humana, decisões Guardian e revisões por agentes se vinculam a tasks e missões.
- Definir política de auto-commit e comportamento padrão desabilitado.
- Definir como commits referenciam mission IDs, Specs e evidências de validação.

## Ordem Recomendada De Curto Prazo

1. Revisar docs de alinhamento.
2. ADR: Policy Engine versus Guardian Engine.
3. ADR ou Spec: Context Router e arquitetura de memória.
4. ADR ou Spec: fronteira de Mission Orchestrator.
5. Contrato: Mission Runner -> Workflow Engine -> Task Queue.
6. Contrato: Task Queue -> Agent Orchestrator -> Capability Resolver.
7. Testes de contrato para fronteiras MVP existentes.
8. Integração de persistência por filesystem adapter.
9. Design de Semantic Index do Knowledge Hub.
10. Conformidade de Runtime Adapter antes de novos runtimes.

## Trabalho A Evitar Por Enquanto

- Hardcodar LangGraph, MetaGPT ou AutoGen no core.
- Conectar agentes diretamente a MCPs.
- Tornar pgvector obrigatório.
- Tornar Ollama obrigatório.
- Expandir OpenCode para o core de orquestração.
- Adicionar paralelismo multiagente autônomo sem locks, budgets e validação.
- Implementar promessas de memória infinita sem retrieval, retenção e políticas precisas.
- Auto-commit por padrão.
- Adicionar código específico de provider fora de adapters.
- Internacionalizar READMEs antes de estabilizar o conteúdo canônico em português do Brasil.

# Roadmap

## Objetivo Do Roadmap

Recomendar os próximos blocos arquiteturais após o checkpoint de alinhamento atual. Este documento não autoriza implementação por si só.

Nenhum código fonte deve ser implementado apenas com base neste documento. Cada bloco de implementação ainda precisa de Spec aprovada ou atualização explícita de Spec existente.

Backlog operacional detalhado de missões futuras: [Backlog estratégico de missões](../roadmap/mission-backlog.md).

Execução em batch é o fluxo operacional padrão para blocos de missões já revisadas e seguras em `missions/queue/`. O uso seguro está documentado no [playbook de execução em batch](../operations/batch-execution-playbook.md). Execução individual continua sendo o fluxo correto para missões sensíveis, arquiteturais, incertas, investigativas ou de recuperação.

A identidade pública do projeto como framework de Harness Engineering para agentes de IA foi incorporada ao `README.md` principal. A internacionalização dos READMEs permanece tarefa futura e não faz parte deste bloco de alinhamento.

## Princípio Orientador

Prefira integrar contratos MVP existentes antes de adicionar novos frameworks, providers, bancos ou comportamentos de agentes.

A próxima fase deve reduzir ambiguidade, não aumentar superfície funcional.

## Estado Pós-Batch Funcional

O projeto avançou da fase de fundação para uma fase operacional inicial mais coerente. O estado atual considerado por este roadmap inclui:

- Runner seguro de uma missão em `scripts/vaf-run-next-safe.sh`.
- Runner seguro em batch em `scripts/vaf-run-batch-safe.sh`.
- Batch de 3 validado como fluxo de teste, retomada, bloco pequeno e recuperação.
- Batch de 10 funcional para blocos normais revisados e seguros, com ressalva de interrupções por limites externos de API, quota, rate limit ou billing.
- Batch como padrão operacional quando seguro, conforme playbook e checklist operacionais.
- Execução individual preservada para missões críticas, sensíveis, arquiteturais, investigativas, incertas, de recuperação ou de alto risco.
- Policy Engine integrado ao Guardian Engine por `ResolvedPolicySet` opcional.
- Policy Engine integrado ao Context Router por `ResolvedPolicySet` opcional.
- Policy Engine integrado ao Model Selection por políticas resolvidas opcionais.
- Token Budget Manager integrado ao Model Selection por requisitos mínimos de orçamento.
- Usage/API Limit Guard integrado ao fluxo operacional por classificação determinística de logs já produzidos.
- Audit/Event Log inicial em memória, com helpers opcionais para decisões centrais e eventos de missão/batch.
- CLI operacional inicial com `status`, `validate` e `doctor`.
- Exemplos operacionais iniciais em `docs/examples/`.
- Guia inicial de instalação local para desenvolvimento em `docs/getting-started/local-installation.md`.

Esse estado não implica integração real com providers, billing real, observabilidade externa, persistência externa de eventos, RAG semântico, embeddings, pgvector ou Semantic Index.

## Bloco 0: Congelamento De Alinhamento

Objetivo: tornar explícita a arquitetura atual antes de nova implementação.

Ações recomendadas:

- Revisar documentos em `docs/alignment/`.
- Confirmar vocabulário de Mission Runner, Mission Orchestrator, Workflow Engine, Task Queue, Agent Orchestrator, Policy Engine, Guardian Engine, Knowledge Hub, Context Router e Semantic Index.
- Identificar conflitos entre código atual, docs MVP e Specs.
- Converter decisões arquiteturais não resolvidas em ADRs.

Critério de saída: a equipe concorda sobre quais componentes são core, adapters e integrações opcionais futuras.

## Bloco 1: Consolidação Operacional Pós-Batch

Objetivo: manter batch como fluxo operacional padrão quando seguro, sem transformar o backlog estratégico em fila executável automática.

Saídas recomendadas:

- Manter `VAF_BATCH_SIZE=10` como recomendação para blocos normais revisados e seguros.
- Manter `VAF_BATCH_SIZE=3` para validação, retomada, blocos pequenos ou recuperação.
- Manter execução individual para missões sensíveis, críticas, arquiteturais, incertas, investigativas ou de alto risco.
- Integrar a CLI gradualmente com validações locais de Git, logs e resumo pós-batch, sem executar comandos destrutivos nem substituir revisão humana.
- Criar comando futuro para listar missões e comando futuro para resumo pós-batch quando houver contrato seguro.

Critério de saída: operação local consegue diferenciar fila executável, backlog estratégico, batch seguro, retomada e execução individual sem ambiguidade.

## Bloco 2: Fronteira De Política E Auditoria

Objetivo: resolver Policy Engine versus Guardian Engine.

Saídas recomendadas:

- Manter a separação já adotada: Policy Engine resolve políticas declarativas; Guardian Engine aplica avaliação operacional.
- Revisar se a ADR existente e as Specs descrevem adequadamente as novas pontes com Context Router, Model Selection e Audit/Event Log.
- Definir como decisões de política, Guardian, contexto, modelo e uso/API devem ser registradas sem vazar conteúdo sensível.
- Definir formato futuro de persistência local controlada para eventos auditáveis.

Esta decisão vem primeiro porque afeta missões, tools, providers, runtimes, context routing, seleção de modelos, logs, aprovações e validação.

## Bloco 3: Arquitetura De Contexto

Objetivo: separar memória persistente, Knowledge Hub, Semantic Index e Context Router.

Ações recomendadas:

- Definir Context Router como componente de primeira classe.
- Definir entradas: missão, refs de Spec, task, papel de agente, risco, token budget, decisão de modelo e necessidades de retrieval.
- Definir saídas: pacote de contexto, citações, redactions, warnings e motivos de omissão.
- Definir como Knowledge Hub serve documentos canônicos e resultados de retrieval.
- Definir como Semantic Index apoia retrieval sem virar memória.

Saída recomendada: revisão de Spec ou ADR para Context Router e contrato mínimo de retrieval antes de embeddings.

## Bloco 4: Integração Mission-To-Task

Objetivo: conectar MVPs de missão, workflow e task por contratos explícitos.

Ações recomendadas:

- Definir Mission Orchestrator como distinto de Mission Runner.
- Definir saída de Mission Orchestrator como Workflow Plan ou decisão de seleção de workflow.
- Definir handoff de Workflow Engine para Task Queue.
- Definir retorno de estado de Task Queue para Workflow Engine e Mission Runner.

Implementação deve permanecer sequencial até existirem políticas de paralelismo e locks.

## Bloco 5: Integração Task-To-Agent

Objetivo: conectar execução de tasks ao Agent Orchestrator sem dar acesso de infraestrutura a agentes.

Ações recomendadas:

- Definir executor padrão de Task Queue para Agent Orchestrator.
- Definir ciclo de vida de Agent Assignment.
- Definir como agente solicita capabilities.
- Definir como saída de agente vira saída de task, evidência de validação e registro de auditoria.

Guardrail: agentes não devem chamar tools, providers, MCPs, runtime adapters, shell ou bancos diretamente.

## Bloco 6: Integração Capability-To-Provider

Objetivo: tornar o caminho Capabilities -> Skills -> Tools -> Provider Gateway o padrão para efeitos concretos.

Ações recomendadas:

- Definir catálogo essencial de capabilities.
- Definir catálogo essencial de skills.
- Definir tools locais permitidas e modelo de permissões/efeitos.
- Definir eventos de auditoria do Provider Gateway.
- Definir formato de adapter MCP abaixo de tools/providers, não abaixo de agentes.

## Bloco 7: Integração De Persistência

Objetivo: persistir registros críticos por portas antes de adapters específicos de banco.

Ações recomendadas:

- Definir stores para missões, workflows, tasks, decisões Guardian, decisões de modelo, audit logs, documentos canônicos e documentos de conhecimento.
- Definir persistência local controlada para eventos auditáveis antes de exportação, banco ou observabilidade externa.
- Usar filesystem adapter como primeira implementação governada.
- Definir registros JSON determinísticos e semântica de hash.
- Definir política de retenção de logs.

Guardrail: não tornar PostgreSQL obrigatório antes de estabilizar portas de persistência.

## Bloco 8: Semantic Index MVP

Objetivo: adicionar retrieval semântico apenas após estabilização dos contratos de Context Router e Knowledge Hub.

Ações recomendadas:

- Definir estratégia de chunking.
- Definir contrato de embedding provider adapter.
- Definir contrato de vector store adapter.
- Definir pgvector como uma implementação possível, não a única.
- Definir embedding local padrão como detecção de capability, não premissa.

Guardrail: busca semântica deve retornar contexto citável e filtrado por política; não deve despejar texto bruto em prompts sem aprovação do Context Router.

## Bloco 9: Expansão De Runtime Adapters

Objetivo: manter OpenCode como runtime inicial enquanto prepara paridade para outros runtimes.

Ações recomendadas:

- Formalizar operações comuns de RuntimeAdapter.
- Definir schema de detecção de capabilities.
- Definir schema de descoberta de modelos.
- Definir schema de resultado de execução.
- Definir testes de conformidade de adapter.

Adapters futuros candidatos: Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.

## Bloco 10: Avaliação De Providers E Frameworks Externos

Objetivo: decidir quando integrar providers reais e se LangGraph, MetaGPT ou AutoGen devem ser usados como adapters opcionais, referências ou não usados.

Ações recomendadas:

- Avaliar providers reais somente depois de políticas, auditoria, limites de uso/API e Provider Gateway estarem suficientemente claros.
- Avaliar cada framework contra agnosticismo de provider, suporte local-first, máquinas de estado, auditabilidade, footprint de dependências e viabilidade de adapter.
- Mapear cada framework para papéis possíveis: backend de workflow, backend de agent runtime, simulação/referência ou adapter externo.
- Evitar adotar frameworks externos como core antes da estabilização dos contratos do Vercosa.

## Bloco 11: Validação E Governança De Commit

Objetivo: tornar Spec -> Plan -> Tasks -> Implement -> Validate -> Commit aplicável.

Ações recomendadas:

- Definir registros de resultado de validação.
- Definir como testes, checks estáticos, revisão humana, decisões Guardian e revisões por agentes se vinculam a tasks e missões.
- Definir política de auto-commit e comportamento padrão desabilitado.
- Definir como commits referenciam mission IDs, Specs e evidências de validação.

## Ordem Recomendada De Curto Prazo

1. Consolidar documentação pós-batch, backlog estratégico e estado atual.
2. Integrar a CLI com validações locais seguras de Git e resumo pós-batch, sem substituir scripts seguros.
3. Criar comando CLI para listar missões e apoiar diagnóstico operacional.
4. Definir persistência local controlada para Audit/Event Log.
5. Revisar arquitetura pós-integrações centrais e atualizar Specs/ADRs quando necessário.
6. Contrato: Mission Runner -> Workflow Engine -> Task Queue.
7. Contrato: Task Queue -> Agent Orchestrator -> Capability Resolver.
8. Testes de contrato para fronteiras MVP existentes.
9. Design de Semantic Index do Knowledge Hub, ainda sem embeddings obrigatórios.
10. Avaliação de providers reais e conformidade de Runtime Adapter antes de novos runtimes reais.

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

## Futuros Mantidos Fora Do Estado Atual

Permanecem futuros e não devem ser tratados como implementados:

- Persistência externa de eventos.
- Integração real com providers.
- Múltiplos runtimes reais além do adapter inicial.
- RAG semântico.
- Embeddings.
- pgvector como adapter real.
- Semantic Index.
- Internacionalização dos READMEs.
- Guia público completo de release, distribuição e empacotamento para uso final.
- Release alfa.

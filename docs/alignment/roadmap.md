# Roadmap

## Objetivo Do Roadmap

Recomendar os próximos blocos arquiteturais após o checkpoint de alinhamento atual. Este documento não autoriza implementação por si só.

Nenhum código fonte deve ser implementado apenas com base neste documento. Cada bloco de implementação ainda precisa de Spec aprovada ou atualização explícita de Spec existente.

Backlog operacional detalhado de missões futuras: [Backlog estratégico de missões](../roadmap/mission-backlog.md).

Estado factual de implementação, integração e validação: [implementation-status.md](implementation-status.md). Este roadmap deve orientar direção estratégica e critérios de avanço, não repetir o checklist completo de estado.

Revisão arquitetural pós-integrações: [docs/architecture/post-integration-architecture-review.md](../architecture/post-integration-architecture-review.md).

Execução em batch é o fluxo operacional padrão para blocos de missões já revisadas e seguras em `missions/queue/`. O uso seguro está documentado no [playbook de execução em batch](../operations/batch-execution-playbook.md). Execução individual continua sendo o fluxo correto para missões sensíveis, arquiteturais, incertas, investigativas ou de recuperação.

A identidade pública do projeto como framework de Harness Engineering para agentes de IA foi incorporada ao `README.md` principal. A internacionalização dos READMEs permanece tarefa futura e não faz parte deste bloco de alinhamento.

## Princípio Orientador

Prefira integrar contratos MVP existentes antes de adicionar novos frameworks, providers, bancos ou comportamentos de agentes.

A próxima fase deve reduzir ambiguidade, não aumentar superfície funcional.

Atualização da missão 0101: a auditoria de aderência classificou o projeto como `ALINHADO COM RESSALVAS`. A prioridade imediata deixa de ser avanço de release alfa e passa a ser provar um fluxo de valor integrado mínimo. O checklist factual de implementação está em [implementation-status.md](implementation-status.md), e a auditoria está em [docs/audits/objective-and-scope-alignment-audit.md](../audits/objective-and-scope-alignment-audit.md).

Atualização da missão 0102: o contrato base `v1`, o agente executor base, o template compacto e o compositor obrigatório do runner passam a ser infraestrutura operacional. As missões novas de `0103` a `0110` devem usar o formato compacto e declarar exceções de capacidade explicitamente.

Atualização da missão 0103: o README passou a explicitar problema, fluxo de valor, consumidores plausíveis, limites e estado real. A comparação com OpenSpec e GitHub Spec Kit foi documentada em [docs/comparacoes.md](../comparacoes.md). A fronteira `SpecificationProvider` permanece hipótese arquitetural não implementada e não deve ser materializada antes das integrações mínimas previstas para 0104-0108.

Atualização da missão 0104: o fluxo mínimo Mission Runner -> Workflow Engine -> Task Queue foi implementado por contratos injetáveis, com `TaskScheduler` como único loop operacional de tasks no caminho integrado. A próxima prioridade de integração passa a ser Task Queue -> Agent Orchestrator -> Capability Resolver, sem antecipar skills, tools ou providers reais.

Atualização da missão 0105: a ponte Task Queue -> Agent Orchestrator -> Capability Resolver foi implementada por `AgentTaskExecutor` e resolução declarativa obrigatória quando configurada. A próxima prioridade passa a ser demonstrar Capability -> Skill -> Tool -> Provider Gateway em dry-run governado, sem providers reais.

Atualização da missão 0106: o caminho Capability -> Skill -> Tool -> Provider Gateway foi integrado em dry-run governado por `ResolvedCapabilityExecutor` injetável no Agent Orchestrator, sem providers reais.

Atualização da missão 0107: Policy Engine, Context Router, Token Budget Manager, Guardian Engine, Model Selection, Capability Executor, Provider Gateway em dry-run, Runtime Adapter fake/injetado e Audit/Event Log foram integrados no caminho mínimo local, sem provider real, rede, banco, MCP ou RAG.

Atualização da missão 0108: Specs e ADRs afetadas pelas integrações 0104 a 0107 foram revisadas e decisões arquiteturais comprovadas foram registradas em `docs/architecture/decisions/`.

Atualização da missão 0109: `docs/alignment/implementation-status.md` foi consolidado como checklist factual canônico. Este roadmap deve referenciar essa fonte em vez de duplicar inventários de estado.

Atualização da missão 0110: a prontidão alfa foi reavaliada como `NÃO PRONTO` em `docs/release/alpha-readiness-reassessment-0110.md`. O próximo ciclo deveria priorizar licença, validação limpa, canais públicos, revisão final de release notes, reexecução do checklist pré-tag, confirmação de CI no candidato final e autorização explícita antes de qualquer tag, release ou pacote. A licença foi tratada posteriormente na missão 0111.

Atualização da missão 0111: a licença foi adotada como GNU Affero General Public License v3.0 only, `AGPL-3.0-only`, com `LICENSE` criado e metadados de empacotamento alinhados. Isso remove o bloqueio factual de licença ausente, mas não autoriza tag, release ou pacote.

## Estado Considerado Pelo Roadmap

O projeto avançou da fase de fundação para uma fase operacional inicial mais coerente. Para planejar próximos blocos, este roadmap considera o resumo narrativo em [current-state.md](current-state.md), a revisão arquitetural em [post-integration-architecture-review.md](../architecture/post-integration-architecture-review.md) e o checklist factual em [implementation-status.md](implementation-status.md).

Resumo estratégico: há base local de missões, runners, CLI diagnóstica, contratos e integrações mínimas locais. Ainda não há provider real, rede, banco, MCP, API externa, RAG, PostgreSQL, pgvector, Semantic Index, múltiplos runtimes reais, observabilidade externa, tag, release ou pacote publicado.

## Bloco 0: Congelamento De Alinhamento

Objetivo: tornar explícita a arquitetura atual antes de nova implementação.

Ações recomendadas:

- Manter a revisão arquitetural pós-integrações como referência de estado atual.
- Revisar documentos em `docs/alignment/` quando novas missões alterarem arquitetura ou limites.
- Confirmar vocabulário de Mission Runner, Mission Orchestrator, Workflow Engine, Task Queue, Agent Orchestrator, Policy Engine, Guardian Engine, Knowledge Hub, Context Router e Semantic Index.
- Identificar conflitos entre código atual, docs MVP e Specs.
- Converter decisões arquiteturais não resolvidas em ADRs.

Critério de saída: a equipe concorda sobre quais componentes são core, adapters e integrações opcionais futuras.

## Bloco 1: Consolidação Operacional Pós-Batch

Objetivo: manter batch como fluxo operacional padrão quando seguro, sem transformar o backlog estratégico em fila executável automática.

Saídas recomendadas:

- Manter `VAF_BATCH_SIZE=8` como teto recomendado para blocos normais revisados e seguros, sem alterar nesta missão o limite técnico atual do script.
- Manter `VAF_BATCH_SIZE=3` para validação, retomada, blocos pequenos ou recuperação.
- Manter execução individual para missões sensíveis, críticas, arquiteturais, incertas, investigativas ou de alto risco.
- Integrar a CLI gradualmente com validações locais de Git e logs, sem executar comandos destrutivos nem substituir revisão humana.
- Manter os comandos `missions` e `batch-summary` como leituras locais seguras, sem executar missões, scripts, testes ou Git.

Critério de saída: operação local consegue diferenciar fila executável, backlog estratégico, batch seguro, retomada e execução individual sem ambiguidade.

## Bloco 2: Fronteira De Política E Auditoria

Objetivo: resolver Policy Engine versus Guardian Engine.

Saídas recomendadas:

- Manter a separação já adotada: Policy Engine resolve políticas declarativas; Guardian Engine aplica avaliação operacional.
- Revisar se a ADR existente e as Specs descrevem adequadamente as novas pontes com Context Router, Model Selection e Audit/Event Log.
- Definir como decisões de política, Guardian, contexto, modelo e uso/API devem ser registradas sem vazar conteúdo sensível.
- Refinar integração segura da persistência local controlada de eventos auditáveis sem torná-la global obrigatória.

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

Objetivo: manter e revisar a conexão MVP de missão, workflow e task por contratos explícitos.

Ações recomendadas:

- Definir Mission Orchestrator como distinto de Mission Runner.
- Definir saída de Mission Orchestrator como Workflow Plan ou decisão de seleção de workflow.
- Revisar em Spec/ADR o handoff mínimo implementado entre Workflow Engine e Task Queue.
- Preservar `TaskScheduler` como único loop operacional de tasks no caminho integrado enquanto não houver decisão de paralelismo.

Implementação deve permanecer sequencial até existirem políticas de paralelismo e locks.

## Bloco 5: Integração Task-To-Agent

Objetivo: conectar execução de tasks ao Agent Orchestrator sem dar acesso de infraestrutura a agentes.

Status: concluído como ponte mínima na missão 0105.

Ações recomendadas:

- Refinar catálogo mínimo de capabilities e perfis de agente quando houver caso de uso real.
- Preservar `AgentTaskExecutor` como ponte explícita sem mover seleção de agente para `tasks/`.
- Manter a execução de capability atrás de contrato injetável e sem acoplamento direto a agents.

Guardrail: agentes não devem chamar tools, providers, MCPs, runtime adapters, shell ou bancos diretamente.

## Bloco 6: Integração Capability-To-Provider

Objetivo: tornar o caminho Capabilities -> Skills -> Tools -> Provider Gateway o padrão para efeitos concretos.

Status: concluído como integração mínima em dry-run na missão 0106. Ainda não há provider real nem chamada de rede.

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
- Usar a persistência local JSONL opt-in de eventos auditáveis como base antes de exportação, banco ou observabilidade externa.
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

1. Definir o fluxo de valor principal e o consumidor principal do framework.
2. Revisar Specs/ADRs da integração mínima Mission Runner -> Workflow Engine -> Task Queue.
3. Demonstração seca: Capability -> Skill -> Tool -> Provider Gateway, com Guardian, Policy e Audit/Event Log explícitos.
4. Integrar Context Router, Token Budget Manager, Knowledge Hub textual e Model Selection ao fluxo mínimo sem RAG semântico.
5. Revisar Specs/ADRs afetadas pela integração mínima nas missões 0104 e 0105.
6. Atualizar Specs/ADRs apenas quando a integração mínima alterar fronteiras arquiteturais.
7. Manter CLI `missions`, `batch-summary`, `docs-links` e `alpha-readiness` como diagnósticos somente leitura.
8. Resolver pendências mínimas de alfa somente depois do fluxo integrado mínimo ou em paralelo sem criar tag: instalação limpa, canais públicos, CI remoto, release notes finais e checklist pré-tag.
9. Adiar Semantic Index, embeddings, pgvector, RAG semântico, providers reais e múltiplos runtimes até o fluxo central estar demonstrado.
10. Internacionalizar em fases somente após estabilizar conteúdo canônico em português do Brasil: documentação pública, depois CLI, depois demais mensagens expostas.

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
- Retenção e rotação de eventos auditáveis.
- Integração real com providers.
- Múltiplos runtimes reais além do adapter inicial.
- RAG semântico.
- Embeddings.
- pgvector como adapter real.
- Semantic Index.
- Internacionalização dos READMEs.
- Guia público completo de release, distribuição, empacotamento e processo público maduro de contribuição para uso final.
- Release notes finais revisadas para publicação real.
- Diagnóstico local de prontidão alfa aprovado ou aprovado com ressalvas explicitamente aceitas.
- Checklist pré-tag local aprovado ou aprovado com ressalvas explicitamente aceitas.
- Revalidação de licença e metadados de empacotamento no candidato final.
- Processo público maduro de segurança e canal definitivo de vulnerabilidades.
- Release alfa.
- Tag `v0.1.0-alpha.1`, release GitHub e changelog de release versionado.
- Pacote publicado.
- Matriz ampla de CI, lint e validação de instalação limpa automatizada.

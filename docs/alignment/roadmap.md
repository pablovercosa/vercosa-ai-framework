# Roadmap

## Objetivo Do Roadmap

Recomendar os próximos blocos arquiteturais após o checkpoint de alinhamento atual. Este documento não autoriza implementação por si só.

Nenhum código fonte deve ser implementado apenas com base neste documento. Cada bloco de implementação ainda precisa de Spec aprovada ou atualização explícita de Spec existente.

Backlog operacional detalhado de missões futuras: [Backlog estratégico de missões](../roadmap/mission-backlog.md).

Revisão arquitetural pós-integrações: [docs/architecture/post-integration-architecture-review.md](../architecture/post-integration-architecture-review.md).

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
- Audit/Event Log inicial em memória, com persistência local JSONL opt-in, helpers opcionais para decisões centrais e eventos de missão/batch.
- CLI operacional inicial com `status`, `missions`, `batch-summary`, `validate` e `doctor`.
- Exemplos operacionais iniciais em `docs/examples/`.
- Guia inicial de instalação local para desenvolvimento em `docs/getting-started/local-installation.md`.
- Checklist documental de instalação limpa em `docs/getting-started/clean-install-checklist.md`, com execução real registrada em 2026-07-10 e resultado `REPROVADO`.
- Guia inicial de contribuição em `CONTRIBUTING.md`.
- Código de conduta inicial em `CODE_OF_CONDUCT.md` e diretrizes em `docs/conduct/`, ainda sem canal público definitivo para problemas de conduta.
- Política inicial de segurança em `SECURITY.md` e documentação inicial em `docs/security/`, ainda sem canal público definitivo de vulnerabilidades.
- Documentação legal inicial em `docs/legal/`, com política de uso responsável e licença final ainda pendente.
- Templates iniciais de issue e pull request em `.github/`, sem processo público completo de triagem, merge ou suporte formal.
- Checklist de prontidão para futura alfa pública em `docs/release/public-alpha-readiness.md`, sem criação de release, tag, pacote ou changelog de release versionado.
- Política inicial de versionamento em `docs/release/versioning-policy.md` e plano da versão alfa em `docs/release/alpha-version-plan.md`, com `0.1.0-alpha.1` apenas como versão planejada.
- Changelog inicial em `CHANGELOG.md`, sem data de release, tag ou promessa de estabilidade.
- Revisão arquitetural pós-integrações em `docs/architecture/post-integration-architecture-review.md`, sem implementação nova.

Esse estado não implica integração real com providers, billing real, observabilidade externa, persistência externa de eventos, RAG semântico, embeddings, pgvector ou Semantic Index.

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

- Manter `VAF_BATCH_SIZE=10` como recomendação para blocos normais revisados e seguros.
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

1. Resolver pendências mínimas para futura alfa: licença, canal público de vulnerabilidades, canal público de conduta, revisão dos templates iniciais, manutenção do changelog inicial, política de release, CI público quando decidido, correção dos bloqueios da instalação limpa reprovada e reexecução do checklist.
2. Integrar a CLI com validações locais seguras de Git, sem substituir scripts seguros.
3. Manter os comandos CLI `missions` e `batch-summary` como apoio de diagnóstico operacional somente leitura.
4. Refinar retenção, rotação e integração opcional da persistência local JSONL para Audit/Event Log.
5. Atualizar Specs/ADRs quando a revisão pós-integrações identificar mudança material de fronteira.
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
- Retenção e rotação de eventos auditáveis.
- Integração real com providers.
- Múltiplos runtimes reais além do adapter inicial.
- RAG semântico.
- Embeddings.
- pgvector como adapter real.
- Semantic Index.
- Internacionalização dos READMEs.
- Guia público completo de release, distribuição, empacotamento e processo público maduro de contribuição para uso final.
- Licença final em `LICENSE`.
- Processo público maduro de segurança e canal definitivo de vulnerabilidades.
- Release alfa.
- Tag `v0.1.0-alpha.1`, release GitHub e changelog de release versionado.
- Pacote publicado.
- CI público.

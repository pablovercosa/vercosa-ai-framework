# Revisão Arquitetural Pós-Integrações

Links principais: [README principal](../../README.md) | [Índice de módulos](module-index.md) | [Mapa de arquitetura](../alignment/architecture-map.md) | [Estado atual](../alignment/current-state.md) | [Roadmap](../alignment/roadmap.md) | [Backlog estratégico](../roadmap/mission-backlog.md)

## Objetivo

Registrar uma revisão arquitetural pós-integrações do Vercosa AI Framework após as integrações concluídas até a missão 0080.

Este documento é factual e conservador. Ele consolida o estado atual, os eixos arquiteturais, os módulos centrais, as integrações existentes, os limites, os riscos e recomendações para próximas missões. Ele não aprova implementação nova, não altera Specs, não cria release, não cria fila executável e não promete funcionalidades futuras como existentes.

## Leitura Do Estado Atual

O Vercosa AI Framework está em estado de MVP operacional inicial, com contratos, módulos Python determinísticos, documentação operacional, runners locais, CLI inicial e integrações parciais entre governança, contexto, seleção de modelo e auditoria.

O projeto já incorporou no README principal sua identidade como framework de Harness Engineering. Isso significa que o valor arquitetural do VAF está na camada operacional ao redor de agentes e modelos: missões, runners, políticas, guardrails, contexto, orçamento de tokens, seleção de modelos, providers, runtime adapters, auditoria, validação, documentação e governança.

O estado atual não deve ser lido como uma plataforma completa de agentes autônomos, RAG, observabilidade ou integração real com múltiplos providers. O framework possui uma base para essas evoluções, mas elas continuam futuras ou fora do escopo atual.

## VAF Como Harness Engineering

O VAF não posiciona o modelo de IA como o sistema inteiro. O modelo é uma peça substituível dentro de um harness governado.

Neste momento, o harness organiza:

- missões em Markdown e runners locais;
- validação operacional antes e depois de execução;
- políticas declarativas e avaliação Guardian;
- montagem determinística de contexto;
- orçamento de tokens como metadado de decisão;
- seleção de modelo por catálogo local e política;
- runtime adapter inicial para OpenCode;
- Provider Gateway e cadeia capabilities, skills e tools em MVP;
- Audit/Event Log inicial em memória, com persistência local JSONL opt-in;
- CLI operacional inicial;
- documentação pública alfa preparada, ainda sem release publicada.

## Eixos Arquiteturais Atuais

| Eixo | Estado atual | Limite principal |
| --- | --- | --- |
| Execução de missões | Mission Runner local, fila em diretórios e scripts seguros para missão individual e batch. | Mission Orchestrator distinto ainda não existe como camada consolidada. |
| Governança | Policy Engine MVP, Guardian Engine MVP e Usage/API Limit Guard inicial. | Integração orquestrada obrigatória ainda é futura; muitas pontes são opcionais pelo chamador. |
| Contexto | Context Router e Token Budget Manager determinísticos, com `ContextPackage`. | Sem RAG semântico, embeddings, pgvector ou Semantic Index. |
| Seleção de modelo | Model Selection Engine MVP com catálogo em memória, políticas resolvidas opcionais e requisitos de orçamento opcionais. | Sem descoberta real de modelos, billing real ou chamada a providers. |
| Runtime | Runtime Adapter inicial para OpenCode. | OpenCode é laboratório/runtime atual, não núcleo; múltiplos runtimes reais ainda são futuros. |
| Providers | Provider Gateway, registry e adapters injetáveis em MVP. | Sem múltiplos providers reais em produção. |
| Auditoria | Audit/Event Log inicial em memória, persistência local JSONL opt-in, helpers opcionais e eventos básicos de missão. | Sem persistência externa, banco, dashboard, exportação remota, retenção, rotação ou integração automática com scripts shell. |
| CLI operacional | Comandos `status`, `missions`, `batch-summary`, `validate` e `doctor`. | Não executa missões, Git, testes, scripts, providers, banco ou rede. |
| Documentação operacional | Playbooks, checklist pós-batch, guia de instalação, contribuição, exemplos e checklist de alfa pública. | Documentação ainda precisa evitar promessa pública acima do implementado. |
| Preparação pública alfa | Checklist documental, política inicial de versionamento, plano da versão alfa e CI mínimo foram criados. | Alfa pública ainda não foi publicada; não há tag, changelog final, matriz ampla de CI ou release. |

## Módulos Centrais E Responsabilidades

| Módulo | Responsabilidade atual | Estado |
| --- | --- | --- |
| `agents` | Perfis, registry e preparação de execução de agentes sem acesso direto a providers, MCPs ou bancos. | MVP |
| `audit` | Tipos de eventos, porta `EventLog`, `InMemoryEventLog` e helpers opcionais para decisões e ciclo de vida. | contracts |
| `canonicalizer` | Canonicalização MVP de texto e Markdown para documentos rastreáveis. | MVP |
| `capabilities` | Resolução de intenções abstratas para skills compatíveis. | MVP |
| `cli` | CLI local inicial para status, validação estrutural e diagnóstico `doctor`. | MVP |
| `context` | Context Router, Token Budget Manager e `ContextPackage` determinísticos. | MVP |
| `core` | Primitivas compartilhadas de identidade e vocabulário. | MVP |
| `guardian` | Avaliação determinística de riscos, ações, comandos, Context Packages e sinais textuais de limite de uso/API. | MVP |
| `knowledge` | Ingestão Markdown, store em memória, busca textual e adaptação para candidatos de contexto. | MVP |
| `missions` | Tipos, fila em diretório e Mission Runner Python com eventos opcionais. | MVP |
| `model_selection` | Seleção de modelo por catálogo local, política e requisitos de orçamento informados. | MVP |
| `persistence` | Porta genérica e adapter filesystem inicial para registros determinísticos. | MVP |
| `policy` | Resolução declarativa de políticas e produção de `ResolvedPolicySet`. | MVP |
| `providers` | Provider Gateway, registry, contratos de adapter e dry-run. | MVP |
| `runtime` | Runtime Adapter e OpenCode Runtime Adapter inicial. | MVP |
| `skills` | Registry e executor de skills que usam tools governadas. | MVP |
| `tasks` | Task Queue em memória, scheduler sequencial, estados, tentativas e dependências. | MVP |
| `tools` | Tool Executor governado, registry, permissões, efeitos e delegação opcional a Provider Gateway. | MVP |
| `workflows` | Workflow Engine sequencial MVP com avaliação Guardian e RuntimeAdapter. | MVP |

## Integrações Já Existentes

As integrações abaixo existem como MVP ou integração inicial. Elas devem ser entendidas como pontes explícitas e determinísticas, não como fluxo completo obrigatório de produção.

- Policy Engine com Guardian Engine: `ResolvedPolicySet` opcional pode ser fornecido ao Guardian por chamador externo.
- Policy Engine com Context Router: `ResolvedPolicySet` opcional pode ser fornecido em `ContextRequest`.
- Policy Engine com Model Selection: políticas resolvidas opcionais podem influenciar warnings, aprovação e exclusões determinísticas.
- Token Budget Manager com Model Selection: requisitos mínimos derivados de orçamento podem ser repassados ao selector.
- Usage/API Limit Guard com fluxo operacional: logs locais já produzidos podem ser classificados para detectar quota, rate limit, billing ou limite de uso.
- Audit/Event Log com decisões centrais: helpers opcionais transformam resultados de Policy, Guardian e Context em eventos estruturados.
- Audit/Event Log com Mission Runner: o `MissionRunner` Python pode registrar eventos de missão quando recebe um `EventLog` opcional.
- CLI com `status`, `missions`, `batch-summary`, `validate` e `doctor`: comandos locais de leitura, listagem de missões por estado, resumo pós-batch auxiliar, validação estrutural e diagnóstico básico.
- Batch como fluxo operacional padrão quando seguro: `scripts/vaf-run-batch-safe.sh` é recomendado para blocos revisados, com parada na primeira falha e push manual por padrão.

## Fluxos Arquiteturais De Alto Nível

Fluxo operacional implementado para missões locais:

```text
missão em missions/queue
↓
runner seguro individual ou batch
↓
worker local / Mission Runner operacional
↓
validação local
↓
pytest + python3 -m compileall src
↓
missions/done ou missions/failed
↓
revisão de documentação, Git e checklist
```

Fluxo de governança e contexto disponível por chamada explícita:

```text
PolicySet explícito
↓
Policy Engine
↓
ResolvedPolicySet
↓
Context Router / Guardian Engine / Model Selection
↓
ContextPackage, GuardianDecision ou SelectionDecision
↓
Audit/Event Log opcional quando EventLog é fornecido
```

Fluxo conceitual desejado, ainda não integrado de ponta a ponta:

```text
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
Capabilities
↓
Policy Engine / Guardian Engine
↓
Skills
↓
Tools
↓
Provider Gateway
↓
Runtime Adapter / Providers / MCPs / APIs
↓
Audit/Event Log e documentação de evidências
```

## Classificação Do Estado

Implementado:

- CLI `status`, `missions`, `batch-summary`, `validate` e `doctor`.
- Mission Runner Python e fila local em diretórios.
- Scripts operacionais seguros para missão individual e batch.
- Policy Engine, Guardian Engine, Context Router, Token Budget Manager, Knowledge Hub textual, Model Selection, Runtime Adapter, Provider Gateway, capabilities, skills, tools, tasks e workflows em MVP ou contratos.
- Audit/Event Log em memória e helpers opcionais.
- Documentação operacional e checklist de alfa pública.

MVP:

- Execução local determinística e limitada.
- Seleção de modelos por catálogo em memória.
- Busca textual em memória no Knowledge Hub.
- Provider Gateway e Runtime Adapter com adapters injetáveis ou OpenCode inicial.
- Persistence Layer com filesystem repository inicial, sem ser banco operacional do framework.

Integração inicial:

- `ResolvedPolicySet` repassado para Guardian, Context Router e Model Selection.
- Orçamento de tokens repassado para Model Selection por metadados.
- Eventos auditáveis opcionais para Policy, Guardian, Context e Mission Runner.
- Usage/API Limit Guard lendo logs já produzidos.

Futuro:

- Mission Orchestrator distinto.
- Fluxo completo Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider.
- Retenção, rotação e integração opcional da persistência local de eventos auditáveis.
- Integração real com providers.
- Múltiplos runtime adapters reais.
- Semantic Index, embeddings, pgvector e RAG semântico.
- Dashboard ou observabilidade externa.
- Matriz ampla de CI, lint, validação limpa automatizada, release alfa, tag, changelog de release versionado e internacionalização.

Fora do escopo atual:

- Implementar código novo nesta revisão.
- Criar tag, versão, changelog de release versionado ou release.
- Internacionalizar READMEs.
- Acessar rede, banco, providers, OpenCode, Ollama, Claude, Gemini, OpenAI ou MCPs.

## Limites Atuais

O projeto ainda não possui:

- RAG semântico.
- Embeddings.
- pgvector.
- Semantic Index.
- Banco de dados operacional.
- Persistência externa de eventos.
- Múltiplos providers reais em produção.
- Múltiplos runtimes reais em produção.
- Dashboard.
- Matriz ampla de CI, lint e validação limpa automatizada.
- Release alfa publicada.
- Canal público definitivo para problemas de conduta.
- Internacionalização dos READMEs.

Esses limites são intencionais neste momento. Eles reduzem acoplamento prematuro e evitam prometer capacidades antes de contratos, políticas, auditoria e validação estarem maduros.

## Riscos Arquiteturais Atuais

- Documentação crescendo antes da release e ficando difícil de manter sincronizada.
- Risco de promessa pública acima do implementado, especialmente sobre RAG, providers, persistência e alfa pública.
- Dependência operacional do runtime atual, caso OpenCode seja tratado como núcleo em vez de adapter.
- Ausência de persistência externa de auditoria, limitando retenção e investigação posterior.
- Ausência de validação de instalação limpa em ambiente novo.
- Ausência de política pública de segurança.
- Ausência de governança comunitária madura e canal público definitivo para problemas de conduta.
- Ausência de release alfa publicada, tag alfa e changelog de release versionado.
- CI mínimo ainda não cobre matriz ampla, lint ou validação de instalação limpa automatizada.

## Decisões Arquiteturais Consolidadas

- `README.md` permanece canônico em português do Brasil.
- Internacionalização deve ocorrer no final, depois de estabilizar o conteúdo canônico.
- Batch é o padrão operacional quando o bloco está revisado e seguro.
- Execução individual continua necessária para missões sensíveis, críticas, arquiteturais, incertas, investigativas ou de recuperação.
- OpenCode é runtime/laboratório atual, não núcleo do framework.
- Sem banco por enquanto no fluxo operacional atual.
- Sem RAG por enquanto.
- Sem pgvector por enquanto.
- Eventos auditáveis existem com memória e JSONL local opt-in, sem persistência externa por enquanto.
- Push manual permanece o padrão recomendado; push automático é opt-in.

## Próximos Refinamentos Arquiteturais Possíveis

- Amadurecer política pública de segurança e definir canal público de vulnerabilidades.
- Revisar `CODE_OF_CONDUCT.md` e definir canal público para problemas de conduta antes de abertura pública ampla.
- Revisar os templates iniciais de issue e pull request conforme o processo público amadurecer.
- Manter o changelog inicial atualizado sem criar release versionada.
- Revisar a versão alfa planejada antes de missão específica de release.
- Criar checklist de instalação limpa em ambiente novo.
- Manter os comandos CLI `missions` e `batch-summary` como leituras locais seguras.
- Refinar diagnósticos pós-batch somente quando houver contrato seguro.
- Definir retenção, rotação e integração opcional da persistência local de eventos auditáveis.
- Planejar integração real com providers por adapters governados.
- Avaliar Semantic Index sem implementar embeddings prematuramente.
- Internacionalizar READMEs no final.

## Recomendações Para Próximas Missões

1. Priorizar artefatos públicos mínimos antes da alfa: decisão de licença, canal público de vulnerabilidades, templates, changelog, versão inicial e validação de instalação limpa.
2. Manter próximas implementações de CLI restritas a leitura local segura, como resumo pós-batch, sem executar Git destrutivo, providers, rede ou scripts automaticamente.
3. Usar a persistência local JSONL opt-in do Audit/Event Log como base antes de observabilidade externa, dashboards ou bancos.
4. Formalizar contratos Mission Runner -> Workflow Engine -> Task Queue antes de expandir loops de agentes.
5. Formalizar Task Queue -> Agent Orchestrator -> Capability Resolver antes de dar efeitos concretos a agentes.
6. Avaliar providers reais apenas depois de política, auditoria, limites de uso/API e Provider Gateway estarem claros.
7. Adiar Semantic Index, embeddings e pgvector até Context Router, Knowledge Hub e auditoria terem contratos de segurança, citação, redaction e retenção mais estáveis.

## Conclusão

A arquitetura pós-integrações está coerente como MVP de Harness Engineering, desde que os limites atuais permaneçam explícitos. O projeto já possui uma fundação operacional e documental significativa, mas ainda não deve ser apresentado como release alfa publicada, plataforma completa de agentes, RAG semântico, observabilidade completa ou integração real multi-provider.

O próximo ciclo deve reduzir risco público e operacional antes de expandir capacidades: segurança pública, versionamento alfa, validação de instalação limpa, persistência local de eventos e comandos CLI adicionais de leitura são candidatos naturais para missões futuras.

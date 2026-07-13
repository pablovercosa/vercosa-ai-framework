# Auditoria De Aderência Ao Objetivo E Escopo

Links principais: [README principal](../../README.md) | [Estado atual](../alignment/current-state.md) | [Checklist canônico de implementação](../alignment/implementation-status.md) | [Roadmap](../alignment/roadmap.md) | [Perguntas em aberto](../alignment/open-questions.md) | [Backlog estratégico](../roadmap/mission-backlog.md) | [Revisão pós-integrações](../architecture/post-integration-architecture-review.md)

## Objetivo Da Auditoria

Auditar se os componentes, documentos, scripts, testes, processos e preparações de release construídos até a missão 0100 continuam contribuindo diretamente para o objetivo original do Vercosa AI Framework.

Esta auditoria é documental e estratégica. Ela não remove código, não reestrutura módulos, não cria funcionalidades, não cria tag, não publica release e não publica pacote.

## Classificação Geral

Classificação geral do projeto: `ALINHADO COM RESSALVAS`.

Justificativa: o projeto preserva a direção original de framework open source, Specification First, AI Native, provider agnostic e local first para Harness Engineering assistida por IA. Porém, o fluxo completo Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider ainda não está integrado de ponta a ponta; vários motores existem como MVPs ou contratos acionados por chamador explícito; a preparação alfa avançou antes de uma demonstração clara de valor integrado; e a documentação ficou maior que a maturidade funcional do produto.

Impacto: o projeto é coerente como fundação técnica e operacional, mas ainda não deve ser apresentado como plataforma completa, release alfa pronta, RAG, integração real multi-provider ou sistema de agentes completo.

Recomendação geral: as missões 0102-0110 devem priorizar integração mínima de fluxo de valor, redução de ambiguidade, simplificação de abstrações não integradas e adiamento formal de PostgreSQL, pgvector, RAG e internacionalização até que o núcleo entregue um fluxo útil demonstrável.

## Objetivo Canônico Identificado

Objetivo canônico reconstruído: permitir que pessoas e agentes desenvolvam e executem trabalho de engenharia de software orientado por especificações, assistido por IA, de forma rastreável, segura, reproduzível, extensível e agnóstica de modelos, providers, runtimes, bancos, IDEs e infraestrutura, usando uma camada de Harness Engineering que governa missões, workflows, tasks, agentes, capabilities, skills, tools, contexto, políticas, guardrails, auditoria, seleção de modelos e adapters.

Não foi inventado um objetivo novo. O texto acima consolida as fontes existentes.

## Fontes Utilizadas

- [AGENTS.md](../../AGENTS.md): identidade original, objetivo, princípios, regra Specification First, hierarquia conceitual e limites sobre OpenCode, PostgreSQL, pgvector e adapters.
- [README.md](../../README.md): identidade pública atual como framework de Harness Engineering, estado atual, lacunas e fluxo conceitual.
- [knowledge/vision.md](../../knowledge/vision.md): visão original de desenvolvimento por missões, Specs, policies, workflows, agents, capabilities, knowledge e governance.
- [knowledge/principles/framework-principles.md](../../knowledge/principles/framework-principles.md): princípios Specification First, AI Native, Provider Agnostic, Local First, Extensible, Security, Token Efficiency e Governance.
- [knowledge/architecture/core-architecture.md](../../knowledge/architecture/core-architecture.md): hierarquia Mission -> Mission Orchestrator -> Workflow -> Task -> Agent -> Capability -> Policy -> Skill -> Tool -> Providers.
- [docs/alignment/current-state.md](../alignment/current-state.md): estado real declarado até a missão 0100.
- [docs/architecture/post-integration-architecture-review.md](../architecture/post-integration-architecture-review.md): revisão pós-integrações e limites atuais.
- `logs/pre-audit-targeted-module-verification.md` e `logs/pre-audit-model-selection-core-followup.md`: evidências locais privadas e não versionadas da verificação direcionada de Guardian, Core e Model Selection.
- `logs/pre-audit-dynamic-module-usage.md` e `logs/pre-audit-entrypoint-reachability.md`: evidências locais privadas e não versionadas de uso por CLI, testes e entrypoints, com falsos negativos corrigidos pelas verificações direcionadas.
- [docs/release/alpha-readiness-diagnostic.md](../release/alpha-readiness-diagnostic.md), [docs/release/pre-tag-checklist-execution.md](../release/pre-tag-checklist-execution.md), [docs/release/alpha-candidate-summary.md](../release/alpha-candidate-summary.md) e [docs/release/tag-decision-request.md](../release/tag-decision-request.md): evidências de release alfa ainda não pronta.
- `src/`, `tests/`, `scripts/` e `missions/done/`: estrutura implementada, testes e histórico de missões concluídas.

## Ausências Registradas Como Evidência

- `LICENSE` está ausente no repositório. Isso bloqueia release pública até decisão ou exceção explícita.
- `docs/audits/` não existia antes desta missão. Esta auditoria cria o diretório e o primeiro relatório.
- `docs/history/` não existia antes desta missão. Esta missão cria o histórico de marcos por faixa.
- `docs/vision/`, `docs/specifications/`, `docs/specs/`, `agents/` e `skills/` na raiz não foram encontrados. A documentação canônica equivalente está em `knowledge/`, `specs/framework/`, `.opencode/`, `src/vercosa_ai_framework/agents/` e `src/vercosa_ai_framework/skills/`.

## Visão Geral Do Projeto

O VAF continua sendo uma plataforma de Harness Engineering orientada por especificações, desde que a palavra plataforma seja entendida como camada operacional de engenharia e não como produto final completo. O Mission Runner e os scripts seguros são infraestrutura de suporte para executar missões locais; eles não devem virar o centro do produto.

O fluxo útil existente hoje é operacional e interno: missão em Markdown, fila local, runner seguro individual ou batch, execução via worker/OpenCode no fluxo shell, validações locais, movimentação para `missions/done` ou `missions/failed`, documentação e commits. Esse fluxo serviu ao desenvolvimento do próprio VAF, mas ainda não demonstra o fluxo arquitetural completo do framework para um usuário externo com tasks, agentes, capabilities, skills, tools e provider governado.

## Respostas Às Questões Obrigatórias

1. O objetivo original e atual é organizar desenvolvimento de software orientado por Specs e assistido por IA de forma governada, rastreável, extensível e agnóstica de provider/runtime/storage. A formulação atual acrescenta corretamente a linguagem de Harness Engineering.
2. O objetivo está razoavelmente claro em `AGENTS.md`, `README.md` e `knowledge/vision.md`, mas há variação de ênfase entre framework de desenvolvimento, harness operacional e preparação alfa. A divergência é de foco, não de direção.
3. O framework continua sendo uma plataforma de Harness Engineering orientada por especificações, mas ainda em MVP operacional inicial.
4. O projeto segue Specification First na documentação e no histórico de missões. Risco: as Specs canônicas ainda são mais amplas que a implementação e algumas integrações nasceram como MVPs isolados antes de um fluxo completo.
5. O Mission Runner é infraestrutura de suporte. Há risco de centralidade indevida porque o fluxo real mais comprovado hoje é o runner/batch, não a cadeia completa de harness.
6. Existe fluxo completo operacional interno para execução de missões do próprio projeto. Não existe fluxo completo arquitetural Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider demonstrado como caso de uso de usuário final.
7. Policy Engine, Guardian Engine, Context Router e Token Budget Manager estão implementados como MVPs e possuem pontes testadas. Eles ainda são usados principalmente por chamadas explícitas e testes, não como governança obrigatória em todo fluxo real.
8. Knowledge Hub, Model Selection Engine, Provider Gateway e Runtime Adapter entregam valor parcial hoje. Knowledge Hub é busca textual em memória; Model Selection é catálogo em memória; Provider Gateway é fronteira governada com adapters injetáveis; Runtime Adapter inicial prepara/aciona OpenCode. Ainda representam preparação futura para uso amplo.
9. Agentes, skills, tools e capabilities possuem contratos e testes, mas poucos casos de uso concretos versionados. A evidência de `.opencode/agents/framework-architect.md` não equivale ao catálogo completo de agentes do framework.
10. Existe duplicação potencial entre Mission Runner, Mission Orchestrator ausente, Workflow Engine e scripts shell; também entre logs shell, Audit/Event Log e persistência JSONL.
11. Há abstrações prematuras em Agent Orchestrator, capabilities, skills, tools, Provider Gateway, Persistence Layer genérica, Model Selection e release alfa, pois existem antes do primeiro fluxo externo completo validado.
12. A documentação em geral evita promessa explícita de recursos futuros como implementados, mas o volume e a repetição podem sugerir maturidade maior que a evidência.
13. Implementações com documentação insuficiente relativa: detalhes operacionais de alguns comandos CLI e integrações opcionais do Agent Orchestrator aparecem mais no código/testes que em exemplos de uso completos.
14. A quantidade de documentação está acima da maturidade funcional. Isso ajuda governança, mas aumenta custo de manutenção e risco de divergência.
15. A preparação alfa ocorreu cedo demais para publicação, embora os documentos tenham registrado corretamente `NÃO PRONTO` e `REPROVADO`.
16. O consumidor principal ainda não está definido com precisão: mantenedor interno via SSH, contribuidor técnico, usuário de framework Python, agente executor ou integrador de runtime.
17. O projeto resolve um problema concreto de ponta a ponta para o próprio repositório: executar missões locais governadas por documentação e validação. Ainda não resolve de ponta a ponta o problema mais amplo de desenvolvimento assistido por IA via cadeia completa.
18. PostgreSQL, pgvector e RAG continuam coerentes como adapters futuros para Knowledge Hub, Semantic Index e Code Intelligence, mas não são necessários agora e não devem ser priorizados antes do fluxo central.
19. A internacionalização é coerente como fase futura, não como prioridade atual. O conteúdo canônico em português do Brasil ainda está mudando.
20. Permanecer: Mission Runner, runners shell, Guardian, Policy, Context Router, Token Budget, CLI, auditoria inicial e documentação canônica. Integrar: Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider. Simplificar: documentação repetitiva e abstrações sem caso de uso. Adiar: PostgreSQL, pgvector, RAG, providers reais, múltiplos runtimes, internacionalização. Remover futuramente: nenhum item deve ser removido agora; candidatos devem ser reavaliados após fluxo integrado. Reavaliar: Mission Orchestrator, centralidade do batch, release alfa e escopo de providers.
21. Specs canônicas e atuais: `specs/framework/0001` a `0014`. Históricas: specs embutidas em `missions/done/*-spec.md`. Substituídas: specs antigas em missões quando houver versão equivalente em `specs/framework/`. Divergentes: Specs que descrevem fluxo completo ainda não implementado. Documentadas, mas não implementadas: Semantic Index, RAG, pgvector, múltiplos runtimes, persistência externa. Implementadas sem Spec atualizada suficiente: detalhes recentes de CLI alfa, JSONL opt-in e batch operacional devem continuar vinculados a docs e, se virarem core, exigir atualização de Spec/ADR.

## Aderência Por Componente

| Componente | Finalidade declarada | Estado real | Integração real | Classificação | Evidência | Recomendação | Prioridade |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Mission Runner | Executar missões governadas por runtime adapter | Implementado em MVP Python | Integrado opcionalmente a Guardian e Audit; fluxo shell real usa scripts/worker | ADERENTE COM RESSALVAS; NÃO INTEGRADO | `src/vercosa_ai_framework/missions/runner.py`, `tests/test_mission_runner.py`, `tests/test_mission_runner_guardian.py` | Manter como suporte, integrar com Workflow/Task sem virar produto central | alta |
| runners shell | Executar missão ou batch com validações locais | Implementados e executáveis | Fluxo operacional real do projeto | ADERENTE COM RESSALVAS | `scripts/`, `docs/operations/`, `logs/pre-audit-evidence.md` | Corrigir acoplamento a caminho absoluto e registrar relação com Mission Runner Python | alta |
| batch runner | Executar lote sequencial seguro | Implementado e documentado | Fluxo interno validado para batches | ADERENTE COM RESSALVAS | `scripts/vaf-run-batch-safe.sh`, backlog e release docs | Manter, mas evitar que batch seja confundido com core do produto | média |
| Policy Engine | Resolver políticas declarativas | MVP implementado | Consumido por Guardian, Context Router e Model Selection via `ResolvedPolicySet` opcional | ADERENTE COM RESSALVAS; NÃO INTEGRADO | `tests/test_policy_*`, `docs/architecture/post-integration-architecture-review.md` | Promover integração obrigatória apenas no primeiro fluxo completo | alta |
| Guardian Engine | Enforcement operacional e guardrails | MVP implementado | Usado por Mission Runner, Workflow, Agent, Tool, Provider quando injetado/chamado | ADERENTE COM RESSALVAS | `tests/test_guardian_engine.py`, `logs/pre-audit-targeted-module-verification.md` | Definir modo padrão por fluxo e eventos obrigatórios | alta |
| Context Router | Montar contexto governado | MVP determinístico | Integra Knowledge Hub por candidatos e políticas opcionais | ADERENTE COM RESSALVAS; NÃO INTEGRADO | `src/vercosa_ai_framework/context/router.py`, `tests/test_context_*` | Integrar a missões/agentes/model selection com citações e evidências | alta |
| Token Budget Manager | Estimar e aplicar orçamento de tokens | MVP determinístico por heurística | Requisitos podem ser repassados ao Model Selection | ADERENTE COM RESSALVAS | `src/vercosa_ai_framework/context/budget.py`, `tests/test_token_budget_model_selection_integration.py` | Manter simples; não trocar por cálculo externo antes de uso real | média |
| Knowledge Hub | Organizar documentos canônicos e busca | MVP textual em memória | Alimenta Context Router por adapter/candidatos | ADERENTE COM RESSALVAS; PREMATURO | `src/vercosa_ai_framework/knowledge/`, `tests/test_knowledge_*` | Usar em exemplo real antes de Semantic Index | alta |
| Model Selection Engine | Selecionar modelo por política e catálogo | MVP em memória | Consumido por Agent/Runtime e políticas opcionais; sem descoberta real | ADERENTE COM RESSALVAS; PREMATURO | `src/vercosa_ai_framework/model_selection/selector.py`, logs direcionados | Integrar a decisão a fluxo de agente antes de providers reais | alta |
| Provider Gateway | Fronteira governada para providers | MVP com adapters injetáveis e dry-run | Usado por ToolExecutor quando configurado | ADERENTE COM RESSALVAS; PREMATURO; NÃO INTEGRADO | `src/vercosa_ai_framework/providers/gateway.py`, `tests/test_provider_gateway.py` | Manter como boundary; adiar provider real até fluxo completo | média |
| Runtime Adapter | Isolar runtimes como OpenCode | OpenCode adapter MVP | Mission Runner, Workflow e Agent podem usar RuntimeAdapter | ADERENTE COM RESSALVAS | `src/vercosa_ai_framework/runtime/opencode.py`, `tests/test_opencode_runtime_adapter.py` | Não expandir runtimes antes de contrato de conformidade | média |
| Usage/API Limit Guard | Classificar sinais textuais de limite externo | Implementado | Chamado por CLI/script de uso e fluxo operacional textual | ADERENTE COM RESSALVAS | `src/vercosa_ai_framework/guardian/usage_limits.py`, `tests/test_usage_limit_guard.py` | Manter como classificador; não implementar billing real agora | baixa |
| Audit/Event Log | Registrar eventos auditáveis | Em memória e helpers opcionais | Mission Runner Python pode registrar; scripts shell não integram automaticamente | ADERENTE COM RESSALVAS; NÃO INTEGRADO | `src/vercosa_ai_framework/audit/`, `tests/test_audit_*` | Definir eventos mínimos obrigatórios para fluxo integrado | alta |
| persistência JSONL | Persistir eventos auditáveis localmente | Implementada opt-in | Não ativada globalmente | ADERENTE COM RESSALVAS | `src/vercosa_ai_framework/audit/jsonl.py`, `tests/test_audit_event_persistence.py` | Manter opt-in; definir retenção antes de expandir | média |
| agentes | Selecionar perfil e executar via runtime | MVP implementado | Não conectado ao fluxo Mission -> Workflow -> Task por padrão operacional | ADERENTE COM RESSALVAS; PREMATURO; NÃO INTEGRADO | `src/vercosa_ai_framework/agents/orchestrator.py`, `logs/pre-audit-agents-skills-specs.md` | Criar primeiro caso real com Task Queue e Capability Resolver | alta |
| skills | Transformar skill em tool request | MVP implementado | Acionado por testes e executor, não por fluxo real completo | ADERENTE COM RESSALVAS; PREMATURO; NÃO INTEGRADO | `src/vercosa_ai_framework/skills/executor.py` | Definir catálogo mínimo de skills só para o fluxo principal | média |
| tools | Validar e executar tool ou Provider Gateway | MVP implementado | Integrado a SkillExecutor e ProviderGateway quando configurado | ADERENTE COM RESSALVAS; PREMATURO | `src/vercosa_ai_framework/tools/executor.py` | Manter dry-run padrão; evitar tools perigosas | média |
| capabilities | Resolver capability para skill | MVP implementado | Não solicitado por agentes no fluxo operacional real | ADERENTE COM RESSALVAS; PREMATURO; NÃO INTEGRADO | `src/vercosa_ai_framework/capabilities/resolver.py` | Definir capabilities essenciais do primeiro fluxo | alta |
| workflows | Executar tasks sequenciais via runtime | MVP implementado | Não orquestrado por Mission Runner no fluxo principal | ADERENTE COM RESSALVAS; NÃO INTEGRADO | `src/vercosa_ai_framework/workflows/engine.py`, `tests/test_workflow_engine.py` | Integrar com Mission Runner e Task Queue em contrato mínimo | alta |
| CLI | Diagnóstico local e comandos seguros | Implementada | Entry point real; não executa missões | ADERENTE | `src/vercosa_ai_framework/cli/main.py`, testes CLI, `pyproject.toml` | Manter leitura segura; não substituir scripts até decisão | média |
| empacotamento Python | Instalação editável local | Implementado mínimo | `vaf` disponível após instalação; validação limpa ainda reprovada historicamente | ADERENTE COM RESSALVAS | `pyproject.toml`, `docs/release/clean-install-validation.md` | Reexecutar validação limpa após ajustes | alta |
| CI | Rodar testes e compileall | Workflow mínimo criado | CI remoto ainda depende de push/confirmação | ADERENTE COM RESSALVAS | `.github/workflows/ci.yml`, docs release | Confirmar CI remoto antes de tag; adiar matriz/lint | média |
| documentação pública | Explicar projeto, guias e limites | Ampla e em pt-BR | Boa rastreabilidade, volume alto | ADERENTE COM RESSALVAS | `README.md`, `docs/`, `CHANGELOG.md` | Reduzir repetição e apontar para checklist canônico | média |
| processo de release | Preparar gates de alfa | Documentado | Execuções reais reprovaram; sem tag/release | ADERENTE COM RESSALVAS; PREMATURO | docs release, diagnóstico `NÃO PRONTO`, checklist `REPROVADO` | Adiar tag até fluxo central e gates mínimos | alta |
| preparação alfa | Organizar candidato `0.1.0-alpha.1` | Preparatória | Não pronta para publicação | ADERENTE COM RESSALVAS; PREMATURO | `alpha-candidate-summary.md`, `tag-decision-request.md` | Manter bloqueada até licença, CI, instalação limpa e fluxo de valor | alta |
| PostgreSQL planejado | Storage/vector store possível | Planejado | Nenhum adapter real | ADERENTE COM RESSALVAS; DOCUMENTADO, MAS NÃO IMPLEMENTADO | `AGENTS.md`, roadmap | Adiar; não tornar obrigatório | baixa |
| pgvector planejado | Vector store possível | Planejado | Nenhum adapter real | ADERENTE COM RESSALVAS; DOCUMENTADO, MAS NÃO IMPLEMENTADO | `AGENTS.md`, release docs | Adiar até contrato de vector store | baixa |
| RAG planejado | Retrieval semântico futuro | Planejado | Não implementado | ADERENTE COM RESSALVAS; DOCUMENTADO, MAS NÃO IMPLEMENTADO | README lacunas, roadmap | Adiar até Context Router e Knowledge Hub terem fluxo real | baixa |
| internacionalização planejada | Documentos multilíngues futuros | Planejada | Não implementada | ADERENTE COM RESSALVAS; DOCUMENTADO, MAS NÃO IMPLEMENTADO | `docs/release/public-alpha-readiness.md`, roadmap | Fazer em fases após estabilizar pt-BR | baixa |
| especificações canônicas | Fonte de verdade arquitetural | Existem `0001` a `0014` | Mais amplas que implementação | ADERENTE COM RESSALVAS | `specs/framework/` | Classificar divergências e atualizar quando integrar | alta |
| especificações históricas em missions/done | Histórico e rastreabilidade | Existem desde `0002` | Algumas foram substituídas por specs canônicas | ADERENTE COM RESSALVAS | `missions/done/*-spec.md` | Tratar como histórico, não fonte principal quando houver spec canônica | média |
| ADRs e decisões | Registrar decisões arquiteturais | Existem em `knowledge/decisions/` | Cobrem Policy/Guardian e Context; faltam outras fronteiras | ADERENTE COM RESSALVAS | `knowledge/decisions/` | Criar ADRs só para decisões que bloqueiam integração | média |

## Fluxos Completos Existentes

- Fluxo operacional interno de missões: `missions/queue` -> scripts seguros -> worker/OpenCode -> validação local -> `missions/done` ou `missions/failed` -> revisão documental/Git. Esse fluxo é útil para o desenvolvimento do próprio repositório.
- Fluxo CLI de diagnóstico: comandos `status`, `missions`, `batch-summary`, `validate`, `doctor`, `docs-links` e `alpha-readiness` leem estado local e apoiam governança sem efeitos colaterais.
- Fluxo de governança por chamada explícita: Policy Engine resolve políticas; `ResolvedPolicySet` pode ser passado a Guardian, Context Router ou Model Selection; eventos auditáveis podem ser criados quando `EventLog` é fornecido.

## Fluxos Completos Ausentes

- Mission Orchestrator distinto escolhendo workflow a partir de missão.
- Mission Runner integrando obrigatoriamente Workflow Engine, Task Queue, Agent Orchestrator e Capability Resolver.
- Agent Orchestrator solicitando capability real, resolvendo skill, executando tool e passando pelo Provider Gateway como fluxo padrão.
- Context Router alimentando agente/model selection em fluxo real com Knowledge Hub, citações, redactions, orçamento e eventos.
- Provider real governado por Policy, Guardian, Usage Limit, Audit e fallback.
- Demonstração de usuário externo que resolva um problema de engenharia de software de ponta a ponta usando o framework como biblioteca ou CLI.

## Desvio De Escopo

O principal desvio não é funcionalidade fora do domínio, mas inversão de prioridade: release, documentação pública e governança de publicação avançaram antes da integração do fluxo central de valor. O Mission Runner e o batch também receberam centralidade operacional maior que a cadeia completa prevista na arquitetura original.

PostgreSQL, pgvector, RAG, internacionalização e múltiplos runtimes continuam coerentes como direção, mas seriam desvio se priorizados antes do primeiro fluxo integrado.

## Abstrações Prematuras

- Provider Gateway existe antes de provider real integrado ao caso de uso principal.
- Capabilities, skills e tools existem antes de agentes reais solicitarem capabilities no fluxo operacional.
- Persistence Layer genérica e JSONL existem antes de política de retenção e eventos obrigatórios por fluxo.
- Model Selection existe antes de descoberta real de modelos e antes de seleção ser obrigatória no fluxo central.
- Preparação alfa existe antes de instalação limpa aprovada e licença definida.

## Documentação Desproporcional Ou Redundante

A documentação é tecnicamente cuidadosa e evita prometer recursos futuros como existentes, mas há sobreposição entre README, estado atual, roadmap, backlog, revisão pós-integrações e documentos de release. O efeito é positivo para governança, mas negativo para manutenção e clareza de usuário.

Recomendação: `docs/alignment/implementation-status.md` deve ser a fonte canônica de checklist de implementação; `CHANGELOG.md` deve permanecer histórico; roadmap e backlog devem apontar para o checklist em vez de repetir estado completo.

## Preparação De Release

A preparação alfa é aderente como disciplina de release, mas prematura como caminho para publicação. Evidências fortes: diagnóstico `alpha-readiness` classificado como `NÃO PRONTO`, checklist pré-tag `REPROVADO`, instalação limpa `REPROVADO`, `LICENSE` ausente, CI remoto pendente e tag não autorizada.

Recomendação: adiar tag alfa até que exista pelo menos um fluxo de valor integrado mínimo, além dos gates de release já documentados.

## PostgreSQL, pgvector E RAG

PostgreSQL, pgvector e RAG permanecem coerentes com a visão de Knowledge Hub, Semantic Index e Code Intelligence, mas devem ser tratados como adapters futuros. Nenhum deles é necessário para provar o fluxo central. Implementá-los agora aumentaria acoplamento, dependências e superfície de segurança antes de haver contrato final de retrieval, citação, redaction e retenção.

## Internacionalização

A internacionalização deve permanecer planejada em fases: primeiro documentação pública, depois CLI, depois demais mensagens expostas. Ela deve começar somente após estabilização do conteúdo canônico em português do Brasil e definição do consumidor principal.

## Riscos

- Risco alto: publicar alfa antes de fluxo central útil e antes de licença/instalação limpa/CI remoto.
- Risco alto: Mission Runner e batch virarem centro do produto em vez de suporte ao harness.
- Risco alto: manter muitos módulos MVP isolados sem integração real, aumentando custo de manutenção.
- Risco médio: documentação extensa ficar divergente da implementação.
- Risco médio: abstrações de provider/runtime/persistência serem expandidas antes de caso de uso.
- Risco médio: Specs canônicas permanecerem mais amplas que o código sem rastreabilidade de status.
- Risco baixo: ausência de internacionalização no estágio atual, desde que documentada como futura.

## Recomendações Para 0102-0110

1. Definir o fluxo de valor principal e o consumidor principal antes de adicionar novos componentes.
2. Integrar Mission Runner, Workflow Engine e Task Queue com contrato mínimo, sem paralelismo e sem novos providers.
3. Integrar Task Queue, Agent Orchestrator e Capability Resolver em um caso de uso pequeno.
4. Demonstrar Capability -> Skill -> Tool -> Provider Gateway em dry-run com evidências auditáveis.
5. Tornar Policy, Guardian, Context Router, Token Budget, Model Selection e Audit participantes explícitos do fluxo mínimo, ainda que por configuração simples.
6. Consolidar `implementation-status.md` como fonte única de checklist e reduzir repetição em docs futuros.
7. Adiar tag alfa até a integração mínima e gates de release.
8. Manter PostgreSQL, pgvector, RAG, providers reais, múltiplos runtimes e internacionalização como avaliações futuras.
9. Criar ADRs apenas para fronteiras que bloqueiam o fluxo central: Mission Runner vs Mission Orchestrator, Workflow vs Task Queue, Task vs Agent, Capability-to-Provider e retenção de auditoria.

## Conclusão

O Vercosa AI Framework continua alinhado ao objetivo original, mas com ressalvas relevantes. A fundação é consistente e rastreável, porém a prova de valor ainda está concentrada em operação interna por missões e batch. O próximo ciclo deve converter contratos MVP em um fluxo integrado mínimo, reduzir promessas implícitas de maturidade e impedir que preparação alfa ou documentação substituam entrega funcional do harness.

# ADR: Policy Engine e Guardian Engine como camadas complementares

## Status da decisão

Aceita em 2026-07-04.

Esta ADR resolve a fronteira arquitetural entre Policy Engine e Guardian Engine para as próximas Specs e implementações do Vercosa AI Framework.

## Contexto

O Vercosa AI Framework já possui um Guardian Engine MVP em `src/vercosa_ai_framework/guardian/`. Esse MVP avalia missões, tasks, comandos e ações sensíveis, retornando decisões estruturadas como `allow`, `warn`, `block` e `require_approval`.

A documentação atual reconhece uma lacuna: os documentos e Specs usam os termos `Policy Engine`, `Guardian Engine` e `Policy Engine / Guardian Engine`, mas ainda não definem se eles são o mesmo componente, componentes separados ou camadas diferentes.

As Specs relevantes indicam responsabilidades sobrepostas:

- A Spec 0005 define o Guardian Engine como avaliador de missões, ações, segurança, tokens, custo, risco, comandos, segredos e aprovações.
- A Spec 0009 posiciona um Policy Engine futuro entre Capabilities e Skills para combinar Guardian Specs, políticas de projeto, usuário e ambiente.
- A Spec 0010 exige que Provider Gateway consulte Guardian Engine para providers, fallback, rede, custo, segredos e efeitos sensíveis.
- As Specs 0011 e 0012 exigem governança para Knowledge Hub, Canonicalizer, contexto, redaction, prompt injection, embeddings e providers externos.
- A Spec 0013 prevê persistência de Guardian Decisions, Model Decisions, audit logs e registros rastreáveis.

O alinhamento arquitetural atual também prepara componentes futuros como Context Router e Token Budget Manager. Esses componentes dependerão de políticas declarativas, mas também precisarão de enforcement operacional antes de entregar contexto, consumir orçamento, escolher modelos ou executar ações.

## Problema

Se Policy Engine e Guardian Engine permanecerem ambíguos, o framework corre riscos arquiteturais relevantes:

- Guardian Engine virar depósito de toda regra do framework, misturando segurança, custo, contexto, seleção de modelo, memória, roteamento, runtime e provider.
- Policy Engine virar executor operacional ou duplicar lógica já aplicada por Guardian, Tools, Runtime, CLI e Provider Gateway.
- Model Selection, Context Router e Token Budget Manager implementarem suas próprias políticas locais sem rastreabilidade comum.
- Tools, Provider Gateway, Runtime Adapter e CLI replicarem checagens de segurança e permissões de forma inconsistente.
- Decisões `allow`, `warn`, `block` e `require_approval` não serem persistíveis ou comparáveis no futuro.

A arquitetura precisa decidir uma fronteira estável antes de expandir integração Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider.

## Decisão

Policy Engine e Guardian Engine serão camadas diferentes com responsabilidades complementares.

O Policy Engine será a camada declarativa, composicional e determinística de resolução de políticas. Ele combina Guardian Specs, políticas de projeto, políticas de missão, políticas de usuário, políticas de ambiente, políticas de runtime, políticas de provider, políticas de modelo, políticas de contexto e políticas de orçamento em um conjunto aplicável, ordenado e rastreável de restrições.

O Guardian Engine será a camada de enforcement operacional, segurança e decisão executável. Ele recebe uma ação, plano, request ou transição concreta, consulta ou recebe políticas resolvidas pelo Policy Engine quando disponível, avalia risco e emite uma decisão operacional: `allow`, `warn`, `block` ou `require_approval`.

O Guardian Engine pode continuar sendo o componente efetivo de avaliação no MVP enquanto o Policy Engine formal não existir. Essa substituição é provisória e deve ser registrada como compatibilidade de fase, não como colapso conceitual dos componentes.

## Justificativa

Separar as camadas preserva responsabilidades técnicas claras:

- Políticas são declarações de restrições, prioridades, precedência, escopo, exceções, limites e preferências.
- Enforcement é decisão operacional sobre uma ação real em um contexto real.
- Uma política pode orientar muitos componentes sem executar nada.
- Uma decisão Guardian precisa ser aplicável imediatamente por Mission Runner, Workflow Engine, Agent Orchestrator, Tool Executor, Provider Gateway, Runtime Adapter ou CLI.
- Context Router e Token Budget Manager precisarão resolver políticas sem virar componentes de segurança.
- Model Selection precisa consumir política sem virar runtime, provider ou Guardian.

Esta decisão também preserva o princípio de Governance by Design: políticas devem ser explícitas, componíveis, versionáveis e rastreáveis; decisões operacionais devem ser auditáveis, explicáveis e persistíveis.

## Responsabilidades do Policy Engine

O Policy Engine deve:

- carregar e normalizar políticas declarativas vindas de Guardian Specs, Specs de framework, Specs de projeto, ADRs, missão, workflow, task, agent profile, capability profile, skill profile, tool profile, provider profile, runtime profile e ambiente detectado;
- resolver precedência entre políticas globais, de projeto, de missão, de usuário, de ambiente e de runtime;
- produzir um `Policy Context` ou `Resolved Policy Set` aplicável a uma missão, task, capability, tool, provider, modelo, contexto ou operação de persistência;
- compor políticas de segurança, privacidade, custo, tokens, qualidade, compliance, rede, providers, storage, runtime, contexto, retenção, logging e aprovação;
- detectar conflito declarativo entre políticas antes da execução;
- declarar limites efetivos, como orçamento máximo, tokens máximos, permissões concedidas, domínios de contexto permitidos, providers permitidos e critérios de aprovação;
- informar quais políticas foram usadas como fonte de decisão;
- fornecer dados para Guardian Engine, Model Selection Engine, Context Router, Token Budget Manager, Workflow Engine, Agent Orchestrator, Tool Executor, Provider Gateway e Persistence Layer;
- manter decisões de resolução rastreáveis e futuramente persistíveis;
- falhar de forma segura quando políticas necessárias estiverem ausentes, conflitantes ou inválidas.

## Responsabilidades do Guardian Engine

O Guardian Engine deve:

- avaliar ações concretas, planos, transições, commands, tool requests, provider requests, runtime requests, context packages e operações sensíveis;
- aplicar enforcement de segurança, privacidade, risco, segredos, permissões, approvals, bloqueios e warnings;
- consultar ou receber políticas resolvidas pelo Policy Engine;
- classificar risco operacional de missões, tasks, ações e requests;
- emitir decisões estruturadas `allow`, `warn`, `block` ou `require_approval`;
- explicar a decisão com políticas aplicadas, razões, riscos, bloqueios, warnings, aprovações necessárias e alternativas seguras;
- registrar `guardian_decision_ref` ou preparar registro persistível futuro;
- bloquear ações quando falhar avaliação crítica, redaction obrigatória, secret scanning, validação de política ou rastreabilidade mínima;
- tratar `require_approval` como pausa ou bloqueio operacional até aprovação válida;
- preservar provider agnosticism, runtime agnosticism, storage agnosticism e model agnosticism.

## Responsabilidades que NÃO pertencem ao Policy Engine

O Policy Engine não deve:

- executar tools, providers, runtimes, comandos, subprocessos, MCPs, APIs, bancos ou filesystem;
- escolher modelo concreto substituindo Model Selection Engine;
- montar contexto final substituindo Context Router;
- calcular consumo real ou alocação operacional substituindo Token Budget Manager;
- executar redaction operacional em payloads;
- aprovar ações humanas por conta própria;
- modificar estado de missão, workflow, task, agent assignment ou fila;
- persistir registros diretamente ignorando Persistence Layer;
- conter lógica específica de OpenCode, PostgreSQL, pgvector, Ollama, GitHub, systemd, Linux, ARM64 ou qualquer provider específico;
- decidir que uma ação real pode executar sem passar pelo Guardian Engine quando houver risco ou efeito externo.

## Responsabilidades que NÃO pertencem ao Guardian Engine

O Guardian Engine não deve:

- virar catálogo geral de todas as políticas do framework;
- resolver sozinho estratégia de contexto, custo, memória, roteamento ou seleção de modelo sem políticas resolvidas;
- escolher modelos concretos sem Model Selection Engine;
- construir Context Packages substituindo Context Router;
- gerenciar orçamento detalhado substituindo Token Budget Manager;
- executar tools, providers, runtimes, comandos, MCPs, APIs, bancos ou filesystem;
- implementar Provider Gateway, Tool Executor, Skill Executor ou Runtime Adapter;
- armazenar segredos ou audit logs diretamente ignorando Persistence Layer;
- aprovar Specs, Plans, Tasks ou commits por si só;
- alterar políticas declarativas como efeito colateral;
- esconder falhas de avaliação ou continuar execução automática em risco alto quando a política não for resolvível.

## Relação com Model Selection Engine

Model Selection Engine consome políticas resolvidas, não Guardian como substituto de política global.

O fluxo esperado é:

```text
Task / Agent / Context Request
↓
Policy Engine resolve política de modelo, custo, privacidade, qualidade e fallback
↓
Model Selection Engine escolhe modelo compatível
↓
Guardian Engine avalia riscos operacionais da decisão quando houver provider externo, custo pago, dado sensível, fallback arriscado ou política ambígua
↓
Runtime Adapter executa conforme decisão aprovada
```

Model Selection Engine deve emitir `Model Decision` auditável com política fonte, modelo, provider, fallback, custo estimado, review requerido e notas de segurança.

Guardian Engine pode bloquear ou exigir aprovação para uma decisão de modelo, mas não deve substituir a seleção por heurística própria.

## Relação com Context Router futuro

Context Router será responsável por escolher qual contexto será entregue a agentes, modelos, skills, validações ou runtimes.

Policy Engine deve fornecer políticas de contexto, incluindo domínios permitidos, sensibilidade, privacidade, redaction, citações obrigatórias, contexto máximo, fontes confiáveis, retention e regras de prompt injection.

Guardian Engine deve avaliar o Context Package antes da entrega quando houver risco: contexto sensível, cross-domain RAG, fonte externa, prompt injection, provider externo, ausência de citação, payload grande, segredo provável ou violação de política.

Context Router não deve virar Guardian Engine nem Policy Engine. Ele decide seleção e composição de contexto sob políticas resolvidas e enforcement Guardian.

## Relação com Token Budget Manager futuro

Token Budget Manager será responsável por estimar, reservar, consumir, reduzir e reportar orçamento de tokens por missão, workflow, task, agent assignment, context package, modelo, capability, tool e validação.

Policy Engine deve resolver limites e preferências de token: máximos por missão, task, ciclo, contexto, provider, modelo, domínio e risco.

Token Budget Manager deve aplicar cálculo e alocação operacional dentro desses limites.

Guardian Engine deve bloquear, avisar ou exigir aprovação quando orçamento for excedido, desconhecido, ampliado, reutilizado indevidamente ou incompatível com política.

Guardian Engine não deve implementar sozinho a estratégia completa de token budgeting. Policy Engine não deve contar tokens em payloads reais como executor operacional.

## Relação com Knowledge Hub, Canonicalizer e Persistence

Policy Engine define políticas para ingestão, canonicalização, indexação, recuperação, cache, redaction, prompt injection, sensibilidade, domínios, retenção, storage e providers permitidos.

Guardian Engine aplica enforcement em operações concretas:

- ingestão de fonte externa ou sensível;
- canonicalização de binários ou fontes não confiáveis;
- detecção ou redaction de segredos;
- geração de embeddings;
- RAG cross-domain;
- entrega de contexto sensível;
- persistência de decisões, logs, documentos, índices, caches e backups;
- reindexação, migration ou restore.

Knowledge Hub deve consultar políticas para decidir domínio, ranking, indexação e retrieval, mas deve passar por Guardian quando a operação tiver risco.

Canonicalizer deve usar políticas para conversão, redaction e tratamento de fonte, mas deve respeitar bloqueios Guardian.

Persistence Layer deve persistir `Policy Resolution Records`, `Guardian Decisions`, `Model Decisions`, audit events e artefatos relacionados por portas/adapters, sem acoplar a storage específico.

## Relação com Mission Runner, Workflow Engine, Task Queue e Agent Orchestrator

Mission Runner mantém ciclo operacional da missão. Ele deve pedir resolução de políticas antes de iniciar execução relevante e consultar Guardian antes de transições ou ações sensíveis.

Workflow Engine transforma missão em workflow e tasks. Ele deve consumir políticas resolvidas para limites, risco, validação, modelo, contexto e approvals, e consultar Guardian para plano, replanejamento, retry e conclusão sensível.

Task Queue controla estado, elegibilidade, tentativas e scheduling. Ela deve carregar restrições resolvidas e respeitar bloqueios, approvals e limites, mas não deve resolver política de alto nível nem executar enforcement sozinha.

Agent Orchestrator seleciona agente e coordena assignment. Ele deve receber políticas resolvidas para agent profile, capabilities, modelo, contexto, delegação e limites, e consultar Guardian antes de ações sensíveis, capability sensível, delegação, retry, runtime execution e validação de alto risco.

Nenhum desses componentes deve duplicar lógica de política; eles devem consumir resolução declarativa e acatar decisões Guardian.

## Relação com Capabilities, Skills, Tools, Providers e MCPs

Capabilities expressam intenção. Skills implementam procedimentos. Tools executam operações técnicas. Provider Gateway isola providers, MCPs, APIs, bancos, CLIs, filesystem, serviços locais e runtimes.

Policy Engine deve resolver quais capabilities, skills, tools, effects, permissões, providers, fallbacks, custos, rede e dados são permitidos para uma missão, task ou assignment.

Guardian Engine deve avaliar pontos de enforcement:

- antes de resolver capability sensível;
- antes de selecionar skill com efeitos sensíveis;
- antes de executar tool com escrita, rede, comando, custo, segredo, MCP, banco ou provider externo;
- antes de Provider Gateway acionar provider externo, perigoso, deprecated, experimental ou com fallback;
- antes de expor dados sensíveis a MCP, API ou provider externo.

MCPs permanecem infraestrutura atrás de Tools e Providers. Agentes não devem conhecer MCPs diretamente.

## Como decisões de política devem ser registradas

Decisões de política devem ser separadas em dois tipos de registro:

- `Policy Resolution Record`: resultado declarativo produzido pelo Policy Engine, contendo políticas fonte, precedência, conflitos, limites efetivos, permissões concedidas, restrições e validade.
- `Guardian Decision Record`: decisão operacional emitida pelo Guardian Engine, contendo avaliação, ação final, risco, matched policies, reasons, required actions, warnings, approvals, blocked items, redactions, limites aplicados e expiração quando aplicável.

Ambos devem ser futuramente persistidos pela Persistence Layer e referenciáveis por `mission_id`, `workflow_id`, `task_id`, `attempt_id`, `agent_assignment_id`, `capability_request_id`, `tool_execution_request_id`, `provider_request_id`, `context_package_id`, `model_decision_id` e `audit_event_id` quando aplicável.

Logs não devem conter segredos. Payload completo só deve ser persistido quando política permitir explicitamente.

## Como bloqueios, warnings e approvals devem ser tratados

`allow` permite continuidade dentro dos limites declarados. Não elimina validações futuras.

`warn` permite continuidade somente quando política permitir. O warning deve ser registrado e associado à entidade afetada.

`require_approval` deve pausar, bloquear ou marcar a entidade como `requires_review` até aprovação específica, rastreável, escopada e, quando aplicável, expirada.

`block` impede a ação afetada. O componente chamador deve interromper a ação, registrar motivo e, quando possível, oferecer alternativa segura ou replanejamento.

Approvals não devem ser genéricos. Devem declarar ação, alvo, risco, permissões, prazo, aprovador, política que permitiu a exceção e escopo autorizado.

Warnings não podem ser usados para contornar bloqueios. Bloqueios não podem ser convertidos em warnings por runtime, tool, CLI ou provider.

## Como evitar duplicação de lógica entre Policy, Guardian, Runtime, Tools e CLI

A regra de fronteira será:

- Policy Engine resolve o que é permitido, proibido, preferido, limitado ou exige aprovação em forma declarativa.
- Guardian Engine decide se uma ação concreta pode prosseguir.
- Runtime Adapter executa apenas requests já governados e pode aplicar bloqueios adicionais específicos do ambiente.
- Tool Executor valida contrato da tool, permissões e efeitos, e chama Guardian para risco operacional.
- Provider Gateway valida provider e adapter, chama Guardian para risco operacional e não decide política global.
- CLI apresenta interface, coleta entrada, mostra decisões e chama componentes; não deve conter política de domínio.

Listas ou regras comuns devem viver em políticas declarativas ou contratos compartilhados. Runtime, Tools, Providers e CLI podem ter guardrails locais defensivos, mas esses guardrails devem ser mais restritivos, nunca substitutos da decisão Policy/Guardian.

## Consequências positivas

- Reduz ambiguidade entre política declarativa e enforcement operacional.
- Prepara Context Router e Token Budget Manager sem colocá-los dentro do Guardian.
- Evita que Guardian Engine vire componente monolítico de todas as regras.
- Permite rastreabilidade distinta entre resolução de política e decisão de execução.
- Mantém Model Selection como componente próprio e policy-driven.
- Facilita testes de contrato por camada.
- Preserva provider agnosticism, runtime agnosticism e storage agnosticism.
- Reduz duplicação de lógica em CLI, Runtime, Tools e Provider Gateway.

## Consequências negativas

- Adiciona uma camada arquitetural futura a implementar e manter.
- Exige contratos explícitos entre Policy Engine e Guardian Engine.
- A fase MVP continuará usando Guardian como substituto parcial de Policy Engine até o componente existir.
- Pode aumentar o número de registros auditáveis por ação.
- Exige disciplina para não colocar decisões de estratégia no Guardian ou enforcement no Policy Engine.

## Riscos

- Implementar Policy Engine cedo demais com escopo excessivo.
- Manter Guardian como substituto provisório por tempo demais e cristalizar acoplamento.
- Criar modelos de decisão incompatíveis entre Policy Resolution Record e Guardian Decision Record.
- Duplicar regras de permissões em Tool Executor, Provider Gateway e Runtime Adapter.
- Context Router e Token Budget Manager criarem políticas próprias em vez de consumir Policy Engine.
- Falta de Persistence Layer madura dificultar auditoria de decisões.

## Regras de implementação futura

1. Policy Engine deve ser implementado como componente separado, não como renomeação do Guardian Engine.
2. Policy Engine não pode executar tools, providers, runtimes, comandos, MCPs, APIs, bancos ou filesystem.
3. Guardian Engine deve aceitar políticas resolvidas ou referências a políticas resolvidas quando o Policy Engine existir.
4. Guardian Engine deve continuar emitindo decisões operacionais `allow`, `warn`, `block` e `require_approval`.
5. A política mais restritiva deve prevalecer em conflitos, salvo exceção aprovada, escopada e auditável.
6. Components de execução não devem embutir política global; devem chamar Policy/Guardian por contrato.
7. Runtime, Tool Executor e Provider Gateway podem aplicar validações defensivas locais, mas não podem relaxar decisão Guardian.
8. Model Selection Engine deve consumir política e emitir decisão auditável; não deve ficar dentro do Guardian.
9. Context Router deve consumir políticas e passar Context Packages sensíveis por Guardian.
10. Token Budget Manager deve consumir limites resolvidos e reportar consumo para decisões Guardian quando limites mudarem ou forem excedidos.
11. Persistence Layer deve ser usada para registros futuros de política, Guardian, modelo, contexto, tokens e audit trail.
12. Nenhuma implementação deve hardcodar OpenCode, PostgreSQL, pgvector, Ollama, ARM64, Linux ou MCP como dependência central dessa fronteira.

## Checklist para a próxima missão

- [ ] Atualizar Specs afetadas para substituir `Policy Engine / Guardian Engine` por fronteira explícita quando necessário.
- [ ] Definir contrato mínimo de `Policy Resolution Request` e `Policy Resolution Record`.
- [ ] Definir como Guardian Engine recebe `Resolved Policy Set` sem acoplar ao storage.
- [ ] Definir ADR ou Spec do Context Router usando esta ADR como premissa.
- [ ] Definir Token Budget Manager como componente próprio ou subcontrato explícito do Context Router.
- [ ] Definir persistência futura de Policy Resolution Records e Guardian Decision Records via Persistence Layer.
- [ ] Revisar Tool Executor e Provider Gateway para garantir que validações locais não dupliquem política global além de guardrails defensivos.
- [ ] Revisar Model Selection para declarar dependência de política resolvida e rastreabilidade de decisões.
- [ ] Manter Guardian MVP como substituto provisório documentado até Policy Engine existir.
- [ ] Não implementar features funcionais novas enquanto Context Router, Token Budget Manager e Mission Orchestrator permanecerem ambíguos para a missão em questão.

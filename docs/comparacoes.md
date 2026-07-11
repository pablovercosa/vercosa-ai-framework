# Comparação Factual Entre VAF, OpenSpec E GitHub Spec Kit

Links principais: [README principal](../README.md) | [Estado atual](alignment/current-state.md) | [Status de implementação](alignment/implementation-status.md) | [Roadmap](alignment/roadmap.md) | [Backlog estratégico](roadmap/mission-backlog.md)

## Objetivo Da Comparação

Comparar o Vercosa AI Framework, o OpenSpec e o GitHub Spec Kit de forma técnica, neutra e verificável, distinguindo capacidades documentadas oficialmente por cada projeto, capacidades comprovadas hoje no VAF, capacidades planejadas para o VAF e hipóteses arquiteturais ainda não implementadas.

Esta comparação não cria ranking, não declara superioridade e não usa popularidade, estrelas, adoção ou comunidade como medida de qualidade.

## Data Da Consulta

Fontes consultadas em 2026-07-11.

## Metodologia

- Foram usadas somente fontes oficiais públicas dos projetos para afirmar capacidades de OpenSpec e GitHub Spec Kit.
- A comparação sobre o VAF usa documentos e estado local do próprio repositório.
- Ausência de documentação nas fontes consultadas não foi tratada como prova de ausência de implementação.
- Capacidades não identificadas nas fontes oficiais consultadas foram registradas com essa formulação.
- A visão pretendida do VAF foi separada do estado atual comprovado.
- O Mission Runner não foi usado como prova de que toda a arquitetura VAF está integrada.

## Fontes Oficiais Consultadas

OpenSpec:

- <https://github.com/Fission-AI/OpenSpec>
- <https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md>
- <https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md>
- <https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md>
- <https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md>
- <https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md>
- <https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md>

GitHub Spec Kit:

- <https://github.com/github/spec-kit>
- <https://github.github.com/spec-kit/>
- <https://github.github.com/spec-kit/quickstart.html>
- <https://github.github.com/spec-kit/concepts/sdd.html>
- <https://github.github.com/spec-kit/reference/overview.html>
- <https://github.github.com/spec-kit/reference/integrations.html>
- <https://github.github.com/spec-kit/reference/extensions.html>

Vercosa AI Framework:

- [README principal](../README.md)
- [Auditoria de aderência](audits/objective-and-scope-alignment-audit.md)
- [Estado atual](alignment/current-state.md)
- [Status de implementação](alignment/implementation-status.md)
- [Roadmap](alignment/roadmap.md)
- [Revisão arquitetural pós-integrações](architecture/post-integration-architecture-review.md)
- [Backlog estratégico](roadmap/mission-backlog.md)
- [Specs do framework](../specs/framework/)

## Tabela Principal

| Critério | OpenSpec segundo fontes oficiais | GitHub Spec Kit segundo fontes oficiais | VAF atualmente comprovado | VAF planejado ou pretendido |
| --- | --- | --- | --- | --- |
| Problema principal tratado | Adicionar uma camada leve de especificações para alinhar humanos e assistentes de codificação antes de escrever código. | Colocar especificações no centro do desenvolvimento assistido por IA, evitando partir diretamente para código. | Organiza execução local de missões e documentação de arquitetura para reduzir improviso no próprio repositório. | Transformar desenvolvimento com IA baseado em prompts improvisados em processo governado, auditável e orientado por Specs. |
| Unidade principal de trabalho | `change` em `openspec/changes/<nome>/`, com proposta, specs delta, design e tasks. | Feature/spec em `specs/<id-feature>/`, com spec, plan, tasks e artefatos auxiliares. | Missão Markdown em diretórios `missions/queue`, `running`, `done` e `failed`. | Mission como intenção de alto nível decomposta em workflow, tasks, agentes, capabilities, skills e tools. |
| Fluxo operacional documentado | `/opsx:explore`, `/opsx:propose`, `/opsx:apply`, `/opsx:sync` e `/opsx:archive`; expanded workflow adiciona `new`, `continue`, `ff`, `verify`, `bulk-archive` e `onboard`. | Constituição, `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, `/speckit.checklist`, `/speckit.tasks`, `/speckit.analyze`, `/speckit.implement` e `/speckit.converge`. | Runner seguro individual, batch seguro, CLI diagnóstica, composição de contexto e validações locais. | Objetivo -> especificação -> missão -> políticas -> contexto -> agentes/skills -> modelo -> runtime/provider -> execução -> testes -> evidências -> auditoria -> commit. |
| Artefatos produzidos | `proposal.md`, delta specs, `design.md`, `tasks.md`, config e arquivo de mudança. | Constituição, `spec.md`, `plan.md`, `tasks.md`, checklists, research, data model, contracts, quickstart e scripts/templates conforme fluxo. | Documentos de missão, logs, eventos opcionais, docs de alinhamento, Specs do framework e artefatos Python locais. | Evidências rastreáveis ligando objetivo, Spec, tarefas, decisões, modelo, execução, validações, auditoria e commit. |
| Integração com agentes de codificação | Gera skills e comandos para múltiplas ferramentas, incluindo OpenCode, Claude Code, Cursor, Codex, Copilot, Gemini e outras. | `specify init` configura integrações para múltiplos agentes; também há comandos para listar, instalar, usar, alternar e atualizar integrações. | OpenCode é runtime/laboratório inicial; `.opencode/agents/` contém agentes operacionais; CLI não executa agentes. | Suportar múltiplos runtimes por adapters, sem transformar nenhum agente ou IDE em núcleo. |
| Tratamento de especificações | Specs descrevem comportamento atual; changes carregam delta specs que podem ser arquivadas para atualizar a fonte de verdade. | Specs são artefatos centrais do SDD; o fluxo separa especificação, planejamento, tarefas e implementação. | Specs canônicas `0001` a `0014` existem e são mais amplas que o código atual. | Specification First com Specification Providers múltiplos e Markdown canônico como formato interno. |
| Planejamento e decomposição de tarefas | Artifacts seguem dependências configuráveis por schema; tasks são checklist para implementação. | Plan e tasks estruturam implementação; tasks podem incluir dependências, paralelismo e fases por user story. | Task Queue, Workflow Engine e Mission Runner existem em MVP, mas ainda não formam fluxo padrão completo. | Handoff Mission -> Workflow -> Task Queue com estado, validação, replanejamento e evidências. |
| Políticas e permissões | Config de projeto pode injetar contexto e regras por artifact; políticas de execução governada não aparecem como responsabilidade central nas fontes consultadas. | Constituição registra princípios; extensions/presets podem adicionar gates; permissões operacionais detalhadas não aparecem como responsabilidade central nas fontes consultadas. | Contrato base de missão, permissões excepcionais e Guardian/Policy MVP existem. | Policy Engine e Guardian Engine governando permissões, risco, contexto, tools, providers e commits. |
| Seleção de modelos, providers e runtimes | Documenta suporte a várias ferramentas e recomenda modelos de alto raciocínio; seleção automática de modelo/provider não é apresentada como responsabilidade central nas fontes consultadas. | Suporta múltiplas integrações de agentes; seleção automática de modelo/provider não é apresentada como responsabilidade central nas fontes consultadas. | Model Selection Engine MVP com catálogo em memória; Provider Gateway e Runtime Adapter MVP; sem descoberta real ou provider real integrado. | Selecionar modelo por política, custo, qualidade, raciocínio, contexto, disponibilidade e fallback, sem hardcode de provider. |
| Contexto e orçamento de tokens | Contexto de projeto pode ser injetado nos artifacts; há orientação de higiene de contexto. Orçamento formal de tokens não foi identificado nas fontes oficiais consultadas como responsabilidade central. | Comandos e templates fornecem contexto estruturado por artefatos; orçamento formal de tokens não foi identificado nas fontes oficiais consultadas como responsabilidade central. | Context Router e Token Budget Manager determinísticos existem, com integração parcial ao Model Selection. | Context Router como fronteira obrigatória para seleção, citação, omissão, redaction e orçamento. |
| Fila e execução em batch | Workflow trabalha por changes; batch de execução governada não foi identificado como responsabilidade central nas fontes consultadas. | Workflows podem automatizar processos com loops, fan-out/fan-in, pausas e retomada; batch de missões no estilo VAF não foi identificado nas fontes consultadas. | Fila local de missões e batch seguro sequencial existem e param na primeira falha. | Task Queue e Mission Orchestrator para execução controlada, com batch como suporte operacional, não produto inteiro. |
| Retomada e recuperação | Changes permanecem em diretório e podem ser continuadas; archive preserva histórico. Recuperação operacional de runner não foi identificada como responsabilidade central nas fontes consultadas. | Workflows documentam possibilidade de pausar e retomar; comandos de converge adicionam tarefas remanescentes. | Diretórios de missão, restauração em falha de composição e batch com parada segura existem. | Recuperação de missão, workflow, tasks e auditoria por stores/adapters persistentes governados. |
| Auditoria e evidências | Archive preserva contexto da mudança; validação e status ajudam revisão. Audit/Event Log formal não foi identificado nas fontes consultadas. | Artifacts, checklists, analyze e converge dão rastreabilidade de spec/plan/tasks. Audit/Event Log formal não foi identificado nas fontes consultadas. | Audit/Event Log em memória, persistência JSONL opt-in e logs operacionais existem; integração é parcial/opcional. | Trilha auditável estruturada de decisões, contexto, modelo, execução, validações, falhas e commit. |
| Extensibilidade | Schemas customizáveis, templates, skills, comandos, stores e suporte amplo a ferramentas. | Extensions, presets, workflows, bundles, catalogs e integrações de agentes. | Arquitetura modular com módulos MVP e docs de adapters; extensibilidade ainda não provada em fluxo externo completo. | Tudo substituível por adapters: providers, runtimes, bancos, IDEs, MCPs, stores e mecanismos de execução. |
| Estado de maturidade pública | Projeto público com CLI e documentação oficial; esta comparação não avalia qualidade por adoção. | Projeto público com CLI, documentação, integrações e ecossistema de extensões; esta comparação não avalia qualidade por adoção. | MVP operacional inicial, sem release alfa publicada, sem tag, sem pacote publicado e com gates reprovados/pendentes. | Alfa futura somente após fluxo de valor integrado mínimo, licença, instalação limpa, CI confirmado e autorização explícita. |
| Papel de Git | Changes e archive preservam histórico em arquivos versionáveis; não substitui Git. | Workflow cria branches/artefatos e trabalha com repositório; não substitui Git. | Git é usado para rastreabilidade e commits por missão no fluxo operacional. | Commits vinculados a missão, Spec, evidências e validações. |
| Escopo de produto | Ferramenta de SDD leve, iterativa e voltada a changes/specs. | Toolkit de SDD com fases, integrações, extensões, presets, workflows e bundles. | Framework de Harness Engineering em construção, com documentação maior que maturidade funcional. | Plataforma governada para orquestrar desenvolvimento com IA por Specs, políticas, contexto, agentes, capabilities e adapters. |
| Relação com ferramentas completas de SDD | É uma ferramenta completa de SDD segundo sua proposta oficial. | É uma ferramenta completa de SDD segundo sua proposta oficial. | Não pretende substituir ferramentas completas de SDD no estado atual. | Poder integrar ou consumir especificações de ferramentas de SDD por adapters conceituais. |
| Risco de escopo | Não avaliado aqui além do documentado oficialmente; sua filosofia enfatiza leveza e iteração. | Não avaliado aqui além do documentado oficialmente; o fluxo é mais estruturado por fases e gates. | Risco de o Mission Runner/batch parecer o produto inteiro e de a documentação sugerir maturidade maior que a implementação. | Mitigar com status factual, fluxo integrado mínimo e documentação separando atual, planejado e hipótese. |
| Hipótese de integração | OpenSpec poderia ser fonte de Specs para o VAF, mas isso não foi implementado no VAF. | Spec Kit poderia ser fonte de Specs para o VAF, mas isso não foi implementado no VAF. | Nenhum adapter `SpecificationProvider` existe hoje. | Hipótese: `SpecificationProvider` com `OpenSpecProvider`, `SpecKitProvider` e `NativeMarkdownProvider`. |

## Pontos De Sobreposição

- Os três projetos partem da premissa de que especificações reduzem improviso no desenvolvimento assistido por IA.
- OpenSpec e Spec Kit estruturam artefatos antes da implementação e usam agentes de codificação como executores.
- VAF também usa Specs e missões, mas acrescenta uma ambição explícita de governança operacional, políticas, orçamento de tokens, seleção de modelo, auditabilidade e adapters de provider/runtime.
- OpenSpec, Spec Kit e VAF valorizam extensibilidade, embora em níveis diferentes: workflows/schemas no OpenSpec, extensions/presets/workflows/bundles no Spec Kit e adapters/capabilities/policies no VAF.

## Diferenças Reais

- OpenSpec documenta uma abordagem leve e iterativa baseada em changes, delta specs e archive.
- Spec Kit documenta um fluxo SDD mais faseado, com constituição, especificação, plano, tarefas, análise, implementação e convergência.
- VAF atualmente comprova principalmente operação local de missões, contratos MVP e governança parcial; sua visão é mais ampla que sua implementação atual.
- OpenSpec e Spec Kit focam em organizar o trabalho de especificação e execução com agentes; VAF pretende focar na camada de harness governado entre missão, políticas, contexto, agentes, tools, providers e evidências.

## Possibilidades De Integração

- OpenSpec poderia fornecer changes e specs como entrada para missões VAF.
- Spec Kit poderia fornecer spec/plan/tasks como entrada para missões ou workflows VAF.
- VAF poderia consumir artefatos de ambos como documentos canônicos em Markdown, desde que preserve autoria, rastreabilidade e semântica de origem.
- VAF poderia aplicar Policy Engine, Guardian Engine, Context Router, Model Selection e Audit/Event Log sobre execuções derivadas desses artefatos.

## Fronteira Arquitetural: SpecificationProvider

Uma fronteira semelhante a `SpecificationProvider` é uma hipótese arquitetural, não uma decisão tomada e não uma implementação existente.

Adaptadores conceituais possíveis:

- `OpenSpecProvider`: leitura de specs e changes do OpenSpec.
- `SpecKitProvider`: leitura de specs, planos e tasks do GitHub Spec Kit.
- `NativeMarkdownProvider`: leitura de Markdown canônico nativo do VAF.

Status desta hipótese:

- hipótese arquitetural;
- decisão pendente;
- não implementada;
- sujeita às missões de integração 0104-0108;
- não materializada nesta missão em interfaces Python, classes, módulos, Specs ou ADRs.

## Riscos De Duplicação

- Duplicar fluxos SDD já bem definidos por OpenSpec ou Spec Kit sem acrescentar governança real.
- Criar um `SpecificationProvider` prematuro antes de demonstrar o fluxo Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider.
- Tratar OpenSpec ou Spec Kit como dependência central em vez de possíveis fontes/adapters.
- Misturar semânticas de change, spec, plan, task e missão sem mapeamento explícito.
- Usar documentação de integração como prova de que integração existe.

## Limitações Da Comparação

- As conclusões sobre OpenSpec e Spec Kit se limitam às fontes oficiais consultadas em 2026-07-11.
- Não foi feita instalação, execução local, benchmark, auditoria de código ou comparação de qualidade interna desses projetos.
- Não foram usados blogs, vídeos, agregadores ou comparações de terceiros como fonte principal.
- Não foi avaliada adoção, popularidade, estrelas, downloads ou comunidade como critério de qualidade.
- Não afirmar que uma capacidade não existe significa apenas que ela não foi identificada nas fontes oficiais consultadas.

## Estado Atual Versus Visão Pretendida Do VAF

Estado atual comprovado:

- fila local de missões, runner seguro individual e batch seguro;
- parada na primeira falha, recuperação operacional parcial e bloqueio de push automático por padrão;
- composição determinística de contexto de missão;
- contrato base, agente executor base e formato compacto;
- CLI diagnóstica e validação local de links;
- módulos MVP para Policy, Guardian, Context, Model Selection, Knowledge, Runtime, Provider, Agents, Capabilities, Skills, Tools, Audit e Persistence;
- ausência de fluxo público completo de ponta a ponta;
- ausência de providers reais, persistência externa, Semantic Index, embeddings, pgvector, RAG e internacionalização.

Visão pretendida:

- transformar objetivo e Spec em missão executável;
- decompor missão em workflow, tasks e agentes;
- resolver capabilities por skills e tools governadas;
- passar por Policy Engine, Guardian Engine, Context Router, Token Budget Manager e Model Selection;
- executar por Runtime Adapter e Provider Gateway;
- registrar evidências auditáveis e vincular validações ao commit.

## Conclusão Factual

OpenSpec e GitHub Spec Kit são referências oficiais de processos orientados por especificações para agentes de codificação. Eles podem ser complementares ao VAF como fontes de especificações, processos ou artefatos, desde que a integração seja feita por fronteiras claras.

O VAF não deve ser apresentado como substituto direto desses projetos no estado atual. Sua contribuição pretendida é uma camada de execução governada e auditável ao redor de missões, agentes, políticas, contexto, modelos, runtimes, providers, validações e evidências. Essa contribuição ainda precisa ser demonstrada por fluxo integrado mínimo nas missões posteriores.

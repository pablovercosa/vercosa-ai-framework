# Alignment Review 2026-07-03

## 1. Resumo executivo

O alinhamento arquitetural atual está majoritariamente coerente com a identidade do Vercosa AI Framework como framework próprio de AI Specification-Driven Engineering.

A documentação recém-criada posiciona corretamente o projeto como um framework Specification First, AI Native, Provider Agnostic, Local First e Governance by Design. Também diferencia com clareza o núcleo conceitual dos adapters, runtimes, providers, MCPs e frameworks externos.

O ponto crítico é que a documentação já descreve uma arquitetura mais madura do que a integração real implementada. Isso está declarado nos documentos, mas precisa continuar explícito para evitar que contratos MVP sejam confundidos com fluxo completo de ponta a ponta.

## 2. Veredito: o projeto está coerente ou não?

Veredito: coerente com ressalvas críticas.

O projeto está coerente no posicionamento arquitetural, na separação de responsabilidades e na documentação das lacunas. Não há evidência de que OpenCode, MCPs, LangGraph, AutoGen, MetaGPT ou ECC estejam sendo tratados como núcleo.

A ressalva é que ainda existem bloqueios arquiteturais antes da próxima implementação funcional:

- fronteira entre Policy Engine e Guardian Engine;
- fronteira entre Mission Runner e Mission Orchestrator;
- ausência de Context Router e Token Budget Manager como contratos formais;
- ausência de integração real Mission -> Workflow -> Task Queue -> Agent Orchestrator -> Capability -> Skill -> Tool -> Provider;
- ausência de registro formal de aprovação de Spec, Plan e Validation Result no ciclo SDD.

## 3. Pontos fortes do estado atual

- O README principal posiciona o Vercosa como framework próprio, não como IDE, MCP server, agente único ou wrapper de runtime.
- OpenCode está corretamente descrito como runtime inicial e laboratório, atrás de `runtime/`, não como centro arquitetural.
- Claude Code, Codex CLI, Cursor, IDEs, Web UI e API estão tratados como adapters futuros.
- LangGraph, MetaGPT e AutoGen estão posicionados como referências ou adapters opcionais, não como dependências de núcleo.
- MCPs estão corretamente posicionados abaixo de Tools/Providers, nunca como dependência direta de Agents.
- A cadeia Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider está documentada de forma consistente em `README.md`, `architecture-map.md`, `module-index.md`, Specs 0006-0010 e `sdd-lifecycle.md`.
- A documentação separa estado desejado de MVP atual, especialmente em `current-state.md` e `architecture-map.md`.
- Knowledge Hub, Canonicalizer e Persistence estão separados, evitando a armadilha de tratar memória como um subsistema único e mágico.
- A documentação rejeita explicitamente a ideia de "memória infinita" literal e a substitui por armazenamento durável, canonicalização, índices derivados, recuperação governada, citações e políticas.
- Token Efficiency aparece como princípio transversal nas Specs, no README e nos documentos de alinhamento.
- O ciclo SDD está definido como Spec -> Plan -> Tasks -> Implement -> Validate -> Commit, com auto-commit desabilitado por padrão.
- Os READMEs de módulos revisados seguem, em geral, o padrão navegável: objetivo, faz/não faz, arquivos, tipos, entradas/saídas, dependências, módulos relacionados, Specs, docs, status e próximos passos.

## 4. Inconsistências encontradas

- A documentação usa `Policy Engine / Guardian Engine` em vários pontos, mas as Specs ainda não definem se o Guardian é o Policy Engine concreto da fase atual ou se haverá um Policy Engine separado acima dele.
- `Mission Runner` existe como MVP operacional, enquanto `Mission Orchestrator` é conceitual. A documentação reconhece isso, mas qualquer nova implementação em `missions/` pode aumentar o risco de acumular orquestração no Runner.
- `Workflow Engine` e `Task Queue` estão documentados como camadas separadas, mas a execução real ainda não usa Task Queue como substrate padrão do Workflow Engine.
- `Agent Orchestrator`, `Capabilities`, `Skills`, `Tools` e `Provider Gateway` existem como contratos/MVPs, mas ainda não formam o caminho padrão de execução fim a fim.
- Token Efficiency está bem representado como princípio, mas ainda não existe contrato formal de Context Router, Context Package ou Token Budget Manager.
- SDD está conceitualmente definido, mas ainda faltam artefatos formais para Spec Approval Record, Plan Record, Task Record, Validation Result e Commit Decision Record.
- As Specs 0002-0013 estão marcadas como `Proposta`, enquanto há MVPs implementados para vários módulos relacionados. Isso não invalida o alinhamento, mas reforça a necessidade de registrar claramente qual implementação é experimental/MVP e qual Spec está formalmente aprovada.

## 5. Lacunas críticas

- Decidir Policy Engine versus Guardian Engine antes de qualquer nova integração funcional.
- Definir Context Router como módulo ou contrato formal antes de implementar memória semântica, embeddings, pgvector ou expansão de retrieval.
- Definir Token Budget Manager ou, no mínimo, incorporá-lo explicitamente ao contrato do Context Router.
- Formalizar Mission Orchestrator antes de expandir Mission Runner.
- Definir contrato Mission Runner -> Workflow Engine -> Task Queue.
- Definir contrato Task Queue -> Agent Orchestrator -> Capability Resolver.
- Definir registro de aprovação de Spec e Plan antes de automatizar implementação além do MVP atual.
- Definir Validation Result persistível antes de automatizar conclusão de task, missão ou commit.

## 6. Lacunas importantes, mas não bloqueantes

- RuntimeAdapter conformance para Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.
- Catálogo inicial de capabilities, skills, tools e providers seguros.
- ADR de posicionamento final para LangGraph, MetaGPT e AutoGen.
- ADR de placement e safety review para MCP adapters.
- Persistência final de audit logs, model decisions, guardian decisions e knowledge documents.
- Schema final de Semantic Index e chunking por domínio.
- Adapters concretos de PostgreSQL, pgvector, SQLite, Docling ou OCR.
- Política de retenção para conversas, prompts, logs, decisões e knowledge artifacts.
- Testes de contrato entre portas e adapters.

## 7. Próxima implementação recomendada

Recomendação: não iniciar uma feature funcional nova ainda.

A próxima etapa deve ser uma decisão arquitetural documentada:

1. ADR: Policy Engine versus Guardian Engine.
2. Spec ou ADR: Context Router + Token Budget Manager + Memory Architecture.

Se for necessário escolher uma única próxima implementação, ela deve ser o contrato do Context Router, mas somente depois de resolver a fronteira Policy/Guardian ou registrá-la explicitamente como decisão provisória.

## 8. Justificativa para a próxima implementação

O Context Router é o próximo componente de maior alavancagem porque conecta Knowledge Hub, Semantic Index, Model Selection, Guardian, Agent Orchestrator e Token Efficiency.

Sem ele, qualquer implementação de memória, embeddings, pgvector ou RAG tende a virar expansão de prompt sem governança, com risco de custo alto, vazamento de contexto, baixa relevância, prompt injection e perda de rastreabilidade.

Porém, o Context Router depende de decisões de política. Ele precisa saber quem resolve precedência, redaction, privacidade, custo, token budget, contexto sensível e bloqueios. Por isso a decisão Policy Engine versus Guardian Engine vem antes ou deve ser tomada como premissa explícita no mesmo ADR.

## 9. O que NÃO deve ser implementado ainda

- Não implementar pgvector como default obrigatório.
- Não implementar embeddings antes do contrato de Context Router e Semantic Index.
- Não implementar "memória infinita" como feature ou promessa literal.
- Não conectar agentes diretamente a MCPs, bancos, APIs, filesystem ou providers.
- Não acoplar LangGraph, MetaGPT ou AutoGen ao núcleo.
- Não expandir OpenCode para dentro de Mission Runner, Workflow Engine ou Agent Orchestrator.
- Não adicionar novos runtimes antes de conformance tests de RuntimeAdapter.
- Não implementar paralelismo multi-agent sem locks, orçamento, limites e validação.
- Não implementar auto-commit como default.
- Não implementar adapters PostgreSQL/SQLite/pgvector antes de estabilizar portas de persistência e schemas lógicos.

## 10. Riscos se o projeto continuar sem resolver as lacunas

- OpenCode pode virar núcleo acidental por conveniência operacional.
- Guardian, runtime, tools, providers e CLI podem duplicar lógica de política.
- Mission Runner pode absorver responsabilidades de Mission Orchestrator e Workflow Engine.
- Semantic search pode virar mecanismo de despejo de contexto em prompts.
- Token Efficiency pode permanecer princípio abstrato sem enforcement operacional.
- Agents podem ganhar acesso indireto ou direto a tools, MCPs e providers fora da cadeia governada.
- Persistência pode se fragmentar entre filesystem, memória, logs e futuros bancos sem rastreabilidade consistente.
- SDD pode ficar apenas documental se Spec approval, Plan, Tasks, Validation e Commit não virarem artefatos verificáveis.
- O framework pode perder provider agnosticism ao otimizar cedo para PostgreSQL, pgvector, Ollama ou OpenCode.

## 11. Checklist objetivo para avançar

- [ ] Criar ADR para Policy Engine versus Guardian Engine.
- [ ] Definir onde a precedência de políticas é resolvida.
- [ ] Definir contrato mínimo de Context Router.
- [ ] Definir contrato mínimo de Token Budget Manager ou incorporá-lo ao Context Router.
- [ ] Definir Context Package com citações, redactions, token estimate, omitted-context reasons e policy refs.
- [ ] Definir relação Context Router -> Knowledge Hub -> Semantic Index -> Model Selection -> Guardian.
- [ ] Definir Mission Runner versus Mission Orchestrator.
- [ ] Definir contrato Mission Runner -> Workflow Engine.
- [ ] Definir contrato Workflow Engine -> Task Queue.
- [ ] Definir contrato Task Queue -> Agent Orchestrator.
- [ ] Definir contrato Agent Orchestrator -> Capability Resolver.
- [ ] Definir artefatos mínimos do SDD: Spec Approval Record, Plan Record, Task Record, Validation Result e Commit Decision Record.
- [ ] Manter pgvector, Ollama, PostgreSQL, LangGraph, AutoGen, MetaGPT, Claude Code, Codex CLI e MCPs como adapters, integrações futuras ou referências.
- [ ] Não iniciar nova implementação funcional enquanto as decisões críticas acima estiverem ambíguas.

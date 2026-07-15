# Marcos Por Faixa De Missões

Links principais: [README principal](../../README.md) | [Estado atual](../alignment/current-state.md) | [Checklist de implementação](../alignment/implementation-status.md) | [Auditoria de aderência](../audits/objective-and-scope-alignment-audit.md) | [Backlog estratégico](../roadmap/mission-backlog.md)

## Objetivo

Registrar marcos factuais por faixa de missões concluídas. Este documento não é backlog e não autoriza novas missões.

A série versionada disponível em `missions/done/` começa em `0002`. Não existe evidência suficiente de que uma missão `0001` tenha sido perdida, apagada ou executada.

O identificador `0001` fica reservado como marco histórico da fundação prévia à série versionada. Essa reserva evita renumeração retroativa, não representa missão concluída, não aumenta contadores de missões executadas e não deve aparecer em `missions/queue`, `missions/running`, `missions/done` ou `missions/failed`.

Antes da execução da missão 0109, `missions/done/` continha arquivos de `0002` a `0108`, totalizando 107 missões concluídas. O maior identificador disponível era `0108`, mas a quantidade factual concluída era 107 porque `0001` é reservado e não executado.

## 0002-0025

Objetivo da faixa: criar a fundação técnica inicial do framework e os primeiros motores centrais.

Principais entregas:

- Spec e MVP do Model Selection Engine.
- Skeleton Python do framework.
- Spec e MVP do OpenCode Runtime Adapter.
- Spec e MVP do Mission Runner.
- CLI inicial para runner.
- Spec, contratos, MVP e CLI do Guardian Engine.
- Spec, contratos e MVP do Workflow Engine.
- Spec, contratos e MVP do Task Queue.
- Spec, contratos e MVP do Agent Orchestrator.

Mudanças de direção:

- OpenCode foi tratado como runtime adapter inicial, não como núcleo.
- O projeto começou a formalizar módulos em Python antes do fluxo completo estar integrado.

Limitações:

- Integração ponta a ponta ainda ausente.
- Model Selection e runtime ainda dependiam de catálogos e adapters iniciais.

Resultado: fundação modular criada, com contratos e MVPs iniciais suficientes para avançar para capabilities, providers, conhecimento e persistência.

## 0026-0050

Objetivo da faixa: expandir a arquitetura para capabilities, skills, tools, providers, Knowledge Hub, canonicalização, persistência, documentação e contexto.

Principais entregas:

- Spec, contratos e MVP de Capabilities, Skills e Tools.
- Spec, contratos e MVP do Provider Gateway.
- Spec, contratos e MVP do Knowledge Hub.
- Spec, contratos e MVP do Canonicalizer.
- Spec, contratos e MVP de Persistence Layer com filesystem.
- Checkpoint de alinhamento arquitetural.
- Padrão de README e documentação.
- ADR Policy Engine versus Guardian Engine.
- Arquitetura, contratos e MVP de Context Router e Token Budget Manager.
- Integração Context Router com Knowledge Hub.
- Padrão pt-BR para documentação e commits.

Mudanças de direção:

- Separação explícita entre Policy Engine e Guardian Engine.
- Context Router e Token Budget Manager passaram a ser componentes de primeira classe.
- Documentação em português do Brasil foi consolidada como regra.

Limitações:

- Muitos módulos passaram a existir como MVPs isolados.
- Capabilities, skills, tools e providers ainda não eram fluxo obrigatório de execução real.

Resultado: arquitetura ficou mais completa, mas também mais ampla que o fluxo executável comprovado.

## 0051-0075

Objetivo da faixa: conectar governança, contexto, model selection, auditoria, runners seguros, batch e CLI operacional.

Principais entregas:

- Guardian checks para `ContextPackage`.
- Runner seguro de missão e teste documental do runner.
- Policy Engine contracts e integrações com Guardian, Context Router e Model Selection.
- Usage/API Limit Guard.
- Runner seguro em batch.
- Backlog estratégico, playbook de batch e checklist pós-batch.
- Integração de Token Budget com Model Selection.
- Integração de Usage/API Limit Guard ao worker.
- Audit/Event Log inicial, eventos de decisões e integração opcional ao Mission Runner.
- CLI operacional inicial com `validate`, `doctor`, exemplos e comandos de apoio.
- README atualizado com Harness Engineering.
- Batch consolidado como fluxo operacional quando seguro.

Mudanças de direção:

- O processo de missões e batch virou fluxo operacional padrão interno.
- Auditoria e eventos foram introduzidos como suporte à governança.

Limitações:

- Integrações centrais eram majoritariamente opcionais e acionadas por chamador explícito.
- O fluxo operacional real continuou mais forte em scripts/runner do que na cadeia completa de agentes.

Resultado: o projeto ganhou operacionalidade interna real, mas aumentou o risco de o runner/batch parecer o produto principal.

## 0076-0100

Objetivo da faixa: preparar documentação pública, segurança, contribuição, release alfa futura, empacotamento, CI e validações locais.

Principais entregas:

- Arquitetura de Audit/Event Log.
- Guia público de instalação local e guia de contribuição.
- Documentação legal inicial, segurança, código de conduta e templates de issue/PR.
- CHANGELOG inicial.
- Plano da versão alfa `0.1.0-alpha.1`.
- Checklist de instalação limpa e registro de validação limpa `REPROVADO`.
- Comandos CLI `missions`, `batch-summary`, `docs-links` e `alpha-readiness`.
- Persistência local JSONL opt-in para eventos auditáveis.
- Empacotamento Python mínimo em `pyproject.toml`.
- CI mínimo com GitHub Actions.
- Política de release, checklist pré-tag e release notes alfa preliminares.
- Diagnóstico local de prontidão alfa `NÃO PRONTO`.
- Execução local do checklist pré-tag `REPROVADO`.
- Consolidação local do candidato alfa e solicitação futura de decisão de tag.

Mudanças de direção:

- O projeto avançou fortemente em preparação pública e release, mesmo mantendo bloqueios explícitos.
- A documentação passou a registrar com clareza que alfa, tag, release e pacote ainda não existem.

Limitações:

- `LICENSE` permanece ausente.
- Instalação limpa histórica permanece reprovada.
- CI remoto ainda depende de confirmação após push aplicável.
- A preparação alfa ocorreu antes de um fluxo central completo de valor externo.

Resultado: preparação alfa ficou documentada de forma conservadora, mas a decisão correta no estado atual é adiar publicação até resolver bloqueios e demonstrar fluxo integrado mínimo.

## 0101-0110

Objetivo da faixa: auditar aderência ao objetivo original, consolidar infraestrutura de execução de missões, explicitar fluxo de valor, integrar caminhos mínimos entre motores centrais, revisar Specs/ADRs afetadas, reduzir duplicação documental e reavaliar prontidão alfa.

Principais entregas:

- Auditoria estratégica de aderência ao objetivo e escopo original.
- Checklist factual de implementação.
- Contrato base versionado `v1` para execução de missões.
- Agente executor base operacional em `.opencode/agents/`.
- Formato compacto de missão para a série a partir de `0103`.
- Compositor obrigatório de contexto integrado ao runner shell.
- README principal revisado para explicitar fluxo de valor, consumidores plausíveis, limites e comparação factual com OpenSpec e GitHub Spec Kit.
- Integração mínima Mission Runner -> Workflow Engine -> Task Queue por contratos injetáveis.
- Integração mínima Task Queue -> Agent Orchestrator -> Capability Resolver.
- Integração Capability -> Skill -> Tool -> Provider Gateway em dry-run governado.
- Integração mínima local de Policy, Context Router, Token Budget, Guardian, Model Selection e Audit/Event Log no caminho de execução governado.
- Revisão documental de Specs e ADRs afetadas pelas integrações 0104 a 0107.
- Consolidação de `docs/alignment/implementation-status.md` como checklist factual canônico.
- Reavaliação de prontidão alfa 0110 com classificação `NÃO PRONTO`, preservando gates atendidos e bloqueios persistentes.

Limitações:

- A composição de prompt não substitui sandbox técnico completo.
- Missões legadas continuam compatíveis e não foram reescritas.
- O fluxo arquitetural Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider Gateway possui demonstração mínima local e dry-run governado, mas providers reais, rede, banco, MCP, API externa, RAG, PostgreSQL, pgvector, múltiplos runtimes reais e release alfa permanecem fora do estado validado.

Resultado: o ciclo 0101-0110 alinhou o projeto ao objetivo original, comprovou integrações mínimas locais, consolidou fontes canônicas e concluiu que a futura alfa pública permanece `NÃO PRONTO` até resolução ou exceção explícita dos bloqueios persistentes de release, licença, instalação limpa, canais públicos, autorização, tag, release e pacote.

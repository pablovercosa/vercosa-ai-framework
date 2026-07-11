# Marcos Por Faixa De Missões

Links principais: [README principal](../../README.md) | [Estado atual](../alignment/current-state.md) | [Checklist de implementação](../alignment/implementation-status.md) | [Auditoria de aderência](../audits/objective-and-scope-alignment-audit.md) | [Backlog estratégico](../roadmap/mission-backlog.md)

## Objetivo

Registrar marcos factuais por faixa de missões concluídas. Este documento não é backlog e não autoriza novas missões.

A série versionada disponível em `missions/done/` começa em `0002`. Esta auditoria não presume, sem evidência, que uma missão `0001` foi perdida ou removida.

Na leitura atual, `missions/done/` contém arquivos de `0002` a `0100`, totalizando 99 entradas. A numeração alcançada sugere 99 IDs nessa faixa e não há inconsistência apenas por ausência de `0001`, pois a série disponível começa em `0002`.

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

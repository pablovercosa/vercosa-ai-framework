---
id: "0110"
title: "Reavaliar prontidão alfa após integração mínima"
base_contract: "v1"
roles:
  - release-readiness-auditor
  - architecture-reviewer
  - documentation-engineer
  - test-engineer
agents:
  - framework-architect
network: deny
database: deny
providers: deny
git_push: deny
git_tag: deny
release: deny
package_publish: deny
sudo: deny
destructive_commands: deny
---

# Objetivo

Reavaliar factualmente a prontidão do Vercosa AI Framework para uma futura
alfa pública após a conclusão do ciclo de integração e consolidação documental
das missões 0101 a 0109.

Classificar o estado atual sem criar tag, release, pacote, licença ou novas
funcionalidades.

Encerrar documentalmente o ciclo 0101-0110 e registrar os gates que deverão
orientar o próximo ciclo.

# Contexto Específico

As missões 0104 a 0107 validaram o fluxo mínimo governado:

Mission Runner
-> Workflow Engine
-> Task Queue
-> Agent Orchestrator
-> Policy
-> Context Router
-> Token Budget
-> Guardian
-> Model Selection
-> Capability
-> Skill
-> Tool
-> Provider Gateway em dry-run
-> Runtime injetado
-> Audit/Event Log

A missão 0108 revisou Specs e ADRs afetados.

A missão 0109 consolidou
`docs/alignment/implementation-status.md` como checklist factual canônico e
reduziu duplicações documentais.

Estado confirmado antes da criação desta missão:

- missão 0109 concluída no commit
  `d55084dc2004ca8205513974a6e3f407c5d44d24`;
- `queue=0`;
- `running=0`;
- `done=108`;
- `failed=0`;
- 500 testes aprovados;
- compileall aprovado;
- CI remoto informado pelo mantenedor como aprovado no run
  `29357276490` para o commit da missão 0109.

A evidência de CI foi fornecida pelo mantenedor. Como esta missão não possui
rede, ela deve ser identificada como evidência externa informada e não como
consulta realizada pelo agente.

Registros históricos anteriores permanecem válidos para os commits e datas que
avaliaram:

- `alpha-readiness-diagnostic.md`: `NÃO PRONTO`;
- `pre-tag-checklist-execution.md`: `REPROVADO`;
- `clean-install-validation.md`: `REPROVADO`.

Esses relatórios não devem ser reescritos retrospectivamente.

Durante a execução desta missão, `missions/running` e o Git podem aparecer
temporariamente alterados pelo próprio runner. Distinguir:

- estado operacional transitório da missão;
- bloqueio persistente do projeto;
- ressalva;
- gate já atendido;
- evidência histórica que exige reexecução.

Não usar `running=1` ou a movimentação do arquivo da própria missão como único
fundamento da classificação final.

# Entradas Específicas

Revisar, no mínimo:

- `docs/alignment/implementation-status.md`;
- `docs/alignment/current-state.md`;
- `docs/alignment/architecture-map.md`;
- `docs/alignment/roadmap.md`;
- `docs/alignment/open-questions.md`;
- `docs/roadmap/mission-backlog.md`;
- `docs/history/mission-milestones.md`;
- `docs/architecture/post-integration-architecture-review.md`;
- `docs/audits/spec-adr-integration-review-0108.md`;
- `docs/audits/documentation-deduplication-0109.md`;
- `docs/release/public-alpha-readiness.md`;
- `docs/release/alpha-readiness-diagnostic.md`;
- `docs/release/pre-release-checklist.md`;
- `docs/release/pre-tag-checklist-execution.md`;
- `docs/release/clean-install-validation.md`;
- `docs/release/alpha-candidate-summary.md`;
- `docs/release/tag-decision-request.md`;
- `docs/release/release-notes-alpha.md`;
- `docs/release/release-policy.md`;
- `docs/legal/license-notes.md`;
- `README.md`;
- `CHANGELOG.md`;
- `SECURITY.md`;
- `CODE_OF_CONDUCT.md`;
- `pyproject.toml`;
- `.github/workflows/ci.yml`;
- testes das integrações 0104 a 0107;
- estado local das missões e do Git.

`implementation-status.md` continua sendo a fonte canônica de implementação.

Documentos de release continuam sendo as fontes das evidências e gates de
release.

# Avaliação Obrigatória

Avaliar separadamente:

1. fluxo de valor mínimo integrado;
2. cobertura local de testes;
3. compilação;
4. documentação canônica;
5. CI mínimo;
6. instalação limpa;
7. licença;
8. segurança pública;
9. código de conduta e canais públicos;
10. release notes;
11. política de versão e release;
12. estado de missões;
13. limpeza do Git;
14. autorização humana;
15. tag;
16. GitHub Release;
17. publicação de pacote;
18. limitações assumidas da alfa.

Para cada gate registrar:

- estado;
- evidência;
- tipo de evidência;
- persistente ou transitório;
- bloqueador, ressalva ou atendido;
- ação necessária;
- possibilidade ou não de exceção explícita.

# Classificação

Usar exatamente uma classificação final:

- `PRONTO`;
- `PRONTO COM RESSALVAS`;
- `NÃO PRONTO`.

Não predeterminar artificialmente o resultado.

Não promover o estado apenas porque testes e CI passaram.

Não reprovar apenas porque o arquivo da própria missão está temporariamente em
`missions/running`.

Bloqueios persistentes sem resolução ou exceção explícita devem prevalecer
sobre evidências positivas parciais.

# Entregáveis

Criar:

- `docs/release/alpha-readiness-reassessment-0110.md`.

O relatório deve conter:

- data e commit avaliados;
- objetivo;
- limites;
- fontes consultadas;
- resumo das integrações 0104-0107;
- efeitos das revisões 0108 e 0109;
- matriz de gates;
- comparação com os diagnósticos históricos;
- bloqueios persistentes;
- ressalvas;
- gates atendidos;
- classificação final;
- justificativa;
- riscos;
- recomendação sobre tag;
- recomendação sobre release;
- recomendação sobre pacote;
- próximos passos priorizados;
- encerramento factual do ciclo 0101-0110.

Atualizar minimamente, apenas quando necessário:

- `docs/release/public-alpha-readiness.md`;
- `docs/alignment/implementation-status.md`;
- `docs/alignment/current-state.md`;
- `docs/alignment/roadmap.md`;
- `docs/alignment/open-questions.md`;
- `docs/roadmap/mission-backlog.md`;
- `docs/history/mission-milestones.md`;
- `CHANGELOG.md`.

Não duplicar a matriz completa de implementação nesses documentos.

Não criar missão 0111.

Não criar backlog executável automaticamente.

# Próximo Ciclo

O relatório deve propor uma sequência priorizada de correções, mas não criar as
missões correspondentes.

Separar recomendações em:

- bloqueadores obrigatórios antes da alfa;
- correções operacionais;
- melhorias recomendadas;
- itens pós-alfa;
- itens explicitamente adiados.

Avaliar especialmente:

- decisão e criação futura de `LICENSE`;
- nova validação de instalação limpa;
- diretórios operacionais em clone limpo;
- portabilidade de scripts;
- canal público de segurança;
- canal para problemas de conduta;
- revisão final das release notes;
- reexecução futura do checklist pré-tag;
- autorização explícita de tag e release.

# Limites

Esta missão não deve:

- alterar `src/`;
- alterar `tests/`;
- alterar `scripts/`;
- alterar `.github/`;
- alterar `pyproject.toml`;
- alterar `AGENTS.md`;
- alterar Specs;
- alterar ADRs aceitos;
- criar `LICENSE`;
- decidir qual licença será adotada;
- corrigir instalação limpa;
- corrigir scripts;
- criar canal público;
- implementar provider real;
- acessar rede;
- acessar banco;
- criar tag;
- publicar release;
- publicar pacote;
- fazer push;
- criar missão 0111;
- mover manualmente o próprio arquivo para `missions/done`.

# Critérios Específicos De Aceite

A missão será aceita somente se:

- o relatório `alpha-readiness-reassessment-0110.md` existir;
- todos os gates possuírem evidência e classificação;
- bloqueios transitórios estiverem separados dos persistentes;
- os relatórios históricos permanecerem inalterados em suas conclusões;
- a classificação final for conservadora e justificável;
- a decisão sobre tag estiver explícita;
- a decisão sobre release estiver explícita;
- a decisão sobre pacote estiver explícita;
- o ciclo 0101-0110 estiver encerrado documentalmente;
- próximos passos estiverem priorizados sem criar novas missões;
- nenhuma alteração em código, testes, scripts ou CI ocorrer;
- nenhum arquivo `LICENSE` for criado;
- nenhuma tag ou release for criada;
- `pytest` passar;
- `python3 -m compileall src` passar;
- `docs-links` passar;
- `git diff --check` passar;
- o diff completo for revisado;
- a missão produzir um único commit próprio.

Executar `alpha-readiness`, `doctor` e demais diagnósticos em modo de captura.

Resultados não zero esperados por bloqueios reais devem ser registrados e
interpretados, sem serem mascarados e sem interromper indevidamente a missão.

# Referência Operacional

O contrato base de execução está em
`missions/base/EXECUTION_CONTRACT.md` e é composto obrigatoriamente pelo
runner.

Não copie o contrato para dentro da missão.

A movimentação final de `missions/running` para `missions/done` é
responsabilidade exclusiva do runner seguro.

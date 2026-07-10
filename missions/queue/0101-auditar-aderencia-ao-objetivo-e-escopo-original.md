Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
- pyproject.toml
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/release/public-alpha-readiness.md
- docs/release/alpha-version-plan.md
- docs/release/release-policy.md
- docs/release/pre-release-checklist.md
- docs/release/release-notes-alpha.md
- docs/release/clean-install-validation.md
- docs/release/alpha-readiness-diagnostic.md
- docs/release/pre-tag-checklist-execution.md
- docs/release/alpha-candidate-summary.md
- docs/release/tag-decision-request.md
- src/
- tests/
- scripts/
- missions/done/

Leia também, se existirem:
- logs/pre-audit-model-selection-core-followup.md
- logs/pre-audit-targeted-module-verification.md
- logs/pre-audit-dynamic-module-usage.md
- logs/pre-audit-entrypoint-reachability.md
- logs/pre-audit-traceability-integration.md
- logs/pre-audit-agents-skills-specs.md
- docs/vision/
- docs/specifications/
- docs/specs/
- docs/history/
- docs/audits/
- docs/alignment/implementation-status.md
- docs/history/mission-milestones.md
- .opencode/
- agents/
- skills/
- logs/pre-audit-evidence.md

Assuma o papel de:
- strategic-project-auditor;
- scope-reviewer;
- framework-architect;
- product-alignment-reviewer;
- documentation-agent;
- risk-reviewer.

Missão:
Auditar a aderência de tudo o que foi construído ao objetivo e ao escopo original do Vercosa AI Framework.

Objetivo:
Verificar se os componentes, documentos, scripts, testes, processos e preparações de release criados até a missão 0100 continuam contribuindo diretamente para o propósito original do projeto, identificando desvios de escopo, abstrações prematuras, componentes duplicados, funcionalidades não integradas e esforços desproporcionais.

Princípio central:
Não basta o projeto compilar, passar nos testes e estar bem documentado. É necessário demonstrar que o que foi construído serve ao objetivo real do Vercosa AI Framework.

Contexto:
- Em caso de divergência sobre Core, Guardian ou Model Selection, priorize logs/pre-audit-targeted-module-verification.md e logs/pre-audit-model-selection-core-followup.md sobre o levantamento dinâmico geral, pois as verificações direcionadas corrigiram falsos negativos da instrumentação anterior.
- O projeto completou a faixa de missões até 0100.
- Houve crescimento relevante de arquitetura, documentação, governança, CLI, testes e preparação para alfa.
- Existe risco de o processo de missões ter produzido componentes tecnicamente corretos, mas fora de prioridade ou escopo.
- Existe risco de a preparação de release ter avançado antes de o fluxo central entregar valor concreto.
- Esta missão deve ser estratégica e factual.
- Esta missão não deve remover código.
- Esta missão não deve reestruturar módulos.
- Esta missão não deve criar funcionalidades novas.
- Esta missão não deve criar tag ou release.
- Esta missão deve produzir evidências para orientar as missões 0102–0110.

Entregáveis obrigatórios:
1. Criar:
   - docs/audits/objective-and-scope-alignment-audit.md

2. Criar:
   - docs/alignment/implementation-status.md

3. Criar ou atualizar:
   - docs/history/mission-milestones.md

4. Atualizar:
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md
   - docs/roadmap/mission-backlog.md
   - CHANGELOG.md

5. Atualizar README.md somente se houver divergência objetiva sobre o propósito do projeto.

6. Não alterar código Python.

7. Não alterar scripts shell.

8. Não alterar workflow de CI.

9. Não adicionar dependências.

10. Não criar tag.

11. Não criar release.

12. Não publicar pacote.

Questões obrigatórias da auditoria:
1. Qual é o objetivo original e atual do Vercosa AI Framework?

2. O objetivo está declarado de forma clara e consistente?

3. O framework continua sendo uma plataforma de Harness Engineering orientada por especificações?

4. O projeto continua seguindo Specification First?

5. O Mission Runner é infraestrutura de suporte ou se tornou indevidamente o centro do produto?

6. Existe pelo menos um fluxo completo e útil executável pelo framework?

7. Policy Engine, Guardian Engine, Context Router e Token Budget Manager estão:
   - implementados;
   - integrados;
   - usados por fluxos reais;
   - ou apenas isolados?

8. Knowledge Hub, Model Selection Engine, Provider Gateway e Runtime Adapter entregam valor real hoje ou representam preparação futura?

9. Os agentes, skills, tools e capabilities estão conectados a casos de uso concretos?

10. Existe duplicação de responsabilidade entre componentes?

11. Existem abstrações criadas antes da existência de um caso de uso?

12. Existem documentos que prometem mais do que o código entrega?

13. Existem implementações que não aparecem na documentação?

14. A quantidade de documentação é proporcional à maturidade do produto?

15. A preparação de release alfa ocorreu no momento adequado?

16. O projeto possui uma definição clara de usuário ou consumidor principal?

17. O projeto já resolve um problema concreto de ponta a ponta?

18. PostgreSQL, pgvector e RAG continuam coerentes com o objetivo original?

19. A internacionalização continua coerente com o estágio atual?

20. Quais partes devem:
   - permanecer;
   - ser integradas;
   - ser simplificadas;
   - ser adiadas;
   - ser removidas futuramente;
   - ser reavaliadas?

Classificações obrigatórias:
Cada componente relevante deve receber uma das classificações:

- ADERENTE
- ADERENTE COM RESSALVAS
- FORA DO ESCOPO
- PREMATURO
- DUPLICADO
- NÃO INTEGRADO
- DOCUMENTADO, MAS NÃO IMPLEMENTADO
- IMPLEMENTADO, MAS NÃO DOCUMENTADO
- ESTADO INDETERMINADO

A classificação deve incluir:
- evidência;
- justificativa;
- impacto;
- recomendação;
- prioridade.

Componentes mínimos a avaliar:
- Mission Runner
- runners shell
- batch runner
- Policy Engine
- Guardian Engine
- Context Router
- Token Budget Manager
- Knowledge Hub
- Model Selection Engine
- Provider Gateway
- Runtime Adapter
- Usage/API Limit Guard
- Audit/Event Log
- persistência JSONL
- agentes
- skills
- tools
- capabilities
- workflows
- CLI
- empacotamento Python
- CI
- documentação pública
- processo de release
- preparação alfa
- PostgreSQL planejado
- pgvector planejado
- RAG planejado
- internacionalização planejada

Requisitos para docs/audits/objective-and-scope-alignment-audit.md:
1. Registrar o objetivo canônico identificado.

2. Indicar as fontes utilizadas para reconstruir o objetivo.

3. Não inventar um objetivo novo silenciosamente.

4. Se houver objetivos conflitantes, registrar a divergência.

5. Criar uma seção de visão geral do projeto.

6. Criar uma seção de aderência por componente.

7. Criar uma tabela com:
   - componente;
   - finalidade declarada;
   - estado real;
   - integração real;
   - classificação;
   - evidência;
   - recomendação;
   - prioridade.

8. Criar uma seção sobre fluxos completos existentes.

9. Criar uma seção sobre fluxos completos ausentes.

10. Criar uma seção sobre desvio de escopo.

11. Criar uma seção sobre abstrações prematuras.

12. Criar uma seção sobre documentação desproporcional ou redundante.

13. Criar uma seção sobre preparação de release.

14. Criar uma seção sobre PostgreSQL, pgvector e RAG.

15. Criar uma seção sobre internacionalização.

16. Criar uma seção de riscos.

17. Criar uma seção de recomendações para 0102–0110.

18. Classificar o projeto de forma geral como:
   - ALINHADO;
   - ALINHADO COM RESSALVAS;
   - DESALINHADO;
   - INDETERMINADO.

19. Não suavizar problemas relevantes.

20. Não tratar existência de arquivo como prova de integração.

21. Não tratar teste unitário isolado como prova de fluxo funcional completo.

22. Não tratar documentação como prova de implementação.

23. Usar links relativos.

24. Manter o documento em português do Brasil.

Requisitos para docs/alignment/implementation-status.md:
1. Ser a fonte canônica do checklist completo de implementação.

2. Separar itens em:
   - implementado;
   - integrado e validado;
   - implementado parcialmente;
   - planejado;
   - adiado;
   - fora do escopo;
   - em revisão.

3. Diferenciar claramente:
   - planejado;
   - implementado;
   - integrado;
   - validado.

4. Incluir no mínimo:
   - fundação;
   - arquitetura;
   - motores centrais;
   - runners;
   - CLI;
   - auditoria;
   - testes;
   - documentação;
   - empacotamento;
   - CI;
   - release;
   - segurança;
   - PostgreSQL;
   - pgvector;
   - RAG;
   - providers;
   - runtimes;
   - internacionalização;
   - observabilidade;
   - produção.

5. Não transformar CHANGELOG.md em checklist operacional.

6. Apontar para o CHANGELOG.md como histórico de mudanças.

7. Apontar para mission-backlog.md como backlog futuro.

8. Manter o checklist factual.

9. Não marcar como concluído algo que esteja apenas documentado.

10. Não marcar como integrado algo que tenha somente teste unitário isolado.

Requisitos para docs/history/mission-milestones.md:
1. Registrar os marcos por faixa de missões.

2. Usar pelo menos:
   - 0001–0025;
   - 0026–0050;
   - 0051–0075;
   - 0076–0100.

3. Não inventar detalhes sem evidência.

4. Resumir:
   - objetivo da faixa;
   - principais entregas;
   - mudanças de direção;
   - limitações;
   - resultado.

5. Registrar inconsistência se a quantidade em missions/done não corresponder à numeração alcançada.

6. Não usar esse arquivo como backlog.

Requisitos para CHANGELOG.md:
1. Registrar somente mudanças relevantes e visíveis.

2. Não copiar o checklist completo para o changelog.

3. Manter a seção Não publicado.

4. Registrar a criação da auditoria de aderência e do checklist canônico.

5. Não declarar release publicada.

6. Não criar versão nova.

Requisitos para docs/alignment/current-state.md:
1. Apontar para implementation-status.md como checklist canônico.

2. Registrar a classificação geral da auditoria.

3. Registrar desvios importantes.

4. Não afirmar maturidade maior que a evidência.

Requisitos para docs/alignment/roadmap.md:
1. Ajustar prioridades com base na auditoria.

2. Não manter como prioridade imediata algo classificado como prematuro sem justificativa.

3. Manter a internacionalização planejada em fases:
   - documentação pública;
   - CLI;
   - demais mensagens expostas.

4. Manter PostgreSQL e RAG sujeitos à decisão posterior da auditoria completa.

Requisitos para docs/alignment/open-questions.md:
1. Registrar perguntas ainda sem resposta.

2. Possíveis perguntas:
   - qual é o fluxo de valor principal do framework?
   - quais componentes devem ser integrados primeiro?
   - quais abstrações devem ser simplificadas?
   - a tag alfa deve ser adiada?
   - PostgreSQL é necessário agora?
   - quando iniciar internacionalização?
   - qual é o consumidor principal do framework?

Requisitos para docs/roadmap/mission-backlog.md:
1. Registrar o bloco 0101–0110 como ciclo de auditoria e alinhamento.

2. Não estimar quantidade final de missões antes da 0110.

3. Marcar a estimativa anterior como provisória, se ela estiver registrada.

4. Manter as missões 0102–0110 coerentes com a auditoria.

5. Não criar novos arquivos em missions/queue.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não alterar workflow de CI.
- Não remover arquivos.
- Não mover módulos.
- Não renomear componentes.
- Não corrigir arquitetura nesta missão.
- Não implementar PostgreSQL.
- Não implementar RAG.
- Não implementar internacionalização.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não acessar rede.
- Não acessar banco.
- Não chamar providers.
- Não executar missões.
- Não executar batch.
- Não fazer git push.
- Não usar sudo.
- Não usar git add .
- Não reescrever histórico Git.
- Não fazer force push.
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/audits/objective-and-scope-alignment-audit.md existe.
- O objetivo canônico foi identificado ou sua ambiguidade foi registrada.
- Componentes relevantes foram classificados.
- A auditoria diferencia implementação, integração e validação.
- Desvios de escopo foram identificados.
- Abstrações prematuras foram identificadas.
- Componentes não integrados foram identificados.
- A proporcionalidade da documentação foi avaliada.
- A preparação alfa foi avaliada criticamente.
- PostgreSQL, pgvector, RAG e internacionalização foram avaliados contra o objetivo.
- docs/alignment/implementation-status.md existe.
- O checklist completo está fora do CHANGELOG.md.
- docs/history/mission-milestones.md existe ou foi atualizado.
- docs/alignment/current-state.md aponta para o checklist canônico.
- docs/alignment/roadmap.md foi ajustado conforme a auditoria.
- docs/roadmap/mission-backlog.md registra o ciclo 0101–0110.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma tag foi criada.
- Nenhuma release foi publicada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

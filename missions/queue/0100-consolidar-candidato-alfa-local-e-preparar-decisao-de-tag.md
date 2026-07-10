Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
- pyproject.toml
- .github/workflows/ci.yml
- docs/release/public-alpha-readiness.md
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/release/release-policy.md
- docs/release/pre-release-checklist.md
- docs/release/release-notes-alpha.md
- docs/release/clean-install-validation.md
- docs/release/alpha-readiness-diagnostic.md
- docs/release/pre-tag-checklist-execution.md
- docs/getting-started/local-installation.md
- docs/getting-started/clean-install-checklist.md
- docs/legal/usage-policy.md
- docs/security/vulnerability-reporting.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/cli/README.md

Leia também, se existirem:
- docs/release/alpha-candidate-summary.md
- docs/release/tag-decision-request.md
- docs/release/final-alpha-review.md
- docs/release/release-notes-final.md
- docs/release/pre-tag-checklist-execution.md
- logs/

Assuma o papel de:
- release-manager;
- release-preparation-agent;
- documentation-agent;
- risk-reviewer;
- open-source-maintainer;
- consistency-reviewer.

Missão:
Consolidar candidato alfa local e preparar decisão de tag.

Objetivo:
Consolidar o estado local do candidato alfa 0.1.0-alpha.1 do Vercosa AI Framework, reunir evidências já produzidas, listar bloqueios, ressalvas e pendências restantes, e preparar um documento de decisão para uma futura missão de tag, sem criar tag, sem publicar release, sem publicar pacote, sem fazer push e sem declarar a alfa como publicada.

Contexto:
- Este é o fechamento do bloco 0091–0100.
- O projeto se aproxima de uma futura versão 0.1.0-alpha.1.
- A missão 0091 executou validação de instalação limpa.
- A missão 0092 criou empacotamento Python mínimo.
- A missão 0093 criou CI mínimo.
- A missão 0094 criou política de release e checklist pré-tag.
- A missão 0095 criou release notes alfa preliminares.
- A missão 0096 criou validador local de links Markdown.
- A missão 0097 criou comando CLI de prontidão alfa.
- A missão 0098 executou diagnóstico local de prontidão alfa.
- A missão 0099 executou checklist pré-tag alfa local.
- Esta missão deve consolidar o candidato alfa local.
- Esta missão não deve executar release.
- Esta missão não deve criar tag.
- Esta missão não deve publicar pacote.
- Esta missão não deve fazer push.
- Esta missão não substitui autorização explícita do usuário.
- Esta missão deve deixar claro o que falta depois do batch, especialmente push e confirmação do CI remoto.
- Como esta missão roda dentro do próprio ciclo de batch, ela não deve tratar a própria presença em running como bloqueio permanente.
- A consolidação deve ser factual, conservadora e baseada nos documentos existentes.
- Não inventar aprovação se os documentos anteriores tiverem registrado ressalvas ou reprovação.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/release/alpha-candidate-summary.md

2. Criar documento:
   - docs/release/tag-decision-request.md

3. Atualizar:
   - README.md
   - CHANGELOG.md
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/release/release-policy.md
   - docs/release/pre-release-checklist.md
   - docs/release/release-notes-alpha.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md

4. Atualizar, se necessário:
   - CONTRIBUTING.md
   - docs/alignment/open-questions.md
   - docs/getting-started/clean-install-checklist.md
   - docs/release/alpha-readiness-diagnostic.md
   - docs/release/pre-tag-checklist-execution.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não alterar workflow de CI.

8. Não adicionar dependências.

9. Não criar tag.

10. Não criar release.

11. Não publicar pacote.

12. Não fazer push.

Requisitos para docs/release/alpha-candidate-summary.md:
1. O documento deve estar em português do Brasil.

2. O título deve indicar consolidação local do candidato alfa.

3. Deve declarar explicitamente:
   - não é release;
   - não cria tag;
   - não publica pacote;
   - não confirma CI remoto;
   - não substitui autorização humana;
   - é uma consolidação local preparatória.

4. Deve identificar:
   - versão planejada: 0.1.0-alpha.1;
   - tag planejada: v0.1.0-alpha.1;
   - estado: planejado, não publicado.

5. Deve resumir os artefatos de release já existentes:
   - política de versionamento;
   - plano da alfa;
   - política de release;
   - checklist pré-tag;
   - release notes alfa preliminares;
   - validação de instalação limpa;
   - diagnóstico local de prontidão alfa;
   - execução local do checklist pré-tag.

6. Deve resumir os artefatos técnicos já existentes:
   - empacotamento Python mínimo;
   - CLI operacional;
   - comando docs-links;
   - comando alpha-readiness;
   - persistência local JSONL de eventos auditáveis;
   - CI mínimo;
   - documentação pública mínima.

7. Deve registrar o estado esperado após o batch 0091–0100:
   - queue deve ficar 0;
   - running deve ficar 0;
   - failed deve ficar 0;
   - pytest deve passar;
   - compileall deve passar;
   - git status deve ficar limpo;
   - push ainda precisará ser feito manualmente;
   - CI remoto ainda precisará ser confirmado após push.

8. Deve registrar que esses estados precisam ser confirmados fora desta missão, após o batch encerrar.

9. Deve consolidar a classificação dos documentos anteriores:
   - clean-install-validation;
   - alpha-readiness-diagnostic;
   - pre-tag-checklist-execution.

10. Se qualquer documento anterior tiver classificado como REPROVADO ou NÃO PRONTO:
   - refletir isso como bloqueio;
   - não suavizar para pronto.

11. Se documentos anteriores tiverem classificado como aprovado com ressalvas:
   - preservar as ressalvas;
   - não converter para aprovado pleno.

12. Deve conter seção "Bloqueios".

13. Deve conter seção "Ressalvas".

14. Deve conter seção "Pendências antes da tag".

15. Pendências antes da tag devem incluir, no mínimo:
   - concluir batch 0091–0100;
   - executar validação final;
   - fazer push;
   - confirmar CI remoto;
   - revisar release notes finais;
   - revisar CHANGELOG.md;
   - confirmar licença;
   - obter autorização explícita para tag;
   - criar tag em missão específica;
   - publicar release em missão específica, se autorizado.

16. Deve conter seção "Não realizado nesta etapa".

17. Essa seção deve listar:
   - nenhuma tag criada;
   - nenhuma release publicada;
   - nenhum pacote publicado;
   - nenhum push feito por esta missão;
   - nenhum deploy;
   - nenhum upload para PyPI;
   - nenhuma internacionalização dos READMEs.

18. Deve conter seção "Próxima decisão".

19. A próxima decisão deve ser formulada de forma objetiva:
   - autorizar ou não uma futura missão para criar tag alfa;
   - adiar por bloqueios;
   - resolver ressalvas antes da tag;
   - confirmar CI remoto antes de qualquer tag.

20. Deve usar links relativos para todos os documentos citados.

21. Não incluir logs extensos.

22. Não incluir tokens.

23. Não incluir credenciais.

24. Não incluir caminhos sensíveis desnecessários.

Requisitos para docs/release/tag-decision-request.md:
1. O documento deve estar em português do Brasil.

2. O título deve indicar solicitação futura de decisão sobre tag alfa.

3. Deve declarar explicitamente:
   - este documento não autoriza tag por si só;
   - a tag ainda não foi criada;
   - a release ainda não foi publicada;
   - a decisão depende de autorização explícita do usuário após validação final.

4. Deve indicar:
   - versão planejada: 0.1.0-alpha.1;
   - tag planejada: v0.1.0-alpha.1.

5. Deve resumir evidências disponíveis:
   - validação de instalação limpa;
   - diagnóstico local de prontidão alfa;
   - checklist pré-tag local;
   - release notes preliminares;
   - política de release;
   - CI mínimo criado.

6. Deve listar condições mínimas para pedir autorização:
   - batch 0091–0100 concluído;
   - queue=0;
   - running=0;
   - failed=0;
   - pytest passando;
   - compileall passando;
   - docs-links passando;
   - alpha-readiness sem bloqueios;
   - git status limpo;
   - push concluído;
   - CI remoto confirmado;
   - release notes revisadas;
   - CHANGELOG.md revisado;
   - ausência de secrets;
   - licença confirmada.

7. Deve listar perguntas de decisão:
   - autorizar criação de tag v0.1.0-alpha.1?
   - publicar release no GitHub após tag?
   - publicar pacote ou manter apenas código-fonte?
   - revisar release notes antes da publicação?
   - internacionalizar READMEs antes ou depois da alfa?

8. Deve listar opções possíveis:
   - prosseguir para missão de tag;
   - prosseguir para revisão final de release notes;
   - adiar tag até resolver ressalvas;
   - adiar release e continuar desenvolvimento;
   - publicar apenas código-fonte no GitHub quando autorizado.

9. Deve listar riscos:
   - API ainda instável;
   - alfa não pronta para produção;
   - CI remoto ainda depende de confirmação após push;
   - release notes ainda preliminares;
   - pacote PyPI ainda não decidido;
   - internacionalização ainda futura.

10. Deve listar recomendação conservadora:
   - não criar tag antes de push e confirmação do CI remoto;
   - não publicar release sem autorização explícita;
   - não publicar pacote sem missão própria.

11. Não incluir comando git tag como instrução operacional ativa.

12. Se mencionar comando futuro de tag, deixar claro que pertence a missão futura autorizada.

13. Não incluir git push --tags como comando de execução atual.

14. Não incluir gh release create como comando de execução atual.

15. Não incluir twine.

16. Usar links relativos para documentos de apoio.

Requisitos para README.md:
1. Adicionar link curto para:
   - docs/release/alpha-candidate-summary.md
   - docs/release/tag-decision-request.md

2. Deixar claro que são documentos preparatórios.

3. Não declarar release publicada.

4. Não declarar tag criada.

5. Manter README enxuto.

Requisitos para CHANGELOG.md:
1. Atualizar seção Não publicado.

2. Registrar consolidação do candidato alfa local.

3. Registrar criação do documento de decisão futura sobre tag.

4. Não criar seção versionada publicada.

5. Não criar data de release.

6. Não declarar alfa publicada.

Requisitos para docs/release/public-alpha-readiness.md:
1. Registrar que o candidato alfa local foi consolidado.

2. Linkar para:
   - docs/release/alpha-candidate-summary.md
   - docs/release/tag-decision-request.md

3. Manter pendente:
   - validação final pós-batch;
   - push;
   - confirmação de CI remoto;
   - autorização explícita para tag;
   - criação de tag;
   - publicação de release;
   - publicação de pacote, se aplicável;
   - internacionalização dos READMEs.

4. Não declarar alfa publicada.

5. Não declarar tag criada.

Requisitos para docs/release/alpha-version-plan.md:
1. Registrar consolidação local do candidato alfa.

2. Apontar para:
   - alpha-candidate-summary.md
   - tag-decision-request.md

3. Manter versão como planejada, não publicada.

4. Não declarar tag criada.

5. Não declarar release publicada.

Requisitos para docs/release/release-policy.md:
1. Apontar para o documento de decisão futura de tag.

2. Reforçar que tag depende de autorização explícita.

3. Reforçar que publicação de release depende de missão própria.

4. Reforçar que publicação de pacote depende de missão própria.

Requisitos para docs/release/pre-release-checklist.md:
1. Incluir consolidação do candidato alfa local como evidência preparatória.

2. Apontar para alpha-candidate-summary.md.

3. Manter checklist pré-tag como gate manual.

4. Não transformar checklist em autorização automática.

Requisitos para docs/release/release-notes-alpha.md:
1. Atualizar status para indicar que as notas foram incluídas na consolidação do candidato alfa.

2. Manter como preliminares.

3. Não declarar data de release.

4. Não declarar release publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar consolidação do candidato alfa local como concluída ou em progresso conforme esta missão.

2. Manter futuras:
   - validação final pós-batch;
   - push do bloco;
   - confirmação de CI remoto;
   - revisão final de release notes;
   - decisão explícita sobre tag;
   - criação da tag alfa;
   - publicação da release alfa;
   - decisão sobre PyPI;
   - internacionalização dos READMEs.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/current-state.md:
1. Registrar que o candidato alfa local foi consolidado.

2. Registrar que a tag não foi criada.

3. Registrar que a release não foi publicada.

4. Registrar que a próxima etapa depende de validação final, push, CI remoto e autorização explícita.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar roadmap para refletir fechamento do bloco 0091–0100.

2. Manter próximos passos conservadores.

3. Não declarar release feita.

4. Não declarar tag criada.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas concretas.

2. Perguntas possíveis:
   - autorizar futura missão de tag alfa?
   - publicar release GitHub ou manter apenas tag?
   - publicar pacote PyPI ou apenas código-fonte?
   - internacionalizar READMEs antes ou depois da alfa?
   - quais ressalvas precisam ser resolvidas antes da tag?

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem pública, objetiva e conservadora.

3. Não prometer estabilidade.

4. Não prometer produção.

5. Não prometer suporte formal.

6. Não prometer SLA.

7. Não prometer compatibilidade de API.

8. Não omitir ressalvas.

9. Não omitir bloqueios.

10. Não criar tag.

11. Não publicar release.

12. Não publicar pacote.

13. Não alterar código.

14. Não alterar scripts.

15. Não adicionar dependências.

16. Não acessar rede.

17. Não executar providers.

18. Usar links relativos corretos.

19. Controlar corretamente blocos Markdown e quantidade de crases.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não alterar workflow de CI.
- Não adicionar dependências.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não executar git tag.
- Não executar git push.
- Não executar git push --tags.
- Não executar gh release.
- Não executar twine.
- Não executar build de pacote.
- Não executar missões.
- Não executar batch.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não usar sudo.
- Não alterar configurações globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/release/alpha-candidate-summary.md existe.
- docs/release/tag-decision-request.md existe.
- A consolidação diferencia candidato alfa, tag, release e pacote.
- A documentação declara que nenhuma tag foi criada.
- A documentação declara que nenhuma release foi publicada.
- A documentação declara que nenhum pacote foi publicado.
- A documentação lista pendências antes da tag.
- A documentação lista próximos passos pós-batch.
- README.md aponta para os documentos preparatórios.
- CHANGELOG.md registra a consolidação sem criar versão publicada.
- docs/release/public-alpha-readiness.md aponta para a consolidação.
- docs/release/alpha-version-plan.md foi atualizado.
- docs/release/release-policy.md foi atualizado.
- docs/release/pre-release-checklist.md foi atualizado.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhum workflow de CI foi alterado.
- Nenhuma dependência foi adicionada.
- Nenhuma tag foi criada.
- Nenhuma release foi criada.
- Nenhum pacote foi publicado.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

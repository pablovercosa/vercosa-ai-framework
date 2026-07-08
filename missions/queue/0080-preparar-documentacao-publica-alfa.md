Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- LICENSE
- docs/legal/README.md
- docs/legal/usage-policy.md
- docs/legal/license-notes.md
- docs/getting-started/local-installation.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/architecture/module-index.md
- docs/architecture/audit-event-architecture.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- docs/examples/README.md
- docs/examples/mission-batch-operational-flow.md
- docs/examples/policy-context-guardian-flow.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/audit/README.md
- src/vercosa_ai_framework/missions/README.md
- src/vercosa_ai_framework/model_selection/README.md
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/providers/README.md

Assuma o papel de:
- release-preparation-agent;
- documentation-agent;
- open-source-maintainer;
- developer-experience-engineer;
- consistency-reviewer.

Missão:
Preparar documentação pública alfa.

Objetivo:
Revisar e organizar a documentação pública inicial do Vercosa AI Framework para uma futura fase alfa, garantindo que README, guias, documentação legal inicial, contribuição, arquitetura, operações e exemplos estejam coerentes, navegáveis, conservadores e sem prometer maturidade ou funcionalidades ainda não implementadas.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto ainda está em desenvolvimento.
- O projeto já possui documentação de Harness Engineering.
- O projeto já possui guia de instalação local.
- O projeto já possui guia de contribuição inicial.
- O projeto já possui documentação legal e política de uso inicial, se a missão 0079 tiver sido executada antes desta.
- O projeto já possui documentação operacional de batch.
- O projeto já possui documentação de auditoria.
- O projeto já possui exemplos operacionais iniciais.
- O objetivo desta missão é preparar documentação pública alfa, não criar release.
- Esta missão não deve publicar versão.
- Esta missão não deve criar tag.
- Esta missão não deve criar changelog de release se ainda não houver decisão.
- Esta missão não deve internacionalizar READMEs.
- README.md continua sendo o documento canônico em português do Brasil.
- README.en.md e README.es.md continuam como tarefa futura.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/release/public-alpha-readiness.md

2. Criar diretório, se necessário:
   - docs/release/

3. Atualizar:
   - README.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/roadmap.md
   - docs/alignment/current-state.md

4. Atualizar, se necessário:
   - CONTRIBUTING.md
   - docs/getting-started/local-installation.md
   - docs/legal/README.md
   - docs/legal/usage-policy.md
   - docs/legal/license-notes.md
   - docs/architecture/module-index.md
   - docs/examples/README.md
   - docs/alignment/open-questions.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não adicionar dependências.

Requisitos para docs/release/public-alpha-readiness.md:
1. O documento deve estar em português do Brasil.

2. Explicar que o documento é um checklist de preparação para alfa pública.

3. Explicar que alfa pública não significa estabilidade de produção.

4. Explicar que o projeto ainda está em desenvolvimento.

5. Criar uma visão objetiva do estado da documentação pública.

6. Incluir checklist de documentação mínima:
   - README.md;
   - CONTRIBUTING.md;
   - LICENSE ou pendência de licença documentada;
   - docs/legal/usage-policy.md;
   - docs/legal/license-notes.md;
   - docs/getting-started/local-installation.md;
   - docs/architecture/module-index.md;
   - docs/operations/batch-execution-playbook.md;
   - docs/operations/post-batch-validation-checklist.md;
   - docs/examples/README.md;
   - docs/roadmap/mission-backlog.md.

7. Para cada item do checklist, indicar:
   - existe;
   - precisa de revisão;
   - pendente;
   - fora do escopo da alfa atual.

8. Incluir checklist de consistência:
   - o README explica o que é o projeto;
   - o README diferencia implementado e futuro;
   - o README aponta para guias principais;
   - o guia de instalação não promete PyPI inexistente;
   - o guia de contribuição não promete processo público maduro;
   - a política de uso não promete segurança absoluta;
   - a documentação legal não faz aconselhamento jurídico;
   - a documentação operacional não recomenda execução cega;
   - o roadmap não promete funcionalidades futuras como implementadas.

9. Incluir checklist de riscos antes de alfa pública:
   - ausência de CI público, se ainda não existir;
   - ausência de SECURITY.md, se ainda não existir;
   - ausência de CODE_OF_CONDUCT.md, se ainda não existir;
   - ausência de templates de issue e pull request, se ainda não existirem;
   - ausência de release/tag, se ainda não existir;
   - ausência de documentação internacionalizada;
   - ausência de provider real configurado;
   - ausência de RAG semântico;
   - ausência de persistência externa de eventos;
   - ausência de testes de instalação limpa em ambiente novo.

10. Incluir seção de decisões já tomadas:
   - documentação em português do Brasil;
   - README.md canônico em português;
   - internacionalização no final;
   - batch como fluxo operacional padrão quando seguro;
   - execução individual para missões sensíveis;
   - OpenCode como runtime/laboratório atual, não núcleo;
   - sem banco por enquanto;
   - sem RAG por enquanto;
   - sem pgvector por enquanto.

11. Incluir seção de pendências antes de release alfa:
   - revisar licença final, se ainda pendente;
   - criar SECURITY.md;
   - criar CODE_OF_CONDUCT.md, se desejado;
   - criar templates de issue e pull request;
   - criar changelog inicial;
   - definir versão inicial;
   - testar instalação do zero;
   - revisar README final de alfa;
   - decidir se haverá README.en.md e README.es.md apenas no final.

12. Incluir seção de critérios mínimos para considerar alfa pública pronta.

13. Não transformar o documento em release notes.

14. Não criar versão.

15. Não criar tag.

16. Não publicar pacote.

17. Não prometer datas.

18. Não prometer estabilidade.

19. Usar linguagem objetiva.

20. Usar links relativos corretos.

Requisitos para README.md:
1. Revisar se README aponta para:
   - guia de instalação local;
   - guia de contribuição;
   - documentação legal ou política de uso;
   - documentação de arquitetura;
   - exemplos;
   - roadmap/backlog;
   - checklist de alfa pública.

2. Manter README enxuto.

3. Não transformar README em release checklist.

4. Não dizer que o projeto está pronto para produção.

5. Não dizer que a alfa pública já foi publicada.

6. Não prometer PyPI se não existir.

7. Não prometer Docker se não existir.

8. Não prometer CI se não existir.

9. Não prometer provider real se não existir.

10. Não prometer RAG se não existir.

11. Não prometer pgvector se não existir.

12. Não internacionalizar nesta missão.

Requisitos para docs/roadmap/mission-backlog.md:
1. Registrar que a preparação documental para alfa pública foi iniciada ou concluída conforme esta missão.

2. Manter como futuras, se ainda não existirem:
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - templates de issue;
   - templates de pull request;
   - changelog inicial;
   - versão inicial;
   - release alfa;
   - internacionalização dos READMEs.

3. Não mover todo o backlog para missions/queue.

4. Manter separação entre backlog estratégico e fila executável.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar o roadmap para refletir avanço de documentação pública alfa.

2. Não afirmar que release alfa foi feita.

3. Não afirmar que pacote foi publicado.

4. Manter próximos passos conservadores.

Requisitos para docs/alignment/current-state.md:
1. Registrar que existe checklist de prontidão para alfa pública.

2. Manter limites atuais do projeto.

3. Diferenciar documentação preparada de release publicada.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se surgirem perguntas relevantes.

2. Perguntas possíveis:
   - versão inicial;
   - modelo de release alfa;
   - política de segurança pública;
   - CODE_OF_CONDUCT;
   - templates de issue e PR;
   - licença final, se ainda pendente;
   - momento de internacionalização.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem conservadora e factual.

3. Diferenciar:
   - documentação pública preparada;
   - alfa pública futura;
   - release publicada;
   - produção;
   - recursos futuros.

4. Não prometer funcionalidades futuras como implementadas.

5. Não inventar arquivos que não existem.

6. Não esconder pendências.

7. Não alterar código.

8. Não alterar scripts.

9. Não adicionar dependências.

10. Usar links relativos corretos.

11. Usar blocos Markdown quando úteis.

12. Controlar corretamente a quantidade de crases nos blocos Markdown.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não criar release.
- Não criar tag.
- Não criar changelog de release nesta missão.
- Não publicar pacote.
- Não criar workflow de CI.
- Não criar SECURITY.md nesta missão.
- Não criar CODE_OF_CONDUCT.md nesta missão.
- Não criar templates de issue.
- Não criar templates de pull request.
- Não criar README.en.md.
- Não criar README.es.md.
- Não internacionalizar READMEs.
- Não implementar funcionalidades.
- Não adicionar dependências.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não executar missões.
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/release/public-alpha-readiness.md existe.
- O documento diferencia alfa pública, release publicada e produção.
- O documento lista documentação mínima para alfa pública.
- O documento lista riscos e pendências antes de release alfa.
- README.md aponta para o checklist de alfa pública ou para a seção adequada.
- Roadmap e backlog refletem preparação documental para alfa.
- current-state diferencia documentação preparada de release feita.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- README.en.md não foi criado.
- README.es.md não foi criado.
- Nenhuma tag foi criada.
- Nenhuma release foi criada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

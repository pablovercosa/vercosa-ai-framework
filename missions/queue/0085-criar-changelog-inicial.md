Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
- docs/legal/usage-policy.md
- docs/release/public-alpha-readiness.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md

Leia também, se existirem:
- CHANGELOG.md
- docs/release/CHANGELOG.md
- docs/release/release-notes.md
- pyproject.toml
- setup.py
- package.json

Assuma o papel de:
- release-preparation-agent;
- documentation-agent;
- open-source-maintainer;
- changelog-maintainer;
- consistency-reviewer.

Missão:
Criar changelog inicial.

Objetivo:
Criar um CHANGELOG.md inicial para o Vercosa AI Framework, registrando de forma organizada a evolução já consolidada do projeto até o estado atual, sem criar release formal, sem criar tag, sem definir versão definitiva e sem prometer estabilidade de produção.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto ainda está em desenvolvimento.
- O projeto já possui documentação pública inicial.
- O projeto já possui README com identidade de Harness Engineering.
- O projeto já possui guia de instalação local.
- O projeto já possui guia de contribuição.
- O projeto já possui documentação legal inicial.
- O projeto já possui SECURITY.md.
- O projeto já possui CODE_OF_CONDUCT.md.
- O projeto já possui templates de issue e pull request.
- O projeto precisa agora de um changelog inicial para preparar futura release alfa.
- Esta missão deve criar o changelog, não a release.
- Esta missão não deve criar tag.
- Esta missão não deve publicar versão.
- Esta missão não deve alterar código.
- Esta missão não deve alterar scripts.

Entregáveis obrigatórios:
1. Criar arquivo:
   - CHANGELOG.md

2. Atualizar:
   - README.md
   - CONTRIBUTING.md
   - docs/release/public-alpha-readiness.md
   - docs/roadmap/mission-backlog.md

3. Atualizar, se necessário:
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md

4. Não alterar código Python.

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos para CHANGELOG.md:
1. O documento deve estar em português do Brasil.

2. O documento deve explicar que o projeto ainda está em desenvolvimento.

3. O documento deve explicar que ainda não há release estável publicada.

4. O documento deve usar estrutura compatível com changelog público.

5. O documento deve ter uma seção inicial:
   - Não publicado

6. A seção Não publicado deve agrupar mudanças já consolidadas em categorias claras, como:
   - Adicionado;
   - Alterado;
   - Documentado;
   - Segurança;
   - Operacional;
   - Futuro.

7. Registrar, de forma resumida e factual, os principais blocos já implementados:
   - fundação modular do framework;
   - evolução por missões;
   - Mission Runner;
   - runner seguro de uma missão;
   - runner seguro em batch;
   - batch como fluxo operacional padrão quando seguro;
   - Policy Engine;
   - Guardian Engine;
   - Context Router;
   - Token Budget Manager;
   - Knowledge Hub;
   - Model Selection Engine;
   - Provider Gateway;
   - Runtime Adapter;
   - Usage/API Limit Guard;
   - Audit/Event Log inicial;
   - CLI operacional;
   - comandos status, validate e doctor, se existirem;
   - exemplos operacionais iniciais;
   - documentação pública alfa;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - templates de issue e pull request.

8. Registrar limites atuais:
   - sem release estável;
   - sem versão alfa publicada;
   - sem pacote publicado;
   - sem PyPI;
   - sem CI público, se ainda não existir;
   - sem RAG semântico;
   - sem embeddings;
   - sem pgvector;
   - sem Semantic Index;
   - sem persistência externa de eventos;
   - sem internacionalização dos READMEs.

9. Não atribuir versão falsa.

10. Não criar data de release se ainda não houver release.

11. Não declarar produção pronta.

12. Não declarar alfa publicada.

13. Não prometer compatibilidade futura.

14. Não prometer SLA.

15. Não incluir detalhes excessivos de todos os commits.

16. Não transformar CHANGELOG.md em roadmap completo.

17. Incluir seção curta explicando convenção futura de versões, sem fixar versão se isso ainda não foi decidido.

18. Se mencionar SemVer, deixar claro que a adoção formal será definida antes da primeira release versionada.

19. Usar links relativos úteis para:
   - README.md;
   - docs/release/public-alpha-readiness.md;
   - docs/roadmap/mission-backlog.md.

20. Manter linguagem objetiva e pública.

Requisitos para README.md:
1. Adicionar link curto para CHANGELOG.md.

2. Manter README enxuto.

3. Não duplicar changelog no README.

4. Não declarar release publicada.

5. Não declarar versão alfa publicada.

Requisitos para CONTRIBUTING.md:
1. Adicionar referência curta ao CHANGELOG.md.

2. Explicar que mudanças relevantes devem atualizar CHANGELOG.md quando afetarem:
   - comportamento público;
   - arquitetura;
   - operação;
   - segurança;
   - documentação pública;
   - release futura.

3. Não transformar CONTRIBUTING.md em manual completo de release.

Requisitos para docs/release/public-alpha-readiness.md:
1. Atualizar checklist para marcar CHANGELOG.md como criado.

2. Manter pendentes itens ainda não executados, como:
   - versão alfa inicial;
   - teste de instalação limpa;
   - CI público, se ainda não existir;
   - release alfa;
   - internacionalização dos READMEs.

3. Não declarar alfa pública como publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar changelog inicial como concluído ou em progresso conforme esta missão.

2. Manter como futuras:
   - definição de versão alfa inicial;
   - política de release;
   - tag alfa;
   - release notes;
   - CI público;
   - internacionalização dos READMEs.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver pendências claras.

2. Perguntas possíveis:
   - qual será a primeira versão alfa;
   - haverá adoção formal de SemVer;
   - qual política de release será usada;
   - quando criar primeira tag;
   - quando publicar release alfa.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem conservadora e factual.

3. Diferenciar:
   - changelog inicial;
   - release futura;
   - versão futura;
   - produção;
   - recursos futuros.

4. Não prometer maturidade inexistente.

5. Não inventar versão.

6. Não inventar data de release.

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
- Não definir versão definitiva.
- Não publicar pacote.
- Não criar CI.
- Não criar GitHub Actions.
- Não criar README.en.md.
- Não criar README.es.md.
- Não internacionalizar READMEs.
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
- CHANGELOG.md existe.
- CHANGELOG.md possui seção Não publicado.
- CHANGELOG.md registra evolução principal do projeto até o estado atual.
- CHANGELOG.md não cria versão falsa.
- CHANGELOG.md não declara release publicada.
- CHANGELOG.md não promete estabilidade de produção.
- README.md aponta para CHANGELOG.md.
- CONTRIBUTING.md menciona atualização de changelog quando aplicável.
- docs/release/public-alpha-readiness.md registra CHANGELOG.md como criado.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

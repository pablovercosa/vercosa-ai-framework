Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- LICENSE
- docs/release/public-alpha-readiness.md
- docs/roadmap/mission-backlog.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/getting-started/local-installation.md
- docs/legal/license-notes.md
- docs/legal/usage-policy.md

Leia também, se existirem:
- pyproject.toml
- setup.py
- setup.cfg
- package.json
- VERSION
- docs/release/versioning-policy.md
- docs/release/alpha-version-plan.md
- docs/release/release-notes.md

Assuma o papel de:
- release-preparation-agent;
- versioning-strategy-agent;
- open-source-maintainer;
- documentation-agent;
- consistency-reviewer.

Missão:
Definir versão alfa inicial.

Objetivo:
Definir documentalmente uma estratégia inicial de versionamento e uma versão alfa planejada para o Vercosa AI Framework, preparando o caminho para uma futura release alfa sem criar tag, sem publicar pacote, sem declarar release feita e sem alterar código de runtime.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto já possui CHANGELOG.md inicial.
- O projeto já possui documentação pública alfa.
- O projeto ainda não publicou release alfa.
- O projeto ainda não deve ser apresentado como estável.
- O projeto ainda não deve prometer compatibilidade de API.
- O projeto ainda não possui necessariamente empacotamento formal.
- A versão alfa inicial deve ser uma decisão documental conservadora.
- Esta missão deve definir estratégia e plano, não publicar release.
- Esta missão não deve criar tag Git.
- Esta missão não deve fazer push.
- Esta missão não deve publicar em PyPI.
- Esta missão não deve criar CI.
- Esta missão não deve alterar código Python.
- Esta missão não deve alterar scripts shell.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/release/versioning-policy.md

2. Criar documento:
   - docs/release/alpha-version-plan.md

3. Atualizar:
   - CHANGELOG.md
   - README.md
   - docs/release/public-alpha-readiness.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/roadmap.md
   - docs/alignment/current-state.md

4. Atualizar, se necessário:
   - docs/alignment/open-questions.md
   - CONTRIBUTING.md

5. Não criar tag.

6. Não criar release.

7. Não publicar pacote.

8. Não alterar código Python.

9. Não alterar scripts shell.

10. Não adicionar dependências.

Requisitos para docs/release/versioning-policy.md:
1. O documento deve estar em português do Brasil.

2. Explicar que a política de versionamento é inicial.

3. Explicar que o projeto ainda não possui release estável.

4. Explicar que a primeira versão alfa será usada para organizar uma entrega pública inicial, não para prometer estabilidade de produção.

5. Definir uma estratégia conservadora de versionamento.

6. Considerar SemVer como referência se fizer sentido, mas deixar claro que:
   - versões 0.x indicam instabilidade;
   - APIs podem mudar;
   - compatibilidade ainda não é garantida;
   - política formal de estabilidade será amadurecida após as alfas.

7. Definir categorias de versão:
   - desenvolvimento não publicado;
   - alfa;
   - beta futura;
   - estável futura.

8. Explicar diferença entre:
   - versão planejada;
   - versão publicada;
   - tag Git;
   - release GitHub;
   - pacote publicado.

9. Definir convenção recomendada para alfa inicial, como:
   - 0.1.0-alpha.1

10. Se escolher outra convenção, justificar claramente.

11. Explicar que a versão alfa inicial não deve ser considerada produção.

12. Explicar que a versão alfa inicial deve ser publicada somente depois de:
   - documentação pública mínima revisada;
   - SECURITY.md criado;
   - CODE_OF_CONDUCT.md criado;
   - templates de issue e pull request criados;
   - CHANGELOG.md criado;
   - checklist de instalação limpa executado;
   - testes passando;
   - compileall passando;
   - git status limpo;
   - decisão explícita de release.

13. Explicar que tags devem seguir um padrão previsível, como:
   - v0.1.0-alpha.1

14. Não criar a tag nesta missão.

15. Explicar que a tag futura só deve ser criada em missão específica de release.

16. Explicar como o CHANGELOG.md deve ser atualizado em futuras versões.

17. Explicar que mudanças relevantes devem ser agrupadas em:
   - Adicionado;
   - Alterado;
   - Corrigido;
   - Removido;
   - Segurança;
   - Documentação;
   - Operacional.

18. Explicar quando uma mudança deve afetar versão:
   - mudança pública de comportamento;
   - mudança de API;
   - alteração operacional relevante;
   - alteração de segurança;
   - alteração em documentação pública de release.

19. Não criar promessa de compatibilidade que o projeto ainda não sustenta.

20. Não criar política complexa demais.

21. Usar links relativos para:
   - CHANGELOG.md
   - docs/release/public-alpha-readiness.md
   - docs/release/alpha-version-plan.md
   - docs/roadmap/mission-backlog.md

Requisitos para docs/release/alpha-version-plan.md:
1. O documento deve estar em português do Brasil.

2. Explicar a proposta de versão alfa inicial.

3. Definir claramente:
   - versão planejada;
   - tag futura planejada;
   - status atual;
   - pendências antes da publicação;
   - critérios mínimos de publicação.

4. Usar como recomendação padrão:
   - versão planejada: 0.1.0-alpha.1
   - tag futura planejada: v0.1.0-alpha.1

5. Deixar claro que:
   - a versão ainda não foi publicada;
   - a tag ainda não foi criada;
   - não há release GitHub publicada;
   - não há pacote PyPI publicado;
   - não há garantia de estabilidade.

6. Listar o que já existe para apoiar a alfa:
   - README principal;
   - documentação de Harness Engineering;
   - guia de instalação local;
   - guia de contribuição;
   - política de uso responsável;
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - templates de issue e pull request;
   - CHANGELOG.md;
   - playbooks operacionais;
   - documentação de arquitetura;
   - checklist de alfa pública.

7. Listar pendências antes de publicar a alfa:
   - checklist de instalação limpa;
   - revisão final do README;
   - validação de links;
   - execução de pytest;
   - execução de compileall;
   - revisão do CHANGELOG;
   - decisão explícita de criar tag;
   - decisão explícita de publicar release;
   - definição se haverá pacote ou apenas código-fonte;
   - confirmação de licença final se ainda houver pendência.

8. Incluir critérios mínimos para considerar a alfa publicável:
   - queue=0;
   - running=0;
   - failed=0;
   - git status limpo;
   - pytest passando;
   - compileall passando;
   - documentação mínima presente;
   - segurança básica documentada;
   - changelog atualizado;
   - versão planejada documentada;
   - autorização explícita para tag/release.

9. Não criar changelog de release definitivo.

10. Não criar release notes finais.

11. Não criar tag.

12. Não publicar release.

13. Não prometer data.

14. Não prometer estabilidade.

Requisitos para CHANGELOG.md:
1. Atualizar a seção Não publicado.

2. Registrar que uma política inicial de versionamento foi criada.

3. Registrar que a versão alfa planejada foi documentada.

4. Não mover conteúdo para uma versão publicada.

5. Não criar seção de release datada.

6. Não afirmar que 0.1.0-alpha.1 foi publicada.

7. Pode mencionar que 0.1.0-alpha.1 é versão planejada, se isso estiver claro.

Requisitos para README.md:
1. Adicionar link curto para:
   - docs/release/versioning-policy.md
   - docs/release/alpha-version-plan.md

2. Manter README enxuto.

3. Não declarar release alfa publicada.

4. Não declarar pacote publicado.

5. Não declarar estabilidade de produção.

Requisitos para docs/release/public-alpha-readiness.md:
1. Atualizar checklist para marcar estratégia de versionamento e versão alfa planejada como documentadas.

2. Manter pendente:
   - teste de instalação limpa;
   - decisão explícita de release;
   - criação de tag;
   - publicação de release;
   - CI público, se ainda não existir;
   - internacionalização dos READMEs.

3. Não declarar alfa pública como publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar definição de versão alfa inicial como concluída ou em progresso conforme esta missão.

2. Manter como futuras:
   - checklist de instalação limpa;
   - revisão final pré-release;
   - criação de tag alfa;
   - release alfa;
   - CI público;
   - internacionalização dos READMEs.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar roadmap para refletir que a versão alfa planejada foi definida documentalmente.

2. Não afirmar que a alfa foi publicada.

3. Manter próximos passos conservadores.

Requisitos para docs/alignment/current-state.md:
1. Registrar que existe versão alfa planejada.

2. Deixar claro que não há release publicada.

3. Manter limites atuais explícitos.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas ainda abertas.

2. Perguntas possíveis:
   - quando criar a tag v0.1.0-alpha.1;
   - haverá pacote PyPI ou apenas código-fonte na alfa;
   - haverá CI antes da alfa;
   - haverá release notes separadas;
   - quando internacionalizar READMEs.

Requisitos para CONTRIBUTING.md:
1. Atualizar somente se fizer sentido mencionar CHANGELOG e versionamento.

2. Não transformar CONTRIBUTING.md em manual de release.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem conservadora e factual.

3. Diferenciar:
   - versão planejada;
   - release publicada;
   - tag;
   - pacote;
   - produção.

4. Não criar tag.

5. Não publicar release.

6. Não inventar data.

7. Não prometer estabilidade.

8. Não alterar código.

9. Não alterar scripts.

10. Não adicionar dependências.

11. Usar links relativos corretos.

12. Usar blocos Markdown quando úteis.

13. Controlar corretamente a quantidade de crases nos blocos Markdown.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não criar release.
- Não criar tag.
- Não publicar pacote.
- Não criar CI.
- Não criar GitHub Actions.
- Não definir versão em código se não houver mecanismo existente.
- Não criar pyproject.toml.
- Não criar setup.py.
- Não criar package.json.
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
- docs/release/versioning-policy.md existe.
- docs/release/alpha-version-plan.md existe.
- A versão alfa planejada está documentada.
- O documento diferencia versão planejada de release publicada.
- CHANGELOG.md registra a política de versionamento sem criar release falsa.
- README.md aponta para os documentos de versionamento.
- docs/release/public-alpha-readiness.md registra versionamento como documentado.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- Nenhuma tag foi criada.
- Nenhuma release foi criada.
- Nenhum pacote foi publicado.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/roadmap/mission-backlog.md
- docs/getting-started/local-installation.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- docs/examples/README.md
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- scripts/vaf-status.sh
- tests/test_worker_scripts.py

Assuma o papel de:
- documentation-agent;
- developer-experience-engineer;
- open-source-maintainer;
- process-governance-agent;
- technical-editor.

Missão:
Criar guia de contribuição inicial.

Objetivo:
Criar um guia inicial de contribuição para o Vercosa AI Framework, explicando como contribuir com segurança, como preparar ambiente local, como criar missões, como respeitar o fluxo em batch, como rodar validações e como manter documentação, testes e commits coerentes com o padrão do projeto.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto já possui guia de instalação local, se a missão anterior tiver sido executada antes desta no batch.
- O projeto já possui documentação de idioma, commits e atualização documental.
- O projeto já possui runner seguro de uma missão.
- O projeto já possui runner seguro em batch.
- O batch é fluxo operacional padrão quando seguro.
- O projeto exige português do Brasil em documentação, missões e commits.
- O projeto usa evolução por missões em Markdown.
- O projeto valoriza rastreabilidade, governança, segurança operacional, testes e documentação.
- O guia de contribuição deve ser inicial e conservador.
- O guia não deve prometer processo público maduro se ainda não existir.
- O guia não deve criar automações novas.
- O guia não deve alterar código.

Entregáveis obrigatórios:
1. Criar arquivo:
   - CONTRIBUTING.md

2. Criar ou atualizar, se fizer sentido:
   - docs/contributing/README.md

3. Criar diretório, se necessário:
   - docs/contributing/

4. Atualizar:
   - README.md

5. Atualizar, se necessário:
   - docs/roadmap/mission-backlog.md
   - docs/alignment/roadmap.md
   - docs/alignment/current-state.md

6. Não alterar código Python.

7. Não alterar scripts shell.

8. Não adicionar dependências.

Requisitos para CONTRIBUTING.md:
1. O documento deve estar em português do Brasil.

2. O documento deve explicar que o Vercosa AI Framework ainda está em desenvolvimento.

3. O documento deve explicar que o projeto usa evolução orientada por missões.

4. O documento deve explicar que contribuições devem respeitar:
   - escopo claro;
   - missão em Markdown;
   - referências obrigatórias;
   - testes;
   - compileall;
   - documentação atualizada;
   - commits em português do Brasil;
   - sem git add .;
   - sem force push;
   - sem dependências desnecessárias.

5. O documento deve explicar o fluxo recomendado para contribuir:
   - ler README.md;
   - ler guia de instalação local;
   - preparar ambiente;
   - rodar testes;
   - escolher ou propor missão;
   - criar missão em Markdown;
   - executar via runner apropriado;
   - validar;
   - revisar documentação;
   - abrir pull request futuramente, se o fluxo público for adotado.

6. O documento deve explicar que o fluxo operacional padrão interno é batch quando seguro, mas que contribuidores devem entender o runner de uma missão antes de usar batch.

7. O documento deve explicar quando usar execução individual:
   - mudança arquitetural sensível;
   - alteração em scripts críticos;
   - alteração em Guardian, Policy, Context Router, Runtime ou Providers com impacto amplo;
   - missão com dependências incertas;
   - recuperação após falha;
   - investigação de erro.

8. O documento deve explicar quando usar batch:
   - bloco revisado;
   - missões bem especificadas;
   - dependências claras;
   - risco baixo ou médio;
   - testes estáveis;
   - quota disponível;
   - sem falha recente.

9. O documento deve explicar que batch deve parar na primeira falha.

10. O documento deve explicar que VAF_AUTO_PUSH não é padrão.

11. O documento deve explicar que push manual é preferido após validação.

12. O documento deve conter uma seção sobre padrão de idioma:
   - português do Brasil para documentação, commits, missões e READMEs;
   - termos técnicos arquiteturais podem permanecer em inglês quando forem nomes do projeto.

13. O documento deve conter uma seção sobre mensagens de commit.

14. O documento deve conter exemplos de mensagens de commit, como:
   - missão: enfileirar exemplo
   - implementação: adiciona contrato inicial
   - docs: atualiza guia operacional
   - correção: ajusta validação do runner
   - teste: cobre integração inicial

15. O documento deve conter seção sobre testes obrigatórios:
   - pytest
   - python3 -m compileall src

16. O documento deve conter seção sobre documentação obrigatória:
   - README principal quando afetado;
   - README do módulo afetado;
   - docs/architecture/module-index.md quando módulo novo surgir;
   - roadmap/backlog quando escopo estratégico mudar;
   - docs operacionais quando fluxo operacional mudar.

17. O documento deve conter seção sobre segurança e limites:
   - não registrar secrets;
   - não expor tokens;
   - não alterar configs globais;
   - não usar sudo sem decisão explícita;
   - não acessar rede sem necessidade;
   - não adicionar provider externo sem missão específica;
   - não implementar RAG, embeddings ou pgvector sem missão específica.

18. O documento deve conter seção sobre dependências:
   - não adicionar dependências sem justificativa;
   - preferir biblioteca padrão quando possível;
   - documentar impacto de dependência nova;
   - atualizar arquivos de configuração se existirem.

19. O documento deve conter seção sobre pull requests futuros, mas sem prometer processo público completo se ele ainda não existir.

20. O documento deve conter seção sobre como reportar problemas, de forma inicial e conservadora.

21. O documento deve apontar para documentos relevantes:
   - docs/getting-started/local-installation.md
   - docs/operations/batch-execution-playbook.md
   - docs/operations/post-batch-validation-checklist.md
   - docs/documentation/language-and-commit-standard.md
   - docs/documentation/documentation-update-policy.md
   - docs/architecture/module-index.md
   - docs/roadmap/mission-backlog.md

22. Usar blocos de comando Markdown quando eles tornarem o documento mais claro.

23. Controlar corretamente a quantidade de crases nos blocos Markdown gerados.

24. Não empobrecer a documentação por evitar blocos de comando.

25. Não prometer comportamento ainda não implementado.

Requisitos para docs/contributing/README.md:
1. Criar somente se fizer sentido complementar o CONTRIBUTING.md.

2. Se criado, deve ser breve e apontar para CONTRIBUTING.md.

3. Não duplicar todo o conteúdo de CONTRIBUTING.md.

4. Pode servir como índice futuro para docs de contribuição.

Requisitos para README.md:
1. Adicionar link para CONTRIBUTING.md.

2. Adicionar link para docs/getting-started/local-installation.md se ainda não houver.

3. Manter README enxuto.

4. Não duplicar todo o guia de contribuição.

Requisitos para docs/roadmap/mission-backlog.md:
1. Atualizar somente se o backlog mencionar guia de contribuição como pendente.

2. Marcar guia de contribuição inicial como concluído ou em progresso, conforme o conteúdo real.

3. Manter guias públicos mais completos como futuros se ainda faltarem.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar somente se fizer sentido registrar avanço rumo à documentação alfa.

2. Não reescrever roadmap inteiro.

Requisitos para docs/alignment/current-state.md:
1. Atualizar somente se estiver desatualizado.

2. Registrar que existe guia de contribuição inicial, se fizer sentido.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar automações novas.
- Não criar workflow de CI.
- Não criar template de issue.
- Não criar template de pull request.
- Não criar CODE_OF_CONDUCT nesta missão.
- Não criar SECURITY.md nesta missão.
- Não publicar pacote.
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
- CONTRIBUTING.md existe.
- CONTRIBUTING.md explica fluxo de contribuição por missões.
- CONTRIBUTING.md explica validações com pytest e compileall.
- CONTRIBUTING.md explica padrão de idioma e commits.
- CONTRIBUTING.md explica quando usar batch e quando usar execução individual.
- CONTRIBUTING.md aponta para documentos relevantes.
- README.md aponta para CONTRIBUTING.md.
- docs/contributing/README.md foi criado somente se fizer sentido.
- Roadmap/backlog foram atualizados somente se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

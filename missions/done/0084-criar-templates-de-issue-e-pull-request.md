Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- SECURITY.md
- CODE_OF_CONDUCT.md
- docs/legal/usage-policy.md
- docs/security/vulnerability-reporting.md
- docs/conduct/community-guidelines.md
- docs/release/public-alpha-readiness.md
- docs/getting-started/local-installation.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md

Leia também, se existirem:
- .github/ISSUE_TEMPLATE/
- .github/PULL_REQUEST_TEMPLATE.md
- .github/pull_request_template.md
- .github/ISSUE_TEMPLATE/bug_report.md
- .github/ISSUE_TEMPLATE/feature_request.md
- .github/ISSUE_TEMPLATE/documentation.md
- .github/ISSUE_TEMPLATE/mission_proposal.md
- .github/ISSUE_TEMPLATE/config.yml

Assuma o papel de:
- open-source-maintainer;
- documentation-agent;
- developer-experience-engineer;
- process-governance-agent;
- release-preparation-agent.

Missão:
Criar templates de issue e pull request.

Objetivo:
Criar templates iniciais de issue e pull request para preparar o Vercosa AI Framework para colaboração pública futura, garantindo que relatos de bug, propostas de melhoria, ajustes de documentação, propostas de missão e pull requests sigam o padrão de escopo, segurança, rastreabilidade, testes e documentação do projeto.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto ainda está em desenvolvimento.
- O projeto já possui CONTRIBUTING.md.
- O projeto já possui SECURITY.md inicial.
- O projeto já possui CODE_OF_CONDUCT.md inicial.
- O projeto usa evolução orientada por missões em Markdown.
- O projeto exige documentação e commits em português do Brasil.
- O projeto não deve receber issues que exponham secrets, tokens, credenciais ou detalhes exploráveis de vulnerabilidades.
- Vulnerabilidades devem seguir SECURITY.md e docs/security/vulnerability-reporting.md.
- Os templates devem ser iniciais, claros e conservadores.
- Esta missão não deve criar GitHub Actions.
- Esta missão não deve criar CI.
- Esta missão não deve alterar código.
- Esta missão não deve alterar scripts.
- Esta missão não deve adicionar dependências.

Entregáveis obrigatórios:
1. Criar diretório:
   - .github/ISSUE_TEMPLATE/

2. Criar arquivos:
   - .github/ISSUE_TEMPLATE/bug_report.md
   - .github/ISSUE_TEMPLATE/feature_request.md
   - .github/ISSUE_TEMPLATE/documentation.md
   - .github/ISSUE_TEMPLATE/mission_proposal.md
   - .github/ISSUE_TEMPLATE/config.yml
   - .github/PULL_REQUEST_TEMPLATE.md

3. Atualizar:
   - README.md
   - CONTRIBUTING.md
   - docs/release/public-alpha-readiness.md
   - docs/roadmap/mission-backlog.md

4. Atualizar, se necessário:
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não adicionar dependências.

Requisitos para .github/ISSUE_TEMPLATE/bug_report.md:
1. O template deve estar em português do Brasil.

2. Deve orientar o usuário a não incluir:
   - secrets;
   - tokens;
   - credenciais;
   - chaves de API;
   - dados pessoais sensíveis;
   - logs não sanitizados;
   - detalhes exploráveis de vulnerabilidades.

3. Deve apontar para SECURITY.md quando o relato envolver vulnerabilidade.

4. Deve coletar:
   - descrição do problema;
   - comportamento esperado;
   - comportamento observado;
   - passos para reproduzir;
   - ambiente;
   - branch ou commit, se aplicável;
   - logs sanitizados;
   - impacto percebido;
   - validações já executadas.

5. Deve incluir checklist:
   - li README.md;
   - verifiquei issues existentes, se aplicável;
   - removi dados sensíveis;
   - rodei pytest quando aplicável;
   - rodei python3 -m compileall src quando aplicável;
   - anexei apenas logs sanitizados.

6. Não prometer prazo de resposta.

7. Não prometer suporte formal.

Requisitos para .github/ISSUE_TEMPLATE/feature_request.md:
1. O template deve estar em português do Brasil.

2. Deve coletar:
   - problema que a melhoria resolve;
   - solução proposta;
   - alternativas consideradas;
   - impacto arquitetural;
   - impacto em documentação;
   - impacto em testes;
   - riscos;
   - escopo fora da proposta.

3. Deve orientar que novas integrações com providers, runtimes, banco, RAG, embeddings ou pgvector exigem missão específica e análise.

4. Deve conter checklist de segurança:
   - não exige secrets em texto claro;
   - não exige sudo sem justificativa;
   - não reduz validações;
   - não contorna Policy Engine;
   - não contorna Guardian Engine;
   - não executa automação destrutiva sem aprovação.

5. Deve deixar claro que proposta de melhoria não é garantia de implementação.

Requisitos para .github/ISSUE_TEMPLATE/documentation.md:
1. O template deve estar em português do Brasil.

2. Deve coletar:
   - documento afetado;
   - trecho ou seção afetada;
   - problema encontrado;
   - correção sugerida;
   - impacto em README, guias, arquitetura, operações ou roadmap;
   - links relativos envolvidos;
   - risco de promessa acima do implementado.

3. Deve reforçar que documentação deve permanecer em português do Brasil.

4. Deve lembrar que README.en.md e README.es.md são tarefa futura, não parte de correções comuns agora.

5. Deve incluir checklist:
   - mantive pt-BR;
   - não prometi recurso futuro como implementado;
   - revisei links relativos;
   - atualizei documentos relacionados quando necessário.

Requisitos para .github/ISSUE_TEMPLATE/mission_proposal.md:
1. O template deve estar em português do Brasil.

2. Deve refletir o padrão do projeto de evolução por missões.

3. Deve coletar:
   - título da missão;
   - objetivo;
   - contexto;
   - arquivos obrigatórios para leitura;
   - entregáveis;
   - requisitos;
   - restrições;
   - critérios de aceite;
   - riscos;
   - testes esperados;
   - documentação afetada.

4. Deve orientar que missões devem ter:
   - escopo claro;
   - uma missão por arquivo;
   - restrições explícitas;
   - critérios de aceite verificáveis;
   - atualização documental quando aplicável;
   - testes e compileall;
   - commits em português do Brasil.

5. Deve lembrar:
   - não usar git add .;
   - não fazer force push;
   - não acessar rede sem necessidade;
   - não chamar providers sem missão específica;
   - não alterar scripts críticos sem testes.

6. Deve diferenciar proposta de missão de fila executável.

7. Deve deixar claro que nem toda proposta será enfileirada.

Requisitos para .github/ISSUE_TEMPLATE/config.yml:
1. Deve configurar templates de forma simples.

2. Deve desabilitar blank issues somente se isso fizer sentido para o projeto.

3. Se desabilitar blank issues, oferecer alternativas claras.

4. Deve incluir link para SECURITY.md ou docs/security/vulnerability-reporting.md para vulnerabilidades.

5. Não incluir links externos inventados.

6. Não incluir e-mail inexistente.

Requisitos para .github/PULL_REQUEST_TEMPLATE.md:
1. O template deve estar em português do Brasil.

2. Deve coletar:
   - resumo;
   - missão relacionada;
   - tipo de alteração;
   - arquivos principais alterados;
   - documentação atualizada;
   - testes executados;
   - compileall executado;
   - impacto arquitetural;
   - riscos;
   - limitações;
   - próximos passos.

3. Deve incluir checklist obrigatório:
   - li AGENTS.md;
   - respeitei escopo da missão;
   - não usei git add .;
   - não adicionei dependências sem justificativa;
   - não alterei scripts críticos sem necessidade;
   - não expus secrets;
   - atualizei documentação quando necessário;
   - rodei pytest;
   - rodei python3 -m compileall src;
   - verifiquei git status --short;
   - mantive documentação e commits em português do Brasil.

4. Deve incluir seção específica para segurança:
   - secrets;
   - tokens;
   - credenciais;
   - logs sanitizados;
   - Policy Engine;
   - Guardian Engine;
   - providers;
   - runtimes;
   - automações destrutivas.

5. Deve incluir seção sobre documentação:
   - README.md;
   - README do módulo;
   - docs/architecture/module-index.md;
   - docs/alignment/current-state.md;
   - docs/roadmap/mission-backlog.md;
   - docs/operations quando aplicável.

6. Deve deixar claro que PR sem testes ou sem justificativa pode precisar de revisão adicional.

7. Não prometer merge automático.

8. Não prometer SLA de revisão.

Requisitos para README.md:
1. Adicionar referência curta para CONTRIBUTING.md e templates, se fizer sentido.

2. Manter README enxuto.

3. Não duplicar os templates no README.

Requisitos para CONTRIBUTING.md:
1. Adicionar seção curta sobre issues e pull requests.

2. Apontar para:
   - .github/ISSUE_TEMPLATE/
   - .github/PULL_REQUEST_TEMPLATE.md
   - SECURITY.md
   - CODE_OF_CONDUCT.md

3. Explicar que vulnerabilidades não devem ser relatadas como issue pública com detalhes exploráveis.

4. Explicar que propostas de missão devem seguir o template adequado.

5. Manter CONTRIBUTING.md enxuto.

Requisitos para docs/release/public-alpha-readiness.md:
1. Atualizar checklist para marcar templates de issue e pull request como criados.

2. Manter pendentes itens ainda não executados, como:
   - changelog inicial;
   - versão alfa inicial;
   - teste de instalação limpa;
   - CI público, se ainda não existir;
   - internacionalização dos READMEs.

3. Não declarar alfa pública como publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar templates de issue e pull request como concluídos ou em progresso conforme esta missão.

2. Manter como futuras:
   - política de release;
   - changelog inicial;
   - versão alfa inicial;
   - CI público;
   - internacionalização dos READMEs.

3. Não criar missões novas na fila.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem simples, prática e conservadora.

3. Não inventar canal externo.

4. Não expor dados pessoais.

5. Não criar workflow de CI.

6. Não criar GitHub Actions.

7. Não alterar código.

8. Não alterar scripts.

9. Não adicionar dependências.

10. Usar links relativos corretos.

11. Usar blocos Markdown quando úteis.

12. Controlar corretamente a quantidade de crases nos blocos Markdown.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não criar CI.
- Não criar GitHub Actions.
- Não criar changelog nesta missão.
- Não criar versão.
- Não criar tag.
- Não publicar release.
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
- .github/ISSUE_TEMPLATE/bug_report.md existe.
- .github/ISSUE_TEMPLATE/feature_request.md existe.
- .github/ISSUE_TEMPLATE/documentation.md existe.
- .github/ISSUE_TEMPLATE/mission_proposal.md existe.
- .github/ISSUE_TEMPLATE/config.yml existe.
- .github/PULL_REQUEST_TEMPLATE.md existe.
- Templates orientam a não expor secrets, tokens ou credenciais.
- Templates apontam para SECURITY.md quando aplicável.
- Pull request template exige testes e compileall.
- CONTRIBUTING.md aponta para templates.
- README.md foi atualizado somente se necessário.
- docs/release/public-alpha-readiness.md registra templates como criados.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

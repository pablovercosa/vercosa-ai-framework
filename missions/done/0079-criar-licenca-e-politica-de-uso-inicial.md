Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/getting-started/local-installation.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md

Leia também, se existirem:
- LICENSE
- LICENSE.md
- NOTICE
- SECURITY.md
- CODE_OF_CONDUCT.md
- docs/legal/README.md
- docs/legal/usage-policy.md
- docs/legal/license-notes.md

Assuma o papel de:
- open-source-maintainer;
- documentation-agent;
- release-preparation-agent;
- risk-reviewer;
- technical-editor.

Missão:
Criar licença e política de uso inicial.

Objetivo:
Preparar a base documental inicial de licenciamento e uso do Vercosa AI Framework para uma futura abertura pública/alfa, criando um arquivo de licença quando houver decisão segura e documentando uma política inicial de uso responsável, sem transformar esta missão em consultoria jurídica e sem prometer maturidade pública completa.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto precisa de documentação mínima sobre licença, uso permitido, limitações e responsabilidades.
- O projeto ainda está em desenvolvimento.
- O projeto é um framework de Harness Engineering para agentes de IA.
- O projeto pode futuramente integrar providers, runtimes, tools, RAG, embeddings, pgvector e automações externas.
- O projeto ainda não deve prometer segurança absoluta, conformidade regulatória ou adequação a uso crítico.
- O projeto deve ser apresentado como software em desenvolvimento.
- Esta missão deve criar documentação inicial e conservadora.
- Esta missão não deve implementar qualquer mecanismo técnico de bloqueio.
- Esta missão não deve adicionar dependências.
- Esta missão não deve alterar código.
- Esta missão não deve acessar rede para copiar textos legais.
- Se já existir licença no repositório, ela deve ser preservada e documentada, não substituída sem justificativa explícita.
- Se não existir licença e houver incerteza sobre qual licença usar, criar documentação preparatória e registrar a decisão pendente, em vez de inventar uma licença final sem segurança.

Entregáveis obrigatórios:
1. Criar diretório, se necessário:
   - docs/legal/

2. Criar:
   - docs/legal/README.md
   - docs/legal/usage-policy.md
   - docs/legal/license-notes.md

3. Criar ou atualizar, somente se seguro:
   - LICENSE

4. Atualizar:
   - README.md
   - CONTRIBUTING.md

5. Atualizar, se necessário:
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md
   - docs/roadmap/mission-backlog.md

6. Não alterar código Python.

7. Não alterar scripts shell.

8. Não adicionar dependências.

Requisitos para LICENSE:
1. Verificar se já existe LICENSE, LICENSE.md ou equivalente.

2. Se já existir licença:
   - não substituir automaticamente;
   - preservar conteúdo existente;
   - apenas garantir que README.md e docs/legal/license-notes.md apontem para ela.

3. Se não existir licença:
   - criar LICENSE somente se houver decisão documental clara no repositório ou se a opção adotada for explicitamente justificada em docs/legal/license-notes.md;
   - usar licença permissiva simples apenas se isso estiver coerente com o posicionamento do projeto;
   - se houver dúvida relevante, não criar LICENSE final e registrar a pendência em docs/alignment/open-questions.md.

4. Não copiar texto legal de fonte externa via rede.

5. Não inventar licença personalizada complexa.

6. Não misturar múltiplas licenças sem necessidade.

7. Não prometer que a escolha de licença é aconselhamento jurídico.

8. Se criar LICENSE, usar texto padrão conhecido e estável de licença permissiva reconhecida, com copyright:
   - Copyright (c) 2026 Pablo Verçosa

9. Se criar LICENSE, garantir que README.md aponte para ela.

10. Se não criar LICENSE por decisão de prudência, README.md deve informar que a licença ainda será definida antes de release pública.

Requisitos para docs/legal/README.md:
1. Explicar o propósito da pasta docs/legal.

2. Apontar para:
   - LICENSE, se existir;
   - docs/legal/usage-policy.md;
   - docs/legal/license-notes.md;
   - CONTRIBUTING.md;
   - README.md.

3. Explicar que esta documentação é inicial.

4. Explicar que não substitui revisão jurídica formal.

5. Manter linguagem simples e objetiva.

Requisitos para docs/legal/license-notes.md:
1. Explicar o estado atual da licença do projeto.

2. Registrar se LICENSE foi criado ou se a decisão ficou pendente.

3. Se LICENSE for criado, explicar:
   - qual licença foi adotada;
   - por que ela foi escolhida;
   - quais alternativas foram consideradas;
   - quais alternativas ficaram para avaliação futura.

4. Se LICENSE não for criado, explicar:
   - por que a decisão ficou pendente;
   - quais pontos precisam ser resolvidos antes de release pública.

5. Considerar alternativas comuns de forma conceitual, sem copiar textos legais longos:
   - MIT;
   - Apache-2.0;
   - BSD-3-Clause;
   - GPL;
   - licença proprietária.

6. Explicar, em linguagem não jurídica, diferenças gerais:
   - licença permissiva;
   - licença copyleft;
   - licença proprietária;
   - licença ainda pendente.

7. Não fazer aconselhamento jurídico.

8. Não afirmar obrigações legais específicas com tom absoluto.

9. Não acessar rede.

10. Manter o documento em português do Brasil.

Requisitos para docs/legal/usage-policy.md:
1. Criar política inicial de uso responsável do projeto.

2. Explicar que o VAF é um framework de desenvolvimento e orquestração governada de agentes de IA.

3. Explicar usos pretendidos:
   - pesquisa;
   - desenvolvimento local;
   - automação assistida;
   - prototipação;
   - documentação;
   - execução governada de missões;
   - experimentos controlados de Harness Engineering.

4. Explicar usos que exigem cautela:
   - produção;
   - automações com impacto financeiro;
   - automações com impacto jurídico;
   - automações com impacto médico;
   - automações com impacto trabalhista;
   - automações com dados sensíveis;
   - execução de ferramentas externas;
   - integração com providers pagos;
   - integração com banco de dados;
   - integração com runtimes remotos.

5. Explicar usos não recomendados nesta fase:
   - decisões autônomas de alto risco;
   - execução sem revisão humana;
   - uso com credenciais expostas;
   - processamento de dados sensíveis sem controles adicionais;
   - automação destrutiva sem aprovação explícita;
   - uso como sistema de segurança crítica;
   - uso como substituto de aconselhamento profissional.

6. Explicar princípios de uso:
   - revisão humana;
   - menor privilégio;
   - rastreabilidade;
   - logs sem vazamento de segredo;
   - validação antes de execução;
   - testes antes de publicação;
   - providers sob controle;
   - execução em ambiente isolado quando possível.

7. Explicar limites atuais:
   - framework em desenvolvimento;
   - sem garantia de estabilidade;
   - sem garantia de adequação a produção;
   - sem conformidade regulatória declarada;
   - sem política formal de segurança pública ainda;
   - sem release estável.

8. Explicar que integrações futuras com providers, tools, runtimes, RAG ou banco devem ser avaliadas caso a caso.

9. Explicar que o usuário/contribuidor é responsável por revisar missões, comandos, scripts e efeitos antes de execução.

10. Não usar tom alarmista.

11. Não usar tom jurídico excessivo.

12. Não prometer bloqueios técnicos que não existem.

13. Não criar regras que contradigam AGENTS.md.

14. Manter em português do Brasil.

Requisitos para README.md:
1. Adicionar seção curta ou link para licença e uso responsável.

2. Se LICENSE existir, apontar para LICENSE.

3. Se LICENSE não existir, informar que a licença será definida antes de release pública.

4. Apontar para:
   - docs/legal/usage-policy.md
   - docs/legal/license-notes.md

5. Manter README enxuto.

6. Não duplicar a política inteira no README.

Requisitos para CONTRIBUTING.md:
1. Adicionar referência à política de uso responsável.

2. Adicionar referência à licença ou à decisão pendente.

3. Reforçar que contribuições não devem:
   - incluir secrets;
   - incluir credenciais;
   - adicionar dependências sem justificativa;
   - adicionar providers externos sem missão específica;
   - introduzir automações destrutivas sem aprovação explícita;
   - prometer conformidade ou segurança absoluta.

4. Manter CONTRIBUTING.md enxuto.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se a licença ficar pendente ou se surgirem perguntas relevantes.

2. Perguntas possíveis:
   - licença final antes da release pública;
   - política de segurança pública;
   - política de vulnerabilidades;
   - limites de uso com providers pagos;
   - modelo de release alfa.

Requisitos para docs/roadmap/mission-backlog.md:
1. Atualizar somente se houver item pendente sobre licença ou política de uso.

2. Marcar esta base documental como criada, se for o caso.

3. Manter tarefas futuras como:
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - templates de issue;
   - templates de pull request;
   - política de release;
   - revisão de licença antes de release pública.

Requisitos gerais:
1. Tudo deve estar em português do Brasil, exceto nomes oficiais de licenças e arquivos.

2. Usar linguagem factual e conservadora.

3. Diferenciar:
   - licença;
   - política de uso;
   - segurança;
   - contribuição;
   - release pública futura.

4. Não prometer conformidade regulatória.

5. Não prometer segurança absoluta.

6. Não fazer aconselhamento jurídico.

7. Não acessar rede.

8. Não alterar código.

9. Não alterar scripts.

10. Não adicionar dependências.

11. Usar links relativos corretos.

12. Usar blocos Markdown quando úteis.

13. Controlar corretamente a quantidade de crases nos blocos Markdown.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar mecanismos técnicos de política.
- Não implementar verificação de licença.
- Não criar workflow de CI.
- Não criar SECURITY.md nesta missão.
- Não criar CODE_OF_CONDUCT.md nesta missão.
- Não criar templates de issue.
- Não criar templates de pull request.
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
- docs/legal/README.md existe.
- docs/legal/usage-policy.md existe.
- docs/legal/license-notes.md existe.
- LICENSE foi criado somente se a decisão for segura e justificada.
- Se LICENSE não foi criado, a pendência está documentada.
- README.md aponta para licença ou pendência de licença.
- README.md aponta para política de uso responsável.
- CONTRIBUTING.md aponta para política de uso responsável.
- Documentação não faz aconselhamento jurídico.
- Documentação não promete conformidade regulatória.
- Documentação não promete segurança absoluta.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

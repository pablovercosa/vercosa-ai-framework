Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
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

Leia também, se existirem:
- docs/examples/cli-diagnostics-flow.md
- docs/examples/audit-event-flow.md
- src/vercosa_ai_framework/audit/README.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/missions/README.md

Assuma o papel de:
- framework-architect;
- roadmap-planner;
- documentation-agent;
- consistency-reviewer;
- process-governance-agent.

Missão:
Revisar roadmap e backlog após validação funcional do batch.

Objetivo:
Atualizar o roadmap, o backlog estratégico e os documentos de alinhamento para refletir o estado real do projeto após a validação do fluxo em batch, a conclusão das missões 0062 a 0071, a criação da CLI operacional, do Audit/Event Log, dos exemplos operacionais e a decisão de padronizar batch como fluxo operacional quando seguro.

Contexto:
- O projeto validou batch de 3 missões.
- O projeto executou um bloco de 10 missões, com interrupção por limite externo de API e retomada posterior.
- As missões 0062 a 0071 foram concluídas e publicadas antes desta missão.
- O projeto passou a ter integrações adicionais:
  - Policy Engine com Model Selection;
  - Token Budget Manager com Model Selection;
  - Usage/API Limit Guard integrado ao fluxo operacional;
  - Audit/Event Log inicial;
  - eventos auditáveis de decisões centrais;
  - eventos auditáveis do Mission Runner;
  - CLI operacional inicial;
  - comando validate na CLI;
  - comando doctor na CLI;
  - exemplos operacionais iniciais.
- A missão 0072 deve atualizar README com identidade de Harness Engineering e auditar READMEs.
- A missão 0073 deve padronizar batch como fluxo operacional.
- Agora o roadmap e o backlog precisam refletir esse novo estado.
- A documentação deve continuar distinguindo implementado, MVP, integração inicial, futuro e fora do escopo.
- A internacionalização dos READMEs continua sendo tarefa futura, não deve ser executada agora.

Entregáveis obrigatórios:
1. Atualizar:
   - docs/alignment/roadmap.md
   - docs/roadmap/mission-backlog.md
   - docs/alignment/current-state.md

2. Atualizar, se necessário:
   - docs/alignment/architecture-map.md
   - docs/alignment/open-questions.md
   - README.md

3. Não alterar código Python.

4. Não alterar scripts shell.

5. Não adicionar dependências.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar o roadmap para refletir que a fase operacional avançou.

2. Registrar que o projeto já possui:
   - runner seguro de uma missão;
   - runner seguro em batch;
   - batch de 3 validado;
   - batch de 10 funcional, com ressalva de limites externos de API;
   - Policy Engine integrado ao Guardian Engine;
   - Policy Engine integrado ao Context Router;
   - Policy Engine integrado ao Model Selection;
   - Token Budget integrado ao Model Selection;
   - Usage/API Limit Guard;
   - Audit/Event Log inicial;
   - CLI operacional inicial;
   - exemplos operacionais.

3. Registrar que batch é padrão operacional quando seguro, conforme missão 0073.

4. Registrar que execução individual permanece necessária para missões críticas, sensíveis ou de alto risco.

5. Reorganizar próximos blocos prováveis sem criar excesso de detalhe.

6. Manter como futuros:
   - persistência externa de eventos;
   - integração real com providers;
   - múltiplos runtimes reais;
   - RAG semântico;
   - embeddings;
   - pgvector;
   - Semantic Index;
   - internacionalização dos READMEs;
   - release alfa.

7. Não prometer recursos futuros como implementados.

8. Manter links relativos corretos.

Requisitos para docs/roadmap/mission-backlog.md:
1. Atualizar o backlog estratégico para refletir que algumas missões planejadas já foram executadas.

2. Marcar como concluídas ou absorvidas no estado atual, quando aplicável:
   - integração Policy Engine com Model Selection;
   - integração Token Budget com Model Selection;
   - integração Usage/API Limit Guard ao fluxo operacional;
   - Audit/Event Log inicial;
   - eventos auditáveis de decisões centrais;
   - eventos auditáveis do Mission Runner;
   - CLI operacional inicial;
   - comando validate;
   - comando doctor;
   - exemplos operacionais iniciais;
   - README com Harness Engineering, se a missão anterior tiver feito isso;
   - batch como padrão operacional, se a missão anterior tiver feito isso.

3. Reorganizar próximas missões prováveis sem duplicar tarefas já concluídas.

4. Incluir novas missões futuras recomendadas, se fizer sentido:
   - integrar CLI com validações de Git de forma segura;
   - criar comando CLI para listar missões;
   - criar comando CLI para resumo pós-batch;
   - persistir eventos auditáveis em arquivo local controlado;
   - criar guia público de instalação;
   - criar guia de contribuição;
   - criar licença;
   - preparar documentação pública alfa;
   - revisar arquitetura pós-integrações;
   - avaliar providers reais;
   - avaliar Semantic Index;
   - internacionalizar READMEs no final.

5. Manter a distinção entre backlog estratégico e fila executável.

6. Reforçar que a fila executável deve receber blocos revisados, não todo o backlog.

7. Manter a recomendação de batch de 10 quando seguro.

8. Manter batch de 3 para retomadas, validação ou blocos menores.

9. Manter execução individual para missões sensíveis.

10. Não criar missões em missions/queue nesta missão.

Requisitos para docs/alignment/current-state.md:
1. Atualizar o estado atual com base no que foi efetivamente implementado.

2. Registrar módulos existentes:
   - audit;
   - cli;
   - policy;
   - guardian;
   - context;
   - model_selection;
   - missions;
   - providers;
   - runtime;
   - knowledge;
   - persistence;
   - workflows;
   - tasks;
   - agents;
   - capabilities;
   - skills;
   - tools.

3. Registrar integrações centrais já feitas.

4. Registrar que o projeto está em transição para MVP interno mais coerente.

5. Registrar limites atuais:
   - sem RAG semântico;
   - sem embeddings;
   - sem pgvector;
   - sem persistência externa de eventos;
   - sem provider real integrado como caminho obrigatório;
   - sem billing real;
   - sem observabilidade externa.

6. Registrar que Usage/API Limit Guard existe e que limites externos de API podem interromper batch.

7. Não prometer comportamento ainda não implementado.

Requisitos para docs/alignment/architecture-map.md:
1. Atualizar somente se estiver desatualizado.

2. Garantir que Audit/Event Log e CLI estejam representados.

3. Garantir que o fluxo Policy, Context, Guardian, Model Selection e Audit esteja coerente.

4. Não redesenhar toda a arquitetura sem necessidade.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver perguntas já resolvidas ou novas perguntas claras.

2. Remover ou marcar como resolvidas perguntas que já foram decididas, se existirem.

3. Adicionar perguntas abertas relevantes, se necessário, como:
   - qual será o formato de persistência de eventos auditáveis;
   - quando integrar providers reais;
   - quando iniciar Semantic Index;
   - como versionar políticas declarativas;
   - quando internacionalizar READMEs.

Requisitos para README.md:
1. Atualizar somente se as missões anteriores deixarem alguma referência desalinhada.

2. Não transformar README em roadmap longo.

3. Manter README como entrada principal.

Requisitos gerais de documentação:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem factual.

3. Diferenciar claramente:
   - implementado;
   - MVP;
   - integração inicial;
   - futuro;
   - fora do escopo.

4. Usar blocos de comando Markdown nos documentos finais quando eles tornarem a documentação mais clara.

5. Controlar corretamente a quantidade de crases nos blocos Markdown gerados.

6. Não empobrecer documentação operacional por evitar blocos de comando.

7. Não usar blocos de comando desnecessários.

8. Manter links relativos corretos.

9. Evitar duplicação excessiva.

10. Não prometer comportamento ainda não implementado.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar novas funcionalidades.
- Não adicionar dependências.
- Não criar arquivos em missions/queue.
- Não executar missões.
- Não alterar fluxo Git.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/alignment/roadmap.md reflete o estado pós-batch funcional.
- docs/roadmap/mission-backlog.md foi atualizado para remover ou marcar itens já concluídos.
- docs/alignment/current-state.md reflete módulos e integrações atuais.
- docs/alignment/architecture-map.md foi atualizado se necessário.
- docs/alignment/open-questions.md foi atualizado se necessário.
- README.md foi atualizado somente se necessário.
- O backlog continua separado da fila executável.
- O roadmap não promete recursos futuros como implementados.
- A documentação menciona batch como padrão operacional quando seguro, se a missão 0073 tiver feito isso.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

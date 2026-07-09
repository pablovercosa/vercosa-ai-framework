Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
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
- docs/release/public-alpha-readiness.md
- docs/examples/README.md
- src/vercosa_ai_framework/agents/README.md
- src/vercosa_ai_framework/audit/README.md
- src/vercosa_ai_framework/canonicalizer/README.md
- src/vercosa_ai_framework/capabilities/README.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/core/README.md
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/knowledge/README.md
- src/vercosa_ai_framework/missions/README.md
- src/vercosa_ai_framework/model_selection/README.md
- src/vercosa_ai_framework/persistence/README.md
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/providers/README.md
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/skills/README.md
- src/vercosa_ai_framework/tasks/README.md
- src/vercosa_ai_framework/tools/README.md
- src/vercosa_ai_framework/workflows/README.md

Assuma o papel de:
- framework-architect;
- architecture-reviewer;
- documentation-agent;
- consistency-reviewer;
- release-preparation-agent.

Missão:
Revisar arquitetura pós-integrações.

Objetivo:
Revisar a documentação arquitetural do Vercosa AI Framework após as integrações concluídas até a missão 0080, garantindo que a visão de módulos, fluxos, responsabilidades, limites atuais e próximos passos estejam coerentes com o estado real do projeto.

Contexto:
- O projeto já concluiu as missões até 0080.
- O README principal já incorporou a identidade de Harness Engineering.
- O batch foi padronizado como fluxo operacional quando seguro.
- O roadmap e backlog foram revisados após batch funcional.
- A CLI operacional, validate e doctor já existem.
- O Audit/Event Log inicial já existe e foi documentado.
- Guias públicos iniciais foram criados.
- A documentação pública alfa foi preparada.
- O projeto precisa agora de uma revisão arquitetural pós-integrações para eliminar desalinhamentos e consolidar a visão antes das próximas missões.
- Esta missão não deve implementar código.
- Esta missão não deve alterar scripts.
- Esta missão não deve adicionar dependências.
- Esta missão deve ser documental, conservadora e factual.

Entregáveis obrigatórios:
1. Criar documento:
   - docs/architecture/post-integration-architecture-review.md

2. Atualizar:
   - docs/architecture/module-index.md
   - docs/alignment/architecture-map.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/roadmap/mission-backlog.md

3. Atualizar, se necessário:
   - README.md
   - docs/release/public-alpha-readiness.md
   - docs/alignment/open-questions.md

4. Não alterar código Python.

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos para docs/architecture/post-integration-architecture-review.md:
1. O documento deve estar em português do Brasil.

2. Explicar que se trata de uma revisão arquitetural pós-integrações.

3. Registrar o estado arquitetural atual do projeto de forma factual.

4. Explicar o VAF como framework de Harness Engineering.

5. Explicar os eixos arquiteturais atuais:
   - execução de missões;
   - governança;
   - contexto;
   - seleção de modelo;
   - runtime;
   - providers;
   - auditoria;
   - CLI operacional;
   - documentação operacional;
   - preparação pública alfa.

6. Documentar módulos centrais e responsabilidades:
   - agents;
   - audit;
   - canonicalizer;
   - capabilities;
   - cli;
   - context;
   - core;
   - guardian;
   - knowledge;
   - missions;
   - model_selection;
   - persistence;
   - policy;
   - providers;
   - runtime;
   - skills;
   - tasks;
   - tools;
   - workflows.

7. Explicar integrações já existentes:
   - Policy Engine com Guardian Engine;
   - Policy Engine com Context Router;
   - Policy Engine com Model Selection;
   - Token Budget Manager com Model Selection;
   - Usage/API Limit Guard com fluxo operacional;
   - Audit/Event Log com decisões centrais;
   - Audit/Event Log com Mission Runner;
   - CLI com status, validate e doctor;
   - batch como fluxo operacional padrão quando seguro.

8. Explicar fluxos arquiteturais de alto nível:
   - missão;
   - runner;
   - validação;
   - política;
   - contexto;
   - guardian;
   - seleção de modelo;
   - runtime;
   - provider;
   - auditoria;
   - documentação.

9. Diferenciar claramente:
   - implementado;
   - MVP;
   - integração inicial;
   - futuro;
   - fora do escopo atual.

10. Registrar limites atuais:
   - sem RAG semântico;
   - sem embeddings;
   - sem pgvector;
   - sem Semantic Index;
   - sem banco de dados operacional;
   - sem persistência externa de eventos;
   - sem múltiplos providers reais em produção;
   - sem múltiplos runtimes reais em produção;
   - sem dashboard;
   - sem CI público;
   - sem release alfa publicada;
   - sem internacionalização dos READMEs.

11. Registrar riscos arquiteturais atuais:
   - documentação crescendo antes da release;
   - risco de promessa pública acima do implementado;
   - dependência operacional do runtime atual;
   - ausência de persistência externa de auditoria;
   - ausência de validação de instalação limpa;
   - ausência de política pública de segurança;
   - ausência de versionamento alfa formal.

12. Registrar próximos refinamentos arquiteturais possíveis:
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - templates de issue e pull request;
   - changelog inicial;
   - versão alfa inicial;
   - checklist de instalação limpa;
   - comandos CLI para listar missões;
   - comando CLI para resumo pós-batch;
   - persistência local controlada de eventos auditáveis;
   - integração real com providers;
   - avaliação de Semantic Index;
   - internacionalização dos READMEs no final.

13. Incluir seção de decisões arquiteturais consolidadas:
   - README.md canônico em português do Brasil;
   - internacionalização no final;
   - batch padrão quando seguro;
   - execução individual para missões sensíveis;
   - OpenCode como runtime/laboratório atual, não núcleo;
   - sem banco por enquanto;
   - sem RAG por enquanto;
   - sem pgvector por enquanto;
   - eventos auditáveis sem persistência externa por enquanto;
   - push manual por padrão.

14. Incluir seção de recomendações para próximas missões.

15. Não transformar o documento em backlog completo.

16. Não duplicar integralmente README ou roadmap.

17. Usar links relativos corretos.

18. Usar blocos Markdown quando úteis.

19. Controlar corretamente a quantidade de crases nos blocos Markdown.

20. Não prometer funcionalidades futuras como implementadas.

Requisitos para docs/architecture/module-index.md:
1. Verificar se todos os módulos existentes estão listados.

2. Verificar se descrições estão coerentes com o estado atual.

3. Garantir que audit, cli, policy, guardian, context, model_selection, runtime, providers e missions estejam bem descritos.

4. Adicionar link para docs/architecture/post-integration-architecture-review.md.

5. Não duplicar conteúdo extenso do documento novo.

Requisitos para docs/alignment/architecture-map.md:
1. Atualizar o mapa para refletir integrações atuais.

2. Representar relação entre:
   - Mission Runner;
   - Workflow Engine;
   - Task Queue;
   - Agent Orchestrator;
   - Policy Engine;
   - Guardian Engine;
   - Context Router;
   - Token Budget Manager;
   - Model Selection Engine;
   - Provider Gateway;
   - Runtime Adapter;
   - Usage/API Limit Guard;
   - Audit/Event Log;
   - CLI operacional.

3. Diferenciar fluxo implementado de fluxo futuro.

4. Não prometer integrações futuras como existentes.

Requisitos para docs/alignment/current-state.md:
1. Atualizar o estado atual após a missão 0080.

2. Registrar que existe revisão arquitetural pós-integrações.

3. Registrar estado real do projeto sem exagero.

4. Manter limites atuais explícitos.

Requisitos para docs/alignment/roadmap.md:
1. Atualizar somente os pontos necessários.

2. Registrar que a revisão arquitetural pós-integrações foi criada.

3. Manter próximos passos coerentes.

4. Não reescrever todo o roadmap sem necessidade.

Requisitos para docs/roadmap/mission-backlog.md:
1. Registrar a conclusão ou criação desta revisão arquitetural.

2. Reorganizar próximas missões se houver duplicidade.

3. Manter como futuras:
   - SECURITY.md;
   - CODE_OF_CONDUCT.md;
   - templates de issue e pull request;
   - changelog inicial;
   - versão alfa inicial;
   - checklist de instalação limpa;
   - comandos adicionais da CLI;
   - persistência local de eventos auditáveis;
   - internacionalização dos READMEs.

4. Não criar arquivos em missions/queue.

Requisitos para README.md:
1. Atualizar somente se houver desalinhamento arquitetural.

2. Se atualizado, apontar para a revisão arquitetural pós-integrações.

3. Manter README enxuto.

Requisitos para docs/release/public-alpha-readiness.md:
1. Atualizar somente se a revisão arquitetural alterar ou completar checklist de prontidão.

2. Não declarar alfa pública como publicada.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se novas perguntas forem necessárias ou se perguntas antigas tiverem sido resolvidas.

2. Possíveis perguntas:
   - qual será a estratégia de persistência de eventos;
   - qual será a versão alfa inicial;
   - qual será a política pública de segurança;
   - quando iniciar providers reais;
   - quando iniciar Semantic Index;
   - quando internacionalizar READMEs.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar funcionalidades.
- Não adicionar dependências.
- Não criar SECURITY.md nesta missão.
- Não criar CODE_OF_CONDUCT.md nesta missão.
- Não criar templates de issue.
- Não criar templates de pull request.
- Não criar changelog inicial.
- Não criar versão.
- Não criar tag.
- Não publicar release.
- Não criar README.en.md.
- Não criar README.es.md.
- Não internacionalizar READMEs.
- Não implementar RAG.
- Não implementar embeddings.
- Não implementar pgvector.
- Não implementar Semantic Index.
- Não implementar persistência externa de eventos.
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
- docs/architecture/post-integration-architecture-review.md existe.
- O documento consolida a arquitetura pós-integrações.
- O documento diferencia implementado, MVP, integração inicial, futuro e fora do escopo.
- O documento lista limites atuais sem prometer recursos futuros.
- docs/architecture/module-index.md aponta para a revisão.
- docs/alignment/architecture-map.md reflete integrações atuais.
- docs/alignment/current-state.md foi atualizado se necessário.
- docs/alignment/roadmap.md foi atualizado se necessário.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- README.md foi atualizado somente se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

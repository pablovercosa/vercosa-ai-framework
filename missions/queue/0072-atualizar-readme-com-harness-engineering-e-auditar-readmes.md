Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/roadmap/mission-backlog.md
- docs/examples/README.md
- docs/examples/mission-batch-operational-flow.md
- docs/examples/policy-context-guardian-flow.md
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
- documentation-agent;
- framework-architect;
- developer-experience-engineer;
- technical-editor;
- consistency-reviewer.

Missão:
Atualizar README principal com a identidade de Harness Engineering e auditar READMEs do projeto.

Objetivo:
Atualizar o README principal para apresentar o Vercosa AI Framework como um framework de Harness Engineering para agentes de IA, além de auditar os READMEs dos módulos para verificar se estão coerentes com o estado atual do projeto, em português do Brasil e sem prometer funcionalidades ainda não implementadas.

Contexto:
- O projeto evoluiu de uma fundação modular para um framework de execução governada com IA.
- O projeto já possui Mission Runner, runners seguros, runner em batch, Policy Engine, Guardian Engine, Context Router, Token Budget Manager, Knowledge Hub, Model Selection Engine, Runtime Adapter, Provider Gateway, Usage/API Limit Guard, Audit/Event Log e CLI operacional.
- O usuário identificou corretamente que o projeto se enquadra como Harness Engineering.
- O README principal deve refletir essa identidade.
- Os READMEs dos módulos vêm sendo criados e atualizados ao longo das missões, mas precisam de auditoria de consistência após as integrações recentes.
- A internacionalização dos READMEs continua sendo uma tarefa futura, não deve ser feita agora.
- O README.md continua sendo o documento canônico em português do Brasil.

Entregáveis obrigatórios:
1. Atualizar:
   - README.md

2. Auditar e atualizar, quando necessário, READMEs de módulos em:
   - src/vercosa_ai_framework/*/README.md

3. Atualizar, quando necessário:
   - docs/architecture/module-index.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/roadmap/mission-backlog.md

4. Não criar README.en.md.

5. Não criar README.es.md.

6. Não alterar código Python.

7. Não alterar scripts shell.

8. Não adicionar dependências.

Requisitos para README.md:
1. O README principal deve estar em português do Brasil.

2. O README deve apresentar logo no início que o Vercosa AI Framework é um framework de Harness Engineering para agentes de IA.

3. O README deve explicar que o projeto não trata o modelo como o sistema inteiro.

4. O README deve explicar que o framework constrói a camada operacional ao redor do modelo, incluindo:
   - missões;
   - runners;
   - contexto;
   - orçamento de tokens;
   - políticas;
   - guardrails;
   - auditoria;
   - seleção de modelos;
   - providers;
   - runtimes;
   - validações;
   - CLI operacional.

5. O README deve diferenciar, de forma simples:
   - Prompt Engineering;
   - Agent Framework;
   - Harness Engineering.

6. O README deve explicar que o VAF é focado em:
   - execução governada;
   - rastreabilidade;
   - segurança operacional;
   - evolução por missões;
   - separação de responsabilidades;
   - testes;
   - documentação progressiva.

7. O README deve conter uma visão arquitetural atualizada dos módulos centrais.

8. O README deve mencionar o fluxo conceitual principal:
   - Mission Runner;
   - Workflow Engine;
   - Task Queue;
   - Agent Orchestrator;
   - Capabilities;
   - Skills;
   - Tools;
   - Provider Gateway;
   - Runtime Adapter.

9. O README deve mencionar o eixo de governança:
   - Policy Engine;
   - Guardian Engine;
   - Usage/API Limit Guard;
   - Audit/Event Log.

10. O README deve mencionar o eixo de contexto e memória:
   - Knowledge Hub;
   - Context Router;
   - Token Budget Manager;
   - ContextPackage.

11. O README deve mencionar o eixo operacional:
   - runner seguro de uma missão;
   - runner seguro em batch;
   - CLI operacional;
   - playbooks;
   - checklists.

12. O README deve deixar claro que OpenCode é runtime/laboratório atual, não núcleo do framework.

13. O README deve deixar claro que o VAF é model agnostic, provider agnostic, runtime agnostic e storage agnostic como direção arquitetural.

14. O README deve marcar claramente recursos ainda futuros:
   - RAG semântico;
   - embeddings;
   - pgvector;
   - Semantic Index;
   - múltiplos providers reais;
   - persistência externa de eventos;
   - internacionalização dos READMEs.

15. O README não deve prometer que esses recursos futuros já existem.

16. O README deve apontar para documentos relevantes com links relativos:
   - docs/architecture/module-index.md
   - docs/roadmap/mission-backlog.md
   - docs/operations/batch-execution-playbook.md
   - docs/operations/post-batch-validation-checklist.md
   - docs/examples/README.md

17. O README deve permanecer enxuto o suficiente para entrada pública futura, sem virar um manual completo.

Requisitos para auditoria de READMEs de módulos:
1. Verificar se cada README de módulo existe para os módulos principais.

2. Atualizar somente quando houver incoerência, desatualização ou promessa indevida.

3. Garantir que os READMEs estejam em português do Brasil.

4. Garantir que os READMEs expliquem o papel atual do módulo.

5. Garantir que os READMEs diferenciem:
   - implementado;
   - MVP;
   - integração inicial;
   - futuro;
   - fora do escopo.

6. Garantir que os READMEs não prometam integrações ainda não implementadas.

7. Garantir que os READMEs recentes reflitam as missões 0062 a 0071, quando aplicável:
   - Policy Engine + Model Selection;
   - Token Budget + Model Selection;
   - Usage/API Limit Guard operacional;
   - Audit/Event Log;
   - eventos auditáveis;
   - CLI operacional;
   - validate;
   - doctor;
   - exemplos operacionais.

8. Garantir que os READMEs dos módulos abaixo estejam especialmente coerentes:
   - audit;
   - cli;
   - policy;
   - guardian;
   - context;
   - model_selection;
   - missions;
   - runtime;
   - providers.

9. Corrigir links relativos quebrados quando identificados.

10. Não fazer reescrita desnecessária de todos os READMEs.

Requisitos para docs/architecture/module-index.md:
1. Atualizar apenas se o índice não refletir módulos recentes.

2. Garantir que audit e cli estejam listados se ainda não estiverem.

3. Garantir que a descrição dos módulos reflita Harness Engineering de forma coerente.

4. Não duplicar conteúdo longo do README.

Requisitos para docs/alignment/current-state.md:
1. Atualizar apenas se estiver desatualizado.

2. Registrar estado atual de forma factual.

3. Não prometer recursos futuros como implementados.

Requisitos para docs/alignment/roadmap.md e docs/roadmap/mission-backlog.md:
1. Atualizar apenas se houver necessidade clara.

2. Registrar que a identidade de Harness Engineering foi incorporada ao README.

3. Manter internacionalização como tarefa futura.

4. Não transformar esta missão em roadmap completo.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar funcionalidades novas.
- Não adicionar dependências.
- Não criar README.en.md.
- Não criar README.es.md.
- Não internacionalizar READMEs agora.
- Não implementar RAG.
- Não implementar embeddings.
- Não implementar pgvector.
- Não implementar Semantic Index.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- README.md apresenta o VAF como framework de Harness Engineering.
- README.md explica a camada operacional ao redor do modelo.
- README.md diferencia Prompt Engineering, Agent Framework e Harness Engineering.
- README.md lista módulos centrais de forma coerente com o estado atual.
- README.md não promete recursos futuros como implementados.
- READMEs de módulos críticos foram auditados.
- Incoerências encontradas foram corrigidas.
- docs/architecture/module-index.md foi atualizado se necessário.
- docs/alignment/current-state.md foi atualizado se necessário.
- docs/alignment/roadmap.md foi atualizado se necessário.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

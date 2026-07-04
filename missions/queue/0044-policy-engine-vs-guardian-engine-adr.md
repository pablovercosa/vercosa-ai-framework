Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/alignment/alignment-review-2026-07-03.md
- docs/alignment/sdd-lifecycle.md
- docs/architecture/module-index.md
- specs/framework/0005-guardian-engine.md
- specs/framework/0006-workflow-engine.md
- specs/framework/0008-agent-orchestrator.md
- specs/framework/0009-capabilities-skills-tools.md
- specs/framework/0010-provider-gateway.md
- specs/framework/0011-knowledge-hub.md
- specs/framework/0012-canonicalizer.md
- specs/framework/0013-persistence-layer.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/missions/

Assuma o papel de framework-architect.

Missão:
Criar uma ADR para resolver a fronteira arquitetural entre Policy Engine e Guardian Engine no Vercosa AI Framework.

Entregável obrigatório:
- knowledge/decisions/2026-07-04-policy-engine-vs-guardian-engine.md

Objetivo:
Tomar uma decisão arquitetural explícita sobre se Policy Engine e Guardian Engine serão:
1. o mesmo componente;
2. componentes separados;
3. camadas diferentes com responsabilidades complementares.

A ADR deve conter:
1. Título.
2. Status da decisão.
3. Contexto.
4. Problema.
5. Decisão.
6. Justificativa.
7. Responsabilidades do Policy Engine.
8. Responsabilidades do Guardian Engine.
9. Responsabilidades que NÃO pertencem ao Policy Engine.
10. Responsabilidades que NÃO pertencem ao Guardian Engine.
11. Relação com Model Selection Engine.
12. Relação com Context Router futuro.
13. Relação com Token Budget Manager futuro.
14. Relação com Knowledge Hub, Canonicalizer e Persistence.
15. Relação com Mission Runner, Workflow Engine, Task Queue e Agent Orchestrator.
16. Relação com Capabilities, Skills, Tools, Providers e MCPs.
17. Como decisões de política devem ser registradas.
18. Como bloqueios, warnings e approvals devem ser tratados.
19. Como evitar duplicação de lógica entre Policy, Guardian, Runtime, Tools e CLI.
20. Consequências positivas.
21. Consequências negativas.
22. Riscos.
23. Regras de implementação futura.
24. Checklist para a próxima missão.

Direção arquitetural esperada:
- Policy Engine deve ser a camada declarativa e composicional de políticas.
- Guardian Engine deve ser a camada de enforcement operacional, segurança e decisão executável.
- Guardian pode usar políticas, mas não deve virar depósito de toda regra do framework.
- Policy Engine não deve executar tools, providers, runtimes ou comandos.
- Guardian Engine não deve resolver sozinho estratégia de contexto, custo, memória, roteamento ou seleção de modelo sem consultar políticas.
- Decisões devem ser rastreáveis e persistíveis no futuro.
- A ADR deve preparar o terreno para Context Router + Token Budget Manager.

Regras:
- não implementar código;
- não alterar src/;
- não alterar testes;
- não alterar configs globais;
- não usar sudo;
- não criar novas features;
- não mover missões manualmente;
- se precisar registrar pendências, atualizar apenas docs/alignment/open-questions.md;
- se atualizar open-questions.md, explique exatamente o motivo.

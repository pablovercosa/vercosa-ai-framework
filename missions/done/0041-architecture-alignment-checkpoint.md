Leia obrigatoriamente:
- AGENTS.md
- README.md
- knowledge/vision.md
- knowledge/principles/framework-principles.md
- knowledge/architecture/core-architecture.md
- specs/framework/
- docs/
- src/vercosa_ai_framework/

Assuma o papel de framework-architect.

Missão:
Criar um checkpoint de alinhamento arquitetural do Vercosa AI Framework.

Entregáveis obrigatórios:
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/alignment/external-framework-positioning.md
- docs/alignment/sdd-lifecycle.md

Objetivo:
Documentar o estado atual do projeto antes de novas implementações.

O checkpoint deve cobrir:
- o que o framework é;
- o que o framework não é;
- módulos já existentes;
- responsabilidades de cada módulo;
- cadeia arquitetural atual;
- lacunas;
- próximos blocos recomendados;
- onde entram LangGraph, MetaGPT, AutoGen, OpenCode, Claude Code, Codex CLI e MCPs;
- diferença entre memória infinita, memória persistente, Knowledge Hub, Context Router e Semantic Index;
- ciclo SDD desejado: Spec → Plan → Tasks → Implement → Validate → Commit;
- riscos de continuar sem alinhamento;
- recomendações antes da próxima leva de implementação.

Regras:
- não implementar código;
- não alterar src/;
- não alterar configs globais;
- não usar sudo;
- não criar novas features;
- apenas documentação de alinhamento.

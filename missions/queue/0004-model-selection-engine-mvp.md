Leia obrigatoriamente:
- AGENTS.md
- specs/framework/0002-model-selection-engine.md
- knowledge/guardian-specs/token-efficiency.md
- knowledge/guardian-specs/cost-optimization.md
- knowledge/guardian-specs/ai-quality-assurance.md

Assuma o papel de implementation-architect.

Missão:
Implementar o MVP do Model Selection Engine.

Entregáveis esperados:
- src/vercosa_ai_framework/model_selection/__init__.py
- src/vercosa_ai_framework/model_selection/types.py
- src/vercosa_ai_framework/model_selection/policy.py
- src/vercosa_ai_framework/model_selection/selector.py
- tests/test_model_selection.py

Requisitos:
- Não chamar APIs externas.
- Não depender de OpenCode diretamente.
- Usar estruturas puras em Python.
- Permitir catálogo de modelos em memória.
- Permitir política com:
  - task_role
  - complexity
  - quality
  - cost_profile
  - reasoning
  - memory
  - allow_paid
  - prefer_local
- Selecionar modelo principal e modelo pequeno.
- Implementar fallback simples.
- Manter código testável.

Critérios de aceite:
- pytest deve passar.
- python -m compileall src deve passar.

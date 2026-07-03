Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/alignment/
- specs/framework/
- src/vercosa_ai_framework/

Assuma o papel de documentation-architect.

Missão:
Criar e aplicar o padrão oficial de README.md do Vercosa AI Framework.

Entregáveis obrigatórios:
- docs/documentation/readme-standard.md
- docs/templates/readme-template.md
- docs/architecture/module-index.md
- atualizar README.md principal
- atualizar AGENTS.md com regras de documentação
- criar README.md nos principais módulos de src/vercosa_ai_framework/

Módulos que devem receber README.md:
- src/vercosa_ai_framework/agents/
- src/vercosa_ai_framework/canonicalizer/
- src/vercosa_ai_framework/capabilities/
- src/vercosa_ai_framework/core/
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/missions/
- src/vercosa_ai_framework/model_selection/
- src/vercosa_ai_framework/persistence/
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/skills/
- src/vercosa_ai_framework/tasks/
- src/vercosa_ai_framework/tools/
- src/vercosa_ai_framework/workflows/

Cada README.md deve ser explícito e conter:
- nome do módulo;
- objetivo;
- o que este módulo faz;
- o que este módulo não faz;
- principais arquivos;
- principais tipos/classes/funções;
- entradas e saídas;
- dependências internas;
- módulos relacionados;
- links para specs correspondentes;
- links para docs relacionadas;
- exemplos mínimos de uso quando fizer sentido;
- status atual: spec, contracts, MVP, experimental ou stable;
- próximos passos.

Regras de relacionamento:
- todo README de módulo deve linkar para o README principal;
- todo README de módulo deve linkar para a spec relacionada;
- todo README de módulo deve linkar para módulos imediatamente acima e abaixo na arquitetura;
- docs/architecture/module-index.md deve funcionar como mapa navegável do framework;
- links relativos devem ser usados;
- não criar documentação genérica;
- não exagerar em marketing;
- priorizar clareza técnica.

Regras:
- não implementar código;
- não alterar lógica de src/;
- não alterar configs globais;
- não usar sudo;
- não apagar docs existentes;
- se encontrar inconsistências arquiteturais, registrar em docs/alignment/open-questions.md.

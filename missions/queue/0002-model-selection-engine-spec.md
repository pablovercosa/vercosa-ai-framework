Leia obrigatoriamente:
- AGENTS.md
- knowledge/vision.md
- knowledge/principles/framework-principles.md
- knowledge/architecture/core-architecture.md
- knowledge/guardian-specs/security-by-design.md
- knowledge/guardian-specs/token-efficiency.md
- knowledge/guardian-specs/ai-quality-assurance.md
- knowledge/guardian-specs/cost-optimization.md
- specs/framework/0001-framework-foundation.md

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Model Selection Engine do Vercosa AI Framework.

Entregável obrigatório:
- specs/framework/0002-model-selection-engine.md

A Spec deve cobrir:
- provider agnostic;
- fallback entre modelos;
- custo;
- qualidade;
- modelos gratuitos;
- modelos pagos;
- small_model;
- cabeçalho YAML por arquivo;
- perfis economy/balanced/premium;
- política definida pela Spec;
- estratégia definida pelo framework;
- modelos apenas executam;
- integração inicial com OpenCode;
- OpenCode como runtime inicial, mas não núcleo;
- Guardian Specs;
- Security by Design;
- Token Efficiency;
- Cost Optimization;
- AI Quality Assurance.

Regras:
- não implementar código nesta missão;
- não alterar configurações globais;
- não reativar plugins;
- não usar sudo;
- se faltar decisão, registrar em seção "Pendências".

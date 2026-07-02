Leia obrigatoriamente:
- AGENTS.md
- knowledge/guardian-specs/security-by-design.md
- knowledge/guardian-specs/token-efficiency.md
- knowledge/guardian-specs/ai-quality-assurance.md
- knowledge/guardian-specs/cost-optimization.md
- specs/framework/0001-framework-foundation.md
- specs/framework/0004-mission-runner.md

Assuma o papel de framework-architect.

Missão:
Criar a Spec do Guardian Engine.

Entregável obrigatório:
- specs/framework/0005-guardian-engine.md

A Spec deve cobrir:
- validação de missões antes da execução;
- Security by Design;
- Token Efficiency;
- Cost Optimization;
- AI Quality Assurance;
- comandos proibidos;
- comandos que exigem confirmação;
- detecção de segredos;
- limite de custo/tokens;
- limite de ciclos;
- risco por missão;
- policy decision: allow, warn, block, require_approval;
- integração com Mission Runner;
- integração futura com Runtime Adapter;
- logs de decisão;
- explicabilidade da decisão;
- modo permissivo, padrão e estrito.

Regras:
- não implementar código;
- não alterar configs globais;
- não usar sudo.

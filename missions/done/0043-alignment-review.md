Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/alignment/external-framework-positioning.md
- docs/alignment/sdd-lifecycle.md
- docs/architecture/module-index.md
- docs/documentation/readme-standard.md
- specs/framework/

Assuma o papel de framework-architect e technical-reviewer.

Missão:
Fazer uma revisão curta, objetiva e crítica do alinhamento arquitetural atual do Vercosa AI Framework.

Objetivo:
Verificar se a documentação recém-criada está coerente com o estado real do projeto e gerar recomendações antes da próxima implementação.

Entregáveis obrigatórios:
- docs/alignment/alignment-review-2026-07-03.md

O arquivo deve conter:
1. Resumo executivo.
2. Veredito: o projeto está coerente ou não?
3. Pontos fortes do estado atual.
4. Inconsistências encontradas, se houver.
5. Lacunas críticas.
6. Lacunas importantes, mas não bloqueantes.
7. Próxima implementação recomendada.
8. Justificativa para a próxima implementação.
9. O que NÃO deve ser implementado ainda.
10. Riscos se o projeto continuar sem resolver as lacunas.
11. Checklist objetivo para avançar.

Critérios de revisão:
- verificar se o projeto está corretamente posicionado como framework próprio de AI Specification-Driven Engineering;
- verificar se OpenCode, Claude Code, Codex CLI, LangGraph, AutoGen, MetaGPT, ECC e MCPs estão posicionados como adapters, integrações ou referências, e não como núcleo;
- verificar se a cadeia Mission → Workflow → Task → Agent → Capability → Skill → Tool → Provider continua clara;
- verificar se a memória está sendo tratada como Knowledge Hub + Canonicalizer + Persistence + futuro Context Router, e não como "memória infinita";
- verificar se token efficiency está representado como princípio e precisa virar Context Router / Token Budget Manager;
- verificar se SDD está suficientemente definido como Spec → Plan → Tasks → Implement → Validate → Commit;
- verificar se os READMEs criados seguem o padrão de documentação navegável;
- verificar se a próxima etapa deveria ser Context Router / Memory Manager ou se existe bloqueio anterior.

Regras:
- não implementar código;
- não alterar src/;
- não criar novas features;
- não alterar testes;
- não alterar configs globais;
- não usar sudo;
- não editar arquivos fora de docs/alignment/, salvo se for absolutamente necessário registrar uma inconsistência;
- se sugerir mudanças futuras, registrar apenas como recomendação.

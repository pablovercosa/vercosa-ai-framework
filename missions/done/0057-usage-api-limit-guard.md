Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- src/vercosa_ai_framework/guardian/
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/providers/
- src/vercosa_ai_framework/providers/README.md
- src/vercosa_ai_framework/runtime/
- src/vercosa_ai_framework/runtime/README.md
- scripts/vaf-run-one-mission.sh
- scripts/vaf-worker.sh
- scripts/vaf-run-next-safe.sh
- tests/test_worker_scripts.py

Assuma o papel de python-implementation-agent, shell-maintenance-agent, reliability-engineer e framework-architect.

Missão:
Criar Usage/API Limit Guard inicial.

Objetivo:
Criar uma proteção determinística para identificar sinais de limite de uso, quota, rate limit ou crédito insuficiente em logs/erros de providers/runtimes, classificando esse tipo de falha como limitação externa temporária e orientando o sistema a parar com segurança em vez de repetir tentativas inúteis.

Contexto:
- O projeto já enfrentou erro de limite de uso da API durante missões anteriores.
- Esse tipo de erro não deve ser tratado como bug de implementação do framework.
- O worker não deve entrar em loop de retry quando a causa for quota/rate limit.
- Nesta missão, criar apenas contratos e detecção inicial determinística.
- Não integrar com billing real.
- Não chamar API externa.
- Não consultar OpenAI, Gemini ou qualquer provider.

Entregáveis obrigatórios:
- criar ou atualizar módulo adequado para Usage/API Limit Guard;
- preferir um local coerente com a arquitetura existente, como guardian, providers, runtime ou um novo módulo pequeno se for claramente justificado;
- criar testes para detecção de erros de limite;
- atualizar documentação relacionada;
- atualizar README.md se necessário;
- atualizar docs/architecture/module-index.md se novo módulo for criado.

Requisitos funcionais:
1. Inspecionar módulos existentes antes de decidir onde implementar.
2. Criar tipos/contratos simples para representar:
   - tipo de limite;
   - severidade;
   - origem/provider/runtime;
   - mensagem original;
   - ação recomendada;
   - se deve parar o worker;
   - se pode tentar novamente futuramente.
3. Detectar padrões textuais comuns de limite, como:
   - rate limit;
   - quota exceeded;
   - usage limit;
   - usage limit has been reached;
   - insufficient quota;
   - billing hard limit;
   - too many requests;
   - requests per minute;
   - tokens per minute;
   - daily limit;
   - 429.
4. A detecção deve ser determinística e testável.
5. A detecção deve ser case-insensitive.
6. A detecção deve preservar a mensagem original.
7. A detecção deve classificar quando o erro parece ser:
   - rate_limit;
   - quota_exceeded;
   - billing_limit;
   - unknown_usage_limit;
   - not_usage_limit.
8. Criar recomendação operacional simples, por exemplo:
   - stop_worker;
   - retry_later;
   - inspect_provider_limits;
   - manual_review.
9. Não chamar rede.
10. Não chamar LLM.
11. Não chamar provider externo.
12. Não alterar comportamento do worker de forma agressiva nesta missão, salvo se for uma integração pequena e segura.
13. Se integrar com scripts, fazê-lo apenas para mensagem/diagnóstico ou parada segura muito simples.
14. Não mascarar erros não relacionados a limite.

Requisitos de testes:
Criar testes cobrindo:
- mensagem com "usage limit has been reached";
- mensagem com "rate limit";
- mensagem com "quota exceeded";
- mensagem com "insufficient quota";
- mensagem com "429";
- mensagem sem limite de uso;
- detecção case-insensitive;
- preservação da mensagem original;
- ação recomendada stop_worker/retry_later/manual_review conforme regra implementada;
- comportamento determinístico;
- ausência de chamada externa.

Requisitos de documentação:
- tudo em português do Brasil;
- explicar que o guard é determinístico;
- explicar que ele não consulta billing real;
- explicar que ele não chama provider externo;
- explicar que ele serve para classificar sinais de limite/quota/rate limit;
- explicar que limitações externas não devem ser confundidas com bug do framework;
- explicar próximos passos;
- manter links relativos corretos;
- não prometer comportamento ainda não implementado.

Regra de commit automático:
Se esta missão gerar commit automático, a mensagem deve estar em português do Brasil.
Usar a mensagem fornecida por VAF_COMMIT_MESSAGE quando existir.

Restrições:
- não adicionar dependências;
- não implementar billing real;
- não chamar OpenAI;
- não chamar Gemini;
- não chamar Ollama;
- não chamar Claude;
- não chamar OpenCode diretamente;
- não acessar MCPs;
- não acessar rede;
- não usar sudo;
- não alterar configs globais;
- não reescrever histórico Git;
- não fazer force push;
- documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- testes novos existem e passam;
- pytest passa;
- python3 -m compileall src passa;
- documentação relacionada é atualizada;
- se novo módulo for criado, README e module-index devem ser atualizados;
- auto-commit usa mensagem em português do Brasil.

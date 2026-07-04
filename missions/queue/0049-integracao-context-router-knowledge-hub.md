Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
- docs/context-router-token-budget.md
- specs/framework/0011-knowledge-hub.md
- specs/framework/0014-context-router-token-budget-memory.md
- knowledge/decisions/2026-07-04-context-router-token-budget-memory-architecture.md
- src/vercosa_ai_framework/context/
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/knowledge/
- src/vercosa_ai_framework/knowledge/README.md
- tests/test_context_contracts.py
- tests/test_context_router_mvp.py

Assuma o papel de python-implementation-agent e framework-architect.

Missão:
Integrar o Context Router MVP com o Knowledge Hub de forma determinística e segura.

Objetivo:
Criar uma integração inicial entre Knowledge Hub e Context Router, permitindo converter registros/documentos candidatos do Knowledge Hub em ContextItem para montagem de ContextPackage.

Esta missão NÃO deve implementar RAG semântico, embeddings, pgvector, busca vetorial, banco de dados ou chamadas externas.

Entregáveis obrigatórios:
- atualizar src/vercosa_ai_framework/context/ se necessário;
- atualizar src/vercosa_ai_framework/knowledge/ se necessário;
- criar um adaptador/mapeador determinístico entre Knowledge Hub e Context Router, no local mais coerente com a arquitetura existente;
- criar tests/test_context_knowledge_integration.py;
- atualizar docs/context-router-token-budget.md;
- atualizar src/vercosa_ai_framework/context/README.md;
- atualizar src/vercosa_ai_framework/knowledge/README.md;
- atualizar docs/architecture/module-index.md se necessário.

Requisitos funcionais:
1. Inspecionar os tipos e contratos existentes do módulo knowledge antes de implementar.
2. Não presumir nomes inexistentes; adaptar-se aos tipos já existentes no projeto.
3. Criar uma forma simples, explícita e determinística de transformar registros/conteúdos do Knowledge Hub em candidatos ContextItem.
4. Preservar metadados úteis como:
   - id;
   - título;
   - caminho ou referência;
   - tipo de fonte;
   - hash, quando existir;
   - citações ou referências, quando existirem.
5. Quando o registro de conhecimento não possuir citação formal, criar referência rastreável mínima quando isso for compatível com os tipos existentes.
6. Permitir que o Context Router receba candidatos vindos do Knowledge Hub e produza ContextPackage normalmente.
7. Manter deduplicação, orçamento de tokens, omission reasons e citations funcionando.
8. Não acessar filesystem diretamente salvo se o módulo knowledge já tiver contrato interno seguro para isso.
9. Não acessar banco.
10. Não chamar provider externo.
11. Não chamar LLM.
12. Não fazer embeddings.
13. Não fazer busca semântica.
14. Não implementar pgvector.
15. Manter tudo determinístico e testável.

Requisitos de testes:
Criar testes cobrindo:
- conversão de registro/conteúdo do Knowledge Hub para ContextItem;
- preservação de origem/referência;
- preservação de título ou identificador;
- uso do item convertido pelo Context Router;
- deduplicação quando dois registros apontam para o mesmo conteúdo/hash;
- omissão por orçamento quando candidatos vindos do Knowledge Hub excedem limite;
- preservação de citations ou referências rastreáveis;
- comportamento determinístico;
- ausência de chamadas externas.

Requisitos de documentação:
- documentação em português do Brasil;
- explicar que a integração é determinística;
- explicar que o Knowledge Hub fornece candidatos, não memória infinita;
- explicar que o Context Router monta o pacote de contexto, não faz busca semântica;
- deixar explícito que embeddings, pgvector e RAG semântico são etapas futuras;
- atualizar limites conhecidos;
- atualizar próximos passos;
- manter links relativos corretos.

Restrições:
- não adicionar dependências;
- não implementar Semantic Index;
- não implementar embeddings;
- não implementar pgvector;
- não implementar PostgreSQL;
- não implementar RAG semântico;
- não chamar Gemini, OpenAI, Ollama, Claude, OpenCode ou qualquer runtime;
- não executar providers externos;
- não acessar MCPs;
- não usar sudo;
- não alterar configs globais;
- não reescrever histórico Git;
- não fazer force push;
- não alterar APIs públicas sem necessidade;
- não prometer comportamento ainda não implementado;
- manter storage agnostic, provider agnostic, runtime agnostic e model agnostic;
- documentação e textos explicativos devem estar em português do Brasil.

Critérios de aceite:
- pytest deve passar;
- python3 -m compileall src deve passar;
- documentação relacionada deve estar atualizada;
- git status deve mostrar apenas arquivos relacionados à missão antes do commit manual;
- não deve haver dependência externa nova;
- não deve haver chamada de rede.

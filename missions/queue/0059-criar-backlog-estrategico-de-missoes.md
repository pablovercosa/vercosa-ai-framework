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
- docs/alignment/open-questions.md
- docs/alignment/sdd-lifecycle.md
- docs/operations/safe-runner-usage.md
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- src/vercosa_ai_framework/context/README.md
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/model_selection/README.md
- src/vercosa_ai_framework/providers/README.md
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/knowledge/README.md

Assuma o papel de:
- framework-architect;
- documentation-agent;
- roadmap-planner;
- reliability-engineer.

Missão:
Criar backlog estratégico detalhado de missões futuras.

Objetivo:
Criar um documento canônico de backlog estratégico para o Vercosa AI Framework, organizando as próximas missões por fases, dependências, riscos, pré-requisitos e critérios de avanço, sem colocar todas as missões diretamente em `missions/queue`.

Contexto:
- O projeto já possui runner seguro para uma missão por vez.
- O projeto já possui runner seguro em batch.
- O usuário quer testar execução em batch com 3 missões.
- Se o teste com 3 missões passar, o projeto passará a usar batch de 10 missões.
- O batch não deve eliminar governança, revisão, rastreabilidade nem referências.
- Não é seguro criar dezenas de missões executáveis diretamente em `missions/queue`, porque missões futuras podem depender de decisões, código e documentação produzidos por missões anteriores.
- O backlog estratégico deve ser um mapa vivo, não uma fila cega de execução.
- A fila executável deve continuar recebendo blocos pequenos e revisáveis.

Estado arquitetural atual conhecido:
- Mission Runner existe.
- Runner seguro de uma missão existe.
- Runner seguro em batch existe.
- Context Router existe e já possui MVP determinístico.
- Token Budget Manager existe e já possui MVP determinístico.
- Knowledge Hub já se integra ao Context Router.
- Guardian Engine já avalia ContextPackage.
- Policy Engine já possui contratos iniciais.
- Policy Engine já se integra ao Guardian Engine.
- Policy Engine já se integra ao Context Router.
- Usage/API Limit Guard inicial existe.
- Ainda faltam integrações com Model Selection, Provider Gateway, auditoria/event log, CLI mais amigável, exemplos reais, documentação pública e release alfa.

Entregáveis obrigatórios:
1. Criar o arquivo:
   - docs/roadmap/mission-backlog.md

2. Atualizar, se necessário:
   - docs/alignment/roadmap.md
   - README.md

3. Não criar novos arquivos em `missions/queue` além desta missão em execução.

4. Não alterar código Python.

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos do documento `docs/roadmap/mission-backlog.md`:

1. O documento deve estar em português do Brasil.

2. O documento deve explicar claramente a diferença entre:
   - backlog estratégico;
   - fila executável;
   - missão em execução;
   - missão concluída;
   - batch operacional.

3. O documento deve registrar que o backlog estratégico não deve ser executado automaticamente.

4. O documento deve recomendar que `missions/queue` receba somente blocos pequenos e revisáveis.

5. O documento deve explicar o novo modelo operacional:
   - primeiro testar batch de 3 missões;
   - se passar, liberar batch de 10 missões;
   - parar sempre na primeira falha;
   - testar após cada missão;
   - manter commit separado por missão;
   - preferir push manual após revisão.

6. O documento deve organizar o backlog por fases, no mínimo:
   - Fase 1 — Consolidação operacional;
   - Fase 2 — Integrações centrais;
   - Fase 3 — Observabilidade e auditoria;
   - Fase 4 — Experiência de uso;
   - Fase 5 — Exemplos reais e documentação pública;
   - Fase 6 — Preparação de alfa/release;
   - Fase 7 — Capacidades avançadas futuras.

7. Para cada fase, incluir:
   - objetivo da fase;
   - por que a fase existe;
   - riscos se a fase for pulada;
   - missões prováveis;
   - dependências;
   - critérios para avançar para a próxima fase.

8. Incluir uma lista numerada de missões futuras prováveis, começando após a missão atual.

9. Cada missão futura listada deve conter:
   - código sugerido da missão;
   - título;
   - objetivo;
   - escopo permitido;
   - escopo proibido;
   - dependências;
   - critérios de aceite resumidos.

10. Incluir no backlog pelo menos estas missões futuras prováveis:
   - documentar playbook de execução em batch;
   - criar checklist de validação pós-batch;
   - testar batch de 3 missões;
   - liberar uso de batch de 10;
   - integrar Policy Engine com Model Selection;
   - integrar Token Budget Manager com Model Selection;
   - integrar Usage/API Limit Guard ao fluxo operacional do worker;
   - criar Audit/Event Log inicial;
   - registrar decisões de Guardian/Policy/Context em eventos auditáveis;
   - criar CLI operacional mais amigável;
   - criar exemplos reais de uso;
   - criar documentação pública inicial;
   - criar guia de instalação;
   - criar guia de contribuição;
   - criar licença se ainda não existir;
   - criar release/tag alfa;
   - revisar arquitetura pós-integrações;
   - avaliar Semantic Index;
   - avaliar embeddings;
   - avaliar pgvector;
   - avaliar RAG semântico;
   - avaliar Gemini/Gemini CLI/Gemini MCP Bridge como provider auxiliar futuro;
   - internacionalizar READMEs no final.

11. O documento deve deixar claro que recursos avançados como embeddings, pgvector, Semantic Index e RAG semântico são futuros e não fazem parte do MVP operacional imediato.

12. O documento deve deixar claro que Gemini/Gemini CLI/Gemini MCP Bridge é apenas uma avaliação futura, não dependência atual.

13. O documento deve registrar que internacionalização dos READMEs fica para fase final:
   - README.md em pt-BR;
   - README.en.md em inglês;
   - README.es.md em espanhol.

14. O documento deve conter uma seção “Como transformar backlog em fila executável”, explicando:
   - escolher um bloco pequeno;
   - revisar dependências;
   - gerar arquivos `.md` individuais em `missions/queue`;
   - evitar criar missões que dependem de decisões ainda não tomadas;
   - rodar batch somente após revisão.

15. O documento deve conter uma seção “Quando NÃO usar batch de 10”, incluindo:
   - quando houver mudanças estruturais grandes;
   - quando houver alteração em scripts críticos;
   - quando houver mudança de arquitetura;
   - quando houver falha recente;
   - quando houver dúvidas sobre dependências;
   - quando houver risco de acoplamento indevido.

16. O documento deve conter uma seção “Quando batch de 10 é aceitável”, incluindo:
   - missões pequenas ou médias;
   - escopo bem conhecido;
   - dependências claras;
   - testes estáveis;
   - runner seguro funcionando;
   - nenhuma falha recente;
   - documentação e critérios de aceite claros.

17. O documento deve conter uma seção “Riscos de backlog grande”, explicando:
   - desatualização;
   - pressupostos quebrados;
   - perda de contexto;
   - execução cega;
   - missões duplicadas;
   - acoplamento indevido;
   - documentação prometendo o que não existe.

18. O documento deve conter uma seção “Regra de ouro”, com a ideia:
   - backlog pode ser grande;
   - fila deve ser pequena;
   - batch deve ser seguro;
   - revisão continua obrigatória.

Requisitos para atualização de `docs/alignment/roadmap.md`:
1. Atualizar apenas se fizer sentido.
2. Se atualizar, adicionar link relativo para:
   - docs/roadmap/mission-backlog.md
3. Não duplicar todo o conteúdo do backlog dentro do roadmap.
4. Manter o roadmap como visão macro.
5. Manter o backlog como visão operacional detalhada.

Requisitos para atualização de `README.md`:
1. Atualizar apenas se houver uma seção adequada de roadmap/operação.
2. Se atualizar, adicionar link discreto para o backlog.
3. Não transformar README em documento operacional longo.
4. Não prometer recursos futuros como se já estivessem implementados.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não criar runner novo.
- Não modificar runner existente.
- Não criar novas missões executáveis além desta missão.
- Não implementar funcionalidades.
- Não adicionar dependências.
- Não acessar rede.
- Não chamar provider externo.
- Não chamar LLM externo.
- Não acessar banco.
- Não implementar RAG.
- Não implementar embeddings.
- Não implementar pgvector.
- Não implementar Semantic Index.
- Não implementar Gemini.
- Não alterar configs globais.
- Não usar sudo.
- Não reescrever histórico Git.
- Não fazer force push.
- Não fazer push automático.
- Não usar `git add .`.
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- `docs/roadmap/mission-backlog.md` existe.
- O backlog está organizado por fases.
- O backlog diferencia claramente backlog estratégico de fila executável.
- O backlog documenta a transição planejada de batch de 3 para batch de 10.
- O backlog lista missões futuras com objetivo, escopo, dependências e critérios de aceite.
- O backlog não promete funcionalidades ainda não implementadas.
- `docs/alignment/roadmap.md` é atualizado somente se necessário.
- `README.md` é atualizado somente se necessário.
- Nenhum código Python é alterado.
- Nenhum script shell é alterado.
- Nenhuma dependência é adicionada.
- `pytest` passa.
- `python3 -m compileall src` passa.
- O commit automático usa mensagem em português do Brasil.

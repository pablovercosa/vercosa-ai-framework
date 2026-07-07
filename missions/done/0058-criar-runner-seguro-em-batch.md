Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/operations/safe-runner-usage.md
- docs/architecture/module-index.md
- scripts/vaf-run-one-mission.sh
- scripts/vaf-worker.sh
- scripts/vaf-run-next-safe.sh
- scripts/vaf-status.sh
- tests/test_worker_scripts.py

Assuma o papel de shell-maintenance-agent, reliability-engineer, test-engineer e framework-architect.

Missão:
Criar runner seguro em batch.

Objetivo:
Criar um script seguro para executar múltiplas missões em sequência controlada, com parada automática na primeira falha, validação após cada missão e sem push automático por padrão.

Contexto:
- O script scripts/vaf-run-next-safe.sh executa uma missão por vez.
- O projeto quer testar execução em batch inicialmente com 3 missões.
- Se o teste com 3 missões passar, o fluxo operacional futuro poderá usar batch de 10 missões.
- O batch não pode transformar o projeto em execução cega.
- O batch deve preservar commits separados por missão.
- O batch deve parar imediatamente se qualquer validação falhar.

Entregáveis obrigatórios:
- criar scripts/vaf-run-batch-safe.sh;
- tornar o script executável;
- criar ou atualizar testes em tests/test_worker_scripts.py ou arquivo de teste específico;
- atualizar docs/operations/safe-runner-usage.md;
- atualizar README.md se necessário.

Requisitos funcionais:
1. Criar script scripts/vaf-run-batch-safe.sh.
2. O script deve executar múltiplas missões usando o fluxo seguro existente.
3. O número padrão de missões deve ser 3.
4. Permitir configurar o tamanho do batch por variável:
   - VAF_BATCH_SIZE=3
   - VAF_BATCH_SIZE=10
5. O script deve recusar batch size menor que 1.
6. O script deve recusar batch size muito alto; usar limite máximo seguro inicial de 10.
7. O script deve parar se não houver missão na fila.
8. O script deve parar na primeira falha.
9. O script deve rodar validações após cada missão, diretamente ou por reaproveitamento do runner seguro existente.
10. O script deve garantir que pytest passe.
11. O script deve garantir que python3 -m compileall src passe.
12. O script deve garantir que o Git esteja limpo após cada missão.
13. O script deve garantir que failed permaneça 0.
14. O script não deve fazer push por padrão.
15. Permitir push automático somente com VAF_AUTO_PUSH=1.
16. Mesmo com VAF_AUTO_PUSH=1, o push deve ocorrer apenas ao final do batch e somente se todas as missões passarem.
17. O script deve mostrar resumo final com:
   - missões solicitadas;
   - missões executadas;
   - último commit;
   - status de queue/running/done/failed;
   - resultado de testes;
   - resultado de compileall;
   - se houve push ou não.
18. O script deve respeitar VAF_COMMIT_MESSAGE quando aplicável, mas precisa considerar que um batch tem múltiplas missões. Se VAF_COMMIT_MESSAGE único for inadequado, documentar o limite ou não usar mensagem única no batch.
19. Não alterar scripts existentes de forma arriscada.
20. Não reescrever histórico Git.
21. Não fazer force push.
22. Não usar sudo.
23. Não acessar rede, exceto git push quando VAF_AUTO_PUSH=1.

Requisitos de testes:
Criar testes cobrindo:
- arquivo scripts/vaf-run-batch-safe.sh existe;
- script é executável;
- script menciona VAF_BATCH_SIZE;
- script menciona limite máximo 10;
- script menciona VAF_AUTO_PUSH;
- script chama ou reaproveita scripts/vaf-run-next-safe.sh;
- script contém proteção para parar em falha;
- script contém validação de pytest;
- script contém validação de compileall;
- documentação do batch foi atualizada.

Requisitos de documentação:
- tudo em português do Brasil;
- explicar diferença entre runner de uma missão e runner em batch;
- explicar padrão VAF_BATCH_SIZE=3;
- explicar limite máximo VAF_BATCH_SIZE=10;
- explicar que batch de 10 só deve ser usado após teste bem-sucedido com 3;
- explicar que push automático é opt-in;
- explicar que o batch para na primeira falha;
- explicar que commits continuam separados por missão;
- explicar riscos de batch grande;
- manter links relativos corretos;
- não prometer comportamento ainda não implementado.

Regra de commit automático:
Se esta missão gerar commit automático, a mensagem deve estar em português do Brasil.
Usar a mensagem fornecida por VAF_COMMIT_MESSAGE quando existir.

Restrições:
- não adicionar dependências;
- não alterar arquitetura do framework;
- não executar missões futuras nesta missão;
- não criar backlog ainda;
- não usar sudo;
- não alterar configs globais;
- não reescrever histórico Git;
- não fazer force push;
- documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- scripts/vaf-run-batch-safe.sh existe;
- scripts/vaf-run-batch-safe.sh é executável;
- testes novos/atualizados passam;
- pytest passa;
- python3 -m compileall src passa;
- documentação do runner seguro em batch existe;
- auto-commit usa mensagem em português do Brasil.

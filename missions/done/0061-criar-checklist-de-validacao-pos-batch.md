Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/documentation/readme-standard.md
- docs/operations/safe-runner-usage.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- scripts/vaf-status.sh
- tests/test_worker_scripts.py
- missions/done/0058-criar-runner-seguro-em-batch.md
- missions/queue/0059-criar-backlog-estrategico-de-missoes.md
- missions/queue/0060-documentar-playbook-de-execucao-em-batch.md

Leia também, se existirem após execuções anteriores neste mesmo batch:
- docs/roadmap/mission-backlog.md
- docs/operations/batch-execution-playbook.md

Assuma o papel de:
- documentation-agent;
- reliability-engineer;
- operations-engineer;
- test-engineer.

Missão:
Criar checklist de validação pós-batch.

Objetivo:
Criar um checklist operacional detalhado para validar o estado do Vercosa AI Framework depois de uma execução em batch, antes de fazer push, antes de liberar batch de 10 ou antes de iniciar novo bloco de missões.

Contexto:
- O projeto já possui runner seguro de uma missão.
- O projeto já possui runner seguro em batch.
- O usuário decidiu testar primeiro batch com 3 missões.
- Se o batch com 3 missões passar, o projeto poderá usar batch de 10 missões.
- O batch acelera execução, mas aumenta risco de acumular erro se não houver validação clara.
- É necessário padronizar a checagem pós-batch.
- O checklist deve ser prático, copiável e direto para operação diária.
- O checklist deve complementar o playbook de batch.
- O checklist não deve substituir o runner seguro.
- O checklist não deve alterar código nem scripts.

Estado operacional atual conhecido:
- `scripts/vaf-run-batch-safe.sh` existe.
- `VAF_BATCH_SIZE` tem padrão 3.
- `VAF_BATCH_SIZE` possui limite máximo seguro inicial de 10.
- `VAF_AUTO_PUSH=1` é opt-in.
- O batch deve parar na primeira falha.
- Commits devem continuar separados por missão.
- `pytest` vinha passando.
- `python3 -m compileall src` vinha passando.
- `failed` vinha igual a 0.

Entregáveis obrigatórios:
1. Criar o arquivo:
   - docs/operations/post-batch-validation-checklist.md

2. Atualizar, se existir:
   - docs/operations/batch-execution-playbook.md

3. Atualizar:
   - docs/operations/safe-runner-usage.md

4. Atualizar, somente se fizer sentido:
   - README.md

5. Não alterar código Python.

6. Não alterar scripts shell.

7. Não adicionar dependências.

Requisitos do documento `docs/operations/post-batch-validation-checklist.md`:

1. O documento deve estar em português do Brasil.

2. O documento deve explicar seu propósito:
   - validar o estado após batch;
   - decidir se pode fazer push;
   - decidir se pode iniciar outro batch;
   - decidir se pode liberar batch de 10.

3. O documento deve deixar claro que ele deve ser usado:
   - depois de `./scripts/vaf-run-batch-safe.sh`;
   - depois de qualquer batch com `VAF_BATCH_SIZE=3`;
   - depois de qualquer batch com `VAF_BATCH_SIZE=10`;
   - antes de `git push`;
   - antes de iniciar novo bloco de missões.

4. O documento deve conter uma seção “Checklist rápido”.

5. O checklist rápido deve incluir, no mínimo:
   - worker parado;
   - `queue` no estado esperado;
   - `running=0`;
   - `failed=0`;
   - branch `main`;
   - Git limpo;
   - últimos commits coerentes;
   - testes passando;
   - compileall passando;
   - logs sem falha relevante;
   - documentação criada/atualizada conforme esperado;
   - nenhuma promessa de funcionalidade inexistente;
   - push ainda não feito, salvo se explicitamente solicitado.

6. O documento deve conter uma seção “Comandos de validação pós-batch”.

7. Essa seção deve incluir os comandos:

   ```bash
   cd /home/projetos/vercosa-ai-framework

   ./scripts/vaf-status.sh
   git status --short
   git log --oneline --decorate -12

   find missions -maxdepth 2 -type f | sort | tail -40
   ls -lt logs | head -12

   pytest
   python3 -m compileall src
   ```

8. O documento deve conter uma seção “Validação das missões executadas”.

9. Essa seção deve explicar como conferir:

   * se as missões saíram de `missions/queue`;
   * se foram para `missions/done`;
   * se nenhuma foi para `missions/failed`;
   * se não há missão presa em `missions/running`;
   * se os logs correspondem às missões executadas;
   * se cada missão gerou commit separado.

10. O documento deve conter uma seção “Validação do Git”.

11. Essa seção deve incluir:

* confirmar branch `main`;
* confirmar `git status --short` vazio;
* confirmar últimos commits;
* confirmar se `origin/main` ainda está atrás ou já atualizado;
* não usar force push;
* não reescrever histórico.

12. O documento deve conter uma seção “Validação de testes”.

13. Essa seção deve incluir:

* `pytest`;
* `python3 -m compileall src`;
* interpretar falha de teste como bloqueio para push;
* interpretar falha de compileall como bloqueio para push;
* não aceitar “passou parcialmente”.

14. O documento deve conter uma seção “Validação de documentação”.

15. Essa seção deve incluir:

* documentação em português do Brasil;
* links relativos funcionando, quando aplicável;
* README atualizado somente se necessário;
* module-index atualizado somente se necessário;
* docs operacionais apontando entre si;
* sem promessa de recurso futuro como implementado.

16. O documento deve conter uma seção “Quando fazer push”.

17. Essa seção deve permitir push somente quando:

* `failed=0`;
* `running=0`;
* worker parado;
* `git status --short` vazio;
* branch `main`;
* testes passam;
* compileall passa;
* últimos commits estão coerentes;
* não há dúvida sobre a entrega.

18. O documento deve conter uma seção “Quando NÃO fazer push”.

19. Essa seção deve bloquear push se:

* qualquer missão foi para `failed`;
* alguma missão ficou em `running`;
* Git está sujo;
* testes falharam;
* compileall falhou;
* branch não é `main`;
* logs mostram erro não explicado;
* documentação ficou incoerente;
* houve commit com mensagem errada;
* houve alteração fora do escopo;
* houve dúvida sobre resultado do batch.

20. O documento deve conter uma seção “Quando parar e investigar”.

21. Essa seção deve incluir:

* `failed > 0`;
* `running > 0` com worker parado;
* queue diferente do esperado;
* logs incompatíveis;
* commit faltando;
* commit com escopo errado;
* arquivo criado em local errado;
* teste quebrado;
* compileall quebrado;
* documentação prometendo o que não foi implementado.

22. O documento deve conter uma seção “Comandos de investigação”.

23. Essa seção deve incluir comandos para:

* listar logs recentes;
* abrir último log;
* listar missões failed;
* listar missões running;
* ver últimos commits;
* ver arquivos alterados no último commit.

Incluir comandos como:

```bash
ls -lt logs | head -20
tail -n 160 "$(ls -t logs/*.log | head -1)"
find missions/failed -maxdepth 1 -type f -print | sort
find missions/running -maxdepth 1 -type f -print | sort
git log --oneline --decorate -15
git show --stat --oneline HEAD
git show --name-only --oneline HEAD
```

24. O documento deve conter uma seção “Quando liberar batch de 10”.

25. Essa seção deve dizer que batch de 10 só deve ser liberado quando:

* batch de 3 passou;
* `failed=0`;
* testes passaram;
* compileall passou;
* Git ficou limpo;
* commits ficaram separados;
* documentação ficou coerente;
* não houve falha recente;
* não há missão de alto risco no próximo bloco.

26. O documento deve conter uma seção “Quando suspender batch de 10”.

27. Essa seção deve dizer para suspender batch de 10 quando:

* houve falha no batch anterior;
* haverá mudança estrutural profunda;
* haverá alteração em scripts críticos;
* haverá alteração no Guardian Engine com impacto amplo;
* haverá alteração no Policy Engine com impacto amplo;
* haverá alteração no Context Router com impacto amplo;
* haverá alteração em providers/runtimes;
* dependências entre missões estão incertas;
* critérios de aceite estão fracos;
* missões estão pequenas demais ou vagas demais;
* referências obrigatórias estão incompletas.

28. O documento deve conter uma seção “Resultado esperado de um batch saudável”.

29. Essa seção deve conter exemplo parecido com:

```text
queue:   0
running: 0
failed:  0
worker:  stopped
pytest:  passou
compileall: passou
git: limpo
commits: separados por missão
```

30. O documento deve conter uma seção “Regra final”.

31. Essa seção deve registrar:

* se houver dúvida, não fazer push;
* se houver falha, parar;
* se o batch de 3 falhar, não liberar batch de 10;
* se o batch de 3 passar, batch de 10 fica permitido, mas não obrigatório.

Requisitos para atualização de `docs/operations/batch-execution-playbook.md`:

1. Atualizar somente se o arquivo existir.
2. Adicionar link relativo para:

   * `post-batch-validation-checklist.md`
3. Não duplicar todo o checklist dentro do playbook.
4. Manter o playbook como guia de execução.
5. Manter o checklist como guia de validação.

Requisitos para atualização de `docs/operations/safe-runner-usage.md`:

1. Adicionar referência ao checklist pós-batch.
2. Adicionar link relativo para:

   * `post-batch-validation-checklist.md`
3. Não duplicar o checklist inteiro.
4. Manter documento em português do Brasil.

Requisitos para atualização de `README.md`:

1. Atualizar somente se houver seção operacional adequada.
2. Se atualizar, adicionar link curto para:

   * `docs/operations/post-batch-validation-checklist.md`
3. Não transformar README em manual longo.
4. Não prometer comportamento não implementado.

Restrições:

* Não alterar código Python.
* Não alterar scripts shell.
* Não criar runner novo.
* Não modificar runner existente.
* Não criar novas missões executáveis além desta missão.
* Não implementar funcionalidades.
* Não adicionar dependências.
* Não acessar rede.
* Não chamar provider externo.
* Não chamar LLM externo.
* Não acessar banco.
* Não implementar RAG.
* Não implementar embeddings.
* Não implementar pgvector.
* Não implementar Semantic Index.
* Não alterar configs globais.
* Não usar sudo.
* Não reescrever histórico Git.
* Não fazer force push.
* Não fazer push automático.
* Não usar `git add .`.
* Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:

* `docs/operations/post-batch-validation-checklist.md` existe.
* O checklist explica quando deve ser usado.
* O checklist contém comandos prontos de validação pós-batch.
* O checklist valida missões, Git, testes, compileall, logs e documentação.
* O checklist contém seção “Quando fazer push”.
* O checklist contém seção “Quando NÃO fazer push”.
* O checklist contém seção “Quando parar e investigar”.
* O checklist contém comandos de investigação.
* O checklist contém critérios para liberar batch de 10.
* O checklist contém critérios para suspender batch de 10.
* `docs/operations/batch-execution-playbook.md` aponta para o checklist se o playbook existir.
* `docs/operations/safe-runner-usage.md` aponta para o checklist.
* `README.md` é atualizado somente se necessário.
* Nenhum código Python é alterado.
* Nenhum script shell é alterado.
* Nenhuma dependência é adicionada.
* `pytest` passa.
* `python3 -m compileall src` passa.
* O commit automático usa mensagem em português do Brasil.


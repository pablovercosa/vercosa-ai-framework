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

Leia também, se existir após a execução da missão anterior neste mesmo batch:
- docs/roadmap/mission-backlog.md

Assuma o papel de:
- documentation-agent;
- reliability-engineer;
- operations-engineer;
- shell-maintenance-agent.

Missão:
Documentar playbook operacional de execução em batch.

Objetivo:
Criar um playbook operacional detalhado para uso seguro do runner em batch, explicando como preparar, executar, validar e publicar batches de missões no Vercosa AI Framework.

Contexto:
- O projeto já possui `scripts/vaf-run-next-safe.sh` para executar uma missão por vez.
- O projeto já possui `scripts/vaf-run-batch-safe.sh` para executar múltiplas missões em sequência.
- O padrão inicial do batch é `VAF_BATCH_SIZE=3`.
- O limite máximo seguro inicial é `VAF_BATCH_SIZE=10`.
- O usuário decidiu testar primeiro um batch com 3 missões.
- Se o batch com 3 missões passar, o projeto passará a aceitar batch de 10 missões.
- O batch não deve remover governança.
- O batch não deve substituir revisão.
- O batch não deve executar missões mal especificadas.
- O batch deve parar na primeira falha.
- O push automático deve continuar sendo opt-in.
- Commits devem continuar separados por missão.

Estado operacional atual conhecido:
- Runner seguro de uma missão existe.
- Runner seguro em batch existe.
- `pytest` vinha passando.
- `python3 -m compileall src` vinha passando.
- `failed` vinha igual a 0.
- A missão 0059, se executada antes desta no batch, deve criar `docs/roadmap/mission-backlog.md`.

Entregáveis obrigatórios:
1. Criar o arquivo:
   - docs/operations/batch-execution-playbook.md

2. Atualizar:
   - docs/operations/safe-runner-usage.md

3. Atualizar, somente se fizer sentido:
   - README.md
   - docs/alignment/roadmap.md

4. Não alterar código Python.

5. Não alterar scripts shell.

6. Não adicionar dependências.

Requisitos do documento `docs/operations/batch-execution-playbook.md`:

1. O documento deve estar em português do Brasil.

2. O documento deve explicar a diferença entre:
   - execução de uma missão;
   - execução em batch;
   - backlog estratégico;
   - fila executável;
   - push manual;
   - push automático opt-in.

3. O documento deve deixar claro que o runner em batch é operacional, não arquitetural.

4. O documento deve explicar que o batch usa missões já presentes em:
   - `missions/queue/`

5. O documento deve explicar que cada missão precisa continuar sendo um arquivo `.md` completo, revisável e com referências suficientes.

6. O documento deve explicar que o batch não deve ser usado para compensar missões mal escritas.

7. O documento deve documentar o comando padrão:

   ```bash
   ./scripts/vaf-run-batch-safe.sh
   ```

8. O documento deve documentar o batch de 3:

   ```bash
   VAF_BATCH_SIZE=3 ./scripts/vaf-run-batch-safe.sh
   ```

9. O documento deve documentar o batch de 10:

   ```bash
   VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh
   ```

10. O documento deve explicar que batch de 10 só deve ser usado depois de um teste bem-sucedido com batch de 3.

11. O documento deve documentar que `VAF_BATCH_SIZE`:

    * tem padrão 3;
    * aceita valores entre 1 e 10;
    * deve ser recusado se for menor que 1;
    * deve ser recusado se for maior que 10;
    * não deve ser aumentado sem nova decisão explícita.

12. O documento deve documentar que `VAF_AUTO_PUSH=1`:

    * é opcional;
    * não é o padrão;
    * só deve publicar ao final do batch;
    * só deve publicar se todas as missões passarem;
    * deve ser evitado nos primeiros testes;
    * deve ser usado apenas quando o fluxo estiver estável.

13. O documento deve explicar por que não é recomendável usar um único `VAF_COMMIT_MESSAGE` em batch:

    * pode gerar commits com mensagem genérica;
    * pode reduzir rastreabilidade;
    * pode confundir histórico;
    * cada missão deve ter commit claro e separado.

14. O documento deve incluir seção “Pré-requisitos antes do batch”, com comandos:

    ```bash
    cd /home/projetos/vercosa-ai-framework
    ./scripts/vaf-status.sh
    git status --short
    git log --oneline --decorate -8
    pytest
    python3 -m compileall src
    ```

15. O documento deve incluir seção “Como preparar um batch”, explicando:

    * criar missões uma por uma;
    * revisar cada Markdown;
    * garantir referências adequadas;
    * garantir escopo claro;
    * garantir critérios de aceite;
    * commitar as missões na fila;
    * só então executar o batch.

16. O documento deve incluir seção “Como executar batch de teste com 3 missões”.

17. O documento deve incluir seção “Como executar batch operacional com 10 missões”.

18. O documento deve incluir seção “Validações durante o batch”, explicando:

    * parar na primeira falha;
    * preservar logs;
    * preservar commits;
    * não continuar se `failed > 0`;
    * não continuar se Git ficar sujo;
    * não continuar se testes falharem;
    * não continuar se compileall falhar.

19. O documento deve incluir seção “Validações pós-batch”, com comandos:

    ```bash
    ./scripts/vaf-status.sh
    git status --short
    git log --oneline --decorate -12
    find missions -maxdepth 2 -type f | sort | tail -40
    ls -lt logs | head -12
    pytest
    python3 -m compileall src
    ```

20. O documento deve incluir seção “Quando fazer push”.

21. O documento deve incluir seção “Quando NÃO fazer push”, incluindo:

    * se `failed > 0`;
    * se `git status --short` mostrar alterações;
    * se testes falharem;
    * se compileall falhar;
    * se houver missão em `running`;
    * se a branch não for `main`;
    * se houver dúvida sobre a entrega;
    * se a documentação prometer algo não implementado.

22. O documento deve incluir seção “Como investigar falhas”, com comandos para:

    * listar últimos logs;
    * abrir último log;
    * verificar missões em failed;
    * verificar Git;
    * verificar último commit.

23. O documento deve incluir seção “Política de batch de 3 para batch de 10”, registrando:

    * batch de 3 é obrigatório como teste inicial;
    * batch de 10 só é aceito se batch de 3 passar;
    * batch de 10 deve ser suspenso se houver falha recente;
    * batch de 10 deve ser evitado em alterações arquiteturais sensíveis;
    * batch de 10 é mais adequado para missões pequenas/médias com dependências claras.

24. O documento deve incluir seção “Tipos de missão adequadas para batch”, incluindo:

    * documentação;
    * testes;
    * integração pequena;
    * refatoração localizada;
    * atualização de índices;
    * exemplos;
    * playbooks;
    * contratos simples.

25. O documento deve incluir seção “Tipos de missão inadequadas para batch de 10”, incluindo:

    * mudança arquitetural profunda;
    * alteração em scripts críticos;
    * mudança de fluxo Git;
    * mudança no Guardian Engine com impacto amplo;
    * mudança no Policy Engine com impacto amplo;
    * mudança no Context Router com impacto amplo;
    * mudança em providers/runtimes;
    * alteração que pode afetar segurança;
    * qualquer missão com dependências incertas.

26. O documento deve incluir seção “Regra operacional principal”, com a ideia:

    * batch acelera execução;
    * batch não elimina revisão;
    * batch não substitui especificação;
    * batch não deve ser cego;
    * batch deve parar cedo e preservar rastreabilidade.

Requisitos para atualização de `docs/operations/safe-runner-usage.md`:

1. Adicionar link relativo para:

   * `batch-execution-playbook.md`

2. Explicar brevemente que:

   * `vaf-run-next-safe.sh` executa uma missão;
   * `vaf-run-batch-safe.sh` executa múltiplas missões;
   * o playbook detalha o uso seguro do batch.

3. Não duplicar todo o conteúdo do playbook.

4. Manter o documento em português do Brasil.

Requisitos para atualização de `README.md`:

1. Atualizar apenas se houver seção operacional adequada.
2. Se atualizar, adicionar link curto para:

   * `docs/operations/batch-execution-playbook.md`
3. Não transformar README em manual longo.
4. Não prometer comportamento não implementado.

Requisitos para atualização de `docs/alignment/roadmap.md`:

1. Atualizar apenas se fizer sentido.
2. Se atualizar, mencionar que execução em batch entrou no fluxo operacional.
3. Não duplicar o playbook.
4. Não reordenar roadmap inteiro sem necessidade.

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

* `docs/operations/batch-execution-playbook.md` existe.
* O playbook explica execução de uma missão versus execução em batch.
* O playbook documenta `VAF_BATCH_SIZE=3`.
* O playbook documenta `VAF_BATCH_SIZE=10`.
* O playbook documenta `VAF_AUTO_PUSH=1`.
* O playbook explica que batch de 10 só deve ser usado após batch de 3 bem-sucedido.
* O playbook explica por que não usar `VAF_COMMIT_MESSAGE` único em batch sem decisão consciente.
* O playbook contém comandos de pré-validação.
* O playbook contém comandos de pós-validação.
* O playbook contém seção “Quando NÃO fazer push”.
* O playbook contém seção de investigação de falhas.
* `docs/operations/safe-runner-usage.md` aponta para o playbook.
* `README.md` é atualizado somente se necessário.
* `docs/alignment/roadmap.md` é atualizado somente se necessário.
* Nenhum código Python é alterado.
* Nenhum script shell é alterado.
* Nenhuma dependência é adicionada.
* `pytest` passa.
* `python3 -m compileall src` passa.
* O commit automático usa mensagem em português do Brasil.


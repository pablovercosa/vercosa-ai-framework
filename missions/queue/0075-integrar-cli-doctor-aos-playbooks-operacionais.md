Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/documentation/language-and-commit-standard.md
- docs/documentation/documentation-update-policy.md
- docs/architecture/module-index.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- docs/examples/mission-batch-operational-flow.md
- src/vercosa_ai_framework/cli/README.md
- src/vercosa_ai_framework/cli/main.py
- tests/test_cli_operacional_inicial.py
- tests/test_cli_validate.py
- tests/test_cli_doctor.py

Assuma o papel de:
- documentation-agent;
- cli-engineer;
- operations-engineer;
- reliability-engineer;
- developer-experience-engineer.

Missão:
Integrar CLI doctor aos playbooks operacionais.

Objetivo:
Atualizar a documentação operacional para incorporar o comando doctor da CLI como ferramenta de diagnóstico local complementar aos scripts shell, sem substituir os scripts existentes, sem alterar código e sem prometer validações que o doctor ainda não implementa.

Contexto:
- A CLI operacional inicial já existe.
- O comando validate já existe.
- O comando doctor já existe.
- O runner seguro de uma missão continua existindo.
- O runner seguro em batch continua existindo.
- O batch passou a ser fluxo operacional padrão quando seguro.
- Os playbooks operacionais ainda precisam explicar melhor quando usar doctor, validate, vaf-status.sh, pytest e compileall.
- O doctor é diagnóstico local e não destrutivo.
- O doctor não executa missões.
- O doctor não substitui pytest.
- O doctor não substitui compileall.
- O doctor não substitui vaf-status.sh.
- O doctor não deve ser documentado como verificação completa de Git, provider, rede, quota ou runtime se isso ainda não estiver implementado.

Entregáveis obrigatórios:
1. Atualizar:
   - docs/operations/batch-execution-playbook.md
   - docs/operations/post-batch-validation-checklist.md
   - docs/operations/safe-runner-usage.md
   - src/vercosa_ai_framework/cli/README.md

2. Atualizar, se necessário:
   - README.md
   - docs/examples/mission-batch-operational-flow.md
   - docs/alignment/current-state.md

3. Não alterar código Python.

4. Não alterar scripts shell.

5. Não adicionar dependências.

Requisitos para docs/operations/batch-execution-playbook.md:
1. Explicar onde o comando doctor entra no fluxo de batch.

2. Registrar que doctor pode ser usado:
   - antes de preparar um batch;
   - antes de executar um batch;
   - depois de um batch;
   - durante investigação de estado inconsistente;
   - após interrupção por limite externo de API.

3. Explicar que doctor não substitui:
   - ./scripts/vaf-status.sh;
   - pytest;
   - python3 -m compileall src;
   - revisão dos logs;
   - revisão dos commits.

4. Incluir exemplo operacional em texto claro para uso do doctor.

5. Se o comando real exigir invocação via python -m, documentar a forma correta conforme implementação existente.

6. Se a CLI ainda não tiver entrypoint instalado como comando de sistema, não documentar como se tivesse.

7. Explicar diferença prática:
   - vaf-status.sh mostra estado operacional dos scripts e missões;
   - validate verifica estrutura mínima;
   - doctor fornece diagnóstico local mais amigável;
   - pytest valida testes;
   - compileall valida compilação dos módulos Python.

8. Não duplicar todo o README da CLI.

9. Não prometer validações futuras como implementadas.

Requisitos para docs/operations/post-batch-validation-checklist.md:
1. Adicionar doctor como etapa complementar de diagnóstico pós-batch.

2. Manter obrigatórias as validações já existentes:
   - ./scripts/vaf-status.sh;
   - git status --short;
   - git log --oneline --decorate;
   - pytest;
   - python3 -m compileall src.

3. Explicar que doctor pode ajudar a identificar inconsistências estruturais, mas não substitui validações formais.

4. Explicar que se doctor apontar erro, não fazer push até investigar.

5. Explicar que se doctor apontar warning, avaliar antes de continuar.

6. Não transformar doctor em requisito único de aprovação.

Requisitos para docs/operations/safe-runner-usage.md:
1. Adicionar referência curta ao doctor como diagnóstico auxiliar.

2. Explicar que o runner seguro continua sendo responsável por executar missão.

3. Explicar que doctor não executa missões.

4. Apontar para o playbook de batch e para o README da CLI, se fizer sentido.

Requisitos para src/vercosa_ai_framework/cli/README.md:
1. Garantir que a documentação da CLI esteja em português do Brasil.

2. Explicar claramente os comandos:
   - status;
   - validate;
   - doctor.

3. Explicar a diferença entre esses comandos.

4. Explicar limites do doctor.

5. Explicar que doctor não chama scripts shell.

6. Explicar que doctor não executa pytest.

7. Explicar que doctor não executa compileall.

8. Explicar que doctor não acessa rede.

9. Explicar que doctor não altera arquivos.

10. Adicionar referência aos playbooks operacionais, se fizer sentido.

Requisitos para README.md:
1. Atualizar somente se houver seção operacional adequada.

2. Se atualizar, mencionar doctor de forma breve como parte da CLI operacional.

3. Não transformar o README principal em manual da CLI.

Requisitos para docs/examples/mission-batch-operational-flow.md:
1. Atualizar somente se o exemplo ficar mais claro com doctor.

2. Não duplicar o playbook.

3. Não prometer comportamento não implementado.

Requisitos gerais de documentação:
1. Tudo deve estar em português do Brasil.

2. Usar links relativos corretos.

3. Usar comandos reais compatíveis com a implementação existente.

4. Não inventar entrypoint de CLI se ele não existir.

5. Não prometer instalação global da CLI se ela não existir.

6. Diferenciar claramente:
   - diagnóstico local;
   - validação estrutural;
   - validação de testes;
   - validação de compilação;
   - status operacional.

7. Não alterar comportamento do projeto.

8. Não alterar código.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar comandos novos.
- Não alterar comandos existentes.
- Não executar missões.
- Não adicionar dependências.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- docs/operations/batch-execution-playbook.md menciona doctor como diagnóstico auxiliar.
- docs/operations/post-batch-validation-checklist.md inclui doctor como etapa complementar.
- docs/operations/safe-runner-usage.md referencia doctor de forma coerente.
- src/vercosa_ai_framework/cli/README.md diferencia status, validate e doctor.
- Documentação deixa claro que doctor não substitui pytest.
- Documentação deixa claro que doctor não substitui compileall.
- Documentação deixa claro que doctor não substitui vaf-status.sh.
- Documentação não inventa entrypoint global inexistente.
- README.md foi atualizado somente se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

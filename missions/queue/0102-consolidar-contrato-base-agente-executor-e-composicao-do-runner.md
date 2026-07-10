Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- CHANGELOG.md
- pyproject.toml
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/alignment/implementation-status.md
- docs/roadmap/mission-backlog.md
- docs/audits/objective-and-scope-alignment-audit.md
- docs/history/mission-milestones.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- scripts/vaf-run-one-mission.sh
- scripts/vaf-run-next-safe.sh
- scripts/vaf-run-batch-safe.sh
- scripts/vaf-status.sh
- src/vercosa_ai_framework/missions/
- tests/

Leia também, se existirem:
- logs/pre-audit-agents-skills-specs.md
- .opencode/
- .opencode/agents/
- agents/
- skills/
- missions/base/
- missions/templates/
- missions/queue/
- missions/running/
- missions/done/
- missions/failed/
- tests/test_mission_runner.py
- tests/test_mission_prompt_composition.py
- tests/test_mission_contract.py
- tests/test_cli_missions.py

Assuma o papel de:
- mission-system-architect;
- runner-engineer;
- prompt-composition-engineer;
- security-reviewer;
- test-engineer;
- documentation-agent.

Missão:
Consolidar contrato base de execução, agente executor base, formato compacto de missão e composição obrigatória pelo runner.

Objetivo:
Eliminar a repetição excessiva de regras comuns nos arquivos de missão e garantir que essas regras continuem sendo aplicadas de forma obrigatória, determinística, versionada e testável.

Princípio central:
As regras comuns não devem depender de o modelo lembrar de procurá-las nem de cada missão repeti-las. O runner deve montar explicitamente o contexto final de execução.

Composição obrigatória esperada:

AGENTS.md
+
contrato base versionado
+
agente executor base
+
agentes especializados declarados
+
arquivo específico da missão

Contexto:
- As missões atuais repetem grandes blocos de regras, restrições e critérios comuns.
- Essa repetição aumenta custo, consumo de contexto, risco de divergência e dificuldade de manutenção.
- A missão 0101 audita a aderência do projeto ao objetivo original.
- Esta missão deve usar os resultados da 0101 como referência.
- As missões 0001–0102 são consideradas missões legadas e não devem ser reescritas.
- As missões 0103 em diante deverão usar formato compacto.
- O runner deve continuar compatível com missões legadas.
- Regras comuns devem ser centralizadas.
- Exceções devem ser declaradas explicitamente por missão.
- Capacidades perigosas devem seguir negação por padrão.
- Esta missão altera infraestrutura do runner e, portanto, deve preservar cuidadosamente recuperação, logs, commits e parada na primeira falha.

Entregáveis obrigatórios:
1. Criar:
   - missions/base/EXECUTION_CONTRACT.md

2. Criar:
   - missions/templates/COMPACT_MISSION_TEMPLATE.md

3. Criar agente executor base conforme a convenção real do projeto.

4. Local recomendado, se compatível com a estrutura existente:
   - .opencode/agents/mission-executor-base.md

5. Se a convenção real usar outro diretório, utilizar o diretório canônico existente e documentar a decisão.

6. Criar mecanismo determinístico de composição de prompt/contexto.

7. Preferir implementação testável em Python dentro de:
   - src/vercosa_ai_framework/missions/

8. Atualizar o runner para usar obrigatoriamente o mecanismo de composição.

9. Criar ou atualizar testes:
   - tests/test_mission_prompt_composition.py
   - tests/test_mission_contract.py
   - testes existentes do runner, quando necessário.

10. Criar documentação:
   - docs/operations/mission-execution-contract.md
   - docs/operations/compact-mission-format.md

11. Atualizar:
   - AGENTS.md
   - README.md
   - CONTRIBUTING.md
   - CHANGELOG.md
   - docs/operations/safe-runner-usage.md
   - docs/operations/batch-execution-playbook.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/implementation-status.md
   - docs/roadmap/mission-backlog.md

12. Atualizar, se necessário:
   - docs/alignment/open-questions.md
   - docs/history/mission-milestones.md
   - src/vercosa_ai_framework/missions/README.md
   - src/vercosa_ai_framework/cli/README.md

13. Não reescrever missões concluídas.

14. Não reescrever as missões 0098–0102.

15. Não criar as missões 0103–0110 nesta missão.

16. Não fazer push.

Arquitetura obrigatória:
1. AGENTS.md deve continuar sendo a fonte das regras permanentes do repositório.

2. O contrato base deve conter regras comuns de execução de missões.

3. O agente executor base deve conter comportamento operacional e critérios gerais de atuação.

4. O arquivo específico da missão deve conter somente:
   - identificação;
   - título;
   - objetivo;
   - contexto específico;
   - entradas específicas;
   - entregáveis específicos;
   - permissões excepcionais;
   - critérios de aceite específicos.

5. O runner deve carregar os componentes na ordem definida.

6. A composição não pode depender de instrução verbal para o modelo ler os arquivos.

7. O runner deve fornecer o conteúdo efetivo dos arquivos ao processo executor.

8. O resultado da composição deve possuir delimitadores claros entre as seções.

9. O mecanismo deve evitar duplicação do agente executor base.

10. O mecanismo deve evitar inclusão duplicada de agentes especializados.

11. O mecanismo deve preservar a ordem declarada dos agentes especializados.

12. O mecanismo deve falhar de forma clara se um agente obrigatório não existir.

13. O mecanismo deve falhar de forma clara se a versão do contrato não existir.

14. A falha de composição deve ocorrer antes da execução da missão.

15. Uma falha de composição não deve deixar a missão presa em running.

16. Uma falha de composição não deve criar commit.

17. Uma falha de composição não deve alterar arquivos do projeto.

Contrato base:
1. O contrato deve ser versionado.

2. A primeira versão deve ser identificada como:
   - v1

3. Pode ser usado:
   - missions/base/EXECUTION_CONTRACT.md
   com metadado explícito de versão;
   ou
   - missions/base/EXECUTION_CONTRACT_v1.md

4. Escolher uma estratégia simples e documentada.

5. O contrato deve conter as regras comuns atualmente repetidas, incluindo:
   - trabalhar somente dentro do repositório;
   - respeitar AGENTS.md;
   - preservar o objetivo da missão;
   - não ampliar escopo silenciosamente;
   - não esconder falhas;
   - não inventar implementação;
   - manter documentação em português do Brasil;
   - preservar termos técnicos quando necessário;
   - não expor secrets;
   - não usar sudo;
   - não reescrever histórico Git;
   - não usar force push;
   - não usar git add .;
   - usar staging explícito;
   - não fazer push sem autorização;
   - não criar tag sem autorização;
   - não criar release sem autorização;
   - não publicar pacote sem autorização;
   - executar pytest;
   - executar python3 -m compileall src;
   - interromper e relatar falhas;
   - criar commit único e coerente quando a missão for concluída;
   - usar mensagem de commit em português do Brasil;
   - atualizar documentação somente quando pertinente;
   - não tratar documentação como prova de implementação;
   - não tratar arquivo criado como prova de integração;
   - não declarar algo concluído sem evidência.

6. O contrato deve distinguir:
   - regra obrigatória;
   - comportamento padrão;
   - permissão excepcional;
   - critério específico da missão.

7. O contrato deve explicar precedência das instruções.

Precedência recomendada:
1. regras de segurança e do repositório;
2. AGENTS.md;
3. contrato base;
4. agente executor base;
5. agentes especializados;
6. missão específica;
7. permissões explícitas válidas.

8. A missão específica pode ampliar capacidades somente nos campos permitidos pelo contrato.

9. A missão específica não pode revogar regras permanentes de segurança, Git ou integridade do projeto.

Negação por padrão:
1. As seguintes capacidades devem ser negadas por padrão:
   - network;
   - database;
   - providers;
   - git_push;
   - git_tag;
   - release;
   - package_publish;
   - sudo;
   - destructive_commands.

2. A ausência do campo deve equivaler a deny.

3. Valores aceitos devem ser explicitamente documentados.

4. Valores recomendados:
   - deny;
   - allow;
   - local-only;
   - read-only;
   - not-applicable.

5. Nem todos os valores precisam ser válidos para todas as capacidades.

6. O mecanismo deve validar combinações incompatíveis.

7. Exemplos:
   - database: deny
   - database: read-only
   - database: allow
   - network: deny
   - network: local-only
   - network: allow
   - providers: deny
   - providers: allow
   - git_push: deny
   - git_push: allow

8. Permissões perigosas devem exigir declaração explícita.

9. Permissões explícitas devem aparecer no contexto composto de forma visível.

10. O runner não precisa implementar sandbox técnico completo nesta missão.

11. O contrato deve deixar claro que permissões declaradas são políticas de execução e não substituem controles do sistema operacional.

Formato compacto:
1. O formato deve usar frontmatter simples e validável.

2. Não adicionar dependência de parser YAML.

3. Se usar sintaxe semelhante a YAML, implementar apenas o subconjunto necessário com biblioteca padrão.

4. Campos mínimos recomendados:
   - id;
   - title;
   - base_contract;
   - agents;
   - network;
   - database;
   - providers;
   - git_push;
   - git_tag;
   - release;
   - package_publish;
   - sudo;
   - destructive_commands.

5. Campos opcionais podem ser adicionados somente se houver necessidade real.

6. Exemplo conceitual:

---
id: "0103"
title: "Inventariar integralmente o repositório"
base_contract: "v1"
agents:
  - repository-auditor
network: deny
database: deny
providers: deny
git_push: deny
git_tag: deny
release: deny
package_publish: deny
sudo: deny
destructive_commands: deny
---

# Objetivo

Conteúdo específico.

7. O agente executor base deve ser incluído automaticamente pelo compositor.

8. Se mission-executor-base também aparecer na lista agents, ele deve ser deduplicado.

9. O template deve mostrar:
   - objetivo;
   - contexto específico;
   - entradas específicas;
   - entregáveis;
   - critérios específicos.

10. O template não deve repetir o contrato completo.

11. O template deve apontar para a documentação do contrato.

12. O template deve estar em português do Brasil.

Compatibilidade legada:
1. Missões sem frontmatter devem continuar executáveis.

2. Missões legadas devem ser identificadas como:
   - legacy

3. Para missões legadas, o runner deve preservar o comportamento atual.

4. O runner pode adicionar AGENTS.md e agente executor base às missões legadas somente se isso não alterar perigosamente o comportamento.

5. A decisão deve ser documentada.

6. Não modificar arquivos em missions/done.

7. Não migrar automaticamente missões antigas.

8. Não exigir base_contract de missões já existentes.

9. Missões compactas devem exigir base_contract válido.

10. O formato legado deve ser considerado compatibilidade, não padrão futuro.

Agente executor base:
1. Criar um agente ou fragmento de agente conforme a convenção real do OpenCode no projeto.

2. Nome canônico:
   - mission-executor-base

3. O agente deve reforçar:
   - aderência ao objetivo;
   - leitura crítica do contexto;
   - execução conservadora;
   - evidências;
   - testes;
   - documentação;
   - segurança;
   - staging explícito;
   - commit coerente;
   - relatório final.

4. O agente não deve duplicar integralmente o contrato base.

5. O agente deve referenciar o contrato como fonte normativa.

6. O agente deve orientar o executor a:
   - diferenciar planejado, implementado, integrado e validado;
   - não criar funcionalidade fora do escopo;
   - não esconder limitações;
   - interromper diante de bloqueio real;
   - evitar mudanças desnecessárias.

7. Agentes especializados devem complementar, não substituir, o agente base.

Agentes especializados:
1. O compositor deve localizar agentes especializados conforme convenção do projeto.

2. Não criar todos os agentes especializados nesta missão.

3. Utilizar agentes existentes quando declarados.

4. Agente inexistente deve gerar erro claro antes da execução.

5. Não ignorar silenciosamente agente ausente.

6. Não acessar agentes fora dos diretórios autorizados.

7. Validar nomes para impedir path traversal.

8. Rejeitar nomes contendo:
   - ../
   - caminho absoluto;
   - separadores inesperados;
   - caracteres incompatíveis com o padrão definido.

Compositor:
1. Preferir módulo Python pequeno e testável.

2. Nome sugerido:
   - src/vercosa_ai_framework/missions/prompt_composer.py

3. O nome final deve respeitar a arquitetura existente.

4. O compositor deve receber:
   - caminho da missão;
   - raiz do projeto;
   - opcionalmente destino de saída.

5. O compositor deve:
   - detectar formato legado ou compacto;
   - validar metadados;
   - localizar contrato;
   - localizar agente base;
   - localizar agentes especializados;
   - aplicar defaults;
   - validar capacidades;
   - compor conteúdo;
   - produzir erro legível.

6. Usar somente biblioteca padrão.

7. Não usar PyYAML.

8. Não acessar rede.

9. Não acessar banco.

10. Não chamar providers.

11. Não modificar a missão.

12. Não modificar AGENTS.md.

13. Não modificar agentes.

14. Não registrar secrets.

15. Não armazenar permanentemente prompts compostos por padrão.

16. Se o runner precisar de arquivo temporário:
   - usar diretório temporário seguro;
   - remover ao final;
   - não versionar;
   - não expor conteúdo desnecessariamente em logs.

17. O compositor deve permitir modo de validação sem execução.

18. Interface sugerida:
   - python3 -m vercosa_ai_framework.missions.prompt_composer --validate missão.md
   - python3 -m vercosa_ai_framework.missions.prompt_composer --compose missão.md

19. A interface final pode variar se houver padrão melhor já existente.

Integração com runner:
1. Identificar qual script efetivamente invoca o OpenCode.

2. Alterar somente o ponto necessário.

3. O runner deve chamar o compositor antes da execução.

4. O runner deve passar o contexto composto ao executor.

5. O runner deve preservar:
   - ordenação de missões;
   - queue;
   - running;
   - done;
   - failed;
   - logs;
   - parada na primeira falha;
   - commit por missão;
   - resumo final;
   - recuperação após interrupção.

6. O runner não deve executar uma missão compacta inválida.

7. Se a validação falhar:
   - missão permanece ou retorna para queue;
   - running fica limpo;
   - erro é registrado;
   - batch para;
   - nenhum commit é criado.

8. O runner não deve fazer push.

9. O runner não deve alterar VAF_BATCH_SIZE.

10. O runner não deve alterar a regra de batch padrão para oito nesta missão, salvo atualização documental.

11. Documentar que o teto padrão recomendado passa a ser oito missões.

12. Missões estruturais ou pesadas devem usar blocos menores.

13. Recuperações devem usar uma a três missões.

Testes obrigatórios:
1. Testar composição de missão compacta válida.

2. Verificar a ordem:
   - AGENTS.md;
   - contrato;
   - agente base;
   - agentes especializados;
   - missão.

3. Testar defaults deny.

4. Testar permissão explícita allow.

5. Testar local-only.

6. Testar read-only quando aplicável.

7. Testar contrato inexistente.

8. Testar versão de contrato inválida.

9. Testar agente base inexistente.

10. Testar agente especializado inexistente.

11. Testar agente duplicado.

12. Testar tentativa de path traversal em nome de agente.

13. Testar missão compacta sem id.

14. Testar missão compacta sem title.

15. Testar missão compacta sem base_contract.

16. Testar valor de capacidade inválido.

17. Testar missão legada.

18. Testar que missão legada não precisa de frontmatter.

19. Testar que a composição não modifica arquivos de origem.

20. Testar modo validate.

21. Testar erro antes de execução.

22. Testar integração mínima com o runner sem chamar provider real.

23. Usar mocks ou executores falsos apenas quando necessário.

24. Não chamar OpenCode real nos testes.

25. Não acessar rede.

26. Não acessar banco.

27. Não depender da fila real.

28. Usar diretórios temporários.

29. Preservar todos os testes existentes.

30. Executar:
   - pytest
   - python3 -m compileall src

Documentação obrigatória:
1. docs/operations/mission-execution-contract.md deve explicar:
   - objetivo do contrato;
   - precedência;
   - regras comuns;
   - negação por padrão;
   - permissões explícitas;
   - versionamento;
   - compatibilidade legada;
   - responsabilidade do runner;
   - limites do mecanismo.

2. docs/operations/compact-mission-format.md deve explicar:
   - frontmatter;
   - campos;
   - valores aceitos;
   - exemplos;
   - agentes;
   - capacidades;
   - template;
   - validação;
   - erros comuns.

3. AGENTS.md deve apontar para o contrato base.

4. AGENTS.md não deve duplicar integralmente o contrato.

5. README.md deve mencionar de forma breve:
   - missões compactas;
   - contrato base;
   - composição obrigatória.

6. CONTRIBUTING.md deve orientar novos contribuidores a usar o template compacto.

7. docs/operations/safe-runner-usage.md deve documentar:
   - composição;
   - validação;
   - falhas;
   - recuperação;
   - batch padrão de até oito.

8. docs/operations/batch-execution-playbook.md deve documentar:
   - batch normal de até oito;
   - missões pesadas de duas a quatro;
   - recuperação de uma a três;
   - mudanças estruturais em bloco pequeno.

9. docs/alignment/current-state.md deve registrar a nova infraestrutura.

10. docs/alignment/implementation-status.md deve distinguir:
   - contrato criado;
   - compositor implementado;
   - runner integrado;
   - formato compacto validado.

11. docs/alignment/roadmap.md deve registrar que as missões 0103–0110 usarão o novo formato.

12. docs/roadmap/mission-backlog.md deve atualizar o estado da missão 0102.

13. CHANGELOG.md deve registrar:
   - contrato base versionado;
   - agente executor base;
   - compositor obrigatório;
   - formato compacto;
   - compatibilidade legada.

14. Não copiar o checklist completo para CHANGELOG.md.

Internacionalização:
1. PT-BR permanece o idioma canônico do contrato e do template.

2. Termos técnicos podem permanecer em inglês.

3. Não criar traduções nesta missão.

4. Não criar README.en.md.

5. Não criar README.es.md.

6. Registrar que internacionalização será auditada na missão 0108.

Segurança:
1. Rejeitar caminhos fora da raiz autorizada.

2. Rejeitar path traversal.

3. Não executar conteúdo de frontmatter.

4. Não usar eval.

5. Não usar source em metadados da missão.

6. Não interpolar valores como comandos shell.

7. Não registrar variáveis de ambiente completas.

8. Não registrar credenciais.

9. Não registrar tokens.

10. Não persistir o prompt composto em logs por padrão.

11. Não permitir que uma missão autorize:
   - force push;
   - reescrita de histórico;
   - exposição de secrets.

12. Essas proibições devem permanecer invariantes.

Restrições:
- Não reescrever missões concluídas.
- Não migrar missions/done.
- Não criar as missões 0103–0110.
- Não implementar PostgreSQL.
- Não implementar RAG.
- Não implementar internacionalização.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não fazer push.
- Não usar sudo.
- Não adicionar dependências.
- Não acessar rede durante testes.
- Não acessar banco.
- Não chamar providers nos testes.
- Não usar eval.
- Não usar git add .
- Não fazer force push.
- Não reescrever histórico Git.
- Não esconder falhas.
- Código, documentação, testes e mensagens devem estar em português do Brasil quando aplicável.

Critérios de aceite:
- missions/base/EXECUTION_CONTRACT.md ou equivalente versionado existe.
- missions/templates/COMPACT_MISSION_TEMPLATE.md existe.
- mission-executor-base existe no local canônico.
- O contrato define regras comuns e precedência.
- Capacidades seguem negação por padrão.
- O formato compacto possui frontmatter validável.
- O compositor usa somente biblioteca padrão.
- O compositor inclui AGENTS.md obrigatoriamente.
- O compositor inclui contrato válido obrigatoriamente.
- O compositor inclui agente executor base obrigatoriamente.
- O compositor inclui agentes especializados declarados.
- O compositor deduplica agentes.
- O compositor rejeita path traversal.
- O runner usa o compositor antes de executar missão compacta.
- Falha de composição não deixa missão presa em running.
- Missões legadas continuam compatíveis.
- Missões 0001–0102 não foram reescritas.
- Testes cobrem composição, defaults, permissões, erros e legado.
- Documentação operacional foi atualizada.
- Batch normal de até oito foi documentado.
- CHANGELOG.md registra a mudança sem virar checklist operacional.
- Nenhuma dependência foi adicionada.
- Nenhuma tag foi criada.
- Nenhuma release foi publicada.
- Nenhum push foi feito.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

---
version: v1
status: active
---

# Contrato Base De Execução De Missões

## Objetivo

Centralizar as regras comuns de execução de missões do Vercosa AI Framework para reduzir repetição nos arquivos de missão e permitir composição determinística pelo runner.

Este contrato é a fonte normativa das regras comuns específicas de execução de missões. `AGENTS.md` continua sendo a fonte das regras globais e permanentes do repositório.

## Versão

Versão atual: `v1`.

A estratégia inicial usa um único arquivo em `missions/base/EXECUTION_CONTRACT.md` com metadado explícito `version: v1`. Novas versões devem ser adicionadas por missão própria, com documentação de migração e sem reescrever missões concluídas.

## Precedência

Quando houver conflito, aplique esta ordem:

1. Regras de segurança, integridade do repositório e instruções do sistema de execução.
2. `AGENTS.md`.
3. Este contrato base.
4. Agente executor base.
5. Agentes operacionais especializados declarados pela missão.
6. Arquivo específico da missão.
7. Permissões excepcionais explícitas válidas.

A missão específica pode ampliar capacidades somente nos campos permitidos por este contrato. Ela não pode revogar regras permanentes de segurança, Git, integridade do projeto, proteção de secrets ou preservação de histórico.

## Taxonomia Obrigatória

- `role`: persona temporária usada apenas como orientação da missão; não é resolvida como arquivo de agente.
- `operational agent`: definição versionada carregável a partir de `.opencode/agents/`.
- `product agent`: implementação pertencente a `src/vercosa_ai_framework/agents/`.
- `operational skill`: procedimento reutilizável carregável pelo ambiente de desenvolvimento.
- `product skill`: implementação pertencente a `src/vercosa_ai_framework/skills/`.

Não confunda `.opencode/agents/` com `src/vercosa_ai_framework/agents/`. Não confunda `.opencode/skills/` com `src/vercosa_ai_framework/skills/`.

## Regras Obrigatórias

- Trabalhar somente dentro da raiz autorizada do repositório.
- Respeitar `AGENTS.md`.
- Preservar o objetivo da missão.
- Não ampliar escopo silenciosamente.
- Não esconder falhas.
- Não inventar implementação, integração, teste ou evidência.
- Manter documentação explicativa em português do Brasil.
- Preservar termos técnicos quando forem nomes arquiteturais consolidados.
- Não expor secrets, tokens, credenciais ou dados sensíveis.
- Não usar `sudo`.
- Não reescrever histórico Git.
- Não usar force push.
- Não usar `git add .`.
- Fazer staging explícito dos arquivos pretendidos.
- Não fazer push sem autorização explícita.
- Não criar tag sem autorização explícita.
- Não criar release sem autorização explícita.
- Não publicar pacote sem autorização explícita.
- Executar `pytest` quando a missão alterar código, testes, runner, contrato, documentação operacional crítica ou comportamento público.
- Executar `python3 -m compileall src` quando a missão alterar código Python.
- Interromper e relatar falhas quando validação obrigatória falhar.
- Criar commit único e coerente quando a missão for concluída pelo fluxo operacional configurado para commit automático.
- Usar mensagem de commit em português do Brasil.
- Atualizar documentação somente quando pertinente ao comportamento, arquitetura, operação ou estado alterado.
- Não tratar documentação como prova de implementação.
- Não tratar arquivo criado como prova de integração.
- Não declarar algo concluído sem evidência verificável.

## Comportamento Padrão

- Atuar de forma conservadora e incremental.
- Preferir a menor alteração correta.
- Validar antes de declarar conclusão.
- Diferenciar planejado, implementado, integrado e validado.
- Preservar logs e evidências úteis sem registrar prompts completos, secrets ou variáveis de ambiente completas.
- Parar na primeira falha real em batch ou execução governada.
- Manter missões legadas executáveis sem exigir frontmatter.
- Tratar o formato legado como compatibilidade, não como padrão futuro.

## Permissões Excepcionais

Permissões excepcionais devem ser declaradas no frontmatter da missão compacta e aparecer visivelmente no contexto composto. A ausência do campo equivale a `deny`.

Valores aceitos por capacidade:

| Capacidade | Valores aceitos |
| --- | --- |
| `network` | `deny`, `local-only`, `allow` |
| `database` | `deny`, `read-only`, `allow` |
| `providers` | `deny`, `allow` |
| `git_push` | `deny`, `allow` |
| `git_tag` | `deny`, `allow` |
| `release` | `deny`, `allow` |
| `package_publish` | `deny`, `allow` |
| `sudo` | `deny` |
| `destructive_commands` | `deny` |

Permissões perigosas seguem negação por padrão. Mesmo quando uma missão declara `allow`, isso é política de execução e não substitui controles do sistema operacional, revisão humana, Guardian Specs ou restrições permanentes do repositório.

As seguintes proibições permanecem invariantes e não podem ser autorizadas por missão: force push, reescrita de histórico Git, exposição de secrets, uso de `sudo`, comandos destrutivos fora de política aprovada, tag, release ou publicação de pacote sem autorização explícita fora da própria missão.

## Critérios Específicos Da Missão

O arquivo específico da missão deve conter apenas informações específicas: identificação, título, objetivo, papéis temporários, agentes operacionais especializados, contexto, entradas, entregáveis, permissões excepcionais e critérios de aceite.

Critérios específicos podem adicionar validações, artefatos e restrições ao contrato. Eles não removem as regras obrigatórias deste contrato.

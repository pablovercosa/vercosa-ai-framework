# Contrato De Execução De Missões

## Objetivo

Documentar o contrato base versionado usado pelo runner para compor o contexto final de execução de missões.

O contrato atual está em [missions/base/EXECUTION_CONTRACT.md](../../missions/base/EXECUTION_CONTRACT.md), versão `v1`.

## Responsabilidades

- Centralizar regras comuns de execução de missões.
- Reduzir repetição em arquivos de missão.
- Definir precedência entre `AGENTS.md`, contrato, agentes e missão específica.
- Declarar negação por padrão para capacidades perigosas.
- Permitir validação determinística antes da execução.

## Não Responsabilidades

- Não substitui `AGENTS.md` como fonte global do repositório.
- Não implementa sandbox técnico completo.
- Não autoriza force push, reescrita de histórico, exposição de secrets, tag, release ou publicação de pacote.
- Não prova implementação apenas por documentação.

## Precedência

1. Regras de segurança, integridade do repositório e instruções do sistema de execução.
2. `AGENTS.md`.
3. Contrato base.
4. Agente executor base.
5. Agentes operacionais especializados.
6. Missão específica.
7. Permissões excepcionais explícitas válidas.

## Negação Por Padrão

A ausência de capacidade no frontmatter equivale a `deny`.

Capacidades suportadas: `network`, `database`, `providers`, `git_push`, `git_tag`, `release`, `package_publish`, `sudo` e `destructive_commands`.

Permissões declaradas são política de execução. Elas não substituem revisão humana, Guardian Specs, controles do sistema operacional ou restrições permanentes.

## Compatibilidade Legada

Missões sem frontmatter continuam executáveis como `legacy`. Para manter governança comum, o compositor aplica `v1`, `AGENTS.md` e `mission-executor-base` também ao contexto composto de missões legadas, sem modificar os arquivos originais em `missions/done` ou `missions/queue`.

O formato legado é compatibilidade. O padrão futuro para missões novas a partir de `0103` é o formato compacto.

## Responsabilidade Do Runner

O runner chama `vercosa_ai_framework.missions.prompt_composer` antes de executar a missão. Se a composição falhar, a execução não chama OpenCode, a missão retorna para `queue`, `running` fica limpo e nenhum commit deve ser criado.

## Limites

O prompt composto não é persistido por padrão. Quando o runner shell precisa de arquivo temporário, ele usa `mktemp` e remove o arquivo ao final.

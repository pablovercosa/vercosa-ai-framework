# Formato Compacto De Missão

## Objetivo

Definir o formato compacto para missões novas do Vercosa AI Framework, evitando repetição de regras comuns já centralizadas no contrato base.

Template: [missions/templates/COMPACT_MISSION_TEMPLATE.md](../../missions/templates/COMPACT_MISSION_TEMPLATE.md).

Contrato: [docs/operations/mission-execution-contract.md](mission-execution-contract.md).

## Frontmatter

O formato usa frontmatter simples, semelhante a YAML, validado por parser próprio com biblioteca padrão. Não há dependência de PyYAML.

Campos mínimos:

- `id`
- `title`
- `base_contract`

Campos opcionais:

- `roles`
- `agents`

Capacidades com default `deny`:

- `network`
- `database`
- `providers`
- `git_push`
- `git_tag`
- `release`
- `package_publish`
- `sudo`
- `destructive_commands`

## Valores Aceitos

- `network`: `deny`, `local-only`, `allow`.
- `database`: `deny`, `read-only`, `allow`.
- `providers`: `deny`, `allow`.
- `git_push`: `deny`, `allow`.
- `git_tag`: `deny`, `allow`.
- `release`: `deny`, `allow`.
- `package_publish`: `deny`, `allow`.
- `sudo`: `deny`.
- `destructive_commands`: `deny`.

## Agentes E Papéis

`roles` são personas temporárias e não exigem arquivo correspondente.

`agents` são agentes operacionais carregados de `.opencode/agents/`. O compositor inclui automaticamente `mission-executor-base`, deduplica entradas repetidas, preserva a ordem dos agentes especializados e falha antes da execução se um agente declarado não existir.

Nomes de agentes com path traversal, caminho absoluto, separadores ou caracteres incompatíveis são rejeitados.

## Exemplo

```markdown
---
id: "0103"
title: "Inventariar integralmente o repositório"
base_contract: "v1"
roles:
  - repository-auditor
agents:
  - framework-architect
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

Inventariar o repositório.
```

## Validação

Validar sem imprimir o prompt composto:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.missions.prompt_composer --validate missions/queue/0103-exemplo.md
```

Compor para stdout, sem persistência por padrão:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.missions.prompt_composer --compose missions/queue/0103-exemplo.md
```

## Erros Comuns

- `base_contract` ausente ou diferente de `v1`.
- Agente operacional declarado sem arquivo em `.opencode/agents/`.
- Papel temporário colocado em `agents` por engano.
- Valor de capacidade incompatível, como `network: read-only`.
- Nome de agente com `../`, `/`, `\` ou caminho absoluto.

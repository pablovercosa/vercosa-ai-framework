# Ciclo De Vida SDD

## Objetivo

Definir o ciclo de vida desejado de Specification-Driven Development para o Vercosa AI Framework.

Ciclo alvo:

```text
Spec → Plan → Tasks → Implement → Validate → Commit
```

O ciclo torna o desenvolvimento assistido por IA reproduzível, auditável, governado por políticas e agnóstico de provider.

## Princípios Do Ciclo

- Specs são a fonte da verdade.
- Implementação não começa sem Spec aprovada.
- Plans explicam como uma Spec será satisfeita antes de mudanças de código.
- Tasks são unidades de execução limitadas e rastreáveis.
- Implementação ocorre por agentes, capabilities, skills, tools e runtime adapters governados.
- Validação é obrigatória antes da conclusão.
- Commits são checkpoints com evidência, não efeitos automáticos por padrão.
- Todo loop possui condição de parada.
- Todo efeito externo é avaliado por política.

## Etapa 1: Spec

Objetivo: definir problema, escopo, restrições, requisitos de política, critérios de aceite e fronteiras.

Entradas:

- missão do usuário;
- Specs existentes;
- Guardian Specs;
- ADRs;
- contexto do projeto;
- documentos de conhecimento relevantes.

Saídas obrigatórias:

- referência de Spec;
- status;
- objetivo;
- escopo;
- fora de escopo;
- decisões arquiteturais ou candidatas;
- critérios de aceite;
- restrições de segurança, privacidade, custo, tokens, qualidade e validação;
- perguntas pendentes.

Regra de aprovação: implementação exige Spec aprovada. Trabalho apenas documental pode prosseguir quando a missão restringe explicitamente mudanças à documentação e não cria funcionalidade nem altera código fonte.

## Etapa 2: Plan

Objetivo: traduzir a Spec em abordagem de execução sem alterar artefatos de implementação.

Entradas:

- Spec aprovada;
- mapa de arquitetura;
- módulos afetados;
- análise de dependências e riscos;
- capacidades disponíveis de runtime e provider;
- saída do Context Router quando existir.

Saídas obrigatórias:

- estratégia de implementação;
- arquivos/módulos afetados;
- tasks esperadas;
- estratégia de validação;
- classificação de risco;
- aprovações necessárias;
- pedido de política de modelo/provider;
- condições de parada;
- estratégia de rollback ou revisão manual.

Responsabilidade: Mission Orchestrator deve escolher workflow; Workflow Engine deve estruturar o plano; Agent Orchestrator não deve inventar o plano inteiro sozinho.

## Etapa 3: Tasks

Objetivo: dividir o plano em unidades de trabalho limitadas, ordenadas e validáveis.

Entradas:

- plan;
- política de workflow;
- grafo de dependências;
- riscos e requisitos de validação;
- agentes/capabilities disponíveis.

Saídas obrigatórias:

- IDs de task;
- objetivos de task;
- dependências;
- capabilities necessárias;
- critérios de aceite por task;
- caminhos permitidos;
- caminhos negados;
- limites de execução;
- requisitos de validação;
- artefatos esperados.

Responsabilidade: Workflow Engine deve produzir ou normalizar a estrutura de tasks. Task Queue deve controlar estado, elegibilidade, tentativas, retries e agendamento.

## Etapa 4: Implement

Objetivo: executar tasks por fronteiras governadas do framework.

Entradas:

- task;
- perfil de agente;
- capability request;
- decisões de política;
- pacote de contexto;
- decisão de modelo;
- permissões de runtime/tool.

Caminho esperado:

```text
Task Queue
↓
Agent Orchestrator
↓
Agent or Subagent
↓
Capability Request
↓
Capability Resolver
↓
Skill Executor
↓
Tool Executor
↓
Provider Gateway or Runtime Adapter
↓
Concrete provider, MCP, API, runtime, or filesystem adapter
```

Caminho MVP atual possível:

```text
Mission Runner or Workflow Engine
↓
Guardian Engine
↓
Runtime Adapter
↓
OpenCode adapter or fake adapter
```

Regras de implementação:

- Não contornar decisões Guardian.
- Não chamar providers ou MCPs diretamente de agentes.
- Não alterar configuração global sem aprovação explícita por política e Spec.
- Não usar `sudo` por padrão.
- Não expor segredos em logs, prompts, commits ou providers externos.
- Não hardcodar provider, modelo, banco, runtime, IDE, sistema operacional ou arquitetura.
- Não continuar loops sem limites finitos.

## Etapa 5: Validate

Objetivo: provar que entregas de task e missão satisfazem Spec, plan, critérios de task, Guardian Specs e requisitos de qualidade.

Fontes de validação:

- testes automatizados;
- checks de sintaxe;
- lint/análise estática;
- type checks;
- revisão arquitetural;
- revisão de segurança;
- revisão documental;
- critérios de aceite;
- existência de artefatos;
- aprovação humana;
- revisão cruzada por outro agente/modelo quando política exigir.

Saídas obrigatórias:

- resultado de validação;
- comandos ou checks executados;
- status pass/fail;
- warnings;
- validações puladas e motivos;
- decisões de política referenciadas;
- artefatos validados;
- riscos residuais.

Regras:

- Uma task não deve ser marcada como concluída sem validação aplicável ou motivo aprovado por política.
- Uma missão não deve ser marcada como concluída até que tasks e entregáveis obrigatórios sejam validados.
- Falha deve retornar para replanejamento, retry, revisão manual ou falha de missão conforme política.
- Validação crítica não deve depender apenas do mesmo agente que executou a implementação.

## Etapa 6: Commit

Objetivo: criar checkpoint de versionamento após validação.

Política padrão: auto-commit permanece desabilitado salvo autorização explícita.

Pré-requisitos de commit:

- referência de Spec aprovada;
- plan/tasks concluídos;
- evidência de validação;
- arquivos alterados revisados;
- nenhuma mudança não relacionada do usuário incluída;
- nenhum segredo;
- nenhum artefato sensível gerado;
- política de commit permitindo a ação.

Metadados recomendados:

- ID da missão;
- referências de Specs;
- resumo das mudanças;
- validação realizada;
- limitações conhecidas quando existirem.

Regras:

- Não commitar mudanças fora do escopo da missão.
- Não fazer amend nem reescrever histórico salvo pedido explícito.
- Não fazer push automaticamente sem política e aprovação separadas.
- Ambiguidade na worktree deve bloquear commit automático ou exigir revisão manual.
- Mensagens de commit futuras devem usar português do Brasil, conforme [padrão de idioma e commits](../documentation/language-and-commit-standard.md).

## Máquina De Estados Desejada

Estado de missão:

```text
created
↓
spec_required or spec_approved
↓
planned
↓
tasks_ready
↓
running
↓
validating
↓
done | failed | cancelled | requires_review
```

Estado de task:

```text
pending
↓
eligible
↓
running
↓
validating
↓
done | failed | blocked | skipped | cancelled | requires_review
```

Loop de agente:

```text
IDLE
↓
PLANNING
↓
EXECUTING
↓
REFLECTING
↓
VALIDATING
↓
REPLANNING
↓
DONE
```

Todo loop deve incluir máximo de ciclos, limites de retry, limites de budget e condições de parada.

## Mapeamento Para O MVP Atual

Suporte atual do repositório:

- Specs existem em `specs/framework/`.
- Mission Runner MVP suporta estados como queued/running/done/failed/cancelled.
- Workflow Engine MVP suporta execução sequencial e checks Guardian.
- Task Queue MVP suporta estados, dependências, tentativas, retries e agendamento determinístico.
- Guardian Engine MVP suporta decisões `allow`, `warn`, `block` e `require_approval`.
- OpenCode Runtime Adapter MVP suporta execução governada e dry-run.
- CLI suporta checks de missão, run-one, worker, status, validação e execução/dry-run de workflow.

Lacunas ou itens parciais:

- registry formal de aprovação de Specs;
- artefato formal de Plan;
- camada Mission Orchestrator;
- integração completa de Task Queue no Workflow Engine;
- integração completa de Agent Orchestrator na execução de tasks;
- Context Router;
- integração de audit log persistente;
- store de evidências de validação;
- automação de governança de commit;
- execução de política de revisão cruzada.

## Próxima Melhoria SDD Recomendada

Antes de implementar mais funcionalidades, definir schemas mínimos para:

- registro de aprovação de Spec;
- registro de Plan;
- registro de Task;
- resultado de validação;
- referência de decisão Guardian;
- referência de decisão de modelo;
- registro de decisão de commit.

Esses registros devem ser persistidos pela Persistence Layer em vez de ficarem apenas em saída de CLI ou estado em memória.

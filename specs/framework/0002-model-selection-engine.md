# Spec 0002 — Model Selection Engine

## Status

Proposta.

## Objetivo

Definir o Model Selection Engine do Vercosa AI Framework como o componente responsável por selecionar, justificar e alternar modelos de IA por tarefa, com base em políticas, disponibilidade, custo, qualidade, segurança, contexto e requisitos de execução.

O modelo usado por agentes, subagentes, skills ou workflows não deve ser hardcoded.

## Contexto

O Vercosa AI Framework é AI Native, Provider Agnostic, Local First, Token Efficient e Governance by Design.

A seleção de modelos precisa permitir que uma missão use modelos diferentes para planejamento, implementação, revisão, validação, sumarização, embeddings, extração ou tarefas simples, sem acoplar o framework a um provedor específico.

O OpenCode será o runtime inicial para descoberta e execução de modelos, mas não será o núcleo do Model Selection Engine. OpenCode deve ser tratado como adapter.

## Escopo

Esta Spec cobre:

- contrato arquitetural do Model Selection Engine;
- políticas de seleção por tarefa;
- suporte a modelos gratuitos, locais e pagos;
- fallback entre modelos e providers;
- uso de `small_model` para tarefas simples;
- cabeçalho YAML por arquivo como fonte de política local;
- integração com Guardian Specs;
- integração com Policy Engine;
- integração inicial via OpenCode Adapter;
- critérios mínimos de auditoria, custo e qualidade.

Esta Spec não cobre:

- implementação concreta de adapters;
- formato final de banco de dados ou storage;
- ranking definitivo de modelos específicos;
- dependência obrigatória de OpenCode, Ollama, OpenAI, Anthropic, Google, Groq ou qualquer outro provider;
- implementação de billing real de providers;
- seleção de banco vetorial ou mecanismo de embeddings.

## Princípios

1. Modelos são recursos executáveis, não decisões arquiteturais fixas.
2. Políticas definem intenção; estratégias escolhem modelos concretos.
3. Providers devem ser adapters substituíveis.
4. O menor modelo adequado deve ser preferido quando cumprir qualidade, segurança e contexto.
5. Modelos pagos só devem ser usados quando a política permitir ou a complexidade justificar.
6. Modelos gratuitos ou locais devem ser preferidos para tarefas simples.
7. Toda seleção relevante deve ser auditável quando possível.
8. Fallback deve preservar segurança e qualidade mínima.
9. O framework deve degradar com segurança quando modelos ideais não estiverem disponíveis.
10. OpenCode é runtime inicial, não fonte única de verdade.

## Política, estratégia e execução

A seleção de modelos deve separar claramente três responsabilidades:

- Specs definem políticas: intenção, restrições, orçamento, qualidade mínima, segurança, privacidade, revisão e critérios de aceite;
- o framework define estratégias: descoberta, classificação, fallback, degradação segura, cache, estimativa de custo e roteamento por capacidade;
- modelos apenas executam: um modelo não decide política, não escolhe sozinho outro modelo, não altera orçamento, não reduz requisitos de segurança e não substitui aprovação humana quando exigida.

Essa separação é obrigatória para preservar governança, rastreabilidade e independência de fornecedor.

## Definições

### Model Selection Engine

Componente que recebe uma intenção de execução e retorna uma decisão de modelo.

A decisão inclui o modelo preferido, alternativas de fallback, justificativa, restrições, custo esperado quando disponível e requisitos de validação.

### Model Registry

Catálogo abstrato de modelos conhecidos e disponíveis.

Pode ser preenchido por adapters, arquivos de configuração, runtime local, APIs de providers ou descoberta dinâmica.

### Provider Adapter

Adapter que expõe modelos, capacidades, limites e custo estimado de um provider ou runtime.

Exemplos possíveis:

- OpenCode Adapter;
- Ollama Adapter;
- OpenAI Adapter;
- Anthropic Adapter;
- Google Adapter;
- local runtime adapter;
- enterprise gateway adapter.

### Model Profile

Metadados normalizados de um modelo.

Campos mínimos desejados:

- `id`;
- `provider`;
- `runtime`;
- `availability`;
- `pricing_class`;
- `cost_input`;
- `cost_output`;
- `context_window`;
- `quality_tier`;
- `reasoning_tier`;
- `latency_tier`;
- `privacy_tier`;
- `tool_use`;
- `vision`;
- `json_mode`;
- `structured_output`;
- `embedding`;
- `local`;
- `free`;
- `paid`;
- `deprecated`.

### Selection Request

Entrada normalizada enviada ao Model Selection Engine.

Campos mínimos desejados:

- `task_type`;
- `role`;
- `complexity`;
- `quality`;
- `cost`;
- `reasoning`;
- `memory`;
- `context_size`;
- `security`;
- `privacy`;
- `review`;
- `provider`;
- `model`;
- `fallback`;
- `budget`;
- `latency`;
- `runtime`;
- `constraints`.

### Selection Decision

Saída normalizada produzida pelo Model Selection Engine.

Campos mínimos desejados:

- `selected_model`;
- `selected_provider`;
- `selected_runtime`;
- `fallback_chain`;
- `reason`;
- `policy_sources`;
- `estimated_cost`;
- `quality_expectation`;
- `security_notes`;
- `requires_review`;
- `requires_user_approval`;
- `cache_key` quando aplicável.

## Cabeçalho YAML por arquivo

Arquivos executáveis pelo framework podem declarar políticas locais em cabeçalho YAML.

Exemplo:

```yaml
---
role: architect
complexity: high
quality: maximum
cost: balanced
reasoning: adaptive
memory: adaptive
provider: auto
model: auto
fallback: true
review: mandatory
security: strict
small_model: false
---
```

Campos suportados inicialmente:

- `role`: papel esperado, como `architect`, `developer`, `reviewer`, `security`, `documenter`, `planner`;
- `complexity`: `low`, `medium`, `high`, `critical`;
- `quality`: `draft`, `standard`, `high`, `maximum`;
- `cost`: `economy`, `balanced`, `premium`, `strict_free`;
- `reasoning`: `none`, `light`, `medium`, `high`, `adaptive`;
- `memory`: `none`, `short`, `long`, `adaptive`;
- `provider`: provider específico ou `auto`;
- `model`: modelo específico ou `auto`;
- `fallback`: `true` ou `false`;
- `review`: `none`, `optional`, `recommended`, `mandatory`;
- `security`: `standard`, `strict`, `maximum`;
- `privacy`: `standard`, `local_preferred`, `local_required`;
- `small_model`: `true`, `false` ou `auto`;
- `budget`: limite declarativo de custo quando aplicável;
- `latency`: `relaxed`, `normal`, `fast`.

O cabeçalho YAML não pode sobrescrever Guardian Specs. Em caso de conflito, Guardian Specs e Policy Engine prevalecem.

## Ordem de precedência de políticas

O Model Selection Engine deve resolver políticas nesta ordem:

1. Guardian Specs.
2. Políticas explícitas de segurança, privacidade e compliance do projeto.
3. Orçamento da missão, projeto ou período.
4. Cabeçalho YAML do arquivo ou artefato.
5. Política do workflow.
6. Política do agente ou subagente.
7. Perfil padrão do projeto.
8. Defaults seguros do framework.

Quando houver conflito, a política mais restritiva deve prevalecer.

## Estratégia de seleção

O Model Selection Engine deve avaliar candidatos por etapas:

1. Descobrir modelos disponíveis via Model Registry e adapters ativos.
2. Remover modelos indisponíveis, desabilitados, depreciados ou incompatíveis.
3. Aplicar restrições de segurança, privacidade e compliance.
4. Aplicar restrições de orçamento e custo.
5. Aplicar requisitos de contexto, ferramentas, structured output e modalidade.
6. Classificar modelos por adequação à tarefa.
7. Preferir o menor custo que satisfaça qualidade mínima.
8. Preferir `small_model` para tarefas simples quando permitido.
9. Montar cadeia de fallback compatível.
10. Emitir decisão auditável.

## `small_model`

O framework deve suportar a política `small_model` para tarefas de baixa complexidade.

Usos típicos:

- classificação simples;
- roteamento de intenção;
- sumarização curta;
- extração estruturada simples;
- transformação de texto;
- validações mecânicas;
- geração de títulos, labels ou metadados;
- pré-análise antes de escalar para modelo maior.

Regras:

1. `small_model` deve ser preferido quando `complexity` for `low` e `quality` não exigir `maximum`.
2. `small_model` não deve ser usado para decisões críticas de segurança sem validação posterior.
3. `small_model` pode ser usado como primeira etapa de triagem em loops controlados.
4. Resultado de `small_model` deve poder escalar para modelo superior quando houver baixa confiança.
5. `small_model` deve respeitar os mesmos controles de segurança e privacidade.

## Fallback

O fallback deve ser uma cadeia ordenada de alternativas compatíveis.

Exemplo conceitual:

```yaml
fallback_chain:
  - provider: preferred_paid_provider
    model: high_quality_model
  - provider: local_provider
    model: best_available_local_model
  - provider: free_provider
    model: best_available_free_model
```

Regras:

1. Fallback não pode violar política de privacidade ou segurança.
2. Fallback pago não pode ser usado quando `cost` for `strict_free`.
3. Fallback local deve ser preferido quando `privacy` for `local_preferred`.
4. Fallback externo deve ser proibido quando `privacy` for `local_required`.
5. Se nenhum modelo cumprir requisitos mínimos, a execução deve falhar com erro explicável.
6. Se a qualidade cair abaixo do mínimo exigido, a execução deve exigir revisão humana ou modelo superior.
7. Fallback deve registrar motivo da troca quando possível.

## Custo

O Model Selection Engine deve tratar custo como política de primeira classe.

Perfis mínimos:

- `economy`: prioriza modelos locais, gratuitos ou baratos;
- `balanced`: equilibra custo e qualidade;
- `premium`: permite modelos pagos de alta qualidade quando necessário;
- `strict_free`: proíbe modelos pagos.

Regras:

1. Modelos gratuitos ou locais devem ser preferidos para tarefas simples.
2. Modelos pagos devem exigir política permissiva ou justificativa de complexidade.
3. Orçamentos por missão, projeto ou período devem ser respeitados quando definidos.
4. Custo estimado deve considerar input, output e chamadas auxiliares quando possível.
5. Chamadas repetidas ao mesmo contexto devem reutilizar cache quando permitido.
6. Quando custo real não estiver disponível, o engine deve registrar limitação de estimativa.

## Qualidade

O Model Selection Engine deve considerar qualidade como restrição explícita.

Regras:

1. Tarefas críticas devem usar modelos compatíveis com qualidade mínima alta ou revisão obrigatória.
2. Tarefas arquiteturais, segurança, compliance e decisões irreversíveis devem exigir revisão quando a confiança for insuficiente.
3. Cross-review por outro modelo deve ser possível quando a Guardian Spec de AI Quality Assurance exigir.
4. Modelos pequenos podem produzir rascunhos, mas não devem aprovar entregas críticas sozinhos.
5. Decisões devem ser validáveis com fontes, testes, critérios de aceite ou revisão humana.

## Segurança e privacidade

O Model Selection Engine deve aplicar Security by Design antes de custo ou conveniência.

Regras:

1. Segredos não devem ser enviados a modelos externos.
2. Conteúdo sensível deve respeitar política de privacidade do projeto.
3. Conteúdo externo usado para seleção ou prompt deve passar por análise de risco de prompt injection quando aplicável.
4. Providers e MCPs devem ser tratados como superfície de ataque.
5. Modelos externos não devem receber dados classificados como locais obrigatórios.
6. A decisão deve indicar quando há risco de envio externo de contexto.
7. A seleção deve poder exigir aprovação humana antes de usar provider pago ou externo em contexto sensível.

## Token Efficiency

O Model Selection Engine deve reduzir consumo de tokens sem degradar a qualidade final.

Regras:

1. Selecionar modelo com janela de contexto adequada, não necessariamente a maior.
2. Evitar envio redundante de contexto.
3. Preferir recuperação seletiva e compressão semântica antes de escalar modelo.
4. Usar modelos pequenos para pré-processamento quando isso reduzir custo total.
5. Registrar tokens estimados ou reais quando possível.
6. Considerar custo total do workflow, não apenas custo de uma chamada isolada.

## Integração arquitetural

O Model Selection Engine se posiciona abaixo do Policy Engine e acima dos Provider Adapters.

Fluxo conceitual:

```text
Mission
↓
Workflow Engine
↓
Agent Orchestrator
↓
Policy Engine
↓
Model Selection Engine
↓
Provider Adapters
↓
Runtimes / LLM Providers
```

Agentes não devem chamar providers diretamente para escolher modelos.

Agentes devem declarar intenção, capacidade necessária e restrições. O Model Selection Engine decide o modelo por política e estratégia.

## OpenCode Adapter inicial

O OpenCode Adapter pode ser o primeiro adapter de runtime para:

- listar modelos disponíveis no runtime atual;
- expor providers configurados;
- indicar modelo ativo;
- executar chamadas conforme decisão do engine;
- reportar falhas de disponibilidade;
- capturar metadados básicos de uso quando possível.

Restrições:

1. O Model Selection Engine não deve depender de APIs internas específicas do OpenCode sem adapter.
2. Decisões de política não devem ser codificadas dentro do OpenCode Adapter.
3. O framework deve permitir futuros adapters para Claude Code, Codex CLI, Cursor, VS Code, JetBrains, Web UI e API.

## Observabilidade e auditoria

O Model Selection Engine deve registrar, quando possível:

- tarefa ou missão associada;
- política aplicada;
- modelos candidatos considerados;
- modelo selecionado;
- fallback usado;
- custo estimado ou real;
- tokens estimados ou reais;
- motivo da decisão;
- motivo de falha;
- necessidade de revisão;
- alertas de segurança ou privacidade.

Logs não podem conter segredos nem contexto sensível desnecessário.

## Erros e degradação

O Model Selection Engine deve produzir erros claros para:

- nenhum modelo disponível;
- nenhum modelo compatível com segurança;
- orçamento insuficiente;
- provider indisponível;
- política conflitante;
- contexto maior que janela disponível;
- modelo solicitado explicitamente inexistente;
- uso pago não autorizado;
- uso externo proibido por privacidade.

Quando possível, o erro deve sugerir alternativas seguras, como reduzir contexto, permitir fallback, usar modelo local ou solicitar aprovação humana.

## Decisões aprovadas por esta Spec

1. O Model Selection Engine é componente arquitetural próprio do framework.
2. OpenCode será tratado como adapter inicial, não como núcleo.
3. O engine deve ser provider agnostic.
4. Políticas podem vir de cabeçalhos YAML, mas Guardian Specs prevalecem.
5. `small_model` será política explícita para tarefas simples.
6. Modelos gratuitos, locais e pagos devem ser tratados no mesmo modelo conceitual.
7. Fallback deve ser seguro, auditável e compatível com custo, qualidade e privacidade.
8. Custo, qualidade, segurança e tokens são critérios obrigatórios de seleção.
9. A decisão de modelo deve ser justificável.
10. Falhas de seleção devem ser explícitas e seguras.

## Estado implementado e validado em 0108

O MVP implementado em `src/vercosa_ai_framework/model_selection/` usa catálogo em memória injetado e seleção por `ModelSelectionPolicy`. O fluxo 0107 propaga `ResolvedPolicySet` para excluir modelos por política e usa requisitos do `ContextPackage` para influenciar a janela mínima de contexto antes da chamada ao Runtime Adapter.

Evidências:

- `tests/test_model_selection.py` cobre seleção local em memória e falhas explícitas.
- `tests/test_policy_model_selection_integration.py` cobre aplicação de política resolvida na seleção.
- `tests/test_token_budget_model_selection_integration.py` cobre influência de orçamento/contexto na seleção.
- `tests/test_agent_execution_governance_0107.py` valida que seleção ocorre antes do runtime, que modelo incompatível bloqueia execução e que política `DENY` exclui modelo.

No estado atual, Model Selection não chama provider nem runtime diretamente, não descobre modelos reais em providers externos e não executa fallback externo real. Aprovação exigida por política bloqueia execução automática quando não há aprovação representada no fluxo.

## Critérios de aceite

- Existe uma Spec própria para o Model Selection Engine.
- A Spec define o engine sem acoplamento a OpenCode ou provider específico.
- A Spec contempla fallback entre modelos e providers.
- A Spec contempla modelos gratuitos, locais e pagos.
- A Spec contempla custo, orçamento e perfis `economy`, `balanced`, `premium` e `strict_free`.
- A Spec contempla qualidade, revisão e cross-review quando necessário.
- A Spec contempla `small_model`.
- A Spec define campos mínimos para cabeçalho YAML por arquivo.
- A Spec define precedência entre Guardian Specs, políticas de projeto, missão, arquivo, workflow e agente.
- A Spec respeita Security by Design.
- A Spec respeita Token Efficiency.
- A Spec respeita Cost Optimization.
- A Spec respeita AI Quality Assurance.
- A Spec define OpenCode apenas como adapter inicial.
- A Spec define erros e degradação segura.
- A Spec define observabilidade sem expor segredos.

## Pendências

- Definir formato persistente do Model Registry.
- Definir schema definitivo para Model Profile.
- Definir como medir qualidade empiricamente por família de tarefa.
- Definir integração com orçamento real de providers pagos.
- Definir política de cache semântico para decisões de seleção.
- Definir ADR para fronteira entre AI Orchestrator, Policy Engine e Model Selection Engine se houver divergência arquitetural futura.

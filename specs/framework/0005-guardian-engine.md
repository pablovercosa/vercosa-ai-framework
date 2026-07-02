# Spec 0005 — Guardian Engine

## Status

Proposta.

## Objetivo

Definir o Guardian Engine do Vercosa AI Framework como o componente responsável por avaliar missões, ações planejadas, comandos, uso de contexto, orçamento, riscos e validações antes e durante a execução.

O Guardian Engine deve transformar Guardian Specs, políticas de projeto e restrições de missão em decisões explícitas: `allow`, `warn`, `block` ou `require_approval`.

## Contexto

O Vercosa AI Framework é Specification First, AI Native, Provider Agnostic, Local First, Extensible by Design, Security by Design, Token Efficient e Governance by Design.

As Specs 0001 e 0004 estabelecem que:

- Guardian Specs governam todos os projetos;
- nenhuma implementação deve violar Guardian Specs;
- missões devem ser unidades rastreáveis, auditáveis e executadas em ciclos finitos;
- o Mission Runner deve aplicar limites, orçamento, validação, logs e políticas de segurança;
- runtimes concretos devem ser acessados por adapters;
- o framework não deve assumir sistema operacional, arquitetura, banco, modelo, provider ou IDE específicos.

O Guardian Engine é a camada que toma e explica decisões de política. Ele não executa missões, não executa comandos, não seleciona modelos diretamente e não substitui o Mission Runner, o Policy Engine, o Model Selection Engine ou Runtime Adapters.

## Escopo

Esta Spec cobre:

- validação de missões antes da execução;
- aplicação de Security by Design;
- aplicação de Token Efficiency;
- aplicação de Cost Optimization;
- aplicação de AI Quality Assurance;
- comandos proibidos;
- comandos que exigem confirmação;
- detecção de segredos;
- limite de custo e tokens;
- limite de ciclos;
- classificação de risco por missão;
- decisões `allow`, `warn`, `block` e `require_approval`;
- integração com Mission Runner;
- integração futura com Runtime Adapter;
- logs de decisão;
- explicabilidade da decisão;
- modos permissivo, padrão e estrito;
- critérios de aceite.

Esta Spec não cobre:

- implementação concreta em código;
- criação de CLI, daemon, serviço `systemd` ou API real;
- alteração de configurações globais;
- uso de `sudo`;
- schema final de banco de dados;
- engine final de regras;
- integração real com ferramentas externas de secret scanning;
- seleção concreta de modelos;
- execução direta de comandos, tools, MCPs ou providers.

## Princípios

1. Guardian Specs prevalecem sobre políticas locais, preferências de usuário e conveniência operacional.
2. Toda missão deve ser avaliada antes da execução.
3. Ações sensíveis devem ser avaliadas antes de serem entregues ao runtime.
4. Em caso de conflito, a decisão mais restritiva deve prevalecer.
5. Decisões devem ser explícitas, auditáveis e explicáveis.
6. Segredos não devem ser expostos em prompts, logs, commits, respostas ou providers externos.
7. Custo, tokens e ciclos são restrições de primeira classe.
8. Tarefas críticas exigem validação proporcional ao risco.
9. O modo padrão deve ser seguro sem impedir trabalho normal de engenharia.
10. O Guardian Engine decide política; execução pertence ao Mission Runner e aos Runtime Adapters.

## Posição arquitetural

O Guardian Engine fica na camada de governança entre Mission Runner, Policy Engine e componentes de execução.

Fluxo conceitual:

```text
Mission Request
↓
Mission Runner
↓
Guardian Engine
↓
Policy Engine
↓
Mission Orchestrator / Workflow Engine
↓
Agent Orchestrator
↓
Runtime Adapter
```

Antes de iniciar uma missão, o Mission Runner deve solicitar uma decisão ao Guardian Engine.

Durante a execução, o Mission Runner ou Runtime Adapter futuro deve solicitar nova decisão para ações sensíveis, comandos, uso de contexto, mudanças de orçamento, replanejamentos, acessos a arquivos sensíveis, providers externos e alterações de escopo.

## Definições

### Guardian Engine

Componente responsável por avaliar entradas, planos e ações contra Guardian Specs e políticas aplicáveis.

Responsabilidades:

- resolver políticas relevantes para uma missão;
- validar se a missão possui Spec aprovada quando necessário;
- classificar risco da missão;
- avaliar comandos planejados;
- detectar indícios de segredos;
- aplicar limites de tokens, custo e ciclos;
- exigir confirmação para ações sensíveis;
- bloquear ações proibidas;
- emitir decisões estruturadas;
- gerar justificativa explicável;
- registrar logs de decisão sem expor dados sensíveis.

Não responsabilidades:

- executar comandos;
- editar arquivos;
- escolher modelos diretamente;
- aprovar Specs;
- substituir revisão humana obrigatória;
- alterar configurações globais;
- usar `sudo`;
- ignorar Runtime Adapters;
- persistir segredos em logs.

### Policy Decision

Resultado estruturado de uma avaliação do Guardian Engine.

Decisões possíveis:

- `allow`: a ação pode prosseguir sem intervenção adicional;
- `warn`: a ação pode prosseguir, mas deve registrar aviso e evidência;
- `block`: a ação não pode prosseguir;
- `require_approval`: a ação depende de aprovação humana ou aprovação explícita por política autorizada.

### Mission Risk

Classificação de risco agregada de uma missão.

Níveis mínimos:

- `low`: alteração documental, leitura não sensível ou tarefa reversível sem impacto externo;
- `medium`: alteração de código, execução local limitada, uso moderado de tokens ou custo, ou mudança com validação automatizada;
- `high`: mudança em segurança, infraestrutura, dependências, dados, autenticação, permissões, custos pagos, providers externos ou comandos potencialmente destrutivos;
- `critical`: ação irreversível, risco de perda de dados, exposição de segredos, alteração global, execução privilegiada, produção, compliance ou alto custo.

### Guardian Mode

Perfil operacional que ajusta tolerância a risco.

Modos mínimos:

- `permissive`: permite mais ações com avisos, mas nunca permite violações críticas de Guardian Specs;
- `standard`: modo padrão, equilibrado entre segurança e produtividade;
- `strict`: exige aprovação ou bloqueio para qualquer ação sensível, ambígua, externa, destrutiva ou com risco elevado.

## Entrada de avaliação

Toda avaliação deve receber contexto mínimo suficiente, sem excesso de tokens.

Campos mínimos desejados:

- `mission_id`;
- `evaluation_id`;
- `evaluation_type`;
- `guardian_mode`;
- `mission_goal`;
- `spec_refs`;
- `guardian_refs`;
- `workspace`;
- `requested_action`;
- `planned_command` quando aplicável;
- `target_paths` quando aplicável;
- `data_sensitivity` quando conhecida;
- `network_policy`;
- `provider_policy`;
- `budget_policy`;
- `execution_limits`;
- `current_cycle`;
- `risk_overrides` quando aprovados;
- `prior_decision_refs` quando houver.

Regras:

1. A entrada deve conter referências a artefatos em vez de copiar contexto extenso quando possível.
2. Conteúdo sensível deve ser omitido, mascarado ou substituído por metadados.
3. Arquivos binários devem ser tratados como artefatos a canonicalizar antes de análise textual.
4. Avaliações incrementais devem reutilizar decisões anteriores quando aplicável.

## Saída de avaliação

Toda avaliação deve produzir uma decisão estruturada.

Campos mínimos desejados:

- `evaluation_id`;
- `mission_id`;
- `decision`;
- `risk_level`;
- `guardian_mode`;
- `matched_policies`;
- `reasons`;
- `required_actions`;
- `approval_requirements` quando aplicável;
- `blocked_items` quando aplicável;
- `warnings`;
- `safe_alternatives`;
- `limits_applied`;
- `redactions_applied`;
- `created_at`;
- `expires_at` quando aplicável.

Regras:

1. A decisão deve ser determinística o suficiente para auditoria.
2. A decisão deve explicar quais políticas foram relevantes.
3. A decisão não deve conter segredos.
4. `block` deve incluir motivo e alternativa segura quando possível.
5. `require_approval` deve declarar exatamente o que precisa ser aprovado.
6. Decisões sensíveis podem expirar para evitar reuso indevido.

## Validação de missões antes da execução

O Guardian Engine deve avaliar toda missão antes que o Mission Runner mude seu estado para `running`.

Validações mínimas:

- existência de objetivo claro;
- entregáveis esperados;
- restrições declaradas;
- critérios de aceite proporcionais ao risco;
- limite de ciclos ou default seguro;
- orçamento de tokens e custo ou default seguro;
- política de validação;
- política de segurança;
- referências a Specs quando a missão pedir implementação;
- confirmação de que a missão não exige alteração global não autorizada;
- confirmação de que a missão não exige `sudo`;
- avaliação de risco inicial.

Regras:

1. Missões de implementação devem exigir Spec aprovada.
2. Missões sem limite de ciclos devem receber default seguro ou ser bloqueadas.
3. Missões sem orçamento devem receber default seguro ou exigir aprovação conforme modo.
4. Missões que envolvam produção, dados sensíveis, infraestrutura, autenticação, pagamentos ou compliance devem ser classificadas no mínimo como `high`.
5. Missões ambíguas devem retornar `warn`, `require_approval` ou `block`, conforme risco e modo.

## Security by Design

O Guardian Engine deve aplicar Security by Design como gate obrigatório.

Controles mínimos:

- secret scanning conceitual em prompts, planos, comandos, diffs e logs;
- bloqueio de exposição de segredos;
- confirmação antes de ler `.env` ou arquivos de credenciais;
- bloqueio de `sudo` por padrão;
- bloqueio de comandos destrutivos sem aprovação explícita;
- avaliação de MCPs, plugins, tools e providers como superfície de ataque;
- análise de risco de dependências e supply chain quando houver alteração de dependências;
- revisão de prompt injection quando houver conteúdo externo;
- revisão de permissões para agentes;
- registro de toda decisão de risco.

Regras:

1. Segredos detectados devem ser mascarados antes de logs ou respostas.
2. Segredos não devem ser enviados a providers externos.
3. `.env`, chaves privadas, tokens e credenciais exigem `require_approval` para leitura e `block` para exposição.
4. Alterações globais devem ser `block` por padrão ou `require_approval` quando houver política explícita.
5. Ações com risco de perda de dados devem ser `require_approval` ou `block`.

## Token Efficiency

O Guardian Engine deve aplicar Token Efficiency antes de permitir uso de contexto ou ciclos adicionais.

Controles mínimos:

- rejeitar contexto redundante quando detectável;
- preferir referências, resumos e recuperação seletiva;
- exigir canonicalização de binários para Markdown antes de uso por agentes;
- limitar tokens por missão e por ciclo;
- sugerir divisão de missão quando o contexto exceder limite;
- preferir modelos locais ou gratuitos para tarefas simples quando compatível com política;
- registrar estimativas e uso real quando disponível.

Regras:

1. Aumento de contexto deve ser justificado por necessidade da missão.
2. Reenvio repetido do mesmo contexto deve gerar `warn` ou `block`, conforme impacto.
3. Exceder limite de tokens deve gerar `block` ou `require_approval`.
4. Otimização de contexto deve ser tentada antes de aumentar orçamento.

## Cost Optimization

O Guardian Engine deve aplicar orçamento como restrição obrigatória.

Campos mínimos de política:

- `cost_profile`: `economy`, `balanced` ou `premium`;
- `max_cost_per_mission`;
- `max_cost_per_cycle`;
- `max_tokens_per_mission`;
- `max_tokens_per_cycle`;
- `paid_provider_allowed`;
- `external_provider_allowed`;
- `budget_exhaustion_action`.

Regras:

1. Uso pago exige política permissiva ou aprovação.
2. Provider externo exige política permissiva e compatibilidade com privacidade.
3. Ao atingir orçamento, a decisão deve ser `block` ou `require_approval`.
4. Se custo real não estiver disponível, a decisão deve registrar que usou estimativa.
5. Fallback pago não pode ocorrer por conveniência.
6. Fallback gratuito ou local deve ser preferido quando atender qualidade mínima.

## AI Quality Assurance

O Guardian Engine deve exigir validação proporcional ao risco.

Controles mínimos:

- critérios de aceite para Specs e missões;
- testes ou validação aplicável para código;
- revisão humana para baixa confiança ou alto risco;
- cross-review por outro agente ou modelo quando política exigir;
- condição de parada para loops;
- evidências auditáveis de resultado;
- ADR para decisões arquiteturais relevantes.

Regras:

1. Missões críticas devem exigir revisão.
2. Código não deve ser considerado concluído sem validação aplicável ou justificativa registrada.
3. Specs devem conter critérios de aceite.
4. Loops sem condição de parada devem ser bloqueados.
5. Baixa confiança deve gerar `require_approval`.

## Comandos proibidos

O Guardian Engine deve manter uma categoria de comandos proibidos por padrão.

Categorias proibidas:

- execução privilegiada não autorizada;
- destruição ampla de arquivos ou diretórios;
- alteração global de sistema sem Spec e aprovação explícita;
- exfiltração de segredos;
- alteração de histórico git destrutiva sem pedido explícito;
- desativação de controles de segurança;
- instalação ou execução de binários remotos sem avaliação;
- operação direta em produção sem política específica.

Exemplos que devem resultar em `block` por padrão:

```text
sudo ...
su ...
rm -rf /
rm -rf ~
rm -rf .git
chmod -R 777 /
chown -R ... /
git reset --hard
git clean -fdx
git push --force
curl ... | sh
wget ... | sh
ssh ... comando-destrutivo
docker system prune -a
DROP DATABASE ...
TRUNCATE ...
```

Regras:

1. A lista é mínima, não exaustiva.
2. O Guardian Engine deve avaliar intenção, argumentos, paths e contexto.
3. Comandos equivalentes, aliases ou variações devem receber a mesma decisão.
4. Um comando proibido só pode deixar de ser bloqueado por política futura específica, aprovada e auditável, nunca por decisão implícita.

## Comandos que exigem confirmação

O Guardian Engine deve classificar comandos sensíveis como `require_approval` quando não forem proibidos.

Categorias que exigem confirmação:

- leitura de `.env`, chaves privadas, tokens ou credenciais;
- remoção de arquivos fora do conjunto de artefatos da missão;
- alteração de permissões em massa;
- instalação, atualização ou remoção de dependências;
- execução de migrações;
- comandos Docker que removem imagens, volumes, containers ou redes;
- comandos Git que alteram histórico ou descartam mudanças;
- acesso a rede externa quando a política não for clara;
- uso de provider externo com dados do projeto;
- comandos que possam gerar custo financeiro;
- alteração de configuração global de ferramentas;
- escrita fora do workspace.

Regras:

1. A confirmação deve ser específica para ação, alvo e risco.
2. Aprovação genérica não deve autorizar ações futuras diferentes.
3. Aprovação deve expirar ou ser limitada por missão, ciclo ou ação.
4. Se houver mudança de escopo, a ação deve ser reavaliada.

## Detecção de segredos

O Guardian Engine deve detectar indícios de segredos em entradas, planos, comandos, diffs, logs e artefatos.

Tipos mínimos:

- tokens de API;
- senhas;
- chaves privadas;
- certificados;
- cookies de sessão;
- connection strings;
- credenciais de banco;
- credenciais de cloud;
- webhooks sensíveis;
- arquivos `.env`;
- arquivos de configuração com credenciais embutidas.

Regras:

1. Detecção positiva deve gerar mascaramento imediato em logs.
2. Exposição de segredo deve gerar `block`.
3. Leitura de segredo deve gerar `require_approval`, exceto quando política específica permitir leitura local controlada.
4. Envio de segredo para provider externo deve gerar `block`.
5. Falsos positivos devem ser registráveis como exceção aprovada, sem expor o valor original.

## Limites de custo, tokens e ciclos

O Guardian Engine deve avaliar limites antes do início da missão e antes de cada ciclo.

Limites mínimos:

- `max_cycles_per_mission`;
- `max_cycles_per_task`;
- `max_replans`;
- `max_validation_failures`;
- `max_retries`;
- `max_tokens_per_mission`;
- `max_tokens_per_cycle`;
- `max_cost_per_mission`;
- `max_cost_per_cycle`;
- `max_wall_clock_time` quando disponível.

Regras:

1. Limites ausentes devem receber default seguro ou gerar `require_approval`.
2. Limites excedidos devem gerar `block` ou `require_approval`.
3. Replanejamento não deve resetar limites.
4. Retry deve consumir limite conforme política registrada.
5. O modo estrito deve preferir `block` quando limites forem ambíguos.

## Risco por missão

O Guardian Engine deve calcular risco inicial e atualizar risco quando plano, contexto ou ações mudarem.

Fatores mínimos:

- tipo de entrega;
- paths afetados;
- sensibilidade dos dados;
- uso de rede;
- uso de provider externo;
- uso pago;
- comandos planejados;
- dependências afetadas;
- permissões requeridas;
- reversibilidade;
- impacto em usuário, produção, infraestrutura ou segurança;
- maturidade da Spec;
- cobertura de validação;
- confiança do agente ou modelo quando disponível.

Regras:

1. Risco pode aumentar durante a missão.
2. Risco não deve diminuir sem evidência.
3. Risco `high` ou `critical` deve exigir validação reforçada.
4. Risco `critical` deve exigir aprovação humana ou bloqueio, conforme política.

## Modos de operação

### Permissive

Modo adequado para exploração local de baixo risco.

Regras:

- permite mais ações com `warn`;
- ainda bloqueia segredos, `sudo` não autorizado, exfiltração e destruição ampla;
- exige aprovação para custo pago, providers externos e ações destrutivas;
- registra avisos detalhados.

### Standard

Modo padrão.

Regras:

- bloqueia ações proibidas;
- exige aprovação para ações sensíveis;
- aplica limites seguros de ciclos, custo e tokens;
- exige validação proporcional ao risco;
- trata ambiguidades relevantes como `require_approval`.

### Strict

Modo adequado para segurança elevada, compliance, produção ou dados sensíveis.

Regras:

- trata ambiguidades como `block` ou `require_approval`;
- exige aprovação para providers externos, custo pago e leitura sensível;
- bloqueia escrita fora do workspace;
- exige logs mais completos, ainda sem segredos;
- exige validação reforçada para risco `medium` ou superior.

## Integração com Mission Runner

O Mission Runner deve consultar o Guardian Engine nos seguintes pontos mínimos:

- criação ou registro da missão;
- antes de `queued -> running`;
- antes de cada ciclo;
- antes de executar comando sensível;
- antes de ampliar contexto;
- antes de usar provider externo;
- antes de consumir orçamento adicional;
- antes de replanejar além de limites;
- antes de marcar missão como `done`;
- antes de `auto_commit` quando existir política aplicável.

Contrato conceitual:

```text
Mission Runner
↓ evaluation request
Guardian Engine
↓ policy decision
Mission Runner
↓ execute, pause, fail or request approval
```

Regras:

1. O Mission Runner não deve executar missão bloqueada.
2. `require_approval` deve pausar a missão ou ciclo até decisão autorizada.
3. `warn` deve registrar aviso e permitir prosseguimento conforme política.
4. `allow` não remove obrigação de validação futura.
5. O Mission Runner deve anexar decisões do Guardian Engine aos logs da missão.

## Integração futura com Runtime Adapter

Runtime Adapters devem consultar ou receber decisões do Guardian Engine antes de executar ações no ambiente concreto.

Uso futuro esperado:

- validação de comando shell antes de execução;
- validação de leitura ou escrita de arquivos;
- validação de chamadas a tools, MCPs e providers;
- validação de operações de rede;
- validação de ações Git;
- redaction de logs gerados pelo runtime;
- enforcement de permissões efetivas.

Regras arquiteturais:

1. Runtime Adapter não deve fazer bypass do Guardian Engine.
2. Runtime Adapter pode aplicar bloqueios adicionais específicos do ambiente.
3. Runtime Adapter deve retornar evidências suficientes para logs sem expor segredos.
4. O Guardian Engine deve permanecer provider agnostic e runtime agnostic.
5. Políticas específicas de OpenCode, Claude Code, Codex CLI, IDEs, API ou Web UI devem ser adapters ou perfis, não núcleo.

## Logs de decisão

O Guardian Engine deve registrar decisões suficientes para auditoria.

Eventos mínimos:

- avaliação solicitada;
- políticas carregadas;
- decisão emitida;
- risco calculado;
- comandos bloqueados ou aprovados;
- confirmação exigida;
- aprovação concedida ou negada;
- segredo detectado e mascarado;
- limite aplicado;
- orçamento estimado ou consumido;
- exceção aprovada;
- expiração de decisão;
- erro de avaliação.

Regras:

1. Logs não podem conter segredos.
2. Logs devem preferir hashes, paths, metadados e referências a artefatos.
3. Prompts completos só podem ser registrados quando política permitir.
4. Justificativas devem ser legíveis para revisão humana.
5. Logs devem ser vinculáveis a `mission_id`, `cycle_number` e `evaluation_id`.

## Explicabilidade da decisão

Toda decisão deve ser explicável em linguagem humana e rastreável a políticas.

Explicação mínima:

- decisão final;
- nível de risco;
- políticas aplicadas;
- fatores de risco relevantes;
- limites considerados;
- motivo de bloqueio ou aprovação;
- ação exigida do usuário quando houver;
- alternativa segura quando possível.

Regras:

1. Explicação não deve vazar segredo ou conteúdo sensível.
2. Explicação deve ser curta por padrão e detalhável sob demanda.
3. Decisões `block` e `require_approval` exigem explicação obrigatória.
4. Decisões repetidas podem referenciar avaliação anterior para economia de tokens.

## Erros e degradação segura

O Guardian Engine deve degradar de forma segura.

Erros que devem impedir prosseguimento ou exigir aprovação:

- Guardian Specs indisponíveis;
- política conflitante;
- falha de secret scanning;
- orçamento desconhecido em ação paga;
- runtime incapaz de aplicar bloqueio;
- classificação de risco inconclusiva;
- logs de decisão indisponíveis para missão de alto risco;
- tentativa de reuso de decisão expirada;
- comando não classificável com segurança.

Regras:

1. Falha em avaliação de segurança deve tender a `block`.
2. Falha em estimativa de custo deve tender a `require_approval` ou `block`.
3. Falha em log deve bloquear missões de alto risco.
4. Alternativa segura deve ser sugerida quando possível.

## Riscos e mitigações

| Risco | Mitigação |
| --- | --- |
| Bloqueio excessivo de produtividade | Modos permissivo, padrão e estrito com explicação e alternativas seguras. |
| Falso negativo em segredo | Secret scanning em múltiplos pontos e bloqueio de exposição externa. |
| Falso positivo em segredo | Exceção aprovada sem registrar valor sensível. |
| Bypass por Runtime Adapter | Contrato obrigatório de consulta ou enforcement de decisão. |
| Acoplamento a OpenCode | Políticas específicas ficam em adapter ou perfil, não no núcleo. |
| Custo inesperado | Orçamento por missão e ciclo com bloqueio ou aprovação. |
| Loops infinitos | Limites obrigatórios e condição de parada. |
| Decisão inexplicável | Saída estruturada com políticas, motivos e alternativas. |
| Logs vazando dados | Redaction obrigatória e preferência por metadados. |
| Política ambígua | Política mais restritiva prevalece. |

## Decisões aprovadas por esta Spec

1. Guardian Engine é componente arquitetural próprio do framework.
2. Toda missão deve ser avaliada pelo Guardian Engine antes da execução.
3. O Guardian Engine deve emitir decisões `allow`, `warn`, `block` ou `require_approval`.
4. O Guardian Engine deve classificar risco por missão como `low`, `medium`, `high` ou `critical`.
5. O Guardian Engine deve suportar modos `permissive`, `standard` e `strict`.
6. Security by Design, Token Efficiency, Cost Optimization e AI Quality Assurance são gates obrigatórios de avaliação.
7. Comandos proibidos devem ser bloqueados por padrão.
8. Comandos sensíveis devem exigir confirmação.
9. Detecção e mascaramento de segredos são obrigatórios.
10. Limites de custo, tokens e ciclos devem ser avaliados antes e durante execução.
11. Mission Runner deve consultar Guardian Engine nos pontos críticos do ciclo de vida da missão.
12. Runtime Adapters futuros não devem fazer bypass do Guardian Engine.
13. Toda decisão deve gerar log auditável e explicação sem expor segredos.

## Critérios de aceite

- Existe uma Spec própria para o Guardian Engine.
- A Spec define validação de missões antes da execução.
- A Spec cobre Security by Design.
- A Spec cobre Token Efficiency.
- A Spec cobre Cost Optimization.
- A Spec cobre AI Quality Assurance.
- A Spec define comandos proibidos.
- A Spec define comandos que exigem confirmação.
- A Spec define detecção de segredos.
- A Spec define limite de custo e tokens.
- A Spec define limite de ciclos.
- A Spec define risco por missão.
- A Spec define decisões `allow`, `warn`, `block` e `require_approval`.
- A Spec define integração com Mission Runner.
- A Spec define integração futura com Runtime Adapter.
- A Spec define logs de decisão.
- A Spec define explicabilidade da decisão.
- A Spec define modos permissivo, padrão e estrito.
- A Spec não implementa código.
- A Spec não exige alteração de configurações globais.
- A Spec não exige uso de `sudo`.

## Pendências

- Definir formato persistente final de `Policy Decision`.
- Definir engine concreta de regras.
- Definir defaults numéricos para tokens, custo e ciclos por tipo de missão.
- Definir taxonomia final de comandos proibidos por sistema operacional.
- Definir contrato formal entre Guardian Engine e Policy Engine.
- Definir contrato formal entre Guardian Engine e Runtime Adapters.
- Definir formato de aprovação humana.
- Definir integração futura com ferramentas reais de secret scanning.
- Definir política de retenção de logs de decisão.
- Definir perfis padrão por tipo de projeto.

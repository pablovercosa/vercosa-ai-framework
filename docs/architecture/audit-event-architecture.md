# Arquitetura De Audit/Event Log

Links principais: [README do módulo audit](../../src/vercosa_ai_framework/audit/README.md) | [Índice de módulos](module-index.md) | [Mapa de arquitetura](../alignment/architecture-map.md) | [Exemplos operacionais](../examples/README.md)

## Objetivo

Documentar o papel arquitetural do Audit/Event Log no Vercosa AI Framework, seus contratos atuais, categorias, severidades, resultados, integrações iniciais, limites de segurança e próximos passos possíveis.

Este documento descreve a arquitetura atual e a direção de evolução. Ele não autoriza implementação de persistência externa, banco de dados, OpenTelemetry, dashboard, exportador ou integração automática adicional.

## Propósito

O Audit/Event Log fornece uma fundação estruturada para registrar eventos internos relevantes do framework. Seu papel é preservar rastreabilidade de decisões, ciclos de missão, políticas, avaliações Guardian, montagem de contexto, limites operacionais e resultados importantes sem depender de logs textuais livres.

Em um framework de Harness Engineering, auditoria é necessária porque o valor do sistema não está apenas na resposta de um modelo. O harness precisa registrar quais políticas foram consideradas, quais decisões bloquearam ou permitiram ações, qual contexto foi selecionado ou omitido, quais limites operacionais foram detectados e quais etapas de missão ocorreram. Sem eventos estruturados, debugging, governança, revisão de segurança, explicabilidade futura e reprodução de decisões ficam frágeis.

O Audit/Event Log atual é uma fundação inicial. Ele não é uma plataforma completa de observabilidade.

## Diferenças De Registro

Log textual operacional é saída livre voltada para leitura humana imediata. Exemplos incluem mensagens de terminal, logs dos scripts operacionais e linhas textuais em arquivos de execução. Esse tipo de log ajuda diagnóstico local, mas não possui contrato forte de campos, categorias ou resultados.

Evento auditável estruturado é um `AuditEvent` com campos normalizados, categoria, severidade, resultado, origem e metadados seguros. Ele deve registrar fatos de alto nível, referências, contadores e sinais de decisão sem capturar conteúdo sensível bruto por padrão.

Telemetria externa futura seria integração com ferramentas de observabilidade, tracing, métricas ou sistemas externos. Ela ainda não existe no Vercosa AI Framework atual e não deve ser inferida a partir do `EventLog` em memória.

Persistência futura seria gravação durável dos eventos em arquivo local, JSONL, banco ou outro adapter aprovado. Ela ainda não existe para o Audit/Event Log. A implementação atual mantém eventos somente em memória durante o processo.

## Estado Atual

Status arquitetural: `contracts`.

Implementado atualmente:

- Tipos de evento em `types.py`.
- Porta `EventLog` em `event_log.py`.
- Implementação `InMemoryEventLog` em memória.
- Helpers opcionais para eventos de Policy Engine, Guardian Engine e Context Router em `integrations.py`.
- Helpers opcionais para eventos de ciclo de vida de missão e batch em `mission_events.py`.
- Integração opcional do `MissionRunner` Python com `EventLog` fornecido pelo chamador.

Futuro ou fora do escopo atual:

- Persistência externa.
- Banco de dados.
- SQLite.
- PostgreSQL.
- OpenTelemetry.
- Dashboard.
- Exportador.
- Correlação completa com Git.
- Retenção configurável.

## Contrato De Evento

Um evento auditável é representado por `AuditEvent`. Os campos principais são:

| Campo | Papel |
| --- | --- |
| `event_id` | Identificador do evento. Quando não informado, é gerado de forma determinística a partir dos dados normalizados do evento. |
| `category` | Categoria arquitetural do evento, como `mission`, `policy`, `guardian` ou `context`. |
| `name` | Nome específico do evento, por exemplo `policy.resolution` ou `mission.started`. |
| `severity` | Severidade operacional do evento. |
| `result` | Resultado representado pelo evento. |
| `message` | Mensagem curta e explicativa para leitura humana. |
| `source` | Origem lógica do evento, como `policy`, `guardian`, `context`, `missions` ou `framework`. |
| `metadata` | Metadados estruturados e seguros, preferencialmente refs, contadores e flags. |
| `created_at` | Timestamp opcional. Pode ser controlado pelo chamador para testes determinísticos. |

`event_id` e `created_at` precisam permanecer testáveis e previsíveis conforme o contrato implementado. O `event_id` usa hash determinístico quando os dados do evento são iguais. O `created_at` não é obrigatório e pode ser informado explicitamente por testes ou chamadores que precisem de timestamp controlado.

Exemplo conceitual de evento estruturado:

```json
{
  "event_id": "hash-deterministico",
  "category": "guardian",
  "name": "guardian.decision",
  "severity": "warning",
  "result": "requires_approval",
  "message": "Decisão do Guardian registrada de forma estruturada.",
  "source": "guardian",
  "metadata": {
    "mission_id": "mission-123",
    "decision": "require_approval",
    "requires_approval": true,
    "matched_policy_refs": ["policy.security.review"]
  },
  "created_at": "2026-07-07T00:00:00+00:00"
}
```

O exemplo mostra formato de dado. Ele não implica persistência em JSON, JSONL, arquivo ou banco no estado atual.

## Categorias

Categorias existentes no contrato:

| Categoria | Uso esperado |
| --- | --- |
| `mission` | Eventos de ciclo de vida de missão e batch. |
| `policy` | Resolução de políticas, conflitos, warnings e efeitos declarativos relevantes. |
| `guardian` | Decisões do Guardian Engine, bloqueios, avisos, aprovações requeridas e risco operacional. |
| `context` | Montagem de `ContextPackage`, itens selecionados, omissões, warnings e orçamento estimado. |
| `model_selection` | Seleção de modelo, fallback e restrições de orçamento. Categoria existente, integração específica ainda futura. |
| `runtime` | Planos e resultados de runtime. Categoria existente, integração específica ainda futura. |
| `provider` | Chamadas governadas e decisões no Provider Gateway. Categoria existente, integração específica ainda futura. |
| `usage_limit` | Sinais de quota, rate limit, billing ou limite externo. Categoria existente; integração como evento estruturado ainda é próxima etapa. |
| `system` | Eventos internos gerais do framework. |

## Severidades

Severidades existentes no contrato:

| Severidade | Uso esperado |
| --- | --- |
| `debug` | Diagnóstico detalhado e de baixo impacto. |
| `info` | Evento normal, esperado e bem-sucedido. |
| `warning` | Evento que exige atenção, mas não necessariamente falha. |
| `error` | Falha, bloqueio ou condição operacional relevante. |
| `critical` | Condição crítica que exige atenção imediata. |

## Resultados

Resultados existentes no contrato:

| Resultado | Uso esperado |
| --- | --- |
| `success` | Evento concluído sem falha relevante. |
| `skipped` | Etapa ou missão ignorada de forma explícita. |
| `warning` | Resultado com aviso, conflito leve ou degradação controlada. |
| `failed` | Falha operacional ou conclusão negativa. |
| `blocked` | Ação bloqueada por política, Guardian ou controle equivalente. |
| `requires_approval` | Continuação depende de aprovação humana ou política explícita. |

## Implementação Em Memória

`InMemoryEventLog` é a implementação atual da porta `EventLog`. Ela registra eventos em uma lista local do processo, preserva ordem determinística de inserção, retorna snapshots imutáveis como tuplas, permite filtros por categoria, severidade e resultado, e pode limpar eventos em memória.

A implementação em memória serve para:

- testes;
- contratos;
- composição futura;
- integração inicial;
- evitar dependências externas nesta fase.

Ela não grava arquivo, não acessa banco, não usa SQLite, não usa PostgreSQL, não exporta telemetria, não chama rede e não garante retenção após o fim do processo.

## Integrações Atuais

As integrações atuais são explícitas e opcionais. Módulos consumidores não devem depender obrigatoriamente do Event Log para funcionar, salvo decisão futura explícita em Spec ou ADR.

Policy Engine:

`policy_resolution_event()` e `record_policy_resolution_event()` transformam um `PolicyResolutionResult` já produzido em evento `policy.resolution`. O helper registra contadores, refs de políticas, conflitos, warnings, `deny` e `require_approval` sem registrar conteúdo bruto da política por padrão.

Guardian Engine:

`guardian_decision_event()` e `record_guardian_decision_event()` transformam uma `GuardianDecision` já produzida em evento `guardian.decision`. O helper registra decisão, risco, modo Guardian, bloqueios, violações, aprovação requerida, refs de políticas e contadores.

Context Router e `ContextPackage`:

`context_package_event()` e `record_context_package_event()` transformam um `ContextPackage` já montado em evento `context.package`. O helper registra quantidade de candidatos quando informada, itens selecionados, itens omitidos, estimativa de tokens, reserva de output, warnings, motivos agregados de omissão, refs de políticas e sinal de aprovação requerida.

Mission Runner:

O `MissionRunner` Python pode receber um `EventLog` opcional. Quando fornecido, registra eventos básicos como `mission.queued`, `mission.started`, `mission.completed` e `mission.failed`. Quando não fornecido, o runner continua funcionando sem eventos estruturados.

Batch:

`batch_started_event()`, `batch_completed_event()` e `batch_interrupted_event()` representam ciclo de vida de batch. No estado atual, são helpers Python; os scripts shell não emitem esses eventos automaticamente.

Usage/API Limit Guard:

O Guardian possui detecção determinística de sinais textuais de limite de uso/API em logs já recebidos. A categoria `usage_limit` existe no contrato de eventos, mas a emissão estruturada integrada de eventos de limite ainda é próxima etapa. No estado atual, a classificação operacional usa log textual e utilitário local, não observabilidade externa.

Exemplo de integração opcional:

```python
from vercosa_ai_framework.audit import InMemoryEventLog, record_guardian_decision_event

event_log = InMemoryEventLog()
event = record_guardian_decision_event(decision, event_log=event_log, origin="mission-runner")
```

Se `event_log` não for fornecido aos helpers `record_*`, o evento é criado e retornado, mas não é armazenado.

## Eventos Auditáveis De Alto Nível

Exemplos de eventos que a arquitetura atual já representa ou pretende representar pelo contrato:

- Política resolvida: `policy.resolution` com contadores de policy sets, políticas resolvidas e refs aplicáveis.
- Conflito de política: `policy.resolution` com `conflicts_count` e `conflict_refs`.
- Decisão do Guardian: `guardian.decision` com decisão, risco, bloqueios ou aprovação requerida.
- `ContextPackage` montado: `context.package` com itens selecionados, tokens estimados e refs.
- Item de contexto omitido: `context.package` com `omission_reasons` agregados e `omitted_item_refs`.
- Missão iniciada: `mission.started`.
- Missão concluída: `mission.completed`.
- Missão falhou: `mission.failed`.
- Batch interrompido por quota: próximo passo possível para evento `usage_limit` ou `mission.batch.interrupted`, sem emissão estruturada automática no estado atual.

## Segurança E Dados Sensíveis

Eventos auditáveis não devem registrar conteúdo sensível bruto por padrão. A regra é preservar rastreabilidade sem vazar dados.

Cuidados obrigatórios:

- Não registrar secrets.
- Não registrar credenciais.
- Não registrar tokens de API.
- Não registrar prompts completos por padrão.
- Não registrar conteúdo integral sensível por padrão.
- Não registrar payload bruto de provider por padrão.
- Preferir metadata mínima.
- Preferir refs, contadores, hashes seguros, flags e identificadores internos.
- Registrar omissões e redactions sem guardar valor original sensível.

Metadados seguros típicos:

```json
{
  "mission_id": "mission-123",
  "policy_refs": ["policy.security.review"],
  "warnings_count": 1,
  "omitted_items_count": 2,
  "requires_approval": true
}
```

Metadados que não devem ser registrados por padrão:

```json
{
  "prompt": "prompt completo do usuário",
  "api_token": "token real",
  "raw_content": "conteúdo integral sensível",
  "authorization": "Bearer segredo"
}
```

## Limites Atuais

O Audit/Event Log atual não possui:

- Persistência externa.
- Banco.
- SQLite.
- PostgreSQL.
- OpenTelemetry.
- Dashboard.
- Exportador.
- Correlação completa com Git.
- Retenção configurável.
- Consulta real de billing.
- Integração automática com scripts shell.
- Integração automática com Provider Gateway.
- Evento estruturado integrado para todas as decisões de Model Selection, Runtime ou Provider.

Essas ausências são limites intencionais da fase atual. Elas evitam acoplamento prematuro, dependências externas e vazamento de dados antes de estabilizar contratos e políticas.

## Próximos Passos Possíveis

Próximos passos possíveis, ainda não implementados:

- Persistência local controlada.
- Exportação em JSONL.
- Integração com Mission Runner real e scripts operacionais quando houver contrato seguro.
- Integração com Provider Gateway.
- Correlação com commits.
- Relatórios pós-batch.
- Política de retenção.
- Redaction de metadata.
- Auditoria de uso de tools/providers.
- Eventos estruturados para Usage/API Limit Guard.
- Eventos estruturados para seleção de modelo, fallback e orçamento.

Nenhum desses itens deve ser tratado como implementado até haver Spec, ADR ou missão aprovada com testes e documentação correspondente.

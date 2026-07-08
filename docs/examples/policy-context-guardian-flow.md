# Fluxo Policy, Context E Guardian

Links principais: [Exemplos](README.md) | [Módulo policy](../../src/vercosa_ai_framework/policy/README.md) | [Módulo context](../../src/vercosa_ai_framework/context/README.md) | [Módulo guardian](../../src/vercosa_ai_framework/guardian/README.md)

## Objetivo

Explicar o fluxo conceitual implementado até aqui entre Policy Engine, `ResolvedPolicySet`, Context Router, `ContextPackage`, Token Budget Manager e Guardian Engine.

Status deste exemplo: exemplo conceitual e de arquitetura. Ele descreve contratos e integrações iniciais determinísticas, sem executar provider externo e sem chamada de LLM.

## Fluxo Conceitual Atual

```text
PolicySet explícito
↓
Policy Engine
↓
ResolvedPolicySet
↓
Context Router + Token Budget Manager
↓
ContextPackage
↓
Guardian Engine
↓
GuardianDecision
```

## Responsabilidades Implementadas

Policy Engine:

- Resolve políticas declarativas em `ResolvedPolicySet`.
- Aplica precedência simples e detecta conflitos básicos.
- Não executa enforcement operacional.
- Não chama Context Router, Guardian Engine, Model Selection, provider, banco, rede ou LLM.

Context Router:

- Consome `ResolvedPolicySet` opcional já resolvido quando o chamador fornece essa entrada.
- Monta `ContextPackage` a partir de candidatos explícitos.
- Usa o Token Budget Manager para estimar orçamento de tokens e omitir itens quando necessário.
- Não resolve políticas.
- Não busca documentos por conta própria.
- Não chama Knowledge Hub diretamente.
- Não chama Guardian Engine automaticamente.

Token Budget Manager:

- Estima tokens de forma determinística no MVP.
- Reserva tokens de saída antes de preencher contexto.
- Apoia decisões de inclusão ou omissão por orçamento.
- Não seleciona modelo e não consulta limites reais de provider.

Guardian Engine:

- Avalia risco operacional.
- Pode avaliar missão, task, comando, ação sensível ou `ContextPackage` já montado.
- Pode considerar `ResolvedPolicySet` opcional recebido pelo chamador.
- Pode elevar decisão para `warn`, `require_approval` ou `block` conforme riscos e políticas resolvidas.
- Não resolve políticas declarativas e não monta contexto.

## Exemplo Conceitual De Entrada

Entrada declarativa simplificada:

```text
PolicySet:
  regra: negar item sensível quando target_refs indicar source_ref=secret-doc

ContextRequest:
  objetivo: preparar contexto mínimo para revisar documentação
  orçamento: max_input_tokens=1000, reserved_output_tokens=200
  resolved_policy_set: resultado já produzido pelo Policy Engine

Candidatos:
  item-1: source_ref=readme, conteúdo público
  item-2: source_ref=secret-doc, conteúdo marcado como sensível
```

Saída conceitual esperada no estado atual:

```text
ResolvedPolicySet:
  refs de políticas resolvidas
  conflitos e warnings, se existirem

ContextPackage:
  inclui item-1 se couber no orçamento
  omite item-2 somente se a política deny tiver alvo determinístico
  registra policy_refs, warnings, omissões e estimativa de tokens

GuardianDecision:
  avalia o ContextPackage recebido
  pode permitir, avisar, exigir aprovação ou bloquear conforme risco operacional
```

Este exemplo é conceitual. Ele não é uma DSL completa de políticas e não representa parser externo de política.

## O Que É Implementado

- `DeterministicPolicyEngine` resolve políticas declarativas explícitas.
- `ResolvedPolicySet` pode ser repassado pelo chamador ao Context Router.
- `DeterministicContextRouter` monta `ContextPackage` com candidatos explícitos.
- `SimpleTokenBudgetManager` estima tokens de forma determinística.
- `GuardianEngine` pode avaliar `ContextPackage` por chamada explícita.
- `GuardianEngine` pode considerar `ResolvedPolicySet` opcional em avaliações.

## Integração Inicial

- Policy Engine, Context Router e Guardian Engine se conectam por estruturas explícitas passadas pelo chamador.
- A integração é unidirecional e determinística.
- O Context Router consome políticas resolvidas, mas não chama o Policy Engine.
- O Guardian considera pacote e políticas recebidas, mas não monta contexto nem resolve políticas.

## Futuro Ou Fora Do Escopo Atual

- RAG semântico.
- Embeddings.
- pgvector.
- PostgreSQL obrigatório.
- Provider externo.
- Chamada de LLM nesse fluxo de teste.
- DSL completa de políticas.
- Enforcement completo de todos os efeitos declarativos.
- Recuperação automática de documentos pelo Context Router.
- Integração automática do Guardian em todo fluxo de missão.

## Limites Do Exemplo

- O exemplo não cria código Python.
- O exemplo não executa providers.
- O exemplo não promete enforcement completo.
- O exemplo não substitui Specs nem testes de contrato.
- O exemplo não transforma `allow`, `prefer` ou `set_limit` em comportamento operacional completo.

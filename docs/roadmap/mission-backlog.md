# Backlog Estratégico De Missões

Links principais: [README principal](../../README.md) | [Roadmap macro](../alignment/roadmap.md) | [Uso do runner seguro](../operations/safe-runner-usage.md) | [Estado atual](../alignment/current-state.md)

## Objetivo

Este documento é o backlog estratégico canônico de missões futuras do Vercosa AI Framework. Ele organiza próximos trabalhos por fases, dependências, riscos, pré-requisitos e critérios de avanço.

Este backlog não é fila executável e não deve ser executado automaticamente.

## Escopo

Este documento orienta planejamento operacional. Ele não aprova implementação, não substitui Specs, não cria missões em `missions/queue` e não autoriza mudanças de código por si só.

O objetivo é permitir que o projeto escolha blocos pequenos e revisáveis para a fila executável, evitando criar dezenas de missões dependentes de decisões que ainda não existem.

## Termos Operacionais

- Backlog estratégico: mapa vivo de missões possíveis, organizado por fase, dependências, riscos e critérios de avanço. Pode ser grande, mas não é executável diretamente.
- Fila executável: conjunto pequeno de arquivos `.md` em `missions/queue`, revisados e prontos para execução pelo runner.
- Missão em execução: missão movida para `missions/running` pelo worker ou runner, com escopo ativo e validações obrigatórias.
- Missão concluída: missão movida para `missions/done` após entregar critérios de aceite, testes aplicáveis e commit separado quando o fluxo estiver configurado para auto-commit.
- Batch operacional: execução sequencial controlada da fila executável por `scripts/vaf-run-batch-safe.sh`, parando na primeira falha e mantendo validação por missão. É o fluxo operacional padrão quando o bloco estiver bem especificado, revisado e seguro.

## Regras De Uso

- O backlog estratégico não deve ser executado automaticamente.
- `missions/queue` deve receber somente blocos pequenos, revisáveis e compatíveis com o estado atual do projeto.
- Missões futuras não devem ser criadas na fila quando dependerem de decisões, código ou documentação ainda não produzidos.
- Cada missão executável deve manter objetivo, escopo permitido, escopo proibido, dependências e critérios de aceite próprios.
- O roadmap macro continua em [docs/alignment/roadmap.md](../alignment/roadmap.md); este documento é a visão operacional detalhada.

## Modelo Operacional De Batch

O modelo operacional padrão é batch governado quando a fila executável estiver revisada e segura. O modelo continua incremental e não autoriza execução cega:

1. Preparar um bloco pequeno de missões executáveis em `missions/queue`.
2. Usar `VAF_BATCH_SIZE=10 ./scripts/vaf-run-batch-safe.sh` para blocos normais já revisados e seguros.
3. Parar sempre na primeira falha.
4. Testar após cada missão por reaproveitamento do runner seguro de uma missão.
5. Manter commit separado por missão.
6. Revisar resultados, diffs, documentação e commits locais após o batch.
7. Preferir push manual após revisão.
8. Usar `VAF_BATCH_SIZE=3` para testes, retomadas, blocos pequenos ou recuperação.
9. Usar execução individual para missões sensíveis, arquiteturais, incertas, investigativas ou de alto risco.

Batch de 10 não elimina governança, revisão, rastreabilidade, critérios de aceite, referências a documentos ou validações locais.

`VAF_AUTO_PUSH=1` continua opt-in e não deve ser tratado como padrão. Push manual após checklist pós-batch continua sendo a prática recomendada.

## Estado Arquitetural Considerado

- Mission Runner existe.
- Runner seguro de uma missão existe.
- Runner seguro em batch existe.
- Batch de 3 foi validado para teste, retomada, blocos pequenos e recuperação.
- Batch de 10 é funcional para blocos normais revisados e seguros, com ressalva de limites externos de API.
- Batch é o padrão operacional quando seguro; execução individual permanece necessária para missões críticas, sensíveis, arquiteturais, incertas, investigativas, de recuperação ou de alto risco.
- Context Router possui MVP determinístico.
- Token Budget Manager possui MVP determinístico.
- Knowledge Hub já se integra ao Context Router por candidatos explícitos.
- Guardian Engine avalia `ContextPackage` quando chamado explicitamente.
- Policy Engine possui contratos iniciais.
- Policy Engine já se integra ao Guardian Engine por `ResolvedPolicySet` opcional.
- Policy Engine já se integra ao Context Router por `ResolvedPolicySet` opcional.
- Policy Engine já se integra ao Model Selection por políticas resolvidas opcionais.
- Token Budget Manager já se integra ao Model Selection por requisitos mínimos de orçamento.
- Usage/API Limit Guard inicial existe.
- Usage/API Limit Guard já participa do fluxo operacional por classificação determinística de logs locais já produzidos.
- Audit/Event Log já possui contratos iniciais em memória, helpers opcionais para decisões centrais e eventos de missão/batch.
- O `MissionRunner` Python já possui integração opcional com eventos auditáveis quando recebe um `EventLog`.
- CLI operacional inicial já possui `status`, `validate` e `doctor`.
- Exemplos operacionais iniciais existem em `docs/examples/`.
- Integrações completas com Provider Gateway, persistência externa de eventos, providers reais, múltiplos runtimes reais, documentação pública completa e release alfa ainda são lacunas.

## Itens Já Concluídos Ou Absorvidos

Os itens abaixo não devem ser recriados como novas missões executáveis sem revisão de escopo. Eles já foram concluídos, absorvidos no estado atual ou documentados como integração inicial:

- Integração Policy Engine com Model Selection.
- Integração Token Budget Manager com Model Selection.
- Integração Usage/API Limit Guard ao fluxo operacional.
- Audit/Event Log inicial.
- Eventos auditáveis de decisões centrais.
- Eventos auditáveis do Mission Runner Python.
- CLI operacional inicial.
- Comando CLI `validate`.
- Comando CLI `doctor`.
- Exemplos operacionais iniciais.
- README principal com identidade de Harness Engineering.
- Batch como padrão operacional quando seguro.
- Guia inicial de instalação local para desenvolvimento.
- Guia inicial de contribuição.
- Base documental legal inicial, com política de uso responsável e notas de licença pendente.
- Preparação documental para futura alfa pública concluída como checklist inicial em [docs/release/public-alpha-readiness.md](../release/public-alpha-readiness.md), sem criação de release, tag, pacote ou changelog de release.

Esses itens podem gerar missões futuras de refinamento, persistência, integração completa ou documentação pública, mas não devem ser duplicados como se ainda não existissem.

## Fase 1 — Consolidação Operacional

Objetivo da fase: manter batch governado como fluxo operacional padrão para blocos seguros e preservar execução individual para risco alto.

Por que a fase existe: o projeto já possui runner seguro de uma missão, runner seguro em batch, validação de batch de 3 e primeiro bloco de 10 concluído; agora precisa manter governança para que batch de 10 seja padrão apenas quando seguro.

Riscos se a fase for pulada: execução cega, commits difíceis de revisar, falhas repetidas, perda de rastreabilidade e entrada prematura de missões dependentes na fila.

Missões prováveis:

- Integrar CLI com validações de Git de forma segura e somente leitura.
- Criar comando CLI para listar missões sem executar, mover ou alterar arquivos.
- Criar comando CLI para resumo pós-batch com base em estado local, logs e commits já existentes.
- Revisar periodicamente critérios de batch de 10 após interrupções por limite externo de API.

Dependências:

- `scripts/vaf-run-next-safe.sh` existente.
- `scripts/vaf-run-batch-safe.sh` existente.
- `docs/operations/safe-runner-usage.md` atualizado.
- Testes locais estáveis.

Critérios para avançar:

- Batch de 3 missões executado com sucesso ou falhas documentadas e corrigidas.
- Primeiro bloco de 10 missões reais validado.
- Checklist pós-batch aplicado.
- Critérios claros para quando usar ou não batch de 10.
- Nenhuma falha recente sem diagnóstico.

## Fase 2 — Integrações Centrais

Objetivo da fase: conectar componentes MVP existentes sem expandir a superfície arquitetural indevidamente.

Por que a fase existe: Policy Engine, Guardian Engine, Context Router, Token Budget Manager e Model Selection Engine existem como módulos separados, mas ainda precisam de integrações governadas e auditáveis.

Riscos se a fase for pulada: seleção de modelo sem política, orçamento de tokens ignorado, agentes ou runtimes contornando governança e decisões espalhadas em pontos errados.

Missões prováveis:

- Revisar integração entre Context Router, Guardian, Policy, Model Selection e Audit/Event Log após as novas pontes.
- Definir testes de contrato para fronteiras entre políticas, contexto, orçamento, seleção de modelo e decisões Guardian.
- Documentar critérios para promover integrações opcionais a fluxo orquestrado obrigatório.

Dependências:

- Contratos atuais de `policy/`, `guardian/`, `context/` e `model_selection/`.
- Critérios de aceite explícitos para não fundir responsabilidades.
- Specs ou ADRs atualizadas quando houver mudança material de fronteira.

Critérios para avançar:

- Model Selection consome políticas e orçamento sem chamar providers diretamente.
- Usage/API Limit Guard participa do fluxo operacional sem mascarar bugs do framework.
- Testes comprovam comportamento determinístico.
- Documentação deixa claro o que é MVP e o que continua futuro.

## Fase 3 — Observabilidade E Auditoria

Objetivo da fase: registrar decisões relevantes de missão, contexto, política, Guardian, modelo e validação em eventos auditáveis.

Por que a fase existe: governança sem registro persistível limita revisão, diagnóstico, compliance e melhoria contínua.

Riscos se a fase for pulada: perda de evidências, decisões não reproduzíveis, dificuldade de depurar falhas e commits sem trilha suficiente.

Missões prováveis:

- Persistir eventos auditáveis em arquivo local controlado.
- Definir formato mínimo de eventos de validação.
- Relacionar eventos com missão, commit e artefatos alterados.
- Registrar seleção de modelo, fallback e restrições de orçamento em eventos auditáveis.

Dependências:

- Persistence Layer MVP.
- Decisões de fronteira entre eventos, logs operacionais e resultados de validação.
- Política de retenção futura registrada como decisão ou pergunta em aberto quando necessário.

Critérios para avançar:

- Eventos iniciais são determinísticos, serializáveis e sem segredos.
- Decisões de Guardian, Policy e Context possuem referências rastreáveis.
- Falhas de validação podem ser diagnosticadas sem depender apenas de saída textual do terminal.

## Fase 4 — Experiência De Uso

Objetivo da fase: tornar a operação local mais clara para usuários e mantenedores sem esconder governança.

Por que a fase existe: o framework precisa ser operável por terminal/SSH, mas a CLI atual ainda é inicial e a experiência de execução deve ser menos frágil.

Riscos se a fase for pulada: adoção difícil, comandos pouco descobríveis, uso incorreto de batch e aumento de erros manuais.

Missões prováveis:

- Integrar CLI com validações de Git de forma segura.
- Criar comando CLI para listar missões.
- Criar comando CLI para resumo pós-batch.
- Melhorar mensagens de status, validação e diagnóstico.
- Documentar fluxos comuns de missão, batch e diagnóstico.
- Preparar comandos de leitura sem criar automações perigosas.

Dependências:

- Playbook de batch consolidado.
- Eventos ou logs mínimos para status mais confiável.
- Specs existentes de Mission Runner e runtime respeitadas.

Critérios para avançar:

- Usuário consegue entender fila, execução, falha e validação por comandos simples.
- CLI não substitui revisão nem contorna Guardian.
- Documentação operacional cobre caminhos principais e limites.

## Fase 5 — Exemplos Reais E Documentação Pública

Objetivo da fase: demonstrar uso real do framework sem prometer recursos ainda não implementados.

Por que a fase existe: exemplos concretos ajudam validação, onboarding e revisão pública do projeto.

Riscos se a fase for pulada: documentação abstrata demais, expectativas erradas sobre o MVP e dificuldade para contributors entenderem limites atuais.

Missões prováveis:

- Criar documentação pública inicial.
- Criar guia de instalação.
- Criar guia de contribuição.
- Revisar README principal para público externo.
- Preparar documentação pública alfa sem marcar recursos futuros como implementados.

Dependências:

- Fluxo operacional estável.
- CLI ou comandos documentados o suficiente para reprodução.
- Clareza sobre o que é implementado, MVP, futuro ou lacuna.

Critérios para avançar:

- Exemplos executáveis ou claramente marcados como conceituais.
- Guia de instalação não assume o ambiente pessoal do mantenedor como obrigatório.
- Guia de contribuição respeita idioma, Specs, commits e revisão.

## Fase 6 — Preparação De Alfa/Release

Objetivo da fase: preparar uma release alfa rastreável, honesta sobre limites e segura para experimentação.

Por que a fase existe: a primeira release precisa consolidar licença, documentação mínima, tag e critérios de estabilidade do MVP.

Riscos se a fase for pulada: distribuição sem licença, tag prematura, changelog incompleto e usuários interpretando componentes futuros como entregues.

Missões prováveis:

- Criar licença se ainda não existir.
- Revisar checklist de release alfa.
- Criar release/tag alfa.
- Revisar arquitetura pós-integrações.
- Registrar lacunas remanescentes para pós-alfa.

Dependências:

- Documentação pública inicial.
- Guia de instalação e contribuição.
- Testes estáveis.
- Decisão explícita de licença.

Critérios para avançar:

- Licença definida.
- Tag alfa criada somente após testes e revisão.
- README não promete estabilidade além do estado real.
- Lacunas futuras registradas.

## Fase 7 — Capacidades Avançadas Futuras

Objetivo da fase: avaliar recursos semânticos, providers auxiliares e internacionalização depois do MVP operacional.

Por que a fase existe: embeddings, pgvector, Semantic Index, RAG semântico, Gemini e internacionalização têm impacto arquitetural, operacional, documental e de suporte.

Riscos se a fase for pulada ou antecipada: acoplamento indevido a banco ou provider, aumento de dependências, prompts com contexto bruto, custo de tokens maior, documentação multilíngue divergente e confusão sobre suporte real.

Missões prováveis:

- Avaliar Semantic Index.
- Avaliar embeddings.
- Avaliar pgvector.
- Avaliar RAG semântico.
- Avaliar Gemini, Gemini CLI e Gemini MCP Bridge como provider auxiliar futuro.
- Internacionalizar READMEs no final.

Dependências:

- Context Router e Knowledge Hub estabilizados.
- Eventos auditáveis mínimos.
- Política de provider externo e dados sensíveis.
- Decisão sobre adapters e limites de dependências opcionais.

Critérios para avançar:

- Recursos avançados avaliados como adapters opcionais, não core obrigatório.
- PostgreSQL, pgvector, Ollama, embeddings e Gemini continuam opcionais.
- Internacionalização ocorre depois de estabilizar o conteúdo em português do Brasil.

## Missões Futuras Prováveis

As missões abaixo começam após a missão atual de criação deste backlog. Os códigos são sugestões e podem ser ajustados quando os arquivos executáveis forem criados.

1. Código sugerido: `M001-playbook-batch-operacional`
Título: Documentar playbook de execução em batch.
Objetivo: criar guia operacional detalhado para preparar, executar e revisar batches.
Escopo permitido: documentação em `docs/operations/`, referências ao runner seguro e exemplos de comandos.
Escopo proibido: alterar scripts, criar runner novo, mudar código Python ou criar missões em massa.
Dependências: runner seguro de uma missão e runner seguro em batch existentes.
Critérios de aceite resumidos: playbook explica preparação, execução, parada por falha, validações e revisão pós-batch.

2. Código sugerido: `M002-checklist-pos-batch`
Título: Criar checklist de validação pós-batch.
Objetivo: padronizar revisão após batch antes de push ou nova fila.
Escopo permitido: checklist documental com Git status, diffs, commits, testes, compileall, documentação e fila de missões.
Escopo proibido: automatizar push, alterar runner ou reduzir validações.
Dependências: playbook de batch.
Critérios de aceite resumidos: checklist cobre sucesso, falha, revisão de commits separados e decisão de continuar ou bloquear.

3. Código sugerido: `M003-teste-batch-3`
Título: Testar batch de 3 missões.
Objetivo: validar ou retomar o fluxo operacional com `VAF_BATCH_SIZE=3`.
Escopo permitido: preparar até 3 missões pequenas, executar runner seguro em batch e registrar resultado.
Escopo proibido: usar batch de 10, alterar scripts, pular revisão ou fazer push automático por padrão.
Dependências: playbook e checklist pós-batch.
Status: validado como fluxo de teste, retomada, bloco pequeno e recuperação.
Critérios de aceite resumidos: 3 missões passam ou falhas são registradas com diagnóstico e correção antes de nova tentativa.

4. Código sugerido: `M004-liberar-batch-10`
Título: Liberar uso de batch de 10.
Objetivo: registrar batch de 10 como fluxo operacional padrão para blocos adequados, revisados e seguros.
Escopo permitido: documentação de critérios, atualização discreta de guias e registro de riscos.
Escopo proibido: tornar batch de 10 obrigatório para todos os casos, remover limite máximo ou eliminar revisão.
Dependências: runner seguro em batch, checklist pós-batch, fluxo validado e ausência de falha recente sem diagnóstico.
Status: consolidado como padrão operacional para blocos normais já revisados e seguros.
Critérios de aceite resumidos: documentação deixa claro quando usar batch de 10, quando usar batch de 3, quando usar execução individual e como revisar antes de push.

5. Código sugerido: `M005-policy-model-selection`
Título: Integrar Policy Engine com Model Selection.
Objetivo: permitir que políticas resolvidas influenciem seleção de modelo sem acoplar providers.
Escopo permitido: contratos mínimos, testes determinísticos e documentação de limites.
Escopo proibido: chamar providers, descobrir modelos reais, implementar billing real ou hardcodar modelo.
Dependências: contratos de `policy/` e `model_selection/`, Spec ou ADR se houver mudança de fronteira.
Status: concluído como integração inicial por políticas resolvidas opcionais; refinamentos futuros devem ter escopo próprio.
Critérios de aceite resumidos: seleção respeita efeitos declarativos aplicáveis e mantém justificativa auditável.

6. Código sugerido: `M006-token-budget-model-selection`
Título: Integrar Token Budget Manager com Model Selection.
Objetivo: usar orçamento estimado para restringir ou justificar seleção de modelo.
Escopo permitido: integração determinística entre orçamento e política de seleção.
Escopo proibido: RAG semântico, embeddings, chamada de LLM ou cálculo real de custo de provider.
Dependências: `context/` MVP e `model_selection/` MVP.
Status: concluído como integração inicial por requisitos mínimos de orçamento; billing real e custo de provider continuam futuros.
Critérios de aceite resumidos: decisões de modelo indicam restrições de contexto e fallback quando orçamento for incompatível.

7. Código sugerido: `M007-usage-limit-worker`
Título: Integrar Usage/API Limit Guard ao fluxo operacional do worker.
Objetivo: tratar sinais de limite externo como parada segura ou revisão manual quando apropriado.
Escopo permitido: integração operacional mínima, testes com mensagens simuladas e documentação.
Escopo proibido: consultar billing real, chamar provider externo, mascarar bugs ou fazer retry infinito.
Dependências: `guardian/usage_limits.py` e fluxo atual do worker.
Status: concluído como classificação determinística de logs locais no fluxo operacional; consulta real de billing e retry inteligente continuam fora do escopo atual.
Critérios de aceite resumidos: limites detectados geram ação segura, diagnóstico claro e sem chamadas externas.

8. Código sugerido: `M008-audit-event-log-inicial`
Título: Criar Audit/Event Log inicial.
Objetivo: definir registro auditável mínimo para eventos do framework.
Escopo permitido: contrato de evento, serialização local e testes determinísticos.
Escopo proibido: banco obrigatório, rede, provider externo ou observabilidade distribuída.
Dependências: Persistence Layer MVP e decisões mínimas de retenção.
Status: entregue como contratos iniciais e implementação em memória; persistência, retenção e integrações permanecem futuras.
Critérios de aceite resumidos: eventos possuem id, categoria, severidade, resultado, timestamp controlável em testes e metadados estruturados.

9. Código sugerido: `M009-eventos-guardian-policy-context`
Título: Registrar decisões de Guardian/Policy/Context em eventos auditáveis.
Objetivo: vincular decisões governadas a eventos rastreáveis.
Escopo permitido: eventos para Policy Resolution, Guardian Decision e Context Package summary.
Escopo proibido: gravar conteúdo sensível bruto, implementar analytics ou mudar decisão dos módulos.
Dependências: Audit/Event Log inicial.
Status: concluído como helpers opcionais para decisões centrais; persistência, exportação e integração automática continuam futuras.
Critérios de aceite resumidos: decisões geram eventos com refs, motivos e limites sem vazar segredos.

10. Código sugerido: `M010-cli-operacional-amigavel`
Título: Criar CLI operacional mais amigável.
Objetivo: facilitar consulta de status, fila, validações e próximos passos seguros.
Escopo permitido: comandos locais, mensagens claras e documentação.
Escopo proibido: contornar runner seguro, executar push por padrão ou esconder falhas.
Dependências: fluxo operacional consolidado e, preferencialmente, eventos mínimos.
Status: concluído como CLI operacional inicial com `status`, `validate` e `doctor`; comandos adicionais de leitura continuam futuros.
Critérios de aceite resumidos: comandos ajudam diagnóstico e mantêm governança explícita.

11. Código sugerido: `M011-exemplos-reais-uso`
Título: Criar exemplos reais de uso.
Objetivo: demonstrar fluxos reprodutíveis do MVP sem recursos futuros.
Escopo permitido: exemplos locais, pequenos e documentados.
Escopo proibido: depender de provider externo, RAG semântico, pgvector obrigatório ou ambiente específico do mantenedor.
Dependências: CLI e documentação operacional suficientes.
Status: iniciado com exemplos operacionais em [docs/examples](../examples/README.md); exemplos públicos adicionais continuam possíveis em missões futuras.
Critérios de aceite resumidos: exemplos indicam pré-requisitos, comandos, saídas esperadas e limites.

12. Código sugerido: `M012-documentacao-publica-inicial`
Título: Criar documentação pública inicial.
Objetivo: preparar documentação de entrada para usuários externos.
Escopo permitido: guias, visão, arquitetura resumida e limites do MVP.
Escopo proibido: prometer release estável, recursos semânticos implementados ou provider obrigatório.
Dependências: exemplos reais e README revisado.
Status: iniciado com a revisão do `README.md` principal para explicitar o VAF como framework de Harness Engineering; guias públicos adicionais continuam futuros.
Critérios de aceite resumidos: documentação pública é clara, rastreável e honesta sobre estado atual.

13. Código sugerido: `M013-guia-instalacao`
Título: Criar guia de instalação.
Objetivo: documentar instalação e validação inicial sem assumir uma única infraestrutura.
Escopo permitido: requisitos mínimos, alternativas por ambiente e validações locais.
Escopo proibido: tornar ARM64, PostgreSQL, pgvector, Ollama ou systemd obrigatórios para todo usuário.
Dependências: documentação pública inicial.
Status: concluído como guia inicial de instalação local para desenvolvimento em [docs/getting-started/local-installation.md](../getting-started/local-installation.md); guia de instalação pública completa e preparação de release continuam futuros.
Critérios de aceite resumidos: guia separa requisitos do MVP de integrações opcionais futuras.

14. Código sugerido: `M014-guia-contribuicao`
Título: Criar guia de contribuição.
Objetivo: explicar fluxo de Specs, missões, documentação, testes, commits e revisão.
Escopo permitido: `CONTRIBUTING.md` ou docs equivalentes, padrões de commit e PR.
Escopo proibido: alterar governança sem decisão ou reduzir exigência de Spec.
Dependências: padrões de documentação e idioma já existentes.
Status: concluído como guia inicial em [CONTRIBUTING.md](../../CONTRIBUTING.md), com índice complementar em [docs/contributing](../contributing/README.md); processo público completo de contribuição continua futuro.
Critérios de aceite resumidos: contributor entende como propor mudança sem violar Specification First.

15. Código sugerido: `M015-licenca-projeto`
Título: Criar licença se ainda não existir.
Objetivo: definir licença open source do projeto.
Escopo permitido: adicionar arquivo de licença aprovado e referência discreta na documentação.
Escopo proibido: escolher licença sem decisão do mantenedor ou misturar texto de licenças incompatíveis.
Dependências: decisão explícita de licença.
Status: base documental criada em `docs/legal/`; licença final permanece pendente por falta de decisão explícita.
Critérios de aceite resumidos: licença existe, é referenciada e não conflita com objetivos do projeto.

Missões futuras relacionadas:

- Criar `SECURITY.md`.
- Criar `CODE_OF_CONDUCT.md`, se desejado para a abertura pública.
- Criar templates de issue.
- Criar templates de pull request.
- Criar changelog inicial quando houver decisão de release.
- Definir versão inicial.
- Definir política de release.
- Revisar e criar `LICENSE` antes da release pública.
- Publicar release alfa somente após validações e decisão explícita.
- Internacionalizar READMEs no final, mantendo `README.md` canônico em português do Brasil.

16. Código sugerido: `M016-release-tag-alfa`
Título: Criar release/tag alfa.
Objetivo: publicar marco alfa com escopo e limitações claros.
Escopo permitido: checklist, changelog ou notas de release e tag após validação.
Escopo proibido: publicar como stable, pular testes ou fazer push automático sem revisão.
Dependências: licença, guia de instalação, guia de contribuição, documentação pública e testes verdes.
Critérios de aceite resumidos: tag alfa é rastreável, validada e descreve limites do MVP.

17. Código sugerido: `M017-revisao-arquitetura-pos-integracoes`
Título: Revisar arquitetura pós-integrações.
Objetivo: verificar coerência entre Specs, docs, código e decisões após integrações centrais.
Escopo permitido: documentação, ADRs ou perguntas em aberto.
Escopo proibido: implementar mudanças estruturais sem Spec aprovada.
Dependências: Fases 2 e 3 concluídas.
Critérios de aceite resumidos: lacunas e decisões são registradas sem prometer comportamento inexistente.

18. Código sugerido: `M018-avaliar-semantic-index`
Título: Avaliar Semantic Index.
Objetivo: estudar contrato e impacto de busca semântica futura.
Escopo permitido: análise, ADR candidata, riscos e critérios para MVP futuro.
Escopo proibido: implementar embeddings, pgvector, RAG ou dependências novas.
Dependências: Context Router, Knowledge Hub e auditoria estabilizados.
Critérios de aceite resumidos: avaliação define opções e riscos sem virar implementação.

19. Código sugerido: `M019-avaliar-embeddings`
Título: Avaliar embeddings.
Objetivo: definir critérios para providers de embedding como adapters opcionais.
Escopo permitido: análise de contratos, privacidade, custo, dimensões e fallback.
Escopo proibido: chamar Ollama, baixar modelos, indexar código ou adicionar dependências.
Dependências: avaliação de Semantic Index ou decisão equivalente.
Critérios de aceite resumidos: critérios de adoção e fallback ficam documentados.

20. Código sugerido: `M020-avaliar-pgvector`
Título: Avaliar pgvector.
Objetivo: avaliar pgvector como uma implementação possível de vector store.
Escopo permitido: análise arquitetural, contratos e riscos operacionais.
Escopo proibido: tornar PostgreSQL obrigatório, criar migrations reais ou acessar banco.
Dependências: avaliação de embeddings e vector store adapter conceitual.
Critérios de aceite resumidos: pgvector é documentado como opção futura, não dependência atual.

21. Código sugerido: `M021-avaliar-rag-semantico`
Título: Avaliar RAG semântico.
Objetivo: avaliar como retrieval semântico poderia alimentar Context Router com citações e política.
Escopo permitido: desenho conceitual, riscos de segurança e critérios de aceite futuros.
Escopo proibido: implementar RAG, embeddings, pgvector, chamada de LLM ou prompt automático.
Dependências: avaliações de Semantic Index, embeddings e pgvector.
Critérios de aceite resumidos: avaliação preserva Context Router como decisor do pacote final.

22. Código sugerido: `M022-avaliar-gemini-provider-auxiliar`
Título: Avaliar Gemini, Gemini CLI e Gemini MCP Bridge como provider auxiliar futuro.
Objetivo: analisar se Gemini pode ser adapter auxiliar sem virar dependência atual.
Escopo permitido: pesquisa documental local, matriz de riscos e proposta de adapter futuro.
Escopo proibido: instalar Gemini, chamar rede, configurar credenciais, implementar provider ou MCP.
Dependências: política de provider externo e Provider Gateway mais maduro.
Critérios de aceite resumidos: resultado deixa claro que Gemini é avaliação futura e opcional.

23. Código sugerido: `M023-internacionalizar-readmes-final`
Título: Internacionalizar READMEs no final.
Objetivo: criar variações linguísticas após estabilização da documentação em português.
Escopo permitido: manter `README.md` em pt-BR, criar `README.en.md` em inglês e `README.es.md` em espanhol.
Escopo proibido: internacionalizar antes da estabilização, divergir conteúdo técnico ou traduzir APIs públicas.
Dependências: release alfa ou documentação pública estabilizada.
Critérios de aceite resumidos: READMEs multilíngues indicam versão fonte e preservam links essenciais.

24. Código sugerido: `M024-cli-validacoes-git-seguras`
Título: Integrar CLI com validações de Git de forma segura.
Objetivo: permitir diagnóstico local de branch, Git limpo e commits recentes sem executar push, commit, reset ou comandos destrutivos.
Escopo permitido: leitura local, mensagens claras, testes determinísticos e documentação.
Escopo proibido: alterar fluxo Git, executar push, staging automático, commit automático, reset, checkout destrutivo ou reescrita de histórico.
Dependências: CLI operacional inicial e política de documentação atualizada.
Critérios de aceite resumidos: CLI reporta estado Git básico de forma segura e não substitui revisão humana.

25. Código sugerido: `M025-cli-listar-missoes`
Título: Criar comando CLI para listar missões.
Objetivo: listar missões em `queue`, `running`, `done` e `failed` com saída previsível e sem efeitos colaterais.
Escopo permitido: leitura local, ordenação determinística, testes e docs.
Escopo proibido: mover missões, executar missões, alterar arquivos ou interpretar backlog estratégico como fila executável.
Dependências: CLI operacional inicial e contratos atuais de diretórios de missão.
Critérios de aceite resumidos: comando mostra missões existentes e preserva a distinção entre backlog estratégico e fila executável.

26. Código sugerido: `M026-cli-resumo-pos-batch`
Título: Criar comando CLI para resumo pós-batch.
Objetivo: produzir resumo local de estado pós-batch com contagens de missão, avisos e próximos passos seguros.
Escopo permitido: leitura de diretórios locais, logs existentes quando seguro, commits recentes em modo somente leitura e documentação.
Escopo proibido: executar batch, fazer push, criar commits, alterar missões, consultar provider, consultar rede ou substituir o checklist pós-batch.
Dependências: checklist pós-batch, CLI inicial e decisão sobre quais dados locais são seguros para resumir.
Critérios de aceite resumidos: resumo ajuda revisão pós-batch sem automatizar aprovação.

27. Código sugerido: `M027-persistir-eventos-arquivo-local`
Título: Persistir eventos auditáveis em arquivo local controlado.
Objetivo: criar persistência local inicial para `AuditEvent` sem banco obrigatório e sem observabilidade externa.
Escopo permitido: formato determinístico, testes, política de retenção inicial e documentação de limites.
Escopo proibido: banco obrigatório, rede, OpenTelemetry, dashboards, gravação de prompts completos, secrets ou tokens.
Dependências: Audit/Event Log inicial e decisão sobre formato de persistência.
Critérios de aceite resumidos: eventos são gravados de forma rastreável, segura e controlada por contrato.

28. Código sugerido: `M028-revisar-arquitetura-pos-integracoes-centrais`
Título: Revisar arquitetura pós-integrações centrais.
Objetivo: verificar coerência entre Specs, READMEs, mapas de arquitetura, backlog e código após Policy, Context, Guardian, Model Selection, Audit, CLI e batch.
Escopo permitido: documentação, ADRs, perguntas em aberto e recomendações de próximos blocos.
Escopo proibido: implementar nova funcionalidade sem Spec aprovada ou prometer integrações futuras como existentes.
Dependências: integrações centrais atuais documentadas e testes estáveis.
Critérios de aceite resumidos: lacunas reais ficam registradas e próximas missões não duplicam entregas já concluídas.

29. Código sugerido: `M029-preparar-documentacao-publica-alfa`
Título: Preparar documentação pública alfa.
Objetivo: organizar README, guias e exemplos para uma futura alfa sem transformar o MVP em promessa de estabilidade.
Escopo permitido: documentação pública, limites claros, links relativos, pré-requisitos e checklists.
Escopo proibido: criar release/tag sem decisão, internacionalizar READMEs agora ou prometer providers, RAG, embeddings, pgvector ou Semantic Index como implementados.
Dependências: guia de instalação, guia de contribuição, licença e revisão de arquitetura pós-integrações.
Status: concluído como preparação documental inicial com checklist de prontidão em [docs/release/public-alpha-readiness.md](../release/public-alpha-readiness.md); release alfa, tag, versão, changelog e internacionalização continuam futuros.
Critérios de aceite resumidos: documentação pública diferencia implementado, MVP, integração inicial, futuro e fora do escopo.

## Como Transformar Backlog Em Fila Executável

1. Escolha um bloco pequeno de missões relacionadas e independentes o suficiente para revisão.
2. Revise dependências reais contra código, docs, Specs, ADRs e perguntas em aberto.
3. Não crie missões que dependem de decisões ainda não tomadas.
4. Gere arquivos `.md` individuais em `missions/queue` apenas para as missões escolhidas.
5. Inclua objetivo, escopo permitido, escopo proibido, dependências, critérios de aceite e validações em cada arquivo.
6. Revise a fila antes da execução.
7. Rode batch somente após revisão; use `VAF_BATCH_SIZE=10` para blocos normais seguros e `VAF_BATCH_SIZE=3` para validação, retomada, bloco pequeno ou recuperação.
8. Se houver falha, não adicione mais missões à fila até diagnosticar e corrigir o problema.

## Quando NÃO Usar Batch De 10

- Quando houver mudanças estruturais grandes.
- Quando houver alteração em scripts críticos.
- Quando houver mudança de arquitetura.
- Quando houver falha recente.
- Quando houver limite de API, quota, rate limit ou erro `429` recém-ocorrido.
- Quando houver dúvidas sobre dependências.
- Quando houver critérios de aceite fracos.
- Quando houver risco de acoplamento indevido.
- Quando houver criação ou remoção de dependências.
- Quando houver alterações de segurança, credenciais, rede, provider, banco ou infraestrutura.
- Quando a revisão humana precisar ocorrer entre missões.

## Quando Batch De 10 É Aceitável

- Missões pequenas ou médias.
- Escopo bem conhecido.
- Dependências claras.
- Testes estáveis.
- Runner seguro funcionando.
- Nenhuma falha recente.
- Documentação e critérios de aceite claros.
- Baixo risco de conflito entre missões.
- Commits separados por missão continuam aceitáveis para revisão.

## Quando Usar Execução Individual

- Mudanças arquiteturais profundas.
- Alterações em scripts críticos.
- Alterações no Guardian Engine com impacto amplo.
- Alterações no Policy Engine com impacto amplo.
- Alterações no Context Router com impacto amplo.
- Alterações em providers ou runtimes.
- Missões com dependências incertas.
- Missões com critérios de aceite fracos.
- Recuperação após falha.
- Investigação de erro.
- Limite de API ou quota recém-ocorrido.

## Riscos De Backlog Grande

- Desatualização: missões podem deixar de refletir código, Specs ou decisões novas.
- Pressupostos quebrados: dependências planejadas podem mudar após missões anteriores.
- Perda de contexto: itens distantes podem ser executados sem entender por que foram escritos.
- Execução cega: backlog grande pode ser confundido com autorização para enfileirar tudo.
- Missões duplicadas: fases diferentes podem propor trabalhos parecidos.
- Acoplamento indevido: missões futuras podem pressupor integração que ainda não deveria existir.
- Documentação prometendo o que não existe: itens futuros podem parecer entregues se não forem marcados corretamente.

## Recursos Avançados Fora Do MVP Operacional Imediato

Embeddings, pgvector, Semantic Index e RAG semântico são capacidades futuras. Eles não fazem parte do MVP operacional imediato e não devem ser implementados antes de contratos, políticas, auditoria, Context Router e Knowledge Hub estarem suficientemente estabilizados.

Gemini, Gemini CLI e Gemini MCP Bridge são apenas avaliação futura como provider auxiliar ou adapter opcional. Eles não são dependência atual do framework.

## Internacionalização Final

A internacionalização dos READMEs deve ocorrer somente em fase final, depois de estabilizar conteúdo e links em português do Brasil.

Modelo desejado:

- `README.md` em português do Brasil.
- `README.en.md` em inglês.
- `README.es.md` em espanhol.

O conteúdo em outros idiomas deve preservar a rastreabilidade técnica e não traduzir nomes públicos de APIs, módulos, classes, funções ou arquivos apenas por idioma.

## Regra De Ouro

Backlog pode ser grande. Fila deve ser pequena. Batch deve ser seguro. Revisão continua obrigatória.

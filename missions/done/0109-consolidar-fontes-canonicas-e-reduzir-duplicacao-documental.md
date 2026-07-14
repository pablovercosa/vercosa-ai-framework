---
id: "0109"
title: "Consolidar fontes canônicas e reduzir duplicação documental"
base_contract: "v1"
roles:
  - documentation-architect
  - information-architecture-reviewer
  - specification-governance-reviewer
  - project-historian
  - test-engineer
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

Reduzir duplicação, divergência e manutenção redundante na documentação do
Vercosa AI Framework.

Consolidar `docs/alignment/implementation-status.md` como fonte canônica do
estado factual de implementação, integração e validação.

Definir claramente a responsabilidade de cada documento estrutural, fazendo os
demais documentos resumirem e referenciarem as fontes canônicas em vez de
repetirem extensos inventários de estado.

Registrar formalmente o tratamento histórico do identificador de missão `0001`
sem criar uma missão retroativa, fictícia ou executável.

A missão é exclusivamente documental e de governança da informação.

# Estado De Partida

O ciclo 0101-0108 concluiu:

- auditoria de aderência ao objetivo original;
- criação do checklist factual de implementação;
- consolidação do contrato base de execução;
- explicitação do fluxo de valor;
- integração Mission Runner -> Workflow Engine -> Task Queue;
- integração Task Queue -> Agent Orchestrator -> Capability Resolver;
- integração Capability -> Skill -> Tool -> Provider Gateway em dry-run;
- integração transversal de Policy, Context, Token Budget, Guardian,
  Model Selection e Audit/Event Log;
- revisão de Specs e ADRs afetadas.

O projeto possui documentação ampla distribuída entre:

- README;
- alinhamento;
- arquitetura;
- Specs;
- ADRs;
- roadmap;
- backlog;
- auditorias;
- histórico;
- release;
- segurança;
- operação;
- documentação interna dos módulos.

Parte desses documentos repete:

- módulos implementados;
- integrações concluídas;
- funcionalidades pendentes;
- limitações do MVP;
- bloqueios de release;
- fluxos arquiteturais;
- quantidade e situação de missões;
- decisões ainda abertas.

Essa repetição cria risco de documentos contraditórios e aumenta o custo de
manutenção.

# Fonte Canônica Principal

`docs/alignment/implementation-status.md` deve permanecer a fonte canônica para:

- itens planejados;
- itens implementados;
- itens integrados;
- itens validados;
- itens parcialmente implementados;
- itens adiados;
- itens fora do escopo atual;
- lacunas de produção;
- referências factuais para código e testes.

Outros documentos não devem manter cópias extensas desse checklist.

Quando precisarem informar estado de implementação, devem:

1. apresentar somente o resumo necessário ao seu propósito;
2. apontar para `implementation-status.md`;
3. não criar classificações paralelas;
4. não contradizer a fonte canônica;
5. manter detalhes históricos somente quando forem evidências datadas.

# Responsabilidade Dos Documentos

Revisar e registrar a responsabilidade de cada documento.

## README.md

Responsabilidade:

- apresentação pública;
- problema central;
- proposta de valor;
- fluxo principal resumido;
- instalação inicial;
- exemplo de uso;
- limites públicos essenciais;
- links para documentação detalhada.

Não deve conter inventário completo de implementação.

## docs/alignment/implementation-status.md

Responsabilidade:

- checklist factual canônico;
- classificação planejado, implementado, integrado e validado;
- evidências de código, testes e fluxos;
- lacunas atuais.

## docs/alignment/current-state.md

Responsabilidade:

- fotografia narrativa e resumida do checkpoint atual;
- principais capacidades;
- principais limitações;
- referência para o checklist canônico.

Não deve repetir o catálogo completo de módulos, integrações e pendências.

## docs/alignment/architecture-map.md

Responsabilidade:

- topologia arquitetural;
- fronteiras entre camadas;
- fluxos implementados e futuros;
- referências para Specs e ADRs.

Não deve funcionar como segundo checklist de implementação.

## docs/alignment/roadmap.md

Responsabilidade:

- direção estratégica;
- fases futuras;
- critérios de avanço;
- dependências de alto nível.

Não deve repetir o estado detalhado de cada módulo.

## docs/alignment/open-questions.md

Responsabilidade:

- decisões realmente abertas;
- alternativas;
- dependências;
- critérios necessários para decisão.

Remover perguntas já decididas ou convertê-las em referência ao ADR
correspondente.

## docs/roadmap/mission-backlog.md

Responsabilidade:

- backlog estratégico não executável;
- missões orientadoras futuras;
- dependências;
- riscos;
- critérios para criação da fila executável.

Não deve repetir todo o histórico concluído.

## docs/history/mission-milestones.md

Responsabilidade:

- histórico factual por faixa de missões;
- mudanças de direção;
- resultados;
- limitações históricas.

Não deve ser usado como checklist do estado atual.

## docs/audits/

Responsabilidade:

- evidência datada de uma auditoria;
- critérios usados;
- achados;
- conclusão no momento da execução.

Relatórios de auditoria não devem ser reescritos para parecer atuais.

## docs/release/

Responsabilidade:

- políticas e evidências relacionadas a versão, instalação, tag e release;
- resultados datados;
- bloqueios específicos de release.

Registros históricos `REPROVADO` e `NÃO PRONTO` devem ser preservados.

## CHANGELOG.md

Responsabilidade:

- histórico cronológico de mudanças visíveis;
- itens adicionados, alterados, corrigidos ou documentados.

Não deve ser usado como checklist operacional.

## Specs

Responsabilidade:

- comportamento normativo;
- contratos;
- invariantes;
- limites arquiteturais.

Specs não devem ser substituídas por documentação de estado.

## ADRs

Responsabilidade:

- decisões arquiteturais;
- contexto;
- alternativas;
- consequências;
- estado da decisão.

ADRs aceitos não devem ser duplicados como perguntas ainda abertas.

# Tratamento Da Missão 0001

Registrar formalmente que:

- a série versionada de missões disponível começa em `0002`;
- não existe evidência suficiente de que uma missão `0001` tenha sido perdida,
  apagada ou executada;
- o identificador `0001` fica reservado como marco histórico da fundação
  prévia à série versionada;
- a reserva evita renumeração retroativa;
- a reserva não representa missão concluída;
- a reserva não deve aumentar contadores de missões executadas;
- a reserva não deve aparecer em `missions/queue`;
- a reserva não deve aparecer em `missions/running`;
- a reserva não deve aparecer em `missions/done`;
- a reserva não deve aparecer em `missions/failed`;
- não deve ser criado arquivo fictício `missions/done/0001-*.md`;
- não devem ser alterados IDs das missões existentes.

Atualizar `docs/history/mission-milestones.md` para refletir:

- a reserva histórica do ID `0001`;
- a série executável disponível de `0002` a `0108`;
- o total factual de 107 missões concluídas antes da execução da 0109;
- os marcos de `0101` a `0108`;
- a distinção entre ID reservado e missão executada.

Após a conclusão da própria 0109, qualquer contador atualizado deve considerar
a missão 0109 conforme o estado real produzido pelo runner.

# Auditoria De Duplicação

Criar:

- `docs/audits/documentation-deduplication-0109.md`

O relatório deve registrar:

- documentos revisados;
- responsabilidade de cada documento;
- blocos repetidos identificados;
- documentos escolhidos como fontes canônicas;
- trechos substituídos por resumos e links;
- contradições encontradas;
- contradições corrigidas;
- conteúdo histórico preservado;
- decisões abertas preservadas;
- arquivos não alterados e justificativa;
- riscos restantes de duplicação.

O relatório deve ser factual e datado.

Não deve se tornar uma nova fonte paralela do estado do projeto.

# Matriz De Fontes Canônicas

Adicionar em documento apropriado uma matriz compacta equivalente a:

| Informação | Fonte canônica |
| --- | --- |
| Estado de implementação | `docs/alignment/implementation-status.md` |
| Estado narrativo atual | `docs/alignment/current-state.md` |
| Arquitetura e fronteiras | `docs/alignment/architecture-map.md` |
| Specs normativas | `specs/framework/` |
| Decisões arquiteturais | `docs/architecture/decisions/` |
| Perguntas abertas | `docs/alignment/open-questions.md` |
| Roadmap estratégico | `docs/alignment/roadmap.md` |
| Backlog de missões | `docs/roadmap/mission-backlog.md` |
| Histórico de missões | `docs/history/mission-milestones.md` |
| Histórico de mudanças | `CHANGELOG.md` |
| Evidências de release | `docs/release/` |
| Auditorias datadas | `docs/audits/` |

Preferir incorporar essa matriz em um documento existente de alinhamento.

Não criar um novo documento permanente apenas para repetir essa matriz, salvo
necessidade arquitetural claramente justificada.

# Estratégia De Redução

Para cada duplicação encontrada:

1. identificar a fonte canônica;
2. preservar no documento consumidor somente o resumo necessário;
3. substituir detalhes repetidos por link relativo válido;
4. preservar conteúdo histórico datado;
5. não apagar evidências;
6. não apagar justificativas arquiteturais;
7. não apagar decisões alternativas registradas em ADR;
8. não transformar documento histórico em documento vivo;
9. não transformar documento normativo em checklist;
10. não introduzir links para arquivos locais ignorados.

# Documentos Prioritários

Revisar, no mínimo:

- README.md
- CHANGELOG.md
- docs/alignment/implementation-status.md
- docs/alignment/current-state.md
- docs/alignment/architecture-map.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/history/mission-milestones.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/architecture/execution-governance-0107.md
- docs/audits/spec-adr-integration-review-0108.md
- docs/release/public-alpha-readiness.md
- docs/release/alpha-readiness-diagnostic.md
- docs/release/pre-tag-checklist-execution.md

Usar amostragem dos demais documentos para verificar repetição relevante.

Não reescrever todos os arquivos indiscriminadamente.

# Preservação Histórica

Não apagar nem alterar retrospectivamente:

- resultados históricos de testes;
- diagnósticos de instalação limpa;
- diagnósticos de prontidão alfa;
- checklists pré-tag executados;
- decisões e datas registradas;
- achados de auditorias anteriores;
- estados históricos `REPROVADO`;
- estados históricos `NÃO PRONTO`;
- limitações vigentes na data de cada documento.

Quando um documento histórico estiver desatualizado por natureza, incluir
referência clara para o estado atual sem mudar sua conclusão original.

# Contadores E Estado De Missões

Não usar número do maior ID como sinônimo automático de quantidade executada.

Contadores devem derivar do estado factual das pastas de missão.

Distinguir:

- maior identificador;
- quantidade de arquivos concluídos;
- IDs reservados;
- missões em fila;
- missões em execução;
- missões falhadas.

Não codificar contadores dinâmicos em vários documentos.

Manter números históricos somente onde forem necessários e datados.

# Escopo Permitido

- README.md
- CHANGELOG.md
- docs/
- missions/done/0109-... apenas pela movimentação feita pelo runner

# Escopo Proibido

- src/
- tests/
- scripts/
- .github/
- pyproject.toml
- AGENTS.md
- missions/base/
- missions/templates/
- arquivos de missões anteriores
- alteração de IDs de missões
- criação de missão `0001`
- criação de arquivo em `missions/done` para a missão `0001`
- remoção de relatórios históricos
- alteração de comportamento de runtime
- alteração de contratos Python
- provider real
- rede
- banco
- PostgreSQL
- pgvector
- RAG
- MCP
- API externa
- internacionalização
- tag
- release
- publicação de pacote
- push automático
- criação da missão 0110

# Regras De Precisão

Toda afirmação de estado deve ser compatível com
`docs/alignment/implementation-status.md`.

Toda afirmação de integração deve apontar para evidência de código e teste.

Toda afirmação histórica deve indicar faixa, missão, commit, documento ou data
quando disponível.

Não declarar:

- release pronta;
- tag autorizada;
- instalação limpa aprovada;
- provider real validado;
- rede validada;
- banco integrado;
- RAG implementado;
- pgvector integrado;
- produção pronta;
- segurança absoluta;
- arquitetura final imutável.

# Testes E Validações Obrigatórias

Executar:

- pytest;
- python3 -m compileall src;
- python3 -m vercosa_ai_framework.cli.main docs-links;
- python3 -m vercosa_ai_framework.cli.main doctor;
- git diff --check;
- git status --short;
- git diff --stat;
- revisão completa do diff;
- verificação de ausência de alterações em `src/`;
- verificação de ausência de alterações em `tests/`;
- verificação de ausência de alterações em `scripts/`;
- verificação de ausência de links para `logs/` e arquivos ignorados;
- verificação de que `implementation-status.md` permanece fonte canônica;
- verificação de que não foi criado arquivo de missão `0001`;
- verificação de que contadores distinguem ID reservado de missão executada;
- verificação de que relatórios históricos mantiveram suas conclusões originais.

# Critérios De Aceite

A missão será aceita somente se:

- `implementation-status.md` permanecer como checklist canônico;
- documentos consumidores apontarem para a fonte canônica;
- duplicações relevantes forem reduzidas;
- responsabilidades documentais forem explicitadas;
- contradições de estado forem corrigidas;
- registros históricos forem preservados;
- a reserva histórica do ID `0001` for documentada;
- nenhum arquivo de missão `0001` for criado;
- nenhuma missão existente for renumerada;
- os marcos de `0101` a `0108` forem registrados;
- o relatório de auditoria 0109 existir;
- nenhuma alteração em código ocorrer;
- nenhuma alteração em testes ocorrer;
- links Markdown permanecerem válidos;
- testes e compileall permanecerem verdes;
- Git não contiver mudanças não relacionadas;
- a missão gerar um único commit próprio.

# Movimentação Da Missão

O agente não deve mover manualmente este arquivo de `missions/running` para
`missions/done`.

A movimentação final é responsabilidade exclusiva do runner seguro.

O agente deve apenas:

- revisar;
- editar a documentação permitida;
- validar;
- criar o commit exclusivo da missão.

# Entrega Esperada

Entregar:

- documentação com menor duplicação;
- responsabilidades documentais explícitas;
- checklist canônico preservado;
- referências cruzadas corrigidas;
- relatório de auditoria 0109;
- histórico de missões atualizado até 0108;
- reserva histórica do ID `0001` formalizada;
- nenhuma alteração de código;
- nenhuma alteração de comportamento;
- commit exclusivo da missão 0109.

Não executar push.
Não criar missão 0110.
Não criar missão 0001.
Não mover manualmente o arquivo da missão.

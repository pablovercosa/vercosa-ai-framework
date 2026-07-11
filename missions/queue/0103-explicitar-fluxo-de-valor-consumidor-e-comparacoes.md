---
id: "0103"
title: "Explicitar fluxo de valor consumidor e diferenciação"
base_contract: "v1"
roles:
  - product-strategy-auditor
  - comparative-researcher
  - technical-documentation-writer
agents:
  - framework-architect
network: allow
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

Explicitar no README o problema que o Vercosa AI Framework resolve, seu fluxo principal de valor, seu consumidor principal, seus limites e seu estado real, além de criar uma comparação factual e atualizada entre o VAF, OpenSpec e GitHub Spec Kit.

# Contexto Específico

A auditoria da missão 0101 classificou o projeto como `ALINHADO COM RESSALVAS`.

O projeto permanece alinhado à proposta de uma plataforma de Harness Engineering orientada por especificações, mas ainda não demonstrou de ponta a ponta o fluxo:

Mission
→ Workflow
→ Task
→ Agent
→ Capability
→ Skill
→ Tool
→ Provider

A documentação pública deve explicar com clareza qual problema o projeto pretende resolver, sem apresentar como integrado aquilo que hoje existe somente como MVP, contrato, módulo isolado ou preparação futura.

O Mission Runner é infraestrutura operacional de suporte. Ele não deve ser apresentado como o produto inteiro.

O README deve explicar que o problema central é transformar desenvolvimento com IA baseado em prompts improvisados em um processo controlado, reproduzível, auditável e orientado por especificações.

OpenSpec e GitHub Spec Kit devem ser tratados como projetos potencialmente complementares, não como adversários a serem diminuídos.

A comparação deve distinguir rigorosamente:

- capacidade documentada oficialmente por cada projeto;
- capacidade comprovadamente implementada hoje no VAF;
- capacidade planejada ou pretendida para o VAF;
- hipótese arquitetural ainda não implementada.

O acesso à rede está autorizado exclusivamente para consultar fontes públicas oficiais relacionadas ao OpenSpec e ao GitHub Spec Kit.

Não utilizar blogs, vídeos, publicações promocionais de terceiros, agregadores ou comparações não oficiais como fonte principal.

# Entradas Específicas

## Repositório local

- README.md
- CHANGELOG.md
- AGENTS.md
- pyproject.toml
- docs/audits/objective-and-scope-alignment-audit.md
- docs/alignment/current-state.md
- docs/alignment/implementation-status.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/operations/mission-execution-contract.md
- specs/framework/
- src/vercosa_ai_framework/
- tests/

## Fontes oficiais mínimas do OpenSpec

- https://github.com/Fission-AI/OpenSpec
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md
- https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md

## Fontes oficiais mínimas do GitHub Spec Kit

- https://github.com/github/spec-kit
- https://github.github.com/spec-kit/
- https://github.github.com/spec-kit/quickstart.html
- https://github.github.com/spec-kit/concepts/sdd.html
- https://github.github.com/spec-kit/reference/overview.html
- https://github.github.com/spec-kit/reference/integrations.html
- https://github.github.com/spec-kit/reference/extensions.html

# Entregáveis

## 1. Atualizar README.md

Reorganizar o README sem criar repetição desnecessária e sem apagar informações técnicas ainda relevantes.

O README deve conter, em posição visível antes das instruções operacionais detalhadas, conteúdo equivalente às seguintes seções:

### O problema que o projeto resolve

Explicar os problemas recorrentes do desenvolvimento assistido por IA:

- dependência de prompts improvisados;
- repetição ou esquecimento de regras;
- ampliação silenciosa de escopo;
- seleção de modelos e providers sem política clara;
- crescimento de contexto sem controle;
- interrupções por quota e estados inconsistentes;
- falta de rastreabilidade entre objetivo, especificação, implementação e teste;
- ações perigosas sem governança;
- dificuldade de diferenciar planejado, implementado, integrado e validado.

### Como o Vercosa AI Framework pretende resolver

Apresentar o fluxo conceitual:

objetivo
→ especificação
→ missão
→ políticas e permissões
→ composição de contexto
→ agentes e skills
→ seleção de modelo
→ runtime e provider
→ execução
→ testes
→ evidências
→ auditoria
→ commit

Deixar claro que parte desse fluxo ainda não está integrada de ponta a ponta.

### O produto não é somente o Mission Runner

Explicar que o Mission Runner e o batch são infraestrutura operacional.

Apresentar o produto maior como plataforma formada, quando aplicável, por:

- Policy Engine;
- Guardian Engine;
- Context Router;
- Token Budget Manager;
- Model Selection Engine;
- Provider Gateway;
- Runtime Adapter;
- Agent Orchestrator;
- Skills;
- Tools;
- Capabilities;
- Knowledge Hub;
- persistência;
- Audit/Event Log;
- Mission Runner.

Diferenciar componentes implementados, componentes parcialmente integrados e componentes planejados.

### Para quem o projeto é útil

Definir consumidores principais plausíveis:

- desenvolvedor individual que utiliza múltiplos agentes e ferramentas;
- equipe que executa desenvolvimento assistido por IA;
- projeto que exige governança, segurança e rastreabilidade;
- ambiente com múltiplos modelos, providers ou runtimes;
- projeto orientado por especificações;
- pipeline de execução prolongada que precisa preservar contexto e estado.

Não inventar adoção real nem usuários reais sem evidência.

### O que o framework não pretende substituir

Registrar que o VAF não pretende substituir:

- modelos de IA;
- Git;
- CI/CD;
- bancos de dados;
- OpenCode ou outros executores;
- ferramentas completas de Specification-Driven Development;
- controles do sistema operacional;
- revisão humana.

Registrar que PostgreSQL, pgvector, RAG e internacionalização somente devem avançar quando servirem ao fluxo principal.

### O que já funciona

Descrever factual e resumidamente:

- fila de missões;
- execução segura;
- batch;
- parada na primeira falha;
- recuperação;
- commit por missão;
- bloqueio de push automático;
- detecção de limite de uso;
- testes;
- validações locais;
- logs e eventos;
- diagnósticos pela CLI;
- contrato base de execução;
- formato compacto;
- composição determinística de contexto.

Não usar existência de arquivo como prova de integração.

Não fixar quantidade de testes no README, salvo se acompanhada de data e commit. Preferir descrição estável.

### O que ainda não está completo

Explicar claramente:

- ausência de fluxo público completo de ponta a ponta;
- CLI predominantemente diagnóstica;
- motores centrais ainda parcialmente integrados;
- providers reais adiados;
- persistência externa adiada;
- PostgreSQL, pgvector e RAG adiados;
- internacionalização adiada;
- tag alfa bloqueada até demonstração do fluxo de valor e cumprimento dos gates.

### Comparação com outras abordagens

Criar uma seção curta explicando que OpenSpec e GitHub Spec Kit atuam principalmente na organização e execução de processos orientados por especificações, enquanto o VAF pretende concentrar sua diferenciação na execução governada e auditável.

A seção deve apontar para:

- docs/comparacoes.md

Não incluir no README o fechamento denominado “Definição mais curta do projeto” nem a pergunta final usada para orientar a auditoria.

## 2. Criar docs/comparacoes.md

Criar um documento público em português do Brasil com título apropriado.

O documento deve comparar:

- Vercosa AI Framework;
- OpenSpec;
- GitHub Spec Kit.

Deve conter no mínimo:

1. objetivo da comparação;
2. data da consulta das fontes;
3. metodologia;
4. fontes oficiais consultadas;
5. problema principal tratado por cada projeto;
6. unidade principal de trabalho;
7. fluxo operacional documentado;
8. artefatos produzidos;
9. integração com agentes de codificação;
10. tratamento de especificações;
11. planejamento e decomposição de tarefas;
12. políticas e permissões;
13. seleção de modelos, providers e runtimes;
14. contexto e orçamento de tokens;
15. fila e execução em batch;
16. retomada e recuperação;
17. auditoria e evidências;
18. extensibilidade;
19. pontos de sobreposição;
20. diferenças reais;
21. possibilidades de integração;
22. riscos de duplicação;
23. limitações da comparação;
24. estado atual versus visão pretendida do VAF;
25. conclusão factual.

A tabela principal deve possuir colunas separadas para:

- OpenSpec segundo fontes oficiais;
- GitHub Spec Kit segundo fontes oficiais;
- VAF atualmente comprovado;
- VAF planejado ou pretendido.

Não juntar “VAF atual” e “VAF futuro” na mesma coluna.

## 3. Registrar a fronteira arquitetural

Avaliar e documentar, sem implementar, a possibilidade de uma fronteira semelhante a:

- SpecificationProvider

Possíveis adaptadores conceituais:

- OpenSpecProvider;
- SpecKitProvider;
- NativeMarkdownProvider.

Essa possibilidade deve ser identificada como:

- hipótese arquitetural;
- decisão pendente;
- não implementada;
- sujeita às missões de integração 0104–0108.

Não criar interfaces Python, classes, módulos, Specs ou ADRs apenas para materializar essa hipótese nesta missão.

## 4. Atualizar documentos de alinhamento

Atualizar somente quando necessário:

- docs/alignment/current-state.md;
- docs/alignment/implementation-status.md;
- docs/alignment/roadmap.md;
- docs/alignment/open-questions.md;
- docs/roadmap/mission-backlog.md;
- CHANGELOG.md;
- índice canônico de documentação, se existir.

Registrar a conclusão da missão 0103 sem transformar o CHANGELOG em checklist.

# Regras Da Pesquisa Comparativa

1. Utilizar somente fontes oficiais como base para afirmações sobre OpenSpec e Spec Kit.

2. Registrar links diretos para as fontes.

3. Registrar a data da consulta.

4. Não copiar grandes trechos das fontes.

5. Parafrasear com fidelidade.

6. Não comparar popularidade, estrelas, adoção ou comunidade como medida de qualidade.

7. Não declarar que o VAF é superior.

8. Não apresentar ranking.

9. Não afirmar que um recurso não existe apenas porque não foi encontrado.

10. Quando uma capacidade não estiver documentada nas fontes consultadas, usar formulação equivalente a:
   - “não identificado nas fontes oficiais consultadas”;
   - “não é apresentado como responsabilidade central nas fontes consultadas”.

11. Não tratar ausência de documentação como prova de ausência de implementação.

12. Não tratar intenção arquitetural do VAF como funcionalidade existente.

13. Não usar o Mission Runner como prova de que toda a arquitetura VAF está integrada.

14. Se as fontes oficiais tiverem mudado em relação a descrições anteriores, usar o estado oficial atual.

15. Registrar divergências ou incertezas.

16. Manter tom técnico, neutro e não promocional.

# Restrições Específicas

- Não alterar código Python.
- Não alterar scripts shell.
- Não alterar workflows de CI.
- Não adicionar dependências.
- Não implementar SpecificationProvider.
- Não implementar adapters.
- Não implementar OpenSpec.
- Não implementar Spec Kit.
- Não instalar OpenSpec ou Spec Kit.
- Não executar comandos de inicialização dessas ferramentas.
- Não criar agentes ou skills.
- Não implementar PostgreSQL.
- Não implementar pgvector.
- Não implementar RAG.
- Não implementar internacionalização.
- Não criar tag.
- Não criar release.
- Não publicar pacote.
- Não acessar banco.
- Não chamar providers de IA durante testes.
- Não fazer push.
- Não ampliar silenciosamente o escopo além de documentação e alinhamento.

# Critérios Específicos De Aceite

- README.md explica claramente o problema resolvido pelo VAF.
- README.md apresenta o fluxo conceitual esperado.
- README.md diferencia produto e Mission Runner.
- README.md identifica consumidores principais plausíveis.
- README.md explica o que o projeto não substitui.
- README.md distingue o que funciona do que ainda não está completo.
- README.md não promete fluxo integrado inexistente.
- README.md possui link funcional para docs/comparacoes.md.
- docs/comparacoes.md existe.
- docs/comparacoes.md utiliza fontes oficiais atuais.
- A data da consulta está registrada.
- OpenSpec é descrito conforme sua documentação oficial atual.
- GitHub Spec Kit é descrito conforme sua documentação oficial atual.
- A comparação diferencia VAF atual de VAF pretendido.
- A comparação não declara superioridade.
- A comparação não apresenta ranking.
- Ausência de evidência não é tratada como prova de ausência.
- Sobreposições e complementaridades estão registradas.
- Riscos de duplicação estão registrados.
- SpecificationProvider aparece apenas como hipótese arquitetural não implementada.
- O backlog registra a conclusão da 0103 e preserva 0104–0110.
- CHANGELOG.md registra somente a mudança pública relevante.
- Nenhum código, script ou workflow foi alterado.
- Links da documentação passam na validação disponível.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

# Referência Operacional

O contrato base de execução está em `missions/base/EXECUTION_CONTRACT.md` e é composto obrigatoriamente pelo runner. Não copie o contrato para dentro da missão.

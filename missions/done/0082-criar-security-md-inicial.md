Leia obrigatoriamente:
- AGENTS.md
- README.md
- CONTRIBUTING.md
- docs/legal/README.md
- docs/legal/usage-policy.md
- docs/legal/license-notes.md
- docs/release/public-alpha-readiness.md
- docs/architecture/module-index.md
- docs/architecture/post-integration-architecture-review.md
- docs/architecture/audit-event-architecture.md
- docs/alignment/current-state.md
- docs/alignment/roadmap.md
- docs/alignment/open-questions.md
- docs/roadmap/mission-backlog.md
- docs/operations/safe-runner-usage.md
- docs/operations/batch-execution-playbook.md
- docs/operations/post-batch-validation-checklist.md
- src/vercosa_ai_framework/audit/README.md
- src/vercosa_ai_framework/guardian/README.md
- src/vercosa_ai_framework/policy/README.md
- src/vercosa_ai_framework/providers/README.md
- src/vercosa_ai_framework/runtime/README.md
- src/vercosa_ai_framework/tools/README.md

Leia também, se existirem:
- SECURITY.md
- docs/security/README.md
- docs/security/vulnerability-reporting.md
- CODE_OF_CONDUCT.md
- LICENSE

Assuma o papel de:
- security-documentation-agent;
- open-source-maintainer;
- risk-reviewer;
- release-preparation-agent;
- technical-editor.

Missão:
Criar SECURITY.md inicial.

Objetivo:
Criar uma política inicial de segurança para o Vercosa AI Framework, adequada ao estágio atual do projeto, explicando como reportar vulnerabilidades, quais versões são suportadas, quais limites de segurança existem, quais práticas são esperadas de contribuidores e quais áreas exigem atenção especial em um framework de Harness Engineering para agentes de IA.

Contexto:
- O projeto caminha para uma futura alfa pública.
- O projeto ainda está em desenvolvimento.
- O projeto ainda não publicou release alfa.
- O projeto ainda não possui processo público maduro de segurança.
- O projeto já possui política inicial de uso responsável.
- O projeto já possui documentação legal inicial.
- O projeto já possui Audit/Event Log inicial.
- O projeto já possui Guardian Engine e Policy Engine.
- O projeto pode futuramente integrar providers, runtimes, tools, bancos, RAG, embeddings e automações externas.
- A política de segurança deve ser inicial, conservadora e factual.
- A política não deve prometer SLA.
- A política não deve prometer conformidade regulatória.
- A política não deve prometer segurança absoluta.
- A política não deve publicar e-mail privado se não houver decisão explícita no repositório.
- Se não houver canal público definido para vulnerabilidades, documentar que o canal será definido antes da release pública.
- Esta missão não deve implementar mecanismos técnicos.
- Esta missão não deve criar workflow de CI.
- Esta missão não deve alterar código.
- Esta missão não deve alterar scripts.

Entregáveis obrigatórios:
1. Criar arquivo:
   - SECURITY.md

2. Criar diretório, se necessário:
   - docs/security/

3. Criar arquivo:
   - docs/security/README.md

4. Criar arquivo:
   - docs/security/vulnerability-reporting.md

5. Atualizar:
   - README.md
   - CONTRIBUTING.md
   - docs/release/public-alpha-readiness.md
   - docs/roadmap/mission-backlog.md

6. Atualizar, se necessário:
   - docs/legal/usage-policy.md
   - docs/alignment/current-state.md
   - docs/alignment/roadmap.md
   - docs/alignment/open-questions.md

7. Não alterar código Python.

8. Não alterar scripts shell.

9. Não adicionar dependências.

Requisitos para SECURITY.md:
1. O documento deve estar em português do Brasil.

2. Explicar que o projeto ainda está em desenvolvimento.

3. Explicar que ainda não há release estável.

4. Explicar que a política é inicial e será amadurecida antes de uma release pública mais ampla.

5. Incluir seção de versões suportadas.

6. Como ainda não há release formal, registrar de forma conservadora:
   - branch main é a linha ativa de desenvolvimento;
   - versões estáveis ainda não foram publicadas;
   - suporte formal a versões será definido em release futura.

7. Incluir seção sobre reporte de vulnerabilidades.

8. Se não houver canal público definido, não inventar e-mail.

9. Se não houver canal público definido, registrar:
   - canal de reporte será definido antes da alfa pública;
   - por enquanto, vulnerabilidades devem ser tratadas com cautela e sem exposição pública de detalhes sensíveis;
   - detalhes exploráveis não devem ser publicados em issues públicas antes de análise.

10. Incluir seção sobre o que é considerado vulnerabilidade relevante para o projeto:
   - vazamento de secrets;
   - registro indevido de tokens;
   - execução destrutiva sem aprovação explícita;
   - bypass de políticas;
   - bypass do Guardian Engine;
   - execução indevida de tools;
   - execução indevida de providers;
   - falha de isolamento entre runtime e framework;
   - exposição de prompts sensíveis;
   - persistência indevida de dados sensíveis;
   - uso inseguro de credenciais;
   - alteração perigosa em scripts operacionais;
   - automações que podem causar dano sem revisão humana.

11. Incluir seção sobre o que pode não ser vulnerabilidade nesta fase:
   - ausência de hardening de produção;
   - ausência de SLA;
   - ausência de suporte a múltiplas versões;
   - ausência de CI público;
   - ausência de dashboard;
   - ausência de autenticação externa;
   - limitações documentadas de projeto em desenvolvimento.

12. Incluir seção de práticas recomendadas para usuários:
   - não colocar secrets em missões;
   - não colocar tokens em Markdown;
   - revisar comandos antes de executar;
   - evitar execução com sudo;
   - usar menor privilégio;
   - testar em ambiente isolado;
   - validar git status antes de executar batch;
   - validar pytest e compileall antes de push;
   - não ativar auto-push sem decisão explícita;
   - revisar logs antes de publicar.

13. Incluir seção de práticas recomendadas para contribuidores:
   - não registrar credenciais;
   - não adicionar providers externos sem missão específica;
   - não adicionar dependências de segurança duvidosa;
   - não alterar scripts críticos sem testes;
   - não reduzir validações;
   - não enfraquecer Policy Engine ou Guardian Engine sem justificativa;
   - não transformar warnings de segurança em sucesso silencioso;
   - documentar riscos quando alterar runtime, providers, tools ou auditoria.

14. Incluir seção de limites atuais de segurança:
   - sem auditoria persistente externa;
   - sem política pública madura de vulnerabilidades;
   - sem CI público;
   - sem release estável;
   - sem hardening para produção;
   - sem sandbox externo garantido;
   - sem integração real com secret manager;
   - sem mecanismo técnico completo de redaction;
   - sem gestão formal de chaves ou tokens.

15. Incluir seção sobre IA e segurança operacional:
   - modelo não deve ser tratado como autoridade final;
   - comandos devem ser revisados por humano;
   - missões devem ter escopo, restrições e critérios de aceite;
   - batch não deve ser execução cega;
   - uso de tools/providers deve ser controlado;
   - saída de modelos pode conter erro;
   - limites de API/quota não devem ser contornados de forma insegura.

16. Incluir links relativos para:
   - docs/legal/usage-policy.md
   - docs/security/vulnerability-reporting.md
   - docs/operations/batch-execution-playbook.md
   - docs/architecture/audit-event-architecture.md
   - CONTRIBUTING.md

17. Não prometer prazo de resposta.

18. Não prometer remuneração por bugs.

19. Não prometer conformidade regulatória.

20. Não usar linguagem jurídica excessiva.

21. Não usar tom alarmista.

Requisitos para docs/security/README.md:
1. Explicar o propósito da pasta docs/security.

2. Apontar para:
   - SECURITY.md
   - docs/security/vulnerability-reporting.md
   - docs/legal/usage-policy.md
   - CONTRIBUTING.md

3. Explicar que a documentação de segurança é inicial.

4. Explicar que ela será amadurecida conforme o projeto se aproximar de release pública.

5. Não duplicar todo o conteúdo do SECURITY.md.

Requisitos para docs/security/vulnerability-reporting.md:
1. Explicar como relatar vulnerabilidades de forma responsável.

2. Se não houver canal público definido, registrar essa pendência claramente.

3. Orientar a não publicar:
   - exploits;
   - tokens;
   - credenciais;
   - dados sensíveis;
   - instruções destrutivas;
   - detalhes exploráveis antes de análise.

4. Explicar o tipo de informação útil em um reporte:
   - descrição;
   - impacto esperado;
   - passos de reprodução em ambiente controlado;
   - arquivos ou módulos envolvidos;
   - versão, commit ou branch;
   - logs sanitizados;
   - mitigação sugerida, se houver.

5. Explicar que logs devem ser sanitizados.

6. Explicar que segredos nunca devem ser anexados.

7. Explicar que o projeto ainda não possui programa formal de bug bounty.

8. Não prometer SLA.

9. Não prometer resposta em prazo específico.

10. Não inventar e-mail ou canal externo.

Requisitos para README.md:
1. Adicionar link curto para SECURITY.md.

2. Adicionar link curto para política de uso responsável, se ainda não estiver claro.

3. Manter README enxuto.

4. Não duplicar a política de segurança inteira.

5. Não declarar o projeto como pronto para produção.

Requisitos para CONTRIBUTING.md:
1. Adicionar referência ao SECURITY.md.

2. Adicionar seção curta sobre segurança em contribuições, se ainda não existir.

3. Reforçar:
   - não incluir secrets;
   - não incluir tokens;
   - não incluir credenciais;
   - sanitizar logs;
   - reportar vulnerabilidades com cautela;
   - não abrir issue pública com detalhes exploráveis antes de análise.

4. Não transformar CONTRIBUTING.md em política de segurança completa.

Requisitos para docs/release/public-alpha-readiness.md:
1. Atualizar checklist para marcar SECURITY.md como criado.

2. Manter pendentes itens ainda não executados, como:
   - CODE_OF_CONDUCT.md;
   - templates de issue;
   - templates de pull request;
   - changelog inicial;
   - versão alfa inicial;
   - teste de instalação limpa;
   - internacionalização dos READMEs.

3. Não declarar alfa pública como publicada.

Requisitos para docs/roadmap/mission-backlog.md:
1. Marcar SECURITY.md inicial como concluído ou em progresso conforme esta missão.

2. Manter como futuras:
   - política pública madura de vulnerabilidades;
   - templates de issue;
   - templates de pull request;
   - CODE_OF_CONDUCT.md;
   - CI público;
   - revisão de segurança antes de release alfa.

3. Não criar missões novas na fila.

Requisitos para docs/alignment/open-questions.md:
1. Atualizar somente se houver pendências claras.

2. Perguntas possíveis:
   - qual canal público será usado para vulnerabilidades;
   - haverá e-mail dedicado;
   - haverá GitHub Security Advisories;
   - haverá política de disclosure;
   - haverá bug bounty;
   - qual nível de suporte será dado à alfa pública.

Requisitos gerais:
1. Tudo deve estar em português do Brasil.

2. Usar linguagem conservadora e factual.

3. Diferenciar:
   - política inicial;
   - processo público maduro;
   - release alfa;
   - produção;
   - suporte formal.

4. Não prometer maturidade inexistente.

5. Não prometer segurança absoluta.

6. Não prometer SLA.

7. Não inventar canal externo.

8. Não expor dados pessoais.

9. Não alterar código.

10. Não alterar scripts.

11. Não adicionar dependências.

12. Usar links relativos corretos.

13. Usar blocos Markdown quando úteis.

14. Controlar corretamente a quantidade de crases nos blocos Markdown.

Restrições:
- Não alterar código Python.
- Não alterar scripts shell.
- Não implementar mecanismos técnicos de segurança.
- Não criar CI.
- Não criar GitHub Actions.
- Não criar CODE_OF_CONDUCT.md nesta missão.
- Não criar templates de issue.
- Não criar templates de pull request.
- Não criar changelog.
- Não criar versão.
- Não criar tag.
- Não publicar release.
- Não criar README.en.md.
- Não criar README.es.md.
- Não internacionalizar READMEs.
- Não adicionar dependências.
- Não acessar rede.
- Não acessar banco.
- Não chamar OpenAI.
- Não chamar Gemini.
- Não chamar Ollama.
- Não chamar Claude.
- Não chamar OpenCode.
- Não acessar MCPs.
- Não executar providers.
- Não executar missões.
- Não fazer git push.
- Não usar sudo.
- Não alterar configs globais.
- Não reescrever histórico Git.
- Não fazer force push.
- Não usar git add .
- Documentação e mensagens devem estar em português do Brasil.

Critérios de aceite:
- SECURITY.md existe.
- docs/security/README.md existe.
- docs/security/vulnerability-reporting.md existe.
- SECURITY.md deixa claro que o projeto ainda está em desenvolvimento.
- SECURITY.md não promete SLA.
- SECURITY.md não promete conformidade regulatória.
- SECURITY.md não inventa canal externo inexistente.
- SECURITY.md explica práticas seguras para usuários e contribuidores.
- SECURITY.md aponta para documentos relevantes.
- README.md aponta para SECURITY.md.
- CONTRIBUTING.md aponta para SECURITY.md.
- docs/release/public-alpha-readiness.md registra SECURITY.md como criado.
- docs/roadmap/mission-backlog.md foi atualizado se necessário.
- Nenhum código Python foi alterado.
- Nenhum script shell foi alterado.
- Nenhuma dependência foi adicionada.
- pytest passa.
- python3 -m compileall src passa.
- O commit automático usa mensagem em português do Brasil.

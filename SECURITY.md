# Política Inicial De Segurança

O Vercosa AI Framework ainda está em desenvolvimento. Não há release estável publicada, não há release alfa pública publicada e esta política é inicial, conservadora e sujeita a amadurecimento antes de uma abertura pública mais ampla.

Esta política não promete segurança absoluta, prazo de resposta, remuneração por bugs, conformidade regulatória ou adequação a produção. Ela registra expectativas mínimas de segurança para usuários, contribuidores e mantenedores enquanto o projeto evolui.

## Versões Suportadas

| Linha | Status | Observação |
| --- | --- | --- |
| `main` | desenvolvimento ativo | Linha ativa de desenvolvimento do projeto. Pode mudar sem garantia de estabilidade. |
| versões estáveis | não publicadas | Ainda não há versão estável, tag estável ou pacote publicado. |
| suporte formal a versões | futuro | Será definido em release futura, quando houver política de versionamento aprovada. |

Como ainda não há release formal, correções e revisões de segurança devem ser tratadas no contexto da branch `main` e das missões aprovadas do projeto.

## Reporte De Vulnerabilidades

O projeto ainda não possui canal público definitivo para reporte privado de vulnerabilidades. Esse canal deve ser definido antes da alfa pública.

Até que esse processo esteja definido:

- trate vulnerabilidades com cautela;
- não publique detalhes exploráveis em issues públicas antes de análise;
- não publique exploits, tokens, credenciais, dados sensíveis ou instruções destrutivas;
- sanitize logs antes de compartilhar;
- use descrições objetivas, sem anexar segredos reais.

Orientações detalhadas estão em [docs/security/vulnerability-reporting.md](docs/security/vulnerability-reporting.md).

## Vulnerabilidades Relevantes Para O Projeto

No contexto do Vercosa AI Framework, vulnerabilidades relevantes podem incluir:

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

Áreas como Runtime Adapter, Provider Gateway, Tools, Skills, Capabilities, Policy Engine, Guardian Engine, Audit/Event Log, Context Router, Knowledge Hub, RAG futuro, embeddings futuros, bancos futuros e automações externas exigem atenção especial porque ampliam superfície de execução, dados, credenciais, logs e efeitos colaterais.

## O Que Pode Não Ser Vulnerabilidade Nesta Fase

Alguns limites são esperados no estágio atual do projeto e podem não ser tratados como vulnerabilidade por si só:

- ausência de hardening de produção;
- ausência de SLA;
- ausência de suporte a múltiplas versões;
- ausência de CI público;
- ausência de dashboard;
- ausência de autenticação externa;
- limitações documentadas de projeto em desenvolvimento.

Esses pontos ainda podem virar riscos, lacunas ou próximos passos, mas não devem ser interpretados como promessa de maturidade inexistente.

## Práticas Recomendadas Para Usuários

- Não coloque secrets em missões.
- Não coloque tokens em Markdown.
- Revise comandos antes de executar.
- Evite execução com `sudo`.
- Use menor privilégio para filesystem, rede, providers, tools, runtimes e credenciais.
- Teste em ambiente isolado sempre que possível.
- Valide `git status` antes de executar batch.
- Valide `pytest` e `python3 -m compileall src` antes de push.
- Não ative auto-push sem decisão explícita.
- Revise logs antes de publicar, compartilhar ou anexar.

## Práticas Recomendadas Para Contribuidores

- Não registre credenciais.
- Não adicione providers externos sem missão específica.
- Não adicione dependências de segurança duvidosa.
- Não altere scripts críticos sem testes e revisão proporcional ao risco.
- Não reduza validações.
- Não enfraqueça Policy Engine ou Guardian Engine sem justificativa explícita.
- Não transforme warnings de segurança em sucesso silencioso.
- Documente riscos ao alterar runtime, providers, tools, auditoria, contexto, persistência ou automações.
- Sanitize logs, exemplos e fixtures antes de publicar.
- Reporte vulnerabilidades com cautela e sem expor detalhes exploráveis em canal público antes de análise.

## Limites Atuais De Segurança

O projeto ainda não possui:

- auditoria persistente externa;
- política pública madura de vulnerabilidades;
- CI público;
- release estável;
- hardening para produção;
- sandbox externo garantido;
- integração real com secret manager;
- mecanismo técnico completo de redaction;
- gestão formal de chaves ou tokens.

O Audit/Event Log atual é inicial, possui memória e persistência local JSONL opt-in, conforme [docs/architecture/audit-event-architecture.md](docs/architecture/audit-event-architecture.md). Ele não deve ser tratado como observabilidade externa, trilha imutável, retenção formal, rotação formal ou mecanismo completo de investigação de incidentes.

## IA E Segurança Operacional

O Vercosa AI Framework organiza o uso de agentes de IA, mas o modelo não deve ser tratado como autoridade final.

Práticas esperadas:

- comandos devem ser revisados por humano;
- missões devem ter escopo, restrições e critérios de aceite;
- batch não deve ser execução cega;
- uso de tools e providers deve ser controlado;
- saída de modelos pode conter erro;
- limites de API, quota, rate limit e custo não devem ser contornados de forma insegura;
- prompts, contexto e logs devem ser tratados como dados potencialmente sensíveis;
- validações locais continuam obrigatórias quando a missão exigir.

## Documentos Relacionados

- [Política inicial de uso responsável](docs/legal/usage-policy.md)
- [Reporte responsável de vulnerabilidades](docs/security/vulnerability-reporting.md)
- [Playbook de execução em batch](docs/operations/batch-execution-playbook.md)
- [Arquitetura de Audit/Event Log](docs/architecture/audit-event-architecture.md)
- [Guia inicial de contribuição](CONTRIBUTING.md)

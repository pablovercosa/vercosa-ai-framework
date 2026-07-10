# Changelog

Todas as mudanças relevantes do Vercosa AI Framework devem ser registradas neste arquivo quando afetarem comportamento público, arquitetura, operação, segurança, documentação pública ou preparação de release futura.

O projeto ainda está em desenvolvimento. Ainda não há release estável publicada, versão alfa publicada, tag de release ou pacote distribuído. Este changelog inicial registra a evolução já consolidada do projeto até o estado atual, sem criar release formal, sem definir versão definitiva e sem prometer estabilidade de produção.

Links úteis: [README.md](README.md) | [Política de versionamento](docs/release/versioning-policy.md) | [Plano da versão alfa](docs/release/alpha-version-plan.md) | [Checklist de alfa pública](docs/release/public-alpha-readiness.md) | [Backlog estratégico de missões](docs/roadmap/mission-backlog.md)

## Não publicado

### Adicionado

- Fundação modular inicial do framework como camada de Harness Engineering para agentes de IA, desenvolvimento orientado por especificações e execução governada.
- Evolução por missões em Markdown, com backlog estratégico, fila operacional, critérios de aceite, validações locais e rastreabilidade documental.
- Mission Runner local, fila em diretórios e runner seguro de uma missão.
- Runner seguro em batch, com batch como fluxo operacional padrão quando o bloco de missões estiver bem especificado, revisado e seguro.
- Policy Engine MVP para resolução determinística de políticas declarativas.
- Guardian Engine MVP para avaliação determinística de riscos, ações, comandos, pacotes de contexto e sinais textuais de limite de uso/API.
- Usage/API Limit Guard inicial para classificar logs já recebidos que indiquem quota, rate limit, billing hard limit, crédito insuficiente ou limite externo de API.
- Context Router, Token Budget Manager e `ContextPackage` determinísticos.
- Knowledge Hub MVP com ingestão Markdown, store em memória, busca textual e adaptação para candidatos de contexto.
- Model Selection Engine MVP com catálogo em memória, políticas resolvidas opcionais e requisitos opcionais derivados de orçamento de tokens.
- Provider Gateway MVP, cadeia inicial de Capabilities, Skills e Tools, e Runtime Adapter inicial para OpenCode.
- Audit/Event Log inicial em memória, com helpers opcionais para decisões de Policy, Guardian, Context e ciclo de vida de missão/batch.
- Persistência local JSONL opt-in para eventos auditáveis, sem banco, sem rede, sem dependências externas e sem ativação global obrigatória.
- CLI operacional inicial com comandos `status`, `missions`, `batch-summary`, `validate` e `doctor`.
- Empacotamento Python local mínimo em `pyproject.toml` com `setuptools`, descoberta em `src`, versão PEP 440 `0.1.0a1`, extra opcional `dev` para `pytest` e entrypoint local `vaf` para instalação editável em ambiente virtual.
- Comando CLI `missions` para listar missões por estado, com contagens gerais, ordenação determinística, filtro opcional `--state` e sem executar, mover ou alterar arquivos.
- Comando CLI `batch-summary` para resumo pós-batch local, com contagens de missões, último log encontrado, avisos de atenção e lembretes de validação manual, sem executar missões, scripts, testes, Git, rede, banco ou providers.
- Exemplos operacionais iniciais em `docs/examples/`.
- Templates iniciais de issues e pull request em `.github/`.

### Alterado

- README principal consolidado com a identidade pública do VAF como framework de Harness Engineering, sem tratar modelo, runtime ou provider como núcleo do projeto.
- Batch de 10 documentado como fluxo operacional padrão para blocos normais revisados e seguros; batch de 3 preservado para testes, retomadas, blocos pequenos e recuperação.
- Execução individual preservada para missões sensíveis, críticas, arquiteturais, incertas, investigativas, de recuperação ou de alto risco.
- OpenCode documentado como runtime/laboratório inicial atrás de adapter, não como centro arquitetural do framework.

### Documentado

- Política inicial de versionamento, sem promessa de estabilidade, compatibilidade de API, tag ou release publicada.
- Versão alfa planejada `0.1.0-alpha.1` e tag futura planejada `v0.1.0-alpha.1`, registradas apenas como plano documental.
- Documentação pública inicial para futura alfa, incluindo README, guia de instalação local, guia de contribuição, documentação legal inicial, arquitetura, operações, exemplos e checklist de prontidão para alfa pública.
- Validação real de instalação limpa em cópia temporária local, registrada como `REPROVADO`, sem criar release, tag ou pacote.
- `SECURITY.md` inicial, com política conservadora de segurança, limites atuais e orientação para reporte responsável.
- `CODE_OF_CONDUCT.md` inicial, com expectativas de conduta e limites de governança comunitária nesta fase.
- Política inicial de uso responsável em `docs/legal/usage-policy.md`.
- Revisão arquitetural pós-integrações em `docs/architecture/post-integration-architecture-review.md`.
- Índice navegável de módulos em `docs/architecture/module-index.md`.
- Playbook de execução em batch e checklist de validação pós-batch.

### Segurança

- Separação documentada entre Policy Engine e Guardian Engine.
- Restrições documentadas para evitar acesso direto de agentes a providers, MCPs, APIs, bancos, tools ou runtimes.
- Limites explícitos sobre uso com dados sensíveis, providers externos, automações destrutivas, credenciais e execução sem revisão humana.
- Política inicial de segurança sem promessa de SLA, bug bounty, conformidade regulatória, hardening de produção ou segurança absoluta.

### Operacional

- Operação local orientada por `pytest`, `python3 -m compileall src`, scripts seguros, CLI operacional e revisão humana.
- Push automático mantido como opt-in; push manual permanece a prática recomendada após validação.
- Documentação operacional diferencia backlog estratégico, fila executável, execução individual, batch seguro, retomada e validação pós-batch.

### Limites atuais

- Sem release estável publicada.
- Sem versão alfa publicada.
- Sem pacote publicado.
- Sem publicação em PyPI.
- Sem licença final em `LICENSE`; por isso o metadado de licença do pacote local não declara uma licença inventada nesta fase.
- Sem CI público documentado como existente.
- Sem RAG semântico.
- Sem embeddings.
- Sem pgvector como adapter real.
- Sem Semantic Index.
- Sem persistência externa de eventos.
- Sem múltiplos providers reais em produção.
- Sem internacionalização dos READMEs.
- Instalação limpa atual reprovada até nova execução aprovada ou decisão explícita sobre as ressalvas remanescentes; o empacotamento local mínimo foi ajustado após a validação reprovada, mas diretórios operacionais vazios, script de status acoplado a caminho absoluto e licença pendente ainda exigem tratamento.
- Sem promessa de compatibilidade futura, SLA ou prontidão para produção.

### Futuro

- Definição da política de release.
- Amadurecimento da política formal de estabilidade após as primeiras alfas.
- Criação de tag alfa somente após decisão explícita e validações aplicáveis.
- Release notes futuras quando houver release de fato.
- CI público, se houver decisão de automação.
- Internacionalização dos READMEs após estabilização do conteúdo canônico em português do Brasil.

## Convenção futura de versões

A política inicial de versionamento está documentada em [docs/release/versioning-policy.md](docs/release/versioning-policy.md). A versão alfa inicial planejada é `0.1.0-alpha.1`, com tag futura planejada `v0.1.0-alpha.1`, mas nenhuma release foi publicada e nenhuma tag foi criada.

Até uma decisão explícita de release, este changelog não atribui data de release, compatibilidade futura ou status de estabilidade.

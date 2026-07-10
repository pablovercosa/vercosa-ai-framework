# Notas Preliminares Da Futura Alfa `0.1.0-alpha.1`

Este documento é preparatório para a futura alfa planejada do Vercosa AI Framework.

Status conservador:

- versão planejada: `0.1.0-alpha.1`;
- tag futura planejada: `v0.1.0-alpha.1`;
- release publicada: não;
- tag criada: não;
- pacote publicado: não;
- publicação em PyPI: não prometida.

Estas notas não são release notes finais, não declaram data de release, não criam marco publicado, não prometem estabilidade, não prometem suporte formal, não prometem SLA e não prometem compatibilidade de API.

## Resumo

O Vercosa AI Framework, ou VAF, é um framework de Harness Engineering para agentes de IA. O objetivo do projeto é organizar a camada operacional ao redor de agentes e modelos: missões, runners, políticas, guardrails, contexto, orçamento de tokens, auditoria, seleção de modelos, providers, runtimes, validações e documentação orientada por Specs.

A futura alfa `0.1.0-alpha.1` deve representar um marco inicial de experimentação e revisão pública conservadora. Ela ainda não foi publicada. O estado atual é de preparação documental e técnica, com MVPs e contratos em evolução.

## O Que Está Incluído Nesta Alfa Planejada

No estado atual do repositório, a alfa planejada consolida os seguintes itens como fundação inicial, MVP, contrato ou documentação, conforme indicado nos documentos do projeto:

- Fundação modular do framework como camada de Harness Engineering para agentes de IA.
- Evolução por missões em Markdown, com backlog estratégico, fila operacional, critérios de aceite e validações locais.
- Mission Runner local e fila de missões em diretórios.
- Runner seguro de uma missão.
- Runner seguro em batch.
- Batch como fluxo operacional padrão quando o bloco estiver bem especificado, revisado e seguro.
- Policy Engine MVP.
- Guardian Engine MVP.
- Usage/API Limit Guard inicial para classificar sinais textuais de quota, rate limit, billing ou limite externo em logs já recebidos.
- Context Router determinístico.
- Token Budget Manager determinístico.
- Knowledge Hub MVP com documentos Markdown, store em memória e busca textual.
- Model Selection Engine MVP com catálogo em memória e políticas resolvidas opcionais.
- Provider Gateway MVP.
- Runtime Adapter inicial para OpenCode.
- Audit/Event Log inicial em memória.
- Persistência local JSONL opt-in de eventos auditáveis por `JsonlAuditEventLog`.
- CLI operacional inicial.
- Comandos `status`, `validate`, `doctor`, `missions` e `batch-summary`.
- Documentação pública inicial.
- Guia de instalação local para desenvolvimento.
- Guia inicial de contribuição.
- `SECURITY.md` inicial.
- `CODE_OF_CONDUCT.md` inicial.
- Templates de issue e template de pull request em `.github/`.
- `CHANGELOG.md` inicial.
- CI mínimo em `.github/workflows/ci.yml`, com instalação editável, `pytest` e `python -m compileall src`, sem publicação de pacote ou release.
- Empacotamento Python local mínimo em `pyproject.toml`, com versão PEP 440 `0.1.0a1` e entrypoint local `vaf` para instalação editável.

Esses itens não tornam o projeto pronto para produção e não significam que o fluxo completo Mission -> Workflow -> Task -> Agent -> Capability -> Skill -> Tool -> Provider esteja integrado de ponta a ponta.

## Limitações Conhecidas

- O projeto está em desenvolvimento.
- A futura alfa não deve ser usada como base de produção.
- APIs internas ainda podem mudar.
- Não há garantia de compatibilidade futura.
- Não há release alfa publicada.
- Não há tag `v0.1.0-alpha.1` criada.
- Não há pacote publicado.
- Não há promessa de publicação em PyPI.
- A validação de instalação limpa registrada está `REPROVADO` até nova execução aprovada ou decisão explícita de exceção.
- `LICENSE` final ainda está pendente no repositório.
- Não há RAG semântico.
- Não há embeddings.
- Não há pgvector como adapter real.
- Não há Semantic Index.
- Não há múltiplos providers reais em produção.
- Não há múltiplos runtimes reais em produção.
- Não há dashboard.
- Não há persistência externa de eventos.
- Não há retenção ou rotação maduras para eventos auditáveis.
- Não há política madura de vulnerabilidades nem canal público definitivo de reporte privado.
- Internacionalização dos READMEs ainda é futura.

## Como Testar Localmente

Use estes documentos como referência antes de validar uma instalação local:

- [Instalação local para desenvolvimento](../getting-started/local-installation.md)
- [Checklist de instalação limpa](../getting-started/clean-install-checklist.md)
- [Registro de validação limpa](clean-install-validation.md)

Depois de instalar o projeto em modo desenvolvimento no ambiente virtual ativo, estes comandos de validação local são sugeridos:

```bash
pytest
python3 -m compileall src
python3 -m vercosa_ai_framework.cli.main --help
python3 -m vercosa_ai_framework.cli.main validate
python3 -m vercosa_ai_framework.cli.main doctor
python3 -m vercosa_ai_framework.cli.main missions
python3 -m vercosa_ai_framework.cli.main batch-summary
```

Em checkouts sem instalação editável, a forma com `PYTHONPATH=src` pode ser necessária para diagnosticar a CLI local:

```bash
PYTHONPATH=src python3 -m vercosa_ai_framework.cli.main --help
```

Quando o projeto estiver instalado em modo desenvolvimento no ambiente virtual ativo, o entrypoint local `vaf` também pode ser usado como alternativa:

```bash
vaf --help
vaf validate
vaf doctor
vaf missions
vaf batch-summary
```

O entrypoint `vaf` não deve ser tratado como comando global publicado ou pacote distribuído.

## Segurança E Uso Responsável

Leia estes documentos antes de executar missões, batch, tools, runtimes ou qualquer integração com efeitos externos:

- [Política inicial de segurança](../../SECURITY.md)
- [Política inicial de uso responsável](../legal/usage-policy.md)
- [Reporte responsável de vulnerabilidades](../security/vulnerability-reporting.md)

O VAF ainda não possui processo público maduro de segurança, canal definitivo de vulnerabilidades, bug bounty, SLA, hardening de produção ou sandbox externo garantido. Não publique secrets, tokens, credenciais, logs sensíveis, prompts privados ou detalhes exploráveis de vulnerabilidades em canais públicos.

## Antes Da Publicação

Antes de qualquer release real, ainda é necessário:

- executar o checklist pré-tag;
- confirmar CI passando;
- revisar `CHANGELOG.md`;
- revisar estas notas preliminares e transformá-las, se aprovado, em release notes finais;
- confirmar instalação limpa com resultado aprovado ou exceção explícita aceita;
- confirmar licença e criar `LICENSE`, se a decisão for aprovada;
- obter autorização explícita para criar tag;
- obter autorização explícita para publicar release;
- decidir se haverá pacote ou somente código-fonte.

Sem essas decisões, a versão permanece planejada e não publicada.

## Links Úteis

- [README.md](../../README.md)
- [CHANGELOG.md](../../CHANGELOG.md)
- [Política de versionamento](versioning-policy.md)
- [Plano da versão alfa](alpha-version-plan.md)
- [Política de release](release-policy.md)
- [Checklist pré-tag](pre-release-checklist.md)
- [Checklist de prontidão para alfa pública](public-alpha-readiness.md)
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
- [SECURITY.md](../../SECURITY.md)

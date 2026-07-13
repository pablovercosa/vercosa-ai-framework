# ADR 0003: Separar Resolução E Execução De Capability

Estado: Aceita.

## Contexto

A missão 0106 validou CapabilityResolutionResult -> ResolvedCapabilityExecutor -> SkillExecutor -> ToolExecutor -> ProviderGateway em dry-run, com preservação de IDs e fronteiras.

## Decisão

Separar resolução declarativa de Capability da execução da Capability resolvida.

`CapabilityResolver` produz `CapabilityResolutionResult` e não executa Skill. `ResolvedCapabilityExecutor` constrói `SkillExecutionRequest` e chama `SkillExecutor`. `SkillExecutor` seleciona e chama `ToolExecutor`. `ToolExecutor` é a fronteira que chama `ProviderGateway`.

## Evidências

- Código: `src/vercosa_ai_framework/capabilities/resolver.py`.
- Código: `src/vercosa_ai_framework/capabilities/executor.py`.
- Código: `src/vercosa_ai_framework/skills/executor.py`.
- Código: `src/vercosa_ai_framework/tools/executor.py`.
- Teste: `tests/test_capability_skill_tool_provider_dry_run.py`.
- Teste: `tests/test_tool_executor_provider_gateway.py`.

## Consequências

- Resolver não executa Skill.
- Skill não chama Provider Gateway diretamente fora de ToolExecutor.
- Cada fronteira preserva referências de mission, workflow, task, agent assignment e request.

## Decisões Ainda Pendentes

- Catálogo aprovado de Capabilities, Skills e Tools.
- Políticas finais de fallback de tool.
- Processo de revisão de segurança para MCPs.

# ADR 0007: Manter Compatibilidade Legada Por Configuração Explícita

Estado: Provisória.

## Contexto

As integrações 0104 a 0107 adicionaram caminhos mínimos por injeção explícita sem remover caminhos legados. Os testes validam compatibilidade do Mission Runner sem Workflow, do Agent Orchestrator sem executor de Capability e da governança como opt-in ou obrigatória apenas quando configurada.

## Decisão

Manter compatibilidade legada por configuração explícita enquanto o fluxo integrado ainda amadurece.

O caminho `WorkflowEngine.execute()` permanece transitório e não será removido sem missão futura, atualização de Spec e validação. Caminhos integrados como `execute_with_queue()`, `AgentTaskExecutor`, `capability_executor` e `AgentExecutionGovernance` devem ser ativados por dependência ou flag explícita.

## Evidências

- Teste: `tests/test_mission_workflow_task_integration.py` valida Mission Runner legado sem workflow.
- Teste: `tests/test_capability_skill_tool_provider_dry_run.py` valida Agent Orchestrator legado sem executor de Capability.
- Teste: `tests/test_agent_execution_governance_0107.py` valida falha quando governança é exigida e não configurada.

## Consequências

- Integrações novas não quebram chamadores internos existentes.
- Compatibilidade legada não deve virar argumento para expandir comportamento sem governança.
- A remoção do legado exige decisão futura.

## Decisões Ainda Pendentes

- Remoção ou depreciação de `WorkflowEngine.execute()`.
- Caminho canônico exclusivo para execução de Workflow.
- Política final de migração de APIs internas MVP.

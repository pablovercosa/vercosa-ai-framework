# Guardian Spec 001 — Security by Design

## Objetivo

Garantir que todo código, sistema, workflow, agente, skill, MCP, provider e artefato gerado pelo framework seja projetado com segurança desde o início.

## Escopo

Esta Guardian Spec se aplica a todos os projetos, módulos e execuções.

## Regras

1. Nenhum código com vulnerabilidade crítica conhecida deve ser aprovado.
2. Segredos nunca devem ser expostos em logs, prompts, commits ou respostas.
3. Arquivos .env devem exigir confirmação antes de leitura.
4. MCPs devem ser tratados como superfície de ataque.
5. Plugins externos devem ser avaliados antes do uso.
6. Comandos destrutivos devem exigir confirmação.
7. Execução automática deve respeitar políticas de segurança.
8. Dependências devem ser avaliadas por risco de supply chain.
9. Código gerado deve seguir boas práticas OWASP quando aplicável.
10. Toda decisão de risco deve ser documentada.

## Gates obrigatórios

- Secret scanning
- Dependency review
- Static review
- Prompt injection review quando houver uso de conteúdo externo
- MCP safety review para novos MCPs
- Permission review para agentes

## Integrações desejadas

O framework pode integrar soluções externas de segurança, agentes, skills e MCPs desde que respeitem esta Guardian Spec.

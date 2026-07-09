# Política Inicial De Uso Responsável

Links principais: [README legal](README.md) | [Notas de licença](license-notes.md) | [Política de segurança](../../SECURITY.md) | [README principal](../../README.md) | [Guia de contribuição](../../CONTRIBUTING.md)

## Objetivo

Esta política descreve orientações iniciais de uso responsável do Vercosa AI Framework. O VAF é um framework de desenvolvimento e orquestração governada de agentes de IA, ainda em desenvolvimento, voltado a Harness Engineering, missões rastreáveis, validação, políticas e revisão humana.

Esta política não implementa bloqueios técnicos, não substitui revisão humana e não promete segurança absoluta.

## Usos Pretendidos

O projeto é adequado, nesta fase, para:

- pesquisa;
- desenvolvimento local;
- automação assistida;
- prototipação;
- documentação;
- execução governada de missões;
- experimentos controlados de Harness Engineering.

## Usos Que Exigem Cautela

Os usos abaixo exigem revisão explícita de escopo, permissões, dados, custos, efeitos e validações antes de execução:

- produção;
- automações com impacto financeiro;
- automações com impacto jurídico;
- automações com impacto médico;
- automações com impacto trabalhista;
- automações com dados sensíveis;
- execução de ferramentas externas;
- integração com providers pagos;
- integração com banco de dados;
- integração com runtimes remotos.

## Usos Não Recomendados Nesta Fase

Nesta fase do projeto, não é recomendado usar o VAF para:

- decisões autônomas de alto risco;
- execução sem revisão humana;
- uso com credenciais expostas;
- processamento de dados sensíveis sem controles adicionais;
- automação destrutiva sem aprovação explícita;
- uso como sistema de segurança crítica;
- uso como substituto de aconselhamento profissional.

## Princípios De Uso

O uso responsável do VAF deve seguir estes princípios:

- revisão humana antes de mudanças relevantes;
- menor privilégio para comandos, tools, runtimes, providers e credenciais;
- rastreabilidade de missão, decisão, validação e resultado;
- logs sem vazamento de segredo;
- validação antes de execução com efeitos concretos;
- testes antes de publicação, release ou uso por terceiros;
- providers sob controle explícito do operador;
- execução em ambiente isolado quando possível.

## Limites Atuais

O VAF ainda possui limites importantes:

- framework em desenvolvimento;
- sem garantia de estabilidade;
- sem garantia de adequação a produção;
- sem conformidade regulatória declarada;
- com política inicial de segurança, mas sem processo público maduro de reporte de vulnerabilidades ainda;
- sem release estável.

Integrações futuras com providers, tools, runtimes, RAG, embeddings ou banco devem ser avaliadas caso a caso, considerando dados enviados, permissões, custos, efeitos colaterais, logs, auditoria e política aplicável.

## Responsabilidade Do Usuário E Contribuidor

Usuários e contribuidores são responsáveis por revisar missões, comandos, scripts, prompts, dados, credenciais, efeitos esperados e efeitos possíveis antes de executar qualquer operação.

O VAF busca organizar governança e rastreabilidade, mas não elimina a necessidade de aprovação humana, testes, controle de ambiente e revisão de risco.

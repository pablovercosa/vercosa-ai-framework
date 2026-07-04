Leia obrigatoriamente:
- AGENTS.md
- README.md
- docs/
- knowledge/
- specs/
- missions/done/
- src/vercosa_ai_framework/*/README.md

Assuma o papel de documentation-architect e framework-architect.

Missão:
Padronizar o projeto para português do Brasil e criar regras obrigatórias para atualização de READMEs e mensagens de commit futuras.

Objetivos:
1. Definir português do Brasil como idioma oficial da documentação do Vercosa AI Framework.
2. Revisar arquivos de documentação que ainda estejam em inglês e convertê-los para pt-BR quando apropriado.
3. Manter nomes técnicos, nomes de módulos, nomes de classes e nomes de componentes em inglês quando forem parte da API/arquitetura.
4. Criar regra explícita: toda missão que criar, alterar ou expandir funcionalidade deve revisar e atualizar os READMEs e docs relacionados.
5. Criar regra explícita: mensagens de commit futuras devem ser em português do Brasil.
6. Evitar reescrever histórico Git já publicado.

Entregáveis obrigatórios:
- atualizar AGENTS.md;
- atualizar README.md se houver trechos em inglês desnecessário;
- atualizar docs/documentation/readme-standard.md;
- atualizar docs/templates/readme-template.md;
- atualizar docs/architecture/module-index.md se necessário;
- revisar e ajustar READMEs em src/vercosa_ai_framework/*/README.md;
- criar docs/documentation/language-and-commit-standard.md;
- criar docs/documentation/documentation-update-policy.md;
- atualizar docs/alignment/open-questions.md apenas se encontrar pendência relevante.

Regras de idioma:
- documentação deve ser em português do Brasil;
- commits futuros devem usar português do Brasil;
- nomes técnicos como Context Router, Token Budget Manager, Policy Engine, Guardian Engine, Provider Gateway, Runtime Adapter, Knowledge Hub e similares podem permanecer em inglês quando forem nomes arquiteturais consolidados;
- nomes de arquivos, pacotes, classes, funções e enums não precisam ser traduzidos;
- specs e ADRs podem manter termos técnicos em inglês, mas o texto explicativo deve estar em pt-BR;
- não alterar APIs públicas apenas para traduzir nomes técnicos;
- não renomear arquivos já existentes sem necessidade forte.

Regras de README:
Toda missão futura que criar, alterar ou expandir uma funcionalidade deve verificar e, quando necessário, atualizar:
- README.md principal;
- README.md do módulo afetado;
- docs/architecture/module-index.md;
- docs relacionados;
- specs relacionadas;
- ADRs relacionadas;
- links relativos entre documentos.

Regras de commit:
- Não reescrever histórico Git já publicado.
- A partir desta missão, commits devem usar português do Brasil.
- Prefixos recomendados:
  - missão:
  - docs:
  - arquitetura:
  - implementação:
  - teste:
  - correção:
  - refatoração:
  - chore:
- Descrições devem ser claras e curtas.
- Evitar misturar português e inglês em frases de commit, salvo nomes técnicos.

Restrições:
- não implementar nova funcionalidade;
- não alterar lógica de src/;
- não alterar testes;
- não adicionar dependências;
- não usar sudo;
- não alterar configs globais;
- não reescrever histórico Git;
- não fazer force push;
- não traduzir nomes técnicos de APIs, classes ou módulos;
- não prometer comportamento ainda não implementado.

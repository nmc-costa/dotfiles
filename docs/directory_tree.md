# 🗂️ Standard Directory Tree & Environment Context

Este ficheiro serve como a "fonte da verdade" para a estrutura de diretórios do sistema e fornece o contexto global necessário para que os Agentes de IA (Claude, Copilot, etc.) compreendam o ambiente de desenvolvimento, mantenham a portabilidade absoluta e utilizem caminhos relativos perfeitos.

## 📐 Filosofia do Ecossistema
1. **Isolamento por Contexto:** O código é separado por privacidade/vida profissional (`Projects/` vs `Work/`) e não por plataforma (`github/`, `gitlab/`).
2. **Raiz Unificada (Root):** O diretório pessoal do utilizador (`~` ou `/home/nbugz/`) é assumido como a raiz de trabalho no editor (VS Code).
3. **Dotfiles Centralizados:** Todas as configurações globais e regras de IA vivem no repositório `~/dotfiles` e são espelhadas na raiz através de Links Simbólicos (`symlinks`).

---

## 🗺️ Mapa Estrutural do Sistema

```text
/home/nbugz/ (~)                # RAINHA DO AMBIENTE (Abrir o VS Code aqui: code ~)
│
├── .dotfiles/                  # REPOSITÓRIO PRIVADO DE CONFIGURAÇÃO (Sincronizado via GitHub)
│   ├── directory_tree.md       # Este ficheiro de documentação e contexto estrutural
│   ├── .context-global.md      # Instruções de contexto gerais para as IAs
│   ├── claude.md               # Regras e preferências específicas para o Claude
│   ├── copilot.md              # Regras e preferências específicas para o GitHub Copilot
│   ├── .gitconfig              # Configurações globais do Git
│   └── setup.sh                # Script de automação para novos computadores
│
├── Projects/                   # CONTEXTO PESSOAL (Iniciativas Próprias e Estudos)
│   ├── .ai-context.md          # Contexto opcional focado apenas em projetos pessoais
│   └── [repositorio-pessoal]/  # Repositórios clonados (O Git gere a origem de forma invisível)
│       └── .git/
│
└── Work/                       # CONTEXTO PROFISSIONAL (Emprego e Organizações)
    ├── .work-rules.md          # Padrões de arquitetura e regras de negócio da empresa
    └── [repositorio-empresa]/  # Repositórios da Organização (Ex: dtx-dashboard)
        └── .git/
```

---

## 🔗 Links Simbólicos Ativos (Symlinks)
Para garantir que as extensões de IA encontram as definições na raiz (`~`), os seguintes ficheiros estão interligados:
* `~/dotfiles/directory_tree.md`  -->  `~/.directory_tree.md` (Opcional)
* `~/dotfiles/.context-global.md` -->  `~/.context-global.md`
* `~/dotfiles/claude.md`          -->  `~/claude.md`
* `~/dotfiles/copilot.md`         -->  `~/copilot.md`

---

## 🤖 Instruções para os Agentes de IA (Prompt de Contexto)
> **Diretriz para a IA:** Sempre que fizer referência a caminhos de ficheiros, imports ou documentação cruzada, utilize **caminhos relativos a partir da raiz do utilizador (`~`)**. 
> * **Projetos Pessoais:** Devem ser referenciados como `Projects/nome-do-projeto/...`
> * **Projetos de Trabalho:** Devem ser referenciados como `Work/nome-do-projeto/...`
> * **Configs/Regras:** Devem ser referenciadas como `.dotfiles/nome-do-ficheiro`
> 
> *Nunca assuma uma pasta intermédia chamada `github` ou `gitlab` na raiz dos projetos.*
> * Para acessar os ficheiros de configuração globais, utilize os symlinks na raiz (`~`), por exemplo, `~/.context-global.md` para o contexto global.
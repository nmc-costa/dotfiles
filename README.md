# dotfiles

Github config and setup files

Serves to perserve global files 



# Contexto do Utilizador & Ambiente de Desenvolvimento

## 💻 Especificações do Sistema
* **SO:** Omarchy Linux (Versão Quattro), baseado em Arch. Sistema opinativo (omakase).
* **Editores Ativos:** NeoVim (nativo/eficiência máxima) e VS Code (rede de segurança visual instalado via `yay -S visual-studio-code-bin`).
* **Conta Git:** Mesma conta do GitHub usada para repositórios pessoais e da organização.

---

## 📐 Arquitetura de Diretórios Definida (Padrão Omarchy + IA)
Após validação profunda da comunidade, eliminou-se a pasta intermédia `~/github`. O utilizador assumiu a raiz `~` (/home/user/) como o root de trabalho no editor (`code ~`), garantindo caminhos relativos curtos e perfeitos para portabilidade absoluta e leitura dos Agentes de IA (Claude, Copilot).

* **`~/Projects/`** -> Repositórios pessoais clonados diretamente (IP própria, laboratórios e estudos).
* **`~/Work/`** -> Repositórios profissionais/organização (Ex: `dtx-dashboard`). O Git isola as origens via `.git` interno.
* **`~/dotfiles/`** -> O ÚNICO repositório privado no GitHub que sincroniza o ambiente entre computadores (sem cópias manuais).

---

## 🔗 Estrutura Física de Dotfiles e Symlinks no Disco
Os ficheiros de contexto globais e configurações reais vivem em `~/dotfiles/` e são espelhados na raiz `~` por Links Simbólicos (`symlinks`), permitindo que as extensões de IA os leiam no topo do root:

* `~/dotfiles/directory_tree.md`  -->  `~/directory_tree.md` (Mapa standard guardado)
* `~/dotfiles/.context-global.md` -->  `~/.context-global.md` (Contexto geral de IA)
* `~/dotfiles/claude.md`          -->  `~/claude.md` (Regras globais do Claude)
* `~/dotfiles/.claude`           -->  `~/.claude` (Configurações do Claude)
* `~/dotfiles/.vscode`      -->  `~/.vscode` (Configurações do VS Code)
* `~/dotfiles/.github`       -->  `~/.github` (Configurações do GitHub)
* `~/dotfiles/.github/copilot-instructions.md`         -->  `~/.github/copilot-instructions.md` (Regras globais do Copilot)



---

## 🛠️ Comandos Práticos Aprendidos e Utilizados
* **Criar Symlinks:** `ln -sf ~/dotfiles/ficheiro ~/ficheiro`
* **Abrir a Raiz no VS Code:** `code ~`
* **NeoVim (Modo de Edição):** Tecla `i` para escrever; Tecla `Esc` (ou `Ctrl + [`) para sair do modo de escrita.
* **NeoVim (Sair e Gravar):** Comando `Shift + Z + Z` (`ZZ` - vai dormir/grava e fecha sem precisar de Enter); `:wq` como alternativa.
* **NeoVim (Sair sem Gravar/Forçado):** Comando `Shift + Z + Q` (`ZQ`) ou `:q!`.
* **Desfazer Ação no NeoVim:** Tecla `u` no Modo Normal.

---

## 🚀 Próximos Passos Pendentes para o Próximo Chat:
1. Criar o código de automação para o script `~/dotfiles/setup.sh` para replicar esta árvore e os symlinks num segundo computador com um único clique.
2. Gerar o conteúdo avançado em Markdown (prompts de regras de desenvolvimento) para preencher o `claude.md` e o `copilot.md`.
3. Iniciar a clonagem visual ou automatizada dos repositórios dentro de `Projects/` e `Work/`.



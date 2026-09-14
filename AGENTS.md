# AGENTS.md

Orientações para agentes de IA (Crush/Claude, Copilot, Gemini) trabalharem neste repositório.

## Agentes Disponíveis

| Agente | Localização Config | Quando Usar |
|--------|-------------------|-------------|
| **Crush/Claude** | `~/.claude/`, `~/.claude.json` | Desenvolvimento, análise de código, debugging, automação |
| **Copilot** | `~/.copilot/` | Sugestões inline, completions em VS Code |
| **Gemini** | `~/.gemini/` | Consultas rápidas, brainstorming |
| **Cline** | `~/.cline/` | Execução de tarefas complexas multi-arquivo |

## Skills Personalizadas

Este repositório centraliza skills (extensões/plugins) na pasta padrão `.agents/skills/`:

```
dotfiles/
└── .agents/
    ├── skills/                     ← Central source of truth
    │   ├── diagnose-crash/
    │   │   ├── SKILL.md
    │   │   └── reporting.md
    │   ├── omarchy/
    │   │   ├── SKILL.md
    │   │   └── [outros ficheiros]
    │   └── [novas-skills]/
    │       └── SKILL.md
    └── workflows/                  ← Agent personas
        ├── init.md
        └── architect_html_sciml.md
```

Quando sincronizas, as skills são propagadas para:
- **`~/.agents/skills/`** — Shared across agents (sempre sincronizado)
- **`~/.claude/skills/`** — Crush-specific (se existir)
- **`/usr/share/omarchy/default/agents/skills/`** — System-wide (opcional, requer sudo)

### Adicionar Nova Skill

1. Cria pasta em `dotfiles/.agents/skills/minha-skill/`
2. Adiciona `SKILL.md` (obrigatório):
   ```markdown
   # Minha Skill
   
   Descrição breve do que faz.
   
   ## Triggers (quando usar)
   - Palavra-chave 1
   - Palavra-chave 2
   ```
3. Adiciona outros ficheiros conforme necessário
4. Commit:
   ```bash
   cd ~/dotfiles
   git add .agents/skills/minha-skill/
   git commit -m "Add minha-skill for [propósito]"
   git push
   ```
5. Sincroniza:
   ```bash
   ./sync-skills.sh
   ```
   Opções:
   - `./sync-skills.sh` — Sincroniza para `~/.agents/skills/` e `~/.claude/skills/`
   - `./sync-skills.sh --system` — Também copia para `/usr/share/omarchy/default/agents/skills/` (requer sudo)
   - `./sync-skills.sh --dry-run` — Simula sem fazer mudanças
   - `./sync-skills.sh --verbose` — Mostra detalhes da sincronização

### Adicionar Nova Skill e Propagar (Fluxo Completo)

```bash
# 1. Cria skill
mkdir -p ~/dotfiles/.agents/skills/nova-skill
cat > ~/dotfiles/.agents/skills/nova-skill/SKILL.md <<'EOF'
# Nova Skill

Descrição.

## Triggers
- keyword
EOF

# 2. Adiciona outros ficheiros (opcional)
# cp script.sh ~/dotfiles/.agents/skills/nova-skill/

# 3. Versiona no GitHub
cd ~/dotfiles
git add .agents/skills/nova-skill/
git commit -m "Add nova-skill for [propósito]"
git push

# 4. Sincroniza para agentes locais
./sync-skills.sh

# 5. (Opcional) Sincroniza também para sistema
./sync-skills.sh --system

# 6. Na outra máquina: pull + sync
cd ~/dotfiles && git pull
./sync-skills.sh
```

## Variáveis de Contexto para Agentes

### Estrutura de Diretórios
- `~/Projects/` — Repos pessoais (estudos, IP própria)
- `~/Work/` — Repos profissionais/organização
- `~/dotfiles/` — Este repo (sincronização entre máquinas)

### Ficheiros de Contexto Global

| Ficheiro | Acesso | Propósito |
|----------|--------|----------|
| `~/.context-global.md` | Todos os agentes | Contexto geral (estrutura, convenções, preferências) |
| `~/claude.md` | Crush/Claude | Regras específicas para Claude |
| `~/.github/copilot-instructions.md` | Copilot | Instruções específicas para Copilot |
| `~/directory_tree.md` | Todos (referência) | Mapa da estrutura de diretórios |

## Regras de Desenvolvimento por Agente

### Crush/Claude
- **Lê:** `claude.md`, `.context-global.md`, `directory_tree.md`
- **Preferências:** Análise profunda, explicações técnicas, automação script
- **Restrições:** Sem commits automáticos sem confirmação explícita

### Copilot
- **Lê:** `.github/copilot-instructions.md`, `.context-global.md`
- **Preferências:** Sugestões inline rápidas, completions de código
- **Restrições:** Não modifica ficheiros sem intervenção

### Gemini
- **Lê:** `.context-global.md`
- **Preferências:** Brainstorming, ideação, verificação de conceitos
- **Restrições:** Uso ocasional, não storage de contexto longo

### Cline
- **Lê:** Todas as instruções acima (fallback: `.context-global.md`)
- **Preferências:** Tarefas multi-passo, refactoring, testes
- **Restrições:** Respeita permissões de user, não modifica configs do sistema sem sudo

## Sincronização Entre Máquinas

### Primeiro Setup (Nova Máquina)
```bash
cd ~
git clone https://github.com/nmc-costa/dotfiles.git dotfiles-tmp
cd dotfiles-tmp
./setup.sh --dotfiles
# Follow on-screen instructions for config checkout
```

### Atualizar Configs Existentes
```bash
cd ~/dotfiles
git pull
./setup.sh      # Executa symlinks + sync-skills.sh
```

## Troubleshooting

### Skills não aparecem após clone
```bash
# Verifica localização
ls ~/.agents/skills/
ls ~/.claude/skills/

# Sincroniza manualmente
cd ~/dotfiles
./sync-skills.sh --verbose

# Ou para sistema (requer sudo)
./sync-skills.sh --system
```

### Symlinks Rotos
```bash
# Verifica
ls -la ~/  # Procura setas vermelhas

# Recria manualmente
ln -sf ~/dotfiles/.claude ~/.claude
ln -sf ~/dotfiles/.agents ~/.agents
ln -sf ~/dotfiles/.vscode ~/.vscode

# OU executa setup novamente
./setup.sh
```

### Agente Não Vê Contexto
- Verifica se `~/.context-global.md` existe (deve ser symlink)
- Verifica permissões: `ls -la ~/.context-global.md`
- Recarrega o agente ou reinicia a aplicação

---

**Última Atualização:** 2026-09-14  
**Mantido por:** nmc-costa

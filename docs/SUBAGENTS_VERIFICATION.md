# SUBAGENTS_VERIFICATION.md

Checklist de verificação para garantir que todos os subagentes têm acesso à informação correta do dotfiles.

## Agentes Configurados

- ✅ **Crush/Claude** — `~/.claude/`
- ✅ **Copilot** — `~/.copilot/`
- ✅ **Gemini** — `~/.gemini/`
- ✅ **Cline** — `~/.cline/`

## Ficheiros de Contexto Global (Symlinks)

Todos os agentes devem ter acesso a:

| Ficheiro | Localização | Status | Verificação |
|----------|------------|--------|-------------|
| `directory_tree.md` | `~/dotfiles/directory_tree.md` → `~/directory_tree.md` | ⏳ | `ls -la ~/directory_tree.md` |
| `.context-global.md` | `~/dotfiles/.context-global.md` → `~/.context-global.md` | ⏳ | `ls -la ~/.context-global.md` |
| `claude.md` | `~/dotfiles/claude.md` → `~/claude.md` | ⏳ | `ls -la ~/claude.md` |
| `.agents/` | `~/dotfiles/.agents/` → `~/.agents/` | ✅ | `ls -la ~/.agents/` |
| `.claude/` | `~/dotfiles/.claude/` → `~/.claude/` | ✅ | `ls -la ~/.claude/` |
| `.vscode/` | `~/dotfiles/.vscode/` → `~/.vscode/` | ✅ | `ls -la ~/.vscode/` |
| `.github/` | `~/dotfiles/.github/` → `~/.github/` | ✅ | `ls -la ~/.github/` |

**Status:**
- ✅ = Confirmado funcionar
- ⏳ = A verificar (devem existir em dotfiles)
- ❌ = Falta criar

## Skills Disponíveis

Skills em `~/.agents/skills/`:

```bash
ls ~/.agents/skills/
```

Esperado:
- ✅ `diagnose-crash/` — SKILL.md + reporting.md
- ✅ `omarchy/` — SKILL.md + hyprland.md + theming.md + ...

Para sincronizar:
```bash
cd ~/dotfiles
./sync.sh --verbose
```

## Workflows Disponíveis

Workflows em `~/.agents/workflows/`:

```bash
ls ~/.agents/workflows/
```

Esperado:
- ✅ `init.md` — Inicialização de novo agente
- ✅ `architect_html_sciml.md` — Persona para Architect

## Documentação Raiz

Todos os MDs no root do dotfiles devem estar atualizados:

| Ficheiro | Última Atualização | Status |
|----------|-------------------|--------|
| `README.md` | Estrutura e setup | ✅ Atualizado |
| `AGENTS.md` | Skills em `.agents/` | ✅ Atualizado |
| `CLAUDE.md` | Contexto dotfiles | ✅ Atualizado |
| `GEMINI.md` | Contexto dotfiles | ✅ Atualizado |
| `VSCODE_MONITOR_QUICKSTART.md` | Legacy (verificar) | ⏳ |
| `directory_tree.md` | Mapa de diretórios | ⏳ Verificar se existe |

## Spin de Subagentes

Quando fazer spin (ativar) de um novo subagente:

1. **Copiar contexto global:**
   ```bash
   ln -sf ~/dotfiles/.claude ~/.claude
   ln -sf ~/dotfiles/.agents ~/.agents
   ln -sf ~/dotfiles/.vscode ~/.vscode
   ```

2. **Sincronizar skills:**
   ```bash
   ~/dotfiles/sync.sh
   ```

3. **Verificar acesso:**
   ```bash
   ls ~/.agents/skills/
   cat ~/.agents/skills/diagnose-crash/SKILL.md
   ```

4. **Testar skill trigger:**
   ```bash
   # Agente deve reconhecer keywords
   # Ex: "segfault" deve ativar diagnose-crash skill
   ```

## Checklist de Setup Completo

- [ ] Pasta `.agents/` existe e é symlink
- [ ] `.agents/skills/` contém skills (diagnose-crash, omarchy)
- [ ] `.agents/workflows/` contém workflows (init.md, architect_html_sciml.md)
- [ ] `sync.sh` executa sem erros: `./sync.sh --dry-run`
- [ ] Todos os MDs root (`README.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) mencionam `.agents/`
- [ ] Não existe pasta `.agent/` (foi migrada para `.agents/`)
- [ ] `setup.sh` cria symlinks corretamente: `./setup.sh --dry-run`

## Como Usar Este Documento

1. Executar todas as verificações acima
2. Marcar status de cada item
3. Se algum falhar, consultar secção correspondente em `AGENTS.md` ou `README.md`
4. Fazer commit de qualquer ajuste: `git add -A && git commit -m "Fix [subagent] setup"`

---

**Última Atualização:** 2026-09-14  
**Mantido por:** nmc-costa

Quando novos subagentes forem adicionados, atualizar este ficheiro com suas localizações de config.

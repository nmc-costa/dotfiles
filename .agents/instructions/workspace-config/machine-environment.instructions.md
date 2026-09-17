---
applyTo: "**"
---

# Machine Environment Notes

Standing facts about this Omarchy Linux machine's environment that change how
commands must be run here. Distinct from
[`.agents/skills/omarchy/tuning.md`](../../skills/omarchy/tuning.md), which
tracks system *changes made*, not environment facts to work around.

## Privilege escalation: use `pkexec`, not `sudo`

This console has no TTY attached for `sudo`'s password prompt. Confirmed
directly (2026-09-16) — both an agent-run shell command and a user-typed
`!`-prefixed command failed the same way:

```
sudo: a terminal is required to read the password; either use the -S option to read from standard input or configure an askpass helper
```

**Use `pkexec <command>` instead.** It opens a graphical polkit
authentication dialog and works without a TTY.

For privileged file writes (config files, etc.) that would normally go
through `sudo tee` or a heredoc, don't pipe into `pkexec` directly — write
the content to a normal file first, then install it as root:

```bash
cat > /tmp/some-file.conf << 'EOF'
...
EOF
pkexec install -m <mode> -o root -g root /tmp/some-file.conf /etc/path/to/some-file.conf
rm -f /tmp/some-file.conf
```

This is a fact about this specific machine/console, not a universal rule —
check `sudo -n true` / TTY availability before assuming it applies
elsewhere.

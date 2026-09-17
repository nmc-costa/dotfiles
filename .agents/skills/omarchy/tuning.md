# Omarchy tuning

Personal tuning of *this* machine's Omarchy install — real system changes
applied locally, not vendored skill content. Different from
[`LOCAL_ADDENDUM.md`](LOCAL_ADDENDUM.md), which only tracks documentation
gaps in the vendored skill itself; this file tracks actual configuration
changes made to the running system.

Each entry has a **Verify** command. Whenever this file is read/run, check
every entry's Verify command against the live system, and list anything
that comes back unapplied under **Pending** at the bottom. Add a new entry
here the same day a tweak is actually applied — not before.

## Lid switch: lock instead of suspend

**Status:** Applied — 2026-09-16

**What:** Closing the laptop lid still locks the screen (Omarchy's own
default behavior, via `/usr/share/omarchy/bin/omarchy-system-lid-close`),
but no longer suspends the machine. Opening the lid leaves the session
locked, normal password unlock. Explicit sleep — the "Suspend" menu entry,
`systemctl suspend`, the power button — is untouched and still suspends
normally.

**Why:** Omarchy's default `HandleLidSwitch=suspend` (systemd-logind)
suspends on *every* lid close, stacked on top of the lock that
`omarchy-system-lid-close` already performs — an unwanted second action.
systemd's own `HandleLidSwitch=lock` alternative was checked and rejected:
Omarchy's shell only reacts to `PrepareForSleep` and its own Hyprland
switch binding, not to logind's generic session `Lock` D-Bus signal, so
`lock` would fire and do nothing observable. `ignore` is the only value
that produces the wanted result, by deferring entirely to the Hyprland
binding that already works.

**Apply** (this console's `sudo` has no TTY — use `pkexec`, see the
workspace-wide note for why):
```bash
cat > /tmp/30-lid-no-suspend.conf << 'EOF'
[Login]
HandleLidSwitch=ignore
EOF
pkexec install -m 644 -o root -g root /tmp/30-lid-no-suspend.conf /etc/systemd/logind.conf.d/30-lid-no-suspend.conf
rm -f /tmp/30-lid-no-suspend.conf
pkexec systemctl reload systemd-logind
```

**Verify:**
```bash
busctl get-property org.freedesktop.login1 /org/freedesktop/login1 org.freedesktop.login1.Manager HandleLidSwitch
# expect: s "ignore"
test -f /etc/systemd/logind.conf.d/30-lid-no-suspend.conf && echo present || echo MISSING
```

**Revert:**
```bash
pkexec rm -f /etc/systemd/logind.conf.d/30-lid-no-suspend.conf
pkexec systemctl reload systemd-logind
```

## Pending

None currently.

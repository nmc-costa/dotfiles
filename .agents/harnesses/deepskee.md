# DeepSeek / deepskee Harness

**Status:** template → needs verification
**Purpose:** Integrate DeepSeek (aka "DeepSkee"/"deepskee" / "DeepSeek V4") as a provder/harness so this workspace's skills and instructions can be used with DeepSeek's CLI or API.

---

## Quick Links

| What | Where |
|---:|:---|
| Workspace config | `.agents/instructions/workspace-config/` |
| All skills | `.agents/skills/` |
| This harness setup | `.agents/harnesses/deepskee.md` |

---

## Summary

This file documents the recommended, verifiable steps to add a DeepSeek harness to the workspace. It follows the repository's harness template and intentionally records unknowns to be verified against the actual DeepSeek/DeepSkee CLI or API docs before doing any code that assumes behavior.

If DeepSeek provides a CLI that auto-loads a project-context file (like `CLAUDE.md`/`GEMINI.md` patterns), prefer creating a small `DEEPSEEK.md` project-context file and/or symlink the CLI's skill directory to `.agents/skills/` rather than duplicating skill content.

---

## ⚡ Quick Start (high level)

1. Confirm DeepSeek's integration surface (CLI vs API vs SDK). See "Discovery" below.
2. If CLI supports a project-context file (e.g. `DEEPSEEK.md`): create `~/dotfiles/DEEPSEEK.md` or instruct the CLI to read `.agents/harnesses/deepskee.md` and reference `.agents/skills/`.
3. If calling the provider API directly, implement a small adapter (`scripts/harness-deepskee/adapter.py`) that loads `.agents/skills/*/SKILL.md` and the master persona and forwards prompts to DeepSeek API.
4. Symlink skill directory only if the DeepSeek runtime expects a directory layout; prefer symlink to copying.
5. Verify with a minimal skill invocation: call the harness with a single `skill:presenthits` test and confirm output.

---

## Discovery (what to verify first)

Before wiring anything, perform these checks on the target machine / DeepSeek documentation:

- Does DeepSeek have an official CLI? If yes, what's the CLI binary name (`deepseek`, `deepskee`, `deepskee-cli`, ...)?
- Does the CLI auto-load a repository-level context file? If so, what is the filename (e.g. `DEEPSEEK.md` or `GEMINI.md` analog)?
- If there is no CLI project-context mechanism, does a documented config option exist to point at a skills dir or a persona file?
- If using an API/SDK, does the provider publish an official Python/Node SDK? (Prefer vendor SDK over reverse-engineered wrappers.)
- Authentication: what credentials does the provider expect (API key, OAuth)? Where is a safe local storage pattern (env var, keyring, credential helper)?

Record answers here after verification and update the Status to `ready`/`active` accordingly.

---

## Type (pick one; explain here)

- Recommended default: `api` — implement a small adapter that loads `.agents/skills/` and calls DeepSeek's HTTP API, storing credentials in environment variables or the OS keyring.
- Alternative (if CLI supports): `native` — rely on the CLI's auto-discovery and create `DEEPSEEK.md` that points at `.agents/skills/`.
- If you run a router/proxy for multiple providers, implement as `abstraction` and register DeepSeek as a backend in the router's config.

---

## Key file paths (what this harness uses in this repo)

- `.agents/skills/` — canonical skill sources (never duplicate these into harness docs)
- `.agents/instructions/base-personas/archi.md` — master persona reference
- `.agents/harnesses/deepskee.md` — this file
- Optional (if CLI expects a project file): `DEEPSEEK.md` at repo root

---

## Minimal adapter example (conceptual)

If API-based, an adapter should:

1. Load the requested SKILL.md from `.agents/skills/<skill>/SKILL.md` (parse `Triggers` / examples) or accept a skill name and map it into a prompt template.
2. Compose the final system+user prompt with the master persona (archi) + skill instructions.
3. Send to DeepSeek's API with credentials from env var `DEEPSEEK_API_KEY` (example name; verify real name).
4. Return the provider response to the caller (CLI/HTTP/CLI wrapper).

(Do not implement this adapter until the provider's SDK/HTTP spec is verified.)

---

## Environment and secrets

- Prefer `DEEPSEEK_API_KEY` (env var) or OS keyring. Avoid committing credentials to repo.
- If the provider issues long-lived tokens, store them in the user's secret manager (Keychain, libsecret, etc.) and document retrieval steps in this file.

---

## Deployment / Verification Checklist

- [ ] Confirm CLI or API surface (binary name, project-context filename, SDK availability). Update this file with findings.
- [ ] Decide harness Type (`native`/`api`/`abstraction`) and set `Status: ready`.
- [ ] If `native`, create `DEEPSEEK.md` (root) or document required config for the CLI and add an example.
- [ ] If `api`, implement a minimal adapter in `scripts/harness-deepskee/` and add unit test calling a sandbox endpoint or a mocked API.
- [ ] Add CLI samples to test: `deepseek --version` or `python3 scripts/harness-deepskee/test_call.py --skill presenthits`
- [ ] Add a short verification doc with exact commands that were run and their output (store under `.agents/validation/deepskee/`).
- [ ] Add `DEEPSEEK` to `.agents/harnesses/TEMPLATE_INDEX.md` (if you maintain an index) and register any required symlinks in `setup.sh`/`sync.sh` if applicable.
- [ ] Commit the changes to a branch `claude/deepskee-harness` and open a PR for review per repo rules.

---

## Example `DEEPSEEK.md` (if CLI requires a project-context file)

```md
# DeepSeek project context
# NOTE: verify actual filename & semantics before using

# Master persona
include: .agents/instructions/base-personas/archi.md

# Skills directory
skills_dir: .agents/skills/

# Skill triggers (optional mapping)
trigger_map:
  presenthits: presenthits
  projecthits: projecthits
```

(Do not create the above file until the CLI's expected format is verified.)

---

## Notes & caveats

- This harness file intentionally avoids code samples that assume an SDK name or CLI flag (`--load-context`) that hasn't been verified — prefer verification-first. The repo's policy is to document discovery behavior precisely and then implement only what is real.
- If DeepSeek's public docs are unavailable or the provider uses closed tooling, consider implementing a small `abstraction` harness that proxies to whichever upstream is available (Claude/Gemini/OpenAI) as a fallback.

---

## Next steps for me (ask the user to confirm/allow)

1. Verify `deepseek`/`deepskee` CLI availability on this machine (`which deepseek` / `deepseek --help`).
2. If CLI exists, discover expected project-context filename and whether it supports `skills_dir` or `include` directives.
3. If CLI is absent, check provider docs for an official HTTP API/SDK and return a recommended adapter implementation.
4. After verification, implement the minimal adapter or create `DEEPSEEK.md` and run the verification checklist.

---

Maintainer: nmc-costa
Last edited: 2026-09-17

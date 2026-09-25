# 🤝 Contributing - Adding New Harnesses

**This guide explains how to add a new LLM harness to this repo.**

There is no `/my/agentic_instructions/` — this repo (`~/dotfiles`) is the single source of
truth. There is also no `REGISTRY.md` (the old one, from the retired `agentic_instructions`
repo, was aspirational/stale and was not carried over) and no per-harness subdirectory with a
separate `integration-guide.md` — each harness is **one file**:
`.agents/harnesses/{harness-name}.md`.

---

## 🚀 Quick Process (3 Steps)

### Step 1: Copy the Template

```bash
cp .agents/harnesses/TEMPLATE.md .agents/harnesses/{new-harness-name}.md
```

Replace `{new-harness-name}` with the actual name (e.g., `claude-code`, `groq`, `together-ai`).

### Step 2: Write the Harness Doc

Edit `.agents/harnesses/{new-harness-name}.md` directly — see
[`.agents/harnesses/TEMPLATE.md`](harnesses/TEMPLATE.md) for the expected sections (how the
harness actually discovers instructions, key file paths in this repo, a skill/trigger table, a
deployment checklist). Look at `.agents/harnesses/claude-code.md` or
`.agents/harnesses/vscode-copilot.md` for harnesses whose auto-discovery mechanism is real and
verified, and at `.agents/harnesses/openai.md` or `.agents/harnesses/litellm.md` for the
"you write the glue code yourself" pattern.

**Be honest about what's real.** The previous version of several harness docs in this repo
described fictional mechanisms (a `.claude/.instructions.md` single-file auto-discovery/registry
that doesn't exist, an `openai.ChatCompletion.create(..., system=...)` call that was never valid
API usage, a mixed-up example that called the Anthropic SDK "the Gemini API"). Don't guess at
how a harness works — verify it, or clearly mark what's unverified.

### Step 3: Update Copilot Discovery (if relevant)

If the new harness should be mentioned to Copilot, add it to `.agents/AGENT.md` (reached from
the root `AGENTS.md`, which is what GitHub Copilot actually reads) — there's no separate registry
to update.

**Done!** ✅

---

## 📋 Detailed Checklist

### Before Starting
- [ ] New harness name decided (lowercase, hyphenated)
- [ ] You've confirmed — not assumed — how this harness actually loads instructions/skills
- [ ] API keys / setup instructions ready, if it's an API-based harness

### Writing `.agents/harnesses/{name}.md`
- [ ] Copied from `TEMPLATE.md`, all `{HARNESS-NAME}` placeholders replaced
- [ ] States plainly whether this is `native` (auto-discovery, like Claude Code/Copilot),
      `api` (you write the glue code), `abstraction` (multi-provider proxy), or `local`
- [ ] Every file path referenced actually exists under `.agents/` in this repo — no
      `/my/agentic_instructions/`, no `REGISTRY.md`, no `config/harness-config.json`
- [ ] Skill/persona trigger table included (see the "Common Tasks" table in `TEMPLATE.md`)
- [ ] Deployment/verification checklist included, specific to this harness
- [ ] If the harness needs a symlinked directory (like `.claude/skills/` does for Claude Code), that's
      set up — don't duplicate skill/instruction content into a harness-specific copy
- [ ] Any code samples use current, correct API syntax for that provider's SDK — test them if
      you can, don't just pattern-match off an old example

### If This Harness Needs Copilot/VS Code Awareness
- [ ] `.agents/AGENT.md` mentions it, if relevant

### Testing
- [ ] Confirm the harness actually reads the files you pointed it at (open a real session and
      check — don't just assume the doc is correct because it reads plausibly)
- [ ] Test at least one skill trigger end-to-end
- [ ] Test workspace config rules (`.agents/instructions/workspace-config/`) are followed

---

## 🔍 Example: Adding Groq

### Step 1: Copy Template
```bash
cp .agents/harnesses/TEMPLATE.md .agents/harnesses/groq.md
```

### Step 2: Edit `.agents/harnesses/groq.md`

Groq's API is OpenAI-compatible, so base this on `.agents/harnesses/openai.md` rather than
starting from scratch — same "you write the glue code" pattern, different `base_url` and model
names. Fix the model list and any Groq-specific setup (API key env var, rate limits) as you go.

### Step 3: Mention it in Copilot's instructions (optional)

If relevant, add a line to `.agents/AGENT.md` noting the new harness doc exists.

---

## ✅ File Structure After Adding New Harness

```
.agents/
├── harnesses/
│   ├── TEMPLATE.md
│   ├── vscode-copilot.md
│   ├── claude-code.md
│   ├── gemini.md
│   ├── openai.md
│   ├── litellm.md
│   └── {new-harness}.md   ← NEW (single file, no subdirectory)
```

Nothing needs to be duplicated outside `.agents/harnesses/`.

---

## 🎯 Benefits of This Process

✅ **Scalable** — same process for any new harness
✅ **Consistent** — all harnesses follow the same template
✅ **Maintainable** — one file per harness, no separate integration-guide subdirectory to keep
   in sync
✅ **No Duplication** — `.agents/` is the single source of truth; no `.github/` mirror
✅ **Honest** — every harness doc states plainly what's verified vs. what still needs checking

---

## 📞 Questions?

1. **Need help with a specific harness?** Check an existing `.agents/harnesses/*.md` for a
   similar provider/mechanism (native vs. API vs. abstraction).
2. **Need to update all harnesses at once?** Edit `TEMPLATE.md`, then update each harness file
   individually — there's no registry to regenerate from.
3. **Want to add a new skill?** See [`.agents/skills/_templates/`](skills/_templates/).

---

## 🚀 Ready to Add a New Harness?

**Just follow the 3 steps above!** Writing one honest, verified `.agents/harnesses/{name}.md`
file is the whole job.

# 🤝 Contributing - Adding New Harnesses

**This guide explains how to add a new LLM harness to the Hybrid C architecture.**

---

## 🚀 Quick Process (4 Steps)

### Step 1: Copy the Template

```bash
cp .github/harnesses/TEMPLATE.md .github/harnesses/{new-harness-name}.md
```

Replace `{new-harness-name}` with actual name (e.g., `claude-code`, `groq`, `together-ai`)

### Step 2: Customize the Reference

Edit `.github/harnesses/{new-harness-name}.md`:
- Replace all `{HARNESS-NAME}` with actual name
- Update "Quick Links" section with harness-specific paths
- Add harness-specific configuration notes

**Example for Groq:**
```markdown
# 🔌 Groq Reference

**Status:** Active  
**Setup:** Via API + function calling  
**Task-Specific:** `/my/agentic_instructions/harnesses/groq/`
```

### Step 3: Create Integration Guide

Create integration guide in `/my/agentic_instructions/`:

```bash
mkdir -p /my/agentic_instructions/harnesses/{new-harness-name}/
touch /my/agentic_instructions/harnesses/{new-harness-name}/integration-guide.md
```

**Copy from existing harness as template:**
```bash
cp /my/agentic_instructions/harnesses/vscode-copilot/integration-guide.md \
   /my/agentic_instructions/harnesses/{new-harness-name}/integration-guide.md
```

### Step 4: Update Links

**In `.github/copilot-instructions.md`:**
Add to "Supported Harnesses" section:
```markdown
- {New Harness Name}: see `.github/harnesses/{new-harness-name}.md`
```

**In `/my/agentic_instructions/REGISTRY.md`:**
Add to harnesses table:
```markdown
| {New Harness} | `harnesses/{new-harness-name}/` | `integration-guide.md` | ✅ Active |
```

**Done!** ✅

---

## 📋 Detailed Checklist

### Before Starting
- [ ] New harness name decided (lowercase, hyphenated)
- [ ] Integration guide draft written
- [ ] API keys / setup instructions ready

### Phase 1: `.github/` Reference
- [ ] Copy TEMPLATE.md to `.github/harnesses/{name}.md`
- [ ] Update all `{HARNESS-NAME}` placeholders
- [ ] Review workspace config links
- [ ] Review agent trigger examples
- [ ] Test links are valid

### Phase 2: Integration Guide
- [ ] Create `/my/agentic_instructions/harnesses/{name}/` folder
- [ ] Copy existing integration-guide.md as template
- [ ] Update setup instructions
- [ ] Update agent trigger configuration
- [ ] Document harness-specific features
- [ ] Test with actual harness

### Phase 3: Central Links
- [ ] Update `.github/copilot-instructions.md`
- [ ] Update `/my/agentic_instructions/REGISTRY.md`
- [ ] Update `/my/agentic_instructions/README.md` if needed
- [ ] Test all links work

### Phase 4: Documentation
- [ ] Document in CONTRIBUTING.md
- [ ] Add to `.github/harnesses/` folder list
- [ ] Update main documentation index

### Phase 5: Testing
- [ ] Test harness auto-discovery (if applicable)
- [ ] Test agent triggers work
- [ ] Test workspace config is loaded
- [ ] Test all 7 agents accessible
- [ ] Test model routing works

---

## 📝 Template Content

### Reference File (`.github/harnesses/{name}.md`)

**Sections to include:**
1. Quick Links (workspace config, agents, setup guide)
2. Workspace Configuration (model routing, optimization, etc.)
3. Task-Specific Agents (all 7 with triggers)
4. Setup Instructions (link to integration guide)
5. Common Tasks (agent + command)
6. Central Discovery (link to REGISTRY.md)
7. Need Help (troubleshooting links)

### Integration Guide (`/my/agentic_instructions/harnesses/{name}/integration-guide.md`)

**Sections to include:**
1. Overview (what is this harness)
2. Prerequisites (API keys, software, etc.)
3. Installation (step-by-step setup)
4. Configuration (how to configure for agents)
5. Persona Loading (how to load personas)
6. Agent Trigger Setup (how to configure triggers)
7. Workspace Config Integration (how to load shared rules)
8. Multi-Agent Coordination (how @architect works)
9. Troubleshooting (common issues)
10. Examples (code/config examples)

---

## 🔍 Example: Adding Groq

### Step 1: Copy Template
```bash
cp .github/harnesses/TEMPLATE.md .github/harnesses/groq.md
```

### Step 2: Edit `.github/harnesses/groq.md`
```markdown
# 🔌 Groq Reference

**Status:** Active  
**Setup:** Via API + function calling  
**Task-Specific:** `/my/agentic_instructions/harnesses/groq/`

[Rest of content with {HARNESS-NAME} → Groq]
```

### Step 3: Create Integration Guide
```bash
mkdir -p /my/agentic_instructions/harnesses/groq
cp /my/agentic_instructions/harnesses/openai/integration-guide.md \
   /my/agentic_instructions/harnesses/groq/integration-guide.md
```

Edit to include Groq-specific setup (API key, model selection, etc.)

### Step 4: Update Links

**`.github/copilot-instructions.md`:**
```markdown
## Supported Harnesses

- VS Code Copilot: see `.github/harnesses/vscode-copilot.md`
- Claude Code: see `.github/harnesses/claude-code.md`
- Gemini: see `.github/harnesses/gemini.md`
- OpenAI: see `.github/harnesses/openai.md`
- LiteLLM: see `.github/harnesses/litellm.md`
- **Groq: see `.github/harnesses/groq.md`** ← NEW
```

**`/my/agentic_instructions/REGISTRY.md`:**
```markdown
| Groq | `harnesses/groq/` | `integration-guide.md` | ✅ Active |
```

---

## ✅ File Structure After Adding New Harness

```
.github/
├── copilot-instructions.md (updated)
└── harnesses/
    ├── TEMPLATE.md (template)
    ├── vscode-copilot.md
    ├── claude-code.md
    ├── gemini.md
    ├── openai.md
    ├── litellm.md
    └── {new-harness}.md ← NEW

my/agentic_instructions/
├── REGISTRY.md (updated)
├── harnesses/
    ├── vscode-copilot/
    ├── claude-code/
    ├── gemini/
    ├── openai/
    ├── litellm/
    └── {new-harness}/ ← NEW
        └── integration-guide.md
```

---

## 🎯 Benefits of This Process

✅ **Scalable** - Same process for any new harness  
✅ **Consistent** - All harnesses follow same pattern  
✅ **Maintainable** - Changes in one place, reflected everywhere  
✅ **Discoverable** - Every entry point linked  
✅ **No Duplication** - Single source of truth  
✅ **Easy to Extend** - Template makes it simple  

---

## 📞 Questions?

1. **Need help with specific harness?** Check existing integration-guide.md for similar provider
2. **Need to update all harnesses at once?** Edit TEMPLATE.md, then update each reference file
3. **Want to add new agent?** See `/my/agentic_instructions/agents/_templates/agent-template.md`
4. **Want to add new skill?** See `/my/agentic_instructions/skills/_templates/skill-template.md`

---

## 🚀 Ready to Add a New Harness?

**Just follow the 4 steps above!**

The process takes ~15 minutes and creates a fully-functional harness integration.

# projectHITs v4 Helpers — Quick Start Guide

## TL;DR

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Install dependencies (one time)
pip install -r requirements.txt

# Run complete workflow
python orchestrate.py your_template.docx your_brief.txt --project-name MyProject

# Review outputs in session folder
cat MyProject_markdown_YYYYMMDD_HHMM/completion_checklist.md
```

✅ Done. All 4 phases (Mirror → Fill → Check → Report) automated.

---

## Setup (One-Time)

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

pip install -r requirements.txt
```

**Dependencies installed:**
- `python-docx` — Parse DOCX files
- `pdfplumber` — Parse PDF files
- `PyPDF2` — PDF manipulation

---

## Workflow: Template → Mirror → Filled Document

### Step 1: Prepare Inputs

**You need:**
1. **Template file** — Any format: DOCX, LaTeX, Markdown, PDF, TXT
   - Example: `my_charter_template.docx`
   
2. **Project brief** — Any format: TXT, JSON, Markdown, Email
   - Example: `project_info.txt`

### Step 2: Run Orchestrator (All Phases at Once)

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python orchestrate.py my_charter_template.docx project_info.txt \
  --format markdown \
  --project-name MyProject
```

**What happens:**
1. ✅ Analyzes template structure
2. ✅ Generates Markdown mirror (structure only)
3. ✅ Auto-fills from brief (VARIABLE/ADAPTIVE content)
4. ✅ Marks missing sections with `[TODO]`
5. ✅ Generates prioritized checklist with director asks
6. ✅ Creates organized session folder

**Output folder:** `MyProject_markdown_20260820_1430/`

### Step 3: Review Completion Checklist

```bash
cat MyProject_markdown_20260820_1430/MyProject_completion_checklist.md
```

Example output:
```
# Completion Status Report

**Overall: 65% Complete**

## ✅ Filled Sections (8)
- [x] Executive Summary
- [x] Project Scope
- ... (8 total)

## ❓ Missing Information (2)
- [ ] Success Metrics
- [ ] Risk Mitigation

## 📋 Director Priority Queue

### 1. Success Metrics [Impact: HIGH]
**Missing:** Define 5-7 measurable KPIs with targets
**Question:** What are your top success metrics?

### 2. Risk Mitigation [Impact: MEDIUM]
**Missing:** Define mitigation strategies for identified risks
**Question:** How will you mitigate each risk?
```

### Step 4: Director Provides Missing Info

Director answers the prioritized questions:
- "Success Metrics: We want 85% accuracy, <5 min latency, 99.5% uptime"
- "Risk Mitigation: For sensor reliability, we'll use redundant sensors..."

### Step 5: Agent Refills & Updates Checklist

(This loop happens in the agent's Phase 5 of v4 workflow)

Agent runs:
```bash
# Refill with director's answers
python auto_filler.py MyProject_mirror.md director_answers.txt \
  --output MyProject_mirror_filled_v2.md

# Generate updated checklist
python completion_checker.py MyProject_mirror_filled_v2.md
```

Completion increases: 65% → 85% → 95% → ✅ 100%

---

## Quick Examples

### Example 1: Mirror a DOCX Template (No Brief)

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Just extract structure
python mirror_generator.py existing_charter.docx --format markdown

# Output:
# - existing_charter_mirror.md (empty structure)
# - existing_charter_mirror_analysis.json (structure map)
```

Use case: Director wants to review template layout before filling.

### Example 2: Auto-fill with Complete JSON Brief

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Assuming you have: template.docx, project.json
python orchestrate.py template.docx project.json \
  --format markdown \
  --project-name ClientAlpha

# Complete workflow runs, outputs organized session folder
```

Use case: Brief is well-structured, need fast turnaround.

### Example 3: Analyze Any Template Format

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Analyze a LaTeX template
python template_analyzer.py project_charter.tex

# Analyze a PDF
python template_analyzer.py old_charter.pdf

# Output: JSON with detected structure (sections, tables, pages)
```

Use case: Understanding existing template before adapting.

### Example 4: Refill After Director Feedback (Loop)

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Initial run
python orchestrate.py template.docx initial_brief.txt --project-name MyProject

# [Director reviews, provides feedback in director_feedback.txt]

# Refill only
python auto_filler.py MyProject_mirror.md director_feedback.txt \
  --output MyProject_mirror_filled_v2.md

# Update checklist
python completion_checker.py MyProject_mirror_filled_v2.md \
  --output MyProject_checklist_v2.md

# [Review new checklist, iterate...]
```

Use case: Brief arrives in stages, or multiple feedback rounds.

---

## Output Structure

After running orchestrator:

```
MyProject_markdown_20260820_1430/
│
├── MyProject_mirror.md
│   └── Structure-only copy (100% fidelity, 0% content)
│       Director validates: "Does this match the original?"
│
├── MyProject_mirror_analysis.json
│   └── Detected structure (sections, tables, metadata)
│
├── MyProject_mirror_filled.md
│   └── Partially filled mirror with embedded [TODO] markers
│       Agent result: "65% complete, see checklist for gaps"
│
├── MyProject_fill_mapping.json
│   └── Field-by-field mapping with confidence scores
│       Internal: Shows what was matched, confidence levels
│
├── MyProject_completion_checklist.md
│   └── Human-readable progress + prioritized director asks
│       Director uses: "I'll answer these 3 priority questions"
│
├── MyProject_completion_checklist.json
│   └── Machine-readable completion data
│       Agent uses: Tracks progress, triggers refills
│
├── workflow_summary.json
│   └── Metadata: inputs, outputs, next steps
│
└── README.md (optional)
    └── Session notes and decisions
```

---

## Key Features

### ✨ Format Agnostic
- Input: DOCX, LaTeX, Markdown, PDF, TXT
- Edit: Markdown (default), LaTeX, Plain Text
- Output: Any format (via phase 6 of v4 workflow)

### ✨ Structure-First
- Mirror replicates 100% of template structure
- Director validates before fills begin
- Prevents cascade errors from bad parsing

### ✨ Intelligent Filling
- VARIABLE fields: Always filled (project names, dates, budgets)
- ADAPTIVE fields: Adapted with context (risks, success criteria)
- REGENERATE fields: Marked [TODO] (needs research or director input)
- TODO fields: Marked transparently (director knows what's missing)

### ✨ Transparent Completion
- Auto-calculated completion %
- Prioritized by business impact (HIGH/MEDIUM/LOW)
- Specific director questions (not open-ended)
- Confidence scoring for auto-fills

### ✨ Session Tracking
- Organized folder per project/date
- All artifacts archived (audit trail)
- Enables rollback and version control

---

## Compilation (Phase 6)

When filled mirror is complete, compile final DOCX:

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python compiler.py \
  --template original_template.docx \
  --content MyProject_mirror_filled.md \
  --output MyProject_Final.docx
```

✅ Final document generated with all styles preserved!

---

## Troubleshooting

### Q: "ModuleNotFoundError"
A: Install dependencies: `pip install -r requirements.txt`

### Q: "Mirror doesn't match template structure"
A: Check template uses proper heading styles:
- DOCX: Heading 1, Heading 2, Heading 3
- LaTeX: \section, \subsection, \subsubsection
- Markdown: #, ##, ###

### Q: "Auto-fill didn't match expected fields"
A: 
1. Check brief format (JSON recommended for accuracy)
2. For TXT: ensure keywords like "Objectives:", "Budget:" are present
3. Review `_fill_mapping.json` for confidence scores (< 50% = low confidence)

### Q: "Completion checker found 0 sections"
A: The filled mirror may not have any proper headers. Check:
1. Mirror structure was correct (Step 2)
2. Auto-fill didn't corrupt headers (unlikely, but possible)
3. Use `completion_checker.py` with verbose output

---

## Integration with v4 Agent

These helpers automate **Phases 1-4 and 6** of the v4 workflow:

| Phase | Agent Action | Helper Used |
|-------|--------------|-------------|
| **1. Mirror** | Parse template, generate structure-only copy | `v4/mirror_generator.py` |
| **2. Validate** | *(Director action)* Approve mirror structure | *(manual review)* |
| **3. Auto-fill** | Fill from brief, mark TODOs, confidence score | `v4/auto_filler.py` |
| **4. Report** | Scan TODOs, prioritize gaps, ask questions | `v4/completion_checker.py` |
| **5. Gap-fill Loop** | *(Director + Agent loop)* Answer → refill → checklist | `v4/auto_filler.py` + `v4/completion_checker.py` |
| **6. Compile** | Inject filled mirror into original template | `v4/compiler.py` |
| **7. QA** | *(Director action)* Review final file | *(manual review)* |

**Helpers cover Phases 1-4 and 6 automatically. Agent handles phase 5 (loop) and 7 (archiving) with director oversight.**

---

## Performance

| Helper | Time | Notes |
|--------|------|-------|
| template_analyzer | < 1 sec | Fast for DOCX/Markdown, 2-5 sec for PDF |
| mirror_generator | < 1 sec | Structure complexity doesn't affect speed |
| auto_filler | 1-3 sec | Depends on brief complexity |
| completion_checker | < 1 sec | Linear scan for TODOs |
| orchestrate (all 4) | ~5-10 sec | Total for complete workflow |

---

## Next Steps After Phase 4

Once orchestrator completes:

1. **Review** `completion_checklist.md`
   - See overall completion %
   - Identify priority gaps
   - Read suggested director questions

2. **Provide Director Input**
   - Answer the prioritized questions
   - Save answers in `director_feedback.txt` or `director_answers.json`

3. **Agent Refills** (Phase 5 of v4 workflow)
   - Run `auto_filler.py` with feedback
   - Run `completion_checker.py` to update checklist
   - Show director updated status

4. **Iterate** until 100% or director approves freeze

5. **Agent Compiles** (Phase 6 of v4 workflow)
   - Apply filled mirror to original template
   - Preserve all styles, structure, formatting
   - Generate final DOCX/PDF/Markdown

6. **Director QA** (Phase 7 of v4 workflow)
   - Review final document
   - Approve for delivery

---

## Questions?

- See `README.md` for detailed helper documentation
- See `README.md` in this folder (the old versioned spec file was retired, not migrated) for complete v4 workflow
- See `INDEX.md` for file inventory and quick reference
- See example sessions in `results/projectHITs/` for reference

---

**Version:** v4.0 | **Status:** Production Ready | **Last Updated:** 2026-08-20

# projectHITs v4 Helpers Index

Complete toolkit for automating the Mirror Architect workflow (Phases 1-4, 6).

## Helpers Overview

| Helper | Phase | Purpose | Input | Output |
|--------|-------|---------|-------|--------|
| **template_analyzer.py** | 1 | Parse template structure | Any format (DOCX/LaTeX/MD/PDF/TXT) | Structure analysis JSON |
| **mirror_generator.py** | 2 | Generate structure-only mirror | Template + editable format choice | Mirror file + structure map |
| **auto_filler.py** | 3 | Fill mirror from brief | Mirror + project brief | Filled mirror + TODO markers |
| **completion_checker.py** | 4 | Generate completion checklist | Filled mirror | Checklist + prioritized asks |
| **compiler.py** | 6 | Compile filled mirror to final DOCX | Filled mirror + original template | Final DOCX with preserved styles |
| **orchestrate.py** | 1-4 | Run all phases at once | Template + brief | Organized session folder |

---

## Quick Reference

### All-in-One Command

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python orchestrate.py <template> <brief> --format markdown --project-name ProjectName
```

### Phase-by-Phase

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Phase 1: Analyze
python template_analyzer.py template.docx

# Phase 2: Mirror
python mirror_generator.py template.docx --format markdown

# Phase 3: Fill
python auto_filler.py mirror.md brief.txt

# Phase 4: Check
python completion_checker.py filled.md

# Phase 6: Compile
python compiler.py --template template.docx --content filled.md --output final.docx
```

---

## File Inventory

```
~/dotfiles/.agents/skills/projecthits/scripts/v4/
├── v4/
│   ├── template_analyzer.py       ← Phase 1: Parse templates
│   ├── mirror_generator.py        ← Phase 2: Generate mirrors
│   ├── auto_filler.py             ← Phase 3: Fill from briefs
│   ├── completion_checker.py      ← Phase 4: Generate checklists
│   ├── compiler.py                ← Phase 6: Compile to DOCX
│   └── orchestrate.py             ← Run phases 1-4 at once
│
├── docs/
│   ├── README.md                  ← Comprehensive guide
│   ├── QUICKSTART.md              ← Quick start (5 min)
│   └── INDEX.md                   ← This file
│
├── __init__.py                    ← Package initialization
├── requirements.txt               ← Dependencies
└── results/                       ← Session outputs (created at runtime)
```

---

## Setup

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Install dependencies (one time)
pip install -r requirements.txt

# Run helpers
python orchestrate.py template.docx brief.txt
```

---

## Documentation

1. **QUICKSTART.md** — Start here (5 min read)
   - TL;DR usage
   - Setup
   - Examples
   - Troubleshooting

2. **README.md** — Complete reference (20 min read)
   - Detailed usage for each helper
   - All supported formats
   - Integration with v4 workflow
   - Performance notes

3. **projectHITs_v4.md** — Full specification (30 min read)
   - Complete v4 workflow (Phases 1-7)
   - Agent calibration header
   - Critical rules and anti-patterns
   - Session example walkthrough

---

## Workflow Context

These helpers automate **Phases 1-4 and 6** of the v4 workflow:

```
Phase 1: Mirror          [Agent → template_analyzer + mirror_generator]
Phase 2: Validate        [Director → manual review of mirror]
Phase 3: Auto-fill       [Agent → auto_filler]
Phase 4: Report          [Agent → completion_checker]
Phase 5: Gap-fill Loop   [Director ↔ Agent → iterate auto_filler + completion_checker]
Phase 6: Compile         [Agent → compiler.py]
Phase 7: QA + Archive    [Director + Agent → final delivery]
```

Helpers cover Phases 1-4 and 6. Agent handles Phase 5 (loop) and 7 (archiving) with director oversight.

---

## Typical Execution

```
1. director uploads template + brief
   ↓
2. agent runs orchestrate.py (all 4 phases)
   ├→ Analyzes template structure
   ├→ Generates mirror (director validates)
   ├→ Auto-fills from brief
   └→ Generates checklist + asks
   ↓
3. director reviews completion checklist
   ↓
4. director provides answers to priority gaps
   ↓
5. agent refills (phases 3-4 loop) with new data
   ↓
6. [repeat 4-5 until complete]
   ↓
7. agent compiles final output
   ↓
8. director QA approves
   ✅ Done
```

---

## Support Resources

- **Issues with helpers?** Check QUICKSTART.md troubleshooting section
- **Want detailed info?** See README.md for complete reference
- **Full workflow?** See `README.md` in this folder (the old versioned spec file was retired, not migrated)
- **Questions?** Check relevant helper's docstring: `python helper.py --help`

---

## Performance

- **orchestrate.py (all 4):** ~5-10 sec
- **Each helper:** < 3 sec (except PDF parsing: 2-5 sec)
- **No dependencies on external services** (local processing only)

---

## Integration Points

- **With v4 Agent:** Helpers automate Phases 1-4, agent controls phases 5-7
- **With Version Control:** Session folders enable rollback and audit trail
- **With Python Ecosystem:** Modular design allows custom extensions

---

## Next Steps

- **Issues with helpers?** Check QUICKSTART.md troubleshooting section
- **Want detailed info?** See README.md for complete reference
- **Full workflow?** See `README.md` in this folder (the old versioned spec file was retired, not migrated)
- **Questions?** Check relevant helper's docstring: `python helper.py --help`
2. Read QUICKSTART.md (5 min)
3. Run example: `python orchestrate.py --help`
4. Use with your templates and briefs

---

**Version:** v4.0 | **Status:** Production Ready | **Last Updated:** 2026-08-20

For questions or issues, refer to:
- `helpers/QUICKSTART.md` — Quick answers
- `helpers/README.md` — Detailed reference
- `README.md` in this folder (the old versioned spec file was retired, not migrated) — Workflow spec

# projectHITs v4 Helper Scripts

Complete toolkit for the Mirror Architect workflow (Phases 1-4, 6 of v4).

## Overview

These helpers automate key phases of the projectHITs v4 workflow:

1. **template_analyzer.py** — Parse any template format and extract structure
2. **mirror_generator.py** — Generate exact-structure mirrors (zero content)
3. **auto_filler.py** — Auto-fill mirrors from project briefs
4. **completion_checker.py** — Scan for TODOs and generate completion checklists
5. **compiler.py** — Compile filled mirror back to final DOCX with styles preserved
6. **orchestrate.py** — Run phases 1-4 in one command

## Quick Start

### Option A: Run Full Workflow (Recommended)

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python orchestrate.py <template.docx> <brief.txt> --format markdown --project-name MyProject
```

**Output:** Session folder with all artifacts organized and ready for director review.

### Option B: Run Individual Helpers

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

# Phase 1: Analyze template
python template_analyzer.py template.docx --output analysis.json

# Phase 2: Generate mirror
python mirror_generator.py template.docx --format markdown --output mirror.md

# Phase 3: Auto-fill from brief
python auto_filler.py mirror.md brief.txt --output filled.md

# Phase 4: Generate checklist
python completion_checker.py filled.md --output checklist.md

# Phase 6: Compile to final DOCX
python compiler.py --template template.docx --content filled.md --output final.docx
```

---

## Detailed Usage

### 1. template_analyzer.py

**Purpose:** Parse template in any format and extract structure information.

**Supported Formats:**
- DOCX (Word documents)
- LaTeX files (.tex)
- Markdown (.md)
- PDF files
- Plain text (.txt)

**Usage:**

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python template_analyzer.py <template_path> [--output output.json]
```

**Examples:**

```bash
python template_analyzer.py charter.docx
python template_analyzer.py project.tex --output structure.json
python template_analyzer.py template.md
```

**Output:**

```json
{
  "format": "docx",
  "total_paragraphs": 45,
  "total_tables": 3,
  "sections": [
    {"level": 1, "title": "Executive Summary", "type": "heading"},
    {"level": 2, "title": "Project Scope", "type": "heading"}
  ],
  "tables": [
    {"index": 0, "rows": 5, "cols": 3, "content": [...]}
  ],
  "metadata": {
    "title": "Project Charter",
    "author": "John Doe",
    "created": "2026-08-20T10:00:00"
  }
}
```

---

### 2. mirror_generator.py

**Purpose:** Generate exact-structure copy of template in editable format (Markdown/LaTeX/Text).

Mirrors replicate 100% of structure (headings, tables, hierarchy) with zero content (only placeholders).

**Usage:**

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python mirror_generator.py <template_path> [--format markdown|latex|text] [--output output.md]
```

**Examples:**

```bash
# Default: DOCX → Markdown mirror
python mirror_generator.py charter.docx

# Generate LaTeX mirror
python mirror_generator.py charter.docx --format latex --output charter_mirror.tex

# Generate plain text mirror
python mirror_generator.py charter.docx --format text
```

**Output:**

Two files:
1. `{template}_mirror.md` — Editable structure mirror
2. `{template}_mirror_analysis.json` — Structure map with section indices

**Example Mirror Output:**

```markdown
# Project Document (Mirrored from DOCX)

*This is a structure-only mirror. Replace placeholders with actual content.*

**Template Title:** Project Charter Template
**Template Author:** John Doe

# Executive Summary

[Content: Executive summary placeholder]

## Project Scope

[Content: Scope details]

### Objectives

[Content: List of objectives]

## Team Structure

| Role | Name | Email |
|------|------|-------|
| [Content] | [Content] | [Content] |

## Budget Overview

[Content: Budget breakdown]
```

**Key Feature:** Director can validate mirror structure against original template *before* any fills begin.

---

### 3. auto_filler.py

**Purpose:** Parse project brief and intelligently fill mirror sections with VARIABLE, ADAPTIVE, REGENERATE, and TODO content.

**Supported Brief Formats:**
- JSON (structured)
- Markdown
- Plain text (with regex pattern matching)
- Email format

**Usage:**

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python auto_filler.py <mirror_path> <brief_path> [--output output.md]
```

**Examples:**

```bash
# Auto-fill from text brief
python auto_filler.py charter_mirror.md project_brief.txt

# Auto-fill from JSON brief
python auto_filler.py charter_mirror.md project.json --output filled.md

# Auto-fill from markdown brief
python auto_filler.py charter_mirror.md brief.md
```

**Brief Format: Plain Text Example**

```
Project Name: PreditSense Platform
Description: Industrial IoT predictive maintenance system

Start Date: 2026-09-01
End Date: 2026-12-31

Budget: $250,000

Team:
- Alice Johnson (Project Manager)
- Bob Smith (Lead Engineer)
- Carol White (Data Scientist)

Objectives:
- Reduce equipment downtime by 30%
- Implement real-time monitoring across 50 assets
- Deploy predictive models with >85% accuracy

Scope:
- IoT sensor integration
- Time-series data pipeline
- ML model training and inference
- Web dashboard

Risks:
- Sensor reliability in harsh environments
- Data quality issues from legacy systems
- Skill gaps in team (ML experience)

Success Criteria:
- 85%+ model accuracy
- <5 min latency for predictions
- 99.5% system uptime
- 300+ monitored assets

Stakeholders:
- Plant Manager (sponsor)
- Operations Team (end users)
- IT Department (infrastructure)
```

**Brief Format: JSON Example**

```json
{
  "project": {
    "name": "PreditSense Platform",
    "description": "Industrial IoT predictive maintenance"
  },
  "timeline": {
    "start_date": "2026-09-01",
    "end_date": "2026-12-31"
  },
  "budget": {
    "total": "250000"
  },
  "team": {
    "pm": "Alice Johnson",
    "lead_engineer": "Bob Smith",
    "data_scientist": "Carol White"
  },
  "objectives": [
    "Reduce equipment downtime by 30%",
    "Implement real-time monitoring across 50 assets"
  ],
  "scope": "IoT integration, data pipeline, ML models, dashboard",
  "risks": [
    "Sensor reliability",
    "Data quality issues",
    "ML skill gaps"
  ],
  "success_criteria": [
    "85%+ model accuracy",
    "99.5% uptime"
  ]
}
```

**Output:**

Two files:
1. `{mirror}_filled.md` — Partially filled mirror with embedded `[TODO]` markers
2. `{mirror}_fill_mapping.json` — Field-by-field mapping with confidence scores

**Example Filled Output:**

```markdown
# Executive Summary

PreditSense Platform — Industrial IoT predictive maintenance system

## Project Scope

IoT integration, data pipeline, ML models, dashboard

### Objectives

- Reduce equipment downtime by 30%
- Implement real-time monitoring across 50 assets

[TODO: Provide alignment with Q3 business targets]

## Team Structure

- Alice Johnson (Project Manager)
- Bob Smith (Lead Engineer)
- Carol White (Data Scientist)

## Budget Overview

$250,000

## Timeline

**Start:** 2026-09-01
**End:** 2026-12-31

[TODO: Define key milestones and dependencies]

## Success Metrics

- 85%+ model accuracy
- <5 min latency for predictions
- 99.5% system uptime

[TODO: Define specific KPI dashboard and reporting frequency]

## Risks

- Sensor reliability in harsh environments
- Data quality issues from legacy systems
- Skill gaps in team (ML experience)

[TODO: Define mitigation strategies for each risk]
```

**Confidence Scoring:** Auto-filled sections are tagged with confidence levels:
- `[REVIEW: Confidence 60%. Please verify...]` — Low confidence, needs director review
- No tag — High confidence (>80%), auto-approved

---

### 4. completion_checker.py

**Purpose:** Scan filled mirror for `[TODO]` markers and generate prioritized completion checklist with specific director asks.

**Usage:**

```bash
python completion_checker.py <filled_mirror_path> [--output output.md]
```

**Examples:**

```bash
python completion_checker.py charter_filled.md

# Custom output path
python completion_checker.py charter_filled.md --output my_checklist.md
```

**Output:**

Two files:
1. `{mirror}_completion_checklist.md` — Human-readable checklist with prioritized director asks
2. `{mirror}_completion_checklist.json` — Machine-readable completion data

**Example Checklist Output:**

```markdown
# Completion Status Report

**Overall: 65% Complete**

Generated: 2026-08-20 14:30:15

## ✅ Filled Sections
- [x] Executive Summary
- [x] Project Scope
- [x] Team Structure
- [x] Budget Overview
- [x] Timeline
- [x] Objectives
- [x] Approval Chain
- [x] Communication Plan

## 🔍 Partial / Flagged for Review
- [~] Success Metrics (1 review)
- [~] Timeline (1 review)

## ❓ Missing Information — Director Input Required
- [ ] Success Metrics (2 TODOs)
- [ ] Risks (1 TODO)

## 📋 Director Priority Queue

**Address these items in order to unblock progress:**

### 1. Success Metrics [Impact: HIGH]

**Missing:** Define specific KPI dashboard and reporting frequency

**Question:** For Success Metrics: Define 5-7 success metrics with targets and measurement methods.

### 2. Timeline [Impact: HIGH]

**Missing:** Define key milestones and dependencies

**Question:** For Timeline: Provide key milestones and dependencies (dates, blockers).

### 3. Risks [Impact: MEDIUM]

**Missing:** Define mitigation strategies for each risk

**Question:** For Risks: Identify top 3-5 risks with likelihood, impact, and mitigation strategies.

## 📊 Summary

- **Total Sections:** 12
- **Completed:** 8/12
- **Partial:** 2
- **Incomplete:** 2
- **Total TODOs:** 5

## ✨ Next Steps

1. Review the Priority Queue above
2. Provide answers to the suggested questions
3. Agent will refill the mirror with your answers
4. Repeat until all sections complete or director approves current state
```

**Features:**
- Automatically calculates completion %
- Identifies section-by-section status
- Generates specific director questions (not open-ended)
- Prioritizes gaps by business impact
- Provides context for each missing item

---

### 5. compiler.py (Phase 6: Compilation)

**Purpose:** Inject filled mirror content back into original template while preserving all styles, formatting, and structure.

**Use Case:** After director completes all TODOs and approves filled mirror, compile final output that looks exactly like the original template but with new content.

**Usage:**

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python compiler.py \
  --template original_template.docx \
  --content filled_mirror.md \
  --output final_document.docx
```

**Examples:**

```bash
# Basic compilation
python compiler.py --template charter.docx --content charter_filled.md --output charter_final.docx

# With log file for audit trail
python compiler.py \
  --template template.docx \
  --content filled.md \
  --output final.docx \
  --log compilation_log.json

# With field replacements JSON
python compiler.py \
  --template template.docx \
  --content filled.md \
  --replacements replacements.json \
  --output final.docx
```

**Output:**

- `final_document.docx` — Complete DOCX with all content filled and styles preserved
- `compilation_log.json` (optional) — Audit trail of what was injected, replacements made, errors encountered

**Features:**
- ✅ Preserves all original DOCX formatting (fonts, colors, styles)
- ✅ Maintains section structure and hierarchy
- ✅ Injects markdown content into corresponding sections
- ✅ Applies field-level replacements (from replacements.json)
- ✅ Generates audit log of all injections
- ✅ Handles tables and complex formatting
- ✅ Supports both section-level and field-level replacements

**Example Workflow:**

```bash
# 1. Generate filled mirror through phases 1-4
python orchestrate.py charter.docx brief.txt --project-name MyProject

# 2. Director reviews completion checklist and provides answers
# (saves to director_answers.txt)

# 3. Agent refills and gets to 100%
python auto_filler.py MyProject_mirror.md director_answers.txt --output MyProject_filled.md
python completion_checker.py MyProject_filled.md

# 4. When approved (100% complete), compile final DOCX
python compiler.py \
  --template charter.docx \
  --content MyProject_filled.md \
  --output MyProject_Final_Charter.docx

# 5. Director does final QA on output
# Done! Ready for delivery.
```

---

### 6. orchestrate.py (All-in-One)

**Purpose:** Run complete workflow (Phases 1-4) in a single command with organized session folder.

**Usage:**

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

python orchestrate.py <template_path> <brief_path> [--format markdown|latex|text] [--project-name MyProject]
```

**Examples:**

```bash
# Full workflow with defaults
python orchestrate.py charter.docx project_brief.txt

# Specify editable format and project name
python orchestrate.py charter.docx brief.json --format markdown --project-name PreditSense

# LaTeX editing format
python orchestrate.py charter.tex brief.txt --format latex --project-name MyProject
```

**Output:**

Creates organized session folder: `{project_name}_{format}_{timestamp}/`

```
PreditSense_markdown_20260820_1430/
├── 1_mirror/
│   ├── PreditSense_mirror.md
│   ├── PreditSense_mirror_analysis.json
│   └── mirror_validation_signoff.txt
├── 2_filled/
│   ├── PreditSense_mirror_filled.md
│   ├── PreditSense_fill_mapping.json
│   └── director_questions_answers.md
├── 3_completion/
│   ├── PreditSense_completion_checklist.md
│   ├── PreditSense_completion_checklist.json
│   └── priority_queue.md
├── audit_trail.md
├── workflow_summary.json
└── README.md (auto-generated)
```

**Session Contents:**

- `workflow_summary.json` — Complete workflow metadata + next steps
- All analyzer, mirror, fill, and completion outputs
- Organized by phase for easy navigation
- Audit trail with timestamps

---

## Integration with v4 Agent Workflow

### Phase 1: Mirror Generation
**Agent uses:** `v4/mirror_generator.py`
- Input: Template file (any format)
- Output: Markdown mirror + structure analysis
- Director action: Validate mirror structure

### Phase 2: Auto-filling
**Agent uses:** `v4/auto_filler.py`
- Input: Approved mirror + project brief
- Output: Filled mirror with [TODO] markers
- Director action: Review completion checklist

### Phase 3: Completion Checking
**Agent uses:** `v4/completion_checker.py`
- Input: Filled mirror
- Output: Prioritized checklist + director asks
- Director action: Answer specific questions

### Phase 4: Iterative Gap-Filling
**Agent loops back to:**
- `v4/auto_filler.py` (refill with director answers)
- `v4/completion_checker.py` (update checklist)
- Repeat until 100% complete or director approves freeze

### Phase 6: Compilation
**Agent uses:** `v4/compiler.py`
- Input: Filled mirror + original template
- Output: Final DOCX with all styles preserved
- Director action: Final QA review

---

## Dependencies

```bash
cd ~/dotfiles/.agents/skills/projecthits/scripts/v4

pip install -r requirements.txt
```

**requirements.txt:**

```
python-docx>=0.8.11
pdfplumber>=0.9.0
PyPDF2>=3.0.0
```

---

## Examples & Workflows

### Workflow 1: Quick DOCX-to-Markdown (No Brief)

```bash
# Just mirror the structure (no auto-fill)
python mirror_generator.py existing_charter.docx --format markdown
```

Use this when:
- Director only wants to review template structure
- Brief not ready yet
- Just setting up editable source file

### Workflow 2: Full Automation (Complete Brief Available)

```bash
# Run orchestrator for complete workflow
python orchestrate.py charter.docx project.json --project-name ClientName
```

Use this when:
- Brief is comprehensive (JSON preferred)
- Streamline Phase 1-4 execution
- Create organized session for audit trail

### Workflow 3: Gradual Fill (Brief Arrives in Stages)

```bash
# Phase 1-2: Mirror only
python mirror_generator.py charter.docx

# [Director validates mirror]

# Phase 3: Auto-fill with partial brief
python auto_filler.py charter_mirror.md brief_part1.txt

# [Review checklist, identify gaps]

# Phase 3b: Refill with additional brief data
python auto_filler.py charter_mirror.md brief_part2.txt

# Phase 4: Final checklist
python completion_checker.py charter_mirror_filled.md
```

Use this when:
- Brief arrives incrementally
- Director needs to see progress mid-workflow
- Build momentum with early wins

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'docx'"

```bash
pip install python-docx
```

### Error: "PDF parsing failed"

```bash
pip install pdfplumber
```

### Mirror structure doesn't match original

1. Check `{template}_mirror_analysis.json` for detected sections
2. Verify original template uses proper heading styles (Heading 1, 2, 3 in DOCX)
3. LaTeX: ensure `\section`, `\subsection`, `\subsubsection` commands used
4. Markdown: ensure `#`, `##`, `###` hierarchy followed

### Auto-fill didn't match expected fields

1. Check brief format (JSON vs text)
2. For text: ensure keywords like "Objectives:", "Budget:", etc. present
3. Review `{mirror}_fill_mapping.json` for confidence scores
4. Low confidence fills are marked `[REVIEW]` — director verifies accuracy

---

## Performance Notes

- **template_analyzer.py:** < 1 sec for DOCX/Markdown, 2-5 sec for PDF
- **mirror_generator.py:** < 1 sec (structure complexity doesn't affect speed)
- **auto_filler.py:** 1-3 sec depending on brief size/complexity
- **completion_checker.py:** < 1 sec
- **orchestrate.py:** ~5-10 sec total for all four phases

---

## Next Steps

After Phase 4 (Completion Checker), the **director**:

1. Reviews `completion_checklist.md`
2. Identifies priority gaps from "Director Priority Queue"
3. Answers agent's specific questions
4. Agent loops back to `auto_filler.py` to refill with answers
5. Repeat Phases 3-4 until done

Then Phase 5-7 (Compilation, QA, Archive) handled by agent in v4 main workflow.

---

## Support

- Questions? See `projectHITs_v4.md` (main workflow document)
- Issues with specific helper? Check usage section above + examples
- Need to extend? Helpers are modular — fork and customize

---

**Version:** v4.0 | **Last Updated:** 2026-08-20

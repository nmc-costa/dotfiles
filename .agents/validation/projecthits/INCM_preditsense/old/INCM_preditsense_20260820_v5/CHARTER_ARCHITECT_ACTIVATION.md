# Charter Architect Activation Guide

## Overview

The Charter Architect has been enhanced with **Preservation Mode Persona** and **Operational Calibration Protocols**. This document explains how to activate and interact with the agent at peak capabilities.

---

## Status: ✅ READY FOR ACTIVATION

**simplifyHIT/SKILL.md:** 95% PASS ✅ (3,037/3,500 tokens)  
**projectHITs_v2.md:** 91% PASS ✅ (4,489/4,500 tokens)

---

## What Changed

### 1. Persona Injection ✅

**Identity:** "The Charter Architect" operating in **Preservation Mode** (Template-Aware Co-Creation)

**Prime Directive:**
1. You are a Guardian of Validated Templates (structural conformance)
2. You are NOT a general document generator; you are DOCX-aware
3. Mantra: "I preserve validated templates, replace what changes, regenerate what's critical, optimize what's reusable"

### 2. Operational Protocol ✅

**Calibration Header** (begins every response):
```
SYSTEM INSTRUCTION: MODE [CHARTER_ARCHITECT] ACTIVE
STATUS: [Current Action: Parsing Template / Identifying Variables / Writing Charter / Manipulating DOCX]
RESONANCE: [Confidence: 0-10] | [Focus: {Primary Task}] | [Entropy: Stable/High]
DIALECTIC: [Tension: 0-10] | [Antithesis: {Risk or Preservation Challenge}]
ANALYSIS: [Meta-cognitive summary of Sponsor's project intent]
TIMESTAMP: [Current date and time]
TEMPLATE: [Base Template File Used]
PRESERVATION_STATUS: [Rigid Fields: N] | [Variables to Replace: N] | [Adaptive: N]
```

### 3. DOCX-Aware Capabilities ✅

**Agent NOW DOES:**
- Analyze DOCX structure + detect template domain
- Build intelligent replacement maps (VARIABLE/ADAPTIVE/REGENERATE)
- Research content + generate 2-3 versions
- Validate content via peer review
- Manipulate DOCX using `python-docx` while maintaining 100% structural fidelity
- Track all changes in JSON + markdown for audit trail

**Agent DOES NOT:**
- Refuse DOCX manipulation requests
- Invent new document structure
- Skip content validation
- Bypass sponsor approval gates

### 4. Enhanced Workflow ✅

**7 Phases (instead of 5):**
1. ✅ Analyze Template (5 min, ~300 tokens)
2. ✅ Build Replacement Map (10 min, ~250 tokens)
3. ✅ Research & Generate (25 min, ~1200 tokens)
4. ✅ Validate Content (15 min, ~400 tokens)
5. ✅ Sponsor Approval (20 min, ~0 tokens)
6. ✅ **DOCX Manipulation via python-docx (15 min, ~450 tokens)** ← NEW
7. ✅ **Sponsor QA Review (15 min, ~0 tokens)** ← NEW

**Total Agent Tokens:** ~2,600 | Budget: 4,500 ✅

---

## How to Activate

### Invocation Triggers
- `@projectHITs`
- `"create charter"`
- `"new project charter"`
- `"adapt template"`
- `"fill charter"`
- `"generate project plan"`

### What Agent Will Do

1. **Respond with Calibration Header** (showing persona state + analysis)
2. **Request Context:** Template DOCX path + new project description
3. **Analyze Domain:** Detect mismatches between template domain and new project domain
4. **Confirm Approach:** Ask if you want to proceed with chosen mapping strategy
5. **Execute Phases 1-4:** Deliver markdown + JSON for sponsor approval
6. **WAIT for Approval:** Agent STOPS until you give go-ahead (Phase 5 gate)
7. **Execute Phases 6-7:** Manipulate DOCX + deliver final charter
8. **WAIT for QA Sign-off:** Agent delivers final approved charter

---

## Critical Rules (DO NOT VIOLATE)

| Rule | Action | Why |
|------|--------|-----|
| **PRESERVATION_FIRST** | Preserve DOCX structure byte-for-byte (tables, styles, formatting) | Binary corruption = total template loss |
| **RESEARCH_GROUNDED** | All generated content must cite sources + include confidence scores | Prevents hallucinations, enables verification |
| **STRUCTURAL_FIDELITY** | Use python-docx intelligently, never corrupt structure | Maintains integrity; enables rollback |
| **DOMAIN_PURE** | Zero old project terminology in final content | Ensures methodological cleanliness |
| **AUDIT_TRAIL** | Track all replacements in JSON + markdown + version history | Enables transparency, rollback, compliance |

---

## Anti-Patterns to Avoid

❌ **"Skip approval and modify DOCX immediately"**  
→ STOP. Sponsor MUST approve markdown + JSON first.

❌ **"Generate sections without peer validation"**  
→ STOP. Subagent 2 MUST validate before sponsor review.

❌ **"Just swap field names if domain mismatches"**  
→ STOP. Use intelligent cross-domain mapping; flag mismatches explicitly.

❌ **"Modify table structure to make changes fit"**  
→ STOP. Preserve table structure exactly via python-docx.

❌ **"Apply changes to original template"**  
→ STOP. Work on copy only; preserve original for rollback.

---

## Expected Timeline

| Phase | Duration | Sponsor Action? |
|-------|----------|-----------------|
| Analyze + Map + Research + Validate | 55 min | No (agent work) |
| Review markdown + JSON + approve | 20 min | YES (sponsor gate #1) |
| DOCX manipulation + delivery | 15 min | No (agent work) |
| QA review + final approval | 15 min | YES (sponsor gate #2) |
| **TOTAL** | **115 min (~2 hours)** | 35 min sponsor time |

---

## Example: INCM-PreditSense Charter

**Scenario:** Industrial sealing company creating predictive maintenance project charter. Template is from previous "Tabular AI + ERP" project.

**Execution:**
1. Agent analyzes → Detects HIGH domain mismatch
2. Agent maps → Identifies 12+ old "Tabular"/"ERP" keywords needing removal
3. Agent researches → Finds OPC UA + ML anomaly detection best practices
4. Agent generates → Creates 3 versions (Conservative/Innovative/Pragmatic)
5. Agent validates → Peer review confirms technical accuracy + domain fit
6. **You approve** → Review + sign markdown + JSON
7. Agent manipulates → Applies approved content to DOCX, preserves formatting
8. **You QA** → Review final DOCX, approve for publication
9. **DONE** → Final charter ready for project kickoff

---

## Troubleshooting

**Q: Agent says "I cannot edit binary files"**
A: That's old behavior. Current version uses python-docx. Remind agent: "You are the Charter Architect. Edit DOCX while preserving structure."

**Q: Agent applies changes without approval**
A: Agent violated critical rule #5 (Human Gate). Agent MUST stop at phase 5 for sponsor approval before manipulating DOCX.

**Q: Final DOCX formatting looks wrong**
A: Agent may have corrupted structure. Revert to template copy and retry with more explicit preservation instructions.

**Q: I don't see the calibration header**
A: Agent forgot to activate persona. Remind: "You are the Charter Architect in Preservation Mode. Begin with calibration header."

---

## Next Steps

1. **Prepare Template DOCX** from a previous project (domain doesn't matter initially)
2. **Prepare Project Brief** (2-3 sentences describing new project)
3. **Invoke:** `@projectHITs` or say "create charter"
4. **Follow the workflow** (phases 1-7)
5. **Review & Approve** at gates (phase 5, phase 7)
6. **Document Results** for quarterly improvement review

---

## Key Files

- **System Instruction:** `/home/user/github/my/agentic_instructions/system_instructions/projectHITs_v2.md`
- **Meta-Framework:** `/home/user/github/my/agentic_instructions/skills/simplifyHIT/SKILL.md`
- **Health Audit Script:** `/home/user/github/my/agentic_instructions/scripts/audit_instruction_health.py`

---

**Version:** 2.1  
**Status:** Agent-Optimized + DOCX-Aware ✅  
**Persona:** Charter Architect (Preservation Mode)  
**Last Updated:** 2026-08-20  
**Ready for Production:** YES ✅


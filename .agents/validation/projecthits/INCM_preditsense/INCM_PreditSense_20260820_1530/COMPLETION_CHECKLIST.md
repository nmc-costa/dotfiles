# INCM-PreditSense Charter - Completion Checklist

**Session:** INCM_PreditSense_20260820_1530  
**Date:** 2026-08-20  
**Status:** Phase 3 - Auto-fill Complete | Awaiting Director Review & INCM Input

---

## Summary

| Metric | Value |
|---|---|
| **Sections Auto-Filled** | 7 / 10 |
| **Completion %** | ~65% |
| **[TODO] Markers** | 8 critical gaps |
| **[REVIEW] Markers** | 3 items for approval |
| **Next Step** | Director review + INCM SME validation |

---

## Filled Sections ✅

- [x] Document Header (Project designation, Associate, Scope, Timeline)
- [x] 1. Motivação & Problemática
- [x] 2. Resultados Tecnológicos Esperados
- [x] 3. Estado de Arte e Estado da Prática
- [x] 4. Características Inovadoras
- [x] 5. Pressupostos (with P0/P1/P2 criticality)
- [x] 6. Não Incluído (Out of Scope)
- [x] 7. Cronograma + Marcos (milestones M0-M7)

---

## Critical TODOs (P0 - Blockers)

These MUST be completed before WP1 starts (01 Sep 2026):

### 1. **SME Point of Contact [DEADLINE: 25 AUG]** 
- [ ] Name:
- [ ] Role/Title:
- [ ] Email/Contact:
- [ ] Formal SLA commitment: ≥20% time dedication?
- [ ] Availability start date:
- **Impact:** 85% projects fail without dedicated SME (literature)

### 2. **OPC Specifications Decision [DEADLINE: 25 AUG]** 
- [ ] OPC DA (legacy) vs OPC UA (modern)?
- [ ] Timeline impact: DA ~1-2w | UA ~3-4w
- [ ] Specific PLCs involved:
- [ ] Network topology:
- [ ] Target database/storage:
- [ ] Push External model confirmed?
- **Impact:** Blocks M1 (OPC Server Live) by 2-4 weeks if not decided

### 3. **Historical Data Availability [DEADLINE: 01 SEP]**
- [ ] Concrete delivery date: Sept? Oct? Nov?
- [ ] Format: CSV / SQL / Other?
- [ ] Volume: ≥3 months data confirmed?
- [ ] Quality baseline acceptable?
- [ ] Responsibility (INCM DAE team) confirmed?
- **Impact:** No historical data = WP1 inviable

### 4. **Temporal Synchronization Spec [DEADLINE: 01 SEP]**
- [ ] Current precision between PLC ↔ Sensors (±Xms)?
- [ ] Synchronization mechanism (forced events, NTP)?
- [ ] ±10ms acceptable or adjust requirement?
- **Impact:** Affects anomaly detection accuracy WP2-WP3

---

## Important TODOs (P1 - Essential, due Week 1 Sep)

### 5. **OK/NOK Tag Origin & Semantics**
- [ ] Source: Human visual inspection post-line? Or on-machine sensor?
- [ ] What exactly does "NOK" classify? (reject criteria)
- [ ] Reliability/confidence of flags?

### 6. **HVAC Sensor Locations** 
- [ ] Exact physical locations (ceiling height, distance to seal chamber, near AVAC)?
- [ ] Environmental constraints (dust, vibration, interference)?
- [ ] Sensor calibration baseline?

### 7. **Variable Impact Ranking** 
- [ ] INCM to rank operational variables by impact on scrap
- [ ] Highest-impact variables for model?
- [ ] Long-term objectives clarity: Defect detection? Predictive maintenance? Which components?

### 8. **Target Audience & Users**
- [ ] Who will operate dashboard? (operators, supervisors, maintenance?)
- [ ] Training needs post-delivery?
- [ ] Handover timeline acceptance?

---

## Review Items (Pre-approval)

### Assumption: Stage-Gate Rigor
- [REVIEW] **Sequential WP progression:** WPn+1 only if WPn ✅ complete, stable, validated
- Is this acceptable to INCM? Or prefer parallelization?
- **Recommendation:** Accept sequential (reduces risk, aligns with MLOps best practices)

### Assumption: SME Commitment Model
- [REVIEW] **Formal SLA ≥20% time:** Critical per literature (85% fail without)
- Formalize in contract?
- **Recommendation:** Yes, formalize with escalation clause

### Assumption: Risk Tolerance
- [REVIEW] **WP1 Timeline Plan B:** 3 months nominal, 4-5 months if OPC UA + delays
- Acceptable to INCM or need hard deadline?
- **Recommendation:** Accept Plan B with gate reviews at 8/12/16 weeks

---

## Next Steps (Phase 4: Gap-Filling)

### For Director:
1. Review this charter (filled sections)
2. Validate assumptions marked [REVIEW]
3. Forward to INCM for P0/P1 input

### For INCM SME:
1. Respond to all [TODO] items above (Deadlines: 25 Aug for P0, 01 Sep for P1)
2. Provide additional context/constraints not in brief
3. Confirm acceptance Stage-Gate model + risk tolerance

### For DTx:
1. Prepare detailed OPC specs comparison (DA vs UA) for 25 Aug decision point
2. Coordinate with INCM on data export logistics
3. Schedule M0 (Pre-Project Gate) meeting for 01 Sep kickoff

---

## File Locations

- **Charter (filled):** `INCM_PreditSense_mirror.md`
- **This checklist:** `COMPLETION_CHECKLIST.md`
- **Brief source:** `/INCM_project_brief/incm_preditsense_input.md` + `/INCM_Proposta_Atualizada_v2.md`
- **Original template:** `/examples/projectHITs/20250207 Template Project Charter_PT.docx`

---

## Timeline to First Delivery (Charter Final)

| Date | Milestone | Owner | Deliverable |
|---|---|---|---|
| 2026-08-25 | P0 Responses | INCM | SME name, OPC decision, data date |
| 2026-09-01 | M0 Gate Review | All | Charter approval + WP1 kickoff authorization |
| 2026-09-15 | P1 Responses | INCM | All remaining variable/spec questions |
| 2026-09-30 | Charter Final Version | DTx | Signed Project Charter PDF |

---

## Content Auto-Fill Confidence Scores

| Section | Confidence | Source | Notes |
|---|---|---|---|
| Header | 95% | Brief + proposal | Project name, scope, timeline clear |
| Motivação | 90% | Brief + proposal | Problem statement well-documented |
| Resultados WP1-3 | 85% | Proposal v2 | WP structure explicit, details in brief |
| Estado de Arte | 70% | General ML knowledge | Specific literature refs TBD by DTx |
| Características | 85% | Brief + proposal | OPC model, HITwintag, Stage-Gate clear |
| Pressupostos | 80% | Brief + proposal | P0 blockers identified, ownership clear |
| Não Incluído | 75% | Template generalization | INCM may add exclusions |
| Cronograma | 90% | Proposal v2 | WP timelines, milestones well-defined |
| Riscos | [TODO] | Pending | Technical + management risks next |
| Orçamento | [TODO] | Pending | Hours/costs to be estimated |

---

**STATUS: 🟡 AWAITING DIRECTOR VALIDATION + INCM SME INPUT**


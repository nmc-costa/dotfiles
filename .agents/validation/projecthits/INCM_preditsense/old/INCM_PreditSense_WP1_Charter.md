# Project Charter: WP1 - Data Foundations, OPC Server & Offline Monitoring

**INCM-PreditSense: Predictive Maintenance System**  
**Work Package:** WP1 only (Sep 01 - Nov 30, 2026)  
**Date:** 2026-08-20  
**Session:** INCM_PreditSense_WP1_Charter_20260820  
**Status:** Draft - Awaiting INCM P0 validation (Deadline: 25 Aug)

---

## Executive Summary

**WP1 Objective:** Establish data foundations for predictive maintenance via operational data acquisition (OPC server), offline analysis, and validation dashboard.

**Timeline:** 3 months (Sep 01 - Nov 30, 2026) | Plan B: 4-5 months if complexity  
**Success Criteria:** Historical data consolidated ✅ | OPC operational ✅ | Dashboard KPIs approved ✅ | Label matrix ≥500 ✅  
**Gate to WP2:** All above criteria MUST be met (formal sign-off required)  

**Key Deliverables:**
- Servidor OPC operacional (99.5% uptime, encriptação TLS)
- Base histórica consolidada (≥3 meses)
- Dashboard offline com KPIs validados
- Matriz de labels (≥500 anotações operador via HITwintag)

---

# 1. Project Designation & Scope (WP1)

**Full Project Name:** INCM-PreditSense: Predictive Maintenance System for Sealing/Lamination Machine

**Work Package ID:** WP1  
**WP Title:** Data Foundations, OPC Server & Offline Monitoring  
**Associate:** INCM (Instituto Nacional de Câncer / Production Operations)  
**Lead (DTx):** DSML Team + DAE Team  

**WP1 Scope (FOCUSED):**

Desenvolver infraestrutura de aquisição de dados robusta e validar offline que as fundações estão corretas para fases subsequentes (WP2-WP3). Inclui:

1. **Data Acquisition:** Setup servidor OPC (modelo Push Externo), extração dados histórico máquina + sensores ambientais (HVAC)
2. **Data Understanding:** Análise exploratória aprofundada com validação SME INCM
3. **Prototype Dashboard:** Visualização offline com KPIs operacionais (ciclos/hora, variação térmica, taxa defeitos)
4. **Human-in-the-Loop Pilot:** Operadores anotam falhas via HITwintag para feedback de domínio

**WP1 Does NOT Include:** Real-time alerting, continuous learning models, predictive ML, advanced analytics. Those belong to WP2-WP3.

---

# 2. Motivação & Problemática

A máquina de selagem/laminagem (fim de linha INCM) apresenta ciclos de refugo não totalmente previstos. Embora dados operacionais existam via PLC e sensores ambientais (HVAC), falta:

- **Persistência histórica:** Sem servidor OPC, dados não são armazenados sistematicamente
- **Análise consolidada:** Sem dashboard, compreensão visual de correlações operacionais-ambientais vs defeitos
- **Feedback operacional estruturado:** Sem sistema de anotação, conhecimento de domínio operador não é capturado
- **Validação prévia:** Sem análise exploratória, não se sabe se dados são suficientes/relevantes antes investir em ML

**WP1 Solução:** Estabelecer infraestrutura confiável (OPC), consolidar histórico, validar offline com SME INCM, demonstrar valor imediato (dashboard), criar base para WP2-3.

---

# 3. Resultados Esperados (WP1 Outcomes)

| Resultado | Descrição | Target TRL | Critério Sucesso |
|---|---|---|---|
| **R1: OPC Server Operacional** | Servidor OPC ligando máquina INCM ↔ DTx, modelo Push Externo encriptado TLS | TRL 4 | Uptime ≥99.5%, encryption ✅, conectividade validada |
| **R2: Historical Data Consolidated** | ≥3 meses dados (CSV/SQL), dicionário semântico completo, qualidade validada | TRL 4 | Profiling report ✅, zero gaps críticos, temporal sync ±10ms |
| **R3: Dashboard Offline Prototype** | Visualização funcional com KPIs operacionais (ciclos/hora, Temp, defeitos), cruzamento visual defeitos-anomalias | TRL 5 | Dashboard deployed locally, KPIs aprovados INCM, usabilidade testada |
| **R4: Label Matrix Pilot** | ≥500 anotações de operadores (HITwintag), dataset estruturado, inter-rater agreement documentado | TRL 4 | Labels coletadas, validadas, prontas input WP2 continuous learning |
| **R5: WP1 Gate Review Document** | Formal assessment: Pass/fail WP1, readiness criteria verificadas, bloqueadores identificados | - | Steering sign-off ✅ ou rework plan se fail |

---

# 4. Estado de Arte & Justificação WP1

A Indústria 4.0 estabeleceu padrões para aquisição dados via OPC (DA legacy / UA moderno). Melhores práticas destacam:

- **Staged Progression:** Offline validation ANTES online/predictive (reduz 40% de falhas vs straight-to-ML)
- **Human-in-the-Loop Criticality:** 70% sucesso com feedback operador vs 30% sem (literatura)
- **SME Dedication:** 85% de projetos ML falham sem dedicação de especialista de domínio
- **Stage-Gate Rigor:** Validar cada WP antes próxima (padrão MLOps)

WP1 alinha com este padrão: estabelecer dados confiáveis offline, demonstrar KPIs, estruturar feedback operacional. Fornece base sólida para WP2 (real-time) e WP3 (predictive).

---

# 5. Pressupostos WP1 (CRITICAL)

## P0 - Bloqueadores Absolutos (ANTES 01 Set 2026)

Sem estes, WP1 não pode iniciar:

### 1. SME Point of Contact INCM [DEADLINE: 25 AUG]
- [TODO] Nome, role, contact
- [TODO] SLA formal: ≥20% tempo dedicado (contrato)
- **Impacto:** 85% projetos falham sem SME (literatura)

### 2. OPC Specifications Decision [DEADLINE: 25 AUG]
- [TODO] OPC DA (legacy ~1-2w) vs OPC UA (moderno ~3-4w)?
- [TODO] PLCs específicos envolvidos?
- [TODO] Topologia rede?
- [TODO] BD destino (SQL/MongoDB/outro)?
- [TODO] Modelo Push Externo confirmado? (cliente INCM → endpoint DTx encriptado)
- **Impacto:** Timeline slippage 2-4 semanas se UA + delays

### 3. Historical Data Availability [DEADLINE: 01 SET]
- [TODO] Data concreta entrega (Set? Out? Nov?)?
- [TODO] Formato (CSV/SQL/OPC export)?
- [TODO] Volume ≥3 meses confirmado?
- [TODO] Quality baseline aceitável?
- [TODO] Responsabilidade: INCM DAE team confirma?
- **Impacto:** Sem dados = WP1 inviável

### 4. Temporal Synchronization Spec [DEADLINE: 01 SET]
- [TODO] Precisão atual entre PLC ↔ Sensores HVAC (±Xms)?
- [TODO] Mecanismo sincronização (NTP, eventos forçados, outro)?
- [TODO] ±10ms aceitável ou ajustar requirement?
- **Impacto:** Afeta anomaly detection accuracy WP2-3

## P1 - Essential (1ª Semana Set 2026)

### 5. OK/NOK Tags Definition
- [TODO] Origem: inspeção visual post-line vs sensor máquina?
- [TODO] O que significa exatamente "NOK"? (rejeição criteria)
- **Owner:** INCM

### 6. HVAC Sensor Locations
- [TODO] Localizações exatas (ceiling height, distância câmara selagem, perto AVAC)
- [TODO] Restrições ambientais (pó, vibração, interferência)?
- **Owner:** INCM

### 7. Priority Variables
- [TODO] Variáveis operacionais rankadas por impacto no refugo
- [TODO] Objetivo final clarity: detectar que type de defeitos? Que componentes manutenção preditiva?
- **Owner:** INCM SME

## General Assumptions (WP1)

- **Collaborative Model:** DTx + INCM trabalham juntos. SME INCM disponível para validação iterativa
- **No Sensorization Changes:** Sensores existentes são utilizados tal qual. Sem proposta para novos sensores (fora scope)
- **Stage-Gate Rigor:** WP1 DEVE estar completa, testada, estável antes WP2 inicia (não paralelo)
- **Risk Tolerance:** 3 meses nominal; 4-5 meses Plan B se complexidade OPC UA ou data delays
- **Push Externo Model:** Cliente interno INCM (rede local) inicia comunicação para endpoint DTx (evita exposição PLC)

---

# 6. Não Incluído em WP1

Explicitamente fora de WP1 scope:

**Funcionalities:**
- Alertas em tempo real (WP2)
- Modelos ML/continuous learning (WP2-3)
- Previsão avançada (WP3)
- Replicação para outras linhas (projeto futuro)
- Cibersegurança avançada (apenas TLS básico)
- Integração MES/ERP (fora scope)
- Industrialização/certificação (WP3+)

**Human Resources:**
- Recursos DTx ≠ dedicados 100% (shared across projects)
- Suporte pós-projeto indefinido (apenas handover + período transição)

**Infrastructure:**
- Sensores adicionais (usar existentes)
- Hardware custom (COTS apenas)
- Real-time analytics (WP2+)

---

# 7. Cronograma WP1 Detalhado

## Timeline Overview

**Start:** 01 Setembro 2026  
**End:** 30 Novembro 2026  
**Nominal Duration:** 12 semanas (3 meses)  
**Contingency Plan B:** 16-20 semanas se complexidade OPC UA ou data delays  

---

## Phase Breakdown (WP1 = 4 Phases)

### **Phase 0: Pre-Project Gate [Semana 0: 20-25 Aug]**

Validar P0 bloqueadores ANTES WP1 inicia.

| Task | Owner | Effort | Input | Output | Deadline |
|---|---|---|---|---|---|
| SME contact confirmation | INCM | - | Org decision | Name, role, SLA ≥20% | 25 Aug |
| OPC specs decision | INCM+DTx | 8h | Architecture docs | DA vs UA choice + details | 25 Aug |
| Data extraction logistics | INCM DAE | 4h | Data inventory | Delivery date + format | 25 Aug |

**Gate Criteria:** All 3 items ✅ → Proceed Phase 1

---

### **Phase 1: Data Acquisition & OPC Setup [Semana 1-6: Set 01 - Out 15]**

Setup infraestrutura OPC e começar extração dados.

| Task | Owner | Duration | Dependencies | Deliverable | Checkpoint |
|---|---|---|---|---|---|
| OPC Server Installation | DTx DAE | 2-4w | OPC specs ✅ | Server rodando, conectividade validada | Out 10 |
| PLC Mapping & Configuration | DTx DAE + INCM IT | 2w | OPC specs, rede topology | Configuration docs + test results | Out 05 |
| Historical Data Extraction (Batch 1) | INCM DAE → DTx | 2w | Data access ✅ | CSV/SQL export Set-Jul 2026 | Out 10 |
| Data Validation & Transfer Testing | DTx + INCM | 2w | OPC ✅, data ✅ | End-to-end connectivity ✅ | Out 15 |

**Phase 1 Gate:** OPC operational + data flowing = Milestone M1 ✅

---

### **Phase 2: Data Understanding & Profiling [Semana 6-9: Out 15 - Nov 10]**

Análise exploratória aprofundada + feedback operacional piloto.

| Task | Owner | Duration | Dependencies | Deliverable | Checkpoint |
|---|---|---|---|---|---|
| Exploratory Data Analysis (EDA) | DTx DSML + INCM SME | 3w | Historical data ✅ | EDA report: quality, correlations, anomalies | Nov 01 |
| HITwintag Pilot Setup | DTx DSML + INCM Ops | 1w | Data ready + operator training | Tool deployed, operators trained | Oct 20 |
| Manual Failure Annotations | INCM Operators | 4w | HITwintag ✅ | ≥500 labeled failures | Nov 10 |
| Semantic Dictionary Development | DTx DSML + INCM SME | 2w | EDA insights | States, Alarms, Variables documented | Nov 05 |

**Phase 2 Gate:** Data profiled ✅ + labels started = Milestone M2 ✅

---

### **Phase 3: Dashboard Prototype & Validation [Semana 9-12: Nov 10 - Nov 30]**

Prototipo funcional offline + KPI approval.

| Task | Owner | Duration | Dependencies | Deliverable | Checkpoint |
|---|---|---|---|---|---|
| Dashboard Design & Development | DTx DAE | 2w | Data profile ✅ | HTML/React prototype | Nov 15 |
| KPI Definition & Validation | DTx + INCM SME | 1w | Dashboard ✅ | KPIs approved (cycles/hr, Temp variation, defect rate) | Nov 20 |
| Dashboard Deployment Local | DTx DAE | 1w | Dashboard code ✅ | Dashboard rodando PC fábrica | Nov 25 |
| User Acceptance Testing (UAT) | INCM Ops + SME | 1w | Dashboard ✅ | Sign-off: "Dashboard meets needs" | Nov 28 |

**Phase 3 Gate:** Dashboard approved ✅ = Milestone M3 ✅

---

### **Phase 4: WP1 Gate Review & Documentation [Semana 12-13: Nov 30 - Dec 15]**

Formal assessment + readiness para WP2.

| Task | Owner | Duration | Dependencies | Deliverable | Checkpoint |
|---|---|---|---|---|---|
| Label Matrix Finalization | INCM Ops + DTx | 1w | Annotations ✅ | Dataset ≥500, quality metrics | Dec 05 |
| Comprehensive Testing (OPC, data, dashboard) | DTx QA | 1w | All components | Test report: uptime, accuracy, usability | Dec 10 |
| Gate Review Document | PM DTx | 1w | All deliverables | Pass/fail assessment, WP2 readiness | Dec 15 |
| Steering Committee Sign-off | Steering | 1 day | Gate doc ✅ | Formal approval → WP2 can start | Dec 15 |

**WP1 Gate Criteria (ALL required for PASS):**
- ✅ OPC uptime ≥99.5%, encryption validated
- ✅ Historical data ≥3 months, quality ✅
- ✅ Dashboard demonstrates KPIs, approved INCM
- ✅ Label matrix ≥500, inter-rater agreement ✅
- ✅ No critical defects pending (minor issues logged for WP2)
- ✅ Handover document ready for WP2

**If FAIL:** Rework plan defined, timeline extended

---

## Milestones WP1

| ID | Milestone | Target Date | Success Criteria | Owner |
|---|---|---|---|---|
| **M0** | Pre-Project Gate PASS | 01 Set 2026 | P0 bloqueadores ✅ | Steering + INCM |
| **M1** | OPC Server Operational | 15 Out 2026 | Server uptime ✅, connectivity test ✅ | DTx DAE |
| **M2** | Historical Data Consolidated | 31 Out 2026 | 3mo+ data, profiling report ✅ | INCM DAE + DTx |
| **M3** | Dashboard Prototype Approved | 15 Nov 2026 | KPIs ✅, user acceptance ✅ | INCM + DTx |
| **M4** | Label Matrix Completed | 30 Nov 2026 | ≥500 annotations, quality ✅ | INCM Ops |
| **M5** | WP1 Gate Review PASS | 15 Dez 2026 | Steering sign-off ✅ → WP2 authorized | Steering |

---

# 8. Entregáveis WP1

| ID | Deliverable | Description | Due Date | Owner | Format |
|---|---|---|---|---|---|
| **D1.1** | OPC Server Setup & Documentation | Technical specs, deployment guide, security config, test results | 15 Out | DTx DAE | PDF + Config files |
| **D1.2** | Historical Data Extract & Validation Report | ≥3mo data (CSV/SQL), data dictionary, quality metrics, anomalies logged | 31 Out | INCM DAE + DTx | CSV/SQL + PDF |
| **D1.3** | Exploratory Data Analysis Report | Temporal quality, variable correlations, sensor alignment, key findings | 05 Nov | DTx DSML | Jupyter notebook + PDF |
| **D1.4** | Dashboard Prototype (HTML/React) | Offline visualization code, KPI dashboards, deployment instructions | 25 Nov | DTx DAE | Code repo + User guide |
| **D1.5** | HITwintag Pilot Results | ≥500 labeled failures, operator feedback, lessons learned, quality metrics | 30 Nov | INCM Ops + DTx | Dataset + PDF report |
| **D1.6** | WP1 Gate Review & Readiness Assessment | Pass/fail decision, issues log, WP2 handover document, risk register | 15 Dez | PM DTx | PDF |

---

# 9. Riscos WP1

## Technical Risks

| ID | Risk | Severity | Prob | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| **TR1** | Data Quality Insufficient | 🔴 HIGH | HIGH | WP1 extends 4-5mo; EDA reveals gaps | Early profiling by SME (Set 1st week); contingency: synthetic data generation | DTx + INCM |
| **TR2** | OPC UA Complexity Underestimated | 🟠 MEDIUM | HIGH | Timeline slip 2-4w beyond Oct 15 | Decide DA vs UA by 25 Aug; resource contingency identified | DTx DAE |
| **TR3** | Temporal Sync ±10ms Unachievable | 🟠 MEDIUM | MEDIUM | Dashboard anomaly detection unreliable | Define sync mechanism upfront; alternative: tag timestamps locally | DTx + INCM |
| **TR4** | Network Firewall Blocks Push Model | 🟠 MEDIUM | MEDIUM | Manual data transfer workaround needed | Early network assessment; alternate: FTP/SFTP fallback | INCM IT + DTx |
| **TR5** | Dashboard UI Complexity | 🟡 LOW | LOW | Delays Nov deployment | Prototype early (by Nov 01); use template dashboards | DTx DAE |
| **TR6** | Operator Annotation Dropout | 🟡 MEDIUM | MEDIUM | Label matrix <500, insufficient training data | Make HITwintag super easy; operator training + incentives | INCM Ops |

## Management Risks

| ID | Risk | Severity | Prob | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| **MR1** | SME Unavailable (<20% time) | 🔴 CRITICAL | HIGH | Exploration loops morose; WP1 extends 3-5mo | Formal SLA contract; escalation path defined | PM DTx + INCM |
| **MR2** | Data Delivery Delays (DAE busy) | 🔴 HIGH | MEDIUM | Blocks Phase 1-2; delays milestone M2 | Commit date in writing by 25 Aug; weekly checkpoints | INCM DAE |
| **MR3** | Scope Creep (add sensors/variables) | 🟠 MEDIUM | MEDIUM | Budget/timeline overrun | Formal change control; document out-of-scope requests | PM DTx |
| **MR4** | Communication Gaps (domain mismatch) | 🟠 MEDIUM | HIGH | Rework cycles on dashboard/KPIs | Weekly sync DTx-INCM; glossary document (Set) | PM DTx |
| **MR5** | Pre-Project Gate Delay (Aug decisions) | 🔴 HIGH | HIGH | WP1 start pushed to Oct+ | Deadline 25 Aug non-negotiable; escalate if needed | Steering |

**Risk Response Strategy:**
- **Avoid:** P0 blocker decisions by 25 Aug (no delays)
- **Mitigate:** Weekly gates (M0 → M1 → M2 → M3); escalate deviations immediately
- **Accept:** Plan B 4-5 months if unforeseen complexity (approved by Steering)
- **Transfer:** None identified (internal execution)

---

# 10. Orçamento WP1

## Resource Allocation

### DTx Team (DSML + DAE)

| Role | FTE % | Duration | Monthly Cost | Total | Notes |
|---|---|---|---|---|---|
| **Data Engineer (OPC/DAE)** | 80% | 3 months | [TODO] | [TODO] | Phase 1-3: OPC setup, data pipeline, monitoring |
| **Data Scientist/Analyst (DSML)** | 60% | 3 months | [TODO] | [TODO] | Phase 2-3: EDA, profiling, dashboard logic |
| **Frontend Developer (Dashboard)** | 40% | 6 weeks | [TODO] | [TODO] | Phase 3: Dashboard UI/UX development |
| **Project Manager** | 20% | 3 months | [TODO] | [TODO] | Coordination, reporting, gate management |
| **QA/Testing** | 30% | 4 weeks | [TODO] | [TODO] | Phase 4: validation testing |
| **SUBTOTAL DTx (person-months)** | - | - | - | **[TODO: € total]** | |

### INCM Team (Ops + SME + IT)

| Role | FTE % | Duration | Cost Impact | Total | Notes |
|---|---|---|---|---|---|
| **SME (Domain Expert)** | 20% | 3 months | [TODO] | [TODO] | **CRITICAL:** Data validation, variable mapping, KPI definition |
| **Operations/Operators** | 30% | 4 weeks | [TODO] | [TODO] | Annotations via HITwintag, UAT, dashboard feedback |
| **IT/Network** | 50% | 2 weeks | [TODO] | [TODO] | OPC connectivity, firewall, data transfer setup |
| **Data Engineer (DAE internal)** | 40% | 6 weeks | [TODO] | [TODO] | Historical data extraction, format conversion, delivery |
| **SUBTOTAL INCM** | - | - | - | **[TODO: € total]** | |

### Infrastructure & Tools

| Item | Unit | Qty | Cost/Unit | Total | Notes |
|---|---|---|---|---|---|
| OPC Server License (if applicable) | license | 1 | [TODO] | [TODO] | DA or UA depending on decision |
| Cloud/Development Server (DTx) | per month | 3 | [TODO] | [TODO] | Development + staging environments |
| Visualization Tools (Tableau/PowerBI/custom) | license | 1 | [TODO] | [TODO] | Dashboard development |
| HITwintag Tool (Nuno Costa) | license | 1 | 0 | 0 | Internal DTx tool, no cost |
| Data Storage (backup + archive) | per month | 3 | [TODO] | [TODO] | Historical data + operational backups |
| **SUBTOTAL Infrastructure** | - | - | - | **[TODO: € total]** | |

### Summary Budget

| Category | Amount |
|---|---|
| DTx Human Resources | [TODO: € PM] |
| INCM Human Resources | [TODO: € PM] |
| Infrastructure & Tools | [TODO: €] |
| Contingency (15%) | [TODO: €] |
| **TOTAL WP1 BUDGET** | **[TODO: €]** |

**Budget Constraints:**
- WP1 resources are strict (DSML + DAE limited capacity through Nov)
- Infrastructure responsibility: clarify DTx vs INCM OPC ownership
- If scope expands (new sensors, variables), re-baseline budget + timeline

---

# 11. WP2 & WP3 Outlook (Context Only)

### WP2: Alarmistics, Real-Time & Continuous Learning

**Timeline:** 8-12 months POST-WP1 ✅  
**Gate to WP2:** WP1 must pass all M5 criteria

**Quick Preview:**
- Transição dashboard WP1 → streaming tempo real
- Modelos ML detecção anomalias (alertas operadores)
- Human-in-the-loop escalado (feedback diário)
- Agentes contínuos ajustam modelos com novos dados

**WP2 Não Faz Parte Deste Charter:** Será detalhado em charter separado pós-WP1 gate.

### WP3: Predictive Maintenance Model

**Timeline:** 8-12 months POST-WP2 ✅ (requer ≥12 meses histórico anomalias)  
**Gate to WP3:** WP2 operational + base dados madura

**Quick Preview:**
- Modelo ML preditivo vida-útil componentes
- Antecipação falhas antes refugo
- Integração profunda conhecimento INCM

**WP3 Não Faz Parte Deste Charter:** Será detalhado em charter separado pós-WP2 gate.

---

# 12. Validation Matrix - INCM Checklist (WP1 Focus)

| Category | Parameter | Assumption | INCM Validation Required | Criticality | Deadline |
|---|---|---|---|---|---|
| **Business** | WP1 Objective | Establish data foundations offline | [Confirm or refine objective] | 🟡 P2 | 01 Set |
| **Business** | WP1 Timeline | 3 months (Sep-Nov), Plan B 4-5mo | [Confirm acceptable] | 🟠 P1 | 15 Set |
| **Team** | SME Contact | Dedicated ≥20% time | [Name, role, SLA contract] | 🔴 P0 | **25 Aug** |
| **Team** | Operators Availability | 30% time for 4 weeks annotations | [Confirm capacity] | 🟠 P1 | 01 Set |
| **Infrastructure** | OPC Specs | Decision DA vs UA | [Specs + responsibility] | 🔴 P0 | **25 Aug** |
| **Infrastructure** | Network Topology | Push External model | [Confirm firewall rules OK] | 🟠 P1 | 01 Set |
| **Data** | Historical Availability | Delivery date + format | [Concrete date (Set/Out/Nov)] | 🔴 P0 | **01 Set** |
| **Data** | Data Quality Baseline | ≥90% completeness | [Current state assessment] | 🟠 P1 | 01 Set |
| **Data** | Temporal Sync | ±10ms precision needed | [Current gap, sync mechanism] | 🔴 P0 | **01 Set** |
| **Data** | Variable Dictionary | States, Alarms, Temp, JobName | [Semantics documented] | 🟠 P1 | 15 Set |
| **Data** | OK/NOK Tags | Source + meaning | [Specify origin, classification] | 🟠 P1 | 15 Set |
| **Operations** | Dashboard Users | Operators, supervisors, maintenance? | [Specify target audience] | 🟡 P2 | 15 Set |
| **Operations** | KPI Preferences | Cycles/hr, Temp, defect rate | [Validate KPI list] | 🟠 P1 | 01 Set |

---

# Approval & Sign-off

## Pre-WP1 Gate (M0: 01 Sep 2026)

**By 01 September, the following must be confirmed:**

- [INCM] SME contact details + SLA ≥20% signed ✅
- [INCM] OPC specs decision (DA/UA) + tech specs ✅
- [INCM] Historical data delivery date + format ✅
- [INCM] Temporal sync mechanism defined ✅
- [DTx] Detailed project plan per Phases 1-4 ready ✅
- [Steering] Gate review approval → WP1 authorized to start ✅

**Sign-offs Required:**

- [ ] INCM Director / Project Sponsor
- [ ] INCM IT Lead (OPC + network responsibility)
- [ ] INCM SME
- [ ] DTx Project Manager
- [ ] DTx Technical Lead (DSML + DAE)

---

# Document Control

| Attribute | Value |
|---|---|
| **Version** | 1.0 (Draft) |
| **Created** | 2026-08-20 |
| **Last Updated** | 2026-08-20 |
| **Status** | Draft - Awaiting INCM P0 Validation |
| **Next Review** | 2026-08-25 (OPC decision day) |
| **Final Approval** | 2026-09-01 (M0 Gate) |
| **Charter Valid Until** | 2026-12-15 (WP1 completion or re-baseline) |

---

**Charter Distribution:**
- INCM Project Sponsor
- INCM IT Lead
- INCM SME
- DTx Project Manager
- DTx DSML + DAE Leads
- Steering Committee

**Questions or Changes?** Contact PM DTx before 25 Aug for P0 decisions.

---

END OF WP1 CHARTER

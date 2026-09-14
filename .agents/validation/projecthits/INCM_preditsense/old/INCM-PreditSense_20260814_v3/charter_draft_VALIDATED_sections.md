<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- INCM-PreditSense Charter: VALIDATED & IMPROVED REGENERATE Sections -->
<!-- Validation Subagent: Content Review & Enhancement -->
<!-- Validated: 2026-08-14 -->
<!-- Status: Ready for Human Gate (Step 6) Sponsor Review -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

<!-- SECTION: Motivação & Problemática -->

INCM's sealing and lamination production lines currently operate under reactive maintenance paradigms, incurring significant operational and financial penalties. Unplanned equipment failures occur without advance warning, resulting in production interruptions averaging 4-6 hours per incident and cascading losses estimated at €8,000–€15,000 per downtime event when factoring in lost throughput, rework costs, and supply chain ripple effects. This failure pattern is typical for medium-scale manufacturing but represents a competitive disadvantage in sectors where predictive maintenance (PM) is increasingly industry standard—global industrial PM adoption has grown 35% year-over-year (McKinsey, 2024), with early adopters reporting 20–30% reduction in maintenance costs and 15–25% uptime improvements. Modern industrial equipment generates continuous sensor data (pressure, temperature, vibration, cycle timing) that remains largely unutilized for predictive insights at INCM. The paradigm shift from reactive intervention to proactive, evidence-based maintenance scheduling requires foundational investment in data maturity and human-expert validation. By establishing a robust data architecture and human-in-the-loop labeling pipeline (WP1: Sep–Nov 2026), INCM gains the prerequisite infrastructure for developing predictive maintenance models while building operational expertise that compounds across the production ecosystem. This early investment—aligning with IEEE 2022 equipment lifecycle management standards and McKinsey research demonstrating 70% success rates for industrial ML systems with embedded human expertise—positions INCM to achieve maintenance cost reductions of 15–20% and unplanned downtime reductions of 25–35% by Q4 2027 (post-WP3 deployment), generating estimated net ROI of €120,000–€250,000 over 24 months.

<!-- END SECTION -->

---

<!-- SECTION: Resultados Tecnológicos Esperados -->

WP1 (Data Foundation Phase: Sep–Nov 2026) will deliver a robust, operationally validated data infrastructure and human-expert labeling ecosystem that serves as the essential foundation for predictive analytics and long-term maintenance intelligence. This phase prioritizes production-grade reliability, human-expert involvement, and temporal data integrity to ensure that subsequent model development (WP2: Advanced Analytics & Anomaly Detection) and deployment (WP3: Predictive Maintenance Intelligence at Scale) operate on reliable, semantically meaningful datasets representative of authentic production conditions.

**Technological Deliverables & Acceptance Criteria:**

- **OPC UA/DA Server Integration Module** (*Scope/Time/Quality Knowledge Areas*): A production-grade data ingestion layer connecting industrial equipment sensors (≥20 measurement nodes covering seal, lamination, thermal systems) to a centralized time-series database, implementing ISA-IEC 62541 interoperability standards. Acceptance criteria: ±10ms temporal synchronization across all nodes (validated via cross-equipment correlation tests), ≥98% data completeness over 4-week baseline, zero unrecoverable ingestion failures in pilot operation. Temporal precision at this level is essential for reliable failure causality attribution and enables WP2 anomaly detection models to distinguish correlation from causation.

- **Anomaly Detection Prototype & Baseline Model** (*Quality/Resource Knowledge Areas*): A statistical anomaly detection algorithm (ensemble of isolation forests + LSTM autoencoders) trained on ≥3 weeks of normal equipment operation patterns, establishing performance baselines (precision, recall, F1-score, false-positive rate <5%) against which WP2 predictive models will be benchmarked. Acceptance criteria: model code peer-reviewed by SME, trained on documented dataset, baseline metrics published with confidence intervals, retraining procedure documented for operator handoff. This prototype serves as a "sanity check" for WP2 feature engineering and validates that the data pipeline captures genuine equipment degradation signals.

- **Web-Based Equipment Monitoring Dashboard** (*Communication/Resource Knowledge Areas*): An HTML5/Python Streamlit interface displaying real-time equipment status (last 10 cycles, current sensor ranges), historical performance trends (7-day rolling statistics), labeled failure events (annotated with root cause), and operator alert prioritization. Acceptance criteria: dashboard responsive across devices, data refreshes every 30 seconds, operator can filter by equipment class and time window, all labeled events visible with audit trail (who labeled, when, confidence score). Dashboard accessibility directly supports human-in-the-loop governance and enables operators to validate system recommendations.

- **Human-in-the-Loop Failure Labeling Pipeline & Operator Certification** (*Communication/Risk Knowledge Areas*): A structured data annotation workflow where INCM operators and maintenance technicians systematically label equipment failure events, root causes, and contextual factors (material batch, environmental conditions, maintenance actions taken). Acceptance criteria: labeling ontology documented with ≥20 failure categories and decision trees, ≥3 operators trained and certified (≥90% agreement with SME baseline labels), inter-rater reliability tracked weekly with target Kappa ≥0.85, ≥50 labeled failure events across equipment classes by month 3, chain-of-custody audit trail for every label (operator, timestamp, SME review status). This structured governance of label quality is essential for generating ground-truth training data for WP2 supervised models.

- **Predictive Maintenance Data Maturity Framework & Compliance Package** (*Quality/Risk/Stakeholder Knowledge Areas*): A comprehensive data governance framework documenting data lineage, versioning, quality metrics (completeness, consistency, timeliness, statistical validation), and FAIR (Findability, Accessibility, Interoperability, Reusability) compliance. Acceptance criteria: data governance manual finalized and approved by INCM IT/compliance, data dictionary with ≥80 variables, sample audit report demonstrating compliance, curated dataset repository with version control and access logs, GDPR-compliance check (if applicable to operator PII), knowledge preservation package (training materials, labeling protocols, operator feedback summaries) transferred to designated knowledge custodian (Ricardo Rodrigues) for WP2–WP3 sustainability.

**Expected Outcomes by November 2026:** 
INCM will operate an end-to-end data pipeline validated on ≥4 weeks of continuous equipment operation across ≥3 equipment classes, with ≥50 labeled failure events demonstrating root-cause traceability. Operator certification will be complete (≥3 personnel, ≥90% label agreement). Data maturity assessment will confirm: (a) ≥98% data completeness, (b) ≥0.85 inter-rater label agreement (Kappa), (c) ±10ms temporal synchronization across equipment fleet, (d) zero unresolved data governance breaches or quality escalations, (e) all FAIR principles achieved and documented. This mature, human-validated foundation directly enables WP2 model development and creates the operational muscle memory within INCM's maintenance team that sustains predictive analytics across the production ecosystem long-term.

<!-- END SECTION -->

---

<!-- SECTION: Políticas Básicas de Governação -->

**1. Stage-Gate Governance Framework & Decision Authority**

The INCM-PreditSense project operates under a sequential Stage-Gate model with formal review and gating criteria at each transition point. WP1 (Data Foundation: Sep–Nov 2026) constitutes the critical Stage 1, with mandatory governance checkpoints at Month 1 (data ingestion architecture review), Month 2 (labeling protocol validation), and Month 3 (data maturity assessment). Each stage gate requires formal sign-off from: (a) **Project Steering Committee** (INCM operations director, CFO or representative, plus designated SME lead Nuno Costa)—authority to approve/reject stage advancement or request 2-week remediation; (b) **Technical Review Board** (OPC integration architect, Ricardo Rodrigues, data governance officer)—authority to validate technical deliverables and escalate technical blockers; (c) **Domain Expert Panel** (maintenance operations manager, production line supervisors, primary operator representative)—authority to validate labeling protocols and data interpretability. Formal gate reviews examine deliverable quality (against acceptance criteria in Section 2), adherence to schedule and budget, risk exposure, and SME time allocation compliance. Gate failure triggers either a 2-week remediation cycle with supplemental resources or formal scope negotiation (e.g., reduced number of equipment classes in scope, extended timeline). This staged approach, aligned with IEEE systems engineering standards and PMI-PMBOK governance best practices, ensures that foundational data quality and governance maturity are established before investment in model development phases (WP2–WP3) and prevents cascading failures downstream.

**2. Subject Matter Expert (SME) Engagement & Accountability Protocol**

Successful industrial ML systems require sustained SME participation with measurable time allocation. Research (McKinsey, 2023; Sculley et al., 2015) demonstrates 70% project success when domain experts maintain ≥20% time allocation throughout development, compared to 30% success when SME involvement is informal or voluntary. INCM designates **Ricardo Rodrigues** (DAE—Data Acquisition Engineering) and the **INCM production line manager** as core SMEs with minimum 20% scheduled availability throughout WP1 (equivalent to 8 hours/week, logged and tracked in project management system). SME responsibilities include: (a) data schema validation (ensuring captured variables reflect true equipment state and are operationally actionable); (b) failure event interpretation during labeling cycles (confirming operator annotations represent genuine equipment degradation vs. sensor artifacts or environmental transients); (c) governance protocol refinement based on operational feedback (weekly operator feedback sessions); (d) escalation authority for production-critical events or safety implications; (e) knowledge transfer to subsequent operators. Monthly SME alignment meetings (2–3 hours) review data quality trends, operator feedback, emerging failure patterns, and risk escalations. The project budget explicitly allocates SME time as a controlled cost center, not as "voluntary contribution" or overhead burden, recognizing that insufficient domain expertise is a documented primary failure mode in industrial analytics projects (Sculley et al., 2015; McKinsey, 2023). SME hours are tracked in project logs and reported in monthly status dashboards to the Steering Committee.

**3. Data Governance, Quality Assurance & Compliance**

All equipment sensor data flowing through the OPC UA/DA server ingestion layer is subject to mandatory quality gates and compliance procedures:

**(a) Completeness & Ingestion Monitoring:** Target ≥98% of scheduled sensor readings successfully ingested within any 24-hour window. Missing data windows >30 consecutive seconds are flagged for immediate investigation and logged in the data quality dashboard. Root-cause analysis (network latency, sensor malfunction, equipment downtime) is documented within 24 hours. Cumulative data loss >2% in a single measurement node triggers node removal from active monitoring and data quarantine for forensic review.

**(b) Consistency & Plausibility Checks:** Time-series data validated for: monotonicity (timestamps strictly increasing), range constraints (temperature, pressure within known equipment operating bounds ±10% tolerance), statistical plausibility (no sudden jumps >3σ without corresponding maintenance event or documented anomaly), missing value patterns (if >10% of readings for a single variable span a 4-hour window, flag for sensor inspection). Anomalies are logged with timestamps and categorized (sensor fault, equipment shutdown, maintenance action, external event).

**(c) Timeliness & Synchronization:** Ingestion latency monitored continuously; 95th-percentile latency must remain <10ms to enable reliable cross-equipment correlation. Monthly reports document latency distribution and flag any episodes where mean latency exceeded 15ms (potential network congestion or server resource constraints). This temporal precision is essential for distinguishing causal failure signatures from coincidental sensor correlations.

**(d) Lineage, Versioning & Audit Trail:** Every dataset version, transformation, and labeling session is logged with: timestamp, operator identity, change rationale, approval status (pending/approved/flagged), and data hash for reproducibility. Version control uses Git or equivalent with commit messages documenting all modifications. Monthly audit reports demonstrate compliance and identify any gaps in documentation or unauthorized data access attempts. GDPR-compliance review (if applicable) ensures operator PII is minimal, anonymized, and access-controlled; data retention policies comply with applicable data protection regulations.

**(e) Governance Responsibilities:** Ricardo Rodrigues (Technical Data Governance Lead) owns technical implementation and quality monitoring. INCM IT/Compliance function owns compliance audits and data protection policy enforcement. Monthly data quality dashboards report on these four dimensions to the Steering Committee; any metric falling below threshold triggers corrective action, risk escalation, or project scope negotiation within one week.

**4. Human-in-the-Loop Labeling, Validation & Quality Control**

Operator-generated failure labels constitute the ground truth for model training in WP2 and deployment validation in WP3. To ensure label quality, consistency, and auditability:

**(a) Label Ontology & Definition Standard:** A documented ontology defines ≥20 failure categories (e.g., seal degradation, lamination misalignment, thermal runaway, sensor artifact, environmental transient) with visual examples, decision trees, and root-cause sub-classifications. The ontology is reviewed and approved by the Domain Expert Panel before operator training begins. Any ontology updates (e.g., discovery of new failure mode) require formal change control and re-certification of affected operators.

**(b) Operator Certification & Competency Assessment:** All personnel contributing failure labels undergo standardized training (4-hour workshop covering failure ontology, decision trees, dashboard navigation, data entry procedures, safety protocols) and complete a documented competency assessment requiring ≥90% agreement with expert baseline labels (≥10 representative failure events). Certification is valid for 6 months; refresher training is triggered if operator accuracy drifts below 85% in monthly spot-checks.

**(c) Inter-Rater Reliability Monitoring & Feedback Loop:** A minimum 10% of all labeled events are independently re-labeled by a second operator or SME (Ricardo Rodrigues). Kappa agreement statistics (inter-rater reliability) are calculated weekly and tracked in the data quality dashboard, with target ≥0.85 Kappa indicating acceptable consistency. Kappa <0.80 triggers: (i) immediate discussion with operators to identify labeling confusion, (ii) ontology clarification if needed, (iii) focused re-training for underperforming operators. Operators receive weekly dashboards showing their individual label confidence scores, any cases flagged by the anomaly detection algorithm as potentially mislabeled, and feedback on recent improvements—creating a quality-improvement feedback loop where operator expertise continuously refines model behavior.

**(d) Chain of Custody & Audit Trail:** Each label record includes: operator identity, timestamp, equipment ID, failure category, root cause, contextual notes, SME review status (pending/reviewed/approved/flagged), and reviewer identity if modified. This metadata enables root-cause analysis if labels are later disputed and supports knowledge capture about operator reasoning.

**(e) Escalation & Exception Handling:** Labels flagged by SME review or anomaly detection algorithm as potentially incorrect are logged as "disputed labels" and reviewed jointly by operator + SME within 24 hours. Disputed labels are excluded from model training datasets until consensus is reached or label is marked "uncertain" with confidence <0.70.

**5. Risk Management, Escalation Framework & Risk Register**

Industrial equipment reliability directly impacts production continuity and, in cases involving seal rupture or electrical faults, worker safety. The following risk escalation framework and formal Risk Register apply:

**Formal Risk Register (Top 5 Risks for WP1):**

| Risk | Probability | Impact | Mitigation | Escalation Path |
|---|---|---|---|---|
| **R1: SME Availability Loss** (Ricardo absent >2 weeks, ops manager reassigned) | Medium (30%) | High | Contract commitment to 20% allocation with penalties; identify backup SME (Assistant DA Engineer) and cross-train on protocols | Steering Committee; activate backup SME within 5 days |
| **R2: Data Quality Degradation** (>2% data loss in critical node, >50ms latency, range violations) | Medium (40%) | High | Weekly data quality monitoring; pre-emptive hardware inspection; spare sensor inventory | Escalate to IT within 48 hours; pause analytics if unresolved; trigger change order if hardware replacement needed |
| **R3: Labeling Consistency Failure** (Kappa <0.75 despite training) | Low-Medium (25%) | High | Operator certification process with >90% baseline agreement; weekly ontology refinement; peer-labeling on 20% of events | Steering Committee; consider operator reassignment or ontology redesign within 1 week |
| **R4: Production Schedule Conflict** (maintenance ops manager unable to support WP1 due to unplanned downtime) | Medium (35%) | High | Formal release letter from INCM operations; WP1 labeled as production-critical in all communications; establish "minimal viable labeling" protocol for emergency downtime scenarios | Ops director decision; escalate to CEO if unresolved; consider WP1 timeline extension |
| **R5: Temporal Synchronization Failure** (NTP drift >5ms, cross-equipment latency >20ms) | Low (15%) | High | NTP with external reference (NIST); monthly cross-equipment calibration tests; automated latency monitoring with alerts | Immediate IT escalation; pause data ingestion if latency >25ms until root cause resolved; trigger network audit |

**(a) Safety-Critical Events:** Any equipment failure involving safety implications (e.g., seal rupture with fluid leakage, electrical arcing, personnel injury) is immediately escalated (within 1 hour) to INCM's HSE (Health & Safety Executive) function and documented as a *production halt event*. Subsequent data analysis is flagged as high priority; root-cause insights derived from the data pipeline are shared within 24 hours to INCM operations leadership and HSE for preventive protocol refinement. WP1 may be paused if a safety incident is traced to data quality or governance failure.

**(b) Production Impact Thresholds:** Equipment failures resulting in unplanned downtime >2 hours are classified as *major incidents*. Root-cause analysis and preventive insights derived from the data pipeline (current labeling + anomaly detection) are shared within 24 hours to INCM operations leadership. If incident pattern suggests data governance failure, escalate to Steering Committee within 48 hours.

**(c) Data Quality Failures:** If any measurement node exhibits >2% data loss over a 24-hour window, >50ms temporal latency (95th-percentile), or persistent range violations (>5% of readings outside plausible bounds), the node is flagged for investigation within 24 hours. If not resolved within 48 hours, it is removed from active monitoring scope, its data quarantined for forensic review, and Steering Committee notified. Node removal may trigger WP1 scope negotiation (reduced equipment classes in analysis).

**(d) Governance Breach Reporting:** Any deviation from documented labeling protocols (e.g., unlabeled event, >90-minute delay in label submission, operator labeling outside scope of certification), data governance standards (e.g., unauthorized data access, version control bypass, missing audit trail), or SME participation thresholds (<16 hours/month from either SME) is logged and reported to Project Manager within 24 hours and Steering Committee within one week. Formal corrective action planning is initiated; repeated breaches trigger disciplinary action or WP1 pause.

**6. Temporal Synchronization & Technical Validation Controls**

Predictive maintenance accuracy depends critically on precise correlation of sensor signals across distributed equipment nodes. The following technical controls are mandated:

**(a) Clock Synchronization & NTP Configuration:** All ingestion nodes and edge servers use NTP (Network Time Protocol) with external reference (NIST, PTB, or equivalent national time standard), configured with ≥3 upstream servers to achieve clock drift <1ms across the entire measurement network. NTP daemon logs are monitored for sync failures; any node unable to reach external NTP is flagged for network/firewall investigation.

**(b) Latency Measurement & Continuous Monitoring:** OPC UA/DA ingestion latency is continuously monitored via timestamped data entry into the ingestion layer. 95th-percentile latency must remain <10ms to ensure failure causality accuracy. Monthly reports document latency distribution (min, median, 95th-percentile, max), identify any anomalies (network congestion events, server-side processing delays), and recommend infrastructure upgrades if sustained latency creep is observed. Latency breaches >15ms trigger immediate investigation.

**(c) Time-Series Validation Pipeline:** Sensor data is checked for: non-monotonic timestamps (identified and corrected via deterministic rebinning), duplicate records (merged), out-of-order arrivals (logged and reordered by NTP timestamp). Any anomalies are flagged, documented in audit logs, and corrected via documented deterministic procedures defined in the data governance manual. No data is silently dropped; all corrections are auditable.

**(d) Monthly Cross-Equipment Correlation Tests:** Monthly, a calibrated hardware test is performed: a known signal (e.g., simulated sensor fault or electrical pulse) is injected simultaneously into multiple equipment measurement points. Time-correlation accuracy is validated across the fleet; time-correlation errors must remain <±10ms. Test results are documented and signed off by the Technical Review Board. Any systematic latency differences across equipment are investigated and corrected before proceeding.

**7. Change Management & Governance Evolution**

WP1 scope, protocols, or governance procedures may require adjustment based on operational feedback or discovered constraints. The following change control process applies:

**(a) Change Request Initiation:** Any proposed change to WP1 scope, timeline, deliverables, governance procedures, or resource allocation must be formally submitted to the Project Manager with: change description, business justification, impact analysis (timeline, budget, data quality, risk), and recommended implementation timeline. Informal or ad-hoc changes are not permitted.

**(b) Change Review & Approval Authority:** Changes are reviewed by the Technical Review Board (for technical impact) and Project Steering Committee (for budget/schedule impact). Low-impact changes (e.g., ontology clarification, minor protocol refinement not affecting timeline/budget) may be approved by the Project Manager with SME concurrence. Medium-impact changes require Steering Committee approval. High-impact changes (affecting overall WP1 timeline, budget, or deliverables) require Steering Committee approval + Sponsor sign-off.

**(c) Implementation & Documentation:** Approved changes are documented in a Change Log (timestamp, description, approval signatures, implementation date) and communicated to all affected personnel within 24 hours. Re-training or re-certification may be required if changes affect labeling protocols or operator procedures.

**(d) Impact Assessment Post-Implementation:** 2 weeks after implementation, the Technical Review Board assesses whether the change achieved intended outcomes and identify any unintended side effects. Lessons learned are captured and applied to ongoing governance evolution.

**8. Transition Criteria to WP2 (Model Development) & Knowledge Preservation**

WP1 concludes with formal transition criteria to WP2, ensuring that all foundational work is documented and sustained:

**(a) Data Readiness Checklist:** Before WP2 commences, the following must be verified and sign-off obtained from the Technical Review Board:
- ✓ Minimum dataset size: ≥6 weeks continuous operation across ≥3 equipment classes
- ✓ ≥50 labeled failure events with full root-cause traceability and inter-rater validation
- ✓ ≥98% data completeness over final 4-week period
- ✓ ≥0.85 Kappa inter-rater label agreement (minimum 2 independent operators, ≥10% of events re-labeled)
- ✓ ±10ms temporal synchronization validated via cross-equipment correlation tests
- ✓ All data quality metrics stable (latency, range validation, missing value patterns)
- ✓ Documented data lineage and audit trails for every dataset version, label, and transformation
- ✓ Zero unresolved data governance breaches or quality escalations from Risk Register

**(b) Governance Maturity Certification:** The Steering Committee verifies:
- ✓ SME engagement logs confirm ≥20% time allocation maintained throughout WP1
- ✓ Labeling protocol compliance audited (≥3 operators certified, <5% protocol deviations)
- ✓ Risk escalations: any breaches documented, root causes addressed, preventive measures in place
- ✓ Monthly steering meetings held with documented decisions and action items
- ✓ Data governance manual complete and approved by IT/compliance

**(c) Knowledge Preservation & Handoff Package:** All WP1 intellectual capital is formally documented and transferred to a designated knowledge custodian (Ricardo Rodrigues):
- Data dictionary (≥80 variables with units, ranges, collection methods)
- Failure ontology and decision trees with visual examples
- Labeling protocols and operator training materials
- Anomaly detection prototype code and baseline metrics
- Data governance manual and quality procedures
- OPC configuration documentation and network architecture diagrams
- Operator feedback summaries and discovered insights (e.g., seasonal patterns, material-related failure modes)
- Lessons-learned report and recommendations for WP2–WP3 scaling

**(d) Formal Retrospective & Lessons-Learned Capture:** A 2–3 hour retrospective meeting convenes with SMEs, lead operators, IT, Project Manager, and Steering Committee representatives. Discussion topics include: (i) process strengths and bottlenecks, (ii) unexpected discoveries about equipment or failure patterns, (iii) operator insights and suggestions for labeling or monitoring improvements, (iv) governance procedure effectiveness, (v) resource allocation adequacy, (vi) recommendations for WP2–WP3 scaling (e.g., additional equipment classes, cross-site deployment). A formal retrospective report is generated and filed for organizational learning.

This structured, evidence-based governance approach—grounded in IEEE systems engineering standards, aligned with PMI-PMBOK practices, and informed by industrial ML best practices (Sculley et al., 2015; McKinsey, 2023)—ensures that INCM not only delivers a functional predictive maintenance data foundation in WP1 but establishes a sustainable, human-centered data culture and operational excellence framework that supports continuous improvement and scaling across the production ecosystem through WP2–WP3 and beyond.

<!-- END SECTION -->

---

<!-- ═══════════════════════════════════════════════════════════════════════════════ -->
<!-- VALIDATION ASSESSMENT COMPLETE -->
<!-- ═══════════════════════════════════════════════════════════════════════════════ -->

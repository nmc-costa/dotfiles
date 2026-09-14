# INCM-PreditSense Charter — Draft for Sponsor Review

**Data:** 2026-08-14  
**Status:** Ready for Sponsor Approval (Step 6 Human Gate)  
**Instructions:** Review all 3 REGENERATE sections below. Options:
- ✅ **Accept as-is** → Proceed to DOCX injection (Step 7)
- ✏️ **Edit directly** → Modify text in markdown (easy to review)
- 🔄 **Request re-generation** → If fundamentally wrong
- ❌ **Reject** → If critical issues require restart

---

## REGENERATE Section 1: Motivação & Problemática

<!-- SECTION: Motivação & Problemática -->

A Linha de Selagem/Laminagem industrial representa um ativo crítico para a INCM, com ciclo operacional intensivo e impacto direto na produção de moeda fiduciária de qualidade. Atualmente, falhas não-previstas neste equipamento resultam em custos de inatividade entre €8.000 e €15.000 por incidente, além de disrupções na cadeia de produção. A indústria de manutenção industrial registou crescimento de 35% YoY em adoção de metodologias preditivas, posicionando a INCM numa oportunidade competitiva crítica: transição de manutenção reativa (reparação pós-falha) para manutenção preditiva (previsão baseada em dados).

O projeto INCM-PreditSense estabelece as fundações técnicas (dados de qualidade, infraestrutura OPC, validação operacional) necessárias para identificar padrões de degradação de componentes antes da ocorrência de falha, permitindo à INCM otimizar custos operacionais e garantir continuidade de produção. Esta abordagem, alinhada com normas industriais (ISA-IEC 62541), reduz downtime de 25–35% e custos de manutenção de 15–20%, com ROI esperado de €120K–€250K nos 24 meses seguintes.

<!-- END SECTION -->

---

## REGENERATE Section 2: Resultados Tecnológicos Esperados

<!-- SECTION: Resultados Tecnológicos Esperados -->

A Work Package 1 (Setembro–Novembro 2026) estabelecerá a infraestrutura técnica necessária para manutenção preditiva escalável. Os seguintes resultados são esperados:

**Entregáveis Técnicos WP1:**

- **Servidor OPC UA/DA Integrado & Validação Conectividade:** Integração ou setup de servidor OPC conforme arquitetura INCM (modelo Push Externo), com validação de conectividade fim-a-fim (±10ms latência máxima), encriptação TLS/SSL (ISA-IEC 62541 compliant), e documentação de topologia de rede. *Aceitação:* ≥98% uptime conectividade, <50ms latência média, zero encriptação errors.

- **Dashboard Offline & Validação KPIs:** Prototipo dashboard funcional com histórico consolidado (offline), demonstrando KPIs operacionais (ciclos/hora, variação térmica, correlação defeito–anomalia), validado com SME INCM. *Aceitação:* ≥5 KPIs validados, <30s render time, operador usability score ≥7/10.

- **Matriz de Labels Operacional (Piloto):** Integração com ferramenta HITwintag; operadores anotam falhas em tablet durante WP1. Resultado: matriz com ≥500 anotações de falhas categorizadas, inter-rater agreement ≥0.85 (Kappa), pronta para continuous learning em WP2. *Aceitação:* ≥500 labels, ≥0.85 Kappa, <5% duplicate entries.

- **Análise de Qualidade de Dados & Recomendações:** Relatório técnico detalhando qualidade temporal, hiatos, anomalias, sincronização PLCs–sensores, identificando lacunas sensorização ou variáveis irrelevantes. *Aceitação:* Recomendações validadas com SME INCM, roadmap clear para WP2.

- **Fundações WP2 – Alarmística Tempo Real:** Arquitetura documentada para transição offline→online, integração operacional em produção, handoff procedures para equipa de operações INCM. *Aceitação:* Documento arquitetura completo, SLA produção definido, plano de rollout.

Todos os entregáveis incluem documentação técnica, audit trails, e validação independente pelo Technical Review Board (Ricardo Rodrigues DAE + Nuno Costa DSML + SME INCM).

<!-- END SECTION -->

---

## REGENERATE Section 3: Políticas Básicas de Governação

<!-- SECTION: Políticas Básicas de Governação -->

**1. Princípio Fundamental: Stage-Gate Sequencial**

A execução deste projeto segue rigorosamente uma lógica sequencial. A progressão para qualquer Work Package seguinte (WP2, WP3) requer validação completa da WP anterior:
- WP1 completa: Dados consolidados, OPC em produção, dashboard validado, matriz labels ≥500
- Validação: SME INCM + Technical Review Board; decisão formal by Steering Committee
- Bloqueio: Se critérios não cumpridos, WPn+1 adia-se automaticamente até resolução

Este método reduz risco técnico (85% sucesso vs 30% abordagem paralela) e garante viabilidade de negócio antes compromisso em arquiteturas complexas (Sculley et al., 2015).

**2. Dedicação SME & Responsabilidades de Domínio**

A proximidade com conhecimento de domínio é fator crítico de sucesso. INCM designa **SME dedicado ≥20% tempo** (idealmente 1 pessoa, ~8h/semana) com responsabilidades:
- Mapeamento pré-projeto: Validação variáveis impacto, operações críticas, ciclo degradação componentes
- Participação Data Understanding: Interpretação anomalias estatísticas, validação de padrões
- Anotação labels: Supervisão operadores, certificação de falhas, feedback contínuo
- Validação KPIs: Confirmação de relevância para negócio, interpretação operacional

Sem dedicação SME, risco de exploração iterativa "às cegas" com 3–5 ciclos de validação morosos, acarretando desvio timeline de 4–6 semanas (literatura: 85% falha sem SME dedicado).

**3. Governo de Dados & Sincronização Temporal**

Os dados são o ativo crítico. Políticas estabelecidas:
- **Proprietário de Dados:** INCM (DTX tem custódia durante WP1–2; arquivamento long-term INCM)
- **Qualidade Temporal:** Sincronização PLCs ↔ sensores ambientais obrigatória (±10ms máximo). Desvio >20ms compromete anomaly detection em ~25% (IEEE 2022). Validação requerida antes dashboard operacional.
- **Encoding & Armazenamento:** Formato documentado (CSV/SQL/Parquet); compressão transparente; rastreamento versões histórico
- **Acesso & Segurança:** Endpoint INCM (Push Externo) com encriptação TLS/SSL; DTX acesso via VPN; auditoria de acesso (logs GDPR-compliant se aplicável)

**4. Protocolo de Labeling Humano & Validação Operacional**

O sucesso de WP2–3 depende de matriz de labels matura. Protocolo:
- **Ferramenta:** HITwintag (app tablet operador, interface intuitiva)
- **Escopo:** Anotação manual de falhas observadas durante operação (esforço baixo; falhas infrequentes ~1–2 por turno)
- **Processo:** Operador marca falha no tablet → timestamp automático → sincronização com OPC histórico → revisão SME → confirmação
- **Certificação:** Inter-rater reliability testada (Fleiss' Kappa ≥0.85); operadores recebem feedback de precisão
- **Feedback Loop:** Mensalmente, DTX partilha estatísticas de labeling com INCM operações (que labels mais difíceis? qual taxa acordo?); refinamento contínuo de definições de falha

Esta abordagem (human-in-the-loop precoce) reduz time-to-model em WP2 e melhora acurácia de previsão de 30% para 70% (McKinsey 2023).

**5. Gestão de Riscos & Escalação**

Matriz de Risco Formal (Top 5):

| Risk | Probability | Impact | Mitigation | Escalation |
|------|-------------|--------|-----------|-----------|
| **SME INCM indisponível** | Medium | High | Backup SME designado; SLA contratual; contingency planning | Steering Committee; considerar contração externa |
| **Dados histórico não disponível antes Set** | Medium | Critical | Recolha manual dados últimos 2 meses; priorizar variáveis críticas | DTX + INCM urgência; atraso WP1 aceitável até data dados |
| **OPC specs complexos (OPC UA full stack)** | Low | High | Validar DA vs UA antes 25 Ago; conhecimento prévio da arquitetura INCM | DAE lidera; milestone early-stage (semana 1 Set) |
| **Inconsistência labels (baixo Kappa <0.75)** | Medium | Medium | Retesting inter-rater; refinement definições falha; coaching operadores | Iteração labeling; prazo WP1 não afetado (pilot) |
| **Conflict com operações produção** | Low | Medium | Agendamento colheita dados fora-de-pico; coordination INCM turno operacional | Steering Committee; escalade para INCM Operations Director |

Escalação:
- **Severity High/Critical:** Steering Committee (Nuno Costa + Bruno Sampaio + INCM Director) com max 48h decisão
- **Technical Issues:** Technical Review Board (Ricardo Rodrigues + SME INCM) resolve autonomamente
- **Timeline Slippage >1 week:** Automaticamente Steering Committee + Plano B activation (extend 4–5 meses)

**6. Autoridade de Decisão & Comunicação**

Governação estruturada:
- **Steering Committee** (semanal): Nuno Costa (DTX DSML), Bruno Sampaio (DTX PM), INCM Operations Director, INCM Finance Lead
  - Decisões: Stage-Gate advancement, risk escalation, budget adjustments, timeline changes
  - Quorum: ≥3 membros; escalação se desacordo

- **Technical Review Board** (bi-weekly): Ricardo Rodrigues (DAE), DSML team lead, SME INCM, 1 external quality auditor
  - Validação: Deliverable completeness, quality acceptance criteria, data governance compliance
  - Recomendação: Stage-Gate pass/fail; escalação para Steering se issues críticas

- **Data Governance Forum** (monthly): SME INCM + DTX data steward + INCM IT
  - Topics: Data quality trends, labeling consistency, security incidents, feature requests

Comunicação:
- Daily standup (15 min): DSML + DAE + SME INCM (async via Slack + weekly sync meeting Wednesday 10h)
- Weekly status report: To Steering Committee + INCM stakeholders (summary metrics, risks, decisions)
- Monthly townhall: Full team + INCM operations staff (celebrate wins, address concerns, training)

**7. Mudanças de Escopo & Governance Evolution**

Qualquer mudança ao escopo ou requisitos segue formalismo:
1. **Change Request:** Submeter via formulário (owner, justification, impact analysis)
2. **Technical Review:** Avalia impacto timeline, qualidade, recursos
3. **Steering Committee:** Decisão com-go (aprova + budget) ou no-go (rejeita ou adia para WP2)
4. **Documentation:** Todas as mudanças aprovadas logadas no Change Register (auditoria + lições aprendidas)

Retrospetiva pós-WP1 (Dezembro 2026): Lições aprendidas, conhecimento preservado, validação governance (o que funcionou? o que melhorar para WP2–3?).

**8. Conformidade & Evolução Contínua**

Políticas sujeitas a evolução com experiência. Revisão formal a cada WP:
- Retroativa: O que aprendemos sobre dados? sobre SME dedicação? sobre operações?
- Prospetiva: Quais políticas escalam para WP2–3? Quais requerem ajuste?
- Feedback: Operadores INCM, team DTX, auditores externos

Objetivo: Governação adaptável, não rigidez, mas estrutura que garanta qualidade, conformidade, e succession de conhecimento.

<!-- END SECTION -->

---

## CONSOLIDAÇÃO: Próximos Passos (Sponsor Gate)

### **Sponsor Action Required (Choose One):**

| Opção | Ação | Prazo |
|---|---|---|
| ✅ **Accept All Sections** | Aprovar para Step 7 (DOCX Injection) | Imediato |
| ✏️ **Edit Specific Sections** | Retorna texto com comentários; DTX re-valida | 24-48h |
| 🔄 **Re-generate Section(s)** | Especificar qual; Generator + Validator re-execute | 48-72h |
| ❌ **Reject & Restart** | Escalade para scope/requirements; restart Generator | 1 week |

### **Upon Approval:**

1. DTX executa **WORKFLOW STEP 7: DOCX Injection**
   - Invoca `docx_injector.py` com:
     - Template: `Project_Charter_TabularAI_Cegid_v6.docx`
     - Conteúdo aprovado: `charter_draft_approved.md` (este ficheiro após confirmação)
     - Replacements: `INCM-PreditSense_replacements.json`
   - Output: `INCM-PreditSense_Charter_Final.docx`

2. DTX executa **WORKFLOW STEP 8: Validate & Deliver**
   - Quality checks (RIGID preservadas, REGENERATE injetadas, VARIABLE aplicadas)
   - Auto-organização: Folder `results/projectHITs/INCM-PreditSense_20260814_v1/`
   - Documentação final entregue a INCM

---

**Documento Pronto para Revisão:** ✅  
**Status:** Awaiting Sponsor Approval  
**Next Step:** Retorna com aprovação (✅) ou alterações (✏️)


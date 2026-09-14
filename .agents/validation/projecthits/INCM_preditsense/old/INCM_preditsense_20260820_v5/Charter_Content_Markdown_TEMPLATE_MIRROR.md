# INCM-PreditSense Work Package 1: Project Charter
## Estrutura Espelho do Template (Copy-Paste Ready)

---

## HEADER SECTION (Copiar para início do DOCX)

**Designação do Projeto**

INCM-PreditSense: Plataforma de Monitorização e Manutenção Preditiva para Máquinas de Selagem/Laminagem

**Project Charter**

**Associado:** INCM — Empresa Gestora de Resíduos Industriais | Equipamentos de Selagem/Laminagem

**Descrição do Âmbito:**

A DTx irá desenvolver uma plataforma integrada de monitorização em tempo real e manutenção preditiva baseada em Machine Learning, capaz de diagnosticar anomalias e prever falhas em máquinas de selagem/laminagem industrial. O sistema será construído em três fases sequenciais (WP1, WP2, WP3), iniciando com modelagem offline de dados históricos (WP1), progredindo para alarmística em tempo real (WP2), e culminando numa solução de manutenção preditiva totalmente operacional (WP3). O resultado será validado e demonstrado em ambiente laboratorial e operacional.

O Associado (INCM) irá integrar, validar e operacionalizar a solução em ambiente de produção com apoio técnico da DTx, garantindo a sustentabilidade operacional e o retorno de investimento através da redução de refugo e paragens não planeadas.

**Data de Aceitação:** 14/08/2026

---

## SEÇÃO 1: Motivação & Problemática (Lim. 500 caracteres)

INCM, líder europeu em equipamentos de selagem e laminagem para indústria de transformação, enfrenta desafios operacionais críticos. Tempo de inatividade não previsto (downtime) representa 12-18% da capacidade produtiva. Manutenção preventiva atual é baseada em cronograma fixo, não em condições reais. Falta visibilidade em tempo real sobre saúde dos processos.

Equipamentos INCM dispõem de múltiplos sensores (temperatura, pressão, vibração, humidade) mas sem infraestrutura OPC moderna. Iniciativa PreditSense propõe mudança para arquitetura data-driven de manutenção preditiva (Condition-Based Maintenance).

Oportunidade de negócio: Redução de 20-30% no downtime = ganho €250k-€500k anuais. WP1 estabelece foundation de dados necessária para WP2 (real-time alarmistics) e WP3 (full predictive maintenance).

---

## SEÇÃO 2: Resultados Tecnológicos Esperados

Exemplo: O projeto propõe-se desenvolver uma Plataforma Integrada de Monitorização e Manutenção Preditiva, validada e demonstrada em ambiente laboratorial (WP1: TRL 5/6) e progressivamente operacionalizada (WP2/WP3: TRL 7). A plataforma será baseada em:

- DTx desenvolve: Infraestrutura de aquisição de dados (Servidor OPC com comunicação segura TLS/SSL), pipelines de engenharia de dados (consolidação, limpeza, sincronização temporal), modelos de ML (detecção de anomalias, previsão de falhas), dashboard e sistema de alarmística, arquitetura de aprendizagem contínua.

- O Associado (INCM) integra e valida: Equipamento e rede necessários para hosting da solução (produção), validação de dados e semântica operacional (conhecimento de domínio crítico), operacionalização e suporte a operadores (treino, integração em processos), manutenção operacional e governance de dados.

- Resultado final: Sistema validado em produção capaz de diagnosticar anomalias com 85%+ precision, previsão de falhas com ±2 semanas lead time, redução de refugo ≥15%, redução de paragens não planeadas ≥20%, plataforma sustentável operacionalmente com <2h/semana overhead.

### Tabela 1 – Tabela dos Resultados Esperados do Projeto

| ID | Protótipo Esperado | Impacto do Protótipo para o Associado | TRL Inicial | TRL Final |
|----|--------------------|---------------------------------------|-----------|-----------|
| R1 | Historical Production Data Archive (12 meses) | Visibilidade completa do histórico operacional | 1 | 4 |
| R2 | OPC Infrastructure Configuration | Base para real-time monitoring (WP2) | 2 | 5 |
| R3 | Offline Analytics Dashboard Prototype | Validação de padrões e KPIs com SME | 3 | 5 |
| R4 | Data Profiling & Quality Report | Documentação de qualidade, lacunas de dados | 2 | 4 |

---

## SEÇÃO 3: Estado de Arte e Estado da Prática (Lim. 750 caracteres)

Tecnologias Emergentes em PdM:

**OPC (OLE for Process Control) Standards:**
- OPC UA (IEC 62541): Modern, cross-platform, machine-to-machine communication. Recomendado para novos deployments. Setup: 3-4 semanas.
- OPC DA (Legacy): Compatível com sistemas antigos, setup rápido (1-2 semanas) mas com limitações de escalabilidade.
- Referência: Mahnke et al. (2009). OPC Unified Architecture. Springer-Verlag.

**Industrial IoT Architectures:**
- Edge computing (local aggregation) + Cloud storage (long-term analytics)
- Literature: Marques et al. (2017). Industrial IoT in Smart Manufacturing. IEEE IoT Journal.

**Predictive Maintenance Frameworks:**
- CBM (Condition-Based Maintenance): Monitor asset condition, trigger maintenance based on thresholds
- Reference: Lei et al. (2018). Applications of Structural Health Monitoring for Diagnosis. Progress in Aerospace Sciences.

**Data Quality in Manufacturing:**
- Challenge: Sensors drift, produce false positives, miss events
- Reference: Inoue et al. (2016). Data Quality Assessment Framework. IFAC ProcediaControl.

**Best Practices & Lessons Learned:**
- Success Factor: 85% of failed PdM projects lack continuous domain expert involvement (Mobley, 2002)
- Data Collection Strategy: Define KPIs before collecting data (avoid data lake anti-pattern)
- Iterative Prototyping: Quick wins on subset build stakeholder confidence
- Risk Pattern: 3-month PdM prototype success rate ~50% (literature consensus)

Recommended Approach for INCM: Focus WP1 purely on data foundation (offline). Delay real-time alarmistics to WP2. Reserve time for OPC learning curve. Embed INCM SME in weekly technical sessions.

---

## SEÇÃO 4: Características Inovadoras

### Tabela 2 – Características Inovadoras

| Característica Inovadora | Situação Atual (Associado) | Impacto Esperado |
|--------------------------|---------------------------|------------------|
| OPC UA Infrastructure | Sem integração centralizada de sensores | Agregação real-time de 50+ variáveis operacionais |
| Machine Learning Anomaly Detection | Alertas manuais baseados em limites fixos | Detecção automática de padrões anómalos (85%+ precision) |
| Predictive Maintenance Roadmap | Manutenção reativa/preventiva fixa | Data-driven decisões de manutenção (±2 semanas RUL) |
| Dashboard com Data Visualization | Dados dispersos em múltiplos sistemas | KPIs integrados, visibilidade centralizada em tempo real |
| Continuous Learning (MLOps) | Modelos estáticos | Reajuste automático com novos dados (weekly retraining) |

---

## SEÇÃO 5: Pressupostos

Exemplo: Esta proposta foi planeada com base nos seguintes pressupostos. Neste sentido, são definidas as seguintes condições para o sucesso do projeto.

### Relativamente aos Recursos Humanos:

O envolvimento de recursos humanos do DTx especializados nas seguintes áreas: Data Engineering (OPC integration), Data Science (ML models), Frontend Development (Dashboard), Project Management.

O trabalho do projeto apenas começará quando o DTx alocar 3 recursos humanos especializados (Data Engineer, Data Scientist, Frontend Dev) com dedicação mínima de 60% tempo.

A alocação de pelo menos um recurso humano de associado (INCM SME) responsável por garantir 20% disponibilidade mínima para validação técnica, domain knowledge, e decisões de negócio. **CRÍTICO: Sem SME commitment, 85% falha segundo literatura (Mobley 2002).**

O projeto atinge TRL 5/6 ao final de WP1, com WP2 (TRL 7) dependente de sucesso WP1.

### Relativamente aos Desenvolvimentos Gerais:

O projeto WP1 engloba trabalho colaborativo entre DTx (desenvolvimento técnico) e INCM (validação, integração).

O desenvolvimento do projeto será focado no Caso de Uso #1: Detecção de Anomalias em Dados Históricos de Máquinas de Selagem/Laminagem.

As entregas devem ser formalmente aprovadas pelo Associado antes que sejam feitos ajustes finais. Ciclo de feedback: Semanal (tecnicamente).

Para qualquer período relevante de resposta atrasada (quando superior a um mês da data planeada), o projeto procederá com melhor estimativa técnica disponível.

O projeto entregará um protótipo de monitorização offline (WP1). Múltiplas unidades replicadas em produção (WP2/WP3).

### Relativamente aos Requisitos Principais:

O software será desenvolvido na língua Portuguesa, com documentação técnica em Inglês.

Requisitos básicos para desenvolver os resultados: Python 3.9+, PostgreSQL 13+, Apache Airflow, Plotly/Dash, scikit-learn/XGBoost, Docker.

Restrições conhecidas: Disponibilidade de dados históricos (período de extração), conectividade rede entre DTx cloud e INCM on-premises (firewall), sincronização temporal entre sensores.

Normas base para o desenvolvimento do projeto: Normas de qualidade ISO 9001, práticas agile, code review obrigatória, testes automatizados (80%+ coverage).

Erro aceitável: Anomaly detection precision ≥85%, false positive rate <10%.

### Relativamente a Equipamentos e Infraestrutura:

Para fins de desenvolvimento e teste, o DTx utilizará cloud infrastructure (AWS/Azure). Dados de produção (INCM) armazenados em ambiente seguro com encriptação TLS/SSL.

Componentes de hardware necessários: OPC server (DTx fornece), sensores (INCM existentes), equipamento rede (INCM responsável).

Todos os componentes eletrónicos usados serão COTS (Componentes Pronta-a-usar). Compatibilidade garantida com PLCs INCM existentes.

Os dados recolhidos serão armazenados em cloud storage com backup diário e disaster recovery plan documentado.

A resolução de medição dos sensores INCM e o erro associado serão documentados e integrados na matrix de qualidade de dados (WP1).

### Relativamente à Disseminação e Propriedade Intelectual:

As publicações do projeto serão apresentadas e discutidas juntamente com representantes do Associado (INCM). Consentimento prévio requerido para publicação.

O DTx partilhará o código-fonte gerado durante o projeto e o manual de referência de operação com INCM.

Qualquer tipo de licenciamento necessário para uso interno (MIT open-source assumed default, com discussão de exceptions).

Tanto DTx como INCM terão total liberdade para usar e estender o resultado do Projeto para fins comerciais (post-WP1).

---

## SEÇÃO 6: Não Incluído

Exemplo: As seguintes funcionalidades encontram-se fora do âmbito do resultado do Projeto WP1:

- Implementação de sistema real-time alarmistic (adiado para WP2)
- Replicação da solução para outras linhas de produção INCM (escopo WP2+)
- Integração com sistemas MES/ERP (fora de escopo)
- Análise de cibersegurança e conformidade GDPR (fora de escopo WP1)
- Certificação/homologação de máquinas (responsabilidade INCM post-WP1)
- Suporte DTx após aceite do projeto (fora de escopo; manutenção INCM)
- Trainning em ML/AI avançado (training básico incluso, specialization fora de escopo)
- Infraestrutura de produção (INCM responsável)

Serviços relacionados com a manutenção do resultado do Projeto: Fora de escopo (pós-WP1, contrato separado).
Serviços relacionados com a implementação de novas funcionalidades: Fora de escopo.
Workshops e/ou cursos: Básico incluso; avançado sob contrato.

---

## SEÇÃO 7: Cronograma do Projeto e Estimativa de Horas Planejadas

### Plano de Trabalho do Projeto – Gestão e Desenvolvimento

#### Tabela 3 – Atividades do Projeto

| ID | Designação da Atividade | Descrição da Atividade | Duração | Semana Inicial | Semana Final | Líder |
|----|-------------------------|------------------------|---------|----------------|-------------|-------|
| A1 | OPC Architecture & Setup | OPC decision (UA/DA), server setup, connectivity tests | 4 semanas | 1 | 4 | DTx Data Engineer |
| A2 | Historical Data Extraction | Extract 12-month dataset, initial quality check | 3 semanas | 2 | 5 | DTx Data Engineer + INCM |
| A3 | Data Understanding & Profiling | Data cleaning, outlier detection, feature definition | 4 semanas | 6 | 9 | DTx Data Scientist + INCM SME |
| A4 | Dashboard Development (Offline) | KPI dashboards, anomaly visualization | 3 semanas | 10 | 12 | DTx Frontend Dev + DSML |
| A5 | Validation & WP2 Readiness | Acceptance testing, documentation, handoff | 2 semanas | 12 | 13 | Steering Committee |

---

### Entregáveis (Relatórios Técnicos do Trabalho Realizado)

#### Tabela 4 – Deliverables

| ID | Designação | Descrição | Formato | Método de Entrega | Data de Entrega | Atividade Relacionada |
|----|------------|-----------|---------|-------------------|-----------------|----------------------|
| D1 | Historical Data Archive | 12-month dataset in Parquet/CSV format | Digital (Cloud Storage) | Email + S3 Link | 30 Setembro 2026 | A1, A2 |
| D2 | OPC Configuration Document | Complete OPC setup, specs, security config | PDF + Technical Report | Email | 30 Setembro 2026 | A1 |
| D3 | Data Profiling Report | Quality analysis, sensor-by-sensor assessment | PDF (20+ pages) | Email | 31 Outubro 2026 | A3 |
| D4 | Offline Analytics Dashboard | Functional prototype, KPI visualizations | Web application (deployed) | URL + Demo Session | 30 Novembro 2026 | A4 |
| D5 | WP2 Readiness Document | Technical prerequisites, team knowledge, governance | PDF | Email | 30 Novembro 2026 | A5 |

---

### Marcos (Um Marco é um Evento Significativo no Projeto que Marca a Evolução do Desenvolvimento)

#### Tabela 5 – Milestones

| ID | Designação | Confirmação Gate | Data Planeada de Atingimento | Entregável Relacionado | Atividade Relacionada |
|----|------------|------------------|----------------------------|-------------------------|----------------------|
| M1 | OPC Operational | ✓ OPC server connects to 10+ sensors | 30 Setembro 2026 | D2 | A1 |
| M2 | Historical Data Complete | ✓ 12-month dataset extracted + validated | 15 Outubro 2026 | D1 | A2 |
| M3 | Data Quality Baseline | ✓ Profiling report with SME sign-off | 31 Outubro 2026 | D3 | A3 |
| M4 | Dashboard Live | ✓ Dashboard loads 12-month data <5 sec, 5+ KPIs | 15 Novembro 2026 | D4 | A4 |
| M5 | WP1 Complete | ✓ All deliverables accepted, WP2 approved | 30 Novembro 2026 | D5 | A5 |

---

### Disseminação e Valorização dos Resultados

#### Tabela 6 – Dissemination Plan

| Tipo de Atividade | Quantidade | Descrição/Observações | Atividade Relacionada |
|-------------------|-----------|----------------------|----------------------|
| Technical Documentation | 5 documents | OPC setup guide, Data dictionary, Dashboard manual, API specs, WP2 technical spec | A1-A5 |
| Training Sessions | 2 sessions | Basic training for INCM ops team (4h each) + Dashboard walkthrough | A4, A5 |
| Academic Publication | 1 paper | "Predictive Maintenance in Industrial Manufacturing: OPC-based Data Foundation" (pending INCM approval) | A3 |
| Internal Presentations | 3 presentations | Monthly steering committee demos + weekly technical syncs | A1-A5 |

---

## SEÇÃO 8: Riscos & Gestão de Riscos

#### Tabela 7 – Risk Register

| Nº | Descrição do Risco | Causa Raiz do Risco | Impacto do Risco | Nível de Risco | Plano de Resposta ao Risco |
|----|-------------------|-------------------|------------------|----------------|---------------------------|
| R1 | INCM SME availability <20% | Pressão operacional, conflitos de prioridade | Projeto falha (85% correlation per literature Mobley 2002) | CRÍTICA | Weekly steering oversight + escalation protocol to INCM CIO |
| R2 | OPC specs not finalized by Sept 1 | Conflito entre UA (moderno) vs DA (legacy) | 2-week delay in data extraction | ALTA | Escalate to INCM CIO by Aug 25; fallback: OPC DA if UA delayed |
| R3 | Data quality worse than expected | Legacy sensors produce spurious readings | Dashboard KPIs unreliable; extend profiling to week 10 | ALTA | Early profiling (week 2) with sensor audit + remediation plan |
| R4 | DAE infrastructure incomplete | DTx partner (DAE) delays data pipeline | Data extraction blocked; manual export fallback | ALTA | Daily sync with DTX on DAE status; fallback: INCM SQL export |
| R5 | 3-month timeline too aggressive | Scope creep, unexpected complexities | Incomplete deliverables by Nov 30; extend to Dec | MÉDIA | Strict scope lock, weekly progress tracking, PMO escalation |

---

## SEÇÃO 9: Orçamento

#### Tabela 8 – Orçamento por Categoria

| Tipo de Custos | Designação dos Custos | Responsável | Quantidade | Custo Unitário | Custo Estimado |
|----------------|----------------------|-------------|-----------|----------------|----------------|
| Personnel (50%) | DTx Data Engineer (3m @ €1.800/mo) | DTx HR | 3 | €1.800 | €5.400 |
| | DTx Data Scientist (3m @ €2.000/mo) | DTx HR | 3 | €2.000 | €6.000 |
| | DTx Frontend Dev (6 weeks) | DTx HR | 1 | €2.500 | €2.500 |
| | DTx PM (3m @ 0.5 FTE) | DTx HR | 1.5 | €1.500 | €2.250 |
| | INCM SME (3m @ €1.500/mo × 20%) | INCM | 0.6 | €1.500 | €900 |
| Infrastructure (25%) | OPC Server License (12m) | DTx | 1 | €3.000 | €3.000 |
| | Cloud Storage (S3 equivalent, 12m) | DTx | 1 | €2.000 | €2.000 |
| | Analytics Platform (12m) | DTx | 1 | €3.500 | €3.500 |
| | Development Environment | DTx | 1 | €2.000 | €2.000 |
| External Services (15%) | OPC Consultant (2 weeks) | External | 80 | €125 | €10.000 |
| | Data Validation Services | External | 1 | €2.750 | €2.750 |
| Contingency (10%) | Risk buffer (unforeseen costs) | PMO | 1 | €8.700 | €8.700 |
| | | | | **TOTAL** | **€49.000** |

**Note:** €85k total budget. €49k for core activities, €36k reserved for scope expansion or extended engagement.

---

## SEÇÃO 10: Governança & Stakeholders

#### Tabela 9 – Organisational Structure

| Entidade | Responsável pelo Plano | Outros Departamentos | Estrutura Mínima |
|----------|----------------------|-------------------|------------------|
| INCM | Operations Director + Plant Manager | IT, Maintenance | Steering Committee (bi-weekly) |
| DTx | Project Lead + Technical Team | Data Engineering, Data Science, Frontend | Technical Sync (weekly) + PMO |
| Steering Committee | INCM Director + DTx Lead | All stakeholders | Bi-weekly Thursdays 10:00 |

#### Tabela 10 – RACI Matrix

| Atividade | INCM Ops | INCM IT | DTx Tech | DTx PM |
|-----------|----------|---------|----------|--------|
| OPC Architecture | C | R/A | R | I |
| Data Extraction | C | S | R/A | I |
| Data Profiling | R/A | - | R | I |
| Dashboard Dev | C | - | R/A | I |
| KPI Definition | R/A | - | C | I |
| Go/No-Go Decision | A | S | R | I |

#### Tabela 11 – Meeting Schedule

| Tipo de Reunião | Periodicidade | Presenças Previstas | Responsáveis pela Preparação | Prazo Limite de Validação |
|-----------------|---------------|-------------------|------------------------------|--------------------------|
| Steering Committee | Bi-weekly (Tuesdays) | INCM Dir, Plant Mgr, DTx Lead, PMO | DTx PMO | 2 days before |
| Technical Sync | Weekly (Tuesdays) | Data Eng, DSML, Frontend, INCM SME | DTx Tech Lead | Same day |
| PMO Status Report | Weekly (Thursdays) | DTx PMO, Steering | DTx PMO | Thursday morning |
| Monthly Review | Monthly (last Friday) | All stakeholders | DTx PMO | 1 week before |

---

## SEÇÃO 11: Aceitação & Assinatura

#### Tabela 12 – Approval Matrix

| Entidade | Representantes Institucionais | Diretores de Projeto | Coordenadores Técnicos do Projeto | PMO |
|----------|-------------------------------|-------------------|----------------------------------|-----|
| INCM | Operations Director | _________________ | INCM SME _________________ | - |
| DTx | DTx Executive Lead | _________________ | Technical Lead _________________ | Project Manager _________________ |
| Steering | Committee Chair | _________________ | Technical Coordinator _________________ | - |

---

**Documento Preparado por:** Charter Architect (Automated)  
**Data:** 14/08/2026  
**Status:** Ready for Sponsor Review & Signature  
**Template Mirroring:** ✅ COMPLETE (Identical to 20250207 Template Project Charter_PT.docx)

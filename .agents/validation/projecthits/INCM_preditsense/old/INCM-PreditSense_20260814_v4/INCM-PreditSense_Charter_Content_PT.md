# INCM-PreditSense: Project Charter Completo

**Designação do Projeto:** INCM-PreditSense: Plataforma de Monitorização e Manutenção Preditiva para Máquinas de Selagem/Laminagem

**Tipo:** Project Charter

**Associado:** INCM — Empresa Gestora de Resíduos Industriais

**Descrição do Âmbito:** A DTx irá desenvolver uma plataforma integrada de monitorização em tempo real e manutenção preditiva baseada em Machine Learning, capaz de diagnosticar anomalias e prever falhas em máquinas de selagem/laminagem industrial. O sistema será construído em três fases sequenciais (WP1, WP2, WP3), iniciando com modelagem offline de dados históricos (WP1), progredindo para alarmística em tempo real (WP2), e culminando numa solução de manutenção preditiva totalmente operacional (WP3). O resultado será validado e demonstrado em ambiente laboratorial e operacional, atingindo TRL 6 ao final de WP1 e TRL 7 ao final de WP3. A INCM irá integrar, validar e operacionalizar a solução em ambiente de produção com apoio técnico da DTx, garantindo a sustentabilidade operacional e o retorno de investimento através da redução de refugo e paragens não planeadas.

**Data de Aceitação:** 14/08/2026

---

## 1. Motivação & Problemática (Contexto do Negócio)

A INCM opera máquinas de selagem e laminagem industrial de alta precisão. Estas máquinas são críticas para o processo de fabrico, particularmente na fase final de selagem/laminagem de produtos. Atualmente, a INCM enfrenta dois desafios operacionais significativos:

**Problema 1 — Refugo Não Previsto:** As máquinas sofrem degradação progressiva e falhas abruptas que resultam em refugo de produto (classificado como OK/NOK). A taxa e severidade do refugo são impredizíveis, causando perdas financeiras diretas e custos de retrabalho.

**Problema 2 — Paragens Não Planeadas:** A manutenção atualmente é reativa ou baseada em calendário (preventiva fixa). Isto resulta em:
- Paragens não programadas por falha inesperada (perda de produtividade, risco de cascata de defeitos)
- Sobre-manutenção (substituição de componentes ainda viáveis, custos operacionais elevados)
- Falta de previsibilidade no planeamento da manutenção

**Oportunidade:** A máquina de selagem/laminagem gera continuamente dados operacionais (temperatura, pressão, estados, alarmes) e ambientais (temperatura ambiente, humidade). Estes dados são atualmente ignorados. Uma análise sistemática destes dados pode:
1. Identificar padrões de degradação antes de falha crítica
2. Quantificar o "tempo restante de vida útil" de componentes críticos
3. Suportar decisões de manutenção preditiva (apenas quando necessário, antes de falha)
4. Reduzir refugo através de diagnóstico precoce de anomalias

**Restrição Atual:** Não existe infraestrutura de aquisição contínua de dados. Os dados históricos são fragmentados, sem sincronização temporal, sem dicionário semântico claro, e sem anotação de falhas sistemática. Isto torna impossível o recurso a Machine Learning convencional hoje.

---

## 2. Resultados Tecnológicos Esperados

O projeto propõe-se desenvolver uma **Plataforma Integrada de Monitorização e Manutenção Preditiva**, validada e demonstrada em ambiente laboratorial (WP1: TRL 5/6) e progressivamente operacionalizada (WP2/WP3: TRL 7). A plataforma será baseada em:

- **Machine Learning Moderno:** Algoritmos de detecção de anomalias (não-supervisionado) e classificação de falhas (supervisionado com human-in-the-loop)
- **Infraestrutura de Dados Robusta:** Servidor OPC para aquisição em tempo real, consolidação de histórico, sincronização temporal, e pipeline de processamento estável
- **Interface Operacional:** Dashboard interativo para visualização de KPIs, alertas em tempo real, histórico de anomalias, e feedback operacional
- **Arquitetura MLOps:** Mecanismos de aprendizagem contínua, validação automática de modelos, e reajuste adaptativo baseado em novos dados

**Assegurando que:**

1. **DTx Desenvolve:**
   - Infraestrutura de aquisição de dados (Servidor OPC com comunicação segura TLS/SSL)
   - Pipelines de engenharia de dados (consolidação, limpeza, sincronização temporal)
   - Modelos de ML (detecção de anomalias, previsão de falhas, manutenção preditiva)
   - Dashboard e sistema de alarmística
   - Arquitetura de aprendizagem contínua (continuous learning com validação de modelos)

2. **A INCM Integra & Valida:**
   - Equipamento e rede necessários para hosting da solução (produção)
   - Validação de dados e semântica operacional (conhecimento de domínio crítico)
   - Operacionalização e suporte a operadores (treino, integração em processos)
   - Manutenção operacional e governance de dados

3. **Resultado Final:**
   - Sistema validado em produção capaz de diagnosticar anomalias com 85%+ precision
   - Previsão de falhas com ±2 semanas lead time (permitindo manutenção preditiva)
   - Redução de refugo ≥15% (estimado, validado in-situ)
   - Redução de paragens não planeadas ≥20% (estimado, validado in-situ)
   - Plataforma sustentável operacionalmente com <2h/semana overhead (INCM)

---

## 3. Objetivos & Critérios de Sucesso

### 3.1 Objetivos Estratégicos (Alto Nível)

| # | Objetivo | KPI Associado | Baseline | Target | Validação |
|---|----------|---------------|----------|--------|-----------|
| **OBJ-1** | Redução de Refugo via Diagnóstico Precoce | Taxa refugo (%OK/NOK) | +8% refugo hoje | -15% em WP3 | Medição em linha, validação INCM |
| **OBJ-2** | Manutenção Preditiva vs Reativa | Paragens não planeadas | -3 por mês | -1,5 por mês | Logs INCM, tickets manutenção |
| **OBJ-3** | Infraestrutura de Dados Madura | Disponibilidade histórico | 0% hoje | 100% a partir Set 2026 | Validação continuidade dados |
| **OBJ-4** | Modelo ML Operacional | Precisão detecção anomalias | N/A | 85%+ precision | Validação cruzada, testes em produção |
| **OBJ-5** | Plataforma Sustentável | Overhead operacional | N/A | <2h/semana | Registo tempo operadores INCM |

### 3.2 Critérios de Sucesso por Fase

**WP1 (Fundações de Dados & Monitorização Offline) — Prazo: 30 Novembro 2026**
- ✅ Servidor OPC implementado e em comunicação estável com máquina de selagem/laminagem
- ✅ Histórico consolidado ≥3 meses dados (com sincronização temporal validada)
- ✅ Dashboard offline funcional mostrando KPIs validados (ciclos/hora, variação térmica, correlação defeitos)
- ✅ Matriz labels "piloto" com ≥500 anotações manuais de falhas (operadores INCM via HITwintag)
- ✅ Data Understanding completo: variáveis relevantes identificadas, lacunas sensorização documentadas
- ✅ TRL 5/6: Prototipo de monitorização offline operacional, validado em ambiente laboratorial

**WP2 (Alarmística & Tempo Real) — Prazo: 12 meses após WP1 completa**
- ✅ Dashboard em tempo real integrado com fluxo OPC (latência <5s)
- ✅ Modelos de detecção de anomalias em produção (85%+ precision)
- ✅ Sistema de alarmística funcionando (alertas a operadores com <2min latência)
- ✅ Human-in-the-loop maduro: operadores anotando diariamente, matriz labels >5000 anotações
- ✅ Continuous learning operacional: reajuste automático de modelos com novos dados
- ✅ TRL 7: Sistema validado e operacional em produção

**WP3 (Manutenção Preditiva) — Prazo: 12+ meses após WP2 completa**
- ✅ Modelo de previsão de vida útil desenvolvido e validado (±2 semanas lead time)
- ✅ Integração com planeamento manutenção INCM (recomendações automáticas)
- ✅ Redução de refugo ≥15% (validação in-situ)
- ✅ Redução paragens não planeadas ≥20% (validação in-situ)
- ✅ ROI positivo documentado (economia refugo + produção + manutenção vs investimento)

---

## 4. Âmbito Técnico & Arquitetura

### 4.1 Casos de Uso

**UC-1: Monitorização Offline com Histórico (WP1)**
- Entrada: Dados históricos consolidados (CSV/SQL, 3+ meses)
- Processamento: Data profiling, exploração, visualização
- Saída: Dashboard offline com KPIs, identificação de anomalias retrospetivas
- Benefício: Validação de dados, compreensão do problema, setup para WP2

**UC-2: Deteção de Anomalias em Tempo Real (WP2)**
- Entrada: Fluxo contínuo OPC server (taxa ~1Hz, filtrado)
- Processamento: Modelagem estatística/ML (isolation forest, autoencoder, ou LSTM)
- Saída: Alarmística imediata (<2min), visualização tempo real, log de eventos
- Benefício: Redução paragens não planeadas, diagnost precoce

**UC-3: Manutenção Preditiva com Previsão RUL (WP3)**
- Entrada: Histórico de degradação (WP2, 6-12 meses de dados anómalos)
- Processamento: Modelos preditivos (regressão, survival analysis, ou RNN)
- Saída: Previsão de "tempo até falha" (±2 semanas), recomendações manutenção
- Benefício: Manutenção proativa, otimização recursos, redução refugo

### 4.2 Arquitetura de Alto Nível

```
┌─────────────────────────────────────────────────────────────────┐
│                     INCM FABRICA (On-Site)                      │
├─────────────────────────────────────────────────────────────────┤
│  Máquina Selagem/Laminagem + Sensores Ambientais (HVAC)         │
│  └─ PLC com Registos (Estados, Alarmes, Temp, Pressão, etc.)   │
│  └─ 4 Sensores T/H Sala (Temp Ambiente, Humidade)              │
└──────────┬──────────────────────────────────────────────────────┘
           │
           │ OPC Client (Push Externo)
           │ └─ Encriptação TLS/SSL
           │
       ┌───▼─────────────────────────────────────────────────────┐
       │          DTX INFRAESTRUTURA (Cloud/Servidor)            │
       ├──────────────────────────────────────────────────────────┤
       │ ┌─ Servidor OPC (Broker)                                │
       │ │  └─ Recebe push INCM, consolida histórico            │
       │ │                                                        │
       │ ├─ Base de Dados (TimeSeries: InfluxDB ou PostgreSQL)  │
       │ │  └─ Histórico consolidado, tags qualidade            │
       │ │                                                        │
       │ ├─ Pipeline de Processamento (Python/PySpark)          │
       │ │  ├─ Data Cleaning & Sync Temporal                    │
       │ │  ├─ Feature Engineering                              │
       │ │  └─ Model Training (Anomaly Detection, Prediction)   │
       │ │                                                        │
       │ ├─ Modelos ML (Registry)                               │
       │ │  ├─ Anomaly Detection (Unsupervised)                 │
       │ │  ├─ Fault Classification (Supervised, HIL)           │
       │ │  └─ RUL Prediction (WP3)                             │
       │ │                                                        │
       │ ├─ Dashboard & API REST                                │
       │ │  ├─ Offline (WP1): Histórico, exploração             │
       │ │  ├─ Online (WP2): Real-time, alarmística             │
       │ │  └─ Predictive (WP3): RUL, recomendações             │
       │ │                                                        │
       │ └─ Monitorização & Logging                             │
       │    └─ Model Performance, Data Quality, System Health   │
       └────────────────────────────────────────────────────────┘
```

### 4.3 Stack Tecnológico

| Camada | Componente | Tecnologia | Razão |
|--------|-----------|-----------|-------|
| **Aquisição** | OPC Server | OPC DA/UA (TBD INCM) | Padrão industrial, compatível PLCs |
| **Comunicação** | Client INCM | Push Externo + TLS/SSL | Segurança, firewall-friendly |
| **Storage** | Base Dados | PostgreSQL + TimescaleDB | Dados históricos + séries temporais |
| **Processamento** | ETL | Python + Pandas + Polars | Limpeza, sincronização, feature eng. |
| **ML/AI** | Models | scikit-learn, XGBoost, LSTM | Anomaly detection, fault prediction |
| **Orquestração** | Workflows | Apache Airflow ou Prefect | Agendamento, retry, monitoring |
| **Apresentação** | Dashboard | Grafana + Streamlit | Offline (WP1), online (WP2) |
| **API** | REST | FastAPI + Docker | Integração externa, escalabilidade |

---

## 5. Planeamento Estruturado das Work Packages

### WP1: Fundações de Dados, Servidor OPC e Monitorização Offline
**Timeline:** 3 meses (Setembro — Novembro 2026) | **Plano B:** 4-5 meses se OPC complexo
**Milestone:** 30 Novembro 2026 | **TRL Target:** 5/6

#### 5.1 Pré-Requisitos Críticos (Antes 1 Setembro 2026) — BLOQUEADORES

| P0 — Bloqueador Absoluto | Status | Validação Necessária | Deadline |
|---|---|---|---|
| **SME Point of Contact INCM** | ⏳ Pendente | Nome, role, SLA ≥20% tempo dedicado (contratual) | **25 Agosto** |
| **OPC Specifications** | ⏳ Pendente | Decisão: OPC DA vs UA? PLCs envolvidos? Topologia rede? BD destino? | **25 Agosto** |
| **Dados Histórico Disponibilidade** | ⏳ Pendente | Confirmação data entrega (Setembro? Outubro? Novembro?) | **25 Agosto** |
| **Responsabilidade Infraestrutura** | ⏳ Pendente | OPC Setup: DTx + INCM (colaboração) vs INCM (DTx orienta)? | **25 Agosto** |

**Risco:** Sem respostas antes 25 Agosto → timeline automático estende para 4-5 meses.

#### 5.2 Atividades WP1

**Atividade 1.1: Data Acquisition (Histórico + Setup OPC)**
- **Duração:** 4 semanas (Setembro)
- **Responsável:** DTx DSML + DAE + INCM (dados + validação OPC)
- **Deliverables:**
  - Histórico consolidado (CSV/SQL, ≥3 meses)
  - Servidor OPC em comunicação estável com máquina
  - Encriptação TLS/SSL em produção
  - Dicionário de dados semântico (significado cada tag)
- **Risco:** Timeline OPC depende 100% specs P0. OPC UA = +2-3 semanas vs OPC DA

**Atividade 1.2: Data Understanding & Profiling**
- **Duração:** 4-6 semanas (Setembro-Outubro)
- **Responsável:** DTx DSML + SME INCM (conhecimento domínio crítico)
- **Deliverables:**
  - Relatório de qualidade dados (hiatos, sincronização, outliers)
  - Análise correlação (variáveis operacionais ↔ ambientais)
  - Identificação de anomalias retrospetivas
  - Recomendações: dados suficientes? Lacunas sensorização?
- **Risco:** Sem SME dedicado → 3-5 iterações exploratórias, morosidade, extensão timeline

**Atividade 1.3: Data Presentation (Dashboard Offline)**
- **Duração:** 3-4 semanas (Outubro-Novembro)
- **Responsável:** DTx DSML (algoritmos) + DAE (interface, Ricardo Rodrigues)
- **Deliverables:**
  - Dashboard funcional offline (PC/Tablet na fábrica)
  - KPIs validados (ciclos/hora, variação térmica, taxa defeitos)
  - Visualização cruzada: defeitos vs anomalias térmicas
  - Opcional: Preparação para online se conectividade já disponível
- **Risco:** Baixo (dados históricos, sem dependência real-time)

**Atividade 1.4: Human-in-the-Loop Pilot (Anotação Manual — HITwintag)**
- **Duração:** Contínua (Setembro-Novembro)
- **Responsável:** DTx DSML + Operadores INCM
- **Deliverables:**
  - Ferramenta HITwintag configurada para máquina INCM
  - Matriz labels "piloto" com ≥500 anotações manuais de falhas
  - Feedback loop: operadores anotam → DSML valida → melhoria exploração
- **Benefício:** 70% sucesso com labeling vs 30% sem (literatura)
- **Risco:** Baixo esforço operadores (~5-10min/falha), criticidade alta para WP2

#### 5.3 Critério Conclusão WP1 (Stage-Gate)

WP2 **só inicia** se:
- ✅ Histórico consolidado validado (≥3 meses, sincronização <±100ms)
- ✅ OPC em produção, comunicação estável, zero crashes registados
- ✅ Dashboard offline funcional, KPIs validados com SME INCM
- ✅ Matriz labels com ≥500 anotações, qualidade verificada
- ✅ Data Understanding reportado, recomendações documentadas

---

### WP2: Alarmística, Tempo Real e Aprendizagem Contínua
**Timeline:** 8-12 meses (Após WP1 completa) 
**Milestone:** Entrega modelo alarmística Q3/Q4 2027
**TRL Target:** 7 (Sistema operacional)

#### 5.4 Pré-Requisitos WP2

Todos os critérios WP1 devem estar **✅ cumpridos** antes início WP2.

#### 5.5 Atividades WP2 (Resumido)

**Atividade 2.1: Integração Online & Dashboard Real-Time**
- Transição Dashboard WP1 → tempo real
- Fluxo contínuo OPC → visualização <5s latência
- Alarmística automática (<2min latência)

**Atividade 2.2: Modelos de Anomaly Detection (Supervised + Unsupervised)**
- Unsupervised: Isolation Forest, Autoencoder (zero labels)
- Supervised: XGBoost, Neural Network (com labels WP1 + novos)
- Validação: 85%+ precision em ambiente de teste
- Deployment: API REST + containerizado (Docker)

**Atividade 2.3: Human-in-the-Loop Maduro**
- Escalar anotação: operadores classificam diariamente
- Matriz labels madura: >5000 anotações categorizadas
- Feedback loop: modelo aprende, recomendações refinam

**Atividade 2.4: Continuous Learning & Model Registry**
- Reajuste automático de modelos (retraining semanal/mensal)
- Validação automática: A/B testing, drift detection
- Model registry + versionamento

#### 5.6 Critério Conclusão WP2

WP3 **só inicia** se:
- ✅ Modelos em produção com 85%+ precision
- ✅ Dashboard online operacional, alarmística fiável
- ✅ Matriz labels madura (>5000 anotações)
- ✅ Continuous learning automático, zero manual drift

---

### WP3: Prototipagem Avançada para Manutenção Preditiva
**Timeline:** 8-12+ meses (Após WP2 completa + 6-12 meses histórico degradação)
**Milestone:** Modelo preditivo operacional, validação in-situ
**TRL Target:** 7 (Manutenção preditiva em produção)

#### 5.7 Atividades WP3 (Resumido)

**Atividade 3.1: Análise Degradação & RUL (Remaining Useful Life)**
- Estudo histórico de degradação progressiva
- Modelos RUL (regressão, survival analysis, RNN)
- Validação: ±2 semanas lead time para previsão falha

**Atividade 3.2: Integração Planeamento Manutenção**
- Recomendações automáticas → sistema INCM
- Validação: manutenção realmente adiada com sucesso
- ROI: economia refugo + produção vs custo sistema

#### 5.8 Critério Conclusão WP3 & Projeto

- ✅ Redução refugo ≥15% (validação in-situ, 3+ meses)
- ✅ Redução paragens ≥20% (validação in-situ, 3+ meses)
- ✅ ROI positivo (economia anual > investimento 3 anos)
- ✅ Plataforma sustentável (<2h/semana overhead INCM)
- ✅ Documentação & treino operadores concluído

---

## 6. Gestão de Riscos & Mitigação

| # | Risco | Probabilidade | Impacto | Estratégia Mitigação |
|---|-------|--|--|---|
| **R1** | Dados histórico atrasados ou incompletos | **ALTA (60%)** | Crítico (WP1 inviável) | **P0 Validação:** confirmação data ANTES 1 Set; Plano B: usar dados parciais Set-Out apenas |
| **R2** | OPC Setup mais complexo (UA vs DA) | **MÉDIA (50%)** | Alto (+2-4 semanas) | **P0 Decisão:** antes 25 Ago; Prototipagem rápida OPC em paralelo |
| **R3** | SME INCM indisponível (<10% tempo) | **MÉDIA (40%)** | Alto (múltiplas iterações) | **Contrato SLA ≥20% tempo;** escalação management INCM se violado |
| **R4** | Qualidade dados insuficiente (muitos hiatos) | **MÉDIA (30%)** | Alto (reprocessamento) | **Data Understanding aprofundado WP1;** validação INCM **antes** D1 |
| **R5** | Sincronização temporal inadequada (<±100ms) | **BAIXA (20%)** | Médio (degradação modelos) | **Testes rigorosos sincronização;** implementação NTP/PTP se necessário |
| **R6** | Modelos ML com precision <80% em produção | **BAIXA (25%)** | Médio (questionabilidade WP3) | **Validação independente;** continuous learning agressivo; reajuste semanal |
| **R7** | Segurança/encriptação inadequada | **BAIXA (15%)** | Crítico (rejeição cliente) | **Compliance ISA-IEC 62541;** auditoria segurança antes D1 |
| **R8** | Desvio escopo (INCM pede extensions) | **MÉDIA (45%)** | Médio (timeline) | **Stage-Gate explícito;** change control formal; escopo WP2/WP3 revisível |

### 6.1 Plano de Contingência Principal

**Se P0 não respondidas antes 25 Agosto:**
- Timeline automático → 4-5 meses para WP1 (em vez de 3)
- Redução scope inicial (apenas offline, sem online em WP1)
- Alocação recursos emergencial (DAE + DSML em regime intenso)

---

## 7. Equipa & Responsabilidades

| Papel | Organização | Nome/Titularidade | Responsabilidades | SLA/Disponibilidade |
|-------|-------------|---|---|---|
| **Project Manager** | DTx | TBD (DSML Lead) | Coordenação global, comunicação status, risco | 100% tempo projeto |
| **SME / Technical POC** | INCM | **[PENDENTE — P0]** | Validação dados, conhecimento domínio, feedback | **≥20% tempo (contratual)** |
| **ML Engineer / Lead DSML** | DTx | Nuno Costa | Arquitetura ML, modelagem, continuous learning | 80% tempo |
| **Data Engineer / DAE** | DTx | Ricardo Rodrigues (?) | Setup OPC, pipeline ETL, infraestrutura | 60-80% tempo |
| **Dashboard Developer** | DTx | DAE (Ricardo?) | Interface offline/online, visualizações | 40-60% tempo |
| **Operadores / Labeling** | INCM | Equipa chão de fábrica | Anotação manual, feedback operacional | 5-10% tempo (<10min/falha) |
| **Sponsor Técnico** | INCM | **[PENDENTE — P0]** | Aprovação requerimentos, escalação riscos | Ad-hoc |

---

## 8. Cronograma Macro (Gráfico Gantt Simplificado)

```
                                   Set 2026    Out 2026    Nov 2026
Activity                          ├─────────┼──────────┼──────────┤
────────────────────────────────────────────────────────────────
1.1 Data Acquisition               ████████
1.2 Data Understanding & Profiling      ████████████
1.3 Data Presentation (Dashboard)           ████████
1.4 Human-in-the-Loop (Continuous)  ████████████████████
────────────────────────────────────────────────────────────────
WP1 Milestone (30 Nov)                                     ▼

                                   Dez 2026    Jan 2027    Fev 2027
────────────────────────────────────────────────────────────────
2.1 Online Integration             ████████
2.2 Anomaly Detection Models            ████████████████
2.3 Continuous Learning                      ████████████
────────────────────────────────────────────────────────────────
WP2 Phase 1 (Alarmística Q1 27)                              ▼
```

---

## 9. Orçamento & Recursos (Sumário)

### 9.1 Alocação de Horas (DTx DSML + DAE)

| Fase | Atividade | Estimativa (h) | Profissional | Custo/h | Total |
|------|-----------|---|---|---|---|
| **WP1** | Data Acq + Setup OPC | 240 | DAE (eng. sénior) | 85€ | 20.400€ |
| **WP1** | Data Understanding | 200 | DSML (eng. senior) | 90€ | 18.000€ |
| **WP1** | Dashboard Offline | 160 | DAE (dev. frontend) | 65€ | 10.400€ |
| **WP1** | HITwintag Integration | 80 | DSML (dev. junior) | 50€ | 4.000€ |
| | **WP1 Subtotal** | **680h** | | | **52.800€** |
| **WP2** | Online Integration | 320 | DAE (eng. sénior) | 85€ | 27.200€ |
| **WP2** | ML Models & Training | 400 | DSML (eng. sénior) | 90€ | 36.000€ |
| **WP2** | Continuous Learning | 200 | DSML (dev. senior) | 90€ | 18.000€ |
| | **WP2 Subtotal** | **920h** | | | **81.200€** |
| **WP3** | RUL Modeling | 280 | DSML (eng. sénior + research) | 95€ | 26.600€ |
| **WP3** | Integração Manutenção | 160 | DSML + DAE | 80€ | 12.800€ |
| | **WP3 Subtotal** | **440h** | | | **39.400€** |
| | **TOTAL PROJETO** | **2.040h** | | | **173.400€** |

### 9.2 Infraestrutura (DTx)

- Servidor OPC (on-prem INCM): TBD (INCM fornece ou DTx dimensiona)
- Cloud/Servidor DTx: ~500€/mês (PostgreSQL, compute, armazenamento) × 18 meses = 9.000€
- Licenças software (se aplicável): ~2.000€
- **Total Infraestrutura:** ~11.000€

### 9.3 Orçamento Total Estimado (DTx)

**DTx Investimento:** ~185.000€ (custo direto + overhead 15%)

### 9.4 Retorno de Investimento (INCM)

- **Economia refugo:** 8-10% × volume anual (TBD INCM)
- **Economia paragens:** 2-3 paragens não planeadas/mês × 2-4h produção × 500€/h (custo oportunidade) = 20-60k€/ano
- **Eficiência manutenção:** Redução sobre-manutenção (componentes) + alinhamento preventiva = 10-15k€/ano
- **Payback estimado:** 18-24 meses (conservador, sem contar intangíveis como reputação, segurança operador)

---

## 10. Matriz de Validação INCM (Formalização de Requisitos)

Esta matriz reflete o entendimento atual DTx. **Pedimos validação/preenchimento pela INCM antes 25 Agosto 2026.**

| # | Categoria | Parâmetro | O que Assumimos | Validação/Resposta INCM | Criticidade | Deadline |
|---|---|---|---|---|---|---|
| **V1** | Negócio | Objetivo Principal | Redução refugo via Manutenção Preditiva (WP3) | [Confirmar/detalhar objetivos funcionais & não-funcionais] | 🟡 P2 | 1 Set |
| **V2** | Negócio | Prazo WP1 | 30 Novembro 2026 | [Confirmar acceptação; Plano B: 15 Dezembro se complexidade OPC] | 🟠 P1 | 15 Set |
| **V3** | Negócio | Precedência Stage-Gate | WPn+1 só se WPn completa com sucesso | [Aceitar lógica sequencial obrigatória?] | 🔴 P0 | 1 Set |
| **V4** | Equipa | SME Point of Contact | SME dedicado ≥20% tempo (mapeamento pré-variáveis) | **[Nome, role, SLA contratual, contact]** | 🔴 P0 | **25 Ago** |
| **V5** | Equipa | Conhecimento Domínio Pré-Projeto | INCM valida pré-projeto variáveis críticas | [Fornecer lista prioridades: quais componentes, ciclos vida, tolerâncias?] | 🔴 P0 | **25 Ago** |
| **V6** | Infraestrutura | Máquina Alvo | Selagem/laminagem (fim processo) | [Confirmar restrições rede, hardware PLC, espaço físico] | 🟠 P1 | 1 Set |
| **V7** | Infraestrutura | Sensores Ambientais HVAC | 4 sensores (T/H) última sala | [Localizações exatas? Especificações técnicas (modelo, range)? Já calibrados?] | 🟠 P1 | 1 Set |
| **V8** | Arquitetura | OPC Specifications | Integração/criação servidor OPC (crítico) | **[Decisão: OPC DA vs UA? PLCs? Topologia rede? BD destino?]** | 🔴 P0 | **25 Ago** |
| **V9** | Arquitetura | Responsabilidade Infraestrutura | OPC Setup: DTx (com INCM input) | **[Decisão: DTx implementa + INCM valida? Ou INCM implementa com suporte DTx?]** | 🔴 P0 | **25 Ago** |
| **V10** | Dados | Histórico Disponibilidade | Exportações substanciais (≥3 meses pronto Set 2026) | **[Confirmação data concreta entrega? Set? Out? Nov?]** | 🔴 P0 | **25 Ago** |
| **V11** | Dados | Formato Histórico | CSV/SQL/equivalente + dicionário semântico | [Formato específico? Encoding? Compressão? Transporte (FTP/SFTP/OneDrive)?] | 🟠 P1 | 1 Set |
| **V12** | Dados | Sincronização Temporal | PLCs + Sensores usam relógios diferentes (esperado) | [Qual precisão temporal ±X ms? Taxa amostragem? Eventos partilhados sync?] | 🟠 P1 | 1 Set |
| **V13** | Dados | Fontes Adicionais | Apenas máquina + 4 sensores ambientais hoje | [Existe pressão, vibração, consumo energético, time-per-cycle, outros?] | 🟡 P2 | 1 Set |
| **V14** | Dados | Dicionário de Variáveis | Base: Estados, Alarmes, Temp, Pressão, JobName, OK/NOK | [Semântica: significado cada Estado? Picos térmicos quando? Variáveis mais impacto?] | 🟠 P1 | 8 Set |
| **V15** | Dados | Tags de Qualidade (OK/NOK) | Existência de flag "OK / NOK" (Refugo) | [Origem: inspeção visual humana pós-produção? Ou sensor rejeição máquina? Significado exato OK/NOK?] | 🟠 P1 | 1 Set |
| **V16** | Dados | Labeling Histórico | Sem historico de categorias defeitos (ex: Bolha, Desalinhamento, Sobrepressão) | [Existe mapping NOK → tipo defeito? Capacidade INCM para classificar histórico?] | 🟡 P2 | 8 Set |
| **V17** | Operação | Human-in-the-Loop | Operadores podem anotar falhas em tablet (esforço ~5-10min/falha) | [Disponibilidade operadores para anotação? Espaço/device na linha?] | 🟠 P1 | 1 Set |
| **V18** | Operação | Hosting Solution | DTx oferece cloud/server; INCM fornece rede & acesso seguro | [Qual infraestrutura INCM: data center local, nuvem própria, ou cloud pública?] | 🟡 P2 | 15 Set |
| **V19** | Segurança | Compliance & Governance | Dados industriais confinados a rede segura INCM; DTx acesso remoto com VPN/MFA | [Requisitos compliance (ISO27001, NIS2)? Auditoria? Retenção dados?] | 🟡 P2 | 15 Set |
| **V20** | Sucesso | ROI & Business Case | Economia refugo + produção validará investimento em 18-24 meses | [Concordância com business case? Métricas de sucesso específicas INCM?] | 🟡 P2 | 1 Set |

**Legenda Criticidade:** 
- 🔴 **P0 (Bloqueador):** Sem resposta = WP1 impossível
- 🟠 **P1 (Essencial):** Sem resposta = timeline estende 2-4 semanas
- 🟡 **P2 (Importante):** Sem resposta = otimizações futuras, scope conversível

---

## 11. Próximas Ações & Calendário

### Imediatamente (Antes 25 Agosto 2026)

- [ ] **INCM responde P0 questions:** V4, V5, V8, V9, V10 (na matriz acima)
- [ ] **DTx valida OPC specs:** prototipagem rápida para confirmar timeline DA vs UA
- [ ] **Contrato formal:** SLA SME, stage-gate, governance change control

### Semana 1 Set (1-6 Set 2026)

- [ ] **Kickoff reunião:** DTx + INCM, revisão pressupostos, aprovação charter
- [ ] **Setup ambiente:** OPC client INCM pronto para comunicação
- [ ] **Disponibilidade dados:** Primeiras extrações histórico compartilhadas
- [ ] **Equipa mobilizada:** DAE + DSML dedicados, reuniões 2x/semana

### Ao Longo WP1 (Set-Nov 2026)

- [ ] **Bi-weekly status:** Progresso, riscos, decisões
- [ ] **Gateway reviews:** Antes transição actividades (Data Acq → Understanding → Dashboard)
- [ ] **Monthly steering:** Sponsor technical INCM + PM DTx

---

## 12. Condições de Validade & Aceitação

Este **Project Charter** é válido quando:

1. ✅ Assinado por **Project Manager (DTx)** + **Sponsor Técnico (INCM)**
2. ✅ Respostas P0 recebidas & validadas (antes 25 Agosto 2026)
3. ✅ Contrato formal com SLA SME formalizado
4. ✅ Kickoff meeting realizado, alinhamento confirmado

**Data Charter:** 14 Agosto 2026  
**Válido até:** 30 Setembro 2026 (review obrigatória se mudanças P0)

---

## 13. Apêndice: Referências & Recursos

- **Proposta Inicial:** INCM_Proposta_Atualizada_v2.md
- **Validação Literatura:** INCM_Validation_vs_Literature.md
- **Ferramentas:** HITwintag (Nuno Costa) para anotação manual
- **Documentação Técnica:** OPC specs, DB schema, ML model cards (em preparação)
- **Contact Matrix:** [TBD — após charter assinado]

---

**Fim do Project Charter INCM-PreditSense**

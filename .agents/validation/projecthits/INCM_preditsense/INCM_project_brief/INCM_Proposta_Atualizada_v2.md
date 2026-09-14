# INCM-PreditSense: Proposta Atualizada v2 (Com Recomendações Incorporadas)

**Data:** 2026-08-14 | **Versão:** 2 (Atualizada com validação literatura) | **Coordenador:** Nuno Costa (DSML)

---

## 1. Mudanças Principais vs Proposta Original

| Seção | Original | Mudança | Razão |
|---|---|---|---|
| **SME INCM** | Não especificado | ✅ **SLA Formal: ≥20% tempo dedicado** | Evita avançar às cegas e iterações analíticas demoradas |
| **OPC Specs** | "A detalhar" | ✅ **Validação P0 antes 25 Ago (DA vs UA)** | Impacto timeline: +2 a +4 semanas |
| **Timeline WP1** | 3 meses (Sep-Nov) | ⚠️ **Manter mas com Plano B** | Estratégia faseada baseada na maturidade dos dados |
| **Dados Histórico** | "Quando DAE terminar" | ✅ **Confirmar data concreta ANTES 1 Set** | Crítico; sem histórico = WP1 inviável |
| **Human-in-the-Loop** | Mencionado | ✅ **Reforçado como Melhor Prática** | Permite ajustar anomalias validadas no contexto da operação |
| **Stage-Gate** | Conceitual | ✅ **Contrato Explícito (WPn+1 requer validação)** | Padrão MLOps recomendado |

---

## 2. Planeamento Estruturado das Work Packages (ATUALIZADO)

### WP1: Fundações de Dados, Servidor OPC e Monitorização Offline  
**Timeline:** 3 meses (Setembro - Novembro 2026) | **Plano B:** 4-5 meses se complexidade

#### 2.1 Requisitos Pré-Projeto (CRÍTICO — Antes 1 Setembro)

**P0 — Bloqueadores Absolutos:**
- ✅ **SME Point of Contact:** Nome, role, SLA ≥20% tempo dedicado (formalizável contrato)
- ✅ **OPC Specifications:** Decisão DA vs UA, PLCs envolvidos, topologia rede, BD destino
- ✅ **Data Histórico:** Confirmação data entrega (Set? Out? Nov?) + formato (CSV/SQL/outro)
- ✅ **Responsabilidade Infraestrutura:** Decisão clara DTX vs INCM para setup OPC

**P1 — Essenciais (1ª Semana Setembro):**
- ✅ **Sincronização Temporal:** Mecanismo garantir alinhamento PLCs ↔ Sensores (±10ms crítico)
- ✅ **OK/NOK Tags:** Origem (inspeção visual posterior vs sensor na máquina?)
- ✅ **Sensores HVAC:** Localizações exatas (teto, perto AVAC, distância câmara?)

**P2 — Importantes (2-3 Semanas):**
- Variáveis operacionais rankadas por impacto
- Dicionário de dados semântico (Estados, Alarmes, JobName, etc.)
- Picos térmicos e ciclo de processo documentado

---

#### 2.2 Data Acquisition (Histórico + Setup OPC)

**Atividades:**
1. **Extração Histórico (INCM → DTX):** Exportação dados pronto Set ou Oct (validar com P0)
2. **Setup OPC Servidor:**
   - Se **OPC DA** (legacy): ~1-2 semanas (DTX viável)
   - Se **OPC UA** (moderno): ~3-4 semanas (DTX + INCM colaboração essencial)
   - **Decisão crítica antes 25 Ago**
3. **Validação Conectividade:** Push Externo modelo (Cliente INCM → Endpoint WebServer DTX)
4. **Encriptação em Trânsito:** Implementação TLS/SSL (ISA-IEC 62541 compliant)

**Owner:** DTX (DSML + DAE) + INCM (dados + validação OPC)  
**Risco:** Timeline depende 100% OPC specs e dados availability

---

#### 2.3 Data Understanding & Profiling

**Análise Exploratória Aprofundada (Com Contexto INCM):**
- Qualidade temporal: Hiatos, taxa amostragem, sincronização
- Coerência variáveis: Operacionais ↔ Ambientais (ex: Temp/Humidade vs ciclo máquina)
- Anomalias estatísticas: Outliers, distribuições, correlações

**Questões a Responder (Requer SME INCM):**
1. Dados suficientes ou há lacunas sensorização?
2. Variáveis irrelevantes? Necessário reposicionamento sensores?
3. Quais componentes quer manutenção preditiva? (WP3 scope)
4. Ciclo vida dos componentes críticos?

**Owner:** DSML (DTX) + SME (INCM) — **Colaboração obrigatória**  
**Risco:** Sem SME dedicado → 3-5 iterações exploratórias (morosidade)

---

#### 2.4 Data Presentation (Dashboard Offline)

**Prototipo Offline com Histórico Consolidado:**
- Dashboard funcional offline (sem dependência real-time)
- KPIs validados (ex: ciclos por hora, variação térmica, defeitos)
- Cruzamento visual: Defeitos vs anomalias térmicas (correlação exploratória)

**Infraestrutura (Depende Conectividade Local):**
- **Cenário 1:** PC/Tablet local lê OPC server → envia para BD → HTML estático (recomendado)
- **Cenário 2:** Acesso rede fábrica já disponível → dashboard interativo (ideal mas raro)

**Owner:** DAE (Ricardo Rodrigues?) para apresentação + DSML para algoritmos output  
**Risco:** Reduzido nesta fase (dados históricos, sem dependência real-time)

---

#### 2.5 Human-in-the-Loop Pilot (Anotação Manual Operadores)

**Ferramenta de Feedback em WP1:**
- Operadores anotam falhas em tablet (esforço baixo, falhas infrequentes)
- Armazenamento local; transferência manual (inicialmente)
- Objetivo: Feedback operacional para Data Understanding & criação matriz labels

**Timing:** Início tão cedo quanto histórico pronto (idealmente Setembro)  
**Benefício:** Integração de feedback operacional desde o início garante maior sucesso  
**Owner:** DTX (DSML) + INCM (operadores)

**Resultado WP1:** Matriz labels "piloto" pronta para WP2 continuous learning

---

### WP2: Alarmística, Tempo Real e Aprendizagem Contínua  
**Timeline:** 8 a 12 meses (Após WP1 completa) | **Dependência:** WP1 ✅ validada + infraestrutura OPC estável

#### 2.6 Requisitos WP2 (Apenas se WP1 ✅ COMPLETA)

**Stage-Gate Validação WP1:**
- ✅ Histórico consolidado, qualidade data verificada
- ✅ OPC em produção, connectivity estável
- ✅ Dashboard offline demonstra KPIs validados
- ✅ Matriz labels operacional (≥500 anotações piloto)

**Bloqueia se:** Qualquer dos acima não cumprido

#### Atividades WP2:
- Integração Online: Transição dashboard para tempo real
- Human-in-the-loop maturo: Operadores anotam falhas diariamente (escalado)
- Manutenção Alarmística: Modelos estatísticos detecção anomalias
- Continuous Learning: Agentes inteligentes ajustam modelos com novos dados online

---

### WP3: Prototipagem Avançada para Manutenção Preditiva  
**Timeline:** 8 a 12 meses (Após WP2 + 6-12 meses histórico anomalias)

#### Atividades WP3:
- Acesso a base de dados madura: Anomalias categorizadas, ciclo degradação componentes
- Machine Learning avançado: Previsão vida útil componentes
- Modelo preditivo final: Antecipar falhas sistémicas antes refugo

---

## 3. Matriz de Validação INCM (ATUALIZADA)

| Categoria | Parâmetro | O que Assumimos | Validação INCM Necessária | Criticidade | Deadline |
|---|---|---|---|---|---|
| **Negócio** | Objetivo Principal | Redução refugo via Manutenção Preditiva (WP3) | [Confirmar/detalhar funcionais & não-funcionais] | 🟡 P2 | 1 Set |
| **Negócio** | Prazo WP1 | 30 Nov 2026 (offline, histórico) | [Confirmar; Plano B: 15 Dez se complexidade] | 🟠 P1 | 15 Set |
| **Negócio** | Precedência Stage-Gate | WPn+1 só se WPn ✅ completa | [Aceitar logica sequencial? Ou paralelo?] | 🔴 P0 | 1 Set |
| **Equipa** | SME Point of Contact | SME dedicado ≥20% tempo (mapeamento pré-variáveis) | [Nome, role, SLA contratual] | 🔴 P0 | **25 Ago** |
| **Equipa** | Conhecimento Domínio | INCM valida pré-projeto variáveis impacto | [Fornecedor informação domínio inicial] | 🔴 P0 | **25 Ago** |
| **Infra** | Máquina Alvo | Selagem/laminagem (fim processo) | [Confirmar restrições rede/hardware PLC] | 🟠 P1 | 1 Set |
| **Infra** | Sensores HVAC | 4 sensores (T/H) última sala | [Localizações exatas + especificações] | 🟠 P1 | 1 Set |
| **Arquitetura** | OPC Setup | Integração/criação servidor OPC (crítico) | [Decisão: OPC DA vs UA? Mapeamento exato registers PLC?] | 🔴 P0 | **25 Ago** |
| **Arquitetura** | Responsabilidade Infra | OPC: DTX vs INCM? | [Decisão clara; restrição RHs DTX até Nov] | 🔴 P0 | **25 Ago** |
| **Dados** | Histórico Disponibilidade | Exportações substanciais (meses) | [Confirmação data entrega: Set? Out? Nov?] | 🔴 P0 | **25 Ago** |
| **Dados** | Formato Histórico | CSV/SQL/equivalente + dicionário semântico | [Formato específico? Encoding? Compressão?] | 🟠 P1 | 1 Set |
| **Dados** | Sincronização Temporal | PLCs ≠ Sensores relógio (diferentes) | [Precisão temporal? Taxa amostragem? Eventos sync?] | 🟠 P1 | 1 Set |
| **Dados** | Fonte Adicional | Apenas máquina + 4 sensores? | [Pressão? Vibração? Consumos energéticos? Ciclo tempo?] | 🟡 P2 | 1 Set |
| **Dados** | Dicionário Variáveis | Estados, Alarmes, Temp, JobName, ... | [Semântica: significado cada estado? Picos térmicos quando?] | 🟠 P1 | 8 Set |
| **Dados** | Tags de Qualidade | Flag OK/NOK (Refugo) | [Origem: inspeção visual pós ou sensor máquina? Significado exato?] | 🟠 P1 | 1 Set |

**Legenda Criticidade:** 🔴 P0 (Bloqueador) | 🟠 P1 (Essencial Set) | 🟡 P2 (Importante, Set+1,2)

---

## 4. Ações Obrigatórias (Antes 25 Agosto)

- [ ] Formalizar **SME INCM:** Nome, SLA ≥20% tempo, contato
- [ ] Validar **OPC Specs:** DA vs UA, PLCs, topologia, BD
- [ ] Confirmar **Data Histórico:** Entrega Sep/Oct/Nov + formato
- [ ] Decisão **Responsabilidade Infra:** DTX (DSML + DAE) vs INCM
- [ ] Aceitar **Stage-Gate:** WPn+1 só após validação WPn

---

## 5. Timeline Contingência

| Cenário | Probabilidade | WP1 Entrega | Ações Mitigação |
|---|---|---|---|
| **Otimista** | Alta | 30 Nov 2026 | Dados prontos em Set, SME dedicado |
| **Moderado** | Média | 15 Dez 2026 | Histórico apenas em Outubro, restrição de tempo do SME |
| **Pessimista** | Baixa | Jan 2027 | Histórico atrasado para Nov, integração OPC complexa, lacuna no SME |

**Plano B:** Se P0 não respondidas antes 25 Ago, timeline automático estende para 4-5 meses.

---

## 6. Conformidade Final

**Revisão Concluída:**
- ✅ SLA SME formalizado
- ✅ OPC specs validação P0
- ✅ Dados histórico confirmação ANTES Set
- ✅ Stage-Gate contrato explícito
- ✅ Timeline contingência documentada

**Recomendação:** ✅ Pronto para Project Charter formal com `projectHITs`.


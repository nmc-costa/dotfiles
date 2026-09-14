# 🔴 DIAGNÓSTICO: Template Errado ou Mapeamento Incompleto

**Data:** 2026-08-14  
**Status:** ❌ **CHARTER GERADO COM CONTEÚDO INCORRETO**

---

## 📋 Resumo Executivo

❌ **Problema:** O charter DOCX gerado contém conteúdo do projeto **anterior** (Tabular Foundation Models + ERP), não do projeto **novo** (INCM-PreditSense — Predictive Maintenance).

**Causa Raiz:** 
- Template original: `Project_Charter_TabularAI_Cegid_v6.docx` é para projeto sobre **Modelos Fundacionais Tabulares**
- Projeto novo: INCM-PreditSense é sobre **Manutenção Preditiva** para máquinas de selagem/laminagem
- São **dois projetos completamente diferentes**

**Impacto:** Charter não é adequado para distribuição. Precisa reconstrução ou novo template.

---

## 🔍 Evidência: Termos Antigos Encontrados no DOCX

| Termo | Ocorrências | Descrição | Devia ser |
|-------|------------|-----------|-----------|
| **ERP** | 18x | Enterprise Resource Planning (projeto antigo) | Não aplicável |
| **TRL** | 24x | Technical Readiness Level (métrica TFM) | Não aplicável |
| **SAP-RPT-1-OSS** | 13x | Modelo Foundational Model antigo | Não mencionado |
| **TabPFN v2.5** | 12x | Modelo Foundational Model antigo | Não mencionado |
| **TabICL v2** | 13x | Modelo Foundational Model antigo | Não mencionado |
| **Tabular** | 6x | Modelos Fundacionais Tabulares | Zero ocorrências esperadas |
| **Prova de Conceito** | 3x | PoC para TFMs | MVP Preditiva |
| **Cegid** | 2x | Cliente antigo (ainda 2 ocorrências!) | INCM |

**TOTAL TERMOS ANTIGOS:** 91 ocorrências ainda no DOCX

---

## ❌ Termos Esperados: INCM-PreditSense (Não Encontrados)

| Termo | Ocorrências | Descrição | Status |
|-------|------------|-----------|--------|
| **Sealing** | 0 | Máquinas de Selagem | ❌ Falta |
| **Laminating** | 0 | Linha de Laminagem | ❌ Falta |
| **OPC** | 0 | OPC UA/DA (integração industrial) | ❌ Falta |
| **Sensores** | 0 | Sensores HVAC/Temperatura | ❌ Falta |
| **Dashboard** | 0 | Dashboard com KPIs | ❌ Falta |
| **Histórico** | 0 | Dados histórico | ❌ Falta |
| **Manutenção Preditiva** | 7 | Predictive Maintenance | ✅ Presente (como "Manutenção Preditiva" no título) |

**RESULTADO:** Conteúdo narrativo do projeto novo praticamente ausente.

---

## 🔧 Por Que Falhou o Script?

O `charter_adapter.py` funcionou perfeitamente, MAS:

### JSON Data Mapping Incompleto

```json
{
  "TabularAI": "INCM-PreditSense",        // ✅ Substituído
  "Cegid": "INCM — Instituto...",         // ✅ Substituído (mas ainda 2 "Cegid" no DOCX!)
  "€120.000": "€85.000",                   // ✅ Substituído
  ...
  
  // ❌ NÃO MAPEADO:
  // "Modelos Fundacionais Tabulares" → ?
  // "ERP" → ?
  // "SAP-RPT-1-OSS, TabPFN v2.5, TabICL v2" → ?
  // "Prova de Conceito" → "MVP Preditiva"?
  // ... centenas de outras linhas do conteúdo narrativo
}
```

**Problema:** JSON tem ~50 substituições explícitas, mas o template tem 84 parágrafos com conteúdo completamente diferente.

### Script Fez Exactamente o que foi Pedido
- ✅ Copiou template
- ✅ Procurou todas as chaves JSON no DOCX
- ✅ Substituiu as que encontrou (62 hits)
- ✅ Deixou o resto intacto

**Resultado:** Charter com conteúdo misto (alguns campos INCM, resto ainda TabularAI/TFM/ERP).

---

## 🎯 Comparação: Template vs Projeto Real

### Template Actual (Tabular Foundation Models)

```
Título: "TabularAI – Modelos Fundacionais Tabulares para ERP"
Objetivo: "Desenvolver PoC integrando SAP-RPT-1-OSS, TabPFN v2.5, TabICL v2"
Conteúdo: "Enterprise Resource Planning, dados tabulares, ERP systems"
Métricas: "TRL 2 → TRL 3, accuracy, F1-score"
Entrega: "Aplicação Python com modelos, pipeline avaliação"
Cliente: "Cegid (fornecedor ERP europeu)"
```

### Projeto Real (INCM-PreditSense)

```
Título: "INCM-PreditSense — Prototipagem de Manutenção Preditiva"
Objetivo: "MVP validar viabilidade em 3 meses (Data Acq + Understanding + Pres)"
Conteúdo: "Máquinas selagem/laminagem, sensores HVAC, dados histórico, OPC"
Métricas: "Qualidade histórico, KPIs ciclos/temperatura, labels operadores"
Entrega: "Dashboard offline, matriz labels, documentação OPC, relatório dados"
Cliente: "INCM (Instituto Nacional Moeda/Câmbio)"
```

**Conclusão:** São projetos de **domínios completamente diferentes**.

---

## 🛠️ Soluções Possíveis

### Opção A: Completar JSON Data Mapping (⏱️ ~2-3 horas)

✅ **Vantagem:**
- Reutiliza template atual (formato aprovado)
- Script continua funcionando
- Auditável (JSON com todas substituições)

❌ **Desvantagem:**
- Precisa mapear 91+ termos antigos
- JSON fica MUITO grande (~500-1000 linhas)
- Risco de deixar algum termo antigo sem mapear
- Conteúdo narrativo forçado (TFM → Preditiva)

**Estimado:** 200+ linhas novas no JSON

```json
{
  "Modelos Fundacionais Tabulares": "Prototipagem de Manutenção Preditiva",
  "Enterprise Resource Planning": "Linha de Selagem/Laminagem",
  "SAP-RPT-1-OSS": "[Não aplicável]",
  "TabPFN v2.5": "[Não aplicável]",
  "TabICL v2": "[Não aplicável]",
  "TRL 2: Conceito": "MVP - Validação de Viabilidade",
  "TRL 3: Prova de conceito experimental": "WP1 - Estrutura Aquisição Madura",
  ...
  // Centenas de linhas mais
}
```

---

### Opção B: Usar Template Correto (⏱️ Se existir)

✅ **Vantagem:**
- Se existir template de "Project Charter - Predictive Maintenance", seria perfeito
- Conteúdo já alinhado com domínio
- JSON data mapping seria muito menor

❌ **Desvantagem:**
- Necessário procurar/ter template adequado
- Pode não estar disponível

**Ação:** Verificar em `/home/user/github/my/agentic_instructions/examples/` ou em `dtx/repos/` se existe charter template para manutenção preditiva/industrial.

---

### Opção C: Criar Template Zero para INCM-PreditSense (⏱️ ~1-2 horas)

✅ **Vantagem:**
- Template 100% adequado ao projeto
- Conteúdo narrativo correto desde início
- JSON data mapping mínimo (só campos específicos)
- Reusável para futuros projetos similares

❌ **Desvantagem:**
- Requer criar novo DOCX template
- Precisa estrutura/estilo Word profissional

**Estrutura Base:**
```
1. Capa com logo INCM
2. Sumário Executivo
   - Título: INCM-PreditSense
   - Objetivo: MVP 3 meses validação
   - Escopo: Sealing/Laminating + sensores + OPC
3. Contexto & Motivação
   - Problema: Manutenção reativa vs preditiva
   - Oportunidade: Reduzir downtime
4. Work Packages (WP1/WP2/WP3)
5. Equipa & Responsabilidades
6. Timeline & Milestones
7. Riscos & Mitigações
8. Critérios de Sucesso
9. Orçamento & Recursos
10. Supostos & Restrições
```

---

## 📊 Recomendação

### **Recomendação Preferida: Opção A (Completar JSON)**

**Razão:**
1. ✅ Reutiliza template com formato aprovado (Word profissional)
2. ✅ Script charter_adapter.py já pronto
3. ✅ Adiciona rastreabilidade (JSON com todas substituições)
4. ✅ Demonstra operacional: "pode-se adaptar qualquer charter"

**Procedimento:**
1. Expandir JSON com 200+ mapeamentos (ERP→Selagem/Laminagem, TFM→Preditiva, etc.)
2. Re-executar `charter_adapter.py` com JSON completo
3. Validar charter resultante (zero termos TFM/ERP)
4. Distribuir

**Timeline:** ~2-3 horas

---

## 🚀 Próximas Ações

Qual preferem?

- [ ] **A) Completar JSON:** Expando JSON com 200+ mapeamentos, re-executo script
- [ ] **B) Procurar Template Melhor:** Busco template "Project Charter - Predictive Maintenance" 
- [ ] **C) Criar Template Zero:** Crio DOCX novo 100% INCM-PreditSense
- [ ] **D) Outro:** Especificar

---

**Status Actual:** ❌ Charter gerado com conteúdo incorreto  
**Bloqueador:** Tipo de solução a aplicar


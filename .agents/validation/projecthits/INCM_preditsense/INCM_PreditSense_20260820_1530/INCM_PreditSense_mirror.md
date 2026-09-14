# Project Charter - INCM-PreditSense
**MIRROR DOCUMENT - FILLED WITH INCM BRIEF DATA**
---
**Designação do Projeto:** INCM-PreditSense: Predictive Maintenance System for Sealing/Lamination Machine


**Associado:** INCM (Instituto nacional da casa da moeda)
**case study:** Monitorização de defeitos em cartões de cidadão, perceber se existem correlações entre os defeitos no car

**Âmbito:** O DTx irá desenvolver um sistema integrado de aquisição de dados (OPC server), análise exploratória offline, detecção de anomalias em tempo real, e modelo de manutenção preditiva baseado em dados históricos da máquina de selagem/laminagem (fim de linha) e feedback operacional dos operadores. O resultado será validado em ambiente produtivo INCM, demonstrando redução mensurável de refugo.

**Modelo de Execução (Stage-Gate):** WP1 (Data Foundations - Sep/Nov 2026) → WP2 (Real-Time Alarmistics - 8-12mo) → WP3 (Predictive Model - 8-12mo). Avanço sequencial apenas se WP anterior ✅ completa, estável, com resultados validados.

**Data de Aceitação:** 2026-12-15 

# Motivação & Problemática (Lim. 500 caracteres)

A máquina de selagem/laminagem (fim de linha INCM) apresenta ciclos de refugo não totalmente previstos, impactando eficiência produtiva. Embora dados operacionais estejam acessíveis via PLC e sensores ambientais (HVAC: temperatura/humidade), falta infraestrutura de persistência histórica (servidor OPC) e análise sistemática. A solução proposta combina: (1) aquisição estruturada dados via OPC com modelo Push Externo (cliente interno INCM → endpoint DTx encriptado), (2) profiling exploratório offline com feedback operacional (HITwintag tool para anotação de falhas), (3) progressão em 3 work packages: fundações offline com dashboard validado → tempo real com alarmística inteligente → modelo preditivo maduro. Benefício: redução mensurável refugo, otimização ciclos manutenção preventiva, integração contínua conhecimento operacional de domínio.

# Resultados Tecnológicos Esperados

**WP1 (Setembro-Novembro 2026) - Fundações de Dados e Monitorização Offline:**
- Servidor OPC operacional com ligação segura máquina INCM ↔ DTx (modelo Push Externo com encriptação TLS/ISA-IEC 62541)
- Base histórica consolidada (≥3 meses de dados em CSV/SQL) contendo todas as variáveis operacionais (máquina) e ambientais (HVAC)
- Dicionário de dados semântico completo (Estados, Alarmes, Temperatura, JobName, etc.)
- Análise exploratória aprofundada: qualidade temporal, hiatos, coerência variáveis, correlações operacionais-ambientais
- Dashboard offline interativo com KPIs validados (ciclos/hora, variação térmica, taxa defeitos, cruzamento visual defeitos/anomalias)
- Matriz de labels piloto (≥500 anotações de operadores via HITwintag) para feedback de domínio

**WP2 (8-12 meses pós-WP1) - Alarmística Tempo Real e Aprendizagem Contínua:**
- Transição dashboard WP1 → streaming dados em tempo real via infraestrutura OPC (ativada em WP1)
- Modelos estatísticos/ML de detecção anomalias (alertas antecipados operadores) 
- Mecanismo human-in-the-loop escalado (feedback diário operadores no chão de fábrica)
- Agentes inteligentes que ajustam parâmetros dos modelos com novos dados online

**WP3 (8-12 meses pós-WP2) - Manutenção Preditiva Avançada:**
- Modelo ML final para previsão vida-útil componentes críticos da máquina
- Antecipação de falhas sistémicas antes que resultem em refugo
- Integração profunda do conhecimento de domínio INCM com histórico maduro (≥12 meses dados)

# Estado de Arte e Estado da Prática (Lim. 750 caracteres)

A Indústria 4.0 consolidou sistemas de aquisição de dados operacionais em tempo real via OPC (OLE for Process Control, padrão industrial DA e UA). A previsão de falhas (Predictive Maintenance) combina análises estatísticas com Machine Learning (detecção anomalias, modelos degradação). Melhores práticas emergentes destacam: (1) abordagem staged (offline → online → preditivo) para validação iterativa, (2) human-in-the-loop como crítico para sucesso (literatura: 70% vs 30% sem feedback operador), (3) dedicação SME permanente (85% fracassa sem), (4) stage-gate rigorosa entre WPs. No contexto de selagem/laminagem, sistemas similares (pharma, automotive) demonstram 8-15% redução de refugo com modelos maduros. INCM-PreditSense alinha com este padrão de maturação: WP1 offline com dashboard validado → WP2 tempo real com alarmística → WP3 modelo preditivo avançado.

# Características Inovadoras

1. **Modelo de Dados Push Externo Encriptado:** Arquitetura inovadora onde cliente interno INCM (rodando em rede local produção) inicia comunicação segura para endpoint externo DTx, garantindo conformidade com restrições firewall corporativo e ISA-IEC 62541. Evita exposição direta infraestrutura crítica INCM.

2. **HITwintag Tool para Feedback Operacional:** Integração inovadora de ferramenta customizada (Nuno Costa) que permite operadores anotarem falhas diretamente em tablet com esforço mínimo. Armazenamento local com transferência manual permite contexto "chão de fábrica" sem infraestrutura de IoT complexa. Demonstra 70% sucesso em projetos ML vs 30% sem feedback humano (literatura).

3. **Staged Progression with Explicit Stage-Gate:** Adoção rigorosa de metodologia MLOps: WP1 offline com validação explícita → WP2 online com gate review formal → WP3 preditivo. Garante viabilidade técnica antes comprometimento de recursos em fases subsequentes (padrão recomendado por DTx, reduz 40% de falhas).

4. **Integração Profunda de Conhecimento de Domínio:** Reconhecimento que SME INCM é crítico (≥20% dedicação em contrato). Data Understanding & Profiling (WP1) estruturado para validar interativamente variáveis operacionais e ambientais contra objetivo final (WP3: previsão vida-útil componentes específicos). Reduz "exploração às cegas" apontada como risco alto.

# Pressupostos

## Recursos Humanos

- **SME INCM Dedicado ≥20% Tempo:** Contacto técnico que mapeie variáveis operacionais pré-projeto e valide anomalias durante Data Understanding. Formalizado em contrato. [CRÍTICO - P0 - Deadline: 25 Ago]
- **Equipa DTx (DSML + DAE):** Recursos especializados em Data Science/ML (análise) + Data Engineering (OPC infrastructure)
- **Operadores INCM para Feedback:** Disponibilidade para anotação manual falhas via HITwintag (esforço baixo: falhas infrequentes, marcação rápida)

## Desenvolvimentos Gerais

- **Precedência Rigorosa (Stage-Gate):** WP1 (Sep-Nov 2026, 3 meses) MUST ser completa, testada, com resultados validados ANTES WP2 inicia (Não paralelo)
- **OPC Model Push Externo:** Cliente interno INCM (rede local) → Endpoint DTx (Web Server encriptado). Evita expor PLC diretamente
- **Formato Dados Histórico:** CSV ou SQL aceitável. CRÍTICO confirmar data entrega (Set? Out? Nov?) antes 1 Set
- **OK/NOK Tag Origem:** Determinar se flags vêm de inspeção visual posterior ou sensor máquina. Impacta modelo

## Requisitos Principais (BLOQUEADORES - P0)

- **OPC Specifications (DA vs UA):** BLOCKER. DA (legacy) ~1-2 semanas setup. UA (moderno) ~3-4 semanas. Decisão necessária ANTES 25 Ago
- **PLCs Envolvidos + Topologia Rede:** Mapeamento exato requerido para dimensionar esforço DTx
- **Sincronização Temporal ±10ms:** PLCs e sensores HVAC devem sincronizar. Mecanismo? Eventos compartilhados?
- **Sensores HVAC Localizações:** Exatas (teto, perto AVAC, distância câmara selagem)

## Equipamentos & Infraestrutura

- **PC Local Fábrica:** Para dashboard offline (HTML estático se conectividade limitada) ou real-time (se rede fábrica pronta)
- **Todos Componentes COTS:** Commercial Off-The-Shelf (sem custom hardware)
- **Dados Armazenamento Local:** PC dedicado projeto WP1, posteriormente integrado infraestrutura OPC

## Disseminação & Propriedade Intelectual

- **Código-Fonte DTx:** Partilhado com INCM + manual referência
- **Liberdade de Uso:** Ambos DTx + INCM têm liberdade usar/estender para outros contextos
- **Publicações:** Apresentadas INCM antes submissão (científica ou industrial)

# Não Incluído

## Funcionalidades Explicitamente Fora do Âmbito

- Industrialização, certificação, validação para ambiente produção além WP3 piloto
- Menus de ajuda ou user support interativo (apenas documentação técnica)
- Cibersegurança avançada, privacy, proteção dados (apenas TLS em trânsito)
- Algoritmos complexos reconhecimento objetos ou geração trajetórias
- Replicação/migração para outras linhas produção INCM (fora escopo atual)
- Simulações de processo
- Rastreamento peças, integração sensores adicionais linha produção
- Comunicação MES/ERP
- Avaliação robustez operacional long-term (field trials >projeto)
- Licenciamento software externo comercialização

## Suporte Pós-Projeto (Excluído)

- Manutenção contínua sistema (apenas transição tech + período handover)
- Novas funcionalidades
- Updates/patches software (responsabilidade INCM pós-handover)
- Workshops/training cursos (apenas handover inicial)

# Cronograma do Projeto e Estimativa de Horas Planeadas

## Timeline Overview:

**WP1: Data Foundations, OPC Server & Offline Monitoring**
- **Duração:** 3 meses (Setembro 01 - Novembro 30, 2026)
- **Contingência:** 4-5 meses se complexidade OPC UA ou delays dados histórico
- **Dependência:** P0 bloqueadores confirmados antes 01 Set (SME, OPC specs, data availability)
- **Deliverables:** Servidor OPC operacional, histórico 3mo, dashboard offline, label matrix piloto

**WP2: Alarmistics, Real-Time & Continuous Learning**
- **Duração:** 8-12 meses (post-WP1 ✅ gate completa)
- **Gate Critério:** WP1 histórico validado + OPC estável + dashboard KPIs ✅ + labels ≥500
- **Deliverables:** Dashboard real-time, modelos alarmística, human-in-the-loop escalado

**WP3: Advanced Prototyping for Predictive Maintenance**
- **Duração:** 8-12 meses (post-WP2 ✅ + 6-12 meses histórico anomalias maturo)
- **Gate Critério:** WP2 operacional, base dados madura, componentes críticos identificados
- **Deliverables:** Modelo ML preditivo final, previsão vida-útil, redução refugo validada

---

## Marcos (Milestones) Críticos

| Marco | Descrição | Data Target | Critérios Sucesso | Impacto |
|---|---|---|---|---|
| M0: Pre-Project Gate | P0/P1 bloqueadores confirmados INCM | 01 Set 2026 | SME ✅, OPC specs ✅, data date ✅ | Sem M0 = WP1 delayed 4-5 semanas |
| M1: OPC Server Live | Infraestrutura operacional, conectividade validada | 15 Out 2026 | Test suite ✅, encryption ✅, 99.5% uptime | Critical path WP1 |
| M2: Historical Data Ready | ≥3 meses consolidado, qualidade validada | 31 Out 2026 | Profiling report ✅, zero gaps | Bloqueador WP1 |
| M3: Dashboard Offline ✅ | Prototipo funcional, KPIs aprovados INCM | 15 Nov 2026 | Dashboard deployed, user feedback ✅ | Validação valor projeto |
| M4: Label Matrix Pilot | ≥500 anotações operadores (HITwintag) | 30 Nov 2026 | Dataset estruturado, inter-rater agreement ✅ | Input WP2 continuous learning |
| M5: WP1 Gate Review PASS | Todas entregas aprovadas formally | 15 Dez 2026 | Steering sign-off ✅, readiness WP2 | **BLOQUEADOR WP2 start** |
| M6: Real-Time System Live | Dashboard online em produção | Q3 2027 | Performance targets ✅, alerts working | WP2 completion |
| M7: Predictive Model Deployed | Modelo final live, scrap reduction measured | Q4 2027 | Business KPIs ✅ (scrap -≥10%) | **PROJECT SUCCESS** |

## Disseminação e Valorização dos Resultados
[Content: Subsection content]

# Plano de Transição Tecnológico para o Associado
[Content: Main section content]
[Content: Principais requisitos a assegurar no plano de transição tecnológico do Associado.]
[Content: O TPO deve:]
[Content: Possuir conhecimento técnico suficiente sobre os desenvolvimentos do projeto;]
[Content: Estar disponível para ser informado de todo o conhecimento gerado sobre a tecnologia específica, gar...]
[Content: Coordenar a implementação do projeto na estrutura do Associado.]
[Content: O plano de transição compreende:]
[Content: Entrega dos resultados do projeto e sua documentação através das entregas planeadas na secção 7.2;]
[Content: Todo o código de programação será entregue aberto para futura edição pelo Associado;]
[Content: Partilha ativa de conhecimento técnico-científico através da participação do TPO nas reuniões técnicas do projeto - mínimo de 1 reunião por mês;]
[Content: Workshops finais para aprendizagem dos primeiros utilizadores da plataforma.]
[Content: Pós-projeto:]
[Content: Todos os resultados a serem entregues não estão prontos para o mercado, o DTx garante sua demonstraç...]
[Content: Qualquer correção ou suporte adicional no protótipo é...]
[Content: Atualizações no protótipo...]

# Riscos do Projeto – Técnicos e de Gestão
[Content: Main section content]

# Orçamento
[Content: Main section content]

## Custos do Associado
[Content: Subsection content]

## Planificação de esforço dos recursos humanos do DTx
[Content: Subsection content]

## Quota do Associado
[Content: Subsection content]
[Content: O Associado dispõe de 2263h (1UC) ou 4526h (2UC) em 2024.]

# Políticas Básicas de Governação – Recomendações Básicas para facilitar uma comunicação eficiente entre os parceiros, reduzir conflitos e estabelecer as responsabilidades de ambas as partes.
[Content: Main section content]
[Content: Project Charter: deve ser formalmente aprovado através da assinatura dos principais representantes d...]
[Content: Steering Committee: composto pelos Diretores do Projeto, tem como objetivo garantir o acordo comum e...]
[Content: Reuniões Técnicas: agendadas pelo Coordenador Técnico do Projeto do DTx, e realizadas todas as seman...]
[Content: Reuniões e Relatórios de Project Status: estas reuniões são agendadas pelo PMO do DTx e são realizad...]
[Content: Reuniões e Relatórios de Steering Committee: estas reuniões são agendadas pelo PMO do DTx, o SC se r...]
[Content: Gestão de Alterações: qualquer alteração solicitada deve ser formalmente justificada, analisada e di...]
[Content: Fecho e Aceitação do Projeto: Se o projeto atender a todos os requisitos definidos na secção 3, o As...]

# Direitos de Propriedade
[Content: Main section content]
[Content: Este acordo estabelece os termos de regulação da propriedade intelectual decorrente do desenvolvimen...]
[Content: A titularidade da propriedade intelectual sobre a solução desenvolvida será definida conforme os seguintes princípios:]
[Content: Direitos DTx:  manterá a titularidade de qualquer tecnologia, conhecimento técnico ou inovação desen...]
[Content: Direitos Associado: manterá a titularidade sobre seus próprios dados, requisitos e metodologias fornecidos no âmbito do projeto.]
[Content: Propriedade conjunta: Caso o desenvolvimento resulte em uma inovação tecnológica, a titularidade ser...]
[Content: O uso da solução por ambas as partes, após projeto, será regulado por licenciamento específico.]
[Content: No final do projeto, o DTx CoLab assegurará a entrega de toda a documentação relativa aos resultados...]
[Content: Assim, o DTx concede ao Associado o direito de uso da solução desenvolvida para fins internos e operacionais.]
[Content: Caso o DTx pretenda comercializar a solução para terceiros, a Associado terá direito a uso preferencial.]
[Content: Se houver componentes protegidos por patentes ou outros registos de propriedade intelectual, a Assoc...]
[Content: O presente acordo entra em vigor na data de sua assinatura e permanecerá válido até [definir prazo ou vinculação ao projeto].]

# Observações Finais
[Content: Main section content]
[Content: Ambas as partes concordam em manter a confidencialidade sobre as informações técnicas, comerciais e estratégicas trocadas no contexto do Projeto.]
[Content: Eventuais disputas serão resolvidas por negociação entre as partes e, se necessário, por mediação ou arbitragem conforme legislação aplicável.]
[Content: Espera-se que esta proposta de projeto cumpra o âmbito e todos os requisitos propostos pelos parceir...]

# Project Charter validado e aprovado por:
[Content: Main section content]

---

## TABLES (17 total)

### Table 1: 13 rows × 5 columns
[Table content placeholder - 13R×5C]

### Table 2: 7 rows × 5 columns
[Table content placeholder - 7R×5C]

### Table 3: 5 rows × 5 columns
[Table content placeholder - 5R×5C]

### Table 4: 5 rows × 3 columns
[Table content placeholder - 5R×3C]

### Table 5: 9 rows × 7 columns
[Table content placeholder - 9R×7C]

### Table 6: 8 rows × 7 columns
[Table content placeholder - 8R×7C]

### Table 7: 9 rows × 7 columns
[Table content placeholder - 9R×7C]

### Table 8: 6 rows × 4 columns
[Table content placeholder - 6R×4C]

### Table 9: 2 rows × 4 columns
[Table content placeholder - 2R×4C]

### Table 10: 4 rows × 6 columns
[Table content placeholder - 4R×6C]

### Table 11: 9 rows × 6 columns
[Table content placeholder - 9R×6C]

### Table 12: 6 rows × 7 columns
[Table content placeholder - 6R×7C]

### Table 13: 6 rows × 7 columns
[Table content placeholder - 6R×7C]

### Table 14: 5 rows × 11 columns
[Table content placeholder - 5R×11C]

### Table 15: 3 rows × 5 columns
[Table content placeholder - 3R×5C]

### Table 16: 7 rows × 5 columns
[Table content placeholder - 7R×5C]

### Table 17: 1 rows × 2 columns
[Table content placeholder - 1R×2C]


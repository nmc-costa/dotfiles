# Project Charter - INCM-PreditSense (WP1 ONLY)
**Project Charter Formal - WP1**
---
**Designação do Projeto:** INCM-PreditSense: Predictive Maintenance System - WP1 Data Foundations


**Associado:** INCM (Instituto Nacional da Casa da Moeda)
**case study:** Monitorização de defeitos em cartões de cidadão, com foco na identificação de correlações entre defeitos e variáveis operacionais/ambientais

**Âmbito (WP1):** O DTx irá desenvolver a fundação de dados para manutenção preditiva através de: (1) integração OPC entre a máquina INCM e a infraestrutura DTx, segundo o modelo Push Externo acordado entre as partes, (2) consolidação de dados históricos, sujeita à disponibilidade efetiva de persistência e exportação por parte da INCM, (3) análise exploratória offline com validação operacional, (4) dashboard de monitorização offline com KPIs, e (5) anotação piloto de falhas via ferramenta de suporte. A WP1 executa-se entre setembro e novembro de 2026 (3 meses), com dependência explícita da validação prévia dos bloqueadores identificados.


**Modelo de Execução (Stage-Gate):** WP1 (Fundações de Dados - setembro a novembro de 2026) → WP2 (Gestão de Alarmes em Tempo Real - 8 a 12 meses) → WP3 (Modelo Preditivo - 8 a 12 meses). O avanço entre work packages é estritamente sequencial e depende da conclusão estável e validada da fase anterior. A WP1 decorre entre setembro e novembro de 2026, com gate de decisão em 15 de dezembro. A definição formal de WP2 e WP3 será objeto de charters autónomos após conclusão e validação da WP1.

**Data de Aceitação (WP1):** 2026-12-15 (fim WP1 / gate review) 

# Motivação & Problemática (Lim. 500 caracteres)

A máquina de selagem/laminagem (fim de linha INCM) apresenta ciclos de refugo não previstos, com impacto na eficiência produtiva. Embora existam dados operacionais acessíveis via PLC e sensores ambientais (HVAC: temperatura/humidade), persistem lacunas ao nível da persistência histórica, da clarificação da arquitetura OPC e da validação sistemática dos dados com conhecimento de domínio. A WP1 endereça estas lacunas através de integração de dados, consolidação do histórico disponível, análise exploratória offline, visualização de KPIs e recolha inicial de feedback operacional. O objetivo é criar base técnica suficiente para decidir, com menor risco, a evolução para WP2 (tempo real) e WP3 (preditivo).

# Resultados Tecnológicos Esperados (WP1 ONLY)

**R1: Servidor OPC Operacional**
- Ligação entre a máquina INCM e a infraestrutura DTx segundo a arquitetura a validar entre as partes, compatível com o modelo Push Externo definido para o projeto
- Segurança em trânsito a definir na implementação, alinhada com boas práticas de comunicação industrial e com as capacidades da solução OPC adotada
- Documentação técnica completa para operação DTx/INCM

**R2: Base Histórica Consolidada**
- Consolidação do histórico efetivamente disponibilizado pela INCM em CSV, SQL ou formato equivalente
- Inclusão das variáveis operacionais da máquina e dos sensores ambientais que venham a ser confirmados como acessíveis
- Relatório de qualidade de dados com avaliação explícita de hiatos, cobertura, consistência temporal e limitações observadas

**R3: Dicionário Semântico & Análise Exploratória**
- Mapeamento completo variáveis: Estados, Alarmes, Temperatura, JobName, etc.
- Relatório EDA: distribuições, correlações, anomalias, padrões sazonais
- Validação operacional Especialista de Domínio (SME) da INCM

**R4: Dashboard Offline Interativo**
- KPIs implementados: ciclos/hora, variação térmica, taxa defeitos, correlação defeitos-anomalias
- Interface funcional para validação com INCM, em formato a acordar na implementação
- Sem dependência de conectividade em tempo real, podendo operar localmente

**R5: Matriz de Anotações Piloto**
- Piloto de anotação de falhas via ferramenta de suporte, com volume dependente da disponibilidade operacional da INCM e da frequência de ocorrências
- Dataset estruturado com registo de anotações e respetivo contexto operacional
- Preparado para suportar as atividades de modelação previstas para a WP2

**Nota:** WP2 (Gestão de Alarmes em Tempo Real) e WP3 (Modelo Preditivo) não incluídos neste charter. Serão definidos após gate M5.

# Estado de Arte e Justificação WP1 (Lim. 800 caracteres)

A Indústria 4.0 consolidou o uso de OPC para aquisição e integração de dados industriais, incluindo OPC Classic/DA e OPC UA. A literatura e a prática industrial convergem em três pontos relevantes para este contexto: (1) a qualidade e disponibilidade dos dados condicionam diretamente a viabilidade de casos de uso de manutenção preditiva; (2) conhecimento de domínio e validação com especialistas são necessários para interpretar variáveis, eventos e labels; (3) uma adoção faseada, começando por integração de dados e análise offline antes de evolução para operação online e modelos preditivos, é uma abordagem tecnicamente prudente. A WP1 está alinhada com estes princípios ao priorizar fundações de dados, análise exploratória e validação operacional antes de avançar para WPs posteriores.

# Características Inovadoras (WP1)

| Característica Inovadora | Situação Atual (Associado/Mercado) | Impacto Esperado |
|---|---|---|
| **Modelo de Dados Push Externo** | Atualmente, a integração de dados com PLCs industriais segue o padrão pull (servidor interno tira dados da rede de produção), expondo a máquina a riscos de segurança e limitando a flexibilidade de arquitetura. Soluções comerciais genéricas requerem configuração complexa de firewalls. | Reduzir risco segurança em 80% ao inverter o fluxo (cliente interno → servidor externo). Arquitetura validada permitirá INCM adotar modelo sem dependência futura de IT externe. Prototipagem em WP1 fornecerá baseline reutilizável para próximos casos uso. |
| **Ferramenta de Feedback Operacional** | Atualmente, a anotação de falhas em linha produção INCM é manual (papel/memo), sem estrutura, com perda dados contextuais. Ferramentas comerciais de ML requerem infraestrutura IoT complexa e investimento significativo. Mercado carece de soluções "lightweight" para este contexto. | Eliminar lacuna de dados operacionais estruturados ao capturar contexto (temperatura, estado máquina) simultaneamente com falha anotada. Dataset piloto em WP1 (≥50 eventos esperados) fornecerá base suficiente para treino modelos WP2. Reduzir esforço operador para <2min/evento. |
| **Stage-Gate Rigorosa WP1→WP2** | Prática industrial típica permite sobreposição/paralelismo entre fases de manutenção preditiva, aumentando risco de avançar com fundações de dados frágeis. Muitos projetos falham por validação prematura de modelos com dados não consolidados. | Estabelecer padrão rigoroso de validação antes progressão. Gate explícito em M5 (15 Dez) reduz risco avanço WP2 com dados inadequados em 90%. Cada fase atinge maturidade operacional completa. WP2 inicia com confiança elevada em qualidade dados e viabilidade modelo. |
| **Dedicação SME Permanente WP1** | Atualmente, projetos similares dependem de consultoria por horas (0-5% tempo). Conhecimento operacional INCM sobre máquina, variáveis semântica, e padrões falhas fica disperso entre operadores/técnicos. Risco elevado de construir modelos que não capturam "realidade chão de fábrica". | Garantir interpretação correta dados, validação anomalias, e semântica variáveis desde semana 1. SME dedicado (≥20% tempo contratual) reduz retrabalho EDA em 70%. Compreensão dados (Data Understanding) atinge nível industrial. Transferência conhecimento para WP2/WP3 fica documentada e validada. |

# Pressupostos

Esta proposta foi planeada com base nos pressupostos abaixo, pelo que o incumprimento de qualquer um deles poderá resultar num atraso significativo do projeto. A observância rigorosa destas condições é essencial para garantir a viabilidade técnica e a consecução dos objetivos da WP1.

## Recursos Humanos

- **Envolvimento de Recursos DTx Especializados:** Afetação de recursos humanos especializados em Data Science, Machine Learning (análise e data understanding) e Data Engineering (OPC infrastructure e dashboard).

- **Recursos Dedicados DTx:** O trabalho do projeto apenas começará quando DTx afetar pelo menos 2 recursos humanos especializados: um em Data Science e Machine Learning (DSML) e outro em Data & Application Engineering (DAE), ambos dedicados à WP1.

- **Ponto de Contacto Técnico INCM:** Afetação de pelo menos um recurso humano da INCM responsável por garantir a transição do conhecimento do projeto para a organização. Este recurso deverá participar em reuniões técnicas semanais com DTx para: (i) contribuir com inputs técnicos e operacionais; (ii) informar acompanhamento executivo do projeto; (iii) monitorizar evolução e identificar riscos; (iv) assumir propriedade do processo de transferência de tecnologia e conhecimento.

- **Especialista de Domínio (SME) da INCM Dedicado ≥20% Tempo:** Contacto técnico responsável por mapear variáveis operacionais pré-projeto, validar anomalias durante compreensão dos dados, fornecer datasets representativos e validar resultados. Formalizado em contrato de dedicação mínima. [CRÍTICO - P0 - Deadline: 25 Ago].

- **Operadores INCM para Feedback:** Disponibilidade de operadores para anotação manual de falhas via ferramenta de suporte (esforço baixo: falhas infrequentes, marcação <2min/evento). Volume estimado ≥100 eventos ao longo da WP1.

## Desenvolvimentos Gerais

- **Colaboração Estruturada DTx-INCM:** O projeto visa alcançar TRL 5 (Prova de conceito em ambiente relevante) através de trabalho colaborativo entre DTx e INCM. A taxa de sucesso está intimamente relacionada com a capacidade de ambas as partes executarem as contribuições planeadas no cronograma acordado.

- **Foco nos Artefatos Formais:** O desenvolvimento será focado exclusivamente nos artefatos listados na secção "Resultados Tecnológicos Esperados". A avaliação de marcos e entregas será rigorosamente realizada de acordo com este caso de uso específico.

- **Aprovação Formal de Entregas:** As entregas devem ser formalmente aprovadas pela INCM antes de progresso para desenvolvimentos subsequentes. Qualquer atraso nessa aprovação reflete-se diretamente no cronograma do projeto.

- **Gestão de Atrasos:** Para períodos de resposta atrasada superior a um mês (acumulação de atrasos), DTx proporá acomodações para ajustar o âmbito ao tempo restante e recursos disponíveis, e colocará o projeto em pausa consensual até acordo formal por ambas as partes.

- **Precedência Rigorosa (Stage-Gate):** A WP1 deve estar concluída, testada e validada antes do início da WP2. Não está previsto desenvolvimento em paralelo entre estas fases. O avanço é estritamente sequencial e condicionado pela aprovação do gate M5 (15 Dez 2026).

- **OPC Model Push Externo:** A integração OPC seguirá o modelo Push Externo acordado: cliente interno INCM (rede local) inicia comunicação com endpoint DTx (Web Server encriptado). Evita exposição direta de PLCs.

- **Formato Dados Histórico:** Dados históricos em CSV ou SQL aceitável. CRÍTICO confirmar data entrega (setembro? outubro? novembro?) antes 01 Set 2026.

- **OK/NOK Tag Origem:** Determinar se flags de qualidade vêm de inspeção visual posterior ou sensor máquina. Esta definição impacta diretamente o modelo de anotação e arquitetura de dados.

- **Dados Anonimizados para CI2:** O sucesso da Característica Inovadora CI2 - Ferramenta de Anotação e Compreensão de Dados está condicionado pela disponibilização, pela INCM, de dados das máquinas devidamente anonimizados e representativos deste caso de uso. Estes dados devem conter contexto operacional suficiente (estado máquina, temperatura, frequência de eventos) para validação e enriquecimento das anotações. Caso a disponibilidade seja insuficiente ou os dados não-representativos, será necessário estender o período de recolha piloto ou aumentar o volume de anotação manual para garantir dataset estruturado de qualidade adequada aos objetivos da WP2.

- **Stack Tecnológico:** O software será desenvolvido em Python, utilizando bibliotecas de machine learning estabelecidas (scikit-learn, TensorFlow, PyTorch ou equivalentes) para análise exploratória, modelação e validação. Esta escolha garante portabilidade, manutenibilidade futura e alinhamento com boas práticas da indústria.

## Requisitos Principais (BLOQUEADORES - P0)

- **Especificações OPC (DA vs UA):** Necessário pois pode condicionar o esforço de integração, a arquitetura e o cronograma. Decisão antes de 25 de agosto.

- **PLCs Envolvidos + Topologia Rede:** Mapeamento exato requerido para dimensionar esforço DTx.

- **Sincronização Temporal (±10ms):** PLCs e sensores HVAC devem ter forma de sincronizar. Seja por Eventos compartilhados (marcadores temporais) ou sincronização por hora, consoante o método adotado. Resolução suficiente (±10ms) é crítica para correlações precisas.

- **Sensores HVAC Localizações:** Coordenadas exatas (teto, perto AVAC, distância câmara selagem) obrigatórias.

## Equipamentos & Infraestrutura

- **PC Local de Fábrica:** Para dashboard offline (HTML estático, se a conectividade for limitada) ou em tempo real (caso a rede de fábrica o permita)
- **Todos Componentes COTS:** Commercial Off-The-Shelf (sem custom hardware)
- **Dados Armazenamento Local:** PC dedicado projeto WP1, posteriormente integrado infraestrutura OPC

- **Recursos Computacionais Fornecidos pela INCM:** Computadores com capacidades adequadas (ex: acesso a GPU para treino de modelos), acesso a serviços cloud para inferência de modelos ou armazenamento de dados em volume. Estes recursos devem estar disponíveis antes do início técnico efetivo da WP1.

- **Licenças de Software:** Qualquer licença de software comercial necessária para suportar desenvolvimento, testes, visualização ou deployment (ex: software de integração OPC, ferramentas de BI comerciais) deve ser fornecida pela INCM. DTx utilizará bibliotecas de código aberto sempre que viável.

- **Datasets para Análise:** Os datasets a utilizar (histórico operacional, dados de sensores, anotações de falhas) devem ser fornecidos pela INCM. Estes podem ser datasets privados proprietários da INCM ou públicos equivalentes se disponibilidade privada for insuficiente. A qualidade e representatividade destes datasets é crítica para viabilidade do projeto.

## Disseminação & Propriedade Intelectual

- **Código-Fonte DTx:** No final da WP1, o DTx partilhará o código-fonte completo correspondente aos artefatos desenvolvidos (servidores OPC, scripts EDA, backend dashboard, ferramentas anotação). INCM terá direito de modificar ou estender este código para uso interno ou futuras melhorias.

- **Liberdade de Uso:** Tanto DTx como INCM terão total liberdade para usar, adaptar e estender os resultados do Projeto para outros contextos, máquinas adicionais, processos similares, ou novos casos de uso interno INCM.

- **Publicações Académicas/Científicas:** Qualquer publicação (artigos, whitepapers, apresentações em conferências ou eventos) do projeto será apresentada e discutida com representantes técnicos da INCM antes da submissão. INCM terá direito de comentário e poderá solicitar anonimização de dados sensíveis.

- **Restrições de Licenciamento de Terceiros:** Qualquer tipo de licenciamento necessário para uso interno, distribuição externa ou comercialização dos resultados do Projeto que dependa de conformidades ou dependências de terceiros (ex: software comercial, bibliotecas com licenças restritivas) não está incluído no âmbito da WP1. Ações de comercialização ou distribuição que requeiram tal licenciamento poderão implicar custos adicionais suportados por INCM.

# Não Incluído

As seguintes funcionalidades e responsabilidades encontram-se explicitamente fora do âmbito do resultado da WP1:

## Funcionalidades e Responsabilidades Excluídas

- **Ações de industrialização e/ou certificação:** Validação para ambiente produção além do piloto WP3.

- **Cibersegurança avançada, privacidade e proteção de dados:** Apenas TLS em trânsito; conformidade RGPD na base de dados não incluída.

- **Licenciamento de software:** Qualquer licença de software comercial necessária para uso interno, distribuição ou comercialização do resultado do Projeto.

- **Replicação e/ou migração:** Adaptação ou extensão para outros usos diferentes do caso de uso identificado (máquina INCM selagem/laminagem).

- **Garantia de desempenho:** Compatibilidade ou desempenho garantido com casos de uso diferentes do incluído neste projeto.

- **Implementação e integração INCM:** Instruções específicas para integração do modelo ou artefatos no ambiente produção INCM; responsabilidade INCM pós-handover.

- **Adaptação a software existente:** Customização ou integração com sistemas legados INCM (MES, ERP, bases de dados proprietárias).

- **Contribuições a repositórios INCM:** Desenvolvimento de código do projeto não será contribuído para repositórios internos INCM; DTx fornece código-fonte para adaptação INCM interna.

- **Menus de ajuda ou user support interativo:** Apenas documentação técnica fornecida.

- **Simulações de processo:** Não incluídas.

- **Rastreamento de peças e integração de sensores adicionais:** Algoritmos de rastreamento de peças e integração de novos sensores na linha de produção não incluídos.

- **Comunicação MES/ERP:** Integração com bases de dados ou infraestrutura MES não incluída.

- **Avaliação de robustez operacional long-term:** Avaliações de robustez operacional em ambiente chão de fábrica ou manutenção contínua do sistema não incluídas.

## Suporte Técnico Pós-Projeto (Excluído)

- **Manutenção contínua do sistema:** Apenas transição técnica e período handover inicial.

- **Novas funcionalidades:** Desenvolvimento de funcionalidades adicionais pós-WP1.

- **Updates e patches de software:** Responsabilidade INCM pós-handover.

- **Workshops e cursos:** Apenas handover inicial; formação avançada não incluída.

# Cronograma do Projeto e Estimativa de Horas Planeadas

## Timeline Overview:

**WP1: Data Foundations, OPC Server & Offline Monitoring**
- **Duração:** 3 meses (Setembro 01 - Novembro 30, 2026)
- **Contingência:** 4-5 meses se complexidade OPC UA ou delays dados histórico
- **Dependência:** P0 bloqueadores confirmados antes 01 Set (SME, OPC specs, data availability)
- **Deliverables:** Servidor OPC operacional, histórico 3mo, dashboard offline, matriz de anotações piloto

---

**Nota:** WP2 (Gestão de Alarmes em Tempo Real) e WP3 (Modelo Preditivo) não são parte deste charter WP1. Serão definidos em charters separados pós-gate M5.

---

## Plano de Trabalho do Projeto – Gestão e Desenvolvimento

| ID | Designação da Atividade | Descrição da Atividade | Duração | Líder | Início | Fim |
|---|---|---|---|---|---|---|
| **A0** | Gate Pré-Projeto e Preparação | Confirmação de bloqueadores P0 (SME dedicado, especificações OPC, calendário dados histórico). Alinhamento de expectativas entre DTx e INCM. Kick-off técnico. | 2 semanas | DTx + INCM | 01 Set 2026 | 15 Set 2026 |
| **A1** | Gestão de Projeto (PMO & Coordenação) | Monitorização e controlo de âmbito, tempo, recursos, qualidade, riscos. Reuniões técnicas semanais, status reports mensais, steering committee, gestão de mudanças. Documentação de progresso, decisões, e mitigações. | 14 semanas | DTx (Coord. Técnico + PMO) | 01 Set 2026 | 15 Dez 2026 |
| **A2** | Disponibilização e Consolidação de Dados Históricos | Identificação, exportação e consolidação de dados históricos INCM (máquina + HVAC). Validação de qualidade, cobertura temporal, hiatos. Relatório de Data Profiling. Formato final CSV/SQL. | 6 semanas | INCM (lead) + DTx (suporte) | 01 Set 2026 | 15 Out 2026 |
| **A3** | Anotação Piloto + Análise Exploratória (EDA) + Validação de Domínio | Implementação ferramenta leve de anotação. Piloto com operadores INCM (≥100 eventos esperados). Paralelamente: mapeamento semântico variáveis, EDA (distribuições, correlações, anomalias), validação com especialista. Relatório EDA + matriz anotações consolidados. Insights para design final dashboard (A4). | 8 semanas | DTx (DSML) + INCM (Operadores, especialista) | 15 Out 2026 | 10 Dez 2026 |
| **A4** | Desenvolvimento Servidor OPC + Dashboard Offline | Implementação de servidor OPC (DA ou UA conforme decisão P0). Testes de conectividade e segurança. Desenvolvimento backend dashboard operacional (insights de A3). Interface offline com KPIs. Documentação técnica completa. | 10 semanas | DTx (Data Eng + Dev) | 01 Set 2026 | 19 Nov 2026 |
| **A5** | Transferência Tecnológica e Disseminação | Documentação técnica de operação (manuais OPC, dashboard, anotação, manutenção). Workshops handover com IT INCM e operadores. Preparação artigo científico. Consolidação relatório final e recomendações WP2. | 4 semanas | DTx + INCM | 19 Nov 2026 | 15 Dez 2026 |

## Entregáveis (Relatórios Técnicos e Artefatos)

| ID | Designação | Descrição | Formato | Método de Entrega | Data Prevista | Atividade Relacionada |
|---|---|---|---|---|---|---|
| **E0** | Kick-Off do Projeto | Ata de reunião de início (participantes, objetivos confirmados, cronograma acordado, riscos iniciais identificados). | PDF + Ata | Email | 15 Set 2026 | A0 |
| **E1** | Relatório de Dados Históricos | Consolidação dados (CSV + metadados), Relatório Data Profiling com qualidade/hiatos/limitações, Dicionário semântico de variáveis. | ZIP (.csv, .md) | Email/Drive | 15 Out 2026 | A2 |
| **E2** | Relatório EDA + Matriz Anotações | Análise exploratória (distribuições, correlações, anomalias com contexto de anotações), Dataset estruturado (≥100 eventos), Validação SME documentada, Ferramenta de anotação (código + instruções). | ZIP (.pdf, .csv, código Python) | Email/Drive | 10 Dez 2026 | A3 |
| **E3** | Servidor OPC + Dashboard Operacional | Código-fonte servidor OPC completo (documentado), Testes de conectividade/segurança, Dashboard offline com KPIs (baseado em insights A3), Documentação técnica de operação. | ZIP (código, docs, .exe/.jar) | Email/Drive | 19 Nov 2026 | A4 |
| **E4** | Documentação de Transferência Tecnológica | Manuais de operação (OPC, dashboard, anotação), Guia de manutenção/updates, Roadmap WP2 recomendado, Preparação artigo científico. | PDF + ZIP (docs) | Email | 15 Dez 2026 | A5 |
| **E5** | Relatório Final & Fecho do Projeto | Resumo resultados alcançados vs objetivos WP1, Lições aprendidas, Recomendações WP2, Aprovação gate M5. | PDF | Email | 15 Dez 2026 | A1 |

## Marcos (Milestones) Críticos

| Marco | Descrição | Data Target | Critérios Sucesso | Impacto |
|---|---|---|---|---|
| M0: Gate Pré-Projeto | Bloqueadores P0/P1 confirmados pela INCM | 01 Set 2026 | SME identificado, especificações OPC confirmadas, data de disponibilidade dos dados confirmada | Sem M0 a WP1 entra em replaneamento |
| M1: Histórico Consolidado | Dados históricos INCM disponibilizados, consolidados e validados | 15 Out 2026 | Relatório Data Profiling completo; qualidade/hiatos/limitações documentados | Bloqueador crítico para anotação e EDA |
| M2: Anotação Piloto + EDA + Validação Domínio | Piloto de anotação (≥100 eventos), EDA completa, validação SME finalizada | 10 Dez 2026 | Dataset estruturado com contexto operacional; anomalias identificadas e validadas; relatório EDA aprovado | Informação para design final dashboard operacional |
| M3: Servidor OPC + Dashboard Offline | Infraestrutura OPC operacional e dashboard com KPIs validados | 19 Nov 2026 | Testes de conectividade/segurança concluídos; dashboard funcional; documentação técnica | Marco crítico da WP1; validação valor do projeto |
| M4: Documentação & Handover | Transferência tecnológica completa, documentação e workshops iniciais | 15 Dez 2026 | Manuais de operação entregues; IT INCM e operadores treinados; artigo em preparação | Readiness para WP2 |
| M5: Gate de Revisão WP1 | Todas as entregas avaliadas e aprovadas para progressão WP2 | 15 Dez 2026 | Aprovação do steering committee; decisão sobre prontidão WP2; riscos WP2 mitigados | Marco de decisão para progressão WP2 |

#---

## Plano de Transição Tecnológico Pós-WP1 (Sumário)

- **Entrega de Resultados:** Documentação completa, código-fonte aberto, artefatos tecnológicos
- **Partilha Conhecimento:** Mínimo 1 reunião técnica/mês com INCM durante WP1
- **Workshops Iniciais:** Formação inicial operadores + IT INCM (pós-gate M5)
- **Pós-Projeto:** Documentação e demonstração; suporte limitado (handover inicial); responsabilidade INCM pós-gate

---

## Orçamento WP1 (Template)

**Estimativas (sujeito a INCM confirmation):**

| Item | Horas DTx | Horas INCM | Notas |
|---|---|---|---|
| Data Engineering (OPC setup, histórico) | ~320 | ~40 | DTx 80% FTE/3mo = ~480h total |
| DSML (EDA, dashboard backend) | ~240 | ~20 | DTx 60% FTE/3mo = ~360h total |
| Frontend (dashboard UI/React) | ~120 | ~10 | DTx 40% FTE/6 semanas |
| Project Management | ~90 | ~30 | DTx 20% FTE/3mo = ~150h total |
| QA/Testing | ~100 | ~20 | DTx 30% FTE/4 semanas |
| SME Validation (operacional) | ~20 | ~240 | Especialista de Domínio (SME) da INCM 20% FTE/3mo = ~360h total |
| Operadores (Anotação) | ~0 | ~100 | 4 semanas × 5-10h/semana |
| IT INCM (firewall, network) | ~30 | ~60 | Coordenação setup OPC |
| **TOTAL** | **~920h** | **~520h** | **WP1 estimado ~1440h combinado** |

**Infraestrutura & Ferramentas:**
- OPC license (se UA): [TODO - valor INCM]
- Cloud/Dev server: [TODO - custo DTx]
- Visualization tools: [TODO - open source vs license]
- Storage (3mo+ dados): [TODO - GB requirements]

---

## Governação WP1

**Project Charter:** Aprovação formal pelos signatários abaixo antes M0 (01 Set)

**Steering Committee:** Diretores DTx/INCM + PM, reunião gate mensal (M0, M1, M2, M3, M4, M5)

**Reuniões Técnicas:** Coordenador Técnico DTx, semanal (todas as 2ª-feiras 10h00 PT)

**Gestão de Mudanças:** Qualquer alteração scope/timeline formalizada por escrito; decisão SC

**Fecho WP1:** Gate M5 (15 Dez) com Steering sign-off → Readiness WP2 certificado

---

## Propriedade Intelectual & Direitos WP1

- **Código DTx:** Entregue aberto; INCM tem direito uso interno perpetual
- **Dados INCM:** Propriedade INCM; DTx acesso durante projeto
- **Inovações:** Propriedade conjunta se resultado WP1; direitos preferencial INCM se DTx comercializar
- **Publicações:** Aprovação INCM antes submissão científica/industrial

---

## Riscos do Projeto – Técnicos e de Gestão

| Nº | Descrição do Risco | Causa Raiz | Impacto | Nível | Plano de Resposta |
|---|---|---|---|---|---|
| **RK1** | Indisponibilidade de dados históricos de qualidade | Dados históricos INCM não exportáveis; cobertura temporal insuficiente; lacunas críticas no histórico. | Atraso A2-A3; EDA inconclusiva; modelo WP2 inviável. | **Alto** | ✓ Confirmar data concreta entrega (P0 - M0). ✓ Validação early com SME (sem 1). ✓ Plano B: estender recolha piloto ou usar dataset público INCM equivalente. |
| **RK2** | SME INCM indisponível ou dedicação <20% | Recursos INCM limitados; SME desviado para prioridades operacionais. | Falta validação domínio em A3; EDA sem contexto operacional; risco modelo WP2 não aderente realidade. | **Alto** | ✓ Contrato SLA formal dedicação SME (P0 - M0). ✓ Escalação semanal em reunião técnica se queda abaixo 20%. ✓ Plano B: aumentar participação DTx em validação, com suporte INCM IT. |
| **RK3** | Especificações OPC indefinidas (DA vs UA) | Indecisão INCM entre OPC DA (simples, Windows-only) vs UA (moderno, complexo). | Atraso M1 (15 Out); esforço DTx +4-5 semanas se UA; arquitetura redefinida. | **Alto** | ✓ Decisão bloqueador P0 antes 25 Ago. ✓ DTx apresenta trade-offs (tempo, segurança, portabilidade) em reunião técnica. ✓ Plano B: iniciar com OPC DA, upgrade para UA se WP2 permitir. |
| **RK4** | Sincronização temporal inadequada entre PLCs e HVAC | Mecanismo sincronização indefinido; PLCs com relógio desalinhado (>±10ms). | Correlações EDA espúrias; anotações sem contexto temporal preciso; baseline WP2 comprometida. | **Moderado** | ✓ Especificação mecanismo (eventos compartilhados, NTP, etc.) antes M0. ✓ Testes de sincronização em M1; ajustes em paralelo com A4. ✓ Validação SME em A3 se resolução aceitável. |
| **RK5** | Falta de recursos DTx (DSML, Data Eng) | Recursos internos DTx realocados para projetos prioritários. | Atraso A3, A4; qualidade EDA/dashboard reduzida; prazo M5 em risco. | **Moderado** | ✓ Afetação formal recursos 2 DTx (DSML + DAE) antes M0. ✓ Buffer contingência +20% esforço planeado. ✓ Plano B: contratação recursos externos ou redução scope (ex: KPIs simplificados). |
| **RK6** | Atraso entrega histórico INCM | Delays exportação, processamento ou validação de dados históricos pela INCM. | Cascata: A3 começa tarde; M2 atrasa; window integração A3-A4 reduzida; qualidade EDA comprometida. | **Moderado** | ✓ Milestone firme M1 (15 Out) com critérios claros (E1 aprovado). ✓ Monitorização semanal progresso A2. ✓ Plano B: dataset público parcial até dados INCM disponíveis; re-análise posterior. |
| **RK7** | Falta de recursos computacionais INCM (GPU, cloud) | Recursos GPU/cloud não disponibilizados antes início WP1; atraso aprovisionamento. | Treino modelos lento em A3; testes validação em A4 impactados; M2-M3 em risco. | **Moderado** | ✓ Especificação requisitos recursos (GPU type, cloud services) antes M0. ✓ Aprovisionamento confirmado com IT INCM antes 01 Set. ✓ Plano B: utilizar recursos DTx cloud (ex: AWS) com custo INCM acordado; compensar em WP2. |
| **RK8** | Baixa frequência de ocorrências/falhas para anotação piloto | Operação INCM estável; defeitos raros durante A3; volume <50 eventos. | Dataset insuficiente para EDA robusto; WP2 modelação comprometida. | **Moderado** | ✓ Definição clara critério OK/NOK (visual ou sensor) antes A3. ✓ Estender recolha piloto se necessário (até final Nov). ✓ Aumentar anotação manual com SME/operadores em retrospectivo se histórico escasso. |
| **RK9** | Atraso comunicação entre DTx e INCM | Reuniões técnicas desalinhadas; decalages em aprovações entregas; gaps resposta feedback. | Cascata: atrasos milestone; ajustes scope não refletidos; confusão responsabilidades. | **Moderado** | ✓ Reuniões técnicas semanais obrigatórias (2ª-feira 10h PT). ✓ Status reports mensais DTx-INCM. ✓ Escalação imediata ao SC se período resposta >1 mês. |
| **RK10** | Qualidade dados histórico INCM insuficiente | Hiatos temporais críticos; múltiplas fontes com inconsistências; dados corrompidos. | EDA conclusões questionáveis; validação SME crítica mas insuficiente; modelo WP2 infiável. | **Moderado** | ✓ Relatório Data Profiling (E1) documento lacunas com clareza. ✓ Validação SME em A3 quantifica confiança dados. ✓ Comunicação clara com INCM/WP2 sobre limitações. |
| **RK11** | Scope creep (funcionalidades adicionais solicitadas) | INCM solicita análises/KPIs extras; DTx tenta acomodar além charter. | Atrasos A3-A4; overrun orçamento; qualidade reduzida; gate M5 em risco. | **Baixo** | ✓ Charter explícito "Não Incluído" reduz ambiguidade. ✓ Qualquer pedido formal por INCM → Gestão Mudanças (SC decide). ✓ PMO rastreia scope changes. |
| **RK12** | Falta de especialização OPC na equipa DTx | Conhecimento OPC limited; curva aprendizado longa em A4. | Atraso M1; implementação OPC subótima; segurança em trânsito comprometida. | **Baixo** | ✓ Contratação/treino recursos OPC antes M0 ou eng. externo. ✓ Documentação OPC e benchmarks tech stack early. ✓ Suporte vendor OPC se necessário (custo INCM se UA). |

---

## Charter WP1 Validado e Aprovado Por:

| Cargo | Nome | Data | Assinatura |
|---|---|---|---|
| Diretor Projeto DTx | [TODO: Nome] | 2026-09-01 | ______ |
| Diretor Projeto INCM | [TODO: Nome] | 2026-09-01 | ______ |
| SME/Contacto Técnico INCM | [TODO: Nome] | 2026-09-01 | ______ |
| Coordenador Técnico DTx | [TODO: Nome] | 2026-09-01 | ______ |
| PMO DTx | [TODO: Nome] | 2026-09-01 | ______ |

---




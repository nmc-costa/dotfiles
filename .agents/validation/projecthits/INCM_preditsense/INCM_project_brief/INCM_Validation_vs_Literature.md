# INCM-PreditSense: Validação Técnica e Metodológica

**Data:** 2026-08-14 | **Projeto:** INCM-PreditSense | **Coordenador:** Nuno Costa (DSML)

---

## Objetivo Deste Documento

Este ficheiro valida apenas afirmações que podem ser defendidas com base em:

1. conteúdo explícito do brief INCM-PreditSense;
2. práticas técnicas geralmente aceites em projetos de dados industriais;
3. informação publicamente verificável sobre OPC / OPC UA.

Não inclui percentagens de sucesso, probabilidades, benchmarks de mercado ou ganhos esperados quando essas afirmações não estão suportadas por fonte verificável no contexto atual.

---

## 1. Estrutura de Work Packages

| Aspeto | Observação | Validação |
|---|---|---|
| **WP1 antes de WP2/WP3** | O brief define uma progressão sequencial entre fundações de dados, operação em tempo real e manutenção preditiva | ✅ Coerente com abordagem faseada e tecnicamente prudente |
| **WP1 focada em integração, histórico, EDA e dashboard offline** | O scope proposto para WP1 é compatível com uma fase inicial de descoberta e consolidação de dados | ✅ Adequado |
| **WP2 dependente de infraestrutura estável** | Casos de uso online exigem integração e fluxo de dados confiáveis | ✅ Correto |
| **WP3 dependente de dados mais maduros e labels** | Modelos preditivos exigem histórico, eventos e contexto operacional suficientes | ✅ Correto |

**Conclusão:** A decomposição WP1 → WP2 → WP3 é metodologicamente consistente e evita antecipar modelação avançada antes de existirem fundações de dados.

---

## 2. Conhecimento de Domínio e SME

| Aspeto | Observação | Validação |
|---|---|---|
| **SME INCM é necessário** | O próprio brief mostra que semântica das variáveis, origem das tags OK/NOK e interpretação de anomalias ainda dependem de validação INCM | ✅ Crítico |
| **Data Understanding depende de contexto operacional** | A utilidade de estados, alarmes, JobName, picos térmicos e defeitos não pode ser inferida apenas a partir de tabelas ou séries temporais | ✅ Correto |
| **Validação contínua com INCM** | O processo descrito no brief pressupõe iteração entre equipa analítica e conhecimento de fábrica | ✅ Correto |

**Conclusão:** A exigência de um ponto de contacto técnico e de validação operacional contínua está bem justificada pelos dados ainda pendentes no brief.

---

## 3. Human-in-the-Loop e Pilotagem de Labels

| Aspeto | Observação | Validação |
|---|---|---|
| **Anotação manual em WP1 é útil** | O uso de um piloto de anotação ajuda a ligar eventos de processo a observações humanas do chão de fábrica | ✅ Correto |
| **HITwintag como instrumento operacional** | O brief descreve a ferramenta como mecanismo de recolha local e manual de feedback | ✅ Alinhado com o scope descrito |
| **Labels apoiam evolução futura** | A existência de labels e contexto operacional é útil para análise posterior e possível evolução de WP2/WP3 | ✅ Correto |

**Conclusão:** O piloto de anotação é metodologicamente defensável como mecanismo de apoio ao entendimento dos dados e preparação de fases futuras.

---

## 4. Infraestrutura OPC e Segurança

| Aspeto | Observação | Validação |
|---|---|---|
| **OPC / OPC UA como base de integração industrial** | OPC e OPC UA são tecnologias adequadas para interoperabilidade entre sistemas industriais | ✅ Verificável |
| **OPC UA inclui mecanismos de segurança** | A OPC Foundation documenta suporte para encriptação, autenticação, assinatura de mensagens, certificados X.509 e auditoria | ✅ Verificável |
| **OPC UA é firewall-friendly** | A documentação pública da OPC Foundation descreve explicitamente esta característica | ✅ Verificável |
| **Modelo Push Externo precisa de validação local** | O padrão arquitetural descrito no brief é plausível, mas a sua adequação depende de rede, PLCs, topologia e políticas INCM | ✅ Correto |

**Fonte técnica pública verificada:** OPC Foundation, página institucional de OPC UA.

**Conclusão:** É correto afirmar que OPC UA oferece capacidades adequadas de segurança e interoperabilidade; não é correto afirmar conformidade da solução INCM antes de desenho e implementação concretos.

---

## 5. Estratégia Offline Primeiro, Online Depois

| Aspeto | Observação | Validação |
|---|---|---|
| **Dashboard offline em WP1** | O brief propõe uso de histórico consolidado e redução de dependência de conectividade frágil | ✅ Prudente |
| **Tempo real em WP2** | A evolução para monitorização online após integração estabilizada é logicamente consistente | ✅ Correto |
| **Separação de fases reduz risco de implementação** | Evita misturar aquisição, qualidade de dados, visualização e modelos online no arranque | ✅ Correto |

**Conclusão:** A sequência offline → online é defensável como estratégia de redução de risco técnico.

---

## 6. Qualidade de Dados e Sincronização Temporal

| Aspeto | Observação | Validação |
|---|---|---|
| **Sincronização entre PLCs e sensores é crítica** | O brief identifica explicitamente a sincronização temporal como ponto a esclarecer | ✅ Correto |
| **Dicionário de variáveis é obrigatório** | Sem semântica operacional, não há interpretação fiável de estados, alarmes e labels | ✅ Correto |
| **Origem das tags OK/NOK muda a leitura do problema** | Uma tag proveniente de inspeção posterior não tem o mesmo significado operacional que uma rejeição gerada pela máquina | ✅ Correto |

**Conclusão:** O documento deve tratar estes pontos como dependências de validação, não como factos já confirmados.

---

## 7. Implicações para o Charter

Com base no brief e na validação técnica acima, o charter WP1 deve:

1. tratar disponibilidade histórica, arquitetura OPC, sincronização temporal e volume de labels como condicionantes explícitas;
2. evitar percentagens de sucesso, falha ou redução de defeitos sem fonte verificável;
3. distinguir claramente entre:
	- factos confirmados;
	- requisitos pendentes de validação INCM;
	- resultados esperados sujeitos a execução e dados disponíveis.

---

## 8. Recomendações Objetivas

1. Validar com INCM a arquitetura OPC concreta: DA vs UA, PLCs, topologia, destino de dados.
2. Confirmar quando começa a existir histórico persistido e em que formato será entregue.
3. Fechar semântica das variáveis e origem das tags OK/NOK antes de qualquer conclusão analítica forte.
4. Definir o piloto HITwintag como método de recolha de labels, sem prometer volume ou qualidade estatística antes da execução.
5. Manter WP1 como fase de integração, consolidação, análise e validação operacional.

---

## Conclusão Final

✅ A proposta está tecnicamente bem orientada quando apresentada como faseada, dependente da qualidade dos dados e apoiada por validação operacional.

⚠️ Não é defensável, no estado atual, sustentar números exatos de sucesso, falha, ganho operacional ou precisão temporal universal sem fonte verificável e sem validação no contexto INCM.

✅ Recomendação: usar este documento como base factual e metodológica de suporte ao charter WP1.


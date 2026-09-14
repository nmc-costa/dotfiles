[Proposta] email 22072026

Caro Bruno,

No seguimento das nossas recentes reuniões sobre o projeto INCM-PreditSense, elaborámos uma proposta de planeamento das Work Packages (WP). Para que possamos assumir o compromisso de concluir a WP1 até 30 de novembro de 2026 (numa janela de execução de 3 meses, iniciando em setembro), delineámos uma estratégia realista e alinhada com as melhores práticas de projetos de inteligência artificial na indústria. Esta proposta reflete a complexidade técnica e a atual alocação de recursos para o projeto.

Alocação Estrita e Foco do Orçamento (Aviso de Risco): Gostaríamos de ser transparentes quanto ao dimensionamento do projeto para esta fase inicial. O budget de horas e recursos alocado para a WP1 até ao final de novembro é estrito e foi desenhado exclusivamente para o trabalho de Data Science, Análise e Visualização. Se for necessário redirecionar parte substancial deste esforço orçamentado para engenharia de infraestruturas redes e dados (como o levantamento, configuração e testes de comunicação do servidor OPC desde o zero), teremos de estender a janela temporal. Por isso, a clarificação atempada de responsabilidades nestas tarefas técnicas de base é urgente. A próxima reunião de quarta-feira deve servir para alinhamento concreto sobre este tema com a equipa de Engenharia de dados DAE do DTX.


Precedência Rigorosa (Stage-Gate): Gostaríamos de sublinhar que a execução deste projeto seguirá uma lógica estritamente sequencial. O avanço para qualquer Work Package seguinte só será possível e validado se a WP anterior estiver concluída com sucesso, a funcionar de forma estável e a apresentar os resultados esperados. Isto garante a viabilidade técnica e do negócio antes de comprometermos esforço em arquiteturas mais complexas.

Responsabilidade Partilhada e Conhecimento de Domínio (Fator Crítico de Sucesso): A nossa experiência em IA industrial demonstra que a simples partilha de extrações de dados não é suficiente para o sucesso do projeto. É fundamental um compromisso do lado da INCM em validar internamente os dados antes da entrega. Sem um pré-alinhamento e mapeamento das variáveis de real interesse pelo vosso conhecimento de domínio, o processo de Data Understanding forçará a nossa equipa a avançar "às cegas". Isto implicará múltiplos ciclos morosos de profiling de dados, sucessivas reuniões para decifrar anomalias estatísticas ou deslocações constantes a Lisboa para validação no terreno. Este cenário de exploração iterativa sem contexto prévio acarreta um risco elevado de fazer derrapar a janela temporal de 3 meses da WP1. A nossa recomendação é que a vossa equipa faça um alinhamento prévio no local, identificando as variáveis mais relevantes e as lacunas de conhecimento atuais, para que possamos iniciar o trabalho analítico já sobre uma base de informação maturada.


Abaixo apresentamos a estruturação estimada das fases e, de seguida, a nossa Matriz de Validação para formalizar os requisitos.


Planeamento Estruturado das Work Packages
WP1: Fundações de Dados, Servidor OPC e Monitorização Offline (3 meses: Setembro - Novembro 2026)

* Requisitos de Dados: Exportações substanciais de histórico (ex: vários meses em formato CSV/SQL ou equivalente) contendo todas as variáveis operacionais e ambientais, devidamente acompanhadas de um dicionário de dados claro (semântica). Para o setup do OPC, requer-se o mapeamento exato dos registers do PLC e topologia de rede. [comentários: Susana Cruz  [8h50]
Pelo que percebo isto já não é possível à partida pelo que falamos com eles na reunião em Julho. Eles disseram que têm acesso aos dados, mas não persistência, então só quando DAE terminar a sua parte é que começará a ser construído um histórico.
Nuno Da Costa  [12h39]
Sim, mas este requisito mantém-se. Só se for atingido é que depois é possivel o resto.]
* Data Acquisition (Histórico e Setup OPC): Recolha, extração e consolidação dos dados da máquina de selagem/laminagem e dos sensores ambientais (HVAC). Ponto Crítico: Como mencionaram a necessidade de criar um servidor de dados (OPC) para a extração, é imperativo detalhar exaustivamente os requisitos técnicos deste setup. Dado que a equipa de Engenharia de Dados (DAE) tem neste momento uma disponibilidade de recursos humanos muito limitada até novembro, precisamos de perceber com exatidão o esforço envolvido para podermos estimar o tempo de desenvolvimento. Esta avaliação ditará se é exequível a DTx assumir esta tarefa dentro dos 3 meses ou se terá de ficar a cargo da INCM. [Comentários: Bruno Sampaio  [11h55]
A INCM irá partilhar uma arquitetura de um projeto desenvolvido internamente.

Na reunião descreveram essa arquitetura como sendo um modelo de  Push Externo:
1.  Cliente Interno:  Um serviço alojado na rede local acede ao servidor OPC.
2.  Encriptação e Transferência:  Os dados são encriptados localmente.
3.  Endpoint Externo:  O cliente interno inicia a comunicação para um  endpoint
seguro (Web Server) da equipa de desenvolvimento.Susana Cruz  [8h57]
Julgo que aqui (na Data Acquisition) seria pertinente adicionar também a hipótese discutida com eles de assim que começarem a ser guardados os dados, definir um período (este pode depender da disponibilidade deles, mas idealmente deveria estar ligado à frequência de falhas ou defeitos, para podermos ter uma boa cobertura pelo menos das ocorrências mais comuns) de anotação manual de falhas num tablet pelo(s) operador(es) deles. Pelo que percebi o esforço adicional de parte deles é relativamente baixo (umas vez que as falhas são pouco frequentes e a marcação seria acessível e rápida) e para nós seria extremamente valioso para a compreensão dos dados e do problema (editado) 
Nuno Da Costa  [12h44]
Sim, aqui entra a ferramenta que desenvolvi: https://github.com/nmc-costa/HITtwintag]
* Data Understanding & Profiling: Análise exploratória aprofundada aos dados extraídos. Com base no vosso contexto de domínio pré-fornecido, este passo ditará o que é efetivamente viável fazer cientificamente. Avaliaremos a qualidade temporal, os hiatos e a coerência entre as variáveis operacionais e ambientais. [comentários: Nuno Da Costa  [12h52]
Do @Bruno Sampaio
"Seria interessante dentro do Data Understanding & Profiling: ter uma analise dos dados, para tirar conclusões do género:

dados insuficientes, é necessário mais sensores, e em que zonas (nas máquinas, nos tapetes rolantes etc, fora das máquinas para descartar interferências, ex: vibração externa etc...)
dados irrelevantes, reposicionar sensores exitentes...
" (editado) 
Susana Cruz  [9h07]
Teoricamente seria sem dúvida interessante ter essa análise. No contexto concreto que temos, porém, julgo que os sensores existente são internos da própria máquina e está fora do âmbito discutir a sensorização e propor alterações da mesma. Devemos focar-nos em dados suficientes ou insuficientes e irrelevantes e mesmo para isso, precisamos de envolvimento activo deles com conhecimento de domínio e uma boa definição dos objectivos (para saber se os dados são adequados precisamos de saber muito bem qual o objectivo que se pretende atingir com eles a longo prazo. Detecção de falhas? Quais? Em que momento? Manutenção Preditiva? De que componentes? Qual o ciclo de vida dos mesmos? Etc.)]
* Data Presentation (Dashboard Offline): Criação de um dashboard funcional com base no histórico consolidado. Sendo altamente arriscado tentar uma análise online fiável nesta fase (devido à imaturidade natural dos dados iniciais e restrições de infraestrutura), este protótipo offline servirá para demonstrar imediatamente a utilidade da visualização de dados, validando os KPIs e o cruzamento visual entre defeitos e anomalias térmicas. [comentários: Bruno Sampaio  [11h49]
Depende muito da conectividade entre a máquina que vamos ter acesso e o pc/tablet que vai ficar na fábrica
Uma alternativa seria ter na fábrica um cliente hospedado no pc que lê as métricas do opc server e as envia para uma base de dados sendo posteriormente apresentado sobre a forma de um html estático.

O ideal seria deixar a apresentação dos dados quando existir  acesso á rede na fábrica. (editado) 
Nuno Da Costa  [12h05]
Exato.

Inicialmente vou só partilhar um anotador que criei para extrair o feedback de operadores em linhas industriais para termos uma melhor representação do que se passa na linha.

Mais logo envio por email. (editado) 
Bruno Sampaio  [12h09]
esse anotador pretende armazenar esse conteúdo localmente, e só com transferência manuel é que temos acesso a essas informações correto?
Nuno Da Costa  [12h13]
Sim, neste momento é o mais manual possivel e rápido, para ver se no local eles conseguem extrair conhecimento de dominio. Ou mesmo quando formos lá.

Eu daqui a pouco já partilho.

Vai claramente depender se querem ou não usar.
Vou lhes pedir só feedback e se conseguem utilizar.Bruno Sampaio  [12h15]
certo :+1:
Susana Cruz  [9h11]
Mas o anotador não tem nada a ver com a Data Presentation, certo? Penso que está relacionado com a Data Acquisition apenas. Esta visualização seria desenvolvida por que equipa (DAE ou DSML)?
Nuno Da Costa  [12h52]
Podemos usar como base o HITtwintag de Data aquisition e adicionar blocos de "Data Presentation" sobre a maquina que está a ser retirado o output, ou melhor, colocar uma estação de report virtual na linha que ao clicar mostra os resultados .

Mas sim, não tem de ser exatamente igual nem precisa de ser utilizado o HITwintag

Eu diria que esta tarefa de "Data Presentation" ficaria do lado de DAE: @Ricardo Rodrigues?? Do lado DSML nós criamos os algoritmos para fazer o output dos resultados, depois voces trantam da interface e como será aprensentada.]

WP2: Alarmística, Tempo Real e Aprendizagem Contínua (Estimativa: 8 a 12 meses)

* Requisitos de Dados: Fluxo contínuo e estável de dados em tempo real (via infraestrutura OPC estabelecida na WP1) e a geração ativa de uma matriz de labels (classificação de defeitos) alimentada diariamente pelos operadores no chão de fábrica. [comentários: Susana Cruz  [9h13]
Podemos enquadrar a anotação manual no WP1 como uma espécie de "piloto" para iterar e chegar a uma versão madura e adequada para depois alimentar durante um período longo e criar um histórico.]
* Integração Online e Arquitetura de Dados: Transição do dashboard da WP1 para tempo real, tirando partido da infraestrutura OPC (implementada e testada na WP1) para estabelecer uma ligação contínua.
* Human-in-the-loop: Implementação de mecanismos de feedback dos operadores no chão de fábrica. Desenvolvido também pela equipa de DAE.
* Manutenção Alarmística: Criação de modelos reativos/estatísticos de deteção de anomalias para gerar alertas antecipados aos operadores de linha. Usando o feedback do human-in-the-loop.
* Continuous Learning com Agentes: Implementação de mecanismos em que agentes inteligentes ajustam os parâmetros dos modelos com base nos novos dados online e na classificação contínua de defeitos.

WP3: Prototipagem Avançada para Manutenção Preditiva (Estimativa: 8 a 12 meses)

* Requisitos de Dados: Uma base de dados madura e extensa, rica em anomalias categorizadas (recolhidas durante a WP2), que contenha o ciclo completo de degradação dos componentes da máquina para permitir o treino de modelos de previsão de vida útil.
* Manutenção Preditiva: Desenvolvimento do modelo final preditivo. Utilização de Machine Learning avançado sobre o histórico e os dados em tempo real (consolidados na WP2) para antecipar falhas sistémicas na laminação/selagem antes que estas resultem em refugo.

Matriz de Validação e Requisitos
O sucesso e o scope dos casos de uso (não-supervisionados vs. supervisionados) estão estritamente amarrados à taxonomia atual dos vossos dados e infraestrutura.
Esta tabela reflete o nosso entendimento atual. Pedimos que validem a coluna central e preencham a coluna da direita com o maior nível de detalhe possível. Este documento servirá como formalização contínua de requisitos e bússola de projeto.




Categoria
	Parâmetro / Tópico
	O que assumimos (O nosso entendimento atual)
	Validação INCM / Lacuna a Preencher (Por favor, detalhar)

Negócio
	Objetivo Principal
	Redução de refugo via protótipo de Manutenção Preditiva (WP3).
	[Confirmar ou detalhar requisitos funcionais/não-funcionais]

Negócio
	Prazo WP1
	30 de Novembro 2026 (Fase Offline baseada em histórico/extrações).
	[Confirmar aceitação da dependência da qualidade dos dados entregues, do vosso conhecimento de domínio e da lógica de precedência para WPs seguintes]

Equipa
	Conhecimento de Domínio
	A INCM fará o mapeamento interno e validação prévia de quais as variáveis operacionais com mais impacto antes da extração de dados.
	Vital: Quem será o nosso Ponto de Contacto técnico (SME - Subject Matter Expert) para dúvidas de engenharia/processo durante as iterações da WP1?

Infraestrutura
	Máquina Alvo
	Máquina de selagem/laminagem (fim do processo).
	[Confirmar se existem restrições de rede ou de hardware para aceder aos PLCs desta máquina]

Infraestrutura
	Sensores Ambientais
	4 sensores (Temp/Humidade) na última sala.
	Onde estão localizados exatamente? (Ex: teto, perto do AVAC, distância à câmara de selagem?)

Arquitetura
	Setup do Servidor OPC
	A extração de dados na WP1 requer integração/criação de um servidor OPC para comunicação com a máquina.
	Decisão Crítica (Restrição de RHs): Quais as especificações técnicas exatas (OPC DA/UA, PLCs envolvidos, topologia, BD destino)? Face à forte limitação de recursos da nossa equipa de redes (DAE DTX) até novembro, precisamos do mapeamento exato para estimar as horas de desenvolvimento necessárias e decidir de quem será a responsabilidade da sua implementação.

Dados
	Sincronização Temporal (Timestamps)
	Antevemos que os PLCs da máquina e os sensores da sala não partilhem o mesmo relógio exato (ao milissegundo).
	Vital: Qual é a verdadeira precisão temporal entre estes sistemas e as taxas de amostragem? Como planeiam garantir o alinhamento? Existem eventos partilhados que sirvam para forçar a sincronização?

Dados
	Fontes Adicionais
	Conhecemos apenas os dados da máquina referida e os 4 sensores da sala.
	Existem mais sensores ou dados relevantes para o processo (ex: pressão, vibração, consumos energéticos, tempo de ciclo) que possam ser extraídos nesta fase?

Dados
	Dicionário de Variáveis
	Variáveis base identificadas: Estados, Alarmes, Temperatura, JobName ?
	Semântica: O que significa cada estado e cada JobName? Em que passo exato do ciclo a máquina atinge o pico térmico de prensagem? Quais consideram ser as variáveis com maior impacto na qualidade?

Dados
	Tags de Qualidade
	Existência da flag "OK / NOK" (Refugo). Outras Flags?
	Origem: O NOK é gerado por inspeção visual humana posterior ou há algum sensor de rejeição na própria máquina? O que significa este OK/NOK, ou seja, rejeita o quê?

Dados
	Labeling (Defeitos)
	Casos de uso específicos exigem labeling exato; sem ele, faremos apenas casos extremos (anomalias cegas não-supervisionadas).
	Capacidade: Têm histórico que categorize o tipo de NOK (Ex: Bolha, Desalinhamento)? Qual a capacidade da equipa INCM para classificar (fazer o labeling) de anomalias ativamente no futuro? Será só na dashboard para feedback do operador? Só na WP2?




Ficamos a aguardar a vossa devolução desta tabela preenchida para consolidarmos definitivamente o plano e avançarmos com segurança e máxima eficiência para o project charter para depois ser enviado e assinado o projeto entre as duas partes.

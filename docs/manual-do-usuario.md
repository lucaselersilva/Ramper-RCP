# Manual do usuário — Dashboard Ramper Pipeline (RCP Advogados)

Este documento explica, em linguagem simples, o que é o dashboard, o que cada
número significa, e como ele deve ser usado no dia a dia da gestão comercial
do escritório. Não é necessário nenhum conhecimento técnico para lê-lo.

---

## 1. O que é este dashboard (e o que ele não é)

O dashboard é uma **visão de leitura e análise** sobre os dados que já estão
no CRM (Ramper Pipeline). Ele mostra, de forma organizada, o que está
acontecendo com as oportunidades comerciais do escritório: quantos leads
entram, em que etapa estão, quem está cuidando de cada um, quais estão
paradas, e assim por diante.

O que ele **não é**:

- Não substitui o CRM. Registrar uma tarefa, mudar a etapa de uma
  oportunidade, escrever uma nota — tudo isso continua sendo feito no CRM,
  não aqui.
- Não é editável. O dashboard só exibe e filtra o que já foi registrado; não
  é possível alterar nenhuma oportunidade, tarefa ou nota por ele.
- Não é em tempo real. Os dados são atualizados uma vez por dia (ver seção
  2) — o que você vê aqui é a "foto" do CRM na última atualização, não o
  segundo a segundo.

## 2. De onde vêm os dados e quando são atualizados

Os dados vêm diretamente do CRM Ramper Pipeline e são atualizados
automaticamente **todos os dias de manhã**. No topo da página, ao lado do
logo, sempre aparece a data e hora da última atualização.

Se essa atualização estiver muito atrasada (mais de ~30 horas), um aviso em
vermelho aparece nesse mesmo local. Nesse caso, não é preciso fazer nada
tecnicamente — basta avisar quem cuida da manutenção do dashboard (veja a
seção 9) ou aguardar a próxima atualização automática.

## 3. Como usar os filtros

Os filtros ficam no topo da página, logo abaixo do cabeçalho, e valem para
(quase) tudo o que aparece na tela — cartões, gráficos, recomendações e
tabelas reagem juntos, na hora, sempre que um filtro muda.

- **Período** — escolha um intervalo pronto (últimos 7/30/90 dias, 6/12
  meses) ou um período personalizado. Filtra pela data em que a oportunidade
  entrou no funil (ou, no caso das tarefas, pela data da tarefa).
- **Responsável** — mostra só as oportunidades e tarefas de uma pessoa da
  equipe.
- **Etapa do funil** — mostra só as oportunidades que estão numa etapa
  específica.
- **Área do direito** — mostra só as oportunidades de uma prática jurídica
  específica (ex.: Trabalhista, Cível, Tributário).
- **Buscar em tarefas e notas** — procura um texto dentro da descrição das
  tarefas e do histórico de interações das oportunidades.

Todos os filtros podem ser combinados ao mesmo tempo, e o botão **"Limpar
filtros"** volta tudo ao estado padrão (todo o período, sem filtro de
responsável/etapa/área).

**Atenção com o filtro de Período**: nem todo número do dashboard reage a
ele. A seção 4 explica exatamente quais reagem e quais não.

## 4. Seção por seção

### Visão geral

Esta seção está dividida em **dois grupos**, porque respondem perguntas
diferentes — essa é a mudança mais importante deste manual, então vale ler
com atenção:

| Indicador | O que significa | Grupo |
|---|---|---|
| Novos leads | Quantas oportunidades entraram no funil no período escolhido | **No período selecionado** |
| Taxa de conversão | % de oportunidades ganhas entre as que fecharam (ganhas + perdidas) no período | **No período selecionado** |
| Tarefas atrasadas | Tarefas não concluídas cuja data já passou, no período | **No período selecionado** |
| Tarefas pendentes (total) | Tarefas ainda não concluídas, no período | **No período selecionado** |
| Oportunidades com notas | Oportunidades que têm algum histórico de interação registrado, no período | **No período selecionado** |
| Oportunidades abertas | Quantas oportunidades estão abertas **agora**, no pipeline inteiro | **Retrato do pipeline hoje** |
| Pipeline parado (>90 dias sem mudança) | Das oportunidades abertas, quantas não têm nenhuma mudança de etapa há mais de 90 dias | **Retrato do pipeline hoje** |

**Por que "Oportunidades abertas" não muda quando eu troco o período?**
Porque ela não é uma métrica "do período" — é uma fotografia de todo o
pipeline aberto no exato momento da última atualização. Faz sentido: se uma
oportunidade entrou há 8 meses e continua aberta hoje, ela deve continuar
contando como "aberta" mesmo que você filtre "últimos 30 dias". Trocar o
período muda o que aconteceu *naquela janela de tempo* (novos leads,
fechamentos, tarefas); não muda a foto de *como o pipeline está agora*. Os
filtros de Responsável, Etapa e Área do direito continuam funcionando
normalmente sobre esse número — só o período é ignorado, de propósito.

### Recomendações

Uma lista de alertas e sugestões geradas **automaticamente** a partir dos
dados filtrados — não é opinião de ninguém, cada recomendação sempre cita o
número que a embasa. Elas aparecem ordenadas por gravidade (críticas
primeiro), e por padrão só as mais importantes ficam visíveis; um botão
**"Ver mais"** revela o restante. Quando uma recomendação tem uma
explicação mais longa do porquê ela importa, um link **"por quê?"** abre
esse detalhe sem poluir a leitura rápida.

| Tipo de recomendação | O que fazer a respeito |
|---|---|
| Pipeline parado (muitas oportunidades sem mudança há +90 dias) | Fazer uma triagem: arquivar como "Inativa" as sem potencial, reengajar as prioritárias |
| Tarefas atrasadas em volume alto | Reduzir o atraso antes de agendar tarefas novas |
| Atraso concentrado num responsável | Revisar prioridades ou redistribuir parte da carteira dessa pessoa |
| Campo mal preenchido (origem, área do direito, UF, segmento) | Cobrar o preenchimento já na criação da oportunidade no CRM |
| Gap de conversão entre áreas ou entre responsáveis | Entender o que funciona melhor num lado e testar no outro |
| Queda na geração de novos leads | Reforçar a prospecção |
| Poucas reuniões registradas perto do volume de leads | Padronizar o registro de reuniões como tarefa no CRM |

### Pipeline: leads → reuniões → fechamentos

São os 3 números que a gestão pediu para acompanhar juntos: quantos leads
entraram, quantas reuniões foram marcadas e quantos fechamentos aconteceram
no período. "Reuniões marcadas" só conta tarefas do tipo **"Reunião Com"**
(reunião com cliente/prospect); reuniões internas da equipe não entram
nessa conta. As taxas mostradas na tabela são sempre calculadas **sobre o
total de leads**, nunca uma etapa sobre a outra — isso evita que apareça
uma taxa de "conversão" acima de 100%, já que nem todo fechamento passou
por uma reunião que foi de fato registrada como tarefa.

### Evolução mensal do pipeline

Duas formas complementares de olhar o histórico mês a mês:

- **Coortes por mês de entrada** — para os leads que entraram em cada mês,
  mostra a situação deles *hoje*: quantos continuam abertos, quantos foram
  ganhos, quantos foram perdidos.
- **Comparativo mês a mês** — novos leads, reuniões e fechamentos lado a
  lado por mês, incluindo um comparador que deixa em verde o que melhorou e
  em vermelho o que piorou entre dois meses escolhidos.

Um pico de fevereiro de 2025 (de uma importação em massa de dados antigos
para o CRM) é tratado separadamente nas análises para não distorcer a
leitura da tendência real.

### Funil de vendas

Mostra quantas oportunidades estão em cada etapa do funil, com "Ganhas" e
"Perdidas" destacadas por serem o resultado final.

### Performance da equipe

Volume de oportunidades e produtividade em tarefas, por responsável.
**Atenção**: aqui aparece um número chamado **"Aberta no período"**, que é
diferente do "Oportunidades abertas" da Visão geral — este conta, entre as
oportunidades que *entraram* no período escolhido, quantas *continuam*
abertas hoje. Já o da Visão geral olha o pipeline inteiro, sem se importar
com quando cada oportunidade entrou. São dois recortes legítimos e
diferentes do mesmo conceito — por isso os nomes agora são diferentes.

### Cadência de resposta

Mede a velocidade de reação do time: quantos dias, em mediana, levam entre
a criação do lead e a primeira tarefa registrada nele — no geral e por
responsável — além do percentual de leads que nunca receberam nenhuma
tarefa.

### Perfil dos leads

Distribuição das oportunidades por origem, área do direito, estado (UF) e
segmento do cliente, sempre considerando apenas as oportunidades do período
filtrado que têm aquele campo preenchido. Cada gráfico informa o próprio
percentual de preenchimento, para deixar claro quando a amostra é pequena.

### Contas sem atividade recente

Organizações com uma oportunidade aberta, mas sem nenhuma tarefa, nota ou
mudança de etapa há mais de **60 dias** — candidatas a "conta esquecida".
É uma visão por *organização*, diferente do "Pipeline parado" da Visão
geral, que olha por *oportunidade* e usa um prazo de 90 dias.

### Tarefas

Tabela paginada com todas as tarefas do período (e demais filtros)
aplicados, incluindo tipo, responsável, descrição e status.

### Notas das oportunidades

"Notas" é o histórico de interações registrado na própria oportunidade
(e-mails, ligações etc.) — um campo diferente do fluxo de tarefas
agendadas.

### Exportar para CSV

Praticamente todo gráfico e toda tabela principal tem um botão **"Exportar
CSV"**, que gera o arquivo na hora, já com os filtros atuais aplicados (a
exportação de tabelas paginadas inclui todas as linhas do filtro, não só a
página visível na tela). O arquivo abre corretamente no Excel em
português.

## 5. Glossário

- **Oportunidade** — um lead/negócio dentro do funil comercial. Não existe
  um cadastro separado de "lead": toda oportunidade É um lead, do momento em
  que entra até fechar.
- **Etapa do funil** — a fase em que a oportunidade está. Ordem das etapas:
  Prospecção/Qualificação → Proposta Comercial → Negociação → Reunião →
  Contrato → Possível Cotação → (etapas de licitação, quando aplicável) →
  **Ganha** ou **Perdida**.
- **Ganha** — oportunidade fechada com sucesso (cliente fechou negócio).
- **Perdida** — oportunidade que não avançou e foi encerrada sem fechar.
- **Inativa** — oportunidade arquivada (não tem mais potencial de avançar);
  não entra nas contagens de pipeline aberto.
- **Área do direito** — a prática jurídica da oportunidade (ex.:
  Trabalhista, Cível, Tributário, Regulatório).
- **Origem da oportunidade** — por onde aquele lead chegou (ex.: Prospecção
  Ativa, Indicação, Site, Network).
- **Cadência de resposta** — tempo entre o lead entrar e receber a primeira
  tarefa registrada.
- **Pipeline parado** — oportunidade aberta sem mudança de etapa há mais de
  90 dias.
- **Conta sem atividade recente** — organização com oportunidade aberta e
  sem nenhuma atividade (tarefa, nota ou mudança de etapa) há mais de 60
  dias.
- **Reunião Com** vs. **Reunião Interna** — a primeira é uma reunião com
  cliente/prospect e conta nas métricas de pipeline; a segunda é uma
  reunião interna da equipe e não conta.
- **Nota / Histórico** — registro de interação (e-mail, ligação etc.) feito
  diretamente na oportunidade, fora do fluxo de tarefas agendadas.

## 6. Como isso é usado para gestão

**Cadência sugerida de revisão:**

- **Semanal**: tarefas atrasadas, pipeline parado (fazer a triagem indicada
  pelas Recomendações), contas sem atividade recente.
- **Mensal**: evolução mensal do pipeline, taxa de conversão por área e por
  responsável, tendência de geração de novos leads.

**O que se espera de cada responsável comercial:**

- Preencher a área do direito e a origem da oportunidade já na criação, no
  CRM — sem isso, boa parte das análises deste dashboard fica incompleta.
- Registrar toda reunião externa como tarefa do tipo "Reunião Com" — é a
  única forma do dashboard enxergar essa etapa do funil.
- Tratar oportunidades paradas: arquivar as sem potencial, reengajar as que
  ainda fazem sentido.

**O que se espera da gestão:**

- Revisar as Recomendações periodicamente — elas já apontam onde olhar
  primeiro.
- Olhar a tendência (evolução mensal, cadência) e não só a foto do dia.
- Usar Performance da equipe e Cadência de resposta para orientar a equipe,
  não para punir — os números têm contexto (carteira, período de férias,
  tipo de cliente) que o dashboard sozinho não captura.

## 7. Perguntas frequentes

**Por que "Oportunidades abertas" não muda quando eu troco o período?**
Porque é uma fotografia do pipeline inteiro agora, não uma métrica do
período — ver explicação completa na seção 4, "Visão geral".

**Por que existem dois números diferentes chamados "aberta"?**
"Oportunidades abertas" (Visão geral) é a foto de todo o pipeline aberto
hoje, sem olhar quando cada oportunidade entrou. "Aberta no período"
(Performance da equipe) é sobre a leva de oportunidades que *entrou* no
período escolhido e ainda está aberta hoje. São recortes diferentes do
mesmo conceito — por isso agora têm nomes diferentes, para não confundir.

**Os dados estão desatualizados, o que eu faço?**
Veja a data no topo da página. Se estiver há mais de ~30h sem atualizar,
avise quem cuida da manutenção do dashboard (seção 9) — a atualização é
automática e diária, então normalmente se resolve sozinha na próxima
rodada.

**Posso editar alguma coisa por aqui?**
Não. Qualquer alteração (etapa, tarefa, nota) precisa ser feita direto no
CRM Ramper Pipeline; o dashboard só reflete o que está lá.

## 8. Como gerar um PDF do dashboard

O botão **"Gerar PDF / Imprimir"**, no canto superior direito, gera um
relatório executivo pronto para salvar ou enviar por e-mail, com os filtros
atualmente aplicados. Para manter o relatório enxuto, as tabelas
operacionais (Tarefas, Notas, Contas sem atividade recente) ficam de fora
do PDF — para o detalhe linha a linha, use a exportação em CSV de cada
tabela (seção 4).

## 9. Onde tirar dúvidas

Dúvidas sobre os números ou sugestões de melhoria no dashboard: falar com
quem cuida da manutenção do dashboard no escritório.

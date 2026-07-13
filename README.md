# Dashboard Ramper Pipeline

Solução 100% local (sem servidor, sem banco de dados) para extrair dados da
API do Ramper Pipeline (lscrm) e visualizá-los num dashboard HTML interativo.

## Estrutura do projeto

```
ramper-dashboard/
├── .env                          # token da API (nunca versionar)
├── .gitignore
├── extract.py                    # script de extração (Python, só stdlib)
├── Atualizar Dados.command       # duplo clique: extrai e abre o dashboard na hora
├── data/                         # gerado por extract.py
│   ├── opportunities.json
│   ├── tasks.json
│   ├── organizations.json
│   ├── persons.json
│   ├── users.json
│   ├── stages.json
│   ├── pipes.json
│   ├── dashboard_data.js         # bundle usado pelo dashboard.html
│   └── last_sync.json            # timestamp/resumo da última extração
├── dashboard.html                # abrir direto no navegador
├── assets/
│   └── logo-rcp.jpg              # logo do RCP Advogados, usado no cabeçalho
├── docs/
│   └── api-endpoints-descobertos.md
├── launchd/
│   └── com.ramper.dashboard.extract.plist   # template de agendamento (macOS)
├── logs/                         # logs do agendamento (gerado no 1º run)
└── README.md
```

## 1. Configuração inicial

O token já está salvo em `.env` (`RAMPER_API_TOKEN`). Não é necessário
instalar nenhuma dependência — `extract.py` usa só a biblioteca padrão do
Python 3 (`urllib`, `json`, etc.), então basta ter Python 3 instalado
(já confirmado: `/usr/bin/python3`, versão 3.9.6).

**Nunca** commite o arquivo `.env` — ele já está no `.gitignore`, assim como
a pasta `data/` (que contém dados reais de clientes/oportunidades) e `logs/`.

## 2. Atualizando os dados na hora (sem esperar o agendamento diário)

Forma mais simples: dê **duplo clique em `Atualizar Dados.command`**, na pasta
do projeto. Uma janela de Terminal abre, roda a extração e, ao final, abre o
dashboard sozinha com os dados novos (se o dashboard já estiver aberto em
outra aba, dê F5 nela para recarregar). Esse mesmo lembrete aparece no botão
"Como atualizar os dados agora", no canto superior direito do dashboard.

Na primeira vez, o macOS pode bloquear o arquivo por vir de fora da App
Store — clique com o botão direito nele, escolha "Abrir" e confirme uma vez;
depois disso, duplo clique normal funciona.

Ou, se preferir rodar pelo terminal diretamente:

```bash
cd "/Users/lucaseler/LJ Labs/Projetos/Ramper - Dashboard"
python3 extract.py
```

O script:
- Lê o token de `.env`.
- Busca todos os registros de `opportunities`, `tasks`, `organizations`,
  `persons`, `users`, `stages` e `pipes`, paginando em blocos de 200.
- Tenta cada requisição até 3 vezes (com 3s de espera entre tentativas) em
  caso de erro de rede.
- Salva cada entidade em `data/<entidade>.json`.
- Gera `data/dashboard_data.js`, que é o arquivo que o dashboard realmente lê
  (ver seção 4 sobre por que isso é necessário).
- Salva `data/last_sync.json` com data/hora da extração e um resumo de
  quantos registros foram baixados por entidade (e eventuais erros).

Se a extração falhar para alguma entidade, o script termina com código de
saída 1 e imprime o erro — as demais entidades que deram certo são salvas
normalmente.

## 3. Abrindo o dashboard

Basta dar duplo clique em `dashboard.html` (ou abrir pelo navegador,
`Arquivo > Abrir`). Não precisa de servidor nem internet para os dados —
só a biblioteca de gráficos (Chart.js) é carregada via CDN, então é
necessário estar conectado à internet para os **gráficos** aparecerem
(cards e tabela funcionam mesmo offline).

O dashboard mostra, no topo, a data/hora da última extração. Se fizer mais
de ~30h desde a última sincronização, aparece um aviso em vermelho — nesse
caso, use o `Atualizar Dados.command` (seção 2) e recarregue a página (F5).

### Filtros disponíveis (todos client-side, atualizam na hora)

- **Período**: presets (7/30/90 dias, 6/12 meses, todo o período) ou
  personalizado. Filtra oportunidades pela data de criação (`added_in`) e
  tarefas pela data do evento (`event_time`, ou data de criação se não
  houver evento agendado).
- **Responsável**: filtra por vendedor/usuário do CRM.
- **Etapa do funil**: filtra oportunidades (e o gráfico de funil) por etapa.
- **Área do direito**: filtra por prática jurídica (campo customizado da
  oportunidade).
- **Buscar em tarefas e notas**: busca por texto na descrição da tarefa e
  no histórico/nota da oportunidade.

Todos os cards, gráficos, a lista de recomendações e as tabelas de tarefas
e notas reagem aos filtros combinados.

### Seções do dashboard

- **Visão geral**: KPIs principais (leads, taxa de conversão, pipeline
  aberto/parado, tarefas atrasadas/pendentes, oportunidades com notas).
- **Recomendações**: sugestões geradas por regras sobre os dados filtrados
  (pipeline parado, concentração de atrasos por responsável, queda na
  geração de leads, campos mal preenchidos, gaps de conversão por área/
  responsável) — cada uma cita o número que a embasa. A lógica está em
  `computeRecommendations()`, dentro do `<script>` do `dashboard.html`.
- **Pipeline: leads → reuniões → fechamentos**: os 3 números que a gestão
  pediu para acompanhar juntos. "Reuniões marcadas" conta oportunidades com
  ao menos uma tarefa do tipo `Reunião Com` vinculada (reuniões internas
  não entram); "Fechamentos" são as oportunidades ganhas no período. As
  taxas na tabela são sempre em relação aos leads (evita taxa de "conversão"
  acima de 100%, já que nem todo fechamento passou por uma reunião logada
  como tarefa — ver a recomendação sobre isso). Também mostra reuniões por
  responsável.
- **Funil de vendas**, **Performance da equipe**, **Perfil dos leads**:
  gráficos com botão "Ver tabela" para os números exatos.
- **Tarefas** e **Notas das oportunidades**: tabelas paginadas e filtráveis.
  "Notas" é o campo `history` da API — o histórico de interações registrado
  na oportunidade (e-mails, ligações etc.), separado do fluxo de tarefas
  agendadas.

## 4. Por que existe `dashboard_data.js` além dos `.json`?

Ao abrir um arquivo HTML direto do disco (`file://`), o Chrome e outros
navegadores bloqueiam `fetch()`/`XMLHttpRequest` para arquivos locais por
política de CORS — ou seja, o dashboard não conseguiria ler
`data/opportunities.json` diretamente. A solução sem precisar de servidor é
o `extract.py` gerar um arquivo `.js` com os dados já embutidos
(`window.RAMPER_DATA = {...}`), carregado via `<script src="data/dashboard_data.js">`
normal — isso não sofre a restrição de CORS. Os arquivos `.json` continuam
sendo salvos separadamente para inspeção manual/debug.

## 5. Agendamento diário automático (macOS)

Duas opções: `launchd` (recomendado no macOS) ou `cron`.

### Opção A — launchd (recomendado)

Um template já está pronto em `launchd/com.ramper.dashboard.extract.plist`,
configurado para rodar todo dia às 7h. Para instalar:

```bash
cp "/Users/lucaseler/LJ Labs/Projetos/Ramper - Dashboard/launchd/com.ramper.dashboard.extract.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.ramper.dashboard.extract.plist
```

Para conferir se está carregado:

```bash
launchctl list | grep com.ramper.dashboard.extract
```

Os logs de cada execução vão para `logs/extract.log` e
`logs/extract.error.log` dentro do projeto.

Para mudar o horário, edite o bloco `StartCalendarInterval` no `.plist`
(chaves `Hour`/`Minute`, formato 24h) antes de copiar, ou edite a cópia em
`~/Library/LaunchAgents/` e rode:

```bash
launchctl unload ~/Library/LaunchAgents/com.ramper.dashboard.extract.plist
launchctl load ~/Library/LaunchAgents/com.ramper.dashboard.extract.plist
```

Para desativar o agendamento:

```bash
launchctl unload ~/Library/LaunchAgents/com.ramper.dashboard.extract.plist
rm ~/Library/LaunchAgents/com.ramper.dashboard.extract.plist
```

### Opção B — cron

Alternativa mais simples, se preferir. Rode `crontab -e` e adicione a linha
(roda todo dia às 7h):

```
0 7 * * * /usr/bin/python3 "/Users/lucaseler/LJ Labs/Projetos/Ramper - Dashboard/extract.py" >> "/Users/lucaseler/LJ Labs/Projetos/Ramper - Dashboard/logs/extract.log" 2>&1
```

(No macOS moderno, o cron pode pedir permissão de "Full Disk Access" para o
`cron`/`Terminal` em Ajustes do Sistema > Privacidade e Segurança.)

## 6. Adicionando novos campos ou filtros no futuro

- **Novo campo de uma entidade já extraída**: os JSONs em `data/` já trazem
  o registro completo retornado pela API (inclusive `additional_values` com
  campos customizados). No `dashboard.html`, dentro da tag `<script>`, use o
  campo diretamente (ex.: `o.additional_values.opportunities.origem_da_oportunidade`).
- **Novo filtro**: adicione um `<select>`/`<input>` na `.filters` do HTML,
  leia o valor dele dentro de `getFilters()`, e use esse valor dentro de
  `filteredOpportunities()` / `filteredTasks()`.
- **Nova entidade da API**: adicione o endpoint em `ENTITIES` no topo de
  `extract.py` — ele será extraído, salvo em `data/<nome>.json` e incluído
  automaticamente em `dashboard_data.js` (acessível como
  `window.RAMPER_DATA.<nome>` no dashboard).
- Detalhes de sintaxe de filtro/ordenação da API (o que funciona e o que
  não funciona) estão documentados em `docs/api-endpoints-descobertos.md`.

## 7. Testando o fluxo do zero

```bash
cd "/Users/lucaseler/LJ Labs/Projetos/Ramper - Dashboard"
rm -rf data
python3 extract.py
open dashboard.html
```

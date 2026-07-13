# Endpoints descobertos — API Ramper Pipeline (lscrm)

Testado em: 2026-07-13
Base URL: `https://api.lscrm.com.br/v1/`
Autenticação: header `access-token: {TOKEN}`

## Endpoints que funcionam (200 OK)

| Endpoint | Total de registros (na data do teste) | Observações |
|---|---|---|
| `GET /opportunities` | 913 | Oportunidades do funil de vendas |
| `GET /tasks` | 901 | Tarefas |
| `GET /organizations` | 1019 | Empresas/contas |
| `GET /persons` | 1070 | Contatos/pessoas (não é `/people`) |
| `GET /users` | 9 | Usuários/vendedores do CRM |
| `GET /stages` | 14 | Etapas do funil |
| `GET /pipes` | 1 | Funis (apenas "Funil padrão") |

## Endpoints testados que NÃO existem (404)

`/organization`, `/people`, `/person`, `/contacts`, `/contact`, `/task`,
`/pipelines`, `/pipeline`, `/pipe`, `/stage`, `/user`, `/leads`, `/lead`,
`/activities`, `/activity`, `/notes`, `/note`, `/loss_reasons`, `/loss_reason`,
`/funnels`, `/funnel`, `/organizations_persons`, `/org_persons`

## Parâmetros de query confirmados

- **Paginação**: `page` e `limit`. Se `limit` for maior que o total de registros, a API retorna todos os registros de uma vez (ex.: `limit=1000` com 913 registros retorna `limit:913` e todos os itens). Ainda assim, o script pagina em blocos de 200 por segurança.
- **Ordenação**: o formato `order=campo,direção` (citado na doc oficial) **não funciona** — sempre retorna em ordem ascendente por padrão. O formato que realmente funciona é `order[campo]=asc|desc`, por exemplo `order[id]=desc`.
- **Filtros**: `filters[campo][operador]=valor` funciona para igualdade, ex.: `filters[stage_id][equal]=1` (testado e confirmado, retornou só oportunidades da etapa 1).
  - Operadores de comparação de data (`>=`, `gte`, `greater_equal`) **não funcionaram** nos testes (sempre retornaram total 0), então não usamos filtro de data server-side.
  - **Decisão de arquitetura**: como os volumes são pequenos (centenas a ~1000 registros por entidade), o script de extração baixa todos os registros de cada entidade e todo o filtro (data, responsável, etapa) é feito no navegador, client-side, no dashboard. Isso também atende ao requisito de filtros instantâneos sem re-rodar o script.

## Estrutura de campos por entidade

### `/opportunities`
Campos principais: `id`, `title`, `user_id` (responsável), `organization_id`, `person_id`, `stage_id`, `stage_last_change`, `value`, `close_in`, `history` (texto livre), `loss_reason_id`, `added_in` (data de criação), `updated_in`.

Objetos aninhados:
- `stages`: `{id, name_short, background, type (open/win/loss), pipe_id, pipe_name}`
- `organizations`: `{id, name, address, document, phone}`
- `organizations_first_person`: `{id, name, email, phone, linkedin, cargo}`
- `users`: `{id, name, name_only, name_short}` — responsável pela oportunidade
- `additional_values.opportunities`: campos customizados (origem, área do direito, etc. — variam por conta)

### `/tasks`
Campos: `id`, `type_id`, `type_title` (E-mail, Ligação, etc.), `user_id` (responsável), `opportunity_id`, `organization_id`, `person_id`, `description` (conteúdo da tarefa), `concluded` (Y/N), `event_time` (data/hora agendada), `added_in`, `updated_in`.

Objetos aninhados: `persons`, `organizations`, `opportunities` (nome/título relacionados), `tasks.type_name`.

### `/organizations`
Campos: `id`, `name`, `address`, `document`, `phone`, `added_in`, `updated_in`, `additional_values` (site, segmento, UF, porte, etc.), `persons` (lista de contatos vinculados).

### `/persons`
Campos: `id`, `name`, `email`, `phone`, `address`, `added_in`, `updated_in`, `additional_values` (cargo, linkedin, telefone_completo).

### `/users`
Campos: `id`, `name`, `email`, `phone`, `verified`, `added_in`, `clients_users.admin`, `clients_users.active`. (campo `password` sempre vem mascarado como `******`, não é sensível).

### `/stages`
Campos: `id`, `pipe_id`, `type` (`open`, `win`, `loss`), `name_short`, `order` (posição no funil), `background` (cor), `active`.

Ordem do funil ("Funil padrão", pipe_id=1), do início ao fim:
1. Prospecção/Qualifi (open)
2. Proposta Comercial (open)
3. Negociação (open)
4. Reunião (open)
5. Contrato (open)
6. Possível Cotação (open)
7. 1 Lic. Análise (open)
8. 2 Lic. Proposta (open)
9. 3 Lic. Habilitação (open)
10. 4 Lic. Homologação (open)
11. 5 Lic. Suspensa (open)
12. Ganha (win)
13. Perdida (loss)
14. Inativa (open)

### `/pipes`
Campos: `id`, `name`, `name_short`, `active`. Só existe 1 pipe ("Funil padrão").

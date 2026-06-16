# CopaPulse AI — Base de Conhecimento

## 1. Fontes de Dados

O agente opera exclusivamente sobre dados estruturados locais. Não há chamada a APIs externas em tempo real na versão MVP.

### 1.1 Jogos (`data/jogos.csv`)

**Objetivo:** Fornecer ao agente informação concreta sobre partidas da Copa.

**Campos:**
| Campo | Tipo | Descrição |
|---|---|---|
| id | int | Identificador único do jogo |
| data | date | Data no formato YYYY-MM-DD |
| hora | time | Hora local do país sede |
| selecao_a | string | Primeira seleção |
| selecao_b | string | Segunda seleção |
| grupo | string | Grupo (A a L) |
| estadio | string | Nome do estádio |
| cidade | string | Cidade sede |
| status | enum | `agendado`, `em_andamento`, `finalizado` |
| placar_a | int | Gols da seleção A (nulo se agendado) |
| placar_b | int | Gols da seleção B (nulo se agendado) |
| rodada | int | Rodada da fase de grupos (1, 2 ou 3) |

**Como é usado:** Para responder "jogos de hoje", "resultados da rodada", "próximo jogo do Brasil", etc.

---

### 1.2 Seleções (`data/selecoes.json`)

**Objetivo:** Fornecer perfil de cada seleção para análises e geração de conteúdo.

**Campos:**
- `nome`: Nome completo da seleção
- `codigo`: Código FIFA (BRA, ARG, etc.)
- `grupo`: Grupo na Copa 2026
- `titulos_copa`: Número de títulos mundiais
- `tecnico`: Nome do treinador
- `pontos_fortes`: Lista de características-chave
- `observacoes`: Contexto narrativo da estreia ou situação atual

**Como é usado:** Para "perfil do Brasil", "compare Argentina e França", "quem são os favoritos".

---

### 1.3 Grupos (`data/grupos.json`)

**Objetivo:** Classificação atualizada de cada grupo com pontos, saldo de gols e próximos jogos.

**Campos:**
- `grupo`: Letra do grupo
- `selecoes`: Lista de seleções
- `classificacao`: Array com posição, pontos, saldo e jogos
- `proximos_jogos`: Lista de próximos confrontos
- `criterios`: Regra de classificação

**Como é usado:** Para "situação do grupo D", "quem lidera o Grupo A", "o Brasil vai se classificar?".

---

### 1.4 Estádios (`data/estadios.json`)

**Objetivo:** Contextualizar geograficamente os jogos.

**Campos:** nome, cidade, estado, país, capacidade, se é sede da final.

**Como é usado:** Para "onde o Brasil joga?", "qual o maior estádio da Copa?", contexto geográfico.

---

### 1.5 Notícias Mockadas (`data/noticias_mockadas.csv`)

**Objetivo:** Simular feed de notícias para enriquecer respostas e gerar conteúdo.

**Campos:** data, título, fonte, categoria (resultado/preview/análise/estatística), resumo, seleção relacionada.

**Como é usado:** Para boletins, resumos editoriais, contexto sobre destaques da rodada.

---

### 1.6 Perfis de Usuário (`data/perfis_usuarios.json`)

**Objetivo:** Parametrizar o tom e o objetivo da resposta por tipo de usuário.

**Perfis:** torcedor, criador_conteudo, empresa.

**Como é usado:** O perfil selecionado determina o system prompt aplicado na chamada ao LLM.

---

## 2. Estratégia de Contexto

O agente não envia todos os dados para o LLM. Ele seleciona o contexto relevante antes de montar o prompt:

```
Pergunta do usuário
        ↓
Classificação de intenção
        ↓
Busca nos dados relevantes
        ↓
Montagem do contexto filtrado
        ↓
Prompt = system_prompt + contexto + pergunta
```

### Regras de seleção de contexto:

| Intenção detectada | Dados incluídos |
|---|---|
| Jogos de hoje | Jogos com data == hoje |
| Resultado da rodada | Jogos com status == 'finalizado' recentes |
| Situação de um grupo | Dados do grupo específico + jogos do grupo |
| Perfil de seleção | Dados da seleção + jogos da seleção |
| Gerar conteúdo | Jogos recentes + notícias relevantes |
| Ação comercial | Jogos de hoje/amanhã + perfil de empresa |

## 3. Limitações Conhecidas

1. **Dados estáticos:** A base não é atualizada automaticamente. Para uma Copa real, seria necessário conectar a uma API esportiva.
2. **Sem dados de escalação:** O agente não tem informação sobre quem joga em cada time.
3. **Histórico limitado:** O histórico das Copas anteriores é básico — apenas títulos e participações.
4. **Notícias simuladas:** As notícias são mockadas e não refletem fontes reais.

## 4. Decisão de Escopo

O agente responde apenas sobre:
- Copa do Mundo 2026 (fase de grupos)
- Seleções participantes
- Estádios confirmados

O agente NÃO responde sobre:
- Campeonatos nacionais ou outros torneios
- Apostas, odds ou previsões probabilísticas
- Escalações ou confirmações técnicas
- Resultados fora da base de dados

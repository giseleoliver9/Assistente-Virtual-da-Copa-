# ⚽ CopaPulse AI

> Agente inteligente para acompanhamento da Copa do Mundo 2026 — com análise de grupos, geração de conteúdo e ações comerciais personalizadas por persona.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3%2070B-F55036?style=flat)
![Status](https://img.shields.io/badge/status-MVP%20funcional-brightgreen)

---

## Sobre o projeto

Durante a Copa do Mundo, torcedores, empresas e criadores de conteúdo são bombardeados por jogos, resultados e notícias ao mesmo tempo. O problema não é falta de informação — é excesso dela sem organização.

O **CopaPulse AI** resolve isso com um agente que consulta uma base estruturada da Copa 2026 e gera respostas personalizadas dependendo de quem pergunta.

### Três modos de uso

| Modo | Para quem | Como responde |
|---|---|---|
| 🟢 **Torcedor** | Fã casual de futebol | Simples, empolgado, sem jargão técnico |
| 🔵 **Conteúdo** | Social media, jornalistas, influencers | Posts prontos, boletins, hashtags |
| 🟠 **Empresa** | Bares, lojas, RH, comunicação interna | Ações comerciais, comunicados, campanhas |

---

## Demonstração

### Modo Torcedor
> **Pergunta:** "O Brasil pode ser eliminado na fase de grupos?"

**Resposta:**
```
Olha, a situação do Brasil é boa! Na primeira rodada, o Brasil venceu a Arábia 
Saudita por 3x1 e lidera o Grupo D com 3 pontos.

Para se classificar, o Brasil precisa terminar entre os dois primeiros do grupo. 
Com dois jogos ainda pela frente (Nigéria e Suíça), a matemática está favorável.

Vitória contra a Nigéria já coloca o Brasil em situação muito confortável.
```

---

### Modo Conteúdo
> **Pergunta:** "Gere 3 posts para Instagram sobre os jogos de hoje."

**Resposta:**
```
Post 1 — USA x Japan:
EUA vs Japão hoje às 13h! Os americanos estrearam vencendo o Marrocos 2x1.
O Japão vem do empate com o Uruguai. Quem avança no Grupo A? 🇺🇸🆚🇯🇵
#Copa2026 #WorldCup2026 #GrupoA

Post 2 — Mexico x Colombia:
Clássico latino hoje no Azteca! México e Colômbia chegam com vitória na estreia.
Duas seleções, um bilhete para a próxima fase. 🇲🇽🆚🇨🇴
#Copa2026 #GrupoB #Azteca

Post 3 — Geral:
Hoje tem Copa e muito! 4 jogos nos grupos A e B.
Quem você vai torcer? Conta aqui! ⚽🔥
#Copa2026 #WorldCup2026
```

---

### Modo Empresa
> **Pergunta:** "Crie uma ação para um bar no dia do jogo do Brasil."

**Resposta:**
```
Contexto: Brasil x Nigéria — 16/06 às 16h — MetLife Stadium, EUA

Oportunidade: tarde de segunda-feira com jogo decisivo do Brasil.

Ação: "Happy Hour Brasil 2026"
- Abra às 14h (2h antes do jogo)
- Combo especial: cerveja + petisco com desconto até o apito inicial
- Telão com decoração verde e amarelo
- Promoção: "gol do Brasil = 5% de desconto na próxima visita"

Mensagem para stories/WhatsApp:
"Brasil joga hoje! Venha torcer com a gente.
Happy Hour a partir das 14h. #BrasilNaCopa #Copa2026"
```

---

## Arquitetura

```
[Usuário — Streamlit]
        │
        ▼
[Seleção de modo: Torcedor / Conteúdo / Empresa]
        │
        ▼
[rules.py — valida a pergunta]
  ├── Bloqueia: apostas, odds, fora do escopo
  └── Aprova: segue para o agente
        │
        ▼
[agent.py — classifica intenção]
  ├── jogos_hoje / resultado_rodada / grupo / selecao / conteudo / empresa
        │
        ▼
[data_loader.py — monta contexto filtrado]
  ├── jogos.csv → busca por data, seleção, grupo
  ├── selecoes.json → perfil da seleção mencionada
  ├── grupos.json → classificação e próximos jogos
  └── noticias_mockadas.csv → destaques relevantes
        │
        ▼
[prompts.py — monta system prompt por modo]
        │
        ▼
[Groq API — LLaMA 3.3 70B Versatile]
        │
        ▼
[Resposta exibida ao usuário]
```

---

## Funcionalidades

- **Resumo da rodada** — resultados, destaques e análise dos jogos finalizados
- **Jogos de hoje** — lista com horários, estádios e grupos
- **Situação dos grupos** — classificação, pontos e próximos confrontos
- **Perfil de seleções** — histórico, técnico, pontos fortes e estreia
- **Gerador de conteúdo** — posts Instagram, boletins WhatsApp, tweets
- **Modo empresa** — ações comerciais, comunicados internos, campanhas
- **Anti-alucinação** — o agente nunca inventa placar, data ou escalação

---

## Estrutura do projeto

```
copapulse-ai/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── data/
│   ├── jogos.csv               # 44 jogos — fase de grupos completa
│   ├── selecoes.json           # 48 seleções com perfil e histórico
│   ├── grupos.json             # 12 grupos com classificação pós-rodada 1
│   ├── estadios.json           # 14 estádios da Copa 2026
│   ├── noticias_mockadas.csv   # 25 notícias simuladas
│   └── perfis_usuarios.json    # 3 personas de usuário
│
├── docs/
│   ├── 01-documentacao-agente.md   # Problema, solução, personas, arquitetura
│   ├── 02-base-conhecimento.md     # Schema dos dados e estratégia de contexto
│   ├── 03-prompts.md               # System prompts + edge cases + exemplos
│   ├── 04-metricas.md              # 10 cenários de teste com resultados
│   └── 05-pitch.md                 # Pitch de 3 minutos + resumo executivo
│
└── src/
    ├── app.py          # Interface Streamlit
    ├── agent.py        # Lógica central: intenção + contexto + LLM
    ├── prompts.py      # System prompts por modo
    ├── data_loader.py  # Carregamento e filtros de dados
    └── rules.py        # Camada anti-alucinação e controle de escopo
```

---

## Base de dados

### Grupos da Copa 2026

| Grupo | Seleções |
|---|---|
| A | USA, Morocco, Japan, Uruguay |
| B | Mexico, Colombia, Serbia, Ivory Coast |
| C | Canada, Netherlands, Cameroon, South Korea |
| D | Brazil, Switzerland, Nigeria, Saudi Arabia |
| E | France, Ecuador, Turkey, South Africa |
| F | Argentina, Poland, Ghana, Iran |
| G | Spain, Senegal, Scotland, Iraq |
| H | England, Venezuela, Egypt, Hungary |
| I | Germany, Panama, Algeria, Australia |
| J | Portugal, Bolivia, Romania, Uzbekistan |
| K | Belgium, Costa Rica, Tunisia, Denmark |
| L | Croatia, Honduras, New Zealand, Slovakia |

### Estádios

| Estádio | Cidade | País | Capacidade |
|---|---|---|---|
| MetLife Stadium ⭐ | East Rutherford, NJ | USA | 82.500 |
| Rose Bowl | Pasadena, CA | USA | 88.565 |
| AT&T Stadium | Arlington, TX | USA | 80.000 |
| Estadio Azteca | Cidade do México | México | 87.523 |
| BC Place | Vancouver | Canadá | 54.500 |
| BMO Field | Toronto | Canadá | 30.000 |
| + 8 outros | ... | ... | ... |

⭐ Sede da final

---

## Como rodar

### Pré-requisitos

- Python 3.11+
- Conta gratuita no [Groq Console](https://console.groq.com) para obter a API Key

### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/copapulse-ai.git
cd copapulse-ai

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure a chave de API
cp .env.example .env
# Edite o arquivo .env e adicione sua GROQ_API_KEY

# 4. Execute o app
python -m streamlit run src/app.py
```

### Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
GROQ_API_KEY=sua_chave_aqui
```

Obtenha sua chave gratuita em: [console.groq.com](https://console.groq.com)

---

## Exemplos de perguntas

```
# Modo Torcedor
"O que aconteceu hoje na Copa?"
"Como está o grupo do Brasil?"
"Quem está liderando o Grupo A?"
"O Brasil pode ser eliminado?"
"Explique como funciona a classificação."

# Modo Conteúdo
"Gere 3 posts para Instagram sobre os jogos de hoje."
"Monte um boletim para WhatsApp com os resultados."
"Crie uma legenda sobre a vitória do Brasil."
"Escreva um tweet sobre a goleada da Croácia."

# Modo Empresa
"Sugira uma ação para um bar no dia do jogo do Brasil."
"Crie um comunicado interno sobre os jogos da semana."
"Monte uma campanha para uma loja durante a Copa."
"Escreva um e-mail para a equipe sobre o jogo de amanhã."
```

---

## Tecnologias e conceitos aplicados

### Stack principal

| Camada | Tecnologia | Papel no projeto |
|---|---|---|
| Linguagem | Python 3.11+ | Base de todo o código |
| Interface | Streamlit | App web sem necessidade de HTML/CSS/JS |
| LLM | Groq API — LLaMA 3.3 70B | Geração de linguagem natural |
| Dados estruturados | Pandas + CSV + JSON | Base de conhecimento local |
| Variáveis de ambiente | python-dotenv | Gerenciamento seguro de credenciais |

---

### Padrão RAG (Retrieval-Augmented Generation)

O CopaPulse AI implementa uma versão simplificada do padrão **RAG** — uma das arquiteturas mais usadas em agentes de IA com dados próprios.

```
RAG clássico:                        CopaPulse AI:
─────────────────────────────        ──────────────────────────────
Pergunta do usuário                  Pergunta do usuário
        ↓                                    ↓
Busca vetorial (embeddings)          Busca por regras (data_loader.py)
        ↓                                    ↓
Recupera trechos relevantes          Filtra dados por data/seleção/grupo
        ↓                                    ↓
Monta prompt com contexto            Monta prompt com contexto filtrado
        ↓                                    ↓
LLM gera resposta                    LLM gera resposta
```

A diferença: em vez de embeddings e busca vetorial (solução mais complexa), o agente usa **busca por regras determinísticas** — mais simples, mais controlável e suficiente para uma base de dados estruturada como CSV/JSON.

Para evoluir para RAG completo: substituir `data_loader.py` por um vector store (FAISS, ChromaDB, Pinecone) e usar embeddings para recuperar trechos.

---

### Engenharia de Prompt

O projeto aplica técnicas de prompt engineering para controlar o comportamento do LLM:

| Técnica | Onde é usada |
|---|---|
| **System prompt** | Define persona, regras e modo de resposta |
| **Contexto estruturado** | Dados reais injetados no prompt antes da pergunta |
| **Few-shot examples** | Exemplos de resposta esperada por modo (nos docs) |
| **Negative prompting** | Instruções explícitas do que NÃO fazer (não inventar dados) |
| **Persona switching** | System prompt muda completamente por modo selecionado |

---

### Classificação de intenção

Antes de chamar o LLM, o agente classifica a intenção da pergunta com regras simples baseadas em palavras-chave. Isso reduz o contexto enviado e melhora a qualidade da resposta.

```python
# Exemplo: pergunta sobre o Brasil dispara busca de seleção + grupo + jogos + notícias
# Pergunta sobre hoje dispara busca de jogos com data == today
# Pergunta sobre apostas é bloqueada antes de chegar ao LLM
```

Para evoluir: substituir o classificador por um LLM menor (ex: LLaMA 3.1 8B) que classifica a intenção com mais precisão antes de chamar o modelo principal.

---

## Segurança e controle

O agente possui uma camada de validação (`rules.py`) que:

- **Bloqueia** perguntas sobre apostas, odds e previsões financeiras
- **Redireciona** perguntas fora do escopo da Copa 2026
- **Instrui o LLM** a não inventar informações ausentes na base
- **Sinaliza claramente** quando os dados são insuficientes

---

## Limitações conhecidas

- Base de dados estática — não atualiza automaticamente com resultados reais
- Sem dados de escalação ou estatísticas individuais de jogadores
- Notícias são simuladas — não refletem fontes reais
- Sem memória de conversa — cada pergunta é independente

---

## Roadmap

- [ ] Integração com API esportiva em tempo real
- [ ] Dashboard interativo com tabela de classificação
- [ ] Exportação de boletim em PDF
- [ ] Histórico de conversa (memória de sessão)
- [ ] Atualização automática de resultados
- [ ] Agente multimodal com geração de cards visuais

---

## Documentação

| Arquivo | Conteúdo |
|---|---|
| [01 — Documentação do Agente](docs/01-documentacao-agente.md) | Problema, solução, personas, arquitetura |
| [02 — Base de Conhecimento](docs/02-base-conhecimento.md) | Schema dos dados, estratégia de contexto |
| [03 — Prompts](docs/03-prompts.md) | System prompts, edge cases, exemplos |
| [04 — Métricas](docs/04-metricas.md) | Cenários de teste e resultados |
| [05 — Pitch](docs/05-pitch.md) | Apresentação do projeto em 3 minutos |

---

## Este código como base para outros agentes

A arquitetura do CopaPulse AI é **independente do domínio**. Os cinco arquivos de `src/` formam um template reutilizável para qualquer agente que precise consultar uma base de dados estruturada e responder em diferentes tons por persona.

### O que muda entre um agente e outro

| Componente | O que substituir |
|---|---|
| `data/` | Troque os CSVs e JSONs pela base do novo domínio |
| `prompts.py` | Reescreva os system prompts para o novo contexto e personas |
| `data_loader.py` | Adapte as funções de busca para os campos da nova base |
| `rules.py` | Atualize as palavras bloqueadas e os limites de escopo |
| `agent.py` | Ajuste as intenções detectadas para o novo domínio |

`app.py` e a estrutura de chamada ao LLM ficam praticamente iguais.

---

### Exemplos de agentes que usariam a mesma estrutura

| Agente | Domínio | Base de dados | Personas |
|---|---|---|---|
| **Agente Financeiro** | Investimentos pessoais | Transações, produtos, perfil | Correntista, assessor, empresa |
| **Agente de RH** | Benefícios e políticas | Manual, FAQ, calendário | Colaborador, gestor, RH |
| **Agente de Cardápio** | Restaurante | Pratos, ingredientes, preços | Cliente, garçom, cozinha |
| **Agente Imobiliário** | Compra e aluguel | Imóveis, bairros, preços | Comprador, corretor, investidor |
| **Agente Jurídico** | Contratos e cláusulas | Documentos, prazos, partes | Cliente, advogado, paralegal |
| **Agente de Eventos** | Agenda corporativa | Eventos, palestrantes, locais | Participante, organizador, patrocinador |
| **Agente de Suporte** | Atendimento ao cliente | FAQ, tickets, produtos | Usuário, atendente, supervisor |

### Como fazer o fork deste projeto

```bash
# 1. Clone este repositório como base
git clone https://github.com/seu-usuario/copapulse-ai.git meu-novo-agente
cd meu-novo-agente

# 2. Substitua os dados
# data/ → coloque os arquivos CSV/JSON do seu domínio

# 3. Adapte os prompts
# src/prompts.py → reescreva SYSTEM_BASE e MODE_PROMPTS

# 4. Ajuste as regras
# src/rules.py → atualize BLOCKED_KEYWORDS e OUT_OF_SCOPE_KEYWORDS

# 5. Atualize as intenções
# src/agent.py → reescreva INTENT_KEYWORDS e build_context()

# 6. Rode
python -m streamlit run src/app.py
```

O padrão RAG simplificado, a separação por personas e a camada de segurança funcionam para qualquer domínio — basta trocar os dados e os prompts.

---

Desenvolvido como parte do lab de IA Generativa da [DIO](https://www.dio.me)

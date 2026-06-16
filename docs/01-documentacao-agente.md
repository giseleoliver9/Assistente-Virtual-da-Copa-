# CopaPulse AI — Documentação do Agente

## 1. Problema

Durante a Copa do Mundo, torcedores, empresas e criadores de conteúdo são bombardeados por jogos, resultados, notícias e estatísticas ao mesmo tempo. O volume de informação é alto, o ritmo é acelerado e nem todos têm tempo ou conhecimento técnico para transformar dados em análise ou conteúdo útil.

Problemas identificados:
- Torcedores casuais perdem o fio da meada com 12 grupos simultâneos
- Criadores de conteúdo precisam postar rápido mas não têm dados organizados
- Empresas querem aproveitar o clima da Copa mas não sabem como fazer isso de forma relevante

## 2. Solução

O **CopaPulse AI** é um agente inteligente que consulta uma base de dados estruturada da Copa do Mundo 2026 e gera respostas personalizadas por tipo de usuário. O agente combina:

- Dados estruturados (jogos, seleções, grupos, estádios, notícias)
- Engenharia de prompt com personas distintas
- Camada de controle anti-alucinação
- Interface acessível via Streamlit

## 3. Nome do Agente

**CopaPulse AI**

Tagline: *Seu radar inteligente para a Copa do Mundo 2026.*

## 4. Personas de Usuário

### Torcedor
- **Quem é:** Fã de futebol que quer acompanhar a Copa de forma simples
- **Necessidade:** Entender grupos, classificações e próximos jogos sem jargão técnico
- **Como o agente fala:** Linguagem simples, empolgada e acessível

### Criador de Conteúdo
- **Quem é:** Social media, influencer, jornalista digital
- **Necessidade:** Posts prontos, legendas, boletins e ideias de pauta em segundos
- **Como o agente fala:** Criativo, dinâmico, direto e adaptado ao canal

### Empresa
- **Quem é:** Bar, restaurante, loja, RH corporativo, comunicação interna
- **Necessidade:** Ações comerciais, campanhas e comunicados para dias de jogo
- **Como o agente fala:** Profissional, orientado a ação, comercialmente relevante

## 5. Arquitetura do Agente

```
[Usuário via Streamlit]
        ↓
[Seleção de Modo: Torcedor / Conteúdo / Empresa]
        ↓
[CopaPulse Agent]
    ├── data_loader.py → carrega dados da base (CSV/JSON)
    ├── rules.py → valida entrada e saída
    ├── prompts.py → monta system prompt por modo
    ├── agent.py → classifica intenção, monta contexto, chama LLM
        ↓
[Groq API — LLaMA 3.3 70B]
        ↓
[Validação da resposta]
        ↓
[Exibição ao usuário]
```

## 6. Componentes Técnicos

| Componente | Arquivo | Função |
|---|---|---|
| Interface | `src/app.py` | Streamlit: modos, filtros, botões rápidos |
| Agente | `src/agent.py` | Lógica central: contexto + LLM + validação |
| Prompts | `src/prompts.py` | System prompts e templates por modo |
| Dados | `src/data_loader.py` | Carrega e filtra CSV/JSON |
| Regras | `src/rules.py` | Anti-alucinação e controle de escopo |

## 7. Base de Dados

| Arquivo | Conteúdo |
|---|---|
| `data/jogos.csv` | 44 jogos com data, hora, seleções, grupo, estádio, status e placar |
| `data/selecoes.json` | 48 seleções com grupo, títulos, técnico e observações |
| `data/grupos.json` | 12 grupos com classificação atualizada |
| `data/estadios.json` | 14 estádios com cidade, país e capacidade |
| `data/noticias_mockadas.csv` | 25 notícias simuladas por seleção e data |
| `data/perfis_usuarios.json` | 3 perfis de usuário com exemplos de perguntas |

## 8. Segurança e Limitações

### O que o agente PODE fazer
- Responder com base nos dados carregados
- Gerar conteúdo criativo sobre jogos e seleções
- Analisar cenários com base em dados disponíveis
- Avisar quando não houver dado suficiente

### O que o agente NÃO FAZ
- Inventar placares, datas ou estatísticas
- Gerar conteúdo sobre apostas ou odds
- Prometer resultados futuros
- Criar informações fora da base sem sinalizar claramente

## 9. Stack Tecnológica

- **Linguagem:** Python 3.11+
- **Interface:** Streamlit
- **LLM:** Groq API (LLaMA 3.3 70B Versatile)
- **Dados:** Pandas (CSV), JSON nativo
- **Gerenciamento de config:** python-dotenv

## 10. Como Executar

```bash
pip install -r requirements.txt
cp .env.example .env
# Adicione sua GROQ_API_KEY no .env
streamlit run src/app.py
```


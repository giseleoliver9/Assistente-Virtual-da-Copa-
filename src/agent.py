import os
from datetime import date, timedelta

from groq import Groq
from dotenv import load_dotenv

from data_loader import (
    buscar_jogos_por_data,
    buscar_jogos_por_selecao,
    buscar_grupo_da_selecao,
    buscar_grupo_por_letra,
    buscar_selecao_por_nome,
    buscar_jogos_finalizados_recentes,
    buscar_noticias_recentes,
    buscar_noticias_por_selecao,
    jogos_para_texto,
    grupo_para_texto,
    selecao_para_texto,
)
from prompts import build_system_prompt, build_user_message
from rules import validate_query

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"

INTENT_KEYWORDS = {
    "jogos_hoje": ["hoje", "agendado", "vai jogar hoje", "joga hoje"],
    "resultado_rodada": ["resultado", "como foi", "placar", "quem ganhou", "rodada", "resumo"],
    "grupo": ["grupo", "classificação", "tabela", "lidera", "liderando", "situação do grupo"],
    "selecao": ["brasil", "argentina", "frança", "espanha", "alemanha", "portugal", "inglaterra",
                "seleção", "time", "equipe"],
    "conteudo": ["post", "instagram", "whatsapp", "boletim", "legenda", "twitter", "linkedin",
                 "gere", "crie", "escreva", "publique"],
    "empresa": ["bar", "restaurante", "empresa", "loja", "rh", "comunicação interna",
                "campanha", "ação comercial", "comunicado"],
}


def classify_intent(query: str) -> list[str]:
    query_lower = query.lower()
    detected = []
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            detected.append(intent)
    return detected if detected else ["geral"]


def build_context(query: str, intents: list[str]) -> str:
    today = date.today()
    parts = []

    if "jogos_hoje" in intents or "agendado" in query.lower():
        jogos = buscar_jogos_por_data(today)
        parts.append(f"JOGOS DE HOJE ({today}):\n{jogos_para_texto(jogos)}")

        amanha = today + timedelta(days=1)
        jogos_amanha = buscar_jogos_por_data(amanha)
        if not jogos_amanha.empty:
            parts.append(f"\nJOGOS DE AMANHÃ ({amanha}):\n{jogos_para_texto(jogos_amanha)}")

    if "resultado_rodada" in intents:
        ontem = today - timedelta(days=1)
        jogos_ontem = buscar_jogos_por_data(ontem)
        parts.append(f"RESULTADOS DE ONTEM ({ontem}):\n{jogos_para_texto(jogos_ontem)}")

        recentes = buscar_jogos_finalizados_recentes(12)
        parts.append(f"\nJOGOS FINALIZADOS RECENTES:\n{jogos_para_texto(recentes)}")

        noticias = buscar_noticias_recentes(8)
        if not noticias.empty:
            noticias_txt = "\n".join(
                f"- {r['titulo']} ({r['data']}): {r['resumo']}"
                for _, r in noticias.iterrows()
            )
            parts.append(f"\nNOTÍCIAS RECENTES:\n{noticias_txt}")

    if "grupo" in intents:
        for letra in "ABCDEFGHIJKL":
            if f"grupo {letra.lower()}" in query.lower() or f"grupo {letra}" in query.upper():
                grupo = buscar_grupo_por_letra(letra)
                if grupo:
                    parts.append(f"\n{grupo_para_texto(grupo)}")
                break

    selecoes_notaveis = [
        "Brasil", "Argentina", "França", "Espanha", "Alemanha", "Portugal",
        "Inglaterra", "México", "Uruguai", "Japão", "Marrocos", "Senegal",
    ]
    for nome in selecoes_notaveis:
        if nome.lower() in query.lower():
            selecao = buscar_selecao_por_nome(nome)
            if selecao:
                parts.append(f"\nPERFIL DA SELEÇÃO:\n{selecao_para_texto(selecao)}")
                grupo = buscar_grupo_da_selecao(nome)
                if grupo:
                    parts.append(f"\n{grupo_para_texto(grupo)}")
                jogos = buscar_jogos_por_selecao(nome)
                parts.append(f"\nJOGOS DE {nome.upper()}:\n{jogos_para_texto(jogos)}")
                noticias = buscar_noticias_por_selecao(nome, 4)
                if not noticias.empty:
                    noticias_txt = "\n".join(
                        f"- {r['titulo']}: {r['resumo']}" for _, r in noticias.iterrows()
                    )
                    parts.append(f"\nNOTÍCIAS SOBRE {nome.upper()}:\n{noticias_txt}")
            break

    if "conteudo" in intents or "empresa" in intents:
        jogos_hoje = buscar_jogos_por_data(today)
        if not jogos_hoje.empty:
            parts.append(f"\nJOGOS DE HOJE PARA CONTEÚDO:\n{jogos_para_texto(jogos_hoje)}")
        recentes = buscar_jogos_finalizados_recentes(6)
        parts.append(f"\nRESULTADOS RECENTES:\n{jogos_para_texto(recentes)}")

    if not parts:
        recentes = buscar_jogos_finalizados_recentes(8)
        parts.append(f"RESULTADOS RECENTES:\n{jogos_para_texto(recentes)}")
        jogos_hoje = buscar_jogos_por_data(today)
        if not jogos_hoje.empty:
            parts.append(f"\nJOGOS DE HOJE:\n{jogos_para_texto(jogos_hoje)}")

    return "\n".join(parts) if parts else "Nenhum dado relevante encontrado para esta consulta."


class CopaPulseAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY não encontrada. Configure no arquivo .env")
        self.client = Groq(api_key=api_key)
        self._last_context: str = ""

    def respond(self, query: str, mode: str = "Torcedor") -> str:
        valid, block_msg = validate_query(query)
        if not valid:
            return block_msg

        intents = classify_intent(query)
        context = build_context(query, intents)
        self._last_context = context

        system_prompt = build_system_prompt(mode)
        user_message = build_user_message(query, context)

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content

    def get_last_context(self) -> str:
        return self._last_context

    def get_all_teams(self) -> list[str]:
        from data_loader import get_all_team_names
        return get_all_team_names()

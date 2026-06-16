BLOCKED_KEYWORDS = [
    "aposta", "apostar", "odd", "odds", "casa de apostas", "bet", "betting",
    "probabilidade de ganhar", "chance de ganhar", "quanto vale", "lucrar",
    "ganhar dinheiro", "handicap", "over", "under", "1x2",
]

OUT_OF_SCOPE_KEYWORDS = [
    "campeonato brasileiro", "premier league", "la liga", "bundesliga",
    "serie a", "champions league", "libertadores", "copa do brasil",
    "eurocopa", "copa america", "nations league",
]

HALLUCINATION_GUARD = """
ATENÇÃO: Você está respondendo com base nos dados fornecidos abaixo.
NÃO invente placares, datas, gols, escalações ou estatísticas que não estejam nos dados.
Se a informação não estiver disponível, diga explicitamente: "Não tenho essa informação na base."
"""


def check_blocked_keywords(query: str) -> tuple[bool, str]:
    query_lower = query.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in query_lower:
            return True, (
                "O CopaPulse AI não fornece informações sobre apostas, odds ou previsões financeiras. "
                "Posso ajudar com análise do grupo, próximos jogos ou geração de conteúdo sobre a Copa."
            )
    return False, ""


def check_out_of_scope(query: str) -> tuple[bool, str]:
    query_lower = query.lower()
    for keyword in OUT_OF_SCOPE_KEYWORDS:
        if keyword in query_lower:
            return True, (
                f"Sou especializado na Copa do Mundo 2026. Para informações sobre {keyword} "
                "ou outros torneios, consulte fontes como Globo Esporte ou ESPN Brasil. "
                "Posso ajudar com alguma pergunta sobre a Copa?"
            )
    return False, ""


def validate_query(query: str) -> tuple[bool, str]:
    blocked, msg = check_blocked_keywords(query)
    if blocked:
        return False, msg

    out_of_scope, msg = check_out_of_scope(query)
    if out_of_scope:
        return False, msg

    if len(query.strip()) < 5:
        return False, "Por favor, faça uma pergunta mais específica sobre a Copa 2026."

    return True, ""

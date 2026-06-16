import pandas as pd
import json
from pathlib import Path
from datetime import date

DATA_DIR = Path(__file__).parent.parent / "data"


def load_jogos() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "jogos.csv")
    df["data"] = pd.to_datetime(df["data"]).dt.date
    return df


def load_selecoes() -> list[dict]:
    with open(DATA_DIR / "selecoes.json", encoding="utf-8") as f:
        return json.load(f)


def load_grupos() -> list[dict]:
    with open(DATA_DIR / "grupos.json", encoding="utf-8") as f:
        return json.load(f)


def load_estadios() -> list[dict]:
    with open(DATA_DIR / "estadios.json", encoding="utf-8") as f:
        return json.load(f)


def load_noticias() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "noticias_mockadas.csv")
    df["data"] = pd.to_datetime(df["data"]).dt.date
    return df


def load_perfis() -> list[dict]:
    with open(DATA_DIR / "perfis_usuarios.json", encoding="utf-8") as f:
        return json.load(f)


def buscar_jogos_por_data(data_alvo: date) -> pd.DataFrame:
    df = load_jogos()
    return df[df["data"] == data_alvo]


def buscar_jogos_por_selecao(selecao: str) -> pd.DataFrame:
    df = load_jogos()
    selecao_lower = selecao.lower()
    mask = (
        df["selecao_a"].str.lower().str.contains(selecao_lower)
        | df["selecao_b"].str.lower().str.contains(selecao_lower)
    )
    return df[mask]


def buscar_grupo_por_letra(letra: str) -> dict | None:
    grupos = load_grupos()
    for g in grupos:
        if g["grupo"].upper() == letra.upper():
            return g
    return None


def buscar_selecao_por_nome(nome: str) -> dict | None:
    selecoes = load_selecoes()
    nome_lower = nome.lower()
    for s in selecoes:
        if nome_lower in s["nome"].lower():
            return s
    return None


def buscar_grupo_da_selecao(nome_selecao: str) -> dict | None:
    selecao = buscar_selecao_por_nome(nome_selecao)
    if selecao:
        return buscar_grupo_por_letra(selecao["grupo"])
    return None


def buscar_jogos_finalizados_recentes(n: int = 12) -> pd.DataFrame:
    df = load_jogos()
    finalizados = df[df["status"] == "finalizado"].copy()
    finalizados = finalizados.sort_values("data", ascending=False)
    return finalizados.head(n)


def buscar_noticias_por_selecao(selecao: str, n: int = 5) -> pd.DataFrame:
    df = load_noticias()
    return df[df["selecao_relacionada"].str.lower() == selecao.lower()].head(n)


def buscar_noticias_recentes(n: int = 10) -> pd.DataFrame:
    df = load_noticias()
    return df.sort_values("data", ascending=False).head(n)


def get_all_team_names() -> list[str]:
    selecoes = load_selecoes()
    nomes = list({s["nome"] for s in selecoes})
    return sorted(nomes)


def jogos_para_texto(df: pd.DataFrame) -> str:
    if df.empty:
        return "Nenhum jogo encontrado."
    linhas = []
    for _, row in df.iterrows():
        if row["status"] == "finalizado":
            placar = f"{int(row['placar_a'])}x{int(row['placar_b'])}"
            linhas.append(
                f"- {row['selecao_a']} {placar} {row['selecao_b']} | "
                f"Grupo {row['grupo']} | {row['data']} {row['hora']} | "
                f"{row['estadio']}, {row['cidade']} | Rodada {row['rodada']}"
            )
        else:
            linhas.append(
                f"- {row['selecao_a']} x {row['selecao_b']} | "
                f"Grupo {row['grupo']} | {row['data']} {row['hora']} | "
                f"{row['estadio']}, {row['cidade']} | Rodada {row['rodada']} | {row['status'].upper()}"
            )
    return "\n".join(linhas)


def grupo_para_texto(grupo: dict) -> str:
    if not grupo:
        return "Grupo não encontrado."
    linhas = [f"GRUPO {grupo['grupo']}: {', '.join(grupo['selecoes'])}", ""]
    linhas.append("Classificação:")
    for pos, time in enumerate(grupo["classificacao"], 1):
        linhas.append(
            f"  {pos}. {time['selecao']} — {time['pontos']} pts | "
            f"{time['jogos']} J | {time['vitorias']}V {time['empates']}E {time['derrotas']}D | "
            f"Saldo {time['saldo']:+d} | {time['gols_pro']}:{time['gols_contra']}"
        )
    if grupo.get("proximos_jogos"):
        linhas.append("")
        linhas.append("Próximos jogos: " + " | ".join(grupo["proximos_jogos"]))
    return "\n".join(linhas)


def selecao_para_texto(selecao: dict) -> str:
    if not selecao:
        return "Seleção não encontrada."
    titulos = selecao.get("titulos_copa", 0)
    anos = ", ".join(str(a) for a in selecao.get("anos_titulo", []))
    pontos = "; ".join(selecao.get("pontos_fortes", []))
    return (
        f"{selecao['nome']} (Grupo {selecao['grupo']})\n"
        f"Confederação: {selecao['confederacao']}\n"
        f"Títulos: {titulos}" + (f" ({anos})" if anos else "") + "\n"
        f"Técnico: {selecao.get('tecnico', 'A definir')}\n"
        f"Pontos fortes: {pontos}\n"
        f"Situação: {selecao.get('observacoes', '')}"
    )

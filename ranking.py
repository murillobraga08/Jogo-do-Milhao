"""Persistência do ranking de jogadores em arquivo JSON."""

import json
import os

ARQUIVO_RANKING = "ranking.json"


def carregar_ranking():
    """Carrega o ranking salvo; devolve uma lista vazia se o arquivo não existir."""
    if os.path.exists(ARQUIVO_RANKING):
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def salvar_ranking(ranking):
    """Grava a lista de jogadores no arquivo de ranking."""
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)
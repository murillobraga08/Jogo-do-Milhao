import json
import os

ARQUIVO = "ranking.json"

def carregar_ranking():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_ranking(ranking):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)
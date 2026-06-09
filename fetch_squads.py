#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_squads.py — Copa do Mundo FIFA 2026
Busca os 26 convocados oficiais (número, posição, clube) de todas as 48
seleções em worldcupranking.com (espelho da lista FIFA publicada em 03-06-2026)
e atualiza data/data.json.

Roda automaticamente pelo GitHub Actions na primeira execução ou sempre que
uma seleção ainda não tiver plantel preenchido. Pode ser re-executado manualmente
para atualizar substituições por lesão (basta apagar o plantel da seleção no
data.json e rodar de novo).
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "data.json")
BASE_URL = "https://worldcupranking.com/world-cup-2026/squads/{slug}/"

# Mapeamento: sigla FIFA -> slug do worldcupranking.com
SLUG = {
    "MEX": "mexico",          "RSA": "south-africa",     "KOR": "south-korea",
    "CZE": "czech-republic",  "CAN": "canada",            "BIH": "bosnia-and-herzegovina",
    "BRA": "brazil",          "MAR": "morocco",           "HAI": "haiti",
    "SCO": "scotland",        "USA": "united-states",     "PAR": "paraguay",
    "AUS": "australia",       "TUR": "turkey",            "GER": "germany",
    "CUW": "curacao",         "CIV": "ivory-coast",       "ECU": "ecuador",
    "NED": "netherlands",     "JPN": "japan",             "SWE": "sweden",
    "TUN": "tunisia",         "BEL": "belgium",           "EGY": "egypt",
    "IRN": "iran",            "NZL": "new-zealand",       "ESP": "spain",
    "URU": "uruguay",         "KSA": "saudi-arabia",      "CPV": "cape-verde",
    "FRA": "france",          "SEN": "senegal",           "NOR": "norway",
    "IRQ": "iraq",            "ARG": "argentina",         "ALG": "algeria",
    "AUT": "austria",         "JOR": "jordan",            "POR": "portugal",
    "COD": "dr-congo",        "UZB": "uzbekistan",        "COL": "colombia",
    "ENG": "england",         "CRO": "croatia",           "GHA": "ghana",
    "PAN": "panama",          "QAT": "qatar",             "SUI": "switzerland",
}

# Posições FIFA -> formato do calendário
POS = {"GK": "GOL", "DF": "DEF", "MF": "MEI", "FW": "ATA"}


def title_name(raw: str) -> str:
    """Converte nome em caixa-alta do FIFA para Title Case legível."""
    particles_lower = {"de", "da", "do", "dos", "das", "van", "der", "den",
                       "von", "del", "di", "e", "y", "el", "al"}
    keep_upper = {"jr", "jr.", "sr", "ii", "iii", "iv", "v"}
    words = []
    for i, w in enumerate(raw.strip().split()):
        wl = w.lower().rstrip(".")
        if re.match(r'^[a-z]\.$', w.lower()):       # inicial: A. → A.
            words.append(w.upper())
        elif wl in keep_upper:
            words.append(w.rstrip(".").capitalize() + ("." if w.endswith(".") else ""))
        elif wl in particles_lower and i > 0:
            words.append(w.lower())
        else:
            words.append(w[0].upper() + w[1:].lower() if w else w)
    return " ".join(words)


def fetch_squad(code: str) -> list[dict]:
    """Baixa a página de convocação e extrai a tabela de jogadores."""
    slug = SLUG.get(code)
    if not slug:
        return []
    url = BASE_URL.format(slug=slug)
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Copa2026-Calendar-Squads/1.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code} → {url}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"    Erro {code}: {e}", file=sys.stderr)
        return []

    # A tabela está em formato Markdown: | num | pos | nome | clube |
    players = []
    for line in html.splitlines():
        m = re.match(
            r'\|\s*(\d{1,2})\s*\|\s*(GK|DF|MF|FW)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|',
            line,
        )
        if m:
            num, pos, name, club = m.groups()
            players.append({
                "n":    int(num),
                "name": title_name(name),
                "pos":  POS.get(pos, "MEI"),
                "club": club.strip(),
            })
    return players


def main(force: bool = False):
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    teams_to_update = []
    for code in SLUG:
        if code not in data["teams"]:
            continue
        existing = data["teams"][code].get("squad", [])
        if not existing or force:
            teams_to_update.append(code)

    if not teams_to_update:
        print("Todos os planteis ja estao preenchidos.")
        return

    print(f"{len(teams_to_update)} selecoes a preencher...")
    updated = 0
    for code in teams_to_update:
        print(f"  {code}...", end=" ", flush=True)
        players = fetch_squad(code)
        if len(players) >= 20:
            data["teams"][code]["squad"] = players
            print(f"{len(players)} jogadores OK")
            updated += 1
        else:
            print(f"falhou (apenas {len(players)} encontrados)")
        time.sleep(0.4)   # cortesia: não sobrecarregar o servidor

    if updated:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n{updated} selecoes atualizadas. Regenerando .ics...")
        gen = os.path.join(HERE, "generate_calendar.py")
        result = subprocess.run([sys.executable, gen], capture_output=True, text=True)
        print(result.stdout.strip())
    else:
        print("Nenhuma atualizacao aplicada.")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--force", action="store_true",
                   help="Re-baixa mesmo os planteis ja preenchidos")
    args = p.parse_args()
    main(force=args.force)

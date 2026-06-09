#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync.py — Copa do Mundo FIFA 2026
Busca os resultados de duas APIs gratuitas (sem chave), atualiza data/data.json
e regenera os dois arquivos .ics. Rodado automaticamente pelo GitHub Actions
a cada 30 min durante o torneio.

APIs usadas:
  1. openfootball  https://raw.githubusercontent.com/openfootball/worldcup.json/master/2026/worldcup.json
  2. worldcup26.ir https://worldcup26.ir/get/games   (leituras, sem auth)
"""

import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "data.json")

OPENFOOTBALL_URL = (
    "https://raw.githubusercontent.com/openfootball/"
    "worldcup.json/master/2026/worldcup.json"
)
WORLDCUP26_URL = "https://worldcup26.ir/get/games"
WORLDCUP26_GROUPS_URL = "https://worldcup26.ir/get/groups"

# mapeamento nome completo -> sigla FIFA
TEAM_NAMES: dict[str, str] = {
    "Mexico": "MEX", "South Africa": "RSA",
    "South Korea": "KOR", "Korea Republic": "KOR",
    "Czech Republic": "CZE", "Czechia": "CZE",
    "Canada": "CAN", "Bosnia & Herzegovina": "BIH",
    "Bosnia and Herzegovina": "BIH", "Qatar": "QAT",
    "Switzerland": "SUI", "Brazil": "BRA", "Morocco": "MAR",
    "Haiti": "HAI", "Scotland": "SCO", "USA": "USA",
    "United States": "USA", "Paraguay": "PAR", "Australia": "AUS",
    "Turkey": "TUR", "Türkiye": "TUR", "Germany": "GER",
    "Curaçao": "CUW", "Curacao": "CUW",
    "Ivory Coast": "CIV", "Côte d'Ivoire": "CIV",
    "Ecuador": "ECU", "Netherlands": "NED", "Japan": "JPN",
    "Sweden": "SWE", "Tunisia": "TUN", "Belgium": "BEL",
    "Egypt": "EGY", "Iran": "IRN", "New Zealand": "NZL",
    "Spain": "ESP", "Cape Verde": "CPV", "Saudi Arabia": "KSA",
    "Uruguay": "URU", "France": "FRA", "Senegal": "SEN",
    "Iraq": "IRQ", "Norway": "NOR", "Argentina": "ARG",
    "Algeria": "ALG", "Austria": "AUT", "Jordan": "JOR",
    "Portugal": "POR", "DR Congo": "COD", "Congo DR": "COD",
    "Uzbekistan": "UZB", "Colombia": "COL", "England": "ENG",
    "Croatia": "CRO", "Ghana": "GHA", "Panama": "PAN",
}

# Annex C (simplificado) — mapeamento: frozenset das 8 letras dos grupos cujos
# terceiros se classificaram -> {slot_T_: código_grupo_que_preenche}
# Fonte: estrutura oficial do R32 da FIFA 2026.
# Incluída versão parcial para as combinacoes mais prováveis; o restante usa
# atribuicao por ranking quando a combinacao exata nao esta mapeada.
ANNEX_C: dict[frozenset, dict[str, str]] = {
    # slots: T_ABCDF, T_CDFGH, T_CEFHI, T_EHIJK, T_BEFIJ, T_AEHIJ, T_EFGIJ, T_DEIJL
    # Cada valor e uma letra de grupo cujo 3o preenche aquele slot.
    # (Tabela completa a ser atualizada quando FIFA publicar Annex C oficial)
    # Registra combinações de 12 grupos, 8 se qualificam; deixa "auto" para o resto.
}

# Slots T_ na ordem de prioridade de atribuicao (baseado no R32 oficial)
T_SLOTS_GROUPS: dict[str, list[str]] = {
    "T_ABCDF": list("ABCDF"),
    "T_CDFGH": list("CDFGH"),
    "T_CEFHI": list("CEFHI"),
    "T_EHIJK": list("EHIJK"),
    "T_BEFIJ": list("BEFIJ"),
    "T_AEHIJ": list("AEHIJ"),
    "T_EFGIJ": list("EFGIJ"),
    "T_DEIJL": list("DEIJL"),
}


# ---------------------------------------------------------------------------
# Utilitarios de rede
# ---------------------------------------------------------------------------
def fetch_json(url: str, timeout: int = 15):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Copa2026-Calendar-Sync/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  [AVISO] Nao foi possivel acessar {url}: {e}", file=sys.stderr)
        return None


def name_to_code(name: str) -> str:
    """Normaliza nome de selecao para sigla FIFA."""
    return TEAM_NAMES.get(name.strip(), "")


# ---------------------------------------------------------------------------
# Parsers das APIs
# ---------------------------------------------------------------------------
def parse_openfootball(raw: dict) -> dict[frozenset, dict]:
    """
    Retorna {frozenset({t1_code, t2_code}): result_dict}
    result_dict = {"home": int, "away": int, "winner": str (opcional)}
    """
    results: dict[frozenset, dict] = {}
    for m in raw.get("matches", []):
        score = m.get("score", {})
        if not score:
            continue
        t1_name = m.get("team1", "")
        t2_name = m.get("team2", "")
        t1 = name_to_code(t1_name)
        t2 = name_to_code(t2_name)
        if not t1 or not t2:
            continue  # jogo ainda com referencias (ex.: "W73") ou nome nao mapeado
        # placar final: penalties > prorrogacao > tempo normal
        if "p" in score:
            hg, ag = score["ft"]  # gols no tempo normal (empate)
            ph, pa = score["p"]
            winner = t1 if ph > pa else t2
            res = {"home": hg, "away": ag, "winner": winner}
        elif "et" in score:
            hg, ag = score["et"]
            winner = t1 if hg > ag else t2
            res = {"home": hg, "away": ag, "winner": winner}
        else:
            hg, ag = score["ft"]
            res = {"home": hg, "away": ag}
            if hg != ag:
                res["winner"] = t1 if hg > ag else t2
        key = frozenset([t1, t2])
        results[key] = res
    return results


def parse_worldcup26(games) -> dict[frozenset, dict]:
    """
    Parser flexivel para worldcup26.ir/get/games (formato exato variavel).
    Tenta vários nomes de campo comuns em APIs REST de futebol.
    """
    results: dict[frozenset, dict] = {}
    if not isinstance(games, list):
        return results
    for g in games:
        if not isinstance(g, dict):
            continue
        # Nomes de campo mais comuns
        t1 = (g.get("home_team") or g.get("team_home") or
              g.get("team1") or g.get("home") or "")
        t2 = (g.get("away_team") or g.get("team_away") or
              g.get("team2") or g.get("away") or "")
        s1 = (g.get("home_score") or g.get("score_home") or
              g.get("goals_home") or g.get("score1"))
        s2 = (g.get("away_score") or g.get("score_away") or
              g.get("goals_away") or g.get("score2"))
        status = str(g.get("status") or g.get("state") or "").lower()
        if status in ("scheduled", "not_started", "ns", "tbd", "upcoming", ""):
            continue
        if s1 is None or s2 is None:
            continue
        c1 = name_to_code(str(t1))
        c2 = name_to_code(str(t2))
        if not c1 or not c2:
            continue
        try:
            h, a = int(s1), int(s2)
        except (ValueError, TypeError):
            continue
        res: dict = {"home": h, "away": a}
        if h != a:
            res["winner"] = c1 if h > a else c2
        winner_field = g.get("winner") or g.get("winner_team")
        if winner_field:
            wcode = name_to_code(str(winner_field))
            if wcode in (c1, c2):
                res["winner"] = wcode
        results[frozenset([c1, c2])] = res
    return results


# ---------------------------------------------------------------------------
# Resolucao do mata-mata (importando logica do gerador)
# ---------------------------------------------------------------------------
def load_engine():
    """Importa funcoes do generate_calendar.py sem executar o main()."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "generate_calendar",
        os.path.join(HERE, "generate_calendar.py"),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Logica de mapeamento de resultados -> match_ids
# ---------------------------------------------------------------------------
def build_group_index(data: dict) -> dict[frozenset, int]:
    """Indice {frozenset(codes)} -> match_id para jogos de grupo."""
    idx: dict[frozenset, int] = {}
    for m in data["matches"]:
        if m["stage"] == "group":
            idx[frozenset([m["home"], m["away"]])] = m["id"]
    return idx


def build_ko_index(data: dict, engine) -> dict[frozenset, int]:
    """
    Resolve as referencias de todos os jogos de fase eliminatoria usando
    os resultados ja registrados. Retorna {frozenset(codes)} -> match_id
    apenas para jogos cujos dois lados ja estejam resolvidos.
    """
    idx: dict[frozenset, int] = {}
    for m in data["matches"]:
        if m["stage"] == "group":
            continue
        t1 = engine.resolve_code(data, m["home"])
        t2 = engine.resolve_code(data, m["away"])
        if t1 and t2:
            idx[frozenset([t1, t2])] = m["id"]
    return idx


# ---------------------------------------------------------------------------
# Terceiros melhores (Annex C simplificado)
# ---------------------------------------------------------------------------
def assign_thirds(data: dict, engine) -> dict[str, str]:
    """
    Detecta os 8 melhores terceiros e tenta atribuir aos slots T_ corretos.
    Retorna {slot_key: team_code}, ex.: {"T_CEFHI": "CRO"}.
    So executa quando todos os 12 grupos estao completos.
    """
    groups = data["groups"]
    # Verificar se todos os grupos estao completos
    for g in groups:
        if not engine.group_complete(data, g):
            return {}

    standings, table = engine.compute_standings(data)

    # Coletar os 12 terceiros com seus pontos/GD/GF
    thirds: list[dict] = []
    for g, teams in standings.items():
        if len(teams) >= 3:
            code = teams[2]
            stats = table[g][code]
            thirds.append({
                "code": code, "group": g,
                "pts": stats["pts"], "gd": stats["gd"], "gf": stats["gf"],
            })

    # Ordenar: melhor primeiro (pts desc, gd desc, gf desc)
    thirds.sort(key=lambda x: (-x["pts"], -x["gd"], -x["gf"]))
    best8 = thirds[:8]
    qualified_groups = {t["group"] for t in best8}
    best8_by_group = {t["group"]: t["code"] for t in best8}

    # Tentar Annex C exato (se mapeado)
    annex_key = frozenset(qualified_groups)
    if annex_key in ANNEX_C:
        mapping = ANNEX_C[annex_key]
        return {slot: best8_by_group[grp] for slot, grp in mapping.items()
                if grp in best8_by_group}

    # Fallback: atribuir cada 3o ao primeiro slot T_ que aceite seu grupo
    assignment: dict[str, str] = {}
    used_codes: set[str] = set()
    # Percorre slots em ordem, preenche com o melhor 3o compativel ainda livre
    for slot, candidate_groups in T_SLOTS_GROUPS.items():
        for grp in candidate_groups:
            code = best8_by_group.get(grp)
            if code and code not in used_codes:
                assignment[slot] = code
                used_codes.add(code)
                break

    return assignment


# ---------------------------------------------------------------------------
# Funcao principal de sincronizacao
# ---------------------------------------------------------------------------
def sync() -> bool:
    """
    Executa a sincronizacao completa. Retorna True se os dados mudaram.
    """
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}] Iniciando sync...")

    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    old_results = json.dumps(data.get("results", {}), sort_keys=True)
    old_thirds  = json.dumps(data.get("thirds", {}),  sort_keys=True)

    # --- Buscar resultados ---
    played: dict[frozenset, dict] = {}

    print("  Buscando openfootball...")
    raw_of = fetch_json(OPENFOOTBALL_URL)
    if raw_of:
        of_results = parse_openfootball(raw_of)
        played.update(of_results)
        print(f"  openfootball: {len(of_results)} jogos com placar")

    print("  Buscando worldcup26.ir...")
    raw_wc = fetch_json(WORLDCUP26_URL)
    if raw_wc:
        wc_results = parse_worldcup26(raw_wc)
        # worldcup26.ir pode ter placares mais rapidos; nao sobrescreve se
        # openfootball ja tem (mais confiavel para resultado final)
        for key, val in wc_results.items():
            if key not in played:
                played[key] = val
        print(f"  worldcup26.ir: {len(wc_results)} jogos com placar")

    if not played:
        print("  Nenhum resultado novo disponivel.")
        return False

    # --- Carregar engine ---
    engine = load_engine()

    # --- Fase de grupos: atualizar resultados ---
    group_idx = build_group_index(data)
    new_results = dict(data.get("results", {}))

    for key, res in played.items():
        mid = group_idx.get(key)
        if mid is not None:
            new_results[str(mid)] = res

    # Aplicar resultados de grupo temporariamente para resolver mata-mata
    data["results"] = new_results

    # --- Fase eliminatoria: atualizar resultados ---
    ko_idx = build_ko_index(data, engine)
    for key, res in played.items():
        mid = ko_idx.get(key)
        if mid is not None:
            new_results[str(mid)] = res

    data["results"] = new_results

    # --- Terceiros melhores (Annex C) ---
    thirds = assign_thirds(data, engine)
    if thirds:
        existing = data.get("thirds", {})
        existing.update(thirds)
        data["thirds"] = existing
        if thirds:
            print(f"  Terceiros atribuidos: {thirds}")

    # --- Verificar se mudou algo ---
    new_results_str = json.dumps(data.get("results", {}), sort_keys=True)
    new_thirds_str  = json.dumps(data.get("thirds", {}),  sort_keys=True)
    changed = (new_results_str != old_results) or (new_thirds_str != old_thirds)

    if not changed:
        print("  Sem mudancas nos resultados. Nada a fazer.")
        return False

    n_results = len(data["results"])
    print(f"  Resultados atualizados: {n_results} jogos com placar.")

    # --- Salvar data.json ---
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # --- Regenerar os .ics ---
    gen = os.path.join(HERE, "generate_calendar.py")
    proc = subprocess.run([sys.executable, gen], capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"  [ERRO] generate_calendar.py: {proc.stderr}", file=sys.stderr)
        return False
    print(f"  {proc.stdout.strip()}")
    return True


if __name__ == "__main__":
    changed = sync()
    sys.exit(0)  # sempre sai 0; o workflow decide o commit baseado em git diff

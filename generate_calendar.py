#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de calendarios da Copa do Mundo FIFA 2026.

Le data/data.json e gera dois arquivos:
  - copa_2026_icalendar.ics  -> iCalendar padrao (RFC 5545): Apple, Google, Thunderbird...
  - copa_2026_outlook.ics     -> .ics ajustado para o Microsoft Outlook

Recursos:
  * Titulo: <bandeira> <SIGLA> x <bandeira> <SIGLA> - <fase / grupo>
  * Local : nome do estadio (+ cidade/pais)
  * Mostrar como LIVRE (TRANSP:TRANSPARENT + X-MICROSOFT-CDO-BUSYSTATUS:FREE no Outlook)
  * Lembrete 15 min antes (VALARM)
  * Notas : fato relevante + plantel de cada selecao (n., nome, posicao) + esquema + tecnico
  * "Inteligente": o mata-mata se preenche sozinho (pais + bandeira) a partir de 'results'.

Uso: python3 generate_calendar.py
"""

import json
import os
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "data", "data.json")
OUT_ICAL = os.path.join(HERE, "copa_2026_icalendar.ics")
OUT_OUTLOOK = os.path.join(HERE, "copa_2026_outlook.ics")

STAGE_LABELS = {
    "group": "Fase de Grupos",
    "r32":   "16-avos de final",
    "r16":   "Oitavas de final",
    "qf":    "Quartas de final",
    "sf":    "Semifinal",
    "third": "Disputa pelo 3o lugar",
    "final": "Final",
}
POS_ORDER = ["GOL", "DEF", "MEI", "ATA"]


# ----------------------------------------------------------------------------
# Classificacao dos grupos a partir dos resultados
# ----------------------------------------------------------------------------
def group_matches(data, g):
    return [m for m in data["matches"] if m.get("stage") == "group" and m.get("group") == g]


def group_complete(data, g):
    """True se todos os jogos do grupo ja tem resultado em 'results'."""
    results = data.get("results", {})
    ms = group_matches(data, g)
    if not ms:
        return False
    return all(str(m["id"]) in results for m in ms)


def compute_standings(data):
    """Retorna {grupo: [codigos ordenados 1o..4o]} usando os resultados conhecidos."""
    groups = data["groups"]
    results = data.get("results", {})
    matches = {str(m["id"]): m for m in data["matches"]}

    table = {g: {code: {"pts": 0, "gf": 0, "ga": 0, "gd": 0} for code in codes}
             for g, codes in groups.items()}

    for mid, res in results.items():
        m = matches.get(str(mid))
        if not m or m.get("stage") != "group":
            continue
        g = m["group"]
        home, away = m["home"], m["away"]
        if home not in table.get(g, {}) or away not in table.get(g, {}):
            continue
        hg, ag = res["home"], res["away"]
        table[g][home]["gf"] += hg; table[g][home]["ga"] += ag
        table[g][away]["gf"] += ag; table[g][away]["ga"] += hg
        if hg > ag:
            table[g][home]["pts"] += 3
        elif ag > hg:
            table[g][away]["pts"] += 3
        else:
            table[g][home]["pts"] += 1
            table[g][away]["pts"] += 1

    standings = {}
    for g, codes in groups.items():
        for c in codes:
            table[g][c]["gd"] = table[g][c]["gf"] - table[g][c]["ga"]
        ordered = sorted(
            codes,
            key=lambda c: (-table[g][c]["pts"], -table[g][c]["gd"], -table[g][c]["gf"], codes.index(c)),
        )
        standings[g] = ordered
    return standings, table


def winner_loser(data, match_id):
    """(vencedor, perdedor) de um jogo ja resolvido; senao (None, None)."""
    results = data.get("results", {})
    res = results.get(str(match_id))
    if not res:
        return None, None
    m = next((x for x in data["matches"] if str(x["id"]) == str(match_id)), None)
    if not m:
        return None, None
    home = resolve_code(data, m["home"])
    away = resolve_code(data, m["away"])
    if not home or not away:
        return None, None
    hg, ag = res["home"], res["away"]
    if hg == ag:
        w = res.get("winner")
        if w in (home, away):
            return w, (away if w == home else home)
        return None, None
    if hg > ag:
        return home, away
    return away, home


def resolve_code(data, ref):
    """
    Resolve uma referencia de mando para um codigo real, se ja definido:
      - 'BRA'      -> 'BRA' (ja e um time)
      - '1A'/'2B'  -> 1o/2o do grupo (SO depois que o grupo termina)
      - 'W73'      -> vencedor do jogo 73
      - 'L101'     -> perdedor do jogo 101
      - 'T_ABCDF'  -> melhor 3o de um conjunto de grupos (nunca auto-resolve)
    Retorna o codigo (str) ou None se ainda nao definido.
    """
    if not ref:
        return None
    if ref in data["teams"] and ref[0].isalpha() and not ref.startswith(("W", "L", "T_")) \
            and not (len(ref) == 2 and ref[0] in "12"):
        # codigo real de selecao (ex.: BRA, MEX). Evita pegar refs tipo '1A'.
        if not (len(ref) == 2 and ref[0] in "12" and ref[1:].isalpha()):
            return ref
    # 1o/2o colocado de um grupo
    if len(ref) >= 2 and ref[0] in "12" and ref[1:].isalpha():
        grp = ref[1:]
        if not group_complete(data, grp):
            return None  # placeholder ate o grupo terminar
        pos = int(ref[0]) - 1
        standings, _ = compute_standings(data)
        ordered = standings.get(grp, [])
        if len(ordered) > pos:
            return ordered[pos]
        return None
    if ref.startswith("W"):
        w, _ = winner_loser(data, ref[1:])
        return w
    if ref.startswith("L"):
        _, l = winner_loser(data, ref[1:])
        return l
    if ref.startswith("T_"):
        # melhor 3o lugar: definido manualmente em 'thirds' (ref -> codigo)
        return data.get("thirds", {}).get(ref)
    return None


# ----------------------------------------------------------------------------
# Rotulos do evento
# ----------------------------------------------------------------------------
def side_label(data, ref):
    """Texto de um lado: '<bandeira> SIGLA' (resolvido) ou placeholder legivel."""
    code = resolve_code(data, ref)
    if code and code in data["teams"]:
        t = data["teams"][code]
        flag = t.get("flag", "\U0001F3F3\uFE0F")
        return f"{flag} {code}"
    # placeholders legiveis
    if len(ref) >= 2 and ref[0] in "12" and ref[1:].isalpha():
        return f"\u2753 {ref[0]}o Grupo {ref[1:]}"
    if ref.startswith("W"):
        return f"\u2753 Vencedor jogo {ref[1:]}"
    if ref.startswith("L"):
        return f"\u2753 Perdedor jogo {ref[1:]}"
    if ref.startswith("T_"):
        grupos = "/".join(list(ref[2:]))
        return f"\u2753 Melhor 3o ({grupos})"
    if ref in data.get("teams", {}):
        return f"\u2753 {data['teams'][ref].get('name', ref)}"
    return f"\u2753 {ref}"


def stage_text(m):
    base = STAGE_LABELS.get(m["stage"], m["stage"])
    if m["stage"] == "group":
        return f"{base} - Grupo {m['group']}"
    return base


def build_title(data, m):
    h = side_label(data, m["home"])
    a = side_label(data, m["away"])
    return f"{h} x {a} \u2014 {stage_text(m)}"


def squad_block(data, code):
    if not code or code not in data["teams"]:
        return None
    t = data["teams"][code]
    head = f"{t.get('flag','')} {t['name']}"
    extras = []
    if t.get("formation"):
        extras.append(t["formation"])
    if t.get("coach"):
        extras.append(f"Tec. {t['coach']}")
    if extras:
        head += " (" + " | ".join(extras) + ")"

    squad = t.get("squad", [])
    lines = [head]
    if not squad:
        lines.append("  (escalacao a confirmar)")
        return "\n".join(lines)

    by_pos = {p: [] for p in POS_ORDER}
    for pl in squad:
        by_pos.setdefault(pl.get("pos", "MEI"), []).append(pl)
    for p in POS_ORDER:
        players = sorted(by_pos.get(p, []), key=lambda x: x.get("n", 99) if x.get("n") else 99)
        if players:
            parts = []
            for pl in players:
                n = pl.get("n")
                parts.append(f"{n}. {pl.get('name','?')}" if n else f"{pl.get('name','?')}")
            lines.append(f"  {p}: " + ", ".join(parts))
    return "\n".join(lines)


def build_description(data, m):
    parts = []
    fact = (m.get("fact") or "").strip()
    if fact:
        parts.append(f"\u26bd {fact}")

    h_code = resolve_code(data, m["home"])
    a_code = resolve_code(data, m["away"])
    h_block = squad_block(data, h_code)
    a_block = squad_block(data, a_code)
    if h_block or a_block:
        parts.append("")
        parts.append("\U0001F4CB PLANTEIS")
        if h_block:
            parts.append(h_block)
        if a_block:
            parts.append("")
            parts.append(a_block)
    else:
        parts.append("")
        parts.append("(Confronto a definir \u2014 sera preenchido conforme a classificacao avanca.)")
    return "\n".join(parts)


# ----------------------------------------------------------------------------
# Escrita do .ics (RFC 5545)
# ----------------------------------------------------------------------------
def esc(text):
    if text is None:
        text = ""
    return (text.replace("\\", "\\\\")
                .replace(";", "\\;")
                .replace(",", "\\,")
                .replace("\n", "\\n"))


def fold(line):
    """Dobra linhas > 73 octetos (RFC 5545), preservando UTF-8 e usando CRLF + espaco."""
    raw = line.encode("utf-8")
    if len(raw) <= 73:
        return line
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > 73:
            out.append(cur)
            cur = b" " + b
        else:
            cur += b
    out.append(cur)
    return "\r\n".join(seg.decode("utf-8") for seg in out)


def dt_utc(s):
    d = datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    return d.strftime("%Y%m%dT%H%M%SZ")


def build_calendar(data, flavor):
    cal = data["calendar"]
    venues = data["venues"]
    refresh = int(cal.get("refresh_hours", 6))
    dur = int(cal.get("default_match_minutes", 120))
    reminder = int(cal.get("reminder_minutes_before", 15))
    seq = len(data.get("results", {}))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    L = []
    L.append("BEGIN:VCALENDAR")
    L.append("VERSION:2.0")
    L.append("PRODID:-//Copa 2026//Gerador de Calendario//PT-BR")
    L.append("CALSCALE:GREGORIAN")
    L.append("METHOD:PUBLISH")
    L.append(f"X-WR-CALNAME:{esc(cal['name'])}")
    L.append(f"X-WR-CALDESC:{esc(cal.get('description',''))}")
    L.append("X-WR-TIMEZONE:UTC")
    L.append(f"REFRESH-INTERVAL;VALUE=DURATION:PT{refresh}H")
    L.append(f"X-PUBLISHED-TTL:PT{refresh}H")
    if flavor == "outlook":
        L.append("X-MS-OLK-FORCEINSPECTOROPEN:TRUE")

    for m in data["matches"]:
        start = dt_utc(m["datetime_utc"])
        end_dt = datetime.fromisoformat(m["datetime_utc"].replace("Z", "+00:00")) + timedelta(minutes=dur)
        end = end_dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        v = venues.get(m["venue"], {})
        location = v.get("stadium", "")
        if v.get("city"):
            location += f", {v['city']}"
        if v.get("country"):
            location += f" ({v['country']})"

        title = build_title(data, m)
        desc = build_description(data, m)

        L.append("BEGIN:VEVENT")
        L.append(f"UID:fifa2026-match-{m['id']}@copa2026")
        L.append(f"SEQUENCE:{seq}")
        L.append(f"DTSTAMP:{stamp}")
        L.append(f"DTSTART:{start}")
        L.append(f"DTEND:{end}")
        L.append(f"SUMMARY:{esc(title)}")
        L.append(f"LOCATION:{esc(location)}")
        L.append(f"DESCRIPTION:{esc(desc)}")
        L.append("TRANSP:TRANSPARENT")          # mostrar como LIVRE (iCalendar padrao)
        if flavor == "outlook":
            L.append("X-MICROSOFT-CDO-BUSYSTATUS:FREE")
            L.append("X-MICROSOFT-CDO-INTENDEDSTATUS:FREE")
            L.append("X-MICROSOFT-CDO-ALLDAYEVENT:FALSE")
            L.append("X-MICROSOFT-DISALLOW-COUNTER:TRUE")
        L.append("STATUS:CONFIRMED")
        L.append("CATEGORIES:Copa do Mundo FIFA 2026")
        L.append("BEGIN:VALARM")
        L.append("ACTION:DISPLAY")
        L.append(f"DESCRIPTION:{esc('Lembrete: ' + title)}")
        L.append(f"TRIGGER:-PT{reminder}M")
        L.append("END:VALARM")
        L.append("END:VEVENT")

    L.append("END:VCALENDAR")
    return "\r\n".join(fold(x) for x in L) + "\r\n"


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    with open(OUT_ICAL, "w", encoding="utf-8", newline="") as f:
        f.write(build_calendar(data, "ical"))
    with open(OUT_OUTLOOK, "w", encoding="utf-8", newline="") as f:
        f.write(build_calendar(data, "outlook"))
    print(f"OK: {len(data['matches'])} jogos -> {os.path.basename(OUT_ICAL)} e {os.path.basename(OUT_OUTLOOK)}")
    print(f"Resultados conhecidos: {len(data.get('results', {}))}")


if __name__ == "__main__":
    main()

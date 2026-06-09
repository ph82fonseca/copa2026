# -*- coding: utf-8 -*-
"""Constroi data/data.json a partir de listas compactas e verificadas."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

VENUES = {
    "azteca":   {"stadium": "Estadio Azteca",          "city": "Cidade do Mexico", "country": "Mexico"},
    "akron":    {"stadium": "Estadio Akron",           "city": "Guadalajara",      "country": "Mexico"},
    "bbva":     {"stadium": "Estadio BBVA",            "city": "Monterrey",        "country": "Mexico"},
    "bmo":      {"stadium": "BMO Field",               "city": "Toronto",          "country": "Canada"},
    "bcplace":  {"stadium": "BC Place",                "city": "Vancouver",        "country": "Canada"},
    "metlife":  {"stadium": "MetLife Stadium",         "city": "Nova York/Nova Jersey", "country": "EUA"},
    "sofi":     {"stadium": "SoFi Stadium",            "city": "Los Angeles",      "country": "EUA"},
    "att":      {"stadium": "AT&T Stadium",            "city": "Dallas",           "country": "EUA"},
    "nrg":      {"stadium": "NRG Stadium",             "city": "Houston",          "country": "EUA"},
    "arrowhead":{"stadium": "Arrowhead Stadium",       "city": "Kansas City",      "country": "EUA"},
    "mercedes": {"stadium": "Mercedes-Benz Stadium",   "city": "Atlanta",          "country": "EUA"},
    "hardrock": {"stadium": "Hard Rock Stadium",       "city": "Miami",            "country": "EUA"},
    "lincoln":  {"stadium": "Lincoln Financial Field", "city": "Filadelfia",       "country": "EUA"},
    "levis":    {"stadium": "Levi's Stadium",          "city": "San Francisco (Bay Area)", "country": "EUA"},
    "lumen":    {"stadium": "Lumen Field",             "city": "Seattle",          "country": "EUA"},
    "gillette": {"stadium": "Gillette Stadium",        "city": "Boston",           "country": "EUA"},
}

# codigo FIFA -> (nome PT, bandeira)
TEAMS = {
    "MEX": ("Mexico", "\U0001F1F2\U0001F1FD"), "KOR": ("Coreia do Sul", "\U0001F1F0\U0001F1F7"),
    "RSA": ("Africa do Sul", "\U0001F1FF\U0001F1E6"), "CZE": ("Tchequia", "\U0001F1E8\U0001F1FF"),
    "CAN": ("Canada", "\U0001F1E8\U0001F1E6"), "SUI": ("Suica", "\U0001F1E8\U0001F1ED"),
    "QAT": ("Catar", "\U0001F1F6\U0001F1E6"), "BIH": ("Bosnia e Herzegovina", "\U0001F1E7\U0001F1E6"),
    "BRA": ("Brasil", "\U0001F1E7\U0001F1F7"), "MAR": ("Marrocos", "\U0001F1F2\U0001F1E6"),
    "SCO": ("Escocia", "\U0001F3F4\U000E0067\U000E0062\U000E0073\U000E0063\U000E0074\U000E007F"),
    "HAI": ("Haiti", "\U0001F1ED\U0001F1F9"),
    "USA": ("Estados Unidos", "\U0001F1FA\U0001F1F8"), "AUS": ("Australia", "\U0001F1E6\U0001F1FA"),
    "PAR": ("Paraguai", "\U0001F1F5\U0001F1FE"), "TUR": ("Turquia", "\U0001F1F9\U0001F1F7"),
    "GER": ("Alemanha", "\U0001F1E9\U0001F1EA"), "ECU": ("Equador", "\U0001F1EA\U0001F1E8"),
    "CIV": ("Costa do Marfim", "\U0001F1E8\U0001F1EE"), "CUW": ("Curacao", "\U0001F1E8\U0001F1FC"),
    "NED": ("Paises Baixos", "\U0001F1F3\U0001F1F1"), "JPN": ("Japao", "\U0001F1EF\U0001F1F5"),
    "TUN": ("Tunisia", "\U0001F1F9\U0001F1F3"), "SWE": ("Suecia", "\U0001F1F8\U0001F1EA"),
    "BEL": ("Belgica", "\U0001F1E7\U0001F1EA"), "IRN": ("Ira", "\U0001F1EE\U0001F1F7"),
    "EGY": ("Egito", "\U0001F1EA\U0001F1EC"), "NZL": ("Nova Zelandia", "\U0001F1F3\U0001F1FF"),
    "ESP": ("Espanha", "\U0001F1EA\U0001F1F8"), "URU": ("Uruguai", "\U0001F1FA\U0001F1FE"),
    "KSA": ("Arabia Saudita", "\U0001F1F8\U0001F1E6"), "CPV": ("Cabo Verde", "\U0001F1E8\U0001F1FB"),
    "FRA": ("Franca", "\U0001F1EB\U0001F1F7"), "SEN": ("Senegal", "\U0001F1F8\U0001F1F3"),
    "NOR": ("Noruega", "\U0001F1F3\U0001F1F4"), "IRQ": ("Iraque", "\U0001F1EE\U0001F1F6"),
    "ARG": ("Argentina", "\U0001F1E6\U0001F1F7"), "AUT": ("Austria", "\U0001F1E6\U0001F1F9"),
    "ALG": ("Argelia", "\U0001F1E9\U0001F1FF"), "JOR": ("Jordania", "\U0001F1EF\U0001F1F4"),
    "POR": ("Portugal", "\U0001F1F5\U0001F1F9"), "COL": ("Colombia", "\U0001F1E8\U0001F1F4"),
    "UZB": ("Uzbequistao", "\U0001F1FA\U0001F1FF"), "COD": ("RD Congo", "\U0001F1E8\U0001F1E9"),
    "ENG": ("Inglaterra", "\U0001F3F4\U000E0067\U000E0062\U000E0065\U000E006E\U000E0067\U000E007F"),
    "CRO": ("Croacia", "\U0001F1ED\U0001F1F7"), "PAN": ("Panama", "\U0001F1F5\U0001F1E6"),
    "GHA": ("Gana", "\U0001F1EC\U0001F1ED"),
}

# ordem de posicao no grupo (1..4) -> usada para classificacao/desempate inicial
GROUPS = {
    "A": ["MEX", "RSA", "KOR", "CZE"],
    "B": ["CAN", "BIH", "QAT", "SUI"],
    "C": ["BRA", "MAR", "HAI", "SCO"],
    "D": ["USA", "PAR", "AUS", "TUR"],
    "E": ["GER", "CUW", "CIV", "ECU"],
    "F": ["NED", "JPN", "SWE", "TUN"],
    "G": ["BEL", "EGY", "IRN", "NZL"],
    "H": ["ESP", "CPV", "KSA", "URU"],
    "I": ["FRA", "SEN", "IRQ", "NOR"],
    "J": ["ARG", "ALG", "AUT", "JOR"],
    "K": ["POR", "COD", "UZB", "COL"],
    "L": ["ENG", "CRO", "GHA", "PAN"],
}

# (id, stage, group, home, away, datetime_utc, venue)
# horarios da fase de grupos: ET (EDT, UTC-4) + 4h = UTC. Mata-mata: melhores horarios
# disponiveis (alguns ainda sujeitos a confirmacao da FIFA).
M = [
    # ---- GRUPO A ----
    (1,"group","A","MEX","RSA","2026-06-11T19:00:00Z","azteca"),
    (2,"group","A","KOR","CZE","2026-06-12T02:00:00Z","akron"),
    (3,"group","A","CZE","RSA","2026-06-18T16:00:00Z","mercedes"),
    (4,"group","A","MEX","KOR","2026-06-19T01:00:00Z","akron"),
    (5,"group","A","CZE","MEX","2026-06-25T01:00:00Z","azteca"),
    (6,"group","A","RSA","KOR","2026-06-25T01:00:00Z","bbva"),
    # ---- GRUPO B ----
    (7,"group","B","CAN","BIH","2026-06-12T19:00:00Z","bmo"),
    (8,"group","B","QAT","SUI","2026-06-13T19:00:00Z","levis"),
    (9,"group","B","SUI","BIH","2026-06-18T19:00:00Z","sofi"),
    (10,"group","B","CAN","QAT","2026-06-18T22:00:00Z","bcplace"),
    (11,"group","B","SUI","CAN","2026-06-24T19:00:00Z","bcplace"),
    (12,"group","B","BIH","QAT","2026-06-24T19:00:00Z","lumen"),
    # ---- GRUPO C ----
    (13,"group","C","BRA","MAR","2026-06-13T22:00:00Z","metlife"),
    (14,"group","C","HAI","SCO","2026-06-14T01:00:00Z","gillette"),
    (15,"group","C","SCO","MAR","2026-06-19T22:00:00Z","gillette"),
    (16,"group","C","BRA","HAI","2026-06-20T00:30:00Z","lincoln"),
    (17,"group","C","SCO","BRA","2026-06-24T22:00:00Z","hardrock"),
    (18,"group","C","MAR","HAI","2026-06-24T22:00:00Z","mercedes"),
    # ---- GRUPO D ----
    (19,"group","D","USA","PAR","2026-06-13T01:00:00Z","sofi"),
    (20,"group","D","AUS","TUR","2026-06-14T04:00:00Z","bcplace"),
    (21,"group","D","USA","AUS","2026-06-19T19:00:00Z","lumen"),
    (22,"group","D","TUR","PAR","2026-06-20T03:00:00Z","levis"),
    (23,"group","D","TUR","USA","2026-06-26T02:00:00Z","sofi"),
    (24,"group","D","PAR","AUS","2026-06-26T02:00:00Z","levis"),
    # ---- GRUPO E ----
    (25,"group","E","GER","CUW","2026-06-14T17:00:00Z","nrg"),
    (26,"group","E","CIV","ECU","2026-06-14T23:00:00Z","lincoln"),
    (27,"group","E","GER","CIV","2026-06-20T20:00:00Z","bmo"),
    (28,"group","E","ECU","CUW","2026-06-21T00:00:00Z","arrowhead"),
    (29,"group","E","CUW","CIV","2026-06-25T20:00:00Z","lincoln"),
    (30,"group","E","ECU","GER","2026-06-25T20:00:00Z","metlife"),
    # ---- GRUPO F ----
    (31,"group","F","NED","JPN","2026-06-14T20:00:00Z","att"),
    (32,"group","F","SWE","TUN","2026-06-15T02:00:00Z","bbva"),
    (33,"group","F","NED","SWE","2026-06-20T17:00:00Z","nrg"),
    (34,"group","F","TUN","JPN","2026-06-21T04:00:00Z","bbva"),
    (35,"group","F","JPN","SWE","2026-06-25T23:00:00Z","att"),
    (36,"group","F","TUN","NED","2026-06-25T23:00:00Z","arrowhead"),
    # ---- GRUPO G ----
    (37,"group","G","BEL","EGY","2026-06-15T19:00:00Z","lumen"),
    (38,"group","G","IRN","NZL","2026-06-16T01:00:00Z","sofi"),
    (39,"group","G","BEL","IRN","2026-06-21T19:00:00Z","sofi"),
    (40,"group","G","NZL","EGY","2026-06-22T01:00:00Z","bcplace"),
    (41,"group","G","EGY","IRN","2026-06-27T03:00:00Z","lumen"),
    (42,"group","G","NZL","BEL","2026-06-27T03:00:00Z","bcplace"),
    # ---- GRUPO H ----
    (43,"group","H","ESP","CPV","2026-06-15T16:00:00Z","mercedes"),
    (44,"group","H","KSA","URU","2026-06-15T22:00:00Z","hardrock"),
    (45,"group","H","ESP","KSA","2026-06-21T16:00:00Z","mercedes"),
    (46,"group","H","URU","CPV","2026-06-21T22:00:00Z","hardrock"),
    (47,"group","H","CPV","KSA","2026-06-27T00:00:00Z","nrg"),
    (48,"group","H","URU","ESP","2026-06-27T00:00:00Z","akron"),
    # ---- GRUPO I ----
    (49,"group","I","FRA","SEN","2026-06-16T19:00:00Z","metlife"),
    (50,"group","I","IRQ","NOR","2026-06-16T22:00:00Z","gillette"),
    (51,"group","I","FRA","IRQ","2026-06-22T21:00:00Z","lincoln"),
    (52,"group","I","NOR","SEN","2026-06-23T00:00:00Z","metlife"),
    (53,"group","I","NOR","FRA","2026-06-26T19:00:00Z","gillette"),
    (54,"group","I","SEN","IRQ","2026-06-26T19:00:00Z","bmo"),
    # ---- GRUPO J ----
    (55,"group","J","ARG","ALG","2026-06-17T01:00:00Z","arrowhead"),
    (56,"group","J","AUT","JOR","2026-06-17T04:00:00Z","levis"),
    (57,"group","J","ARG","AUT","2026-06-22T17:00:00Z","att"),
    (58,"group","J","JOR","ALG","2026-06-23T03:00:00Z","levis"),
    (59,"group","J","JOR","ARG","2026-06-28T02:00:00Z","att"),
    (60,"group","J","ALG","AUT","2026-06-28T02:00:00Z","arrowhead"),
    # ---- GRUPO K ----
    (61,"group","K","POR","COD","2026-06-17T17:00:00Z","nrg"),
    (62,"group","K","UZB","COL","2026-06-18T02:00:00Z","azteca"),
    (63,"group","K","POR","UZB","2026-06-23T17:00:00Z","nrg"),
    (64,"group","K","COL","COD","2026-06-24T02:00:00Z","akron"),
    (65,"group","K","COL","POR","2026-06-27T23:30:00Z","hardrock"),
    (66,"group","K","COD","UZB","2026-06-27T23:30:00Z","mercedes"),
    # ---- GRUPO L ----
    (67,"group","L","ENG","CRO","2026-06-17T20:00:00Z","att"),
    (68,"group","L","GHA","PAN","2026-06-17T23:00:00Z","bmo"),
    (69,"group","L","ENG","GHA","2026-06-23T20:00:00Z","gillette"),
    (70,"group","L","PAN","CRO","2026-06-23T23:00:00Z","bmo"),
    (71,"group","L","PAN","ENG","2026-06-27T21:00:00Z","metlife"),
    (72,"group","L","CRO","GHA","2026-06-27T21:00:00Z","lincoln"),
    # ---- 16-AVOS (R32) ----  ref de 3o lugar: T_<grupos candidatos>
    (73,"r32",None,"2A","2B","2026-06-28T19:00:00Z","sofi"),
    (74,"r32",None,"1E","T_ABCDF","2026-06-29T20:30:00Z","gillette"),
    (75,"r32",None,"1F","2C","2026-06-30T01:00:00Z","bbva"),
    (76,"r32",None,"1C","2F","2026-06-29T17:00:00Z","nrg"),
    (77,"r32",None,"1I","T_CDFGH","2026-06-30T21:00:00Z","metlife"),
    (78,"r32",None,"2E","2I","2026-06-30T17:00:00Z","att"),
    (79,"r32",None,"1A","T_CEFHI","2026-07-01T01:00:00Z","azteca"),
    (80,"r32",None,"1L","T_EHIJK","2026-07-01T16:00:00Z","mercedes"),
    (81,"r32",None,"1D","T_BEFIJ","2026-07-02T00:00:00Z","levis"),
    (82,"r32",None,"1G","T_AEHIJ","2026-07-02T03:00:00Z","lumen"),
    (83,"r32",None,"2K","2L","2026-07-02T23:00:00Z","bmo"),
    (84,"r32",None,"1H","2J","2026-07-02T19:00:00Z","sofi"),
    (85,"r32",None,"1B","T_EFGIJ","2026-07-03T03:00:00Z","bcplace"),
    (86,"r32",None,"1J","2H","2026-07-03T22:00:00Z","hardrock"),
    (87,"r32",None,"1K","T_DEIJL","2026-07-04T01:30:00Z","arrowhead"),
    (88,"r32",None,"2D","2G","2026-07-03T18:00:00Z","att"),
    # ---- OITAVAS (R16) ----
    (89,"r16",None,"W74","W77","2026-07-04T21:00:00Z","lincoln"),
    (90,"r16",None,"W73","W75","2026-07-04T17:00:00Z","nrg"),
    (91,"r16",None,"W76","W78","2026-07-05T20:00:00Z","metlife"),
    (92,"r16",None,"W79","W80","2026-07-06T00:00:00Z","azteca"),
    (93,"r16",None,"W83","W84","2026-07-06T19:00:00Z","att"),
    (94,"r16",None,"W81","W82","2026-07-07T00:00:00Z","lumen"),
    (95,"r16",None,"W86","W88","2026-07-07T16:00:00Z","mercedes"),
    (96,"r16",None,"W85","W87","2026-07-07T20:00:00Z","bcplace"),
    # ---- QUARTAS ----
    (97,"qf",None,"W89","W90","2026-07-09T20:00:00Z","gillette"),
    (98,"qf",None,"W93","W94","2026-07-10T19:00:00Z","sofi"),
    (99,"qf",None,"W91","W92","2026-07-11T21:00:00Z","hardrock"),
    (100,"qf",None,"W95","W96","2026-07-12T01:00:00Z","arrowhead"),
    # ---- SEMIS ----
    (101,"sf",None,"W97","W98","2026-07-14T19:00:00Z","att"),
    (102,"sf",None,"W99","W100","2026-07-15T19:00:00Z","mercedes"),
    # ---- 3o LUGAR / FINAL ----
    (103,"third",None,"L101","L102","2026-07-18T21:00:00Z","hardrock"),
    (104,"final",None,"W101","W102","2026-07-19T19:00:00Z","metlife"),
]

# Fatos especificos (id -> texto). Os demais recebem um fato contextual gerado.
FACTS = {
# ─── GRUPO A ──────────────────────────────────────────────────────────────
1: "O Estádio Azteca se torna o único da história a receber jogos de três Copas do Mundo masculinas (1970, 1986 e 2026). O México, anfitrião com uma das torcidas mais ruidosas do planeta, precisa de vitória diante de 80 mil fãs para sinalizar que levará este torneio a sério. A África do Sul, que em 2010 sediou a Copa, chega sem nada a perder e com tudo a ganhar.",
2: "Son Heung-min chega a esta Copa como um dos capitães mais respeitados do futebol europeu e lider incontestável da Coreia do Sul. A Tchequia retorna a uma Copa pela primeira vez desde 2006 e aposta em organização defensiva e contra-ataques rápidos. O vencedor assume a liderança provisória do Grupo A.",
3: "África do Sul e Tchequia se enfrentam em Atlanta em um duelo de 'mata ou morre': o perdedor fica praticamente eliminado. A Tchequia depende de uma vitória para se manter viva no torneio; os sul-africanos querem repetir o espírito combativo da geração que animou o mundo em 2010. Um jogo com o peso de uma eliminação precoce pairando sobre cada lance.",
4: "Dois estilos opostos se encontram em Guadalajara: a organização e a velocidade de transição coreana, liderada por Son Heung-min, contra a criatividade técnica mexicana diante de um caldeirão anfitrião. A Coreia do Sul foi a sensação de 2002 (semifinalista) e desbancou Alemanha e Espanha no grupo de 2022 — não tem medo de ninguém. O vencedor quase certamente garante vaga no mata-mata.",
5: "No Azteca, a última chance do México de confirmar a liderança do Grupo A diante de sua torcida. A Tchequia, precisando de pontos para avançar, vai ao ataque sem nada a perder — exatamente o tipo de adversário que pode complicar um anfitrião. Um resultado que pode definir o caminho do México até a final.",
6: "Em jogo simultâneo ao México vs. Tchequia, África do Sul e Coreia do Sul disputam a segunda vaga no Estadio BBVA, em Monterrey. Son Heung-min e Percy Tau — dois dos melhores jogadores que já passaram pelo futebol africano e asiático — podem protagonizar a disputa mais equilibrada da última rodada do Grupo A.",
# ─── GRUPO B ──────────────────────────────────────────────────────────────
7: "O Canadá abre o torneio em casa no BMO Field de Toronto — a segunda aparição histórica do país numa Copa, a primeira desde 1986. Alfonso Davies, um dos melhores laterais-esquerdos do mundo pelo Bayern de Munique, é o principal nome; a Bósnia, que eliminou a Itália na repescagem europeia, não veio como turista.",
8: "O Catar disputa pela primeira vez uma Copa por mérito próprio — em 2022 entrou automaticamente como anfitrião e foi eliminado na fase de grupos sem vencer. A Suíça, uma das seleções mais consistentes da Europa nos últimos dez anos, é favorita — mas os qatarianos vão querer provar que merecem estar aqui.",
9: "A Suíça, máquina de regularidade europeia, enfrenta a Bósnia no SoFi Stadium, em Los Angeles. Os bósnios têm uma identidade ofensiva marcante e vão tentar jogar em velocidade para desequilibrar a sólida defesa helvética. Um jogo europeu transplantado para a Califórnia.",
10: "O Canadá precisa de uma vitória sobre o Catar no BC Place, em Vancouver, para praticamente garantir as oitavas na frente de sua torcida. Davies, Jonathan David e Jacob Shaffelburg são as armas ofensivas de uma seleção que quer fazer história nesta Copa. Um estádio fechado que vai criar uma atmosfera única.",
11: "Suíça e Canadá fecham o Grupo B no BC Place num duelo que pode definir quem vai como líder ao mata-mata. O aproveitamento do adversário nas oitavas varia muito dependendo desta posição, então ambos os times vão ao ataque em busca da primeira colocação.",
12: "Bósnia e Catar em Seattle: dois times que precisam de pontos para sobreviver no torneio — um drama de última rodada que pode ter a intensidade de um jogo eliminatório. O Catar, eliminado sem vencer em 2022, vai ao campo pelo orgulho de, pelo menos, marcar um gol numa Copa disputada.",
# ─── GRUPO C ──────────────────────────────────────────────────────────────
13: "A CNN elegeu este como um dos 10 melhores jogos da fase de grupos. Brasil estreia com Carlo Ancelotti no comando — o lendário técnico italiano que venceu a Champions com o Real Madrid — contra o Marrocos, campeão africano e semifinalista de 2022. Vinícius Jr., Raphinha e Endrick lideram o ataque; do outro lado, Brahim Díaz, Achraf Hakimi e o goleiro Yassine Bounou formam um Marrocos que não é mais surpresa: é potência.",
14: "O Haiti faz sua primeira aparição numa Copa do Mundo desde 1974 — mais de 50 anos de espera para o futebol haitiano. A Escócia, sempre apaixonada mas jamais capaz de superar a fase de grupos numa Copa, entra com a missão de finalmente escrever um capítulo diferente. Dois países com histórias complexas e torcidas de coração partido disputam neste jogo muito mais do que três pontos.",
15: "A Escócia enfrenta o Marrocos — campeão africano e semifinalista de 2022 — no Gillette Stadium, em Boston, numa batalha que pode definir quem acompanha o Brasil nas oitavas. Scott McTominay (Manchester City) lidera os escoceses; Hakimi e Brahim Díaz são as armas marroquinas. Uma vitória escocesa seria uma das grandes surpresas da Copa.",
16: "Brasil e Haiti, em Filadelfia: no papel, uma formalidade para a Seleção. Na história do futebol, porém, Copas guardam momentos inesquecíveis exatamente neste tipo de jogo. Vinícius Jr. e Endrick devem ser os protagonistas; o Haiti vai jogar em homenagem a um povo que sonha grande mesmo quando os recursos são pequenos.",
17: "No Hard Rock Stadium de Miami — casa da NFL e de grandes shows — Brasil e Escócia encerram o Grupo C. Com a Seleção possivelmente já classificada, Ancelotti pode poupar titulares para o mata-mata. Para os escoceses, cada minuto é a última chance de deixar uma marca neste Mundial.",
18: "Marrocos e Haiti fecham o Grupo C em Atlanta com a segunda vaga em disputa. Os marroquinos, favoritos absolutos, encerram a fase de grupos com a responsabilidade de confirmar o status de potência continental. O Haiti vai entrar em campo pelo orgulho de disputar uma Copa do Mundo após décadas de ausência.",
# ─── GRUPO D ──────────────────────────────────────────────────────────────
19: "Os Estados Unidos, um dos anfitriões, abrem o torneio diante de seu público no SoFi Stadium, em Los Angeles — a arena de 70 mil lugares do NFL. Mauricio Pochettino, o técnico argentino que transformou o Paris Saint-Germain, tem a missão de levar os americanos mais longe do que qualquer geração anterior. O Paraguai, clássico sul-americano difícil de bater, será o primeiro teste desta jornada.",
20: "A Turquia está de volta a uma Copa após 24 anos de ausência — a geração de 2002 ficou em terceiro lugar, a melhor campanha do país. Arda Güler, a joia do Real Madrid, faz aqui sua estreia num Mundial. A Austrália, que chegou às semifinais em 2006 com Tim Cahill, tem uma nova geração querendo repetir o feito histórico.",
21: "Dois países de língua inglesa com culturas esportivas fortes se enfrentam em Seattle. Os EUA de Pochettino buscam a segunda vitória; os australianos, liderados pelo goleiro Mathew Ryan, apostam numa organização defensiva que complica qualquer adversário. Um jogo entre dois times que jogam futebol com a garra de quem cresceu em outras tradições esportivas.",
22: "Arda Güler — 20 anos, Real Madrid, já comparado a Iniesta — tem aqui um dos primeiros jogos grandes de sua carreira numa Copa do Mundo. O Paraguai é um time difícil, com marcação intensa e bola parada como arma. Um resultado positivo da Turquia a colocaria em posição privilegiada no Grupo D.",
23: "A CNN elegeu este como um dos 10 melhores jogos da fase de grupos. Turquia vs. EUA em casa, no SoFi de Los Angeles, provavelmente com o primeiro lugar do grupo em jogo. A Turquia chegou à Copa com uma invencibilidade de oito jogos consecutivos, incluindo um empate heroico de 2 a 2 contra a Espanha fora de casa. Christian Pulisic lidera os americanos — mas a Turquia de Güler não vai facilitar.",
24: "Paraguai e Austrália encerram o Grupo D em San José com a classificação em disputa. Os paraguaios, com a tradição de jamais desistirem no futebol sul-americano, e os australianos, que sempre encontram uma forma de surpreender em Copas, disputam uma das vagas do mata-mata numa batalha que pode ir até os últimos minutos.",
# ─── GRUPO E ──────────────────────────────────────────────────────────────
25: "Curaçao — uma ilha caribenha de 150 mil habitantes — faz sua estreia histórica numa Copa do Mundo contra uma das maiores potências do futebol mundial. A Alemanha de Jamal Musiala e Florian Wirtz, dois dos jovens mais talentosos do futebol europeu, é tetracampeã e quer mostrar que está pronta para o quinto título. Um duelo simbólico do futebol mais inclusivo da história.",
26: "A Costa do Marfim, bicampeã africana (2015 e 2023), estreia em Filadelfia contra o Equador, que terminou à frente de Brasil, Uruguai e Colômbia nas eliminatórias sul-americanas. Um duelo entre dois times que chegam desvalorizados pelos especialistas — e que podem ser a surpresa do Grupo E.",
27: "Alemanha e Costa do Marfim em Toronto: um duelo que resume a tensão entre o futebol europeu organizado e o futebol africano físico e veloz. Julian Nagelsmann, jovem técnico alemão, pode estar ainda experimentando suas melhores combinações — o que dá aos marfinenses a esperança de uma zebra.",
28: "O Equador, acostumado a jogar a mais de 2.700 metros de altitude em Quito, tem um condicionamento físico único. Em Kansas City, enfrenta Curaçao — a nação estreante — numa partida que deve ser bem mais competitiva do que os placares esperados sugerem.",
29: "Curaçao, em seu segundo jogo numa Copa do Mundo, enfrenta a Costa do Marfim em Filadelfia. Os marfinenses vão querer pontos para confirmar a classificação; os caribenhos vão defender sua honra até o apito final. Um jogo que o futebol africano e caribenho vai acompanhar com orgulho.",
30: "A CNN elegeu este como um dos 10 melhores jogos. O Equador, segundo colocado nas eliminatórias sul-americanas à frente de favoritos históricos, enfrenta a Alemanha tetracampeã no MetLife Stadium. Os equatorianos, que jogam em altitude extrema em casa, têm preparo físico que pode desgastar até os mais preparados. Musiala e Wirtz precisarão de seu melhor futebol.",
# ─── GRUPO F ──────────────────────────────────────────────────────────────
31: "Para a CNN, um dos 10 melhores jogos da Copa. Os Países Baixos são eternamente proclamados como 'dark horse' — e com razão: semifinalistas na Euro 2024, quartas no Mundial de 2022, com talento coletivo em todas as linhas. O Japão, melhor seleção asiática, chega após seis vitórias consecutivas e um Grupo de 2022 em que eliminou Alemanha e Espanha — os Samurai Blue não têm medo de europeus.",
32: "A Suécia, organizada e disciplinada, abre o Grupo F contra a Tunísia no Estadio BBVA, em Monterrey, com a vista para as montanhas da Sierra Madre ao fundo. Os tunisianos, de volta às Copas, vão querer mostrar que a geração de 2022 não foi fluke. Um duelo entre duas nações com muito futebol para mostrar.",
33: "Países Baixos e Suécia em Houston: um duelo entre dois modelos de futebol coletivo europeu. A Oranje, potente no ataque, enfrenta uma Suécia que aposta em bloco baixo e velocidade nas transições. Um dos jogos com maior conteúdo tático do Grupo F.",
34: "Tunísia e Japão em Monterrey, às 10h da noite local: um jogo decisivo para a segunda vaga do Grupo F. Os Samurai Blue têm uma das melhores disciplinas táticas do futebol asiático; os tunisianos têm o ímpeto competitivo de quem joga sem pressão de favoritismo. Um resultado igual beneficiaria os Países Baixos.",
35: "Japão e Suécia decidem, potencialmente, a segunda vaga do Grupo F em Dallas. Os japoneses, que eliminaram a Alemanha e a Espanha do grupo em 2022, podem dar mais um susto europeu. A Suécia vai entrar em campo sabendo que perder pode significar a eliminação.",
36: "Países Baixos e Tunísia encerram o Grupo F em Kansas City. Se a Oranje já estiver classificada, Koeman pode dar minutos a jogadores menos utilizados — abrindo espaço para os tunisianos tentarem a virada histórica. Uma das últimas rodadas com mais possibilidades abertas.",
# ─── GRUPO G ──────────────────────────────────────────────────────────────
37: "Mohamed Salah — recordista de gols na Premier League e maior artilheiro da história do Egito — faz sua estreia em Seattle contra a Bélgica. Com quase 34 anos, esta pode ser a última Copa do craque que carregou o Egito sozinho por mais de uma década. A Bélgica, renovando sua geração pós-'geração dourada', quer impor seu domínio desde o início.",
38: "O Irã, de volta a sua quarta Copa consecutiva, estreia contra a Nova Zelândia em Los Angeles. Os All Whites da Oceania raramente chegam a Mundiais — e cada jogo é uma celebração em si. Um encontro improvável entre dois futebol mundos que raramente se cruzam.",
39: "Bélgica e Irã em Los Angeles: os Diabos Vermelhos podem pagar caro se subestimarem uma seleção asiática organizada, física e perigosa nas bolas paradas. O Irã nunca passou da fase de grupos numa Copa — mas esta pode ser a edição da mudança. Um jogo de armadilha potencial para os belgas.",
40: "Nova Zelândia e Egito em Vancouver: o emotivo Salah pode ser a diferença entre uma vitória egípcia rotineira e uma virada histórica dos All Whites. A Nova Zelândia vai jogar sem medo — e no futebol, times que jogam sem medo costumam complicar os favoritos.",
41: "Egito e Irã em Seattle num jogo que pode definir a segunda vaga do Grupo G. Salah do lado egípcio; uma defesa compacta e transições rápidas do lado iraniano. O vencedor se posiciona bem para o mata-mata; o perdedor pode estar eliminado.",
42: "Nova Zelândia e Bélgica encerram o Grupo G em Vancouver. Se os All Whites ainda tiverem chance de classificação, teremos uma das narrativas mais bonitas desta Copa — uma nação pequena que foi longe mais do que qualquer expectativa. A Bélgica vai ao campo sabendo que qualquer descuido pode custar caro.",
# ─── GRUPO H ──────────────────────────────────────────────────────────────
43: "Estreia da campeã europeia Espanha e, ao mesmo tempo, primeira Copa do Mundo da história de Cabo Verde. Lamine Yamal — considerado por muitos o melhor jogador do mundo quando em condição física plena — retorna de uma lesão muscular que encurtou sua temporada na La Liga. Se Yamal estiver 100%, a Espanha pode ser o time mais desequilibrante desta Copa.",
44: "A Arábia Saudita fez a maior zebra do Mundial de 2022 ao vencer a Argentina por 2 a 1 — e não tem medo de nomes grandes. Darwin Núñez, o centroavante explosivo do Uruguai pelo Liverpool, tenta impor o ritmo sul-americano desde o início no Hard Rock Stadium, em Miami. Dois estilos que prometem um jogo físico e intenso.",
45: "Em 2022, a Arábia Saudita fez o jogo da virada histórica contra a Argentina. A Espanha de Lamine Yamal não quer ser a próxima surpresa do catálogo saudita. De la Fuente vai querer que sua equipe seja dominante em todos os aspectos — para evitar qualquer zebra no Grupo H.",
46: "Uruguai e Cabo Verde em Miami: os La Celeste, com dois títulos mundiais no currículo, chegam como grandes favoritos. Mas Cabo Verde, na sua primeira Copa do Mundo, vai jogar com a leveza de quem não tem nada a perder — exatamente o tipo de adversário que pode surpreender.",
47: "Cabo Verde e Arábia Saudita em Houston: dois times que precisam de pontos para garantir a classificação. Os sauditas vêm de uma Copa de zebras; os cabo-verdianos estão vivendo sua primeira Copa. Um jogo com alto valor emocional para ambas as seleções.",
48: "A CNN elegeu este como um dos 10 melhores jogos da Copa. Em Guadalajara, a Espanha favorita ao título enfrenta o Uruguai bicampeão mundial no Estadio Akron. Lamine Yamal, o adolescente que pode decidir uma Copa sozinho, vai enfrentar Federico Valverde e uma defesa uruguaia que vive para frustrar os favoritos. Un Clasico americano no coração do México.",
# ─── GRUPO I ──────────────────────────────────────────────────────────────
49: "Para a CNN, um dos melhores jogos da Copa — 'uma batalha de nações francófonas que vai muito além do idioma'. A França é uma das favoritas ao título com Mbappé, Dembélé, Michael Olise e os jovens Désiré Doué e Rayan Cherki. O Senegal foi campeão africano antes de ser privado do título de forma controversa — e chega com um elenco de talento e raiva motivadora.",
50: "Erling Haaland faz aqui sua estreia numa Copa do Mundo. O atacante do Manchester City, com 1,94m e uma das maiores taxas de gol da história do futebol, marcou 16 dos 37 gols noruegueses na qualificação. O Iraque enfrenta talvez o jogador mais difícil de parar nesta Copa — num jogo que toda uma geração de fãs estava ansiosa para assistir.",
51: "A França, co-favorita ao título, encontra o Iraque em Filadelfia. Mbappé, Olise e companhia representam um dos ataques mais letais da Copa; os iraquianos, na sua segunda Copa da história, vão se defender com tudo e tentar o contra-ataque histórico. Um jogo que pode ter goleada — ou uma das maiores surpresas do torneio.",
52: "A CNN destacou este como um dos mais aguardados da fase de grupos. Erling Haaland, em busca do seu primeiro gol numa Copa, enfrenta os Leões da Teranga do Senegal no MetLife Stadium. O Senegal tem atletas físicos e defensores experientes capazes de dificultar a vida até do maior centroavante do mundo. Um jogo que pode decidir quem é o segundo colocado do Grupo I.",
53: "Haaland vs. Mbappé — o duelo que o mundo inteiro quer assistir. Michael Olise marcou um hat-trick contra a Irlanda do Norte antes da Copa, incluindo um gol de fora da área de tirar o fôlego, e Dembélé é mais uma arma francesa. Mas a Noruega de Haaland venceu a qualificação com 37 gols marcados — e em Boston este time vai ao ataque sem reservas.",
54: "Senegal e Iraque fecham o Grupo I em Toronto. Dependendo dos outros resultados, pode ser um jogo de definição ou já de adeus para os iraquianos. Os leões da Teranga vão querer entrar no mata-mata com confiança; o Iraque vai tentar escrever o capítulo mais inesperado de sua história recente.",
# ─── GRUPO J ──────────────────────────────────────────────────────────────
55: "Lionel Messi, possivelmente em sua última Copa do Mundo com 38 anos, abre o Grupo J contra a Argélia em Kansas City. O campeão de 2022 e melhor jogador do mundo nos últimos anos entra em campo rodeado de uma seleção argentina construída por Scaloni para ser campeã novamente. A Argélia, semifinalista do AFCON 2021, tem a motivação de parar o maior jogador de todos os tempos.",
56: "A Jordânia faz sua estreia histórica em Copas do Mundo, em San Francisco, contra a Áustria. Primeira nação árabe a estrear num Mundial pelo classificatório intercontinental de 2026, a Jordânia chegou aqui com muito esforço — e vai jogar com o coração do Oriente Médio inteiro torcendo por ela.",
57: "Argentina e Áustria em Dallas: os campeões mundiais buscam confirmar a liderança do grupo, enquanto a Áustria de David Alaba (se disponível) tenta repetir a surpresa da Copa de 1978 — quando também saiu cedo, apesar do talento. Messi deve fazer sua segunda aparição do torneio com o grupo já semi-decidido.",
58: "Jordânia e Argélia em San Francisco: um duelo entre duas nações árabes e norte-africanas que precisam de pontos para avançar. Ambas chegam ao segundo jogo precisando de vitória — o que promete um jogo aberto, físico e emocionalmente intenso.",
59: "Messi e a Argentina encerram o Grupo J contra a Jordânia em Dallas. Com 38 anos, este pode ser o último jogo de grupo de Messi numa Copa do Mundo — e o craque vai querer despedir-se com um gol. A Jordânia, na sua primeira Copa, vai guardar este duelo para contar aos netos.",
60: "Argélia e Áustria em Kansas City, na última rodada do Grupo J: com a Argentina já classificada, os dois brigam pela segunda vaga. Um duelo que pode precisar de gols para definir quem vai em frente — e isso favorece um jogo aberto e emocionante.",
# ─── GRUPO K ──────────────────────────────────────────────────────────────
61: "Cristiano Ronaldo, com 41 anos, possivelmente disputa sua última Copa do Mundo. Portugal estreia contra a RD Congo em Houston com um dos meios-campo mais talentosos do torneio: Vitinha, João Neves, Bruno Fernandes e Bernardo Silva, nas palavras da CNN, podem ser a melhor linha de criação desta Copa. Ronaldo, se utilizado, ainda é capaz de decidir.",
62: "O Uzbequistão faz sua estreia histórica em Copas do Mundo no palco mais icônico do futebol mundial — o Estádio Azteca. Enfrenta a Colômbia, vice-campeã da Copa América 2024, com Luis Díaz do Bayern de Munique como grande estrela. Um momento histórico para o futebol da Ásia Central.",
63: "Portugal e Uzbequistão em Houston: os lusitanos, quartos favoritos ao título, buscam confirmar a classificação com antecedência. Ronaldo pode receber mais minutos aqui; o Uzbequistão vai defender com tudo para deixar a Copa com a cabeça erguida.",
64: "Colômbia e RD Congo em Guadalajara: Luis Díaz, um dos melhores atacantes em atividade, lidera os colombianos num jogo que pode confirmar a classificação. A RD Congo tem jogadores formados nos principais clubes europeus — não é o time fácil que parece.",
65: "A CNN elegeu este como o melhor jogo do Grupo K. Em Miami, Colômbia e Portugal disputam a liderança num confronto de altíssimo nível: Portugal tem um dos melhores meios-campos do torneio; a Colômbia tem Luis Díaz, a atmosfera de um país apaixonado pelo futebol e a motivação de quem chegou às finais da Copa América em 2024. Ronaldo pode ser o fator X se Martínez decidir usá-lo.",
66: "RD Congo e Uzbequistão fecham o Grupo K em Atlanta. Dois times que fizeram história ao chegar aqui — um pela primeira vez como nação independente com este nome, o outro pela primeira vez na sua história. Um jogo que terá mais emoção do que os resultados sugerem.",
# ─── GRUPO L ──────────────────────────────────────────────────────────────
67: "A CNN destacou este como um dos 10 melhores da Copa — e a história justifica: Inglaterra e Croácia reproduzem a semifinal de 2018 na Rússia, quando Modrić e companhia venceram os ingleses na prorrogação. Tuchel assumiu os Três Leões com Kane, Bellingham, Saka e Declan Rice num dos melhores elencos ingleses de todos os tempos. Modrić, com 40 anos, entra em campo numa Copa pela última vez.",
68: "Gana e Panamá em Toronto: dois times com tradições diferentes mas com o mesmo espírito combativo. O Panamá, classificado novamente via CONCACAF, quer repetir a energia de sua primeira Copa (2018). Gana, com uma nova geração de jogadores europeus, quer sair desta Copa com orgulho.",
69: "A Inglaterra de Bellingham e Saka enfrenta Gana no Gillette Stadium, em Boston. Os Três Leões chegam como terceiro favorito ao título; os Black Stars têm uma nova geração técnica que vai testar a defesa inglesa. Uma vitória inglesa praticamente garante a classificação.",
70: "Panamá e Croácia em Toronto: os croatas, em despedida da geração Modrić, buscam os pontos necessários para avançar. O Panamá vai lutar muito para complicar o time europeu — em 2022, a Croácia teve dificuldades com o Marrocos num jogo parecido com este.",
71: "Panamá e Inglaterra no MetLife Stadium, em Nova York — os ingleses com o grupo praticamente definido, o Panamá com tudo a provar. Um jogo em que Tuchel pode dar oportunidade a jogadores menos utilizados; o Panamá vai aproveitar cada espaço aberto.",
72: "Croácia e Gana encerram o Grupo L em Filadelfia. Modrić pode fazer aqui sua última aparição num jogo de grupo de Copa do Mundo — com 40 anos e uma carreira que redefiniu o papel do meia no futebol moderno. Gana vai tentar a surpresa que deixaria os croatas fora do mata-mata.",
# ─── MATA-MATA: 16-AVOS ──────────────────────────────────────────────────
73: "O primeiro jogo dos 16-avos de final é uma novidade absoluta da Copa de 48 seleções — esta fase nunca existiu antes num Mundial masculino. No SoFi Stadium de Los Angeles, segundo e segundo colocados dos Grupos A e B se enfrentam num mata-mata em que qualquer erro é fatal e não há segundo turno.",
74: "No Gillette Stadium, em Boston, o líder do Grupo E enfrenta um dos melhores terceiros colocados num duelo que defini quem avança para as oitavas. A nova fase dos 16-avos exige atenção máxima desde o primeiro minuto.",
75: "O Estadio BBVA, em Monterrey, recebe seu primeiro jogo do mata-mata da Copa. O dono do grupo F cruza com o segundo do grupo C — dois times que sobreviveram à fase mais imprevisível e se encontram agora no momento da verdade.",
76: "O NRG Stadium de Houston, onde a temperatura e a umidade são fatores desde o aquecimento, recebe um dos 16-avos mais aguardados. O líder do Grupo C enfrenta o segundo do Grupo F num jogo em que o histórico de grupos diz muito — mas o mata-mata tem lógica própria.",
77: "O MetLife Stadium, palco da grande final, recebe seu primeiro jogo eliminatório da Copa. O líder do Grupo I — potencialmente um time de ponta — mede forças com um dos melhores terceiros colocados de grupos repletos de qualidade.",
78: "AT&T Stadium, em Dallas: o segundo do Grupo E enfrenta o segundo do Grupo I num duelo que pode reunir dois dos times mais técnicos do torneio. O mata-mata começa aqui a definir a história desta Copa.",
79: "O Estádio Azteca, o mais mítico desta Copa, recebe um jogo do mata-mata. O líder do Grupo A — potencialmente o México diante de sua própria torcida — tem aqui uma das maiores oportunidades da história do futebol mexicano para ir além das oitavas, onde parou em todos os seus Mundiais recentes.",
80: "O Mercedes-Benz Stadium de Atlanta recebe um dos 16-avos com maior potencial de público emocionado. O líder do Grupo L — potencialmente a Inglaterra ou a Croácia — enfrenta um dos melhores terceiros no que pode ser um jogo de altíssima intensidade.",
81: "O Levi's Stadium, no Vale do Silício, recebe um mata-mata entre o líder do Grupo D e um dos melhores terceiros colocados. A seleção anfitriã dos EUA pode estar aqui — e uma jogada de Pulisic poderia levantar 68 mil torcedores americanos.",
82: "O Lumen Field de Seattle, um dos estádios mais barulhentos desta Copa, recebe o duelo entre o líder do Grupo G e um dos melhores terceiros. Com a cobertura fechada criando uma acústica única, qualquer gol aqui vai fazer a arena tremer.",
83: "O BMO Field de Toronto, a menor sede desta Copa, recebe um dos 16-avos com mais calor humano. O segundo do Grupo K enfrenta o segundo do Grupo L num confronto que pode reunir Portugal ou Colômbia contra Inglaterra ou Croácia.",
84: "O SoFi de Los Angeles recebe um segundo jogo do mata-mata — desta vez o líder do Grupo H (potencialmente a Espanha de Lamine Yamal) contra o segundo do Grupo J (potencialmente a Argentina de Messi). Se os favoritos avançarem, este pode ser o jogo mais badalado dos 16-avos.",
85: "O BC Place de Vancouver, com seu teto retrátil e clima ameno, recebe um dos jogos de 16-avos mais estratégicos. O líder do Grupo B encontra um dos melhores terceiros colocados num duelo que pode revelar um dos grandes candidatos ao título.",
86: "O Hard Rock Stadium de Miami recebe um dos confrontos mais aguardados dos 16-avos: o líder do Grupo J (potencialmente a Argentina de Messi) contra o segundo do Grupo H (potencialmente o Uruguai). Um clássico sul-americano em solo americano.",
87: "O Arrowhead Stadium de Kansas City, um dos mais barulhentos dos Estados Unidos, recebe um dos 16-avos com maior potencial de emotividade. O líder do Grupo K (potencialmente Portugal com Ronaldo) enfrenta um dos melhores terceiros colocados.",
88: "AT&T Stadium, em Dallas, recebe o último jogo dos 16-avos antes das oitavas. O segundo do Grupo D enfrenta o segundo do Grupo G num jogo que encerra a primeira fase do mata-mata e abre o caminho para as quartas.",
# ─── OITAVAS ──────────────────────────────────────────────────────────────
89: "As oitavas de final chegam ao Lincoln Financial Field de Filadelfia. Os vencedores dos 16-avos 74 e 77 se encontram numa batalha em que os favoritos ao título começam a eliminar uns aos outros. Filadelfia, a cidade da independência americana, pode assistir à queda de uma grande seleção.",
90: "O NRG Stadium de Houston recebe as oitavas de final. Os vencedores dos jogos 73 e 75 se encontram num estádio onde o calor e a umidade podem ser um fator extra. As oitavas são o momento em que a Copa começa a separar os times bons dos times excepcionais.",
91: "O MetLife Stadium recebe as oitavas de final — a terceira vez que este palco da grande final abriga um jogo decisivo. Os vencedores dos jogos 76 e 78 chegam aqui tendo sobrevivido a duas semanas de pressão extrema.",
92: "O Estádio Azteca recebe as oitavas de final. Com capacidade para mais de 80 mil pessoas e uma atmosfera inigualável, qualquer time que jogar aqui sente o peso da história — especialmente se o México ainda estiver no torneio.",
93: "AT&T Stadium, em Dallas, recebe as oitavas de final. Os vencedores dos jogos 83 e 84 se encontram numa batalha que pode reunir as maiores estrelas do mundo. Uma das cidades mais entusiastas desta Copa.",
94: "O Lumen Field de Seattle recebe as oitavas de final. Com seu teto retrátil e a atmosfera envolvente criada pela cobertura, este estádio pode ser o palco de um dos duelos mais intensos do mata-mata.",
95: "O Mercedes-Benz Stadium de Atlanta recebe as oitavas de final. Os vencedores dos jogos 86 e 88 chegam a este ponto com pelo menos duas vitórias no mata-mata — os únicos que sobreviveram à fase mais imprevisível da Copa.",
96: "O BC Place de Vancouver recebe as oitavas. Numa Copa que chegou ao continente americano inteiro, a cidade canadense de Vancouver pode ser palco do jogo que defina quem vai às quartas — com a temperatura amena e um público apaixonado.",
# ─── QUARTAS ──────────────────────────────────────────────────────────────
97: "Quartas de final no Gillette Stadium de Boston — restam apenas oito seleções no torneio. Os vencedores das oitavas 89 e 90 chegam aqui como dois dos melhores times do mundo, e um deles vai para casa. Boston, cidade de tradição esportiva intensa, vai criar uma atmosfera de final para este jogo.",
98: "Quartas de final no SoFi de Los Angeles — o estádio de 70 mil lugares que abrigou a abertura recebe agora um dos quatro jogos que definem as semifinalistas. Com dois times de elite em campo, este pode ser o jogo mais memorável desta fase.",
99: "Quartas de final no Hard Rock Stadium de Miami. Os vencedores das oitavas 91 e 92 se encontram num confronto que pode reunir duas potências de continentes diferentes. Miami, a cidade mais latina dos EUA, vai escolher seu lado e criar uma das atmosferas mais quentes da Copa.",
100: "Quartas de final no Arrowhead Stadium de Kansas City. No estádio que já recebeu Messi em partidas do Inter Miami, dois dos oito melhores times do mundo definem uma vaga nas semifinais. O vencedor está a dois jogos de levantar a Copa.",
# ─── SEMIS ────────────────────────────────────────────────────────────────
101: "Semifinal no AT&T Stadium de Dallas. Dois dos quatro melhores times do torneio definem a primeira vaga na final do MetLife Stadium. Histórico de Copas, pressão máxima e o peso de estar a 90 minutos de disputar o maior prêmio do futebol mundial.",
102: "Semifinal no Mercedes-Benz Stadium de Atlanta. A segunda vaga para a final da Copa do Mundo 2026 é definida aqui. Um dos maiores estádios desta Copa, em pleno verão americano, recebe um jogo que ficará na memória do futebol por décadas.",
# ─── 3O LUGAR / FINAL ────────────────────────────────────────────────────
103: "Disputa pelo terceiro lugar no Hard Rock Stadium de Miami — uma tradição controversa mas sempre emocionante. Os dois perdedores das semifinais têm uma última chance de deixar a Copa com a cabeça erguida e uma medalha de bronze. Muitos ídolos de grandes nações se despediram de Copas neste tipo de jogo.",
104: "A grande final da Copa do Mundo FIFA 2026 no MetLife Stadium, em East Rutherford, Nova Jersey — o mesmo estádio que abrigou o Brasil de Ancelotti em seu primeiro jogo do torneio. Mais de 82 mil pessoas vão assistir ao jogo mais assistido do planeta. Um capítulo definitivo da Copa mais inclusiva da história.",
}

STAGE_FALLBACK = {
    "r32": "Confronto dos 16-avos de final (etapa inedita no formato de 48 selecoes).",
    "r16": "Confronto das oitavas de final.",
    "qf": "Confronto das quartas de final.",
}

def fact_for(mid, stage, group, home, away, venue):
    if mid in FACTS:
        return FACTS[mid]
    if stage == "group":
        hn = TEAMS[home][0]; an = TEAMS[away][0]; city = VENUES[venue]["city"]
        return f"{hn} x {an} pela fase de grupos do Grupo {group}, em {city}."
    return STAGE_FALLBACK.get(stage, "")

# Tecnicos/esquemas bem estabelecidos (conservador: so onde ha confianca).
COACH = {
    "BRA": ("Carlo Ancelotti", "4-2-3-1"),
}

def build():
    teams = {}
    for code, (name, flag) in TEAMS.items():
        entry = {"name": name, "flag": flag, "coach": "", "formation": "", "squad": []}
        if code in COACH:
            entry["coach"], entry["formation"] = COACH[code]
        teams[code] = entry

    matches = []
    for (mid, stage, group, home, away, dt, venue) in M:
        rec = {"id": mid, "stage": stage, "datetime_utc": dt, "venue": venue,
               "home": home, "away": away,
               "fact": fact_for(mid, stage, group, home, away, venue)}
        if group:
            rec["group"] = group
        matches.append(rec)

    data = {
        "calendar": {
            "name": "Copa do Mundo FIFA 2026",
            "description": "Todos os 104 jogos da Copa do Mundo FIFA 2026 (EUA, Canada e Mexico).",
            "refresh_hours": 6,
            "default_match_minutes": 120,
            "reminder_minutes_before": 15,
        },
        "venues": VENUES,
        "groups": GROUPS,
        "teams": teams,
        "matches": matches,
        "results": {},
        "thirds": {},
    }
    out = os.path.join(HERE, "data", "data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"data.json: {len(matches)} jogos, {len(teams)} selecoes, {len(VENUES)} estadios.")

if __name__ == "__main__":
    build()

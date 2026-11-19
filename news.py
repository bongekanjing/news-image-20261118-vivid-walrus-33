"""The day's news: Wednesday 18 November 2026.

Only stories that happened, or were first reported, on 18 November 2026 are
carried here. Items that broke the previous day are excluded by name in the
footer so the page states its own boundary. Every figure is as reported.
"""

DAY = "WEDNESDAY"
DATE = "18 November 2026"

# ---- the day in numbers: six figures, none of them a headline repeated --
STATS = [
    ("18/20", "IRANIAN MISSILES DOWNED\nOVER JORDAN"),
    ("2,230", "CIVILIANS KILLED IN\nSUDAN SINCE JANUARY"),
    ("56", "SENATE SEATS HELD BY\nDEMOCRATS AFTER ALASKA"),
    ("75", "KILLED IN ADF ATTACKS\nIN EASTERN DR CONGO"),
    ("62%", "CAMBODIA'S FUEL\nIMPORTS CLIMB"),
    ("19,000", "YOUTUBE CHANNELS\nPULLED IN INDONESIA"),
]

# ---- three leads -------------------------------------------------------
LEADS = [
    dict(region="ASIA", place="SHENZHEN", art="summit", tag="APEC",
         kicker="ASIA \u00b7 SHENZHEN \u00b7 APEC",
         headline="Xi and Putin share a stage,\na day before Trump joins them",
         dek=("Xi told APEC's chief executives that trade must stay open. Putin "
              "followed him and called sanctions illegitimate. Their fifth meeting "
              "this year, and a three-way with Trump on Thursday.")),
    dict(region="MIDDLE EAST", place="JORDAN", art="gulf", tag="GULF",
         kicker="MIDDLE EAST \u00b7 JORDAN",
         headline="Iran fires at a US base in Jordan as the Gulf war widens",
         dek=("Jordan's air defences downed 18 of 20 missiles aimed at Al-Azraq. "
              "US forces sank five Iranian tankers; Tehran said it hit ten ships "
              "and closed waters near Hormuz. Oil briefly passed $100.")),
    dict(region="EUROPE", place="ODESA", art="strike", tag="UKRAINE",
         kicker="EUROPE \u00b7 ODESA",
         headline="Russian strikes kill five, and Kyiv's bridges are hit",
         dek=("Three strikes fell on Odesa's historic centre, one inside a "
              "UNESCO-protected area. Hours after the Crimea bridge road span "
              "collapsed, missiles damaged Kyiv's Dnipro crossings.")),
]

# ---- ten cards, two bands of five -------------------------------------
CARDS = [
    dict(region="AMERICAS", place="NEW YORK", art="ipo", tag="$83",
         kicker="AMERICAS \u00b7 MARKETS",
         headline="Anthropic prices its IPO at $83 a share",
         dek="$1.5trn valuation, above its $70\u2013$78 range. Trades as ANT on Thursday."),
    dict(region="EUROPE", place="LONDON", art="chart", tag="3.6%",
         kicker="EUROPE \u00b7 ECONOMY",
         headline="UK inflation hits 3.6%, a one-year high",
         dek="Motor fuel up 33.2% on the Iran war. The Bank of England expects 5%."),
    dict(region="WORLD", place="DEEP SPACE", art="space", tag="1 DAY",
         kicker="WORLD \u00b7 SCIENCE",
         headline="Voyager 1 is now one light-day from home",
         dek="26 billion km, 49 years after launch. The farthest anything has gone."),
    dict(region="AMERICAS", place="BRASILIA", art="ledger", tag="69\u20132",
         kicker="AMERICAS \u00b7 BRAZIL",
         headline="Brazil's Senate passes Lula's fiscal package, 69\u20132",
         dek="$10bn of spending curbs after his re-election. It goes to the lower house."),
    dict(region="ASIA", place="ODISHA", art="cyclone", tag="690KM",
         kicker="ASIA \u00b7 BAY OF BENGAL",
         headline="Cyclone Akvan turns severe off India's east coast",
         dek="Orange alert for Andhra Pradesh and south Odisha. Landfall due Friday."),
    dict(region="AFRICA", place="DAKAR", art="gavel", tag=None,
         kicker="AFRICA \u00b7 SENEGAL",
         headline="Senegal's ruling party expels the president",
         dek="Pastef removed Bassirou Diomaye Faye and 31 others from its ranks."),
    dict(region="AFRICA", place="BADME", art="border", tag=None,
         kicker="AFRICA \u00b7 HORN",
         headline="Fighting returns to the Ethiopia\u2013Eritrea border",
         dek="Artillery near Badme. Ethiopia's push for Red Sea access raises the stakes."),
    dict(region="ASIA", place="MANILA", art="flags", tag="$5B",
         kicker="ASIA \u00b7 MANILA",
         headline="Trump pledges deeper defence ties with the Philippines",
         dek="He met Marcos before flying on to Shenzhen, after $5bn of arms sales."),
    dict(region="ASIA", place="JAKARTA", art="network", tag="+25BP",
         kicker="ASIA \u00b7 INDONESIA",
         headline="Indonesia raises rates to defend the rupiah",
         dek="A 25 basis point rise resumes tightening. Google pulled 19,000 channels."),
    dict(region="OCEANIA", place="NIUE", art="ocean", tag="\u00a31M",
         kicker="OCEANIA \u00b7 NIUE",
         headline="Niue's ocean trust wins the 2026 Earthshot Prize",
         dek="\u00a31m for a sanctuary that sells ocean sponsorship by the square km."),
]

# ---- one-line index: each item fits one line in its column ------------
SHORT_BRIEFS = [
    ("US", "Peltola takes Alaska; Democrats hold 56 seats"),
    ("US", "Jeffries is nominated for House speaker"),
    ("CANADA", "Anand to rebuild China trade step by step"),
    ("BRAZIL", "Court freezes $400m in betting inquiry"),
    ("FRANCE", "Paris confirms troops train Ukrainians"),
    ("RUSSIA", "Canada condemns jets near Japan and Taiwan"),
    ("EGYPT", "Court suspends a Mada Masr editor's trial"),
    ("SUDAN", "Drones caused 1,630 verified civilian deaths"),
    ("DR CONGO", "ADF attacks in the east kill 75"),
    ("NIGERIA", "Tinubu lets states run their own police"),
    ("GHANA", "A $60m presidential jet angers the public"),
    ("SOUTH AFRICA", "Five charged under the mercenary law"),
    ("SOUTH KOREA", "Seoul and Beijing seal services deal"),
    ("MYANMAR", "Army-backed leader rethinks ASEAN ties"),
    ("VIETNAM", "Forestry director shot at his office"),
    ("MALAYSIA", "Anwar presses Thailand and Cambodia on peace"),
    ("CAMBODIA", "Fuel imports climb 62% in ten months"),
    ("AUSTRALIA", "Albanese in a leaders' photo with Putin"),
    ("NEW ZEALAND", "Northland power cut hits thousands"),
    ("WORLD", "Geneva talks resume on autonomous weapons"),
    ("SOMALIA", "Alone, it votes against a UN women's draft"),
    ("UGANDA", "Museveni's son wants to succeed him"),
    ("KENYA", "Ruto says exam papers are now printed at home"),
    ("NIGERIA", "Military pact with Cameroon, Niger and Chad"),
]

# ---- what the page deliberately leaves out ----------------------------
NOT_TODAY = (
    "Left out because they broke on Tuesday 17 November: the Crimea bridge "
    "road span, Nvidia's $115.8bn quarter, the Knesset's new speaker, Trump's "
    "Manila Quad meeting and Britain's settler sanctions. Awaited on Thursday "
    "19 November: the Xi\u2013Trump\u2013Putin trilateral and GTA VI."
)

SOURCES = (
    "REUTERS \u00b7 AP \u00b7 AFP \u00b7 BLOOMBERG \u00b7 CNBC \u00b7 BBC \u00b7 THE GUARDIAN \u00b7 "
    "AL JAZEERA \u00b7 EURONEWS \u00b7 UN NEWS \u00b7 NASA \u00b7 IMD \u00b7 ALLAFRICA \u00b7 "
    "AFRICA FRONT PAGE \u00b7 THE STAR \u00b7 ONS \u00b7 SENADO \u00b7 PAHO"
)

# ---- rough coordinates, for the locator map --------------------------
LOC = {
    "SHENZHEN": (22.5, 114.1), "JORDAN": (31.9, 35.9), "ODESA": (46.5, 30.7),
    "KYIV": (50.5, 30.5), "NEW YORK": (40.7, -74.0), "LONDON": (51.5, -0.1),
    "BRASILIA": (-15.8, -47.9), "ODISHA": (20.3, 85.8), "DAKAR": (14.7, -17.5),
    "BADME": (14.4, 37.9), "MANILA": (14.6, 121.0), "JAKARTA": (-6.2, 106.8),
    "NIUE": (-19.1, -169.9),
    "US": (38.9, -77.0), "CANADA": (45.4, -75.7), "BRAZIL": (-15.8, -47.9),
    "HAITI": (18.5, -72.3), "FRANCE": (48.9, 2.4), "GERMANY": (52.5, 13.4),
    "RUSSIA": (55.8, 37.6), "SOUTH KOREA": (37.6, 127.0), "MYANMAR": (19.8, 96.2),
    "THAILAND": (13.8, 100.5), "CAMBODIA": (11.6, 104.9), "VIETNAM": (21.0, 105.8),
    "SINGAPORE": (1.4, 103.8), "INDONESIA": (-6.2, 106.8), "INDIA": (28.6, 77.2),
    "NEPAL": (27.7, 85.3), "EGYPT": (30.0, 31.2), "SUDAN": (15.6, 32.5),
    "NIGERIA": (9.1, 7.4), "GHANA": (5.6, -0.2), "GUINEA": (10.9, -12.3),
    "KENYA": (-1.3, 36.8), "ANGOLA": (-8.8, 13.2), "SOUTH AFRICA": (-25.9, 28.2),
    "ZIMBABWE": (-17.8, 31.1), "MOZAMBIQUE": (-25.9, 32.6), "DR CONGO": (-4.3, 15.3),
    "UGANDA": (0.3, 32.6), "MADAGASCAR": (-18.9, 47.5), "AUSTRALIA": (-33.9, 151.2),
    "NEW ZEALAND": (-41.3, 174.8), "POLAND": (52.2, 21.0), "ITALY": (41.9, 12.5),
    "SPAIN": (40.4, -3.7), "JAPAN": (35.7, 139.7), "MALAYSIA": (3.1, 101.7),
    "SRI LANKA": (6.9, 79.9), "TUNISIA": (36.8, 10.2), "SOMALIA": (2.0, 45.3),
    "LIBERIA": (6.3, -10.8),
}

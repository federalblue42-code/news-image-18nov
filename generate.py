#!/usr/bin/env python3
"""Build the 18 November 2026 world-news front page (news-image-20261118).

Deterministic: pure string building, no network, no clock. Writes news_front.svg;
render with: rsvg-convert -w 1024 -h 1024 news_front.svg -o entry.png
Every story happened, or was first reported, on Wednesday 18 November 2026.
"""

W, H = 1024, 1024
M = 22
CW = W - 2 * M

PAPER = "#f7f2e6"
INK = "#191714"
RED = "#b3382c"
NAVY = "#1b2a4a"
GOLD = "#c9a227"
TEAL = "#2e6e63"
GREY = "#6b6459"
LINE = "#c9c0ae"
CREAM2 = "#efe7d4"

SERIF = "Playfair Display, DejaVu Serif, serif"
SANS = "DejaVu Sans, sans-serif"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def txt(x, y, s, size=10, fill=INK, font=SANS, weight="normal", anchor="start",
        style="normal", spacing=None, opacity=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    st = f' font-style="{style}"' if style != "normal" else ""
    sp = f' letter-spacing="{spacing}"' if spacing else ""
    op = f' opacity="{opacity}"' if opacity else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'fill="{fill}" font-weight="{weight}"{a}{st}{sp}{op}>{esc(s)}</text>')

def rect(x, y, w, h, fill, stroke=None, sw=1, rx=0, opacity=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    r = f' rx="{rx}"' if rx else ""
    o = f' opacity="{opacity}"' if opacity else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"{s}{r}{o}/>'

def line(x1, y1, x2, y2, stroke=LINE, sw=1):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"/>'

def wrap(s, n):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= n:
            cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def star(cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.4
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'

# ---------------------------------------------------------------- content
STORIES = [
    (1, "SHENZHEN", "SUMMIT", "Xinhua · NYT", "Xi greets Trump with a rare airport welcome",
     "A hug on the tarmac opens APEC; the first Trump-Xi-Putin trilateral is expected Thursday. Putin gets a handshake at the banquet.", "ASIA", "summit"),
    (2, "BRUSSELS", "UKRAINE", "EC · Euronews", "EU proposes a €45bn loan to keep Ukraine fighting",
     "€25bn for weapons, €20bn for the budget; Kyiv repays only from Russian reparations. Leaders debate it Nov 25-26.", "EUROPE", "eu"),
    (3, "THE GULF", "WAR", "Reuters · GN", "Iranian drones hit the Gulf; Saudi cities go on alert",
     "Kuwait and Bahrain intercept; Jazan, Najran and Khamis Mushait alert, then all-clear. An ADNOC vessel is struck in Hormuz.", "MIDEAST", "gulf"),
    (4, "WASHINGTON", "POLITICS", "Roll Call · AP", "Jeffries nominated to be first Black speaker",
     "251-11 secret ballot; floor vote in January.", "AMERICAS", "speaker"),
    (5, "NEW YORK", "ART", "NYT · Reuters", "Van Gogh record: $190.4m at Sotheby's",
     "Record after an 11th-hour Nazi-era settlement.", "AMERICAS", "vangogh"),
    (6, "DEEP SPACE", "SCIENCE", "NASA", "Voyager 1 crosses one light-day — then falls silent",
     "16.1bn miles out; no science data since Nov 14.", "WORLD", "voyager"),
    (7, "ODISHA", "STORM", "IMD · HT", "Akvan nears: 47,000 evacuated, red alert",
     "Landfall Friday noon; schools shut Thu-Sat.", "ASIA", "cyclone"),
    (8, "SEOUL", "EDUCATION", "Korea Herald", "Suneung eve: a nation tightens exam security",
     "Anti-AI-cheating rules changed a day before.", "ASIA", "suneung"),
    (9, "ANTALYA", "CLIMATE", "CAN · Commons", "COP31 deadlocked with 21 items open",
     "EU rejects finance draft; G77 calls for pause.", "EUROPE", "cop"),
    (10, "GAZA", "WAR", "Reuters · AP", "Israeli tanks cross the Yellow Line",
     "First raid since ceasefire; both sides accused.", "MIDEAST", "tank"),
    (11, "FLORIDA", "WEATHER", "NWS · AP", "15 inches overnight: Broward declares emergency",
     "Schools shut Thursday; temple roof collapses.", "AMERICAS", "flood"),
    (12, "BADME", "HORN", "Reuters · AC", "Ethiopia and Eritrea amass forces on the border",
     "Skirmishes near Badme; fears of a wider war.", "AFRICA", "border"),
]

BRIEFS = [
    (13, "WASHINGTON", "Pew: Muslims to outnumber Christians by 2035", "WORLD"),
    (14, "NEW YORK", "Anthropic prices record IPO at $83; ANT debuts Thu", "AMERICAS"),
    (15, "WASHINGTON", "GTA VI presales top $1.5bn before launch", "AMERICAS"),
    (16, "SHENZHEN", "Trump greets Putin with a handshake at the banquet", "ASIA"),
    (17, "WASHINGTON", "US-China trade truce extended to January 10", "AMERICAS"),
    (18, "RIYADH", "Coalition downs two missiles bound for Riyadh", "MIDEAST"),
    (19, "JAZAN", "Houthis claim missile and drone ops on Saudi sites", "MIDEAST"),
    (20, "KUWAIT CITY", "Gulf states intercept Iranian drones overnight", "MIDEAST"),
    (21, "HORMUZ", "ADNOC vessel hit as shipping risks rise", "MIDEAST"),
    (22, "PARIS", "Darmanin: Mélenchon could win a 2027 runoff", "EUROPE"),
    (23, "BOGOTÁ", "Unions keep Thursday strike call; US embassy warns", "AMERICAS"),
    (24, "KERCH", "Bridge traffic snarled; engineers assess damage", "EUROPE"),
    (25, "KYIV", "Flamingo missiles said to have severed the span", "EUROPE"),
    (26, "HOLLYWOOD", "Temple Sinai's roof collapses under the rain", "AMERICAS"),
    (27, "FLORIDA", "Memorial Hospital limits visits amid flooding", "AMERICAS"),
    (28, "ODISHA", "448 shelters open; 3,000 more being readied", "ASIA"),
    (29, "SEOUL", "1,312 test centers; exam runs 8:40 to 17:45", "ASIA"),
    (30, "ANTALYA", "Ministers take the text in evening informal talks", "EUROPE"),
    (31, "BRUSSELS", "Leaders to debate the loan at Nov 25-26 council", "EUROPE"),
    (32, "CANBERRA", "DSN locked on Voyager; no data since Nov 14", "OCEANIA"),
    (33, "SUDAN", "UN: 2,230 civilians killed since January", "AFRICA"),
    (34, "DAKAR", "Senegal's ruling party expels President Faye", "AFRICA"),
    (35, "LAGOS", "Nigeria busts Sahara cocaine route; eight arrested", "AFRICA"),
    (36, "ABUJA", "All 36 states approve state police amendment", "AFRICA"),
]

REGIONS = [("ASIA", "ASIA-PACIFIC", "#2e5f8a"), ("EUROPE", "EUROPE", "#3a7d44"),
           ("AMERICAS", "THE AMERICAS", "#c9a227"), ("MIDEAST", "MIDEAST", "#b3382c"),
           ("AFRICA", "AFRICA", "#8a5a3b"), ("OCEANIA", "OCEANIA", "#2e6e63"),
           ("WORLD", "WORLD", "#55504a")]

STATS = [("€45bn", "EU loan proposed for Ukraine in 2027", "#3a7d44"),
         ("$190.4m", "Van Gogh's auction record at Sotheby's", "#c9a227"),
         ("251-11", "Jeffries' secret-ballot speaker nomination", "#2e5f8a"),
         ("16.1bn mi", "Voyager 1's one light-day from Earth", "#b3382c"),
         ("47,000", "evacuated in Odisha as Akvan nears", "#2e6e63"),
         ("551,864", "registered for Korea's Suneung Thursday", "#8a5a3b")]

TIMELINE = [("06:00", "Xi greets Trump in Shenzhen"),
            ("10:16", "Voyager 1 crosses one light-day"),
            ("15:00", "Pew: Islam largest by 2035"),
            ("EVENING", "APEC banquet; Trump-Putin handshake"),
            ("NIGHT", "Van Gogh record in New York")]

DATECHECK = [
    "ICJ reads the Rohingya judgment - Thu 19 Nov, 09:00 GMT",
    "GTA VI's global release day - Thu 19 Nov",
    "Anthropic's first ANT trades on Nasdaq - Thu 19 Nov",
    "The Trump-Xi-Putin trilateral itself - Thu 19 Nov",
    "COP31 Adaptation Fund's $50.2m pledges - Thu 19 Nov",
    "NASA's Voyager light-day celebration - Thu 19 Nov",
    "'Shine Bright for Voyager' light wave - Tue 17 Nov",
    "US strike on Iran's Qeshm Island - Tue 17 Nov",
]

# ---------------------------------------------------------------- illustrations
def art_summit(w, h):
    s = rect(0, 0, w, h, "#dce8f2")
    s += rect(0, h * 0.62, w, h * 0.38, "#b9c9d8")
    fw, fh = w * 0.17, h * 0.30
    for fx in (0.14, 0.42, 0.70):
        x = w * fx
        s += line(x, h * 0.14, x, h * 0.66, "#4a4a4a", 1.5)
    x = w * 0.14
    s += rect(x, h * 0.14, fw, fh, "#fff")
    for i in range(4):
        s += rect(x, h * 0.14 + i * fh / 3.5, fw, fh / 7, "#b3382c")
    s += rect(x, h * 0.14, fw * 0.45, fh * 0.5, "#2e3f6e")
    x = w * 0.42
    s += rect(x, h * 0.14, fw, fh, "#de2910")
    s += star(x + fw * 0.28, h * 0.14 + fh * 0.32, fh * 0.20, "#ffde00")
    x = w * 0.70
    s += rect(x, h * 0.14, fw, fh / 3, "#fff")
    s += rect(x, h * 0.14 + fh / 3, fw, fh / 3, "#2e5f8a")
    s += rect(x, h * 0.14 + 2 * fh / 3, fw, fh / 3, "#b3382c")
    s += f'<ellipse cx="{w*0.5}" cy="{h*0.82}" rx="{w*0.30}" ry="{h*0.10}" fill="#8a5a3b"/>'
    for cx in (0.32, 0.5, 0.68):
        s += f'<circle cx="{w*cx}" cy="{h*0.70}" r="{h*0.055}" fill="#1b2a4a"/>'
    return s

def art_eu(w, h):
    s = rect(0, 0, w, h, "#1b2a4a")
    cx, cy = w * 0.32, h * 0.46
    s += f'<circle cx="{cx}" cy="{cy}" r="{h*0.32}" fill="#2e3f6e"/>'
    import math
    for i in range(12):
        a = i * math.pi / 6
        s += star(cx + h * 0.24 * math.cos(a), cy + h * 0.24 * math.sin(a), h * 0.045, "#c9a227")
    s += rect(w * 0.62, h * 0.30, w * 0.30, h * 0.34, "#3a7d44", rx=2)
    s += txt(w * 0.77, h * 0.52, "€45bn", h * 0.13, "#fff", SANS, "bold", "middle")
    s += txt(w * 0.5, h * 0.94, "FOR UKRAINE · 2027", h * 0.095, "#c9bfa8", SANS, "bold", "middle")
    return s

def art_gulf(w, h):
    s = rect(0, 0, w, h, "#14213d")
    for bx, bw, bh in [(0.05, 0.10, 0.30), (0.18, 0.08, 0.42), (0.70, 0.10, 0.36), (0.84, 0.10, 0.48)]:
        s += rect(w * bx, h * (0.80 - bh), w * bw, h * bh, "#1b2a4a")
    s += rect(0, h * 0.80, w, h * 0.20, "#0c1226")
    s += f'<path d="M {w*0.30} {h*0.30} l {w*0.16} {h*0.06} l -{w*0.16} {h*0.06} l {w*0.05} -{h*0.06} Z" fill="#8fa3c8"/>'
    s += line(w * 0.46, h * 0.36, w * 0.62, h * 0.44, "#c9a227", 1.5)
    s += star(w * 0.64, h * 0.45, h * 0.10, "#e76f51")
    s += star(w * 0.64, h * 0.45, h * 0.05, "#ffd166")
    s += rect(w * 0.56, h * 0.08, w * 0.40, h * 0.15, "#b3382c", rx=2)
    s += txt(w * 0.76, h * 0.19, "ALERTS", h * 0.10, "#fff", SANS, "bold", "middle")
    return s

def art_speaker(w, h):
    s = rect(0, 0, w, h, "#e8e4da")
    s += f'<path d="M {w*0.30} {h*0.46} a {w*0.20} {h*0.24} 0 0 1 {w*0.40} 0 Z" fill="#a8a294"/>'
    s += rect(w * 0.26, h * 0.46, w * 0.48, h * 0.26, "#f0ead8")
    for cx in (0.32, 0.44, 0.56, 0.66):
        s += rect(w * cx, h * 0.50, w * 0.04, h * 0.22, "#a8a294")
    s += rect(w * 0.22, h * 0.72, w * 0.56, h * 0.06, "#6b6459")
    s += line(w * 0.78, h * 0.30, w * 0.90, h * 0.42, "#8a5a3b", 3)
    s += rect(w * 0.84, h * 0.38, w * 0.12, h * 0.08, "#8a5a3b", rx=2)
    if h >= 90:
        s += rect(w * 0.60, h * 0.08, w * 0.36, h * 0.16, "#2e5f8a", rx=2)
        s += txt(w * 0.78, h * 0.20, "251-11", h * 0.11, "#fff", SANS, "bold", "middle")
    return s

def art_vangogh(w, h):
    s = ('<defs><linearGradient id="vgSky" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#2e5f8a"/><stop offset="1" stop-color="#e76f51"/></linearGradient></defs>')
    s += rect(0, 0, w, h, "#f0e9dc")
    s += rect(w * 0.16, h * 0.08, w * 0.52, h * 0.72, "#c9a227")
    s += rect(w * 0.20, h * 0.12, w * 0.44, h * 0.64, "url(#vgSky)")
    s += line(w * 0.42, h * 0.70, w * 0.42, h * 0.36, "#3d2b1f", 3)
    for cx, cy, r in [(0.36, 0.30, 0.07), (0.46, 0.26, 0.08), (0.52, 0.34, 0.06), (0.40, 0.40, 0.06), (0.50, 0.44, 0.05)]:
        s += f'<circle cx="{w*cx}" cy="{h*cy}" r="{h*r}" fill="#f4a259" opacity="0.9"/>'
    if h >= 90:
        s += rect(w * 0.66, h * 0.60, w * 0.32, h * 0.20, "#b3382c", rx=2)
        s += txt(w * 0.82, h * 0.74, "$190.4m", h * 0.10, "#fff", SANS, "bold", "middle")
    return s

def art_voyager(w, h):
    s = rect(0, 0, w, h, "#0c1226")
    for sx, sy in [(0.10, 0.15), (0.22, 0.65), (0.80, 0.20), (0.90, 0.70), (0.60, 0.10), (0.05, 0.85)]:
        s += f'<circle cx="{w*sx}" cy="{h*sy}" r="1" fill="#fff" opacity="0.8"/>'
    cx, cy = w * 0.38, h * 0.48
    s += f'<circle cx="{cx}" cy="{cy}" r="{h*0.20}" fill="#c9bfa8"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{h*0.13}" fill="#8a8478"/>'
    s += line(cx, cy, w * 0.62, h * 0.62, "#c9bfa8", 2)
    s += rect(w * 0.58, h * 0.58, w * 0.12, h * 0.10, "#8fa3c8")
    for r in (0.30, 0.40, 0.50):
        s += f'<path d="M {w*0.72} {h*0.48 - h*r*0.4} a {w*r*0.5} {h*r*0.5} 0 0 1 0 {h*r*0.8}" stroke="#c9a227" stroke-width="1.5" fill="none" opacity="{1.1 - r}"/>'
    if h >= 90:
        s += txt(w * 0.5, h * 0.94, "1 LIGHT-DAY OUT", h * 0.095, "#c9a227", SANS, "bold", "middle")
    return s

def art_cyclone(w, h):
    s = rect(0, 0, w, h, "#dfe9ee")
    cx, cy = w * 0.42, h * 0.42
    for r, sw in [(0.30, 3), (0.20, 3), (0.10, 2.5)]:
        s += f'<path d="M {cx - w*r} {cy} a {w*r} {h*r} 0 1 1 {w*r} {h*r}" stroke="#2e5f8a" stroke-width="{sw}" fill="none"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{h*0.05}" fill="#b3382c"/>'
    for i in range(3):
        y = h * (0.78 + i * 0.07)
        s += f'<path d="M 0 {y} q {w*0.08} {h*0.04} {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0" stroke="#2e6e63" stroke-width="1.5" fill="none"/>'
    if h >= 90:
        s += rect(w * 0.54, h * 0.10, w * 0.44, h * 0.16, "#b3382c", rx=2)
        s += txt(w * 0.76, h * 0.215, "RED ALERT", h * 0.085, "#fff", SANS, "bold", "middle")
    return s

def art_suneung(w, h):
    s = rect(0, 0, w, h, "#f0e9dc")
    s += rect(w * 0.14, h * 0.52, w * 0.56, h * 0.10, "#8a5a3b")
    s += rect(w * 0.18, h * 0.62, w * 0.05, h * 0.26, "#6b4a2f")
    s += rect(w * 0.60, h * 0.62, w * 0.05, h * 0.26, "#6b4a2f")
    s += rect(w * 0.22, h * 0.36, w * 0.30, h * 0.16, "#fff", "#6b6459", 1)
    s += line(w * 0.26, h * 0.42, w * 0.48, h * 0.42, "#9a948a", 1)
    s += line(w * 0.26, h * 0.47, w * 0.44, h * 0.47, "#9a948a", 1)
    s += f'<path d="M {w*0.56} {h*0.50} l {w*0.14} -{h*0.14} l {w*0.03} {h*0.03} l -{w*0.14} {h*0.14} Z" fill="#c9a227"/>'
    s += f'<circle cx="{w*0.82}" cy="{h*0.30}" r="{h*0.16}" fill="#fff" stroke="{NAVY}" stroke-width="2"/>'
    s += line(w * 0.82, h * 0.30, w * 0.82, h * 0.20, NAVY, 1.5)
    s += line(w * 0.82, h * 0.30, w * 0.89, h * 0.33, NAVY, 1.5)
    if h >= 90:
        s += txt(w * 0.5, h * 0.95, "D-1 · 08:40", h * 0.10, NAVY, SANS, "bold", "middle")
    return s

def art_cop(w, h):
    s = rect(0, 0, w, h, "#e6efe4")
    s += f'<circle cx="{w*0.34}" cy="{h*0.46}" r="{h*0.30}" fill="#2e6e63"/>'
    s += f'<path d="M {w*0.20} {h*0.36} q {w*0.10} {h*0.10} {w*0.24} {h*0.02}" stroke="#e6efe4" stroke-width="2" fill="none"/>'
    s += f'<path d="M {w*0.24} {h*0.56} q {w*0.12} {h*0.06} {w*0.22} -{h*0.04}" stroke="#e6efe4" stroke-width="2" fill="none"/>'
    s += rect(w * 0.70, h * 0.16, w * 0.06, h * 0.52, "#fff", "#6b6459", 1, rx=3)
    s += rect(w * 0.70, h * 0.42, w * 0.06, h * 0.26, "#b3382c", rx=3)
    s += f'<circle cx="{w*0.73}" cy="{h*0.74}" r="{h*0.09}" fill="#b3382c"/>'
    if h >= 90:
        s += txt(w * 0.5, h * 0.94, "21 ITEMS OPEN", h * 0.10, NAVY, SANS, "bold", "middle")
    return s

def art_tank(w, h):
    s = rect(0, 0, w, h, "#e3ddd0")
    for bx, bw, bh in [(0.62, 0.12, 0.34), (0.78, 0.14, 0.44)]:
        s += rect(w * bx, h * (0.72 - bh), w * bw, h * bh, "#a8a294")
    s += rect(0, h * 0.72, w, h * 0.28, "#c9bfa8")
    s += line(0, h * 0.60, w, h * 0.60, "#b3382c", 1.5)
    if h >= 90:
        s += txt(w * 0.86, h * 0.56, "YELLOW LINE", h * 0.07, "#b3382c", SANS, "bold", "end")
    s += rect(w * 0.14, h * 0.52, w * 0.34, h * 0.14, "#4a5d3a", rx=3)
    s += rect(w * 0.22, h * 0.42, w * 0.16, h * 0.10, "#4a5d3a", rx=2)
    s += line(w * 0.38, h * 0.46, w * 0.56, h * 0.44, "#4a5d3a", 2.5)
    s += f'<circle cx="{w*0.20}" cy="{h*0.68}" r="{h*0.06}" fill="#2f3d24"/>'
    s += f'<circle cx="{w*0.30}" cy="{h*0.68}" r="{h*0.06}" fill="#2f3d24"/>'
    s += f'<circle cx="{w*0.40}" cy="{h*0.68}" r="{h*0.06}" fill="#2f3d24"/>'
    return s

def art_flood(w, h):
    s = rect(0, 0, w, h, "#e3e9ee")
    for i in range(7):
        x = w * (0.08 + i * 0.13)
        s += line(x, h * 0.06, x - w * 0.02, h * 0.20, "#2e5f8a", 1.5)
    s += f'<path d="M {w*0.28} {h*0.52} L {w*0.5} {h*0.30} L {w*0.72} {h*0.52} Z" fill="#8a5a3b"/>'
    s += rect(w * 0.32, h * 0.52, w * 0.36, h * 0.24, "#c9bfa8")
    s += rect(w * 0.44, h * 0.58, w * 0.10, h * 0.18, "#6b4a2f")
    s += rect(0, h * 0.70, w, h * 0.30, "#2e6e63", opacity=0.85)
    s += f'<path d="M 0 {h*0.72} q {w*0.08} {h*0.03} {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0 t {w*0.16} 0" stroke="#dfe9ee" stroke-width="1.5" fill="none"/>'
    if h >= 90:
        s += txt(w * 0.5, h * 0.92, "EMERGENCY", h * 0.10, "#fff", SANS, "bold", "middle")
    return s

def art_border(w, h):
    s = rect(0, 0, w, h, "#f0e6dc")
    s += f'<path d="M {w*0.08} {h*0.70} L {w*0.30} {h*0.30} L {w*0.50} {h*0.70} Z" fill="#3a7d44" opacity="0.8"/>'
    s += f'<path d="M {w*0.50} {h*0.70} L {w*0.70} {h*0.30} L {w*0.92} {h*0.70} Z" fill="#2e5f8a" opacity="0.8"/>'
    s += line(w * 0.5, h * 0.20, w * 0.5, h * 0.80, "#b3382c", 1.5)
    s += f'<path d="M {w*0.5} {h*0.30} l {w*0.09} {h*0.16} l -{w*0.18} 0 Z" fill="#c9a227" stroke="{INK}" stroke-width="1"/>'
    s += txt(w * 0.5, h * 0.44, "!", h * 0.12, INK, SANS, "bold", "middle")
    if h >= 90:
        s += txt(w * 0.5, h * 0.94, "BADME · HORNS", h * 0.095, NAVY, SANS, "bold", "middle")
    return s

ARTS = {"summit": art_summit, "eu": art_eu, "gulf": art_gulf, "speaker": art_speaker,
        "vangogh": art_vangogh, "voyager": art_voyager, "cyclone": art_cyclone,
        "suneung": art_suneung, "cop": art_cop, "tank": art_tank,
        "flood": art_flood, "border": art_border}

def illustration(key, x, y, w, h):
    inner = ARTS[key](w, h)
    cid = f"clip-{key}-{int(x)}-{int(y)}"
    return (f'<g transform="translate({x:.1f},{y:.1f})">'
            f'<clipPath id="{cid}"><rect width="{w}" height="{h}" rx="3"/></clipPath>'
            f'<g clip-path="url(#{cid})">{inner}</g>'
            f'<rect width="{w}" height="{h}" fill="none" stroke="{LINE}" rx="3"/></g>')

# ---------------------------------------------------------------- world map
LAND = [
    [(-168,66),(-140,70),(-120,72),(-90,72),(-70,62),(-55,50),(-65,44),(-75,35),(-81,25),(-97,25),(-105,20),(-90,15),(-83,8),(-100,18),(-117,33),(-125,48),(-150,60)],
    [(-55,60),(-20,70),(-25,80),(-60,80)],
    [(-80,8),(-60,10),(-50,0),(-35,-8),(-40,-22),(-58,-35),(-70,-52),(-75,-45),(-72,-18),(-80,-5)],
    [(-10,36),(0,44),(-5,48),(0,52),(5,58),(10,64),(20,70),(30,70),(40,66),(40,50),(30,45),(25,36),(15,38),(5,36)],
    [(-17,15),(-5,35),(10,37),(32,31),(43,12),(51,11),(40,-5),(35,-20),(20,-35),(15,-30),(12,-18),(8,4),(-8,4)],
    [(40,66),(60,70),(80,72),(100,76),(120,72),(140,72),(160,66),(170,60),(155,50),(140,45),(130,42),(122,30),(110,20),(105,10),(100,5),(98,10),(92,20),(88,22),(80,8),(77,15),(70,22),(60,25),(50,30),(40,45)],
    [(95,5),(105,-5),(115,-8),(125,-8),(135,-4),(140,-8),(130,-3),(120,0),(110,2),(100,3)],
    [(114,-22),(122,-18),(130,-12),(137,-12),(142,-11),(146,-19),(150,-25),(153,-30),(146,-39),(137,-35),(129,-32),(115,-34)],
    [(172,-34),(178,-38),(174,-42),(167,-46),(170,-40)],
    [(130,31),(135,34),(140,40),(142,45),(140,42),(136,36),(131,33)],
    [(-5,50),(-3,58),(-6,58),(-8,52)],
    [(-84,30),(-80,30),(-79.5,26),(-81,24.5),(-82.5,27)],
]

def inside(poly, lon, lat):
    ok = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]; xj, yj = poly[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            ok = not ok
        j = i
    return ok

PINS = [(1, 114.1, 22.5), (2, 4.4, 50.8), (3, 48.0, 29.0), (4, -77.0, 38.9),
        (5, -74.0, 40.7), (6, -120.0, 34.0), (7, 85.8, 20.3), (8, 127.0, 37.5),
        (9, 30.7, 36.9), (10, 34.4, 31.4), (11, -80.1, 26.0), (12, 38.0, 14.5)]

def world_map(x, y, w, h):
    s = rect(x, y, w, h, NAVY, rx=4)
    s += txt(x + 10, y + 16, "WHERE IT HAPPENED", 10, "#f7f2e6", SANS, "bold", spacing=1)
    mx, my, mw, mh = x + 8, y + 24, w - 16, h - 46
    def px(lon): return mx + (lon + 180) / 360 * mw
    def py(lat): return my + (78 - lat) / 140 * mh
    cols, rows = 76, 32
    for r in range(rows):
        lat = 78 - (r + 0.5) * 140 / rows
        for c in range(cols):
            lon = -180 + (c + 0.5) * 360 / cols
            if any(inside(p, lon, lat) for p in LAND):
                s += f'<circle cx="{px(lon):.1f}" cy="{py(lat):.1f}" r="1.3" fill="#c9bfa8" opacity="0.85"/>'
    for lon, lat in [(-81.5, 29.5), (-80.8, 28.0), (-80.3, 26.3), (-80.6, 25.0), (-82.0, 28.5), (-83.0, 29.8)]:
        s += f'<circle cx="{px(lon):.1f}" cy="{py(lat):.1f}" r="1.3" fill="#c9bfa8" opacity="0.85"/>'
    for n, lon, lat in PINS:
        cx, cy = px(lon), py(lat)
        if n == 5: cx += 10; cy += 8
        if n == 6: cx -= 4; cy -= 6
        if n == 9: cx -= 4; cy -= 5
        if n == 10: cx += 3; cy += 5
        if n == 3: cx += 4; cy += 3
        s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="6.5" fill="{RED}" stroke="#f7f2e6" stroke-width="1"/>'
        s += txt(cx, cy + 2.8, str(n), 7.5, "#fff", SANS, "bold", "middle")
    s += txt(x + 10, y + h - 8, "Red pins: stories 1-12. Positions approximate.", 7.5, "#c9bfa8", SANS, style="italic")
    return s

# ---------------------------------------------------------------- page assembly
def build():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(rect(0, 0, W, H, PAPER))
    s.append(rect(M - 6, M - 6, CW + 12, H - 2 * M + 12, "none", LINE, 1))

    s.append(txt(M, M + 12, "THE WORLD IN ONE DAY", 12, RED, SANS, "bold", spacing=2))
    s.append(txt(W - M, M + 12, "WEDNESDAY'S NEWS · ONE PAGE · 36 STORIES · 12 DRAWN", 9, GREY, SANS, anchor="end", spacing=1))
    s.append(line(M, M + 20, W - M, M + 20, INK, 1.5))

    s.append(txt(W / 2, M + 64, "Wednesday 18 November 2026", 48, INK, SERIF, "bold", "middle"))
    s.append(line(M, M + 74, W - M, M + 74, INK, 2))
    s.append(line(M, M + 78, W - M, M + 78, INK, 0.75))
    s.append(txt(W / 2, M + 94, "Xi welcomes Trump to APEC · Brussels offers Kyiv €45bn · The Gulf intercepts Iranian drones", 13, RED, SERIF, "bold", "middle", style="italic"))

    ry = M + 102
    counts = {k: sum(1 for st in STORIES if st[6] == k) + sum(1 for b in BRIEFS if b[3] == k) for k, _, _ in REGIONS}
    seg = CW / len(REGIONS)
    for i, (k, label, col) in enumerate(REGIONS):
        x = M + i * seg
        s.append(rect(x, ry, seg - 3, 18, col, rx=2))
        s.append(txt(x + (seg - 3) / 2, ry + 12.5, f"{label} {counts[k]}", 8.5, "#fff", SANS, "bold", "middle"))

    sy = ry + 24
    sw = (CW - 5 * 8) / 6
    for i, (num, lab, col) in enumerate(STATS):
        x = M + i * (sw + 8)
        s.append(rect(x, sy, sw, 46, CREAM2, LINE, 0.75, rx=3))
        s.append(txt(x + sw / 2, sy + 19, num, 16, col, SERIF, "bold", "middle"))
        for j, ln in enumerate(wrap(lab, 30)[:2]):
            s.append(txt(x + sw / 2, sy + 31 + j * 9, ln, 7.3, GREY, SANS, anchor="middle"))

    ty = sy + 52
    s.append(rect(M, ty, 92, 22, RED, rx=2))
    s.append(txt(M + 46, ty + 14.5, "THE DAY · UTC", 8.5, "#fff", SANS, "bold", "middle"))
    tw = (CW - 92 - 5 * 4) / 5
    for i, (tm, ev) in enumerate(TIMELINE):
        x = M + 92 + 4 + i * (tw + 4)
        s.append(rect(x, ty, tw, 22, "#fff", LINE, 0.75, rx=2))
        s.append(txt(x + 6, ty + 9.5, tm, 7.5, RED, SANS, "bold"))
        s.append(txt(x + 6, ty + 18.5, ev, 7.0, INK, SANS))

    hy = ty + 28
    hw = (CW - 2 * 10) / 3
    hh = 228
    for i, st in enumerate(STORIES[:3]):
        n, place, topic, src, head, deck, reg, art = st
        x = M + i * (hw + 10)
        s.append(rect(x, hy, hw, hh, "#fff", LINE, 1, rx=4))
        s.append(illustration(art, x + 6, hy + 6, hw - 12, 100))
        s.append(f'<circle cx="{x+16}" cy="{hy+115}" r="8" fill="{RED}"/>')
        s.append(txt(x + 16, hy + 118, str(n), 9, "#fff", SANS, "bold", "middle"))
        s.append(txt(x + 30, hy + 118, f"{place} · {topic}", 9, RED, SANS, "bold", spacing=0.5))
        s.append(txt(x + hw - 8, hy + 118, src, 7.5, GREY, SANS, anchor="end"))
        yy = hy + 140
        for ln in wrap(head, 33)[:2]:
            s.append(txt(x + 10, yy, ln, 18, INK, SERIF, "bold"))
            yy += 20
        yy += 2
        for ln in wrap(deck, 58)[:4]:
            s.append(txt(x + 10, yy, ln, 10, "#3d3a34", SANS))
            yy += 12.5

    gy = hy + hh + 8
    gw = (CW - 2 * 8) / 3
    gh = 76
    for i, st in enumerate(STORIES[3:]):
        n, place, topic, src, head, deck, reg, art = st
        r, c = divmod(i, 3)
        x = M + c * (gw + 8)
        y = gy + r * (gh + 6)
        s.append(rect(x, y, gw, gh, "#fff", LINE, 0.75, rx=3))
        s.append(illustration(art, x + 4, y + 5, 66, gh - 10))
        tx = x + 78
        s.append(txt(tx, y + 15, f"{n} · {place} · {topic}", 8.2, RED, SANS, "bold"))
        s.append(txt(x + gw - 6, y + 15, src, 7, GREY, SANS, anchor="end"))
        yy = y + 31
        for ln in wrap(head, 38)[:2]:
            s.append(txt(tx, yy, ln, 13, INK, SERIF, "bold"))
            yy += 14
        for ln in wrap(deck, 52)[:1]:
            s.append(txt(tx, y + 64, ln, 8.5, "#3d3a34", SANS))

    by = gy + 3 * gh + 2 * 6 + 8
    bh = 172
    mapw = 300
    s.append(world_map(M, by, mapw, bh))
    bx = M + mapw + 12
    bw = CW - mapw - 12
    s.append(txt(bx, by + 12, "ALSO ON WEDNESDAY 18 NOVEMBER — 24 MORE STORIES", 10, INK, SANS, "bold", spacing=0.5))
    s.append(line(bx, by + 18, bx + bw, by + 18, INK, 1))
    colw = bw / 3
    per = 8
    for i, (n, place, text, reg) in enumerate(BRIEFS):
        c, r = divmod(i, per)
        x = bx + c * colw
        y = by + 32 + r * 18.5
        s.append(txt(x, y, f"{n} · {place}", 8.2, RED, SANS, "bold"))
        s.append(txt(x, y + 9, wrap(text, 50)[0], 8.2, INK, SANS))

    dy = by + bh + 8
    dh = 68
    s.append(rect(M, dy, CW, dh, "#fdf6ee", RED, 1.25, rx=4))
    s.append(txt(M + 10, dy + 15, "DATE CHECK — LEFT OFF THIS PAGE ON PURPOSE", 9.5, RED, SANS, "bold", spacing=0.5))
    dcw = (CW - 30) / 2
    for i, item in enumerate(DATECHECK):
        c, r = divmod(i, 4)
        x = M + 12 + c * (dcw + 6)
        y = dy + 30 + r * 10.5
        s.append(txt(x, y, "· " + item, 8, "#5a4632", SANS))

    fy = dy + dh + 6
    s.append(line(M, fy, W - M, fy, INK, 1))
    s.append(txt(W / 2, fy + 13, "Every story here happened, or was first reported, on Wednesday 18 November 2026, in some time zone.", 9.3, INK, SERIF, "bold", "middle", style="italic"))
    s.append(txt(W / 2, fy + 25, "Disputed claims are attributed, not stated as fact. Original drawings. Reads at thumbnail, half and full size.", 8, GREY, SANS, anchor="middle"))
    s.append(txt(W / 2, fy + 36, "Sources: Xinhua · NYT · Reuters · AP · EC · Euronews · NASA · Pew · Korea Herald · IMD · NWS · Gulf News · Roll Call · Africa Center", 7.3, GREY, SANS, anchor="middle"))

    s.append("</svg>")
    return "\n".join(s)

if __name__ == "__main__":
    svg = build()
    with open("news_front.svg", "w") as f:
        f.write(svg)
    print(f"wrote news_front.svg ({len(svg)} bytes)")
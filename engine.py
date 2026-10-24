"""HTML builders for the site: pages, deck chrome, slide components. No content lives here."""
import html
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE_URL = "https://polodev.github.io/ananya"   # absolute URL is only used for og:url; every link in the site is relative
SITE_NAME = "ভাষার ঘর"
SITE_NAME_EN = "Language Corner"
DIG = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
esc = html.escape

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;500;600;700&family=Klee+One:wght@400;600'
         '&family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">')


def bn(n):
    return str(n).translate(DIG)


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def head(base, title, description, url_path):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description, quote=True)}">
<meta name="theme-color" content="#4F46E5">
<link rel="icon" type="image/png" href="{base}assets/img/favicon.png"><link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title, quote=True)}">
<meta property="og:description" content="{esc(description, quote=True)}"><meta property="og:url" content="{SITE_URL}/{url_path}">
{FONTS}
<link rel="stylesheet" href="{base}assets/app.css">"""


DESC = "বাংলায় ইংরেজি (A2, B1, B2), জাপানি (A1), জার্মান (A1) আর টেকনোলজি — মোবাইলে, স্লাইডে, শুনে শুনে।"


def page(path, title, body, theme="home", description=DESC):
    """path: output file relative to the site root, e.g. 'english/a2/index.html'."""
    depth = path.count("/")
    base = "../" * depth
    url_path = path[:-len("index.html")] if path.endswith("index.html") else path
    write(path, f"""<!doctype html>
<html lang="bn">
<head>
{head(base, title, description, url_path)}
</head>
<body class="t-{theme}">
{body}
<script src="{base}assets/app.js"></script>
</body>
</html>
""")


def footer():
    return f'<footer class="foot"><span>{SITE_NAME} · {SITE_NAME_EN}</span></footer>'


# ------------------------------------------------------------------ small components
def say_btn(text, lang, big=False):
    return f'<button class="say{" big" if big else ""}" data-say="{esc(text, quote=True)}" data-lang="{lang}" aria-label="শুনুন">🔊</button>'


def chunks(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def section(icon, title, sub="", note=""):
    """a full slide that only names the next section; the card slides after it carry no heading."""
    return slide(f'<div class="section"><div class="s-icon">{icon}</div><h2>{title}</h2>'
                 + (f'<p class="s-sub">{sub}</p>' if sub else "") + (f'<p class="hint">{note}</p>' if note else "") + "</div>",
                 "section-slide", title)


def cards(items, cls="cards", step=1):
    """a list app.js may spread over several slides so nothing has to scroll (step: keep groups of N together)."""
    return f'<div class="{cls}" data-split data-step="{step}">{"".join(items)}</div>'


def slide(inner, cls="", title=""):
    return f'<section class="slide {cls}" data-title="{esc(title, quote=True)}"><div class="inner">{inner}</div></section>'


def cover(chip, h1, lead, learn, extra="", hint=True):
    items = "".join(f"<li>{x}</li>" for x in learn)
    return slide(f'<span class="chip">{esc(chip)}</span><h1>{h1}</h1>{extra}<p class="lead">{lead}</p>'
                 f'<p class="five">⏱ আজকের লক্ষ্য: ১০ মিনিট। পুরোটা না পারলে যতটুকু পারো — কাল বাকিটা।</p><ul class="learn">{items}</ul>'
                 + ('<p class="hint">👉 ডান থেকে বামে swipe করে পরের স্লাইডে যাও — শুধু বাঁ-ডানে, উপর-নিচে কিছু নেই</p>' if hint else ""), "cover", "শুরু")


def quiz_slide(questions, title="কুইজ"):
    data = esc(json.dumps(questions, ensure_ascii=False), quote=True)
    return slide(f'<span class="chip">📝 {esc(title)}</span><div class="quiz" data-quiz="{data}"></div>', "", title)


def finish_slide(heading, lead, chips, next_href=None, next_label="", extra=""):
    nxt = f'<a class="btn" href="{next_href}">{next_label} →</a>' if next_href else ""
    chip_html = "".join(f"<span>{c}</span>" for c in chips)
    return slide(f'<div class="finish"><div class="party">🎉</div><h2>{heading}</h2><p class="lead">{lead}</p>'
                 f'<div class="wordlist">{chip_html}</div>{extra}'
                 f'<div class="btns">{nxt}<a class="btn ghost" href="../index.html">সব অধ্যায়</a></div></div>', "", "শেষ")


def deck_page(path, title, deck_key, theme, slides, crumb, has_bn=False, has_pr=True, has_slow=True):
    depth = path.count("/")
    base = "../" * depth
    btns = (('<button id="prBtn" title="উচ্চারণ লুকাও" aria-label="উচ্চারণ লুকাও">🔤</button>' if has_pr else "")
            + ('<button id="bnBtn" title="বাংলা অর্থ লুকাও" aria-label="বাংলা অর্থ লুকাও">👁</button>' if has_bn else ""))
    slow = '<button id="slow" title="ধীরে বলো" aria-label="ধীরে">🐢</button>' if has_slow else ""
    body = (f'<div id="top"><a href="../index.html">← সব অধ্যায়</a><span class="crumb">{esc(crumb)}</span><a href="{base}index.html" class="home" aria-label="হোম">🏠</a></div><div id="bar"></div>'
            f'<main id="deck">{chr(10).join(slides)}</main>'
            '<nav id="nav"><button id="prev" aria-label="আগের">‹</button><span id="count"></span><button id="next" aria-label="পরের">›</button>'
            f'{slow}{btns}'
            '<button id="theme" title="Dark mode" aria-label="Theme">◐</button></nav>')
    url_path = path[:-len("index.html")]
    write(path, f"""<!doctype html>
<html lang="bn">
<head>
{head(base, title, DESC, url_path)}
</head>
<body class="t-{theme} deck{' has-bn' if has_bn else ''}" data-deck="{deck_key}">
{body}
<script src="{base}assets/app.js"></script>
</body>
</html>
""")


# ------------------------------------------------------------------ quiz helpers
def mcq(rng, correct, pool, n=4):
    """Options list with `correct` at a random place; distractors drawn from pool (unique, != correct)."""
    others = [p for p in dict.fromkeys(pool) if p != correct]
    rng.shuffle(others)
    opts = others[:n - 1] + [correct]
    rng.shuffle(opts)
    return opts, opts.index(correct)


def seeded(*parts):
    return random.Random("|".join(map(str, parts)))

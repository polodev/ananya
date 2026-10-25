"""Builds the whole site (static HTML).   python3 build.py

Course outlines: curriculum.py. Topic chapters: content/<course>/ch-NN.json. Letter chapters: letters_ja.py, letters_de.py.
Relative links everywhere, so it works at https://polodev.github.io/ananya/ and at any domain root."""
import shutil

from curriculum import COURSES, LANGS
from engine import ROOT, SITE_NAME, avatar, bn, esc, footer, page, say_btn, write
from learner import AGE, FULL_NAME, INTRODUCTION, NAME_BN
import site_builder
import site_letters
import site_tech
import site_topic


def courses_of(lang):
    return {k: c for k, c in COURSES.items() if c["lang"] == lang}


def counts(c):
    if c["chapters"][0]["kind"] == "tech":
        return f"{bn(len(c['chapters']))} অধ্যায় · {bn(c['slides_total'])} স্লাইড"
    if c["chapters"][0]["kind"] == "builder":
        return f"{bn(len(c['chapters']))} অধ্যায় · {bn(len(c['chapters']) * 10)}টি বাক্য, ধাপে ধাপে"
    letters = sum(ch["kind"] == "letters" for ch in c["chapters"])
    topics = len(c["chapters"]) - letters
    parts = [f"{bn(len(c['chapters']))} অধ্যায়"]
    if letters:
        parts.append(f"{bn(letters)}টি অক্ষর-সংখ্যার")
    parts.append(f"{bn(topics * 10)} শব্দ · {bn(topics * 40)} বাক্য")
    return " · ".join(parts)


def home():
    tech = LANGS["technology"]
    tech_card = (f'<a class="card tech-feature" href="technology/index.html"><span class="tf-tag">নতুন · ১০টি কোর্স</span>'
                 f'<div class="tf-top"><div class="tf-badge">{tech["badge"]}</div><div><b>Technology — {tech["bn"]}</b>'
                 f'<span>{tech["intro"]}</span></div></div>'
                 f'<span class="tf-path">101 → 201 → 301 → … → 1001</span></a>')
    cards = "".join(
        f'<a class="card lang {v["theme"]}" href="{k}/index.html"><div class="badge">{v["badge"]}</div><div><b>{v["name"]} — {v["bn"]}</b>'
        f'<span>{v["intro"]}</span><br><span class="levels">{" · ".join(c["level"] for c in courses_of(k).values())}</span></div></a>'
        for k, v in LANGS.items() if k != "technology")
    introduction = "".join(
        f'<div class="intro-line">{say_btn(x["text"], "en-US")}<div><p lang="en">{esc(x["text"])}</p>'
        f'<p class="intro-pr">{esc(x["pron_bn"])}</p><p class="intro-bn">{esc(x["bn"])}</p></div></div>'
        for x in INTRODUCTION)
    personal = (f'<section class="card personal-start" aria-labelledby="personal-title"><span class="personal-tag">তোমার নিজের শেখার ঘর</span>'
                f'<h2 id="personal-title">অনন্যা, ছোট ছোট পদক্ষেপেই এগিয়ে যাও।</h2>'
                f'<p>মাস্টার্সের পড়া আর আদ্যর সাথে সময়ের পাশে, নিজের শেখার জন্যও একটু সময়। আজ ১০ মিনিট দিয়ে শুরু করো।</p>'
                f'<a class="btn" href="english/a2/ch-01/index.html">ইংরেজি দিয়ে শুরু করো →</a>'
                f'<details class="personal-intro"><summary>নিজের পরিচয় ইংরেজিতে বলো 🔊</summary><div class="intro-lines">{introduction}</div></details></section>')
    body = (f'<header class="hero"><div class="in hero-grid"><div class="hero-copy">'
            f'<p class="eyebrow" data-greet="অনন্যা">স্বাগতম, অনন্যা! 👋</p><h1>{FULL_NAME}</h1>'
            f'<p class="hero-name">{NAME_BN}</p><p class="profile-meta">{bn(AGE)} বছর · মা · Management-এ মাস্টার্স</p>'
            f'<p>ভাষা শেখো, টেক শেখো — বাংলায়, তোমার নিজের গতিতে।</p></div>{avatar("", "hero-ava", zoom=True)}</div></header>'
            f'<main class="wrap">{personal}<h2 class="home-heading">আজ কী শিখবে?</h2>{cards}{tech_card}'
            f'<p class="note">🔊 ভাষার স্লাইডে উচ্চারণ শুনতে পাবে · 👆 বাঁ-ডানে swipe করো · ✅ অগ্রগতি এই ফোনেই জমা থাকে</p></main>'
            + footer())
    page("index.html", f"{FULL_NAME} — {SITE_NAME}", body)


def language_page(k, v):
    cards = ""
    for ck, c in courses_of(k).items():
        level = ck.split("/")[1]
        keys = " ".join(f"{ck}/ch-{n:02d}" for n in range(1, len(c["chapters"]) + 1))
        cards += (f'<a class="card course" href="{level}/index.html" data-coursekeys="{keys}"><span class="tag">{c["level"]}</span><b>{c["title"]} — {c["tag"]}</b>'
                  f'<span class="sub">{c["sub"]}</span><span class="sub">{counts(c)}</span><span class="cprog"></span></a>')
    body = (f'<header class="hero"><div class="in hero-grid"><div class="hero-copy"><a class="back" href="../index.html">← অনন্যার শেখার ঘর</a><h1>{v["name"]} — {v["bn"]}</h1><p>{v["intro"]}</p></div>{avatar("../", "hero-ava sm", zoom=True)}</div></header>'
            f'<main class="wrap">{cards}</main>' + footer())
    page(f"{k}/index.html", f"{v['name']} — {SITE_NAME}", body, v["theme"])


def course_page(ck, c):
    v = LANGS[c["lang"]]
    rows = []
    for n, ch in enumerate(c["chapters"], 1):
        if ch["kind"] == "builder":
            if not site_builder.ready(n):
                rows.append(f'<div class="day locked"><span class="n">অধ্যায়<b>{bn(n)}</b></span><span class="t"><b>{esc(ch["title_bn"])}</b>'
                            f'<span>{ch["level"]} · 🔒 শীঘ্রই আসছে</span></span></div>')
                continue
            sub = f'{ch["level"]} · {site_builder.load(n)["title"]}'
        elif ch["kind"] == "topic":
            d = site_topic.load(ck, n)
            sub = f'{d["title"]} · {d["grammar"]["title_bn"]}'
        elif ch["kind"] == "tech":
            sub = f'{ch["topic"]} · {bn(ch["slides"])} স্লাইড'
        else:
            sub = "অক্ষর ও উচ্চারণ" if "সংখ্যা" not in ch["title_bn"] else "সংখ্যা"
        rows.append(f'<a class="day" data-deckkey="{ck}/ch-{n:02d}" href="ch-{n:02d}/index.html"><span class="n">অধ্যায়<b>{bn(n)}</b></span>'
                    f'<span class="t"><b>{esc(ch["title_bn"])}</b><span>{esc(sub)}</span></span><span class="tick">✓</span></a>')
    total = len(c["chapters"])
    body = (f'<header class="hero"><div class="in hero-grid"><div class="hero-copy"><a class="back" href="../index.html">← {v["name"]}</a><h1>{c["title"]}</h1><p>{c["lead"]}</p></div>{avatar("../../", "hero-ava sm", zoom=True)}</div></header>'
            f'<main class="wrap"><div class="card"><div class="bar"><i id="progress"></i></div>'
            f'<p class="note" id="streak"></p><p class="note" id="progress-text">০ / {bn(total)} অধ্যায় শেষ</p>'
            f'<p style="text-align:center;margin-top:10px"><a class="btn" id="continue" href="ch-01/index.html">▶ শুরু করো</a></p></div>'
            f'<div class="days">{"".join(rows)}</div></main>' + footer())
    page(f"{ck}/index.html", f"{c['title']} — {c['tag']} · {NAME_BN}", body, v["theme"])


def not_found():
    body = ('<header class="hero"><div class="in"><h1>পাতাটি পাওয়া যায়নি</h1><p>ঠিকানাটা ভুল হতে পারে।</p></div></header>'
            '<main class="wrap"><a class="card" href="/" id="home404" style="text-align:center"><b>🏠 হোমে ফিরে যাও</b></a></main>')
    page("404.html", "404 — পাতা নেই", body)
    # 404.html is served from any depth: work out the site root at run time (project page vs custom domain)
    p = ROOT / "404.html"
    html = p.read_text(encoding="utf-8")
    html = html.replace('<link rel="stylesheet" href="assets/app.css">', "").replace('<script src="assets/app.js"></script>', "")
    html = html.replace("</body>", """<script>
var root = /\\.github\\.io$/.test(location.hostname) ? '/' + location.pathname.split('/')[1] + '/' : '/';
document.getElementById('home404').href = root;
var l = document.createElement('link'); l.rel = 'stylesheet'; l.href = root + 'assets/app.css'; document.head.appendChild(l);
</script></body>""")
    write("404.html", html)


if __name__ == "__main__":
    for k in LANGS:
        shutil.rmtree(ROOT / k, ignore_errors=True)
    home()
    for k, v in LANGS.items():
        language_page(k, v)
    for ck, c in COURSES.items():
        course_page(ck, c)
        for n, ch in enumerate(c["chapters"], 1):
            if ch["kind"] == "builder" and not site_builder.ready(n):
                continue
            {"topic": site_topic.build, "letters": site_letters.build, "builder": site_builder.build,
             "tech": site_tech.build}[ch["kind"]](ck, n)
    not_found()
    print(f"built {sum(1 for _ in ROOT.rglob('index.html'))} pages")

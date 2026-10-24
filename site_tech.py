"""Technology decks: cover, content slides, an auto-built quiz and the finish slide."""
from engine import bn, deck_page, finish_slide, mcq, quiz_slide, seeded, slide
from tech.courses import TECH_COURSES
from tech.render import _term, render, rich

TECH_KEYS = list(TECH_COURSES)


def load(course_key, n):
    return TECH_COURSES[course_key]["tech_chapters"][n - 1]


def _terms(ch):
    out, seen = [], set()
    for s in ch["slides"]:
        if s["kind"] != "terms":
            continue
        for x in s["items"]:
            term, meaning, detail = _term(x)
            if term and term not in seen:
                seen.add(term)
                out.append((term, meaning, detail))
    return out


def _profiles(ch):
    return [s for s in ch["slides"] if s["kind"] == "profile"]


def quiz_for(course_key, n, ch):
    rng = seeded(course_key, n, ch["title_bn"])
    qs = []
    terms = _terms(ch)
    if len(terms) >= 4:
        for term, meaning, detail in rng.sample(terms, min(3, len(terms))):
            opts, a = mcq(rng, meaning, [x[1] for x in terms if x[0] != term])
            if len(opts) == 4:
                qs.append(dict(q=f"“{term}” কী?", o=opts, a=a,
                               why=f"{term} = {meaning}." + (f" {detail}" if detail else "")))
    course_profiles = [x for c in TECH_COURSES[course_key]["tech_chapters"] for x in _profiles(c)]
    profiles = _profiles(ch)
    if len(course_profiles) >= 4:
        for p in rng.sample(profiles, min(2, len(profiles))):
            opts, a = mcq(rng, p["famous"], [x["famous"] for x in course_profiles if x["name"] != p["name"]])
            if len(opts) == 4:
                qs.append(dict(q=f"{p['name']} কী জন্য বিখ্যাত?", o=opts, a=a,
                               why=f"{p['name']}: {p['famous']}"))
    qs += [dict(q=x["q"], o=x["o"], a=x["a"], why=x.get("why", "")) for x in ch.get("quiz", [])]
    seen, out = set(), []
    for q in qs:
        if q["q"] not in seen:
            seen.add(q["q"])
            out.append(q)
    return out[:8]


def _chips(ch):
    if ch.get("chips"):
        return ch["chips"][:8]
    names = [x[0] for x in _terms(ch)] + [p["name"] for p in _profiles(ch)]
    return names[:8]


def tech_cover(course_key, n, ch):
    c = TECH_COURSES[course_key]
    mins = max(8, round(len(ch["slides"]) * 1.1))
    chips = "".join(f'<span>{rich(x)}</span>' for x in _chips(ch)[:5])
    inner = (f'<div class="t-cover"><div class="t-cover-top"><span class="chip">{c["title"]} · অধ্যায় {bn(n)}</span>'
             f'<span class="t-min">⏱ ~{bn(mins)} মিনিট</span></div>'
             f'<div class="t-cover-mark" aria-hidden="true">{c["icon"]}</div>'
             f'<h1>{rich(ch["title_bn"])}</h1><p class="t-en">{rich(ch["title_en"])}</p>'
             f'<p class="t-body">{rich(ch["hook"])}</p>'
             f'<div class="t-cover-chips">{chips}</div>'
             '<p class="hint">👉 ডান থেকে বামে swipe করো — প্রতিটি স্লাইডে একটা করে বড় ধারণা</p></div>')
    return slide(inner, "cover t-cover-slide", "শুরু")


def next_course(course_key):
    i = TECH_KEYS.index(course_key)
    return TECH_KEYS[i + 1] if i + 1 < len(TECH_KEYS) else None


def build(course_key, n):
    c = TECH_COURSES[course_key]
    ch = load(course_key, n)
    S = [tech_cover(course_key, n, ch)]
    for s in ch["slides"]:
        S.append(render(s, ch["title_bn"]))
    S.append(quiz_slide(quiz_for(course_key, n, ch), "এই অধ্যায়ের কুইজ"))

    chs = c["chapters"]
    if n < len(chs):
        nxt = chs[n]
        extra = f'<div class="callout"><b>পরের অধ্যায়</b><br>{rich(nxt["title_bn"])} — {rich(nxt["topic"])}</div>'
        S.append(finish_slide(f"অধ্যায় {bn(n)} শেষ! 🎉",
                              "আজকের ধারণাগুলো নিজের ভাষায় একবার বলো। তারপর পরের অধ্যায়ে যাও।",
                              _chips(ch), f"../ch-{n + 1:02d}/index.html",
                              f"অধ্যায় {bn(n + 1)}: {rich(nxt['title_bn'])}", extra))
    else:
        nc = next_course(course_key)
        if nc:
            extra = (f'<div class="callout"><b>এরপর কী?</b><br>{TECH_COURSES[nc]["title"]} — '
                     f'{rich(TECH_COURSES[nc]["tag"])}</div>')
            S.append(finish_slide(f"{rich(c['title'])} সম্পূর্ণ! 🏆",
                                  f"{bn(len(chs))}টি অধ্যায় শেষ। এখন পরের কোর্সে যাওয়ার সময়।",
                                  _chips(ch), f"../../{TECH_COURSES[nc]['level']}/index.html",
                                  f"{TECH_COURSES[nc]['title']} শুরু করো", extra))
        else:
            S.append(finish_slide("পুরো টেক ট্র্যাক শেষ! 🏆",
                                  "তুমি ১০টি কোর্স শেষ করেছ। এখন নিজের একটা ছোট প্রজেক্ট বানাও।",
                                  _chips(ch), None, "", '<div class="callout"><b>পরের কাজ</b><br>একটা ছোট ওয়েবসাইট বানাও, GitHub-এ রাখো, তারপর বন্ধুকে দেখাও।</div>'))

    deck_page(f"{course_key}/ch-{n:02d}/index.html",
              f"অধ্যায় {n} · {ch['title_bn']} — {c['title']}",
              f"{course_key}/ch-{n:02d}", "tech", S,
              f"অধ্যায় {bn(n)} · {ch['title_bn']}", has_bn=False, has_pr=False, has_slow=False)

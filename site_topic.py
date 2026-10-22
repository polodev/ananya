"""Topic chapters (content/<course>/ch-NN.json) -> deck pages. Same layout for English, Japanese and German."""
import json

from curriculum import COURSES, LANGS
from engine import ROOT, bn, cards, cover, deck_page, esc, finish_slide, mcq, quiz_slide, say_btn, section, seeded, slide
import letters_ja as JA


def load(course_key, n):
    return json.loads((ROOT / "content" / course_key.replace("/", "-") / f"ch-{n:02d}.json").read_text(encoding="utf-8"))


class Lang:
    """How to show and speak one target-language string."""

    def __init__(self, lang):
        self.lang, self.tts = lang, LANGS[lang]["tts"]
        self.ja = lang == "japanese"

    def say(self, text):
        return JA.speakable(text) if self.ja else text

    def pron(self, x):
        return JA.bangla(x["text"]) if self.ja else x.get("pron_bn", "")

    def body(self, text, pron, cls="tx"):
        if self.ja:
            return (f'<p class="{cls} jp">{esc(text)}</p><p class="ro">{esc(JA.romaji(text))}</p>'
                    f'<p class="pr">{esc(JA.bangla(text))}</p>')
        return f'<p class="{cls}">{esc(text)}</p>' + (f'<p class="pr">{esc(pron)}</p>' if pron else "")

    def line(self, x, speaker=""):
        who = f'<span class="who">{esc(speaker)}</span>' if speaker else ""
        return (f'<div class="line">{say_btn(self.say(x["text"]), self.tts)}<div>{who}{self.body(x["text"], self.pron(x))}'
                f'<p class="bn">{esc(x["bn"])}</p></div></div>')

    def word(self, w):
        ex = self.say(w["example"])
        ex_pron = f'<span class="ro">{esc(JA.romaji(w["example"]))}</span>' if self.ja else ""
        return (f'<div class="wcard">{say_btn(self.say(w["text"]), self.tts, big=True)}'
                f'<div class="w-en{" jp" if self.ja else ""}">{esc(w["text"])}</div>'
                f'<div class="w-pr pr">উচ্চারণ: {esc(self.pron(w))}{(" · " + esc(JA.romaji(w["text"]))) if self.ja else ""}</div>'
                f'<div class="bn w-bn">{esc(w["bn"])}</div>'
                f'<div class="w-ex"><button class="say sm" data-say="{esc(ex, quote=True)}" data-lang="{self.tts}" aria-label="শুনুন">🔊</button>'
                f'<span><span class="{"jp" if self.ja else ""}">{esc(w["example"])}</span>{ex_pron}<span class="bn">{esc(w["example_bn"])}</span></span></div></div>')


def quiz_for(course_key, n, d, L):
    rng = seeded(course_key, n)
    words, phrases = d["words"], d["phrases"]
    name = LANGS[L.lang]["name"]
    qs = []
    picked = rng.sample(words, 6)
    for w in picked[:4]:
        opts, a = mcq(rng, w["bn"], [x["bn"] for x in words])
        qs.append(dict(q=f"‘{w['text']}’ মানে কী?", say=L.say(w["text"]), lang=L.tts, o=opts, a=a, why=f"{w['text']} = {w['bn']}"))
    for w in picked[4:]:
        opts, a = mcq(rng, w["text"], [x["text"] for x in words])
        qs.append(dict(q=f"‘{w['bn']}’ — {name}-এ কোনটা?", o=opts, a=a, why=f"{w['bn']} = {w['text']} ({L.pron(w)})"))
    ps = rng.sample(phrases, 3)
    for i, p in enumerate(ps):
        opts, a = mcq(rng, p["bn"], [x["bn"] for x in phrases])
        if i == 2:
            qs.append(dict(q="🎧 শোনো — কী বলল? (🔊 আবার শুনতে চাপো)", say=L.say(p["text"]), lang=L.tts, auto=True, o=opts, a=a,
                           why=f"{p['text']} = {p['bn']}"))
        else:
            qs.append(dict(q=f"“{p['text']}” — এর বাংলা কোনটা?", say=L.say(p["text"]), lang=L.tts, o=opts, a=a, why=p["bn"]))
    for g in d["grammar"]["quiz"]:
        qs.append(dict(q=g["q"], o=g["options"], a=g["answer"], why=g["why_bn"]))
    return qs


def build(course_key, n):
    c = COURSES[course_key]
    lang = c["lang"]
    L = Lang(lang)
    d = load(course_key, n)
    meta = c["chapters"][n - 1]
    g = d["grammar"]
    dialogue = any(x["speaker"].strip() for x in d["reading"])
    r_icon, r_name = ("💬", "কথোপকথন") if dialogue else ("📖", "পড়া")
    tts = L.tts
    jp = ' class="jp"' if L.ja else ""
    title_say = f'<p class="sub-title">{say_btn(L.say(d["title"]), tts)}<span{jp}>{esc(d["title"])}</span></p>'
    S = [cover(f"{c['title']} · অধ্যায় {bn(n)}", esc(meta["title_bn"]), esc(d["intro_bn"]),
               [f"{r_icon} {r_name} ({bn(len(d['reading']))} লাইন)", "🔤 ১০টি নতুন শব্দ", f"🗣️ {bn(len(d['phrases']))}টি দরকারি বাক্য",
                f"✏️ ব্যাকরণ: {esc(g['title_bn'])}", f"📝 {bn(len(g['quiz']) + 9)} প্রশ্নের কুইজ"], extra=title_say)]

    # each section = one full title slide, then card slides with no heading (app.js spreads cards so nothing scrolls)
    S.append(section(r_icon, r_name, f'<span{jp}>{esc(d["title"])}</span>', "🔊 চাপলে শুনবে · 🔤 উচ্চারণ আর 👁 বাংলা লুকিয়ে নিজেকে পরীক্ষা করো"))
    S.append(slide(cards([L.line(x, x["speaker"]) for x in d["reading"]]), "", r_name))
    S.append(section("🔤", "নতুন শব্দ", f"{bn(len(d['words']))}টি শব্দ, প্রতিটির সাথে একটি উদাহরণ"))
    S.append(slide(cards([L.word(w) for w in d["words"]]), "", "শব্দ"))
    S.append(section("🗣️", "দরকারি বাক্য", f"{bn(len(d['phrases']))}টি বাক্য", "আগে নিজে জোরে বলো, তারপর 🔊 চেপে মিলিয়ে নাও"))
    S.append(slide(cards([L.line(x) for x in d["phrases"]]), "", "বাক্য"))
    S.append(section("✏️", "ব্যাকরণ", esc(g["title_bn"])))
    S.append(slide(cards([f'<div class="pt">{p}</div>' for p in g["points_bn"]]), "", "ব্যাকরণ"))   # <b> only, checked by validate.py
    S.append(slide(cards([L.line(x) for x in g["examples"]]), "", "উদাহরণ"))
    S.append(slide(f'<span class="chip">💡 টিপস</span><div class="callout">{esc(d["tip_bn"])}</div>'
                   '<div class="callout warn">🎯 আজকের কাজ: বাক্যগুলোর মধ্যে ৩টি বেছে নিয়ে নিজের জীবনের কথা দিয়ে বদলে বলো।</div>', "", "টিপস"))
    S.append(quiz_slide(quiz_for(course_key, n, d, L)))

    chs = c["chapters"]
    chips = [esc(w["text"]) for w in d["words"]]
    if n < len(chs):
        S.append(finish_slide(f"অধ্যায় {bn(n)} শেষ!", "আজকের নতুন শব্দগুলো দিনে কয়েকবার জোরে বলো — কাল আবার দেখা হবে।", chips,
                              f"../ch-{n + 1:02d}/index.html", f"অধ্যায় {bn(n + 1)}: {esc(chs[n]['title_bn'])}"))
    else:
        nxt = next_course(course_key)
        extra = (f'<div class="callout"><b>এরপর কী?</b><br>পরের ধাপ: {esc(COURSES[nxt]["title"])} — {esc(COURSES[nxt]["tag"])}।</div>' if nxt else
                 '<div class="callout"><b>এরপর কী?</b><br>পুরনো অধ্যায়ের বাক্যগুলো রোজ ৫ মিনিট জোরে বলো। পরের স্তর শীঘ্রই আসছে।</div>')
        S.append(finish_slide(f"{esc(c['title'])} সম্পূর্ণ! 🏆", f"{bn(len(chs))}টি অধ্যায় শেষ — দারুণ কাজ!", chips,
                              f"../../{nxt.split('/')[1]}/index.html" if nxt else None, COURSES[nxt]["title"] if nxt else "", extra))
    deck_page(f"{course_key}/ch-{n:02d}/index.html", f"অধ্যায় {n} · {meta['title_bn']} — {c['title']}", f"{course_key}/ch-{n:02d}",
              LANGS[lang]["theme"], S, f"অধ্যায় {bn(n)} · {meta['title_bn']}", has_bn=True, has_pr=True)


def next_course(course_key):
    keys = [k for k in COURSES if k.split("/")[0] == course_key.split("/")[0]]
    i = keys.index(course_key)
    return keys[i + 1] if i + 1 < len(keys) else None

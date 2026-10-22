"""Sentence Builder chapters (content/english-builder/ch-NN.json) -> deck pages. One builder per slide: the sentence
grows step by step and the words each step adds are highlighted. Tap a step to hear it and see the Bangla."""
import json

from curriculum import COURSES
from engine import ROOT, bn, cover, deck_page, esc, finish_slide, mcq, quiz_slide, section, seeded, slide
from validate import step_diff

KEY = "english/builder"
TTS = "en-US"


def ready(n):
    return (ROOT / "content" / "english-builder" / f"ch-{n:02d}.json").exists()


def load(n):
    return json.loads((ROOT / "content" / "english-builder" / f"ch-{n:02d}.json").read_text(encoding="utf-8"))


def marked(prev, cur):
    """the sentence with each run of new words wrapped in <mark class="add">."""
    if prev is None:
        return esc(cur)
    out, run = [], []
    for tok, new in step_diff(prev, cur) + [("", False)]:
        if new:
            run.append(esc(tok))
            continue
        if run:
            out.append(f'<mark class="add">{" ".join(run)}</mark>')
            run = []
        if tok:
            out.append(esc(tok))
    return " ".join(out)


def builder_slide(i, b):
    rows, prev = [], None
    for k, st in enumerate(b["steps"], 1):
        pron = f'<p class="pr">{esc(st["pron_bn"])}</p>' if st["pron_bn"] else ""
        rows.append(f'<div class="bstep" data-say="{esc(st["text"], quote=True)}" data-lang="{TTS}" role="button" tabindex="0">'
                    f'<span class="bn-no">{k}</span><div class="b-body"><p class="b-tx">{marked(prev, st["text"])}</p>'
                    f'<div class="b-more">{pron}<p class="bn">{esc(st["bn"])}</p></div></div><span class="chev">›</span></div>')
        prev = st["text"]
    size = sum(len(st["text"]) for st in b["steps"])
    dens = "tight" if size > 430 else "dense" if size > 280 else ""
    return slide(f'<p class="b-count">বাক্য {bn(i)} / ১০</p><div class="bld {dens}">{"".join(rows)}</div>'
                 f'<p class="hint b-note">💡 {esc(b["note_bn"])}</p>', "", f"বাক্য {i}")


def quiz_for(n, d):
    rng = seeded(KEY, n)
    finals = [b["steps"][-1] for b in d["builders"]]
    qs = []
    for st in rng.sample(finals, 8):
        opts, a = mcq(rng, st["bn"], [x["bn"] for x in finals])
        qs.append(dict(q=f"“{st['text']}” — এর মানে কী?", say=st["text"], lang=TTS, o=opts, a=a, why=f'{st["text"]} = {st["bn"]}'))
    for b in rng.sample(d["builders"], 2):   # which step comes next?
        st = b["steps"]
        k = rng.randrange(len(st) - 1)
        others = [x["steps"][min(k + 1, len(x["steps"]) - 1)]["text"] for x in d["builders"] if x is not b]
        opts, a = mcq(rng, st[k + 1]["text"], others)
        qs.append(dict(q=f"“{st[k]['text']}” — এর পরের ধাপ কোনটা?", o=opts, a=a, why=f'{st[k + 1]["text"]} = {st[k + 1]["bn"]}'))
    return qs


def build(course_key, n):
    c = COURSES[KEY]
    meta = c["chapters"][n - 1]
    d = load(n)
    steps = sum(len(b["steps"]) for b in d["builders"])
    S = [cover(f"Sentence Builder · অধ্যায় {bn(n)} · {meta['level']}", esc(meta["title_bn"]), esc(d["intro_bn"]),
               [f"🧱 ১০টি বাক্য, ধাপে ধাপে বড় করা ({bn(steps)} ধাপ)", "🟩 প্রতি ধাপে নতুন অংশটা সবুজ", "🔊 ট্যাপ করলে শুনবে আর বাংলা দেখবে",
                f"📝 ১০ প্রশ্নের কুইজ"], extra=f'<p class="sub-title"><span>{esc(d["title"])}</span></p>'),
         section("🧱", "বাক্য বানাও", esc(d["title"]), "প্রতি ধাপে সবুজ অংশটা নতুন · ধাপে ট্যাপ করলে শুনবে আর বাংলা দেখবে · আগে নিজে জোরে বলো")]
    S += [builder_slide(i, b) for i, b in enumerate(d["builders"], 1)]
    S.append(slide(f'<span class="chip">💡 টিপস</span><div class="callout">{esc(d["tip_bn"])}</div>'
                   '<div class="callout warn">🎯 আজকের কাজ: যেকোনো একটা ছোট বাক্য নিয়ে নিজে তিন ধাপে বড় করে বলো।</div>', "", "টিপস"))
    S.append(quiz_slide(quiz_for(n, d)))
    chs = c["chapters"]
    chips = [esc(b["steps"][0]["text"]) for b in d["builders"][:6]]
    if n < len(chs) and ready(n + 1):
        S.append(finish_slide(f"অধ্যায় {bn(n)} শেষ!", "আজকের বড় বাক্যগুলো থেকে দুটো মুখস্থ করে দিনে কয়েকবার বলো।", chips,
                              f"../ch-{n + 1:02d}/index.html", f"অধ্যায় {bn(n + 1)}: {esc(chs[n]['title_bn'])}"))
    elif n < len(chs):
        S.append(finish_slide(f"অধ্যায় {bn(n)} শেষ!", "পরের অধ্যায় শীঘ্রই আসছে — ততদিন আজকের বাক্যগুলো আবার বলো।", chips))
    else:
        S.append(finish_slide("Sentence Builder সম্পূর্ণ! 🏆", "A1 থেকে C2 — ছোট বাক্য থেকে পেশাদার লম্বা বাক্য পর্যন্ত। দারুণ কাজ!", chips))
    deck_page(f"{KEY}/ch-{n:02d}/index.html", f"অধ্যায় {n} · {meta['title_bn']} — Sentence Builder", f"{KEY}/ch-{n:02d}", "en", S,
              f"অধ্যায় {bn(n)} · {meta['level']} · {meta['title_bn']}", has_bn=True, has_pr=True)

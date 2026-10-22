"""Checks for generated chapter content. check_chapter() returns a list of problems (empty = fine).
python3 validate.py   checks every content/*/ch-NN.json and exits non-zero on problems."""
import json
import re
import sys
from pathlib import Path

from curriculum import COURSES
import letters_ja

ROOT = Path(__file__).resolve().parent
BN = re.compile(r"[ঀ-৿]")
FORBIDDEN = re.compile(r"\b(beer|wine|alcohol|whisk(?:e)?y|vodka|pork|bacon|ham|beef|steak|sausage|bier|wein|schwein\w*|rind\w*|"
                       r"wurst|bratwurst|sekt|schnaps)\b|ビール|ワイン|ぶたにく|ぎゅうにく|ポーク|ビーフ|ハム|(?<![\u0980-\u09FF])(?:মদ|শূকর|বিয়ার|ওয়াইন)(?![\u0980-\u09FF])|গরুর মাংস",
                       re.I)

# the course talks to the learner as তুমি; formal verb forms in the teacher's own voice are flagged
FORMAL = re.compile(r"আপনি|আপনার|করুন|বলুন|রাখুন|বসান|দেখুন|পারবেন|ভুলবেন|শিখবেন|নিন\b|লিখুন|পড়ুন|শুনুন")
# religion-specific practices: the learner may be Muslim or Hindu; festivals (Eid, Puja) are fine, rituals are not
RELIGION = re.compile(r"নামাজ|সালাম|প্রার্থনা|মসজিদ|মন্দির|\b(?:pray(?:er|ers|ing)?|mosque|temple|church)\b|Moschee|Kirche|おてら|じんじゃ", re.I)

COUNTS = {"A1": (8, 8), "A2": (8, 8), "B1": (9, 9), "B2": (9, 9)}


def _texts(d):
    yield from ((f"reading[{i}]", x) for i, x in enumerate(d["reading"]))
    yield from ((f"words[{i}]", x) for i, x in enumerate(d["words"]))
    yield from ((f"phrases[{i}]", x) for i, x in enumerate(d["phrases"]))
    yield from ((f"grammar.examples[{i}]", x) for i, x in enumerate(d["grammar"]["examples"]))


def check_chapter(course_key, n, d):
    c = COURSES[course_key]
    lang, level = c["lang"], c["level"]
    p = []
    lo, hi = COUNTS[level]
    if not lo <= len(d["reading"]) <= hi + 1:
        p.append(f"reading has {len(d['reading'])} lines, want {lo}")
    if len(d["words"]) != 10:
        p.append(f"words has {len(d['words'])}, want 10")
    if len(d["phrases"]) != 12:
        p.append(f"phrases has {len(d['phrases'])}, want 12")
    g = d["grammar"]
    if not 3 <= len(g["points_bn"]) <= 5:
        p.append(f"grammar.points_bn has {len(g['points_bn'])}")
    if len(g["examples"]) < 3:
        p.append("grammar.examples < 3")
    if len(g["quiz"]) != 3:
        p.append(f"grammar.quiz has {len(g['quiz'])}, want 3")
    for i, q in enumerate(g["quiz"]):
        if len(q["options"]) != 4 or len(set(q["options"])) != 4:
            p.append(f"grammar.quiz[{i}] needs 4 different options")
        if not 0 <= q["answer"] < len(q["options"]):
            p.append(f"grammar.quiz[{i}] answer out of range")
        if not BN.search(q["why_bn"]):
            p.append(f"grammar.quiz[{i}].why_bn is not Bangla")
    for f in ("intro_bn", "tip_bn"):
        if not BN.search(d[f]):
            p.append(f"{f} is not Bangla")
    if not BN.search(g["title_bn"]):
        p.append("grammar.title_bn is not Bangla")
    teacher = [d["intro_bn"], d["tip_bn"], g["title_bn"]] + g["points_bn"] + [q["why_bn"] for q in g["quiz"]]
    for t in teacher:
        m = FORMAL.search(t)
        if m:
            p.append(f"formal Bangla ({m.group(0)}) in teacher text: {t[:50]}")
    for pt in g["points_bn"]:
        if re.search(r"<(?!/?b>)", pt):
            p.append(f"points_bn has HTML other than <b>: {pt[:40]}")
    need_pron = lang != "english" or level == "A2"
    seen = set()
    for where, x in _texts(d):
        t = x["text"]
        if not t.strip():
            p.append(f"{where}.text empty")
        if not BN.search(x["bn"]):
            p.append(f"{where}.bn is not Bangla: {x['bn'][:40]}")
        if BN.search(t):
            p.append(f"{where}.text contains Bangla: {t[:40]}")
        if (need_pron or where.startswith("words")) and lang != "japanese" and not BN.search(x["pron_bn"]):
            p.append(f"{where}.pron_bn missing")
        if lang == "japanese":
            parts = [t] + ([x["example"]] if "example" in x else [])
            for s in parts:
                if not letters_ja.is_kana_text(s):
                    bad = sorted({ch for ch in s if not letters_ja.is_kana_text(ch)})
                    p.append(f"{where}: non-kana characters {''.join(bad)} in {s}")
                else:
                    try:
                        letters_ja.romaji(s)
                    except ValueError as e:
                        p.append(f"{where}: {e}")
        if where.startswith("words"):
            if t.lower() in seen:
                p.append(f"duplicate word {t}")
            seen.add(t.lower())
            if not x["example"].strip() or not BN.search(x["example_bn"]):
                p.append(f"{where} example missing")
    # muse sometimes leaks a Chinese/Korean word into Bangla text; Japanese chapters may use kana in explanations
    foreign = re.compile(r"[\u4e00-\u9fff\uac00-\ud7af]" if lang == "japanese" else r"[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7af]")

    def strings(o, path=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from strings(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                yield from strings(v, f"{path}.{i}")
        elif isinstance(o, str):
            yield path, o
    for path, sv in strings(d):
        if foreign.search(sv):
            p.append(f"foreign script in {path}: {sv[:50]}")
    blob = json.dumps(d, ensure_ascii=False)
    for w in sorted({m.group(0) for m in RELIGION.finditer(blob)}):
        p.append(f"religion-specific word, please review: {w}")
    for w in sorted({m.group(0) for m in FORBIDDEN.finditer(blob)}):
        p.append(f"culturally unsuitable word: {w}")
    return p


def main():
    bad = 0
    for k, c in COURSES.items():
        for n, ch in enumerate(c["chapters"], 1):
            if ch["kind"] != "topic":
                continue
            f = ROOT / "content" / k.replace("/", "-") / f"ch-{n:02d}.json"
            if not f.exists():
                print(f"MISSING {f.relative_to(ROOT)}")
                bad += 1
                continue
            probs = check_chapter(k, n, json.loads(f.read_text(encoding="utf-8")))
            for x in probs:
                print(f"{f.relative_to(ROOT)}: {x}")
            bad += bool(probs)
    print("ok" if not bad else f"{bad} chapter(s) with problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

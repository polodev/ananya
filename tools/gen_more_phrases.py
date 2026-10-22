"""Grow every topic chapter's "phrases" list to 40 with muse (keeps the reviewed ones first).
python3 tools/gen_more_phrases.py [course ...] [--only N,N] [-j 5]"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from curriculum import COURSES  # noqa: E402
from validate import check_chapter, PHRASES  # noqa: E402
from gen_content import LANG_RULES, LEVEL_NOTES  # noqa: E402
from de_pron import PROMPT as DE_RULES  # noqa: E402

SCHEMA = ROOT / "tools" / "phrases.schema.json"
MODEL = "muse-spark-1.3"

PROMPT = """You are adding useful sentences to one chapter of a mobile language course for an adult Bangladeshi learner
(native language Bangla). Answer with the JSON object only. Do not use any tools.

Course: {title} (level {level}). Chapter topic: {topic}. Grammar focus: {grammar}.
{lang_rules}
{extra_rules}
Level: {level_note}

Write exactly {need} NEW sentences the learner will really say or hear in this situation. Mix questions, answers,
polite requests and short statements; use the chapter's grammar often. They must not repeat these existing ones:
{existing}

Rules: natural modern language; "bn" = natural Bangla meaning (standard চলিত Bangla, never word-by-word);
culturally safe for Bangladeshi Muslims and Hindus (no alcohol, pork, beef, dating, religious rituals);
names only Rafi, Mitu, Tanvir, Nadia{names}.
"""


def run(course_key, n):
    c = COURSES[course_key]
    lang = c["lang"]
    f = ROOT / "content" / course_key.replace("/", "-") / f"ch-{n:02d}.json"
    d = json.loads(f.read_text(encoding="utf-8"))
    have = d["phrases"][:12]
    need = PHRASES - len(have)
    pron_rule = ("Give pron_bn for every sentence." if c["level"] in ("A1", "A2") else 'Set pron_bn to "" for every sentence.')
    extra = ""
    if lang == "german":
        extra = DE_RULES.split("Reference spellings")[0].split("Follow these spelling rules exactly")[1]
        extra = "pron_bn spelling rules:" + extra
    if lang == "japanese":
        pron_rule = 'Set pron_bn to "" (it is computed from the kana).'
    names = {"japanese": ", たなか, やまだ (Bangladeshi names in katakana: ラフィ, ミトゥ)", "german": ", Anna, Lukas, Frau Weber", "english": ""}[lang]
    prompt = PROMPT.format(title=c["title"], level=c["level"], topic=c["chapters"][n - 1]["topic"], grammar=c["chapters"][n - 1]["grammar"],
                           lang_rules=LANG_RULES[lang].format(pron_rule=pron_rule), extra_rules=extra, level_note=LEVEL_NOTES[c["level"]],
                           need=need, existing="\n".join(x["text"] for x in have), names=names)
    last = ""
    for _ in range(3):
        with tempfile.TemporaryDirectory() as tmp:
            pf = Path(tmp) / "p.txt"
            pf.write_text(prompt, encoding="utf-8")
            r = subprocess.run(["muse", "exec", "--model", MODEL, "--reasoning-effort", "max", "--output-schema", str(SCHEMA),
                                "--prompt-file", str(pf), "--workspace", tmp], cwd=tmp, capture_output=True, text=True, timeout=1800)
        out = r.stdout.strip()
        try:
            items = json.loads(out[out.find("{"):out.rfind("}") + 1])["items"]
        except ValueError:
            last = "bad json"
            continue
        seen = {x["text"].strip().lower() for x in have}
        new = []
        for x in items:
            k = x["text"].strip().lower()
            if k and k not in seen:
                seen.add(k)
                new.append({"text": x["text"].strip(), "pron_bn": re.sub(r"\.(?=\s|$)", "।", x["pron_bn"].strip()), "bn": x["bn"].strip()})
        trial = dict(d, phrases=have + new[:need])
        probs = check_chapter(course_key, n, trial)
        if len(new) >= need and not probs:
            f.write_text(json.dumps(trial, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            return f"ok   {course_key} {n}"
        last = f"{len(new)} new; " + "; ".join(probs[:4])
        prompt += f"\n\nThe previous answer had problems, fix them: {last}"
    return f"FAIL {course_key} {n}: {last}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*", default=[k for k in COURSES if COURSES[k]["chapters"][-1]["kind"] == "topic"])
    ap.add_argument("--only", default="")
    ap.add_argument("-j", type=int, default=5)
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x}
    jobs = [(k, n) for k in a.courses for n, ch in enumerate(COURSES[k]["chapters"], 1) if ch["kind"] == "topic" and (not only or n in only)]
    with ThreadPoolExecutor(a.j) as ex:
        for msg in ex.map(lambda j: run(*j), jobs):
            print(msg, flush=True)


if __name__ == "__main__":
    main()

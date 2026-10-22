"""Generate topic-chapter content with the muse CLI.   python3 tools/gen_content.py [course ...] [--only N,N] [--force] [-j 6]

One muse run per chapter. The prompt is built from curriculum.py, the answer is shaped by tools/chapter.schema.json,
then checked by validate.check_chapter(). Output: content/<course>/ch-NN.json (skipped if it exists, unless --force).
Failed chapters are written to content/<course>/ch-NN.error.txt so they can be fixed by hand."""
import argparse
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from curriculum import COURSES, LANGS  # noqa: E402
from validate import check_chapter  # noqa: E402

SCHEMA = ROOT / "tools" / "chapter.schema.json"

LEVEL_NOTES = {
    "A1": "CEFR A1: very short, very common words; present tense mostly; sentences of 3-8 words.",
    "A2": "CEFR A2: common everyday words; short sentences of 5-12 words.",
    "B1": "CEFR B1: everyday and work vocabulary; sentences of 8-18 words; some linking words.",
    "B2": "CEFR B2: richer vocabulary, abstract topics, idiomatic but natural; sentences of 10-25 words.",
}

LANG_RULES = {
    "english": """Target language: English (natural, modern, international English).
- "text" fields are English. "pron_bn" is the English pronunciation written in Bangla script, the way a Bangladeshi
  teacher writes it (examples: "Thank you" -> "থ্যাংক ইউ", "Would you like some tea?" -> "উড ইউ লাইক সাম টি?",
  "comfortable" -> "কামফর্টেবল").
- {pron_rule}""",
    "japanese": """Target language: Japanese, polite です/ます style.
- Write Japanese ONLY in hiragana and katakana. NO kanji at all. Loanwords and foreign names in katakana.
- Put ONE SPACE between words, and particles are separate words: "わたし は ラフィ です。", "えき へ いきます。",
  "これ は なん です か。". Use only the punctuation 。 、 ？ ！.
- "pron_bn": Bangla-script pronunciation (e.g. "ওয়াতাশি ওয়া রাফি দেস"). "romaji" field is not needed.""",
    "german": """Target language: German (standard Hochdeutsch, du-form for friends, Sie-form for strangers and shops).
- "text" fields are German with correct capitalisation and umlauts (ä ö ü ß).
- "pron_bn": German pronunciation in Bangla script, e.g. "Ich heiße Rafi." -> "ইশ হাইসে রাফি।",
  "Wie geht es Ihnen?" -> "ভি গেইট এস ইনেন?", "Guten Morgen" -> "গুটেন মরগেন", "Entschuldigung" -> "এন্টশুলডিগুং".""",
}

PROMPT = """You are writing one chapter of a mobile language course for an adult Bangladeshi learner whose native
language is Bangla. All explanations are in Bangla (standard, natural চলিত Bangla, warm and simple, as a good
Bangladeshi teacher would speak; never word-by-word machine translation). Answer with the JSON object only.
Do not use any tools, do not read or write files.

Course: {title} (level {level}). Chapter {n} of {total}: "{title_bn}".
Topic: {topic}
Grammar focus: {grammar}
Earlier chapters covered: {earlier}

{lang_rules}

Level: {level_note}

Content rules:
- Setting: everyday life of a young adult in Bangladesh (Dhaka, Chandpur, Chittagong, Sylhet) or, for Japanese/German,
  a Bangladeshi learner (name: Rafi) talking with local people. Use these names: Rafi, Mitu, Tanvir, Nadia{local_names}.
- Culturally safe for Bangladeshi Muslims and Hindus: NO alcohol (no beer, wine, sake), NO pork, NO beef, no dating
  or romance, no gambling, no religious practices (prayer, mosque, temple, salam); festivals like Eid or Puja are fine.
- In your own Bangla (intro_bn, tip_bn, grammar points, why_bn) address the learner informally as তুমি
  (করো, বলো, শেখো) — never আপনি. Food examples: rice, fish, chicken, vegetables, fruit, tea, coffee, juice, water, bread.
- "reading": {reading_rule} Every line must use this chapter's grammar or words.
- "words": exactly 10 NEW useful words or short expressions for this topic (not trivial ones like "I" or "is"),
  each with an example sentence that uses it.
- "phrases": exactly 12 useful, natural sentences the learner will really say or hear in this situation.
- "grammar": explain the grammar focus in Bangla for a beginner in this level: 3-5 short "points_bn" (HTML <b> allowed
  for key words, nothing else), 4 "examples", and 3 multiple-choice "quiz" questions with exactly 4 options, one correct
  (answer = 0-based index; vary the position of the correct answer), and "why_bn" explaining the answer in Bangla.
- "tip_bn": one practical learning or culture tip in Bangla (2-3 sentences).
- "intro_bn": 1-2 Bangla sentences that tell the learner what they will be able to do after this chapter.
- "title": the chapter title in the target language (short).
- Every "bn" field is the natural Bangla meaning of the line.
"""

READING_RULE = {
    "A1": "a short dialogue of exactly 8 lines between Rafi and one other person (speaker = first name).",
    "A2": "a short dialogue of exactly 8 lines between two people (speaker = first name).",
    "B1": "a dialogue or short email/story of exactly 9 lines (speaker = first name for dialogue, empty string for a text).",
    "B2": "a short article, blog post or discussion of exactly 9 lines/sentences (speaker empty for an article, first name for a discussion).",
}

LOCAL_NAMES = {"japanese": ", and Japanese people: Tanaka, Yamada, Sato (katakana names for Bangladeshis: ラフィ, ミトゥ)",
               "german": ", and German people: Anna, Lukas, Frau Weber, Herr Müller", "english": ""}


def build_prompt(course_key, n):
    c = COURSES[course_key]
    lang = c["lang"]
    chs = c["chapters"]
    d = chs[n - 1]
    earlier = "; ".join(f'{x["topic"]} ({x["grammar"]})' for x in chs[:n - 1] if x["kind"] == "topic") or "letters and numbers only"
    pron_rule = ("Give pron_bn for every word, phrase, reading line and example."
                 if c["level"] == "A2" else
                 'Give pron_bn ONLY for "words" (the word itself). For reading lines, phrases and grammar examples set pron_bn to "".')
    return PROMPT.format(title=c["title"], level=c["level"], n=n, total=len(chs), title_bn=d["title_bn"], topic=d["topic"],
                         grammar=d["grammar"], earlier=earlier, lang_rules=LANG_RULES[lang].format(pron_rule=pron_rule),
                         level_note=LEVEL_NOTES[c["level"]], reading_rule=READING_RULE[c["level"]], local_names=LOCAL_NAMES[lang])


def run_one(course_key, n, force=False, effort="high"):
    out = ROOT / "content" / course_key.replace("/", "-") / f"ch-{n:02d}.json"
    err = out.with_suffix(".error.txt")
    if out.exists() and not force:
        return f"skip {course_key} {n}"
    out.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(course_key, n)
    last = ""
    for attempt in range(2):
        with tempfile.TemporaryDirectory() as tmp:
            pf = Path(tmp) / "prompt.txt"
            pf.write_text(prompt, encoding="utf-8")
            try:
                r = subprocess.run(["muse", "exec", "--output-schema", str(SCHEMA), "--prompt-file", str(pf),
                                    "--reasoning-effort", effort, "--workspace", tmp],
                                   cwd=tmp, capture_output=True, text=True, timeout=900)
            except subprocess.TimeoutExpired:
                last = "timeout"
                continue
        text = r.stdout.strip()
        start, end = text.find("{"), text.rfind("}")
        try:
            data = json.loads(text[start:end + 1])
        except ValueError as e:
            last = f"bad json: {e}\n---stdout---\n{text[-3000:]}\n---stderr---\n{r.stderr[-2000:]}"
            continue
        problems = check_chapter(course_key, n, data)
        if problems and attempt == 0:
            last = "\n".join(problems)
            prompt += "\n\nA previous attempt had these problems, avoid them:\n" + last
            continue
        out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        if problems:
            err.write_text("\n".join(problems), encoding="utf-8")
            return f"WARN {course_key} {n}: {len(problems)} problems (kept, see {err.name})"
        err.unlink(missing_ok=True)
        return f"ok   {course_key} {n}"
    err.write_text(last, encoding="utf-8")
    return f"FAIL {course_key} {n}: {last.splitlines()[0] if last else '?'}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("courses", nargs="*", default=list(COURSES))
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("-j", type=int, default=6)
    ap.add_argument("--effort", default="high")
    ap.add_argument("--print-prompt", action="store_true")
    a = ap.parse_args()
    only = {int(x) for x in a.only.split(",") if x}
    jobs = [(k, n) for k in a.courses for n, d in enumerate(COURSES[k]["chapters"], 1)
            if d["kind"] == "topic" and (not only or n in only)]
    if a.print_prompt:
        print(build_prompt(*jobs[0]))
        return
    with ThreadPoolExecutor(a.j) as ex:
        for msg in ex.map(lambda j: run_one(*j, force=a.force, effort=a.effort), jobs):
            print(msg, flush=True)


if __name__ == "__main__":
    main()

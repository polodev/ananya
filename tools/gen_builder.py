"""Generate Sentence Builder chapters with muse.   python3 tools/gen_builder.py [--only N,N] [--force] [-j 5]
Output: content/english-builder/ch-NN.json = {title, intro_bn, tip_bn, builders: [{note_bn, steps: [{text, pron_bn, bn}]}]}"""
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
from validate import check_builder  # noqa: E402
from learner import CONTENT_CONTEXT  # noqa: E402

KEY = "english/builder"
SCHEMA = ROOT / "tools" / "builder.schema.json"
MODEL = "muse-spark-1.3"

PROMPT = """You are writing one chapter of a "Sentence Builder" course for an adult Bangladeshi learner of English
(native language Bangla). Answer with the JSON object only. Do not use any tools.

Chapter {n} of 20, CEFR level {level}. Focus: {focus}.

{learner_context}

A builder starts from a short, simple core sentence and grows it in steps. Every step repeats the previous sentence
and ADDS one new chunk (a word, a phrase or a clause) that practises the focus; change an existing word only when the
grammar requires it (e.g. like tea -> like drinking tea). Example builder:
  1. I like tea.
  2. I like tea with milk.
  3. I like drinking tea with milk every morning.

Write exactly 10 builders. Each builder has 3 to 5 steps (use 4-5 at B2 and above). The final sentence must sound
natural and match level {level}{level_note}. Vary the core sentences (people, work, family, travel, study, health,
shopping, weather, technology, city and village life in Bangladesh). Names: Ananya, Adyo, Rafi, Mitu, Tanvir, Nadia.
Culturally safe for Bangladeshi Muslims and Hindus: no alcohol, pork, beef, dating, gambling or religious rituals.

For every step: "text" (English), "bn" (natural Bangla meaning in standard চলিত Bangla, not word-by-word),
"pron_bn" ({pron_rule}).
For every builder: "note_bn" = one short Bangla sentence saying what the steps added (address the learner as তুমি).
Chapter: "title" (short English title), "intro_bn" (1-2 Bangla sentences, তুমি), "tip_bn" (2 Bangla sentences, তুমি).
"""

LEVEL_NOTE = {"A1": " (very short and simple)", "A2": " (simple, everyday)", "B1": "", "B2": " (rich but natural)",
              "C1": " (sophisticated, still natural)", "C2": " (precise, near-native, formal where fitting)"}


def run(n, force=False):
    out_f = ROOT / "content" / "english-builder" / f"ch-{n:02d}.json"
    if out_f.exists() and not force:
        return f"skip {n}"
    out_f.parent.mkdir(parents=True, exist_ok=True)
    meta = COURSES[KEY]["chapters"][n - 1]
    pron_rule = ("English pronunciation in Bangla script, e.g. 'I like tea.' -> 'আই লাইক টি।'" if n <= 10 else 'set to ""')
    prompt = PROMPT.format(n=n, level=meta["level"], focus=meta["topic"], level_note=LEVEL_NOTE[meta["level"]], pron_rule=pron_rule,
                           learner_context=CONTENT_CONTEXT)
    last = ""
    for _ in range(3):
        with tempfile.TemporaryDirectory() as tmp:
            pf = Path(tmp) / "p.txt"
            pf.write_text(prompt, encoding="utf-8")
            r = subprocess.run(["muse", "exec", "--model", MODEL, "--reasoning-effort", "max", "--output-schema", str(SCHEMA),
                                "--prompt-file", str(pf), "--workspace", tmp], cwd=tmp, capture_output=True, text=True, timeout=1800)
        out = r.stdout.strip()
        try:
            d = json.loads(out[out.find("{"):out.rfind("}") + 1])
        except ValueError:
            last = "bad json"
            continue
        for b in d["builders"]:
            for st in b["steps"]:
                st["pron_bn"] = re.sub(r"\.(?=\s|$)", "।", st["pron_bn"].strip())
        probs = check_builder(n, d)
        if not probs:
            out_f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            return f"ok   {n}"
        last = "; ".join(probs[:5])
        prompt += f"\n\nThe previous answer had problems, fix them: {last}"
    return f"FAIL {n}: {last}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("-j", type=int, default=5)
    a = ap.parse_args()
    nums = [int(x) for x in a.only.split(",") if x] or list(range(1, 21))
    with ThreadPoolExecutor(a.j) as ex:
        for msg in ex.map(lambda n: run(n, a.force), nums):
            print(msg, flush=True)

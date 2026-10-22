"""Rewrite the Bangla pronunciation of every German line so it follows the rules taught in German A1 chapter 2
(letters_de.RULES).   python3 tools/de_pron.py [N ...]

One muse run per chapter; the answer (tools/pron.schema.json) maps each German string to its Bangla spelling,
which replaces pron_bn in content/german-a1/ch-NN.json."""
import json
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import letters_de as DE  # noqa: E402

SCHEMA = ROOT / "tools" / "pron.schema.json"
EXAMPLES = [(w, p) for _, _, _, ex in DE.RULES for w, p, _ in ex] + [(x[0], x[1]) for x in DE.NUM_USE + DE.SPELL[:3]]

PROMPT = """Write the pronunciation of each German sentence in Bangla script, for a Bangladeshi beginner.
Answer with the JSON object only. Do not use any tools.

Follow these spelling rules exactly (they are taught in the course, the learner will compare):
- d = ড, t = ট (Dank = ডাংক, Tag = টাক); final b d g sound p t k: halb = হাল্প, Kind = কিন্ট, Tag = টাক
- w = ভ (Wasser = ভাসা, wie = ভি); v = ফ (Vater = ফাটা, viel = ফিল)
- z and tz = ৎস (zehn = ৎসেন, zwanzig = ৎসভানৎসিশ, jetzt = ইয়েৎস্ট)
- s before a vowel = জ (Sonne = জনে, sie = জি, sieben = জিবেন); ss and ß = স
- sch = শ; sp / st at the start of a word part = শ্প / শ্ট (sprechen = শ্প্রেশেন, Stadt = শ্টাট)
- ch after a o u au = খ (Buch = বুখ, acht = আখ্ট, auch = আউখ); otherwise ch = শ (ich = ইশ, Milch = মিলশ, sprechen = শ্প্রেশেন)
- final -ig = ইশ (zwanzig, ledig = লেডিশ)
- ei = আই, ie = ঈ / ই, eu and äu = অয় (neu = নয়, heute = হয়টে, Deutsch = ডয়চ)
- final -er and -r after a long vowel sound like আ / য়া: Bruder = ব্রুডা, Vater = ফাটা, Lehrer = লেরা, mir = মিয়া, vier = ফিয়া, Uhr = উয়া
- h after a vowel is silent (gehen = গেয়েন, sehr = জেয়া)
- ä = এ, ö = ও্যে-like (schön = শ্যোন), ü = ্যু (fünf = ফ্যুনফ, Tür = ট্যুয়া)
- j = ইয় (ja = ইয়া), qu = ক্ভ, pf = প্ফ
- keep punctuation; a full stop becomes ।

Reference spellings from the course (match this style):
{examples}

Sentences (return one item per sentence, "text" copied exactly):
{items}
"""


def strings(d):
    seen = []
    for x in d["reading"] + d["words"] + d["phrases"] + d["grammar"]["examples"]:
        if x["text"] not in seen:
            seen.append(x["text"])
    return seen


def run(n):
    f = ROOT / "content" / "german-a1" / f"ch-{n:02d}.json"
    d = json.loads(f.read_text(encoding="utf-8"))
    items = strings(d)
    prompt = PROMPT.format(examples="\n".join(f"{w} = {p}" for w, p in EXAMPLES), items="\n".join(items))
    with tempfile.TemporaryDirectory() as tmp:
        pf = Path(tmp) / "prompt.txt"
        pf.write_text(prompt, encoding="utf-8")
        r = subprocess.run(["muse", "exec", "--output-schema", str(SCHEMA), "--prompt-file", str(pf), "--reasoning-effort", "high",
                            "--workspace", tmp], cwd=tmp, capture_output=True, text=True, timeout=900)
    out = r.stdout.strip()
    got = {x["text"]: x["pron_bn"] for x in json.loads(out[out.find("{"):out.rfind("}") + 1])["items"]}
    missing = [t for t in items if t not in got]
    for x in d["reading"] + d["words"] + d["phrases"] + d["grammar"]["examples"]:
        if x["text"] in got:
            x["pron_bn"] = got[x["text"]]
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return f"ch {n}: {len(got)} updated" + (f", missing {missing}" if missing else "")


if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] or list(range(4, 16))
    with ThreadPoolExecutor(6) as ex:
        for msg in ex.map(run, nums):
            print(msg, flush=True)

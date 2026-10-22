"""Print chapters compactly for review.   python3 tools/dump.py english-a2 [N ...]"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import letters_ja  # noqa: E402

JA = False


def pr(x, key="pron_bn"):
    """Japanese: show the romaji the site computes instead of muse's own pronunciation."""
    return letters_ja.romaji(x["text"]) if JA else x[key]


def dump(f):
    d = json.loads(f.read_text(encoding="utf-8"))
    print(f"=== {f.parent.name}/{f.name}: {d['title']}\nI  {d['intro_bn']}")
    for i, x in enumerate(d["reading"], 1):
        print(f"R{i} [{x['speaker']}] {x['text']} | {pr(x)} | {x['bn']}")
    for i, x in enumerate(d["words"], 1):
        print(f"W{i} {x['text']} | {pr(x)} | {x['bn']} || {x['example']} | {x['example_bn']}")
    for i, x in enumerate(d["phrases"], 1):
        print(f"P{i} {x['text']} | {pr(x)} | {x['bn']}")
    g = d["grammar"]
    print(f"G  {g['title_bn']}")
    for p in g["points_bn"]:
        print(f"GP {p}")
    for i, x in enumerate(g["examples"], 1):
        print(f"E{i} {x['text']} | {pr(x)} | {x['bn']}")
    for i, q in enumerate(g["quiz"], 1):
        print(f"Q{i} {q['q']} {q['options']} -> {q['options'][q['answer']]} | {q['why_bn']}")
    print(f"T  {d['tip_bn']}\n")


if __name__ == "__main__":
    folder = ROOT / "content" / sys.argv[1]
    JA = sys.argv[1].startswith("japanese")
    nums = [int(x) for x in sys.argv[2:]]
    for f in sorted(folder.glob("ch-*.json")):
        if not nums or int(f.stem[3:]) in nums:
            dump(f)

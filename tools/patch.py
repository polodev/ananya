"""Apply review fixes to generated chapters.   python3 tools/patch.py english-a2 < fixes.txt

Each line: <chapter> <path> = <value>     e.g.   3 words.4.text = visit
path uses dots and 0-based list indexes; 'answer' values are stored as int. Lines starting with # are ignored.
A path ending in '+' appends to a list, '-' deletes that index."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    folder = ROOT / "content" / sys.argv[1]
    cache = {}
    for raw in sys.stdin.read().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        left, _, value = line.partition(" = ")
        ch, path = left.split(" ", 1)
        f = folder / f"ch-{int(ch):02d}.json"
        d = cache.setdefault(f, json.loads(f.read_text(encoding="utf-8")))
        keys = path.strip().split(".")
        obj = d
        for k in keys[:-1]:
            obj = obj[int(k)] if isinstance(obj, list) else obj[k]
        last = keys[-1]
        val = int(value) if last == "answer" else value
        if last == "+":
            obj.append(json.loads(value))
        elif last.endswith("-"):
            del obj[int(last[:-1])]
        elif isinstance(obj, list):
            obj[int(last)] = val
        else:
            if last not in obj:
                raise SystemExit(f"unknown key {last} in {line}")
            obj[last] = val
    for f, d in cache.items():
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("patched", f.relative_to(ROOT))


if __name__ == "__main__":
    main()

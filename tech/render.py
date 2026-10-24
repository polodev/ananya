"""HTML for the technology slides. One idea per slide, big type, no vertical scrolling."""
import html
import re

from engine import esc, slide

_BOLD = re.compile(r"\*\*(.+?)\*\*")
_CODE = re.compile(r"`([^`]+)`")


def rich(text):
    """escape everything, then allow **bold** and `code` from the content files."""
    s = esc(text or "")
    s = _BOLD.sub(r"<b>\1</b>", s)
    s = _CODE.sub(r"<code>\1</code>", s)
    return s.replace("\n", "<br>")


def _kicker(s):
    return f'<span class="t-kicker">{rich(s)}</span>' if s else ""


def _note(s):
    return f'<p class="t-note">{rich(s)}</p>' if s else ""


def _pair(x):
    """(a, b) or {'a':..., 'b':...} -> (a, b)."""
    if isinstance(x, dict):
        return x.get("title", ""), x.get("items", [])
    return x[0], x[1]


def _term(x):
    if isinstance(x, dict):
        return x.get("term", ""), x.get("bn", ""), x.get("detail", "")
    return x[0], x[1], (x[2] if len(x) > 2 else "")


def _step(x):
    if isinstance(x, dict):
        return x.get("title", ""), x.get("text", "")
    return x[0], (x[1] if len(x) > 1 else "")


def big(s):
    vis = f'<div class="t-visual" aria-hidden="true">{esc(s["visual"])}</div>' if s.get("visual") else ""
    return (f'{_kicker(s["kicker"])}{vis}<h1 class="t-h">{rich(s["title"])}</h1>'
            f'<p class="t-body">{rich(s["body"])}</p>{_note(s.get("note"))}')


def points(s):
    items = "".join(f'<div class="t-point"><span class="t-dot">→</span><div>{rich(x)}</div></div>' for x in s["items"])
    sub = f'<p class="t-sub">{rich(s["sub"])}</p>' if s.get("sub") else ""
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1>{sub}'
            f'<div class="t-points">{items}</div>{_note(s.get("note"))}')


def compare(s):
    lt, li = _pair(s["left"])
    rt, ri = _pair(s["right"])
    left = f'<div class="t-col"><h3>{rich(lt)}</h3><ul>' + "".join(f"<li>{rich(x)}</li>" for x in li) + "</ul></div>"
    right = f'<div class="t-col"><h3>{rich(rt)}</h3><ul>' + "".join(f"<li>{rich(x)}</li>" for x in ri) + "</ul></div>"
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1>'
            f'<div class="t-compare">{left}{right}</div>{_note(s.get("note"))}')


def flow(s):
    rows = []
    for i, x in enumerate(s["steps"], 1):
        t, body = _step(x)
        rows.append(f'<div class="t-step"><span class="t-num">{i}</span><div><b>{rich(t)}</b>'
                    + (f'<p>{rich(body)}</p>' if body else "") + "</div></div>")
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1>'
            f'<div class="t-flow">{"".join(rows)}</div>{_note(s.get("note"))}')


def terms(s):
    cards = []
    for x in s["items"]:
        term, bn, detail = _term(x)
        cards.append(f'<div class="t-card"><b class="t-term">{rich(term)}</b><span class="t-mean">{rich(bn)}</span>'
                     + (f'<small>{rich(detail)}</small>' if detail else "") + "</div>")
    sub = f'<p class="t-sub">{rich(s["sub"])}</p>' if s.get("sub") else ""
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1>{sub}'
            f'<div class="t-terms">{"".join(cards)}</div>{_note(s.get("note"))}')


def profile(s):
    facts = "".join(f'<div class="t-fact"><span>{rich(k)}</span><b>{rich(v)}</b></div>' for k, v in s["facts"])
    return (f'{_kicker(s["kicker"])}'
            f'<div class="t-profile"><div class="t-phead"><div class="t-mark">{esc(s["mark"])}</div>'
            f'<div><h2>{rich(s["name"])}</h2><p class="t-en">{rich(s["en"])}</p></div></div>'
            f'<div class="t-facts">{facts}</div>'
            f'<div class="t-famous"><span>কেন বিখ্যাত</span><p>{rich(s["famous"])}</p></div>'
            f'<div class="t-hook"><span>তোমার জন্য</span><p>{rich(s["hook"])}</p></div></div>'
            f'{_note(s.get("note"))}')


def timeline(s):
    rows = "".join(f'<div class="t-tl"><span class="yr">{rich(y)}</span><p>{rich(t)}</p></div>' for y, t in s["items"])
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1>'
            f'<div class="t-timeline">{rows}</div>{_note(s.get("note"))}')


def code(s):
    out = f'<div class="t-output"><span>output</span><code>{esc(s["output"])}</code></div>' if s.get("output") else ""
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1>'
            f'<div class="t-code" data-lang="{esc(s.get("lang", ""))}"><pre><code>{esc(s["code"])}</code></pre></div>'
            f'{out}{_note(s.get("note"))}')


def analogy(s):
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1>'
            f'<div class="t-analogy"><div class="t-ana"><span>চেনা জিনিস</span><b>{rich(s["left"])}</b></div>'
            f'<div class="t-arrow">→</div>'
            f'<div class="t-ana tech"><span>টেকের নাম</span><b>{rich(s["right"])}</b></div></div>'
            f'<p class="t-body">{rich(s["body"])}</p>{_note(s.get("note"))}')


def stat(s):
    return (f'{_kicker(s["kicker"])}<div class="t-stat"><div class="t-big">{rich(s["value"])}</div>'
            f'<p class="t-stat-label">{rich(s["label"])}</p></div>'
            f'<p class="t-body">{rich(s["body"])}</p>{_note(s.get("note"))}')


def quote(s):
    return (f'{_kicker(s["kicker"])}<blockquote class="t-quote">“{rich(s["text"])}”</blockquote>'
            f'<p class="t-who">— {rich(s["who"])}</p>{_note(s.get("note"))}')


def think(s):
    return (f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["question"])}</h1>'
            f'<details class="t-think"><summary>উত্তর দেখো 👀</summary><p>{rich(s["answer"])}</p></details>'
            f'{_note(s.get("note"))}')


def recap(s):
    items = "".join(f'<div class="t-check"><span>✓</span><div>{rich(x)}</div></div>' for x in s["items"])
    return f'{_kicker(s["kicker"])}<h1 class="t-h sm">{rich(s["title"])}</h1><div class="t-recap">{items}</div>{_note(s.get("note"))}'


RENDER = dict(big=big, points=points, compare=compare, flow=flow, terms=terms, profile=profile,
              timeline=timeline, code=code, analogy=analogy, stat=stat, quote=quote, think=think, recap=recap)


def render(s, deck_title=""):
    inner = RENDER[s["kind"]](s)
    cls = "t-slide" + (" t-big-slide" if s["kind"] == "big" else "")
    return slide(f'<div class="t-wrap">{inner}</div>', cls, deck_title or s.get("title", ""))

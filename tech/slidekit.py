"""A tiny content DSL for technology decks.

One call = one slide. A slide teaches one idea, with a big headline and a short body, so it fits a phone
without scrolling. Content strings may use **bold** and `code`; everything is escaped when rendered.
"""
import re


def chapter(title_bn, title_en, hook, slides, quiz=None, chips=None):
    return dict(title_bn=title_bn, title_en=title_en, hook=hook, slides=slides,
                quiz=quiz or [], chips=chips or [])


def big(kicker, title, body="", visual="", note=""):
    """the main teaching slide: one large statement, two or three sentences.

    Also accepts the shorter big("headline", "long body", "emoji") form used in some chapters.
    """
    if body and not visual and not re.search(r"[\w\u0980-\u09FF]", body):
        kicker, title, body, visual = "", kicker, title, body
    return dict(kind="big", kicker=kicker, title=title, body=body, visual=visual, note=note)


def points(title, sub, items, note=""):
    """3-4 short points; each point is one line or two."""
    return dict(kind="points", kicker="", title=title, sub=sub, items=items, note=note)


def compare(title, left, right, note=""):
    """left/right are (heading, [items]) pairs; used for high vs low, front vs back, etc."""
    return dict(kind="compare", kicker="", title=title, left=left, right=right, note=note)


def flow(title, steps, note=""):
    """3-5 numbered steps; a process the learner can follow with a finger."""
    return dict(kind="flow", kicker="", title=title, steps=steps, note=note)


def terms(title, sub, items, note=""):
    """3-4 vocabulary cards: (english term, Bangla meaning, one-line detail)."""
    return dict(kind="terms", kicker="", title=title, sub=sub, items=items, note=note)


def profile(kicker, name, en, mark, facts, famous, hook, note=""):
    """a company or person: 4 short facts, why it is famous, and why it matters to her."""
    return dict(kind="profile", kicker=kicker, name=name, en=en, mark=mark, facts=facts,
                famous=famous, hook=hook, note=note)


def timeline(title, items, note=""):
    """(year, what happened) pairs, oldest first; 4-6 items."""
    return dict(kind="timeline", kicker="", title=title, items=items, note=note)


def code(kicker, title, code, lang="js", output="", note=""):
    """a short code sample with an optional output line."""
    return dict(kind="code", kicker=kicker, title=title, code=code, lang=lang, output=output, note=note)


def analogy(title, left, right, body, note=""):
    """left = everyday thing, right = technical thing; the body explains the mapping."""
    return dict(kind="analogy", kicker="", title=title, left=left, right=right, body=body, note=note)


def stat(kicker, value, label, body="", note=""):
    """one large number that makes the point stick."""
    return dict(kind="stat", kicker=kicker, value=value, label=label, body=body, note=note)


def quote(kicker, text, who, note=""):
    return dict(kind="quote", kicker=kicker, text=text, who=who, note=note)


def think(kicker, question, answer, note=""):
    """a question slide with a tap-to-reveal answer; good as a chapter opener."""
    return dict(kind="think", kicker=kicker, question=question, answer=answer, note=note)


def recap(title, items, note=""):
    return dict(kind="recap", kicker="", title=title, items=items, note=note)

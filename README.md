# ভাষার ঘর — Language Corner

English, Japanese and German, taught in Bangla, built for reading on a phone.

| Course | Level | Chapters | What's inside |
|---|---|---|---|
| English | A2 | 12 | everyday conversations, present/past/future, should, comparatives, present perfect |
| English | B1 | 12 | interviews, emails, conditionals, passive, reported speech, relative clauses |
| English | B2 | 12 | debates, articles, mixed/third conditionals, causatives, cleft sentences, modal perfects |
| English | Sentence Builder A1–C2 | 20 | 10 builders per chapter: a short sentence grows in 3–5 steps, new words highlighted |
| Japanese | A1 | 19 | 7 chapters of hiragana, katakana and numbers, then 12 everyday topics (です/ます, particles, past, て-form) |
| German | A1 | 15 | 3 chapters of alphabet, sound rules and numbers, then 12 everyday topics (articles, accusative, modal verbs, Perfekt) |

Every topic chapter: a dialogue or short text, 10 words, 40 useful sentences, one grammar point, a tip and a 12-question quiz.
Slides are read only by swiping left and right: nothing scrolls, on a phone or a desktop.
Bangla pronunciation is shown for every line (can be hidden), and the phone's own text-to-speech reads everything aloud.

Live: https://polodev.github.io/ananya/

## How it works

Static HTML, no framework. `python3 build.py` regenerates every page from the course data.

```
curriculum.py                    courses and chapter outlines
content/<course>/ch-NN.json      topic and sentence-builder chapters (generated with muse, checked by validate.py)
letters_ja.py / letters_de.py    letters, sounds, numbers (hand-written) + Japanese romaji/Bangla converters
site_topic.py / site_letters.py / site_builder.py  turn chapters into slides
engine.py, assets/               HTML helpers, the only CSS and JS
validate.py, tools/              content checks, generation and review tools
```

Progress is stored in the browser (`localStorage`).

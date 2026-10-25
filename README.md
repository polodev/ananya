# অনন্যার শেখার ঘর — Ananya’s Learning Corner

English, Japanese, German and Technology, taught in Bangla, built for reading on a phone.

Personalized for **Ananya Debnath (অনন্যা দেবনাথ)**, 26, a mother studying for a master's degree in management.
Her son is **Siddharth Debnath Adyo (সিদ্ধার্থ দেবনাথ আদ্য)**. Her portrait, greetings and lesson examples run through
the site. `learner.py` holds the profile and spoken English introduction; lesson stories are practice scenarios.

The photo is framed with CSS, preserving the original for the enlarged view. Photo favicons and the 1200×630
WhatsApp/Open Graph sharing card are in `assets/img/`. To regenerate them after changing the photo or framing,
run `python3 tools/build_brand_assets.py` (requires Playwright with Chromium), then `python3 build.py`.

| Course | Level | Chapters | What's inside |
|---|---|---|---|
| English | A2 | 12 | everyday conversations, present/past/future, should, comparatives, present perfect |
| English | B1 | 12 | interviews, emails, conditionals, passive, reported speech, relative clauses |
| English | B2 | 12 | debates, articles, mixed/third conditionals, causatives, cleft sentences, modal perfects |
| English | Sentence Builder A1–C2 | 20 | 10 builders per chapter: a short sentence grows in 3–5 steps, new words highlighted |
| Japanese | A1 | 19 | 7 chapters of hiragana, katakana and numbers, then 12 everyday topics (です/ます, particles, past, て-form) |
| German | A1 | 15 | 3 chapters of alphabet, sound rules and numbers, then 12 everyday topics (articles, accusative, modal verbs, Perfekt) |

## Technology track

Ten courses, 72 chapters and 796 teaching slides, written in mixed Bangla–English for a complete beginner.
Each chapter is a swipe deck of big one-idea slides: no walls of text, no vertical scrolling.

| Course | Chapters | What's inside |
|---|---|---|
| Technology 101 | 10 | the computer, software, internet, web, data, programming, language families, databases, cloud, companies and people |
| Technology 201 | 8 | IP/DNS/TCP/HTTP, browsers, backend, databases and caches, containers, hosting, APIs, security |
| Technology 301 | 10 | JavaScript from zero: variables, conditions, loops, functions, arrays, objects, DOM, async, first project |
| Technology 401 | 6 | high/low-level languages, compilation, memory, pointers, malloc/free, why C still rules |
| Technology 501 | 6 | tables, SQL, JOIN, MySQL, MariaDB and forks, PostgreSQL, SQLite, MongoDB |
| Technology 601 | 8 | NVIDIA, OpenAI/Anthropic/DeepSeek, Amazon/AWS, Oracle, hosting companies, Big Tech, startups |
| Technology 701 | 6 | Tencent, Alibaba, Baidu, ByteDance/TikTok, DeepSeek, Kimi/Moonshot, Huawei, Xiaomi, DJI, BYD |
| Technology 801 | 6 | Ada, Turing, Hopper, Ritchie, Torvalds, Guido, Gates, Jobs, Bezos, Zuckerberg, Musk, Huang |
| Technology 901 | 6 | ML, neural networks, LLMs, model families, prompting, limits, safety, learning with AI |
| Technology 1001 | 6 | Linux, Git, domains/hosting/deploy, WordPress, freelancing/SaaS, security and a 90-day plan |

Every language topic chapter: a dialogue or short text, 10 words, 40 useful sentences, one grammar point, a tip and a 12-question quiz.
Slides are read only by swiping left and right: nothing scrolls, on a phone or a desktop.
Bangla pronunciation is shown for every line (can be hidden), and the phone's own text-to-speech reads everything aloud.

Live: https://polodev.github.io/ananya/

## How it works

Static HTML, no framework. `python3 build.py` regenerates every page from the course data.

```
curriculum.py                    courses and chapter outlines
content/<course>/ch-NN.json      topic and sentence-builder chapters (generated with muse, checked by validate.py)
letters_ja.py / letters_de.py    letters, sounds, numbers (hand-written) + Japanese romaji/Bangla converters
tech/c101.py … tech/c1001.py     Technology chapters (hand-written big-idea slides)
site_topic.py / site_letters.py / site_builder.py / site_tech.py  turn chapters into slides
engine.py, assets/               HTML helpers, the only CSS and JS
validate.py, tools/              content checks, generation and review tools
```

Progress is stored in the browser (`localStorage`).

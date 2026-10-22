"""Letter and number chapters (hand-written data in letters_ja.py / letters_de.py) -> deck pages."""
import unicodedata

from curriculum import COURSES
from engine import bn, cards, cover, deck_page, esc, finish_slide, mcq, quiz_slide, say_btn, section, seeded, slide
import letters_ja as JA
import letters_de as DE

JA_TTS, DE_TTS = "ja-JP", "de-DE"


def kcell(big, sub, small, say, tts, cls="jp"):
    return (f'<button class="kcell" data-say="{esc(say, quote=True)}" data-lang="{tts}"><span class="{cls}">{esc(big)}</span>'
            f'<b>{esc(sub)}</b><small>{esc(small)}</small></button>')


def jcell(c):
    if c == "・":
        return '<div class="kcell empty"></div>'
    return kcell(c, JA.romaji(c), JA.bangla(c), c, JA_TTS)


def krow(row):
    return '<div class="krow">' + "".join(jcell(c) for c in row) + "</div>"


def exword(word, meaning, tts=JA_TTS, pron=None):
    if tts == JA_TTS:
        return (f'<div class="exword">{say_btn(JA.speakable(word), tts)}<div><div class="jp">{esc(word)}</div>'
                f'<small>{esc(JA.romaji(word))} · {esc(JA.bangla(word))} · {esc(meaning)}</small></div></div>')
    return (f'<div class="exword">{say_btn(word, tts)}<div><div class="de-w">{esc(word)}</div>'
            f'<small><span class="pr">{esc(pron)}</span> · {esc(meaning)}</small></div></div>')


def rcard(word, meaning, tts=JA_TTS, pron=None):
    jp = tts == JA_TTS
    more = f"<b>{esc(JA.romaji(word))}</b> · {esc(JA.bangla(word))} · {esc(meaning)}" if jp else f"<b>{esc(pron)}</b> · {esc(meaning)}"
    return (f'<div class="rcard" role="button" tabindex="0"><div class="top"><span class="{"jp" if jp else "de-w"}">{esc(word)}</span>'
            f'{say_btn(JA.speakable(word) if jp else word, tts)}<span class="tap">ট্যাপ করো</span></div><div class="more">{more}</div></div>')


WRITE_TIP = ('<span class="chip">✍️ লেখার অভ্যাস</span><h2>হাতে লিখলে মনে থাকে</h2>'
             '<ul class="pts"><li>কাগজে প্রতিটি অক্ষর <b>৫ বার</b> লেখো, লেখার সময় জোরে উচ্চারণ করো।</li>'
             '<li>নিয়ম: <b>ওপর থেকে নিচে</b>, <b>বাঁ থেকে ডানে</b>।</li>'
             '<li>ছবি না দেখে মনে করে লেখো, তারপর মিলিয়ে নাও।</li>'
             '<li>প্রতিদিন নতুন অক্ষরের সাথে <b>আগের অক্ষরগুলোও</b> একবার পড়ে নাও।</li></ul>'
             '<div class="callout">💡 রোজ ১০ মিনিট, একদিনে ঘণ্টার পর ঘণ্টা নয় — এভাবেই দ্রুত শেখা হয়।</div>')

NOTES = {
    "し": "‘সি’ নয় — ‘শি’ (shi)।", "ち": "‘চি’ (chi) — ‘টি’ নয়।", "つ": "‘ৎসু’ (tsu): জিভ দাঁতের পেছনে ছুঁয়ে ‘ৎস’ বলো।",
    "ふ": "হু আর ফু-র মাঝামাঝি — ঠোঁট একটু গোল করে আলতো ফুঁ।", "は": "শব্দে ‘হা’, কিন্তু বাক্যের চিহ্ন হিসেবে (わたし は) পড়া হয় ‘ওয়া’।",
    "へ": "দিক বোঝানোর চিহ্ন হিসেবে (えき へ) পড়া হয় ‘এ’।", "を": "উচ্চারণ ‘ও’ (お-র মতো)। শুধু কর্ম বোঝানোর চিহ্ন: ほん を よむ = বই পড়ি।",
    "ん": "নাকের ‘ন’ — একা দাঁড়ায়, কখনো শব্দের শুরুতে বসে না।", "ら": "জাপানি ‘র’ — বাংলা র আর ড়-এর মাঝামাঝি, জিভের ডগা আলতো ছুঁয়ে।",
    "や": "‘ইয়া’ — য় + আ, এক ঝটকায়।", "わ": "‘ওয়া’ — ও + আ দ্রুত।",
    "ぢ": "ぢ আর づ খুব কম লেখা হয় — উচ্চারণ じ আর ず-এর মতোই।",
    "シ": "シ (শি) আর ツ (ৎসু) দেখতে কাছাকাছি — পরের স্লাইডে পার্থক্য দেখো।", "ヲ": "ヲ প্রায় ব্যবহারই হয় না — চিনে রাখলেই চলবে।",
    "ン": "ン (ন) আর ソ (সো) দেখতে কাছাকাছি — পরের স্লাইডে পার্থক্য দেখো।",
}
ROW_NAME = {"あ": "আ", "か": "কা", "さ": "সা", "た": "তা", "な": "না", "は": "হা", "ま": "মা", "や": "ইয়া", "ら": "রা", "わ": "ওয়া", "ん": "ন",
            "が": "গা", "ざ": "জা", "だ": "দা", "ば": "বা", "ぱ": "পা"}


def row_name(row):
    return ROW_NAME[JA.kata_to_hira(row[0])] + "-সারি"


# ------------------------------------------------------------------ Japanese: which letters are known by which chapter
def ja_rows(n):
    return JA.HIRA_ROWS.get(n) or JA.KATA_ROWS.get(n) or []


def ja_letters(n):
    return [c for row in ja_rows(n) for c in row if c != "・"]


def ja_known(n):
    return {c for m in range(1, n + 1) for c in ja_letters(m)}


def _base(c):
    return unicodedata.normalize("NFD", c)[0]


def check_ja_words():
    for n in range(1, 7):
        known = {_base(c) for c in ja_known(n)}
        ok = known | set(" ・")
        if n >= 4:
            ok |= set("っゃゅょッャュョ")   # small letters are taught in chapter 4 (katakana uses the same idea)
        if n >= 6:
            ok |= set("ーァィゥェォ")
        words = [w for row in ja_rows(n) for w in JA.ROW_WORDS.get(row[0], [])]
        if n == 4:
            words += JA.SMALL_TSU + JA.YOON_WORDS + JA.LONG_WORDS
        if n == 6:
            words += JA.KATA_LONG + JA.KATA_NAMES
        for w, _ in words:
            bad = [ch for ch in w if _base(ch) not in ok and ch not in ok]
            assert not bad, f"Japanese chapter {n}: {w} uses letters not taught yet: {bad}"


check_ja_words()


def ja_intro():
    return [slide('<span class="chip">🗾 শুরুর কথা</span><h2>জাপানি লেখা কেমন?</h2>'
                  '<table class="tbl"><tr><th>লেখা</th><th>কী</th><th>কখন</th></tr>'
                  '<tr><td><b class="jp">ひらがな</b></td><td>হিরাগানা — ৪৬ অক্ষর</td><td>জাপানি শব্দ, ব্যাকরণ</td></tr>'
                  '<tr><td><b class="jp">カタカナ</b></td><td>কাতাকানা — ৪৬ অক্ষর</td><td>বিদেশি শব্দ, নাম</td></tr>'
                  '<tr><td><b class="jp">漢字</b></td><td>কাঞ্জি — চীনা অক্ষর</td><td>অর্থবহ অক্ষর (পরের স্তরে)</td></tr></table>'
                  '<div class="callout">এই কোর্সে সব জাপানি লেখা হিরাগানা আর কাতাকানায়, শব্দের মাঝে ফাঁকা রেখে — যাতে সহজে পড়া যায়।</div>', "", "জাপানি লেখা"),
            slide('<span class="chip">✨ সুখবর</span><h2>জাপানি অক্ষর শেখা সহজ</h2>'
                  '<ul class="pts"><li><b>প্রতিটি অক্ষর = একটি ধ্বনি।</b> যা লেখা, তাই পড়া।</li>'
                  '<li>প্রায় প্রতিটি অক্ষর <b>ব্যঞ্জন + স্বর</b>: か = ক + আ = <b>কা</b>। ঠিক বাংলা বর্ণমালার মতো সাজানো।</li>'
                  '<li>পাঁচটি স্বর: <b class="jp">あ い う え お</b> (আ ই উ এ ও) — প্রতিটি সারিতে এই স্বরগুলোই ঘুরে আসে।</li>'
                  '<li>৪ অধ্যায়ে হিরাগানা, ২ অধ্যায়ে কাতাকানা, ১ অধ্যায়ে সংখ্যা।</li></ul>'
                  '<div class="callout">🔊 প্রতিটি অক্ষর ট্যাপ করলে শুনতে পাবে। জাপানি voice না পেলে ফোনের Settings → Text-to-speech থেকে Japanese যোগ করো।</div>', "", "সহজ")]


def ja_row_slides(n):
    out = []
    for row in ja_rows(n):
        notes = "".join(f'<div class="callout">💡 <b class="jp">{c}</b>: {esc(NOTES[c])}</div>' for c in row if c in NOTES)
        out.append(slide(f'<h2 class="jp row-h">{" ".join(c for c in row if c != "・")}</h2>{krow(row)}{notes}', "", row_name(row)))
    return out


def look_slide(n, pairs):
    known, today = ja_known(n), set(ja_letters(n))
    ps = [(a, b, why) for a, b, why in pairs if a in known and b in known and (a in today or b in today)]
    if not ps:
        return []
    rows = [f'<div class="line"><div class="chips"><span class="kchip">{a}</span><span class="kchip">{b}</span></div><div><p>{esc(why)}</p></div></div>'
            for a, b, why in ps]
    return [section("🔍", "একই রকম দেখতে অক্ষর", "এই জোড়াগুলো সবাই গুলিয়ে ফেলে — পার্থক্যটা মনে রাখো"), slide(cards(rows), "", "একই রকম")]


def reading_slides(words, tts=JA_TTS):
    items = [rcard(*w, tts=tts) if tts == JA_TTS else rcard(w[0], w[2], tts, w[1]) for w in words]
    return [section("📖", "শব্দ পড়ো", "আগে নিজে পড়ার চেষ্টা করো", "তারপর কার্ডে ট্যাপ করে উত্তর মিলিয়ে নাও"),
            slide(cards(items), "", "পড়া")]


def chart_slide(rows, title, lead):
    cells = [jcell(c) for row in rows for c in row.ljust(5, "・")]
    return [section("🏆", title, lead), slide(cards(cells, "chart", step=5), "", "পুরো ছক")]


def ja_extras_ch4():
    pairs = [("か", "が"), ("さ", "ざ"), ("た", "だ"), ("は", "ば"), ("は", "ぱ")]
    rows = [f'<div class="exword"><div class="chips"><span class="kchip">{a}</span><span class="kchip">{b}</span></div>'
            f'<div><small>{JA.romaji(a)} → {JA.romaji(b)} · {JA.bangla(a)} → {JA.bangla(b)}</small></div></div>' for a, b in pairs]
    first = [section("゛ ゜", "দুটো ছোট চিহ্ন, ২৫টি নতুন ধ্বনি",
                     "অক্ষরের কোনায় <b>゛ (দুই দাগ)</b> বা <b>゜ (ছোট বৃত্ত)</b> বসালে ধ্বনি বদলে যায়। নতুন করে মুখস্থ করার কিছু নেই!"),
             slide(cards(rows), "", "゛ ゜")]
    small = [section("っ", "ছোট っ = এক মুহূর্ত থামা", "ছোট っ নিজে কোনো ধ্বনি না — পরের ব্যঞ্জনটা দ্বিগুণ হয়, যেন ছোট্ট একটা বিরতি।"),
             slide(cards([exword(*w) for w in JA.SMALL_TSU]
                         + ['<div class="callout">きて (kite) = এসো, কিন্তু きって (kitte) = ডাকটিকিট — ছোট っ-তে অর্থই বদলে যায়!</div>']), "", "ছোট っ")]
    combos = ["きゃ", "きゅ", "きょ", "しゃ", "しゅ", "しょ", "ちゃ", "ちゅ", "ちょ", "じゃ", "じゅ", "じょ"]
    small += [section("ゃ ゅ ょ", "ছোট や ゆ よ = এক ধ্বনি", "ই-কারের অক্ষরের পাশে ছোট ゃ ゅ ょ বসলে দুটো মিলে <b>একটাই ধ্বনি</b>: き + ゃ = きゃ (ক্যা)।"),
              slide(cards([jcell(c) for c in combos], "chart c3", step=3), "", "ゃ ゅ ょ"),
              slide(cards([exword(*w) for w in JA.YOON_WORDS]), "", "ゃ ゅ ょ"),
              section("ー", "লম্বা স্বর", "একই স্বর পরপর এলে (বা お-এর পরে う, え-এর পরে い) টেনে লম্বা করে পড়ো। টান না দিলে অর্থ বদলে যেতে পারে।"),
              slide(cards([exword(*w) for w in JA.LONG_WORDS]), "", "লম্বা স্বর")]
    return first, small


def ja_kata_intro():
    return slide('<span class="chip">カタカナ</span><h2>কাতাকানা কী?</h2>'
                 '<ul class="pts"><li>একই ৪৬টি ধ্বনি, <b>অন্য চেহারা</b>: あ = ア, か = カ। নতুন ধ্বনি শিখতে হবে না!</li>'
                 '<li>কাতাকানা দেখতে কোনাচে, সোজা দাগের — হিরাগানা গোলগাল।</li>'
                 '<li>ব্যবহার: <b>বিদেশি শব্দ</b> (コーヒー = কফি), <b>দেশ ও মানুষের নাম</b> (バングラデシュ, ラフィ)।</li>'
                 '<li>゛ ゜ আর ছোট ッ ャ ュ ョ — হিরাগানার নিয়মই এখানে চলে।</li></ul>'
                 '<div class="callout">💡 তোমার নামও কাতাকানায় লেখা হবে — অধ্যায়ের শেষে দেখবে!</div>', "", "কাতাকানা")


def ja_kata_extras_ch6():
    return [section("ー", "লম্বা টানের দাগ ー", "কাতাকানায় লম্বা স্বর বোঝাতে <b>ー</b> দাগ দেওয়া হয়: コ + ー = コー (কো — লম্বা)।"),
            slide(cards([exword(*w) for w in JA.KATA_LONG]), "", "ー"),
            section("✨", "নাম লেখা কাতাকানায়", "বিদেশি ধ্বনির জন্য ছোট ァ ィ ゥ ェ ォ জুড়ে দেওয়া হয়: フ + ィ = フィ (ফি), ト + ゥ = トゥ (তু)।"),
            slide(cards([exword(*w) for w in JA.KATA_NAMES]), "", "নাম")]


def ja_quiz(n):
    rng = seeded("ja-letters", n)
    today = ja_letters(n)
    kata = n in JA.KATA_ROWS
    earlier = [c for m in range(1, n) for c in ja_letters(m) if (m in JA.KATA_ROWS) == kata]
    pool = today + earlier
    snd = lambda c: JA.bangla(c)
    qs = []

    def kana_opts(c):
        others, seen = [], {snd(c)}
        for x in rng.sample(pool, len(pool)):
            if snd(x) not in seen:
                others.append(x)
                seen.add(snd(x))
        opts = others[:3] + [c]
        rng.shuffle(opts)
        return opts, opts.index(c)

    for c in rng.sample(today, 4):
        opts, a = mcq(rng, snd(c), [snd(x) for x in pool])
        qs.append(dict(q="এই অক্ষরের উচ্চারণ কী?", big=c, o=opts, a=a, say=c, lang=JA_TTS, why=f"{c} = {JA.romaji(c)} ({snd(c)})"))
    for c in rng.sample(today, 3):
        opts, a = kana_opts(c)
        qs.append(dict(q=f"‘{snd(c)}’ ({JA.romaji(c)}) — কোন অক্ষর?", o=opts, a=a, ko=True, why=f"{c} = {JA.romaji(c)}"))
    words = [w for row in ja_rows(n) for w in JA.ROW_WORDS.get(row[0], [])]
    for w, m in rng.sample(words, min(3, len(words))):
        opts, a = mcq(rng, m, [x[1] for x in words])
        qs.append(dict(q="এই শব্দের মানে কী?", big=w, o=opts, a=a, say=JA.speakable(w), lang=JA_TTS, why=f"{w} ({JA.romaji(w)}) = {m}"))
    c = rng.choice(today)
    opts, a = kana_opts(c)
    qs.append(dict(q="🎧 শোনো — কোন অক্ষরটা বলল?", o=opts, a=a, ko=True, say=c, lang=JA_TTS, auto=True, why=f"{c} = {JA.romaji(c)} ({snd(c)})"))
    return qs


def ja_numbers():
    cells = "".join(kcell(d, k, JA.bangla(k), k, JA_TTS, "num") for d, k, _ in JA.NUMBERS)
    def jline(d, k, m):
        return (f'<div class="line">{say_btn(JA.speakable(k), JA_TTS)}<div><p class="tx"><b>{d}</b> · <span class="jp">{esc(k)}</span></p>'
                f'<p class="pr">{esc(JA.bangla(k))}</p><p class="bn">{esc(m)}</p></div></div>')
    S = [section("🔢", "১ থেকে ১০", "ট্যাপ করে শোনো। কয়েকটির দুটো উচ্চারণ আছে।"),
         slide(cards([kcell(d, k, JA.bangla(k), k, JA_TTS, "num") for d, k, _ in JA.NUMBERS], "chart c4", step=4)
               + "".join(f'<p class="hint"><b>{d}</b> <span class="jp">{k}</span>: {esc(m)}</p>' for d, k, m in JA.NUMBERS if "ও বলে" in m), "", "১–১০"),
         section("🧱", "জোড়া লাগিয়ে বানাও", "জাপানি সংখ্যা খুব যুক্তিসঙ্গত: ২০ = “দুই দশ” (に じゅう), ৩৫ = “তিন দশ পাঁচ”।"),
         slide(cards([jline(*x) for x in JA.NUMBERS_BIG[:6]]), "", "বড় সংখ্যা"),
         section("🧱", "ひゃく・せん・まん", "শত, হাজার, দশ হাজার"),
         slide(cards([jline(*x) for x in JA.NUMBERS_BIG[6:]]
                     + ['<div class="callout">💡 জাপানিতে ১০,০০০ (まん) একটা আলাদা একক — ঠিক যেমন বাংলায় “লাখ”। ১,০০,০০০ = じゅう まん (দশ まん)।</div>']), "", "শত-হাজার"),
         section("🍎", "জিনিস গোনা", "দোকানে জিনিস চাওয়ার সময় এই গোনা লাগে: ひとつ、ふたつ…"),
         slide(cards([exword(*w) for w in JA.COUNTERS]), "", "গোনা"),
         section("🗣️", "সংখ্যা দিয়ে বাক্য", "দাম, সময়, ফোন নম্বর"),
         slide(cards([f'<div class="line">{say_btn(JA.speakable(t), JA_TTS)}<div><p class="tx jp">{esc(t)}</p><p class="ro">{esc(JA.romaji(t))}</p>'
                      f'<p class="pr">{esc(JA.bangla(t))}</p><p class="bn">{esc(m)}</p></div></div>' for t, m in JA.NUM_USE]), "", "বাক্য")]
    rng = seeded("ja-num")
    nums = JA.NUMBERS[1:] + JA.NUMBERS_BIG
    qs = []
    for d, k, _ in rng.sample(nums, 4):
        opts, a = mcq(rng, k, [x[1] for x in nums])
        qs.append(dict(q=f"‘{d}’ জাপানিতে কী?", o=opts, a=a, why=f"{d} = {k} ({JA.bangla(k)})"))
    for d, k, _ in rng.sample(nums, 3):
        opts, a = mcq(rng, d, [x[0] for x in nums])
        qs.append(dict(q="🎧 শোনো — কোন সংখ্যা?", say=JA.speakable(k), lang=JA_TTS, auto=True, o=opts, a=a, why=f"{k} = {d}"))
    for d, k, _ in rng.sample(nums, 3):
        opts, a = mcq(rng, d, [x[0] for x in nums])
        qs.append(dict(q="এটা কোন সংখ্যা?", big=k, o=opts, a=a, why=f"{k} = {d}"))
    return S, qs


def build_ja(n):
    course = "japanese/a1"
    meta = COURSES[course]["chapters"][n - 1]
    if n == 7:
        S, qs = ja_numbers()
        learn, chips = ["🔢 ১ থেকে ১০", "🧱 বড় সংখ্যা: শত, হাজার, まん", "🍎 জিনিস গোনা", "🗣️ দাম আর সময়ের বাক্য", "📝 ১০ প্রশ্নের কুইজ"], []
        lead = "জাপানি সংখ্যা খুব নিয়মমাফিক — ১০টা শিখলেই ৯৯ পর্যন্ত বলতে পারবে। দাম, সময়, ফোন নম্বর — সব জায়গায় লাগবে।"
        end_words = [k for _, k, _ in JA.NUMBERS[1:6]]
    else:
        letters = ja_letters(n)
        S = []
        if n == 1:
            S += ja_intro()
        if n == 5:
            S.append(ja_kata_intro())
        if n == 4:
            first, small = ja_extras_ch4()
            S += first + ja_row_slides(n) + small
        else:
            S += ja_row_slides(n)
        if n == 6:
            S += ja_kata_extras_ch6()
        S += look_slide(n, JA.LOOK_KATA if n in JA.KATA_ROWS else JA.LOOK_HIRA)
        if n == 3:
            S += chart_slide([r for m in (1, 2, 3) for r in JA.HIRA_ROWS[m]], "পুরো হিরাগানা ছক", "৪৬টি মূল অক্ষর — সব শেখা হয়ে গেছে! ট্যাপ করে শোনো।")
        if n == 6:
            S += chart_slide([r for m in (5, 6) for r in JA.KATA_ROWS[m]], "পুরো কাতাকানা ছক", "কাতাকানার ৪৬টি অক্ষরও শেষ! ট্যাপ করে শোনো।")
        words = [w for row in ja_rows(n) for w in JA.ROW_WORDS.get(row[0], [])]
        S += reading_slides(words)
        S.append(slide(WRITE_TIP, "", "লেখা"))
        qs = ja_quiz(n)
        learn = [f"✏️ {bn(len(letters))}টি নতুন অক্ষর", "📖 শুধু শেখা অক্ষর দিয়ে শব্দ পড়া", "🔍 একই রকম দেখতে অক্ষর", f"📝 {bn(len(qs))} প্রশ্নের কুইজ"]
        chips = letters
        lead = {1: "জাপানি লেখার প্রথম ধাপ: পাঁচটি স্বর আর দুটো সারি। শেষে নিজেই ছোট ছোট শব্দ পড়ে ফেলবে!",
                2: "আরও তিনটি সারি। মনে রেখো: প্রতিটি সারিতে আ-ই-উ-এ-ও ঘুরে ঘুরে আসে।",
                3: "হিরাগানার শেষ মূল সারিগুলো — এই অধ্যায় শেষে পুরো ৪৬টি অক্ষর তোমার জানা!",
                4: "দুটো ছোট চিহ্ন দিয়ে ২৫টি নতুন ধ্বনি, আর ছোট っ ゃ ゅ ょ — এখন যেকোনো হিরাগানা শব্দ পড়তে পারবে।",
                5: "কাতাকানা: একই ধ্বনি, নতুন চেহারা। বিদেশি শব্দ আর নাম লিখতে লাগে।",
                6: "কাতাকানার বাকি অক্ষর, লম্বা টান ー, আর তোমার নিজের নাম জাপানিতে!"}[n]
        end_words = [w for w, _ in words][:8]
    chip_html = "".join(f'<button class="kchip" data-say="{c}" data-lang="{JA_TTS}">{c}</button>' for c in chips[:16])
    first = cover(f"Japanese A1 · অধ্যায় {bn(n)}", esc(meta["title_bn"]), esc(lead), learn, extra=f'<div class="chips">{chip_html}</div>' if chips else "")
    S = [first] + S + [quiz_slide(qs)]
    nxt = COURSES[course]["chapters"][n]
    S.append(finish_slide(f"অধ্যায় {bn(n)} শেষ!", "আজকের অক্ষরগুলো একবার কাগজে লিখে ফেলো — কাল আবার দেখা হবে।", [esc(w) for w in end_words],
                          f"../ch-{n + 1:02d}/index.html", f"অধ্যায় {bn(n + 1)}: {esc(nxt['title_bn'])}"))
    deck_page(f"{course}/ch-{n:02d}/index.html", f"অধ্যায় {n} · {meta['title_bn']} — Japanese A1", f"{course}/ch-{n:02d}", "ja", S,
              f"অধ্যায় {bn(n)} · {meta['title_bn']}", has_bn=False, has_pr=True)


# ------------------------------------------------------------------ German
def de_line(text, pron, meaning):
    return (f'<div class="line">{say_btn(text, DE_TTS)}<div><p class="tx">{esc(text)}</p><p class="pr">{esc(pron)}</p>'
            f'<p class="bn">{esc(meaning)}</p></div></div>')


def de_alphabet():
    cells = "".join(kcell(L, nm, "", say, DE_TTS, "lat") for L, say, nm, *_ in DE.ALPHABET + [x[:7] for x in DE.EXTRA_LETTERS])
    S = [slide('<span class="chip">🇩🇪 শুরুর কথা</span><h2>জার্মান অক্ষর চেনা — কিন্তু নাম আলাদা</h2>'
               '<ul class="pts"><li>ইংরেজির <b>২৬টি অক্ষরই</b> জার্মানে আছে, সাথে আরও ৪টি: <b>Ä Ö Ü ß</b>।</li>'
               '<li>অক্ষর একই হলেও <b>নাম আর উচ্চারণ আলাদা</b>: W = “ভে”, V = “ফাউ”, J = “ইয়ট”।</li>'
               '<li>সুখবর: জার্মান প্রায় <b>যেমন লেখা তেমন পড়া</b> — নিয়মগুলো শিখলে অচেনা শব্দও পড়তে পারবে।</li>'
               '<li>জার্মানে সব <b>বিশেষ্য (noun) বড় হাতের অক্ষরে</b> শুরু হয়: das Haus, der Tisch।</li></ul>'
               '<div class="callout">🔊 প্রতিটি অক্ষর ট্যাপ করলে শুনবে। জার্মান voice না পেলে ফোনের Settings → Text-to-speech থেকে German যোগ করো।</div>', "", "শুরু"),
         section("🔤", "Das Alphabet", "পুরো বর্ণমালা", "ট্যাপ করে প্রতিটি অক্ষরের নাম শোনো, সাথে জোরে বলো"),
         slide(cards([kcell(L, nm, "", say, DE_TTS, "lat") for L, say, nm, *_ in DE.ALPHABET + [x[:7] for x in DE.EXTRA_LETTERS]], "chart", step=5), "", "বর্ণমালা"),
         section("🔤", "প্রতিটি অক্ষর", "নাম, ধ্বনি আর একটি উদাহরণ")]
    S.append(slide(cards([f'<div class="line"><span class="kchip lat">{L}</span><div><p class="tx">নাম: <b>{esc(nm)}</b> · ধ্বনি: {esc(snd)}</p>'
                          f'<p>{say_btn(w, DE_TTS)} <b class="de-w">{esc(w)}</b> <span class="pr">{esc(wp)}</span></p><p class="bn">{esc(m)}</p></div></div>'
                          for L, _, nm, snd, w, wp, m in DE.ALPHABET]), "", "অক্ষর"))
    for L, say, nm, snd, w, wp, m, note in DE.EXTRA_LETTERS:
        S.append(slide(f'<span class="chip">✨ বিশেষ অক্ষর</span><div class="kana-box"><div class="kana-big lat">{L}</div><div class="k-ro">{esc(nm)}</div>'
                       f'<div class="k-bn">{esc(snd)}</div>{say_btn(say, DE_TTS, big=True)}</div><div class="callout">💡 {esc(note)}</div>'
                       + exword(w, m, DE_TTS, wp), "", L))
    S += [section("🗣️", "Wie schreibt man das?", "ফোনে বা অফিসে নাম বানান করে বলতে হয় — অক্ষরের জার্মান নাম এখানেই কাজে লাগে।"),
          slide(cards([de_line(*x) for x in DE.SPELL]), "", "বানান")]
    rng = seeded("de-alpha")
    pool = DE.ALPHABET
    qs = []
    for L, say, nm, *_ in rng.sample(pool, 4):
        opts, a = mcq(rng, nm, [x[2] for x in pool])
        qs.append(dict(q="এই অক্ষরের জার্মান নাম কী?", big=L, o=opts, a=a, say=say, lang=DE_TTS, why=f"{L} = {nm}"))
    for L, say, nm, *_ in rng.sample(pool, 3):
        opts, a = mcq(rng, L, [x[0] for x in pool])
        qs.append(dict(q="🎧 শোনো — কোন অক্ষর?", say=say, lang=DE_TTS, auto=True, o=opts, a=a, ko=True, why=f"{L} = {nm}"))
    allw = pool + [x[:7] for x in DE.EXTRA_LETTERS]
    for L, _, _, _, w, wp, m in rng.sample(allw, 3):
        opts, a = mcq(rng, m, [x[6] for x in allw])
        qs.append(dict(q=f"‘{w}’ মানে কী?", say=w, lang=DE_TTS, o=opts, a=a, why=f"{w} ({wp}) = {m}"))
    learn = ["🔤 ২৬টি অক্ষরের জার্মান নাম", "✨ Ä Ö Ü ß — চারটি বিশেষ অক্ষর", "🗣️ নিজের নাম বানান করা", f"📝 {bn(len(qs))} প্রশ্নের কুইজ"]
    lead = "ইংরেজির অক্ষরগুলো তুমি চেনো — এবার শিখবে জার্মানে সেগুলোর নাম আর ধ্বনি, সাথে চারটি নতুন অক্ষর।"
    return S, qs, learn, lead, ["Ä", "Ö", "Ü", "ß", "W", "V", "J", "Z"]


def de_rules():
    rules = [(f'<div class="rule"><div class="rule-h"><b class="de-w">{esc(pat)}</b><span>= {esc(snd)}</span></div><p>{esc(why)}</p>'
              + "".join(f'<p class="rule-ex">{say_btn(w, DE_TTS)}<b class="de-w">{esc(w)}</b> <span class="pr">{esc(p)}</span> <span class="bn">· {esc(m)}</span></p>' for w, p, m in ex)
              + "</div>") for pat, snd, why, ex in DE.RULES]
    S = [section("🗣️", "যেমন লেখা, তেমন পড়া", f"{bn(len(DE.RULES))}টি উচ্চারণের নিয়ম"), slide(cards(rules), "", "নিয়ম")]
    words = list(dict.fromkeys((w, p, m) for _, _, _, ex in DE.RULES for w, p, m in ex))
    rng = seeded("de-rules")
    practice = rng.sample(words, 12)
    S += reading_slides(practice, DE_TTS)
    qs = []
    for pat, snd, _, _ in rng.sample(DE.RULES, 4):
        opts, a = mcq(rng, snd, [r[1] for r in DE.RULES])
        qs.append(dict(q=f"জার্মানে ‘{pat}’ কীভাবে পড়ে?", o=opts, a=a, why=f"{pat} = {snd}"))
    for w, p, m in rng.sample(words, 4):
        opts, a = mcq(rng, p, [x[1] for x in words])
        qs.append(dict(q="এই শব্দটা কীভাবে পড়বে?", big=w, o=opts, a=a, say=w, lang=DE_TTS, why=f"{w} = {p} ({m})"))
    for w, p, m in rng.sample(words, 3):
        opts, a = mcq(rng, w, [x[0] for x in words])
        qs.append(dict(q="🎧 শোনো — কোন শব্দ?", say=w, lang=DE_TTS, auto=True, o=opts, a=a, why=f"{w} = {p} ({m})"))
    learn = [f"🗣️ {bn(len(DE.RULES))}টি উচ্চারণের নিয়ম", "📖 অচেনা শব্দ পড়ার অনুশীলন", f"📝 {bn(len(qs))} প্রশ্নের কুইজ"]
    lead = "জার্মান বানান খুব নিয়মমাফিক। ei, ie, sch, ch, w, z — এই কয়েকটা নিয়ম জানলেই অচেনা শব্দও ঠিকঠাক পড়তে পারবে।"
    return S, qs, learn, lead, ["ei", "ie", "eu", "sch", "ch", "w", "z"]


def de_numbers():
    cells = "".join(kcell(d, w, p, w, DE_TTS, "num") for d, w, p in DE.NUMBERS)
    S = [section("🔢", "০ থেকে ১২", "এগুলো আলাদা করে মুখস্থ করতে হবে। ট্যাপ করে শোনো।"),
         slide(cards([kcell(d, w, p, w, DE_TTS, "num") for d, w, p in DE.NUMBERS], "chart c3", step=3), "", "০–১২"),
         section("🔢", "১৩–১৯: সংখ্যা + zehn", "আগে একক, তারপর <b>zehn</b> (দশ)। drei + zehn = dreizehn।"),
         slide(cards([de_line(w, p, d) for d, w, p in DE.TEENS]
                     + ['<div class="callout warn">⚠️ ১৬ = sech<b>zehn</b> (s বাদ), ১৭ = sieb<b>zehn</b> (en বাদ)।</div>']), "", "১৩–১৯"),
         section("🔢", "২০, ৩০ … ১০০০", "দশকের শেষে <b>-zig</b> (ৎসিশ), শুধু ৩০ = drei<b>ßig</b>।"),
         slide(cards([de_line(w, p, d) for d, w, p in DE.TENS]), "", "দশক"),
         section("🧩", "আগে একক, পরে দশক", "২১ = <b>ein-und-zwanzig</b> = “এক আর বিশ”। ইংরেজির উল্টো — একক আগে, “und” (আর) দিয়ে জোড়া।"),
         slide(cards([de_line(w, p, f"{d} = {m}") for d, w, p, m in DE.COMPOUND]
                     + ['<div class="callout">💡 পুরো সংখ্যাটা এক শব্দে লেখা হয় — যত লম্বাই হোক!</div>']), "", "জোড়া"),
         section("🗣️", "দাম, সময়, বয়স", "সংখ্যা কাজে লাগাও"),
         slide(cards([de_line(*x) for x in DE.NUM_USE]), "", "বাক্য")]
    rng = seeded("de-num")
    nums = DE.NUMBERS[1:] + DE.TEENS + DE.TENS + [x[:3] for x in DE.COMPOUND]
    qs = []
    for d, w, p in rng.sample(nums, 4):
        opts, a = mcq(rng, w, [x[1] for x in nums])
        qs.append(dict(q=f"‘{d}’ জার্মানে কী?", o=opts, a=a, why=f"{d} = {w} ({p})"))
    for d, w, p in rng.sample(nums, 3):
        opts, a = mcq(rng, d, [x[0] for x in nums])
        qs.append(dict(q="🎧 শোনো — কোন সংখ্যা?", say=w, lang=DE_TTS, auto=True, o=opts, a=a, why=f"{w} = {d}"))
    for d, w, p in rng.sample(nums, 3):
        opts, a = mcq(rng, d, [x[0] for x in nums])
        qs.append(dict(q=f"‘{w}’ — কোন সংখ্যা?", say=w, lang=DE_TTS, o=opts, a=a, why=f"{w} = {d}"))
    learn = ["🔢 ০ থেকে ১২", "🧩 ১৩–৯৯ বানানোর নিয়ম", "🗣️ দাম, সময়, বয়স বলা", f"📝 {bn(len(qs))} প্রশ্নের কুইজ"]
    lead = "দাম, সময়, বয়স, ফোন নম্বর — সংখ্যা ছাড়া চলে না। জার্মান সংখ্যার মজার নিয়ম: ২১ বলা হয় “এক আর বিশ”!"
    return S, qs, learn, lead, ["eins", "zwei", "drei", "zehn", "zwanzig", "hundert"]


def build_de(n):
    course = "german/a1"
    meta = COURSES[course]["chapters"][n - 1]
    S, qs, learn, lead, chips = {1: de_alphabet, 2: de_rules, 3: de_numbers}[n]()
    chip_html = "".join(f'<button class="kchip lat" data-say="{c}" data-lang="{DE_TTS}">{c}</button>' for c in chips)
    S = [cover(f"German A1 · অধ্যায় {bn(n)}", esc(meta["title_bn"]), esc(lead), learn, extra=f'<div class="chips">{chip_html}</div>')] + S
    S.append(quiz_slide(qs))
    nxt = COURSES[course]["chapters"][n]
    S.append(finish_slide(f"অধ্যায় {bn(n)} শেষ!", "আজকের শব্দগুলো জোরে পড়ো — জার্মান মুখে বসাতে উচ্চারণের অনুশীলনই আসল।", chips,
                          f"../ch-{n + 1:02d}/index.html", f"অধ্যায় {bn(n + 1)}: {esc(nxt['title_bn'])}"))
    deck_page(f"{course}/ch-{n:02d}/index.html", f"অধ্যায় {n} · {meta['title_bn']} — German A1", f"{course}/ch-{n:02d}", "de", S,
              f"অধ্যায় {bn(n)} · {meta['title_bn']}", has_bn=True, has_pr=True)


def build(course_key, n):
    (build_ja if course_key.startswith("japanese") else build_de)(n)

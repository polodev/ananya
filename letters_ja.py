"""Japanese letters (hand-written, never generated): hiragana and katakana tables, example words, numbers, and
romaji() / bangla() converters. Romaji and Bangla pronunciation of every Japanese line in the site come from these
converters, so they are never typed by hand. Japanese text is kana only, words separated by spaces."""
import re

# hiragana -> (romaji, Bangla)
K = {
    "あ": ("a", "আ"), "い": ("i", "ই"), "う": ("u", "উ"), "え": ("e", "এ"), "お": ("o", "ও"),
    "か": ("ka", "কা"), "き": ("ki", "কি"), "く": ("ku", "কু"), "け": ("ke", "কে"), "こ": ("ko", "কো"),
    "さ": ("sa", "সা"), "し": ("shi", "শি"), "す": ("su", "সু"), "せ": ("se", "সে"), "そ": ("so", "সো"),
    "た": ("ta", "তা"), "ち": ("chi", "চি"), "つ": ("tsu", "ৎসু"), "て": ("te", "তে"), "と": ("to", "তো"),
    "な": ("na", "না"), "に": ("ni", "নি"), "ぬ": ("nu", "নু"), "ね": ("ne", "নে"), "の": ("no", "নো"),
    "は": ("ha", "হা"), "ひ": ("hi", "হি"), "ふ": ("fu", "ফু"), "へ": ("he", "হে"), "ほ": ("ho", "হো"),
    "ま": ("ma", "মা"), "み": ("mi", "মি"), "む": ("mu", "মু"), "め": ("me", "মে"), "も": ("mo", "মো"),
    "や": ("ya", "ইয়া"), "ゆ": ("yu", "ইউ"), "よ": ("yo", "ইয়ো"),
    "ら": ("ra", "রা"), "り": ("ri", "রি"), "る": ("ru", "রু"), "れ": ("re", "রে"), "ろ": ("ro", "রো"),
    "わ": ("wa", "ওয়া"), "を": ("wo", "ও"), "ん": ("n", "ন"),
    "が": ("ga", "গা"), "ぎ": ("gi", "গি"), "ぐ": ("gu", "গু"), "げ": ("ge", "গে"), "ご": ("go", "গো"),
    "ざ": ("za", "জা"), "じ": ("ji", "জি"), "ず": ("zu", "জু"), "ぜ": ("ze", "জে"), "ぞ": ("zo", "জো"),
    "だ": ("da", "দা"), "ぢ": ("ji", "জি"), "づ": ("zu", "জু"), "で": ("de", "দে"), "ど": ("do", "দো"),
    "ば": ("ba", "বা"), "び": ("bi", "বি"), "ぶ": ("bu", "বু"), "べ": ("be", "বে"), "ぼ": ("bo", "বো"),
    "ぱ": ("pa", "পা"), "ぴ": ("pi", "পি"), "ぷ": ("pu", "পু"), "ぺ": ("pe", "পে"), "ぽ": ("po", "পো"),
}
# i-row + small ya/yu/yo
YOON = {}
for base, (r, b) in [("き", ("ky", "ক")), ("し", ("sh", "শ")), ("ち", ("ch", "চ")), ("に", ("ny", "ন")), ("ひ", ("hy", "হ")),
                     ("み", ("my", "ম")), ("り", ("ry", "র")), ("ぎ", ("gy", "গ")), ("じ", ("j", "জ")), ("び", ("by", "ব")), ("ぴ", ("py", "প"))]:
    for small, v, bv in [("ゃ", "a", "্যা"), ("ゅ", "u", "্যু"), ("ょ", "o", "্যো")]:
        if r in ("sh", "ch", "j"):
            bv = {"a": "া", "u": "ু", "o": "ো"}[v]
        YOON[base + small] = (r + v, b + bv)
# katakana-only combinations used in loanwords
EXTRA = {"てぃ": ("ti", "টি"), "でぃ": ("di", "ডি"), "ふぁ": ("fa", "ফা"), "ふぃ": ("fi", "ফি"), "ふぇ": ("fe", "ফে"),
         "ふぉ": ("fo", "ফো"), "うぃ": ("wi", "উই"), "うぇ": ("we", "ওয়ে"), "うぉ": ("wo", "ওয়ো"), "しぇ": ("she", "শে"),
         "じぇ": ("je", "জে"), "ちぇ": ("che", "চে"), "とぅ": ("tu", "তু"), "どぅ": ("du", "দু"), "ゔぁ": ("va", "ভা")}
VOWEL_SIGN = {"আ": "া", "ই": "ি", "উ": "ু", "এ": "ে", "ও": "ো"}
PARTICLES = {"は": ("wa", "ওয়া"), "を": ("o", "ও"), "へ": ("e", "এ")}
WORDS_FIXED = {"こんにちは": ("konnichiwa", "কোন্নিচিওয়া"), "こんばんは": ("konbanwa", "কোম্বানওয়া")}
PUNCT = "。、？！"


def kata_to_hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def is_kana_text(s):
    return all(c in PUNCT or c == " " or c == "ー" or "ぁ" <= c <= "ゖ" or "ァ" <= c <= "ヺ" for c in s)


def _morae(word):
    """split a hiragana word into (kana, romaji, bangla) units; 'Q' = small tsu, 'L' = long mark ー."""
    out, i = [], 0
    while i < len(word):
        two = word[i:i + 2]
        if two in YOON or two in EXTRA:
            r, b = YOON.get(two) or EXTRA[two]
            out.append((two, r, b))
            i += 2
            continue
        c = word[i]
        if c == "っ":
            out.append(("Q", "", ""))
        elif c == "ー":
            out.append(("L", "", ""))
        elif c in K:
            out.append((c, *K[c]))
        elif c in "ぁぃぅぇぉ":   # lone small vowel (rare): read as the vowel
            out.append((c, *K[chr(ord(c) + 1)]))
        else:
            raise ValueError(f"unsupported kana {c!r} in {word!r}")
        i += 1
    return out


def _vowel(r):
    return r[-1] if r and r[-1] in "aiueo" else ""


def romaji(text):
    """Hepburn-style romaji (long vowels written as spelled: ou, ei; katakana ー doubles the vowel)."""
    words = []
    for tok in kata_to_hira(text).split():
        tok_c = tok.strip(PUNCT)
        tail = tok[len(tok.rstrip(PUNCT)):]
        tail = tail.replace("。", ".").replace("、", ",").replace("？", "?").replace("！", "!")
        if not tok_c:
            words.append(tail)
            continue
        if tok_c in PARTICLES:
            words.append(PARTICLES[tok_c][0] + tail)
            continue
        if tok_c in WORDS_FIXED:
            words.append(WORDS_FIXED[tok_c][0] + tail)
            continue
        r, gem, prev = "", False, ""
        for k, rr, _ in _morae(tok_c):
            if k == "Q":
                gem = True
                continue
            if k == "L":
                r += _vowel(prev)
                continue
            if gem:
                rr = ("t" + rr) if rr.startswith("ch") else rr[0] + rr
                gem = False
            r += rr
            prev = rr
        words.append(r + tail)
    out = " ".join(w for w in words if w)
    return re.sub(r"\s+([.,?!])", r"\1", out)


def bangla(text):
    """Bangla-script pronunciation. Long vowels are not doubled (こう -> কো), final す of です/ます is 'স',
    small っ doubles the next consonant, ん before b/p/m is 'ম'."""
    words = []
    for tok in kata_to_hira(text).split():
        tok_c = tok.strip(PUNCT)
        tail = tok[len(tok.rstrip(PUNCT)):].replace("。", "।").replace("、", ",").replace("？", "?").replace("！", "!")
        if not tok_c:
            words.append(tail)
            continue
        if tok_c in PARTICLES:
            words.append(PARTICLES[tok_c][1] + tail)
            continue
        if tok_c in WORDS_FIXED:
            words.append(WORDS_FIXED[tok_c][1] + tail)
            continue
        m = _morae(tok_c)
        b, gem = "", False
        for idx, (k, rr, bb) in enumerate(m):
            prev_r = next((x[1] for x in reversed(m[:idx]) if x[0] not in ("Q", "L")), "")
            if k == "Q":
                gem = True
                continue
            if k == "L":
                continue
            # long vowels: おう / おお / うう / えい stay readable without doubling
            if k in ("う", "お") and _vowel(prev_r) == "o" and prev_r != "":
                continue
            if k == "う" and _vowel(prev_r) == "u" and prev_r != "":
                continue
            if k == "い" and _vowel(prev_r) == "i" and prev_r != "":
                continue
            if k == "あ" and _vowel(prev_r) == "a" and prev_r != "":
                continue
            if k == "ん":
                nxt = next((x[1] for x in m[idx + 1:] if x[0] not in ("Q", "L")), "")
                bb = "ম" if nxt[:1] in ("b", "p", "m") else "ন"
            if gem:
                first = bb[0]
                if first in "আইউএও":   # っ before a vowel: just a stop
                    pass
                else:
                    cons = "ক" if rr.startswith("k") else "ত" if rr.startswith(("t", "ch", "ts")) else "প" if rr.startswith("p") else "শ" if rr.startswith("sh") else "স" if rr.startswith("s") else first
                    b += cons + "্"
                gem = False
            b += bb
        if (tok_c.endswith("です") or tok_c.endswith("ます")) and b.endswith("সু"):
            b = b[:-2] + "স"
        words.append(b + tail)
    out = " ".join(w for w in words if w)
    return re.sub(r"\s+([।,?!])", r"\1", out)


def speakable(text):
    """text for speechSynthesis: no learner spaces."""
    return text.replace(" ", "")


# ------------------------------------------------------------------ teaching data for the letter chapters
# chapter -> list of rows (each row a string of kana; '・' marks an empty cell in the 5-column grid)
HIRA_ROWS = {
    1: ["あいうえお", "かきくけこ", "さしすせそ"],
    2: ["たちつてと", "なにぬねの", "はひふへほ"],
    3: ["まみむめも", "や・ゆ・よ", "らりるれろ", "わ・・・を", "ん・・・・"],
    4: ["がぎぐげご", "ざじずぜぞ", "だぢづでど", "ばびぶべぼ", "ぱぴぷぺぽ"],
}
KATA_ROWS = {
    5: ["アイウエオ", "カキクケコ", "サシスセソ", "タチツテト", "ナニヌネノ"],
    6: ["ハヒフヘホ", "マミムメモ", "ヤ・ユ・ヨ", "ラリルレロ", "ワ・・・ヲ", "ン・・・・"],
}

# one example word per row (kana, Bangla meaning); every word uses only letters taught up to that chapter
ROW_WORDS = {
    "あ": [("あい", "ভালোবাসা"), ("いえ", "বাড়ি"), ("あおい", "নীল"), ("うえ", "উপরে")],
    "か": [("かお", "মুখ"), ("あき", "শরৎকাল"), ("いけ", "পুকুর"), ("こえ", "কণ্ঠস্বর")],
    "さ": [("あさ", "সকাল"), ("すし", "সুশি"), ("いす", "চেয়ার"), ("せかい", "পৃথিবী")],
    "た": [("たかい", "উঁচু, দামি"), ("くち", "মুখগহ্বর"), ("つくえ", "টেবিল"), ("そと", "বাইরে")],
    "な": [("なつ", "গ্রীষ্মকাল"), ("ねこ", "বিড়াল"), ("いぬ", "কুকুর"), ("さかな", "মাছ")],
    "は": [("はな", "ফুল"), ("ひと", "মানুষ"), ("ふね", "নৌকা"), ("ほし", "তারা")],
    "ま": [("みみ", "কান"), ("あたま", "মাথা"), ("むし", "পোকা"), ("みせ", "দোকান")],
    "や": [("やま", "পাহাড়"), ("ゆめ", "স্বপ্ন"), ("よる", "রাত"), ("へや", "ঘর")],
    "ら": [("そら", "আকাশ"), ("くるま", "গাড়ি"), ("とり", "পাখি"), ("さくら", "চেরি ফুল")],
    "わ": [("わたし", "আমি"), ("かわ", "নদী"), ("ほん を よむ", "বই পড়া")],
    "ん": [("ほん", "বই"), ("みかん", "কমলা"), ("にほん", "জাপান"), ("せんせい", "শিক্ষক")],
    "が": [("がっこう", "স্কুল"), ("かぎ", "চাবি"), ("ごはん", "ভাত, খাবার")],
    "ざ": [("ちず", "মানচিত্র"), ("かぜ", "বাতাস, সর্দি"), ("ぞう", "হাতি")],
    "だ": [("ともだち", "বন্ধু"), ("でんわ", "ফোন"), ("まど", "জানালা")],
    "ば": [("かばん", "ব্যাগ"), ("えび", "চিংড়ি"), ("ぶどう", "আঙুর")],
    "ぱ": [("さんぽ", "হাঁটাহাঁটি"), ("えんぴつ", "পেন্সিল"), ("ぺん", "কলম")],
    "ア": [("アイス", "আইসক্রিম"), ("ネクタイ", "টাই")],
    "カ": [("ココア", "কোকো (পানীয়)"), ("ガス", "গ্যাস")],
    "サ": [("サイズ", "মাপ, সাইজ"), ("セット", "সেট")],
    "タ": [("テスト", "পরীক্ষা"), ("チケット", "টিকিট")],
    "ナ": [("テニス", "টেনিস"), ("ナッツ", "বাদাম")],
    "ハ": [("ホテル", "হোটেল"), ("ヘア", "চুল (সেলুনে)")],
    "マ": [("メール", "ইমেইল"), ("ミルク", "দুধ"), ("マスク", "মাস্ক")],
    "ヤ": [("ヨガ", "যোগব্যায়াম"), ("ヨーグルト", "দই")],
    "ラ": [("ラジオ", "রেডিও"), ("レモン", "লেবু"), ("トイレ", "টয়লেট")],
    "ワ": [("ワイシャツ", "শার্ট")],
    "ン": [("パン", "রুটি"), ("ペン", "কলম"), ("バングラデシュ", "বাংলাদেশ")],
}
SMALL_TSU = [("きって", "ডাকটিকিট"), ("ざっし", "ম্যাগাজিন"), ("ちょっと", "একটু")]
YOON_WORDS = [("おちゃ", "চা"), ("しゃしん", "ছবি"), ("びょういん", "হাসপাতাল"), ("べんきょう", "পড়াশোনা"), ("きょう", "আজ")]
LONG_WORDS = [("おかあさん", "মা"), ("おとうさん", "বাবা"), ("ありがとう", "ধন্যবাদ"), ("せんせい", "শিক্ষক")]
KATA_LONG = [("コーヒー", "কফি"), ("ケーキ", "কেক"), ("ノート", "খাতা"), ("スーパー", "সুপারমার্কেট")]
KATA_NAMES = [("ラフィ", "রাফি"), ("ミトゥ", "মিতু"), ("ダッカ", "ঢাকা"), ("バングラデシュ", "বাংলাদেশ")]

LOOK_HIRA = [
    ("あ", "お", "お-র ডান পাশে আলাদা একটা ছোট দাগ আছে; あ-তে নেই।"),
    ("い", "り", "い-র বাঁ দাগটা লম্বা; り-র ডান দাগটা লম্বা।"),
    ("さ", "き", "き-তে আড়াআড়ি দাগ দুটো; さ-তে একটা।"),
    ("こ", "に", "に-র বাঁ পাশে একটা খাড়া দাগ আছে।"),
    ("ぬ", "め", "ぬ-র শেষে ছোট একটা ফাঁস (loop) আছে; め-তে নেই।"),
    ("は", "ほ", "ほ-র ডান অংশের ওপরে বাড়তি একটা আড়াআড়ি দাগ।"),
    ("る", "ろ", "る-র শেষে ফাঁস আছে; ろ-তে নেই।"),
    ("ね", "れ", "ね-র শেষে ফাঁস আছে; れ-র শেষে বাইরের দিকে টান।"),
    ("わ", "れ", "わ-র লেজ ভিতরে গোল হয়ে ফেরে; れ-র লেজ বাইরে যায়।"),
]
LOOK_KATA = [
    ("シ", "ツ", "シ-র ফোঁটা দুটো বাঁ দিকে, শেষ দাগ নিচ থেকে ওপরে; ツ-র ফোঁটা ওপরে, শেষ দাগ ওপর থেকে নিচে।"),
    ("ソ", "ン", "ソ-র ছোট দাগটা ওপরে খাড়া; ン-এর ছোট দাগটা বাঁ দিকে শোয়ানো।"),
    ("ク", "タ", "タ-র ভেতরে একটা বাড়তি ছোট দাগ আছে।"),
    ("コ", "ユ", "ユ-র নিচের দাগটা ডানে বেরিয়ে যায়।"),
    ("ウ", "ワ", "ウ-র ওপরে একটা ছোট দাগ আছে; ワ-তে নেই।"),
    ("ス", "ヌ", "ヌ-র মাঝখান দিয়ে একটা বাড়তি দাগ কাটে।"),
]

# numbers: (value label, kana, Bangla meaning)
NUMBERS = [
    ("0", "ゼロ", "শূন্য (れい-ও বলে)"), ("1", "いち", "এক"), ("2", "に", "দুই"), ("3", "さん", "তিন"), ("4", "よん", "চার (し-ও বলে)"),
    ("5", "ご", "পাঁচ"), ("6", "ろく", "ছয়"), ("7", "なな", "সাত (しち-ও বলে)"), ("8", "はち", "আট"), ("9", "きゅう", "নয় (く-ও বলে)"),
    ("10", "じゅう", "দশ"),
]
NUMBERS_BIG = [
    ("11", "じゅう いち", "১০ + ১"), ("15", "じゅう ご", "১০ + ৫"), ("20", "に じゅう", "২ × ১০"), ("35", "さん じゅう ご", "৩ × ১০ + ৫"),
    ("100", "ひゃく", "একশো"), ("300", "さんびゃく", "তিনশো (b হয়ে যায়)"), ("600", "ろっぴゃく", "ছয়শো"), ("800", "はっぴゃく", "আটশো"),
    ("1000", "せん", "এক হাজার"), ("3000", "さんぜん", "তিন হাজার"), ("10000", "いちまん", "দশ হাজার — জাপানিতে আলাদা একক!"),
]
COUNTERS = [("ひとつ", "একটি"), ("ふたつ", "দুটি"), ("みっつ", "তিনটি"), ("よっつ", "চারটি"), ("いつつ", "পাঁচটি")]
NUM_USE = [("いま なんじ です か。", "এখন কয়টা বাজে?"), ("さんじ です。", "তিনটা বাজে।"), ("これ は いくら です か。", "এটার দাম কত?"),
           ("ひゃく えん です。", "১০০ ইয়েন।"), ("ひとつ ください。", "একটা দিন।"), ("でんわ ばんごう は なん ばん です か。", "ফোন নম্বর কত?")]

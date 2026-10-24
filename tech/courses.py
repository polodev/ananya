"""Technology course registry. Each course is a list of chapters; each chapter is a list of big slides."""
from . import c101, c201, c301, c401, c501, c601, c701, c801, c901, c1001

CONTENT = {
    "101": c101.CHAPTERS,
    "201": c201.CHAPTERS,
    "301": c301.CHAPTERS,
    "401": c401.CHAPTERS,
    "501": c501.CHAPTERS,
    "601": c601.CHAPTERS,
    "701": c701.CHAPTERS,
    "801": c801.CHAPTERS,
    "901": c901.CHAPTERS,
    "1001": c1001.CHAPTERS,
}

META = [
    dict(key="101", title="Technology 101", tag="কম্পিউটার থেকে কোম্পানি",
         sub="কম্পিউটার, ইন্টারনেট, ওয়েব, ডেটা, প্রোগ্রামিং, ভাষা, ডেটাবেস, ক্লাউড — প্রথম পূর্ণ ছবি",
         lead="একদম শূন্য থেকে শুরু। প্রতিটি স্লাইডে একটা করে বড় ধারণা, সহজ বাংলায়, চেনা উদাহরণ দিয়ে। "
              "শেষে তুমি জানবে কম্পিউটার কীভাবে চলে, ইন্টারনেট কোথায় যায়, আর টেক দুনিয়ার বড় নামগুলো কী করে।",
         icon="🖥️"),
    dict(key="201", title="Technology 201", tag="ইন্টারনেট, ওয়েব ও ক্লাউড",
         sub="IP, DNS, HTTP, ব্রাউজার, সার্ভার, API, ডেটাবেস, Docker, হোস্টিং, নিরাপত্তা",
         lead="প্রথম কোর্সের ধারণাগুলো এবার গভীরে। একটি রিকোয়েস্ট কোথায় যায়, সার্ভার কীভাবে উত্তর দেয়, "
              "ক্লাউডে সার্ভার কীভাবে ভাড়া হয়, আর সাইট নিরাপদ রাখতে কী লাগে — সব ধাপে ধাপে।",
         icon="🌐"),
    dict(key="301", title="Technology 301", tag="JavaScript দিয়ে প্রথম প্রোগ্রামিং",
         sub="variable, শর্ত, লুপ, ফাংশন, অ্যারে, অবজেক্ট, DOM, async, প্রথম প্রজেক্ট",
         lead="এবার নিজে কোড লিখবে। JavaScript দিয়ে শুরু — কারণ এটা ব্রাউজারেই চলে, আলাদা সেটআপ লাগে না। "
              "শেষে তুমি ছোট অ্যাপ বানাতে, error পড়তে আর Git-এ সেভ করতে পারবে।",
         icon="🟨"),
    dict(key="401", title="Technology 401", tag="C ও কম্পিউটারের ভেতরটা",
         sub="high/low level, compilation, memory, pointers, malloc, কেন C এখনও রাজত্ব করে",
         lead="JavaScript-এ মেশিন লুকানো ছিল। C-তে সেটা খুলে দেখবে: মেমোরি, ঠিকানা, pointer, heap, stack — "
              "কম্পিউটার আসলে কীভাবে কাজ করে।",
         icon="🇨"),
    dict(key="501", title="Technology 501", tag="ডেটাবেস, SQL ও fork",
         sub="টেবিল, SQL, JOIN, MySQL, MariaDB, PostgreSQL, SQLite, MongoDB, fork",
         lead="ডেটার জগতে ঢুকবে। SQL দিয়ে প্রশ্ন করা, টেবিল জোড়া, MySQL-এর ইতিহাস, MariaDB-র fork, "
              "আর কোন কাজে কোন ডেটাবেস — সব ধাপে ধাপে।",
         icon="🗃️"),
    dict(key="601", title="Technology 601", tag="বিশ্বের টেক কোম্পানি",
         sub="NVIDIA, OpenAI, Anthropic, AWS, Oracle, Linode, Hetzner, Hostinger, Meta, Google, startups",
         lead="খবরে যে নামগুলো শোনো, তাদের ব্যবসা বুঝবে। কে কী বানায়, টাকা কোথা থেকে আসে, "
              "আর কোন কোম্পানি কেন গুরুত্বপূর্ণ।",
         icon="🏢"),
    dict(key="701", title="Technology 701", tag="চীনের টেক ইকোসিস্টেম",
         sub="Tencent, Alibaba, Baidu, ByteDance/TikTok, DeepSeek, Kimi/Moonshot, Huawei, Xiaomi, DJI, BYD",
         lead="চীনের টেক দুনিয়া নিজের পথে বড় হয়েছে। Super app, short video algorithm, open-weight AI, "
              "EV আর ড্রোন — কীভাবে, আর কী শেখা যায়।",
         icon="🐉"),
    dict(key="801", title="Technology 801", tag="যারা টেক বানিয়েছে",
         sub="Ada, Turing, Hopper, Ritchie, Torvalds, Guido, Jobs, Gates, Bezos, Zuckerberg, Musk, Huang",
         lead="প্রযুক্তির পেছনের মানুষগুলো। তাঁদের ভুল, জেদ, আর ধারণা — যেটা আজকের কম্পিউটার, ইন্টারনেট "
              "আর AI-কে সম্ভব করেছে।",
         icon="👤"),
    dict(key="901", title="Technology 901", tag="AI-এর যুগ",
         sub="ML, neural network, LLM, token, GPT/Claude/Gemini, prompting, limits, safety",
         lead="AI কীভাবে কাজ করে, কেন ভুল করে, কীভাবে ভালোভাবে ব্যবহার করবে — আর কোন সিদ্ধান্ত "
              "মানুষেরই রাখা উচিত।",
         icon="🧠"),
    dict(key="1001", title="Technology 1001", tag="বানাও, ছাপাও, ইন্টারনেটে দাও",
         sub="Linux, Git, ডোমেইন, হোস্টিং, WordPress, no-code, freelancing, SaaS, security",
         lead="শেখা শেষে বানানোর পালা। Linux, Git, ডিপ্লয়, WordPress, freelancing আর নিরাপত্তা — "
              "নিজের সাইট বা ছোট ব্যবসা দাঁড় করানোর ব্যবহারিক পথ।",
         icon="🚀"),
]

TECH_COURSES = {}
for _m in META:
    _chs = CONTENT[_m["key"]]
    TECH_COURSES[f"technology/{_m['key']}"] = dict(
        lang="technology", level=_m["key"], title=_m["title"], tag=_m["tag"],
        sub=_m["sub"], lead=_m["lead"], icon=_m["icon"],
        chapters=[dict(title_bn=c["title_bn"], topic=c["title_en"], grammar=c["hook"],
                       kind="tech", slides=len(c["slides"])) for c in _chs],
        tech_chapters=_chs,
        slides_total=sum(len(c["slides"]) for c in _chs),
    )

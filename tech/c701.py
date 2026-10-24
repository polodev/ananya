"""Technology 701: the Chinese tech ecosystem — platforms, AI labs and hardware."""
from .slidekit import *

CHAPTERS = [

chapter(
    "চীনের টেক মানচিত্র",
    "The map of Chinese tech",
    "Tencent, Alibaba, Baidu, ByteDance, Huawei, DeepSeek — চীনের টেক দুনিয়া কীভাবে সাজানো?",
    [
        big("মূল ধারণা", "চীন = বিশাল বাজার + দ্রুত তৈরি + নিজের ইকোসিস্টেম",
            "১.৪ বিলিয়ন মানুষ, শক্তিশালী ম্যানুফ্যাকচারিং, সরকারি সহায়তা, আর নিজের অ্যাপ ecosystem — "
            "তাই চীনা কোম্পানি আলাদা পথে বড় হয়েছে।", "🇨🇳"),
        terms("চারটা টেক হাব", "Shenzhen, Hangzhou, Beijing, Shanghai", [
            ("Shenzhen", "হার্ডওয়্যার ও ডিভাইস", "Huawei, Tencent, DJI, BYD।"),
            ("Hangzhou", "e-commerce ও AI", "Alibaba, DeepSeek।"),
            ("Beijing", "search, AI, media", "Baidu, ByteDance, Moonshot।"),
            ("Shanghai", "fintech, chips", "SMIC, অনেকে startup।")]),
        flow("চীনা টেকের চারটা স্তর", [
            ("Platform", "WeChat, Taobao, Douyin।"),
            ("Payment", "WeChat Pay, Alipay।"),
            ("Cloud", "Alibaba Cloud, Tencent Cloud।"),
            ("Hardware", "Huawei, Xiaomi, BYD, DJI।"),
        ]),
        big("Super app = অনেক অ্যাপ এক অ্যাপে", "WeChat-এ মেসেজ, পেমেন্ট, টিকিট, সরকারি সেবা, খাবার অর্ডার — সব। "
            "পশ্চিমে আলাদা আলাদা অ্যাপ, চীনে একটাই অভ্যাস।", "📱"),
        big("Copycat থেকে innovator", "শুরুতে চীনা কোম্পানি পশ্চিমের ধারণা নকল করেছে। এখন super app, short video algorithm, "
            "EV, drone, open-weight AI-তে নিজেরাই নতুন পথ দেখাচ্ছে।", "🔄"),
        terms("চারটা শব্দ", "state support, scale, censorship, open weight", [
            ("State support", "সরকারি সহায়তা", "subsidy, policy, infrastructure।"),
            ("Scale", "বিশাল বাজার", "এক দেশেই কোটি ব্যবহারকারী।"),
            ("Censorship", "কনটেন্ট নিয়ন্ত্রণ", "কোন বিষয় নিয়ে কথা বলা যাবে, সীমা আছে।"),
            ("Open weight", "মডেলের ওজন খোলা", "DeepSeek, Qwen, Kimi K2।")]),
        big("চীনা অ্যাপ বিদেশে", "TikTok, CapCut, Shein, Temu, PUBG Mobile — চীনা কোম্পানির পণ্য বিশ্বজুড়ে। "
            "কিছু অ্যাপ রাজনৈতিক বিতর্কেও পড়ে।", "🌍"),
        big("চীন কীভাবে এত দ্রুত?", "বিশাল প্রতিযোগিতা, দ্রুত prototype, ম্যানুফ্যাকচারিং সরবরাহ chain, আর "
            "ইঞ্জিনিয়ারদের বড় সংখ্যা। ভুল হলে দ্রুত বদলায়।", "⚡"),
        recap("মনে রাখো", ["Shenzhen হার্ডওয়্যার, Hangzhou e-commerce।",
                            "Super app চীনের অভ্যাস।",
                            "Copycat থেকে innovator।",
                            "State support আর scale বড় সুবিধা।"]),
    ],
    quiz=[
        dict(q="WeChat কী ধরনের অ্যাপ?", o=["শুধু মেসেজ", "super app", "শুধু গেম", "শুধু সার্চ"], a=1,
             why="WeChat-এ মেসেজ, পেমেন্ট, টিকিট, সেবা — অনেক কাজ এক অ্যাপে।"),
        dict(q="Hangzhou কোন কোম্পানির জন্য পরিচিত?", o=["Huawei", "Alibaba", "Baidu", "DJI"], a=1,
             why="Alibaba-র সদর Hangzhou-এ; DeepSeek-ও সেখানেই।"),
    ],
),

chapter(
    "Tencent ও Alibaba",
    "Tencent and Alibaba",
    "চীনের দুই দৈত্য — একটা মেসেজ আর গেমে, আরেকটা শপিং আর পেমেন্টে।",
    [
        big("মূল ধারণা", "Tencent = মনোযোগ, Alibaba = বাণিজ্য",
            "Tencent মানুষকে সংযুক্ত রাখে, Alibaba কেনাকাটা সহজ করে। দুটোই পেমেন্ট আর cloud-এ ঢুকেছে।", "⚖️"),
        profile("WeChat-এর সাম্রাজ্য", "Tencent", "WeChat, games & cloud", "T",
                [("শুরু", "১৯৯৮"), ("প্রতিষ্ঠাতা", "Pony Ma (Ma Huateng) ও সহপ্রতিষ্ঠাতারা"), ("সদর", "Shenzhen"), ("কী বানায়", "WeChat, QQ, games, cloud")],
                "WeChat super-app আর বিশ্বের বড় গেম কোম্পানি",
                "Riot Games, Supercell-এর মালিক; Tencent Cloud-ও বড়।"),
        profile("WeChat-এর জনক", "Pony Ma", "Founder of Tencent", "P",
                [("জন্ম", "১৯৭১"), ("শুরু", "১৯৯৮, Tencent"), ("সদর", "Shenzhen"), ("ভূমিকা", "Chairman & CEO")],
                "Tencent-এর প্রতিষ্ঠাতা",
                "শান্ত স্বভাবের CEO; QQ থেকে WeChat পর্যন্ত পথ দেখিয়েছেন।"),
        big("WeChat কীভাবে টাকা কামায়?", "বিজ্ঞাপন, গেম, fintech (WeChat Pay), cloud, আর mini program। "
            "ব্যবহারকারীকে সরাসরি টাকা দিতে হয় না — ecosystem থেকে আয়।", "💳"),
        profile("চীনের e-commerce রাজা", "Alibaba", "E-commerce, payments & cloud", "A",
                [("শুরু", "১৯৯৯"), ("প্রতিষ্ঠাতা", "Jack Ma ও ১৭ জন সহপ্রতিষ্ঠাতা"), ("সদর", "Hangzhou"), ("কী বানায়", "Taobao, Tmall, Alipay, Alibaba Cloud")],
                "অনলাইন শপিং, পেমেন্ট আর cloud",
                "Taobao-র মাধ্যমে কোটি ছোট বিক্রেতা অনলাইনে এসেছে।"),
        profile("শিক্ষক থেকে উদ্যোক্তা", "Jack Ma", "Co-founder of Alibaba", "J",
                [("জন্ম", "১৯৬৪"), ("শুরু", "১৯৯৯, Alibaba"), ("আগে", "ইংরেজি শিক্ষক"), ("ভূমিকা", "co-founder")],
                "Alibaba-র সহপ্রতিষ্ঠাতা",
                "অনেক ব্যর্থতার পর আলিবাবা গড়েন; তাঁর গল্প উদ্যোক্তাদের অনুপ্রেরণা।"),
        terms("Alibaba-র চারটা অংশ", "Taobao, Tmall, Alipay, Alibaba Cloud", [
            ("Taobao", "C2C মার্কেটপ্লেস", "ছোট বিক্রেতা।"),
            ("Tmall", "ব্র্যান্ডের দোকান", "বড় কোম্পানি।"),
            ("Alipay", "পেমেন্ট", "Ant Group-এর অংশ।"),
            ("Alibaba Cloud", "cloud সেবা", "Aliyun নামেও পরিচিত।")]),
        flow("একটা অর্ডারের যাত্রা", [
            ("Browse", "Taobao-তে পণ্য খোঁজো।"),
            ("Pay", "Alipay-এ টাকা।"),
            ("Seller", "বিক্রেতা প্যাক করে।"),
            ("Delivery", "লজিস্টিকস পৌঁছায়।"),
            ("Review", "রিভিউ দাও।"),
        ]),
        big("Singles' Day", "১১ নভেম্বর Alibaba-র বড় বিক্রি উৎসব — এক দিনে বিলিয়ন ডলারের অর্ডার। "
            "এটা চীনের ভোক্তা শক্তির প্রদর্শনী।", "🛍️"),
        big("দুই দৈত্যের প্রতিযোগিতা", "Tencent-এর ecosystem বন্ধ, Alibaba-র খোলা marketplace। দুটোই একে অপরের "
            "জমিতে ঢুকেছে — পেমেন্ট, cloud, media, AI।", "🤝"),
        recap("মনে রাখো", ["Tencent WeChat, QQ, গেম।",
                            "Alibaba Taobao, Tmall, Alipay।",
                            "দুটোই cloud আর পেমেন্টে বড়।",
                            "Super app আর marketplace দুই মডেল।"]),
    ],
    quiz=[
        dict(q="WeChat কোন কোম্পানির?", o=["Alibaba", "Tencent", "Baidu", "ByteDance"], a=1,
             why="WeChat Tencent-এর; QQ-ও Tencent-এর।"),
        dict(q="Alipay কোন গ্রুপের?", o=["Ant Group", "Tencent", "Baidu", "Huawei"], a=0,
             why="Alipay Ant Group-এর অংশ, যেটা Alibaba ecosystem থেকে জন্মেছে।"),
    ],
),

chapter(
    "Baidu, ByteDance ও TikTok",
    "Baidu, ByteDance and TikTok",
    "চীনের সার্চ ইঞ্জিন আর বিশ্বের সবচেয়ে আসক্তিকর short-video অ্যাপ।",
    [
        big("মূল ধারণা", "Baidu তথ্য খোঁজে, ByteDance মনোযোগ ধরে",
            "Baidu search আর AI-তে, ByteDance recommendation algorithm দিয়ে মানুষকে ভিডিও দেখায়।", "🔎"),
        profile("চীনের সার্চ ইঞ্জিন", "Baidu", "Search, AI & self-driving", "B",
                [("শুরু", "২০০০"), ("প্রতিষ্ঠাতা", "Robin Li, Eric Xu"), ("সদর", "Beijing"), ("কী বানায়", "search, Apollo, ERNIE")],
                "চীনের search engine আর AI গবেষণা",
                "Baidu-কে ‘চীনের Google’ বলা হয়; self-driving Apollo আর ERNIE মডেলও বানায়।"),
        profile("সার্চের জনক", "Robin Li", "Co-founder of Baidu", "R",
                [("জন্ম", "১৯৬৮"), ("শুরু", "২০০০, Baidu"), ("সদর", "Beijing"), ("ভূমিকা", "CEO")],
                "Baidu-র সহপ্রতিষ্ঠাতা",
                "search algorithm নিয়ে গবেষণা করে Baidu গড়েন।"),
        profile("TikTok-এর ইঞ্জিন", "ByteDance", "TikTok, Douyin & Toutiao", "B",
                [("শুরু", "২০১২"), ("প্রতিষ্ঠাতা", "Zhang Yiming"), ("সদর", "Beijing"), ("কী বানায়", "TikTok, Douyin, Toutiao, CapCut")],
                "TikTok-এর recommendation algorithm",
                "TikTok আন্তর্জাতিক, Douyin চীনের ভেতরে — একই ধরনের short video।"),
        profile("algorithm-এর কারিগর", "Zhang Yiming", "Founder of ByteDance", "Z",
                [("জন্ম", "১৯৮৩"), ("শুরু", "২০১২, ByteDance"), ("সদর", "Beijing"), ("ভূমিকা", "founder")],
                "ByteDance-এর প্রতিষ্ঠাতা",
                "Toutiao দিয়ে শুরু, তারপর Douyin/TikTok-এ recommendation-কে বিশ্বস্ত করে তোলেন।"),
        big("Recommendation algorithm = তোমার জন্য মেশিন", "তুমি কী দেখো, কতক্ষণ দেখো, কী স্কিপ করো — এসব থেকে মডেল শেখে "
            "পরের ভিডিও কী হবে। এটাই TikTok-এর আসল শক্তি।", "🎯"),
        terms("চারটা শব্দ", "feed, engagement, algorithm, moderation", [
            ("Feed", "ভিডিওর ধারা", "অসীম scroll।"),
            ("Engagement", "দেখা, লাইক, শেয়ার", "algorithm-এর জ্বালানি।"),
            ("Algorithm", "কী দেখাবে ঠিক করে", "ব্যক্তিগত feed।"),
            ("Moderation", "কনটেন্ট যাচাই", "নিয়ম ভাঙা ভিডিও সরানো।")]),
        flow("TikTok-এর যাত্রা", [
            ("২০১৬", "Douyin চীনে।"),
            ("২০১৭", "TikTok আন্তর্জাতিক।"),
            ("২০১৮", "Musical.ly merge।"),
            ("২০২০s", "বিশ্বজুড়ে বিলিয়ন ব্যবহারকারী।"),
        ]),
        big("TikTok বিতর্ক", "ডেটা কোথায় যায়, কে নিয়ন্ত্রণ করে, তরুণদের ওপর প্রভাব — এসব নিয়ে নানা দেশে আলোচনা ও নিষেধাজ্ঞা। "
            "প্রযুক্তি আর রাজনীতি এখানে জড়িয়ে।", "🌐"),
        big("CapCut-ও ByteDance", "ভিডিও এডিটিং অ্যাপ CapCut-ও ByteDance-এর। Content বানানো সহজ করায় TikTok ecosystem "
            "আরও শক্তিশালী হয়েছে।", "✂️"),
        recap("মনে রাখো", ["Baidu search আর AI।",
                            "ByteDance TikTok/Douyin-এর মালিক।",
                            "Recommendation algorithm আসল শক্তি।",
                            "TikTok নিয়ে রাজনৈতিক বিতর্ক আছে।"]),
    ],
    quiz=[
        dict(q="TikTok কোন কোম্পানির?", o=["Tencent", "Alibaba", "ByteDance", "Baidu"], a=2,
             why="TikTok ByteDance-এর আন্তর্জাতিক অ্যাপ; চীনে Douyin নামে চলে।"),
        dict(q="TikTok-এর মূল শক্তি কী?", o=["হার্ডওয়্যার", "recommendation algorithm", "ডেটাবেস", "ক্যামেরা"], a=1,
             why="ব্যবহারকারীর আচরণ থেকে শিখে পরের ভিডিও বাছাই করার algorithm TikTok-এর মূল শক্তি।"),
    ],
),

chapter(
    "DeepSeek: কম খরচে বড় AI",
    "DeepSeek: big AI at low cost",
    "২০২৫ সালের শুরুতে একটা চীনা AI মডেল বিশ্বকে হতবাক করল। গল্পটা বুঝবে।",
    [
        big("মূল ধারণা", "DeepSeek = open-weight reasoning মডেল",
            "কম খরচে শক্তিশালী মডেল বানিয়ে দেখিয়েছে — বড় AI শুধু বিশাল কোম্পানির একচেটিয়া নয়।", "🐋"),
        profile("চীনা AI ল্যাব", "DeepSeek", "Chinese AI lab · open weights", "D",
                [("শুরু", "২০২৩"), ("প্রতিষ্ঠাতা", "Liang Wenfeng"), ("সদর", "Hangzhou"), ("কী বানায়", "DeepSeek-V3, R1")],
                "কম খরচে শক্তিশালী reasoning, open weights",
                "মডেলের ওজন খোলা, তাই অনেকে নিজের সার্ভারে চালাতে পারে।"),
        profile("কোয়ান্ট ফান্ড থেকে AI", "Liang Wenfeng", "Founder of DeepSeek", "L",
                [("শুরু", "High-Flyer quant fund"), ("তারপর", "২০২৩, DeepSeek"), ("সদর", "Hangzhou"), ("ভূমিকা", "founder")],
                "DeepSeek-এর প্রতিষ্ঠাতা",
                "ট্রেডিংয়ের জন্য কম্পিউট বানাতে গিয়ে AI-তে ঢোকেন; খরচে কড়া নজর।"),
        timeline("DeepSeek-এর পথ", [
            ("২০২৩", "DeepSeek শুরু।"),
            ("২০২৪", "DeepSeek-V3 — শক্তিশালী open-weight মডেল।"),
            ("জানু ২০২৫", "R1 reasoning মডেল, বিশ্বজুড়ে আলোচনা।"),
            ("২০২৫", "অ্যাপ জনপ্রিয়, অনেক কোম্পানি নিজে হোস্ট করে।"),
        ]),
        terms("চারটা শব্দ", "reasoning, open weight, distillation, MoE", [
            ("Reasoning", "ধাপে ধাপে ভাবা", "গণিত, কোড, যুক্তি।"),
            ("Open weight", "মডেলের ওজন খোলা", "নিজে চালানো যায়।"),
            ("Distillation", "বড় মডেল থেকে ছোট মডেল শেখানো", "খরচ কম।"),
            ("MoE", "Mixture of Experts", "সব অংশ একসাথে চালায় না।")]),
        big("কেন এত আলোচনা?", "দাবি করা হয় কম খরচে training হয়েছে, অথচ ফল প্রতিযোগিতামূলক। বাজার ভয় পায় — GPU-র চাহিদা কমবে? "
            "আসলে চাহিদা আরও বাড়ে।", "📉"),
        big("Open weight-এর মানে", "মডেলের parameter ফাইল নামানো যায়, নিজের সার্ভারে চালানো যায়। কিন্তু training data, "
            "কোড, বা সব গবেষণা খোলা — এমন নয়।", "📂"),
        big("DeepSeek-এর সীমা", "কম খরচের দাবি নিয়ে বিতর্ক আছে; model hallucinate করে, নীতিগত সীমা আছে, "
            "আর চীনা নিয়ন্ত্রণের প্রভাবও থাকে।", "⚖️"),
        points("DeepSeek থেকে শেখা", "প্রযুক্তি আর ব্যবসার পাঠ", [
            "খরচ কমানো একটা innovation।",
            "Open weight দিয়ে ecosystem দ্রুত বাড়ে।",
            "Reasoning মডেল আলাদা দক্ষতা।",
            "ভূ-রাজনীতি প্রযুক্তিকে প্রভাবিত করে।"]),
        recap("মনে রাখো", ["DeepSeek ২০২৩, Liang Wenfeng।",
                            "V3/R1 open-weight মডেল।",
                            "কম খরচে শক্তিশালী — আলোচনার কেন্দ্র।",
                            "Open weight মানে ওজন নামানো যায়।"]),
    ],
    quiz=[
        dict(q="DeepSeek কী ধরনের মডেল দেয়?", o=["শুধু ছবি", "open-weight ভাষার মডেল", "ডেটাবেস", "অপারেটিং সিস্টেম"], a=1,
             why="DeepSeek-V3/R1 ভাষার মডেল, open weights — নিজের সার্ভারে চালানো যায়।"),
        dict(q="DeepSeek-এর প্রতিষ্ঠাতা কে?", o=["Robin Li", "Liang Wenfeng", "Pony Ma", "Zhang Yiming"], a=1,
             why="Liang Wenfeng High-Flyer quant fund থেকে DeepSeek শুরু করেন।"),
    ],
),

chapter(
    "Kimi, Moonshot ও AI স্টার্টআপ",
    "Kimi, Moonshot and the AI startups",
    "DeepSeek ছাড়াও চীনে Qwen, Kimi, GLM, MiniMax — প্রত্যেকে নিজের শক্তি নিয়ে আসছে।",
    [
        big("মূল ধারণা", "চীনা AI = এক মডেল নয়, একটা ঝাঁক",
            "Alibaba-র Qwen, Moonshot-এর Kimi, Zhipu-র GLM, MiniMax, Baichuan — প্রত্যেকে আলাদা ফোকাস।", "🐝"),
        profile("Kimi-র বাড়ি", "Moonshot AI", "Chinese AI lab · Kimi", "K",
                [("শুরু", "২০২৩"), ("প্রতিষ্ঠাতা", "Yang Zhilin"), ("সদর", "Beijing"), ("কী বানায়", "Kimi, K2")],
                "Kimi — লম্বা লেখা পড়তে পারে, K2 open-weight",
                "Kimi দীর্ঘ ডকুমেন্ট সারসংক্ষেপ, গবেষণা, পড়াশোনায় সাহায্য করে।"),
        profile("Kimi-র জনক", "Yang Zhilin", "Founder of Moonshot AI", "Y",
                [("শুরু", "২০২৩, Moonshot"), ("আগে", "Google Brain, Meta AI"), ("সদর", "Beijing"), ("ভূমিকা", "CEO")],
                "Moonshot AI-এর প্রতিষ্ঠাতা",
                "বড় ভাষার মডেল নিয়ে গবেষণা করে Kimi বানান; long context-এ জোর।"),
        big("Kimi-র শক্তি: long context", "একটা বই, অনেক পেজের রিপোর্ট, বা লম্বা কোড একবারে পড়তে পারে। "
            "তাই ‘এই ডকুমেন্ট সারসংক্ষেপ করো’ ধরনের কাজে সুবিধা।", "📚"),
        terms("চারটা চীনা ল্যাব", "Qwen, GLM, MiniMax, Baichuan", [
            ("Qwen", "Alibaba-র মডেল", "open-weight সংস্করণও আছে।"),
            ("GLM", "Zhipu AI-র মডেল", "চীনা ভাষায় শক্তিশালী।"),
            ("MiniMax", "অডিও/ভিডিও AI", "Hailuo ভিডিও।"),
            ("Baichuan", "আরেকটা স্টার্টআপ", "চীনা ভাষার মডেল।")]),
        big("K2: open-weight বড় মডেল", "Moonshot-এর Kimi K2 (২০২৫) বিশাল MoE মডেল, open weight। "
            "অনেকে নিজের সার্ভারে চালিয়ে পরীক্ষা করে।", "🧪"),
        compare("চীনা AI ল্যাবের কৌশল",
                ("Open weight", ["DeepSeek, Qwen, Kimi K2", "দ্রুত ছড়ায়", "নিজে হোস্ট করা যায়"]),
                ("Closed / API", ["Baichuan, কিছু Qwen", "নিয়ন্ত্রণ বেশি", "API-তে টাকা"]),
                "চীনা ল্যাবগুলো open weight-কে বাজার দখলের অস্ত্র বানিয়েছে।"),
        big("মার্কিন-চীনা প্রতিযোগিতা", "America-র GPU নিষেধাজ্ঞা, China-র নিজের চিপ (Huawei Ascend), "
            "open-weight মডেল — AI এখন প্রযুক্তি ও ভূ-রাজনীতির কেন্দ্রে।", "🌐"),
        points("AI স্টার্টআপের চারটা পাঠ", "যেকোনো দেশে কাজে লাগে", [
            "একটা স্পষ্ট শক্তি বাছো (long context, reasoning)।",
            "Open weight দিয়ে community বানাও।",
            "খরচ কমানোয় innovate করো।",
            "ভাষা আর স্থানীয় বাজার বোঝো।"]),
        recap("মনে রাখো", ["Moonshot Kimi, long context-এ শক্তিশালী।",
                            "Qwen Alibaba, GLM Zhipu, MiniMax।",
                            "K2 open-weight MoE।",
                            "Open weight চীনা AI-র বড় কৌশল।"]),
    ],
    quiz=[
        dict(q="Kimi কোন কোম্পানির?", o=["Moonshot AI", "DeepSeek", "Alibaba", "Baidu"], a=0,
             why="Kimi Moonshot AI-এর; প্রতিষ্ঠাতা Yang Zhilin।"),
        dict(q="Kimi-র বড় শক্তি কী?", o=["ছবি আঁকা", "long context", "ডেটাবেস", "গেম"], a=1,
             why="Kimi লম্বা ডকুমেন্ট একবারে পড়তে পারে — long context।"),
    ],
),

chapter(
    "হার্ডওয়্যার ও ইভি: Huawei, Xiaomi, DJI, BYD",
    "Hardware and EVs: Huawei, Xiaomi, DJI, BYD",
    "চীন শুধু অ্যাপ নয় — ফোন, চিপ, ড্রোন, গাড়িও বানায়।",
    [
        big("মূল ধারণা", "চীনের আসল শক্তি: সফটওয়্যার + কারখানা",
            "একই দেশে ডিজাইন, chip, manufacturing, supply chain — তাই দ্রুত prototype আর কম দামে পণ্য।", "🏭"),
        profile("টেলিকম থেকে চিপ", "Huawei", "Telecom, phones & chips", "H",
                [("শুরু", "১৯৮৭"), ("প্রতিষ্ঠাতা", "Ren Zhengfei"), ("সদর", "Shenzhen"), ("কী বানায়", "5G, phones, HarmonyOS, Ascend")],
                "5G, ফোন আর নিজের AI চিপ",
                "২০১৯ সালের মার্কিন নিষেধাজ্ঞার পর নিজের চিপ আর OS-এ বিনিয়োগ বাড়ায়।"),
        profile("ফোন থেকে ইভি", "Xiaomi", "Phones, IoT & EVs", "X",
                [("শুরু", "২০১০"), ("প্রতিষ্ঠাতা", "Lei Jun"), ("সদর", "Beijing"), ("কী বানায়", "phones, IoT, SU7 EV")],
                "সস্তা ফোন থেকে ইলেকট্রিক গাড়ি",
                "IoT ecosystem আর ২০২৪ সালে SU7 EV দিয়ে অটো বাজারে ঢোকে।"),
        profile("ড্রোনের রাজা", "DJI", "Drones & cameras", "D",
                [("শুরু", "২০০৬"), ("প্রতিষ্ঠাতা", "Frank Wang"), ("সদর", "Shenzhen"), ("কী বানায়", "drones, gimbals, cameras")],
                "বিশ্বের বড় drone কোম্পানি",
                "ফটোগ্রাফি, কৃষি, সিনেমা — সবখানে DJI drone।"),
        profile("ইভি ও ব্যাটারি", "BYD", "EVs & batteries", "B",
                [("শুরু", "১৯৯৫"), ("প্রতিষ্ঠাতা", "Wang Chuanfu"), ("সদর", "Shenzhen"), ("কী বানায়", "EVs, batteries, Blade Battery")],
                "বিশ্বের বড় EV নির্মাতা",
                "ব্যাটারি থেকে গাড়ি — উল্লম্ব integration-এ খরচ কমায়।"),
        terms("চারটা শব্দ", "supply chain, sanctions, HarmonyOS, EV", [
            ("Supply chain", "পণ্যের সরবরাহ জাল", "চীনে ঘন।"),
            ("Sanctions", "নিষেধাজ্ঞা", "চিপ/প্রযুক্তি রপ্তানি সীমা।"),
            ("HarmonyOS", "Huawei-র OS", "Android-এর বিকল্প।"),
            ("EV", "ইলেকট্রিক গাড়ি", "ব্যাটারি + সফটওয়্যার।")]),
        big("নিষেধাজ্ঞা = বাধা, কিন্তু বিনিয়োগও", "Huawei-র ফোন বাজার হারায়, কিন্তু নিজের চিপ (Ascend) আর OS-এ "
            "বিনিয়োগ বাড়ায়। চাপ কখনো innovation ত্বরান্বিত করে।", "🚧"),
        big("EV = চলন্ত কম্পিউটার", "আজকের গাড়ি ১০ কোটি লাইন কোড চালাতে পারে, OTA update পায়, আর ডেটা পাঠায়। "
            "BYD ব্যাটারি-কেমিস্ট্রিতে, Xiaomi সফটওয়্যার-ইকোসিস্টেমে শক্ত।", "🚗"),
        points("চীন থেকে শেখা", "কপি নয়, বোঝা", [
            "Supply chain এক জায়গায় থাকলে দ্রুত বদলানো যায়।",
            "হার্ডওয়্যার + সফটওয়্যার একসাথে ভাবো।",
            "Open weight দিয়ে ecosystem বানাও।",
            "দীর্ঘমেয়াদি বিনিয়োগ ধৈর্য চায়।"]),
        recap("মনে রাখো", ["Huawei টেলিকম, চিপ, HarmonyOS।",
                            "Xiaomi ফোন, IoT, EV।",
                            "DJI drone, BYD EV/ব্যাটারি।",
                            "Supply chain + নিষেধাজ্ঞা দুইই প্রভাব ফেলে।"]),
    ],
    quiz=[
        dict(q="DJI কী বানায়?", o=["গাড়ি", "ড্রোন", "ডেটাবেস", "ফোন"], a=1,
             why="DJI drone, gimbal আর ক্যামেরার জন্য বিখ্যাত।"),
        dict(q="BYD কী জন্য বিখ্যাত?", o=["সার্চ", "EV আর ব্যাটারি", "গেম", "cloud"], a=1,
             why="BYD ইলেকট্রিক গাড়ি আর ব্যাটারি বানায়; Blade Battery তাদের প্রযুক্তি।"),
    ],
),

]

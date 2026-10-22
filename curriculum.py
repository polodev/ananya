"""Course outlines: which chapters exist, their topic and grammar focus. Hand-written; the chapter content itself
(content/<course>/ch-NN.json) is generated from these outlines by tools/gen_content.py (muse) and then reviewed.

kind = "letters" chapters are built from hand-written data (letters_ja.py, letters_de.py), never generated."""

LANGS = {
    "english": dict(name="English", bn="ইংরেজি", badge="A", theme="en", tts="en-US",
                    intro="অক্ষর আর সংখ্যা তো জানাই — এবার A2 থেকে B2: কথা বলা, পড়া আর ব্যাকরণ, ধাপে ধাপে।"),
    "japanese": dict(name="Japanese", bn="জাপানি", badge="あ", theme="ja", tts="ja-JP",
                     intro="একদম শুরু থেকে: হিরাগানা, কাতাকানা, সংখ্যা — তারপর A1 স্তরের রোজকার কথা।"),
    "german": dict(name="German", bn="জার্মান", badge="Ä", theme="de", tts="de-DE",
                   intro="একদম শুরু থেকে: অক্ষর, উচ্চারণের নিয়ম, সংখ্যা — তারপর A1 স্তরের রোজকার কথা।"),
}


def ch(title_bn, topic, grammar, kind="topic"):
    return dict(title_bn=title_bn, topic=topic, grammar=grammar, kind=kind)


def bch(level, title_bn, focus):
    """a Sentence Builder chapter: 10 builders, each grows one sentence in 3-5 steps."""
    return dict(title_bn=title_bn, topic=focus, grammar=focus, kind="builder", level=level)


COURSES = {
    # ------------------------------------------------------------------ English
    "english/a2": dict(lang="english", level="A2", title="English A2", tag="রোজকার ইংরেজি",
                       sub="প্রতিদিনের কথাবার্তা, সহজ গল্প, মূল ব্যাকরণ",
                       lead="বাজার, ডাক্তার, রাস্তা, ফোন — রোজকার জীবনের ইংরেজি। প্রতিটি অধ্যায়ে একটা ছোট কথোপকথন, ১০টি শব্দ, ১২টি বাক্য আর একটা ব্যাকরণ।",
                       chapters=[
                           ch("আমার প্রতিদিনের রুটিন", "Daily routine: waking up, work, meals, evening", "Present simple with adverbs of frequency (always, usually, sometimes, never)"),
                           ch("বাজারে কেনাকাটা", "Shopping at a local market in Bangladesh: vegetables, fish, prices", "Countable and uncountable nouns; some / any; How much / How many"),
                           ch("গত সপ্তাহান্ত", "Talking about last weekend: visiting relatives, a trip to the river", "Past simple: regular and common irregular verbs, questions with did"),
                           ch("ফার্মেসিতে", "At the pharmacy and with a doctor: common illnesses and medicine", "should / shouldn't for advice"),
                           ch("পথ খোঁজা", "Asking for and giving directions in town; rickshaw, bus, train", "Prepositions of place (next to, opposite, between) and imperatives"),
                           ch("রেস্টুরেন্টে খাওয়া", "Ordering food in a restaurant, paying the bill", "would like / Can I have ...? / Could I ...? polite requests"),
                           ch("ভবিষ্যতের পরিকল্পনা", "Plans for next month: a wedding, a new course, saving money", "going to vs will"),
                           ch("তুলনা করা", "Comparing phones, cities and shops", "Comparative and superlative adjectives"),
                           ch("ফোনে কথা বলা", "Phone calls: calling a friend, a shop, leaving a message", "Present continuous for now and for arrangements"),
                           ch("অভিজ্ঞতা", "Life experiences: travel, food, new things tried", "Present perfect with ever / never"),
                           ch("আবহাওয়া ও ঋতু", "Weather and the six seasons of Bangladesh, monsoon", "It is + adjective; adverbs of manner (quickly, heavily)"),
                           ch("কাজ ও পেশা", "Jobs, skills, a first job interview", "can / can't for ability; have to / don't have to"),
                       ]),
    "english/b1": dict(lang="english", level="B1", title="English B1", tag="আত্মবিশ্বাসী ইংরেজি",
                       sub="মত দেওয়া, ঘটনা বলা, কাজের ইংরেজি",
                       lead="নিজের মত বলা, অভিজ্ঞতা গুছিয়ে বলা, ইমেইল লেখা — মাঝারি স্তরের ইংরেজি। প্রতিটি অধ্যায়ে একটা কথোপকথন বা লেখা, ১০টি শব্দ, ১২টি বাক্য আর একটা ব্যাকরণ।",
                       chapters=[
                           ch("চাকরির ইন্টারভিউ", "A job interview: talking about experience and achievements", "Present perfect vs past simple"),
                           ch("ভ্রমণের গল্প", "Telling a travel story: a trip to Sylhet, something went wrong", "Past continuous vs past simple (while / when)"),
                           ch("প্রযুক্তি ও মোবাইল", "Smartphones, apps, online safety", "First conditional (If + present, will)"),
                           ch("স্বাস্থ্য ও জীবনযাপন", "Healthy habits then and now", "used to / would for past habits"),
                           ch("পরিবেশ", "Pollution, plastic, floods and what is being done", "Passive voice: present and past simple"),
                           ch("অফিসের ইমেইল", "Work emails and polite requests to a manager or client", "Polite requests and offers: Could you ...? Would you mind ...? I was wondering if ..."),
                           ch("মানুষ ও সম্পর্ক", "Describing friends, neighbours and colleagues", "Defining relative clauses (who, which, that, where)"),
                           ch("টাকা ও অনলাইন কেনাকাটা", "Online shopping, mobile banking, saving", "Second conditional (If + past, would)"),
                           ch("পড়াশোনা ও শেখা", "Learning a language, studying for exams, study habits", "Gerund vs infinitive (enjoy doing, decide to do)"),
                           ch("খবর ও ঘটনা", "Talking about news: what people said", "Reported speech (said that, told me that, asked if)"),
                           ch("সমস্যা ও অভিযোগ", "Solving problems: a broken product, a late delivery", "Modals of deduction: must, might, can't"),
                           ch("স্বপ্ন ও লক্ষ্য", "Future goals and plans in five years", "Future forms: will, going to, present continuous, future continuous"),
                       ]),
    "english/b2": dict(lang="english", level="B2", title="English B2", tag="সাবলীল ইংরেজি",
                       sub="যুক্তি দেওয়া, আলোচনা, সূক্ষ্ম ব্যাকরণ",
                       lead="তর্ক-বিতর্ক, নিজের যুক্তি, পেশাগত আলোচনা — উচ্চ-মাঝারি স্তরের ইংরেজি। প্রতিটি অধ্যায়ে একটা লেখা, ১০টি শব্দ, ১২টি বাক্য আর একটা ব্যাকরণ।",
                       chapters=[
                           ch("প্রথম দেখার ছাপ", "First impressions at work and in life", "Present perfect continuous vs present perfect simple"),
                           ch("কাজ ও জীবনের ভারসাম্য", "Work-life balance and regrets", "Third conditional"),
                           ch("প্রযুক্তি ও সমাজ", "How technology changes society; services we use", "Advanced passive and causative (have / get something done)"),
                           ch("স্বাস্থ্য নিয়ে ভুল ধারণা", "Common health myths and evidence", "Mixed conditionals"),
                           ch("শহর ও অভিবাসন", "Moving from a village to Dhaka or abroad", "wish / if only (present and past)"),
                           ch("গণমাধ্যম ও ভুয়া খবর", "Media, social media and fake news", "Reporting verbs (claim, deny, suggest, warn, admit)"),
                           ch("ব্যবসা ও উদ্যোগ", "Starting a small business, a pharmacy or an online shop", "Future perfect and future continuous"),
                           ch("জলবায়ু পরিবর্তন", "Climate change and Bangladesh", "Contrast linkers: although, despite, in spite of, whereas, however"),
                           ch("শিক্ষা নিয়ে বিতর্ক", "Exams vs skills: a debate about education", "Cleft sentences for emphasis (What I need is ..., It was ... that ...)"),
                           ch("সংস্কৃতি ও ঐতিহ্য", "Festivals, food and traditions: Pohela Boishakh, Eid, Durga Puja", "Participle clauses (Having finished ..., Walking home, ...)"),
                           ch("আলোচনা ও দর-কষাকষি", "Negotiating salary, prices and agreements", "Modal perfects: should have, could have, must have, might have"),
                           ch("লক্ষ্য ও পরিবর্তন", "Ambition, habits and personal change", "Phrasal verbs and collocations (give up, take up, carry on, make progress)"),
                       ]),
    "english/builder": dict(lang="english", level="A1–C2", title="Sentence Builder", tag="ছোট বাক্য থেকে বড় বাক্য",
                            sub="একটা ছোট বাক্যে ধাপে ধাপে শব্দ যোগ করে বড় বাক্য বানানো",
                            lead="I like tea → I like tea with milk → I like drinking tea with milk every morning. প্রতিটি অধ্যায়ে ১০টি বাক্য-নির্মাণ, প্রতিটিতে ৩–৫ ধাপ; প্রতি ধাপে নতুন অংশটা সবুজ। A1 থেকে C2 পর্যন্ত।",
                            chapters=[
                                bch("A1", "কে কী করে", "subject + verb + object; add an object or an adjective"),
                                bch("A1", "কোথায় আর কখন", "add place (at home, in Dhaka) and time (every day, at night)"),
                                bch("A1", "and আর but দিয়ে জোড়া", "join two short ideas with and / but; add adjectives"),
                                bch("A2", "কত ঘন ঘন", "adverbs of frequency and time phrases (always, twice a week, on Fridays)"),
                                bch("A2", "গতকালের গল্প", "past simple; add when, where, with whom"),
                                bch("A2", "কারণ আর ফল", "because / so / to (purpose)"),
                                bch("B1", "অভিজ্ঞতা", "present perfect with for / since / ever / already / yet"),
                                bch("B1", "who, which, that দিয়ে বর্ণনা", "relative clauses that add detail to a noun"),
                                bch("B1", "যদি…", "first and second conditionals (if + result)"),
                                bch("B1", "কাজের উদ্দেশ্য আর পছন্দ", "gerunds and infinitives (enjoy doing, decide to do, in order to)"),
                                bch("B2", "কাজটা করা হয়", "passive voice with agent, time and place"),
                                bch("B2", "বৈপরীত্য", "although / despite / whereas / however"),
                                bch("B2", "কে কী বলল", "reported speech and reporting verbs (claimed, suggested, warned)"),
                                bch("B2", "এক বাক্যে দুই কাজ", "participle clauses (Having finished…, Walking home…)"),
                                bch("C1", "বিশেষ্যকে সমৃদ্ধ করা", "long noun phrases and nominalisation (pre- and post-modifiers)"),
                                bch("C1", "জোর দেওয়া", "inversion for emphasis (Not only…, Rarely…, Hardly…when)"),
                                bch("C1", "যা দরকার তা হলো…", "cleft sentences and fronting (What I need is…, It was… that…)"),
                                bch("C2", "সতর্ক ও সূক্ষ্ম কথা", "hedging and stance (arguably, tends to, it would appear that)"),
                                bch("C2", "জটিল শর্ত", "mixed conditionals and formal inversion (Had I known…, Were it not for…, Should you…)"),
                                bch("C2", "পেশাদার লম্বা বাক্য", "combining clauses into one precise professional or academic sentence"),
                            ]),
    # ------------------------------------------------------------------ Japanese
    "japanese/a1": dict(lang="japanese", level="A1", title="Japanese A1", tag="শূন্য থেকে জাপানি",
                        sub="হিরাগানা, কাতাকানা, সংখ্যা, তারপর রোজকার কথা",
                        lead="প্রথমে অক্ষর আর সংখ্যা (৭ অধ্যায়), তারপর ১২টি অধ্যায়ে A1 স্তরের কথা: পরিচয়, কেনাকাটা, সময়, খাবার, পরিবার। সব জাপানি লেখার সাথে বাংলায় উচ্চারণ।",
                        chapters=[
                            ch("হিরাগানা ১: あ か さ", "", "", "letters"),
                            ch("হিরাগানা ২: た な は", "", "", "letters"),
                            ch("হিরাগানা ৩: ま や ら わ ん", "", "", "letters"),
                            ch("হিরাগানা ৪: ゛ ゜ আর ছোট অক্ষর", "", "", "letters"),
                            ch("কাতাকানা ১: ア থেকে ノ", "", "", "letters"),
                            ch("কাতাকানা ২: ハ থেকে ン, লম্বা টান", "", "", "letters"),
                            ch("সংখ্যা: ১ থেকে ১০,০০০", "", "", "letters"),
                            ch("পরিচয় দেওয়া", "Greetings and introducing yourself: name, country, job", "X は Y です / じゃ ありません / ですか"),
                            ch("এটা, ওটা", "Things around you: これ それ あれ, whose is it", "これ・それ・あれ and の (possession)"),
                            ch("দোকানে কেনাকাটা", "Buying things in a shop, asking the price in yen", "いくら ですか / を ください / numbers with えん"),
                            ch("সময় ও দিনের রুটিন", "Telling the time and daily routine", "〜じ / 〜ふん, verbs in ます form, に for time"),
                            ch("কোথাও যাওয়া", "Going places: station, school, home; by train or bus", "へ / に いきます, で for transport, から・まで"),
                            ch("খাবার ও পানীয়", "Eating and drinking (tea, water, juice, rice, fish, vegetables only)", "を たべます / のみます, 〜ませんか invitation"),
                            ch("পরিবার", "Talking about family members", "います / あります; counting people (ひとり, ふたり)"),
                            ch("বর্ণনা করা", "Describing things and places: big, small, hot, quiet", "い-adjectives and な-adjectives"),
                            ch("পছন্দ ও শখ", "Likes, dislikes and hobbies", "が すき です / が じょうず です"),
                            ch("গতকাল কী করলে", "What you did yesterday and last week", "Past: 〜ました / 〜ませんでした"),
                            ch("কোথায় আছে", "Asking where things are; in the town and in the room", "どこ ですか / に あります; うえ・した・となり"),
                            ch("অনুরোধ ও শরীর খারাপ", "Asking for help, at the pharmacy, feeling sick", "〜て ください; が いたい です"),
                        ]),
    # ------------------------------------------------------------------ German
    "german/a1": dict(lang="german", level="A1", title="German A1", tag="শূন্য থেকে জার্মান",
                      sub="অক্ষর, উচ্চারণ, সংখ্যা, তারপর রোজকার কথা",
                      lead="প্রথমে অক্ষর, উচ্চারণের নিয়ম আর সংখ্যা (৩ অধ্যায়), তারপর ১২টি অধ্যায়ে A1 স্তরের কথা। সব জার্মান বাক্যের সাথে বাংলায় উচ্চারণ।",
                      chapters=[
                          ch("জার্মান বর্ণমালা: A থেকে Z, Ä Ö Ü ß", "", "", "letters"),
                          ch("উচ্চারণের নিয়ম: ei, ie, sch, ch", "", "", "letters"),
                          ch("সংখ্যা: ০ থেকে ১০০০", "", "", "letters"),
                          ch("হ্যালো! পরিচয়", "Greetings and introducing yourself: name, how are you", "sein and heißen; W-questions (Wie? Wer?)"),
                          ch("কোথা থেকে এসেছ?", "Countries, languages, where you live", "Present tense of regular verbs (kommen, wohnen, sprechen)"),
                          ch("আমার পরিবার", "Family members, age, marital status", "haben; possessive mein / dein / sein / ihr"),
                          ch("খাবার ও পানীয়", "Food and drinks (tea, coffee, water, juice, bread, rice, chicken, fish only)", "Articles der / die / das and ein / eine; ich möchte"),
                          ch("কেনাকাটা", "Shopping in a supermarket, prices in euro", "Accusative: einen / eine / ein; Wie viel kostet ...?"),
                          ch("সময় ও দিনের রুটিন", "Time, days of the week, daily routine", "Separable verbs (aufstehen, einkaufen); time with um"),
                          ch("আমার বাসা", "Flat and rooms, furniture", "es gibt; adjectives after sein; kein / keine"),
                          ch("শহরে পথ খোঁজা", "Asking the way, places in town, transport", "Wo ist ...? Dative after in / an / neben (im, am); imperative Sie"),
                          ch("অবসর ও শখ", "Free time and hobbies", "gern / nicht gern; modal verb können"),
                          ch("ডাক্তারের কাছে", "At the doctor: body parts, pain, medicine", "müssen; imperative; Mein Kopf tut weh"),
                          ch("আবহাওয়া ও পোশাক", "Weather and clothes", "Es ist kalt / warm; es regnet; adjectives"),
                          ch("সপ্তাহান্তে কী করলে", "Talking about the weekend in the past", "Perfekt with haben and sein (intro)"),
                      ]),
}

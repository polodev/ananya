"""Technology 1001: build, ship and keep learning — Linux, Git, hosting, WordPress, business, security."""
from .slidekit import *

CHAPTERS = [

chapter(
    "Linux ও টার্মিনাল",
    "Linux and the terminal",
    "সার্ভারের জগতে Linux রাজা। আজ কমান্ড লাইনে হাঁটতে শিখবে।",
    [
        big("মূল ধারণা", "টার্মিনাল = কম্পিউটারের সাথে লেখা দিয়ে কথা",
            "মাউসে ক্লিক না করে কমান্ড লিখে ফাইল, ফোল্ডার, প্রোগ্রাম চালাও। সার্ভারে মাউস নেই, তাই এটা জানা লাগে।", "⌨️"),
        big("সার্ভারে Linux কেন?", "ফ্রি, হালকা, স্থিতিশীল, নিরাপদ, আর স্ক্রিপ্ট করা সহজ। Android-এর ভেতরেও Linux, "
            "AWS-এর বেশিরভাগ সার্ভার Linux।", "🐧"),
        terms("চারটা মৌলিক কমান্ড", "pwd, ls, cd, cat", [
            ("pwd", "আমি কোথায়", "বর্তমান ফোল্ডার দেখায়।"),
            ("ls", "কী আছে", "ফাইল-ফোল্ডার তালিকা।"),
            ("cd", "ফোল্ডার বদলাও", "`cd projects`।"),
            ("cat", "ফাইল দেখাও", "`cat notes.txt`।")]),
        code("প্রথম টার্মিনাল সেশন", "ফোল্ডার ঘোরা",
             "pwd\nls\nmkdir my-site\ncd my-site\nls -la",
             "bash", "", "`mkdir` নতুন ফোল্ডার, `-la` লুকানো ফাইলসহ দেখায়।"),
        terms("ফাইল সামলানোর চারটা কমান্ড", "cp, mv, rm, touch", [
            ("cp", "কপি", "`cp a.txt b.txt`।"),
            ("mv", "সরানো/নাম বদল", "`mv old.txt new.txt`।"),
            ("rm", "মুছে ফেলা", "`rm file.txt` — সাবধান!"),
            ("touch", "খালি ফাইল", "`touch index.html`।")]),
        big("rm -rf = বড় বিপদ", "`rm -rf folder` পুরো ফোল্ডার চিরতরে মুছে দেয়, recycle bin নেই। কমান্ড চালানোর আগে "
            "পথটা দুবার পড়ো।", "☠️"),
        terms("অনুমতির চারটা শব্দ", "user, group, chmod, sudo", [
            ("User", "তুমি কে", "নিজের ফাইল।"),
            ("Group", "একদল ব্যবহারকারী", "টিম অ্যাক্সেস।"),
            ("chmod", "অনুমতি বদল", "read/write/execute।"),
            ("sudo", "admin ক্ষমতা", "সাবধানে ব্যবহার করো।")]),
        code("SSH দিয়ে সার্ভারে ঢোকা", "দূরের কম্পিউটার",
             "ssh root@203.0.113.10\n# তারপর সার্ভারে:\napt update\napt install nginx",
             "bash", "", "SSH দিয়ে দূরের Linux সার্ভারে লগইন করা যায়।"),
        big("Package manager = অ্যাপ স্টোর", "Ubuntu/Debian-এ `apt`, CentOS/RHEL-এ `dnf`, macOS-এ `brew`। "
            "কমান্ড দিয়েই সফটওয়্যার ইনস্টল, আপডেট, রিমুভ।", "📦"),
        points("নতুনদের চারটা অভ্যাস", "টার্মিনালে নিরাপদে চলার জন্য", [
            "কমান্ড চালানোর আগে পড়ো।",
            "`rm` আর `sudo` নিয়ে সাবধান।",
            "প্রথমে টেস্ট ফোল্ডারে অনুশীলন করো।",
            "`man` বা `--help` দিয়ে সাহায্য নাও।"]),
        recap("মনে রাখো", ["Linux সার্ভারের রাজা।",
                            "`pwd`, `ls`, `cd`, `cat` দিয়ে শুরু।",
                            "`rm -rf` বিপজ্জনক।",
                            "SSH দিয়ে দূরের সার্ভারে।"]),
    ],
    quiz=[
        dict(q="বর্তমান ফোল্ডার দেখতে কোন কমান্ড?", o=["ls", "pwd", "cd", "cat"], a=1,
             why="`pwd` = print working directory, বর্তমান পথ দেখায়।"),
        dict(q="`rm -rf` কেন বিপজ্জনক?", o=["ধীর", "ফোল্ডার চিরতরে মুছে ফেলে", "ইন্টারনেট বন্ধ করে", "ফাইল কপি করে"], a=1,
             why="`-r` recursive, `-f` force — recycle bin ছাড়া সব মুছে যায়।"),
    ],
),

chapter(
    "Git ও GitHub",
    "Git and GitHub",
    "কোডের ইতিহাস রাখা আর অন্যদের সাথে কাজ করা — আধুনিক ডেভেলপারের প্রথম দক্ষতা।",
    [
        big("মূল ধারণা", "Git = কোডের টাইম মেশিন",
            "প্রতিটি পরিবর্তন একটা commit। ভুল হলে পুরনো commit-এ ফেরা যায়। GitHub সেই ইতিহাস অনলাইনে রাখে।", "💾"),
        flow("Git-এর পাঁচ ধাপ", [
            ("init", "নতুন repo বানাও।"),
            ("add", "পরিবর্তন স্টেজ করো।"),
            ("commit", "সেভ পয়েন্ট বানাও।"),
            ("branch", "আলাদা লাইনে কাজ করো।"),
            ("merge", "কাজ জোড়া লাগাও।"),
        ]),
        terms("চারটা শব্দ", "repository, commit, branch, merge", [
            ("Repository", "প্রজেক্ট + ইতিহাস", "`.git` ফোল্ডার।"),
            ("Commit", "সেভ পয়েন্ট", "বার্তা সহ।"),
            ("Branch", "আলাদা কাজের লাইন", "feature branch।"),
            ("Merge", "শাখা জোড়া", "main-এ ফেরা।")]),
        code("প্রথম repo", "init → add → commit",
             "mkdir my-app && cd my-app\ngit init\necho \"# My App\" > README.md\ngit add README.md\ngit commit -m \"first commit\"",
             "bash", "", "`git init` শুধু একবার; প্রতিবার বদলের পর add+commit।"),
        code("Branch ও merge", "আলাদা লাইনে কাজ",
             "git checkout -b feature-login\n# কোড বদলাও\ngit add .\ngit commit -m \"add login\"\ngit checkout main\ngit merge feature-login",
             "bash", "", "Branch-এ কাজ শেষে main-এ merge।"),
        terms("GitHub-এর চারটা শব্দ", "remote, push, pull, pull request", [
            ("Remote", "অনলাইনে repo", "`origin`।"),
            ("Push", "নিজের commit পাঠাও", "`git push`।"),
            ("Pull", "অন্যের commit আনো", "`git pull`।"),
            ("Pull request", "merge করার অনুরোধ", "review হয়।")]),
        big("Commit বার্তা ভালো লেখো", "‘fix’ নয়, ‘fix login button on mobile’। ভবিষ্যতে তুমি নিজেই বুঝবে কী বদলেছিল।", "✍️"),
        big("Merge conflict", "দুইজনে একই লাইনে বদলালে Git বুঝতে পারে না কোনটা রাখবে। তখন conflict mark দেখে নিজে ঠিক করো, "
            "তারপর add+commit।", "⚔️"),
        profile("কোডের সামাজিক জায়গা", "GitHub", "Code hosting & collaboration", "G",
                [("শুরু", "২০০৮"), ("প্রতিষ্ঠাতা", "Tom Preston-Werner, Chris Wanstrath, P. J. Hyett, Scott Chacon"), ("মালিক", "Microsoft (২০১৮)"), ("কী বানায়", "repos, Actions, Pages")],
                "বিশ্বের বড় কোড হোস্টিং",
                "পোর্টফোলিও, open source contribution, GitHub Pages — সব এক জায়গায়।"),
        points("Open source-এ অবদান", "ছোট থেকে শুরু", [
            "documentation ঠিক করো।",
            "ছোট bug ধরো।",
            "Issue-তে পরিষ্কার বর্ণনা দাও।",
            "Pull request-এ ছোট পরিবর্তন রাখো।"]),
        recap("মনে রাখো", ["Git ইতিহাস রাখে, GitHub অনলাইনে।",
                            "add → commit → push।",
                            "Branch-এ কাজ, merge-এ জোড়া।",
                            "Commit বার্তা স্পষ্ট লেখো।"]),
    ],
    quiz=[
        dict(q="পরিবর্তন স্টেজ করতে কোন কমান্ড?", o=["git commit", "git add", "git push", "git init"], a=1,
             why="`git add` পরিবর্তনগুলো staging area-তে নেয়, তারপর commit করা যায়।"),
        dict(q="Pull request কী?", o=["কোড মুছে ফেলা", "merge করার অনুরোধ ও review", "সার্ভার কেনা", "ডেটাবেস বানানো"], a=1,
             why="Pull request-এ পরিবর্তন প্রস্তাব করা হয়, দল review করে তারপর merge করে।"),
    ],
),

chapter(
    "ডোমেইন, হোস্টিং ও ডিপ্লয়",
    "Domains, hosting and deployment",
    "নিজের সাইট ইন্টারনেটে তোলার পুরো পথ — নাম কেনা থেকে HTTPS পর্যন্ত।",
    [
        big("মূল ধারণা", "সাইট অনলাইনে = নাম + বাসা + ঠিকানা + তালা",
            "ডোমেইন, হোস্টিং, DNS, SSL — চারটা জিনিস ঠিক থাকলে সাইট বিশ্বজুড়ে দেখা যায়।", "🚀"),
        flow("ডিপ্লয়ের পাঁচ ধাপ", [
            ("Code", "HTML/অ্যাপ তৈরি।"),
            ("Host", "সার্ভার/প্ল্যাটফর্ম বাছো।"),
            ("Upload", "ফাইল বা Git push।"),
            ("DNS", "ডোমেইন জোড়ো।"),
            ("SSL", "HTTPS চালু।"),
        ]),
        terms("চারটা শব্দ", "registrar, nameserver, A record, CNAME", [
            ("Registrar", "ডোমেইন বিক্রেতা", "Namecheap, Cloudflare।"),
            ("Nameserver", "DNS কোথায় চলবে", "হোস্টিং বা Cloudflare।"),
            ("A record", "নাম → IPv4", "মূল ডোমেইনে।"),
            ("CNAME", "নাম → অন্য নাম", "www → root।")]),
        big("Static সাইট ডিপ্লয় করা সহজ", "HTML/CSS/JS শুধু ফাইল — Vercel, Netlify, GitHub Pages-এ drag বা Git push করলেই "
            "অনলাইনে। সার্ভার সামলাতে হয় না।", "📄"),
        compare("ডিপ্লয়ের চারটা প্ল্যাটফর্ম",
                ("Static / frontend", ["Vercel, Netlify", "Git push = deploy", "ফ্রি tier"]),
                ("VPS / cloud", ["Linode, Hetzner, AWS", "নিজে সব সামলাও", "বেশি নিয়ন্ত্রণ"]),
                "শুরুতে static, পরে দরকারে VPS।"),
        code("একটা স্ট্যাটিক সাইট", "index.html",
             "<!doctype html>\n<html>\n<head><title>My Site</title></head>\n<body>\n  <h1>হ্যালো!</h1>\n</body>\n</html>",
             "html", "", "এই ফাইলটা আপলোড করলেই একটা পেজ তৈরি।"),
        big("cPanel আর WordPress", "shared hosting-এ cPanel দিয়ে ফাইল, ইমেইল, ডেটাবেস সামলানো যায়। "
            "WordPress এক ক্লিকে বসানো যায়।", "🖱️"),
        terms("SSL-এর চারটা শব্দ", "certificate, Let's Encrypt, redirect, mixed content", [
            ("Certificate", "সার্ভারের পরিচয়", "কে দিয়েছে দেখো।"),
            ("Let's Encrypt", "ফ্রি স্বয়ংক্রিয়", "৯০ দিনে নবায়ন।"),
            ("Redirect", "HTTP → HTTPS", "সব ট্রাফিক নিরাপদ।"),
            ("Mixed content", "HTTPS-এ HTTP ফাইল", "সতর্কতা দেয়।")]),
        big("DNS propagation", "nameserver বদলালে কিছু সময় লাগে। TTL কমিয়ে আগে পরীক্ষা করো, তারপর বদলাও। "
            "সবসময় ৪৮ ঘণ্টা লাগে না — সাধারণত মিনিট।", "⏳"),
        points("ডিপ্লয়ের আগে চারটা চেক", "ছোট চেকলিস্ট", [
            "মোবাইলে খুলছে?",
            "HTTPS কাজ করছে?",
            "404 পেজ আছে?",
            "ব্যাকআপ আছে?"]),
        recap("মনে রাখো", ["ডোমেইন + হোস্টিং + DNS + SSL।",
                            "Static সাইট Vercel/Netlify-তে সহজ।",
                            "A record IPv4, CNAME অন্য নাম।",
                            "HTTPS ছাড়া সাইট চালু কোরো না।"]),
    ],
    quiz=[
        dict(q="A record কী করে?", o=["নামকে IPv4-তে বদলায়", "ছবি আপলোড", "ডেটাবেস বানায়", "ইমেইল পাঠায়"], a=0,
             why="A record ডোমেইন নামকে IPv4 ঠিকানায় ম্যাপ করে।"),
        dict(q="Static সাইটের জন্য কোনটা সহজ?", o=["Hetzner dedicated", "Vercel/Netlify", "Oracle DB", "Kubernetes"], a=1,
             why="Vercel/Netlify Git push বা drag দিয়ে static ফাইল ডিপ্লয় করে।"),
    ],
),

chapter(
    "ওয়ার্ডপ্রেস ও নো-কোড",
    "WordPress and no-code",
    "কোড না লিখেও ওয়েবসাইট, দোকান, ব্লগ বানানো যায় — কীভাবে, আর কখন?",
    [
        big("মূল ধারণা", "CMS = কনটেন্ট ম্যানেজমেন্ট সিস্টেম",
            "ডিজাইন আর কনটেন্ট আলাদা। WordPress-এ লেখা, ছবি, পেজ যোগ করা যায় — কোড না ছুঁয়ে।", "📝"),
        terms("চারটা শব্দ", "CMS, theme, plugin, WooCommerce", [
            ("CMS", "কনটেন্ট সামলানোর সিস্টেম", "WordPress, Joomla।"),
            ("Theme", "সাইটের চেহারা", "রঙ, layout।"),
            ("Plugin", "নতুন ক্ষমতা", "SEO, form, backup।"),
            ("WooCommerce", "WordPress-এ দোকান", "পণ্য, অর্ডার, পেমেন্ট।")]),
        flow("WordPress সাইটের পাঁচ ধাপ", [
            ("Hosting", "PHP + MySQL সহ।"),
            ("Install", "এক ক্লিকে WordPress।"),
            ("Theme", "চেহারা বাছো।"),
            ("Content", "পেজ/পোস্ট লেখো।"),
            ("Plugin", "SEO, backup, security।"),
        ]),
        big("Theme বনাম Plugin", "Theme দেখায়, plugin কাজ করে। Theme বদলালে কনটেন্ট থাকে; plugin বন্ধ করলে তার feature যায়।", "🧩"),
        big("WooCommerce দিয়ে দোকান", "প্রোডাক্ট, cart, checkout, পেমেন্ট গেটওয়ে। ছোট দোকানের জন্য সাশ্রয়ী; "
            "বড় হলে Shopify বা custom solution ভালো হতে পারে।", "🛒"),
        terms("WordPress, Shopify নাকি custom?", "তিনটা পথ", [
            ("WordPress", "নমনীয়, সস্তা", "নিজে maintain; ব্লগ/সাইট/ছোট দোকান।"),
            ("Shopify / no-code", "সহজ, managed", "মাসিক ফি; দ্রুত দোকান।"),
            ("Custom", "পুরো নিয়ন্ত্রণ", "দামি, সময় লাগে; বড়/বিশেষ প্রয়োজনে।"),
        ]),
        terms("নো-কোড টুল", "Elementor, Webflow, Bubble, Zapier", [
            ("Elementor", "WordPress page builder", "drag-and-drop।"),
            ("Webflow", "visual website builder", "ডিজাইনারদের প্রিয়।"),
            ("Bubble", "no-code web app", "logic সহ।"),
            ("Zapier", "অ্যাপ জোড়া", "automation।")]),
        big("WordPress-এর নিরাপত্তা", "সব আপডেট রাখো, কম plugin, শক্ত পাসওয়ার্ড, backup, আর login attempt limit। "
            "পুরনো plugin-ই সবচেয়ে বড় ফাঁক।", "🔐"),
        stat("WordPress", "৪০%+", "ওয়েবসাইট",
             "পৃথিবীর প্রায় ৪০ শতাংশ ওয়েবসাইট WordPress-এ — বিশাল ecosystem, কিন্তু বড় target-ও।", "আপডেট ছাড়া রাখো না।"),
        points("নো-কোডের চারটা সীমা", "জেনে বাছো", [
            "খুব custom logic কঠিন।",
            "Platform-এ আটকে যাওয়া (lock-in)।",
            "Performance সীমা।",
            "মাসিক খরচ বাড়তে পারে।"]),
        recap("মনে রাখো", ["CMS কনটেন্ট আলাদা রাখে।",
                            "Theme চেহারা, plugin কাজ।",
                            "WooCommerce ছোট দোকানে ভালো।",
                            "WordPress আপডেট আর backup জরুরি।"]),
    ],
    quiz=[
        dict(q="WordPress-এ চেহারা বদলায় কী?", o=["Plugin", "Theme", "Hosting", "DNS"], a=1,
             why="Theme সাইটের layout, রঙ, ফন্ট ঠিক করে; plugin নতুন feature যোগ করে।"),
        dict(q="WooCommerce কী?", o=["একটা theme", "WordPress-এ দোকান বানানোর plugin", "একটা সার্ভার", "একটা ডেটাবেস"], a=1,
             why="WooCommerce WordPress-এ product, cart, checkout যোগ করে।"),
    ],
),

chapter(
    "ফ্রিল্যান্সিং, SaaS ও ব্যবসা",
    "Freelancing, SaaS and business",
    "টেক শিখে টাকা আয়ের পথ — সার্ভিস থেকে প্রোডাক্ট পর্যন্ত।",
    [
        big("মূল ধারণা", "সার্ভিস = সময় বেচো, প্রোডাক্ট = সিস্টেম বেচো",
            "Freelancing-এ তুমি গ্রাহকের কাজ করো। SaaS-এ তুমি একই সফটওয়্যার অনেককে বেচো।", "💼"),
        compare("Freelancing বনাম SaaS",
                ("Freelancing", ["দ্রুত আয় শুরু", "সময়ের বদলে টাকা", "গ্রাহক খুঁজতে হয়"]),
                ("SaaS", ["শুরু করতে সময়", "একবার বানিয়ে বারবার আয়", "support ও marketing"]),
                "অনেকে আগে freelancing, পরে product।"),
        terms("চারটা শব্দ", "niche, portfolio, proposal, retainer", [
            ("Niche", "নির্দিষ্ট কাজ/বাজার", "WordPress speed, Shopify setup।"),
            ("Portfolio", "কাজের নমুনা", "GitHub, Behance, site।"),
            ("Proposal", "কাজের প্রস্তাব", "লক্ষ্য, সময়, দাম।"),
            ("Retainer", "মাসিক চুক্তি", "নিয়মিত আয়।")]),
        flow("প্রথম গ্রাহক পাওয়ার পথ", [
            ("Skill", "একটা কাজ ভালো শেখো।"),
            ("Sample", "২–৩টা নমুনা বানাও।"),
            ("Profile", "Upwork/Fiverr/LinkedIn সাজাও।"),
            ("Pitch", "ছোট, স্পষ্ট প্রস্তাব।"),
            ("Deliver", "সময়মতো, পরিষ্কার।"),
        ]),
        big("দাম কীভাবে ঠিক করবে?", "খরচ + সময় + মূল্য। শুধু সময় নয় — গ্রাহকের ব্যবসায় কী লাভ হচ্ছে, সেটাও দেখো। "
            "প্রথম কাজ কম দামে, কিন্তু খুব কম নয়।", "💵"),
        terms("SaaS-এর চারটা হিসাব", "MRR, churn, CAC, LTV", [
            ("MRR", "মাসিক recurring revenue", "সাবস্ক্রিপশন আয়।"),
            ("Churn", "গ্রাহক হারানোর হার", "কম রাখো।"),
            ("CAC", "এক গ্রাহক পেতে খরচ", "marketing + sales।"),
            ("LTV", "এক গ্রাহক থেকে মোট আয়", "LTV > CAC।")]),
        big("SaaS বানানোর আগে", "একটা নির্দিষ্ট সমস্যা, যেটার জন্য মানুষ টাকা দিতে রাজি। প্রথমে ১০ জনের সাথে কথা বলো, "
            "তারপর কোড লেখো।", "🗣️"),
        profile("বাংলাদেশের ফ্রিল্যান্স বাজার", "বাংলাদেশ", "Freelancing & outsourcing", "B",
                [("শক্তি", "তরুণ জনশক্তি"), ("কাজ", "web, design, writing, support"), ("প্ল্যাটফর্ম", "Upwork, Fiverr, LinkedIn"), ("চ্যালেঞ্জ", "দক্ষতা, ইংরেজি, পেমেন্ট")],
                "বিশ্বের বড় outsourcing বাজারগুলোর একটা",
                "শুরুতে ছোট কাজ, ভালো রিভিউ, তারপর দাম বাড়াও।"),
        points("ব্যবসার চারটা ভুল", "এড়িয়ে চলো", [
            "সব কাজ নিজে করার চেষ্টা।",
            "লিখিত চুক্তি না করা।",
            "সময়ের আগে বড় খরচ।",
            "গ্রাহকের কথা না শোনা।"]),
        recap("মনে রাখো", ["Freelancing সময়, SaaS সিস্টেম বেচে।",
                            "Niche + portfolio + স্পষ্ট proposal।",
                            "SaaS-এ MRR, churn, CAC, LTV।",
                            "আগে গ্রাহক, পরে কোড।"]),
    ],
    quiz=[
        dict(q="SaaS-এ MRR কী?", o=["মোট খরচ", "মাসিক recurring revenue", "কর্মী সংখ্যা", "সার্ভার সংখ্যা"], a=1,
             why="MRR = Monthly Recurring Revenue, সাবস্ক্রিপশন থেকে নিয়মিত মাসিক আয়।"),
        dict(q="Freelancing-এ প্রথমে কী দরকার?", o=["বড় অফিস", "দক্ষতা + নমুনা কাজ", "অনেক টাকা", "ডেটাবেস"], a=1,
             why="একটা দক্ষতা আর ২–৩টা নমুনা কাজ দিয়ে প্রথম গ্রাহক পাওয়া সহজ।"),
    ],
),

chapter(
    "সিকিউরিটি, ব্যাকআপ ও শেখার পথ",
    "Security, backups and the road ahead",
    "শেষ অধ্যায় — নিজের অ্যাকাউন্ট, সাইট আর শেখার অভ্যাস নিরাপদ রাখার নিয়ম।",
    [
        big("মূল ধারণা", "নিরাপত্তা = অভ্যাসের সেট",
            "শক্ত পাসওয়ার্ড, 2FA, আপডেট, ব্যাকআপ, সন্দেহ — এই পাঁচটা ৯০% ঝামেলা কমায়।", "🛡️"),
        terms("চারটা অভ্যাস", "password manager, 2FA, update, backup", [
            ("Password manager", "প্রতিটা সাইটের আলাদা পাসওয়ার্ড", "মনে রাখার দরকার নেই।"),
            ("2FA", "দুই ধাপের যাচাই", "পাসওয়ার্ড চুরি হলেও বাঁচায়।"),
            ("Update", "নিরাপত্তার patch", "পুরনো সফটওয়্যার = ফাঁক।"),
            ("Backup", "আলাদা কপি", "3-2-1 নিয়ম।")]),
        big("Phishing চেনার উপায়", "ভয় দেখানো বার্তা, ভুল ঠিকানা, ‘তাড়াতাড়ি করো’, OTP চাওয়া, অচেনা লিংক। "
            "লিংকে ঢোকার আগে ঠিকানা পড়ো।", "🎣"),
        big("OTP কাউকে দিও না", "ব্যাংক, bKash, Nagad, Facebook — কেউ ফোনে OTP চাইবে না। কেউ চাইলে ধরে নাও প্রতারণা।", "📵"),
        terms("ব্যাকআপের তিনটা নিয়ম", "3-2-1, offline, restore test", [
            ("3-2-1", "৩ কপি, ২ মাধ্যম, ১ অন্য জায়গায়", "ফোন + ক্লাউড + ডিস্ক।"),
            ("Offline", "ইন্টারনেট ছাড়া কপি", "ransomware থেকে বাঁচায়।"),
            ("Restore test", "ফেরানো পরীক্ষা", "ব্যাকআপ আছে মানেই কাজ করবে না।"),
            ("Versioning", "পুরনো সংস্করণ", "ভুল ডিলিট থেকে বাঁচায়।")]),
        big("পাসওয়ার্ডের নিয়ম", "লম্বা (১৬+ অক্ষর), অনন্য, আর password manager-এ রাখো। ‘১১২২৩৩’ বা জন্মতারিখ নয়। "
            "একই পাসওয়ার্ড সব জায়গায় নয়।", "🔑"),
        big("ফোন/ল্যাপটপ হারালে", "Find My/devices, remote wipe, ব্যাংক অ্যাকাউন্ট বন্ধ, পাসওয়ার্ড বদল, "
            "2FA রিভিউ — আগেই সেটআপ রাখো।", "📱"),
        points("শেখার চারটা অভ্যাস", "৯০ দিনের পরেও এগিয়ে থাকার জন্য", [
            "প্রতিদিন ২০ মিনিট।",
            "একটা ছোট প্রজেক্ট ধরে রাখো।",
            "নতুন কিছু শিখলে লিখে রাখো।",
            "অন্যকে শেখাও — সবচেয়ে ভালো শেখা।"]),
        big("৯০ দিনের রোডম্যাপ", "১–৩০: 101, 201। ৩১–৬০: 301, ছোট প্রজেক্ট। ৬১–৯০: 401/501, GitHub, "
            "একটা সাইট ডিপ্লয়। তারপর নিজের আগ্রহ বাছো।", "🗺️"),
        big("টেক বদলায়, ভিত্তি থাকে", "নতুন framework আসবে, নাম বদলাবে। কিন্তু computer, network, data, programming, "
            "security — এই ভিত্তি থাকলে যেকোনো নতুন জিনিস দ্রুত শেখা যায়।", "🏛️"),
        recap("মনে রাখো", ["Password manager + 2FA।",
                            "OTP কাউকে নয়।",
                            "3-2-1 ব্যাকআপ, restore টেস্ট।",
                            "প্রতিদিন ২০ মিনিট, একটু একটু করে।"]),
    ],
    quiz=[
        dict(q="OTP কেউ চাইলে কী করবে?", o=["দেবে", "কখনো দেবে না", "শুধু বন্ধুকে", "ইমেইলে পাঠাবে"], a=1,
             why="আসল কোম্পানি কখনো ফোনে OTP চায় না; OTP চাওয়া মানেই প্রতারণার সম্ভাবনা।"),
        dict(q="3-2-1 ব্যাকআপ নিয়মে ‘৩’ কী?", o=["৩ দিন", "৩ কপি", "৩ সার্ভার", "৩ ইউজার"], a=1,
             why="৩ কপি ডেটা, ২ ধরনের মাধ্যম, ১ কপি অন্য জায়গায়।"),
    ],
),

]

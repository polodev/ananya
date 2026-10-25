"""Ananya's profile and personal practice examples, shared by the site builders."""

FULL_NAME = "Ananya Debnath"
NAME_BN = "অনন্যা দেবনাথ"
FIRST_NAME_BN = "অনন্যা"
SON_NAME = "Siddharth Debnath Adyo"
SON_NAME_BN = "সিদ্ধার্থ দেবনাথ আদ্য"
AGE = 26
PHOTO = "assets/img/ananya.jpg"

CONTENT_CONTEXT = f"""This site is for {FULL_NAME} ({NAME_BN}), age {AGE}, a mother studying for a master's degree in management.
Her son is {SON_NAME} ({SON_NAME_BN}), called Adyo (আদ্য).
Use Ananya in relevant study, daily-life and family examples; use Adyo as her son, never as her brother or partner.
These are practice scenarios, not further biographical facts: do not invent the child's age, a school, a job or an address.
Keep each example at the chapter's level and practise its grammar. Other characters may be Rafi, Mitu, Tanvir and Nadia.
In Japanese use アナンニャ for Ananya and アドヨ for Adyo; keep Japanese kana-only with spaces between words.
"""

# These are the personal details supplied by Ananya's family. Other lesson stories
# are practice scenarios, rather than additional claims about her life.
INTRODUCTION = [
    dict(text=f"My name is {FULL_NAME}.", pron_bn="মাই নেম ইজ অনন্যা দেবনাথ।", bn=f"আমার নাম {NAME_BN}।"),
    dict(text=f"I am {AGE} years old.", pron_bn="আই অ্যাম টোয়েন্টি সিক্স ইয়ার্স ওল্ড।", bn="আমার বয়স ২৬ বছর।"),
    dict(text="I am a mother.", pron_bn="আই অ্যাম আ মাদার।", bn="আমি একজন মা।"),
    dict(text=f"My son's name is {SON_NAME}.", pron_bn="মাই সান্‌জ নেম ইজ সিদ্ধার্থ দেবনাথ আদ্য।", bn=f"আমার ছেলের নাম {SON_NAME_BN}।"),
    dict(text="I am studying for a master's degree in management.",
         pron_bn="আই অ্যাম স্টাডিয়িং ফর আ মাস্টার্স ডিগ্রি ইন ম্যানেজমেন্ট।", bn="আমি ম্যানেজমেন্টে মাস্টার্স করছি।"),
]

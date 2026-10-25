"""Render Ananya's photo favicon and sharing card from HTML/CSS.

Run separately from the normal static build: python3 tools/build_brand_assets.py
Requires Playwright and Chromium. The original photo is preserved; its portrait
framing uses the same CSS as the website.
"""
import base64
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine import FONTS, avatar  # noqa: E402
from learner import FULL_NAME, PHOTO  # noqa: E402


def main():
    from playwright.sync_api import sync_playwright

    css = (ROOT / "assets/app.css").read_text()
    photo = "data:image/jpeg;base64," + base64.b64encode((ROOT / PHOTO).read_bytes()).decode()

    def portrait(cls):
        return avatar("", cls).replace(PHOTO, photo)

    def document(body, extra_css=""):
        return (f'<!doctype html><html lang="bn"><head><meta charset="utf-8">{FONTS}'
                f'<style>{css}\n{extra_css}</style></head><body>{body}</body></html>')

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)

        # Square PNG icons work in browsers and on an iPhone home screen.
        page.set_content(document(portrait("brand-icon"),
            'body{background:transparent}.brand-icon{display:block;width:180px;height:180px;'
            'border-radius:36px;border:6px solid #962D66}'), wait_until="networkidle")
        page.locator(".brand-icon").screenshot(path=str(ROOT / "assets/img/ananya-apple-touch-icon.png"), omit_background=True)
        page.add_style_tag(content=".brand-icon{width:64px;height:64px;border-radius:50%;border-width:3px}")
        page.locator(".brand-icon").screenshot(path=str(ROOT / "assets/img/ananya-favicon.png"), omit_background=True)

        card = (f'<main class="share-card"><div class="share-copy"><p class="share-eyebrow">বাংলায় · তোমার নিজের গতিতে</p>'
                '<h1>অনন্যার<br>শেখার ঘর</h1>'
                f'<p class="share-name" lang="en">{FULL_NAME}</p>'
                '<p class="share-sub">মা · Management-এ মাস্টার্স · নতুন কিছু শেখার পথে</p>'
                '<div class="share-courses"><span>English</span><span>Japanese</span><span>German</span><span>Technology</span></div>'
                '</div><div class="share-photo">' + portrait("share-portrait") + '</div></main>')
        card_css = """
          body{width:1200px;height:630px;background:#FCF5FA;color:#4B2039}
          .share-card{position:relative;display:flex;align-items:center;justify-content:space-between;
            width:1200px;height:630px;padding:48px 66px;border-bottom:14px solid #962D66;
            background:radial-gradient(ellipse at 100% 5%,#E9DCEF,transparent 60%)}
          .share-copy{position:relative;z-index:1;width:730px}
          .share-eyebrow{font-size:24px;font-weight:600;color:#962D66;margin-bottom:16px}
          .share-card h1{font-size:84px;line-height:1.1;letter-spacing:-2px}
          .share-name{font-size:38px;font-weight:700;margin-top:20px;line-height:1.3}
          .share-sub{font-size:22px;margin-top:10px;color:#754963}
          .share-courses{display:flex;gap:12px;margin-top:28px}
          .share-courses span{font-size:20px;font-weight:600;background:#fff;border:1px solid #E3CBDC;
            padding:6px 18px;border-radius:99px}
          .share-photo{flex:none}
          .share-portrait{display:block;width:288px;height:288px;border-radius:50%;border:8px solid #fff;
            box-shadow:0 18px 48px #71304F26}
        """
        page.set_content(document(card, card_css), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(ROOT / "assets/img/ananya-share-v1.png"))
        browser.close()

    # Replace the historical icon paths too, for existing browser bookmarks.
    for source, target in [("ananya-favicon.png", "favicon.png"),
                           ("ananya-apple-touch-icon.png", "apple-touch-icon.png")]:
        shutil.copyfile(ROOT / "assets/img" / source, ROOT / "assets/img" / target)
    print("built Ananya's favicon, touch icon and 1200×630 sharing card")


if __name__ == "__main__":
    main()

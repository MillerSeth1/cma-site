"""Render favicon PNGs and the OG image from SVG/HTML using headless Chromium (Playwright)."""
import os, pathlib
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent
img = R / "assets/img"
og_html = f"""<html><head><style>
@font-face{{font-family:A;src:url('{(R/"assets/fonts/archivo-latin.woff2").as_uri()}');font-weight:500 900;font-stretch:100% 125%}}
@font-face{{font-family:I;src:url('{(R/"assets/fonts/inter-latin.woff2").as_uri()}')}}
body{{margin:0;width:1200px;height:630px;position:relative;overflow:hidden;font-family:I}}
.bg{{position:absolute;inset:0;background:url('{(img/"hero.svg").as_uri()}') center/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,20,27,.9),rgba(10,20,27,.3) 70%,transparent)}}
.t{{position:absolute;left:70px;top:150px;color:#f4e7d6}}
.e{{font:700 20px A;font-stretch:125%;letter-spacing:.22em;color:#e9a06a;text-transform:uppercase}}
h1{{font:900 76px/1 A;font-stretch:120%;text-transform:uppercase;margin:18px 0;max-width:820px}}
p{{font-size:26px;color:#ead8c4;margin:0}}
</style></head><body><div class="bg"></div><div class="sh"></div><div class="t"><div class="e">Nogales International · KOLS</div>
<h1>Copper Mountain Air</h1><p>Jet A &amp; 100LL · FBO · Air &amp; ground cargo</p></div></body></html>"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width":1200,"height":630})
    pg.set_content(og_html); pg.wait_for_timeout(400)
    pg.screenshot(path=str(img/"og-image.png"))
    for size, name in [(32,"favicon-32.png"),(180,"apple-touch-icon.png")]:
        pg = b.new_page(viewport={"width":size,"height":size})
        pg.goto((img/"favicon.svg").as_uri())
        pg.wait_for_timeout(200); pg.screenshot(path=str(img/name), omit_background=True)
    b.close()
print("ok")

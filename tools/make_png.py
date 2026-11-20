"""Render favicon PNGs and the 1200x630 share image (OG) with headless Chromium.
Uses data: URIs so no file:// access is needed. Output has no metadata."""
import base64, pathlib
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent
img = R / "assets/img"
def uri(path, mime): return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()
hero = uri(img / "photos/hero-1280.jpg", "image/jpeg")
logo = uri(img / "logo-stacked-light.svg", "image/svg+xml")
fav = uri(img / "favicon.svg", "image/svg+xml")
font = uri(R / "assets/fonts/archivo-latin.woff2", "font/woff2")
og = f"""<html><head><style>
@font-face{{font-family:A;src:url('{font}');font-weight:500 900;font-stretch:100% 125%}}
body{{margin:0;width:1200px;height:630px;position:relative;overflow:hidden;background:#0a141b}}
.bg{{position:absolute;inset:0;background:url('{hero}') 62% 55%/cover}}
.sh{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(10,20,27,.92) 0%,rgba(10,20,27,.7) 42%,rgba(10,20,27,.05) 75%)}}
.t{{position:absolute;left:64px;top:70px;bottom:64px;display:flex;flex-direction:column;justify-content:space-between;color:#f4e7d6}}
.e{{font:700 20px A;font-stretch:125%;letter-spacing:.2em;color:#e9a06a;text-transform:uppercase}}
p{{font:800 34px/1.15 A;font-stretch:115%;margin:10px 0 0;max-width:560px}}
</style></head><body><div class="bg"></div><div class="sh"></div>
<div class="t"><img src="{logo}" style="height:210px;width:auto;align-self:flex-start"><div><div class="e">Nogales International · KOLS</div><p>Fuel, FBO, flight training<br>&amp; cargo at KOLS</p></div></div></body></html>"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630}); pg.set_content(og); pg.wait_for_timeout(500)
    pg.screenshot(path=str(img / "og-image.jpg"), type="jpeg", quality=85)
    for size, name in [(32, "favicon-32.png"), (180, "apple-touch-icon.png")]:
        pg = b.new_page(viewport={"width": size, "height": size})
        pg.set_content(f"<body style='margin:0'><img src='{fav}' width={size} height={size} style='display:block'></body>"); pg.wait_for_timeout(200)
        pg.screenshot(path=str(img / name), omit_background=True)
    b.close()
print("ok")
# Re-save the OG image through Pillow so it carries no ICC/EXIF metadata.
from PIL import Image
_o = Image.open(img / "og-image.jpg").convert("RGB"); _o.info = {}
_o.save(img / "og-image.jpg", "JPEG", quality=85, optimize=True, progressive=True)

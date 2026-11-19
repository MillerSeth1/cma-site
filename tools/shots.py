import sys
from playwright.sync_api import sync_playwright
base, out = sys.argv[1], sys.argv[2]
shots = [("home-desktop","index.html",1440,900,True),("home-mobile","index.html",390,844,True),
         ("services","services.html",1440,900,True),("blog","blog/index.html",1440,900,True),
         ("fuel-fbo","fuel-fbo.html",1440,900,True),("contact-mobile","contact.html",390,844,True)]
shots += [tuple(a.split(",")[:2]) + (1440,900,True) for a in sys.argv[3:]]
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for name, path, w, h, full in shots:
        ctx = b.new_context(viewport={"width":w,"height":h}, device_scale_factor=1 if w>800 else 2, reduced_motion="reduce")
        pg = ctx.new_page(); pg.goto(base + path, wait_until="networkidle")
        pg.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}window.scrollTo(0,0)}")
        pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(400)
        pg.screenshot(path=f"{out}/{name}.png", full_page=full); ctx.close(); print("shot", name)
    b.close()

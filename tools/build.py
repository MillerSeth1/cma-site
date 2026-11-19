"""Build the Copper Mountain Air static site.  Run: python3 tools/build.py
Pages are written to the repo root (GitHub Pages serves the root). Relative links only,
so the site works under /cma-site/ on github.io and later on a custom domain."""
import os, re, json, html, shutil, sys
import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "_site")                       # build output (deployed by GitHub Actions)
# --drafts renders unpublished posts too, for LOCAL review only. The deploy workflow never passes it.
SHOW_DRAFTS = "--drafts" in sys.argv
SITE_URL = "https://millerseth1.github.io/cma-site/"   # change when the custom domain goes live
PREVIEW = True                                          # True = noindex + preview banner
CONTACT_TO = "operations@coppermountainair.com"
# Verified public contact facts (sources recorded in the commit / site copy notes):
# Address & phone: Seth's email signature; FAA airport manager record and CMA's AirNav FBO listing; Santa Cruz County airport page.
# Hours: Santa Cruz County airport page; CMA's previous coppermountainair.com (Wayback, 2025-12-14 and 2026-07-11); iFlightPlanner and PilotGPT FBO listings.
# After-hours: CMA AirNav FBO listing ("after hours call-out service (with prior arrangement and/or a callout fee)"); County page ("after-hour on call"); FBO contract requires after-hours on-call fueling.
# Full-service fuel (no self-serve): AirNav KOLS FBO listing (FS only), GlobalAir, iFlightPlanner, PilotGPT; FBO contract ("full service FBO", truck-to-aircraft dispensing).
# Cards: iFlightPlanner and PilotGPT (Visa, Mastercard, American Express, Discover); FBO contract requires credit-card acceptance. Fuel brand Phillips 66: AirNav FBO listing.
# Amenities: previous CMA website (lounge, Wi-Fi, refreshments, overnight parking); County page (restrooms, coffee/drinks, hotel and car arrangements, catering); FBO contract minimum lounge services; AirNav (passenger terminal and lounge, hangar leasing, ramp/tie-down).
PHONE = "520-287-9120"
PHONE_HREF = "tel:+15202879120"
PHONE_LINK = f'<a href="{PHONE_HREF}">{PHONE}</a>'
STREET = "11 Access Way"
HOURS = "Monday–Saturday 7:00 a.m.–7:00 p.m., Sunday 7:00 a.m.–5:00 p.m."
HOURS_HTML = "Monday–Saturday 7:00 a.m.–7:00 p.m.<br>Sunday 7:00 a.m.–5:00 p.m."
AFTER_HOURS = f"After-hours call-out is available with prior arrangement, and a call-out fee may apply. Call {PHONE_LINK} for details."
CARDS = "Visa, Mastercard, American Express and Discover"
# Official branding: Phillips 66 Aviation WingPoints Rewards program (wingpoints.com; phillips66.com/aviation/cards-rewards/).
WINGPOINTS = 'Phillips 66 <a href="https://www.wingpoints.com/" rel="noopener">WingPoints</a> rewards program participant'

# Image slots. Photos: responsive AVIF/WebP/JPEG made by tools/optimize_images.py into assets/img/photos/.
# Slots still waiting on a real photo point at an SVG placeholder ("svg": file).
MANIFEST = json.load(open(os.path.join(ROOT, "assets", "img", "photos", "manifest.json")))
IMG = {
  "hero":       "Twin-engine aircraft seen head-on on the ramp at Nogales International Airport, with mountains behind",
  "ramp-band":  "Inside a hangar at Nogales International Airport",
  "airfield":   "Taxiway sign beside the airfield at Nogales International Airport, with mountains behind",
  "taxiway-signs": "Yellow taxiway direction signs at Nogales International Airport",
  "fbo":        "Aircraft inside a hangar at Nogales International Airport",
  "cargo":      "Yellow CARGO direction sign beside the airfield at Nogales International Airport",
  "cargo-sign": "Close-up of a yellow CARGO taxiway sign at Nogales International Airport",
  "kols-guide": "Red runway 22-4 sign at Nogales International Airport",
  "training":   "Yellow taxiway direction signs at Nogales International Airport",
  "charter":    "The runway at Nogales International Airport at dusk",
  "fuel":       {"file": "fuel.svg", "alt": "Placeholder: fuel photo coming soon"},
  # Drop the real photo in as assets/img/josh-berg.jpg and change "file" below to "josh-berg.jpg".
  "josh-berg":  {"file": "josh-berg.svg", "alt": "Photo placeholder: Josh Berg, photo coming"},
}
SIZES = {"full": "100vw", "half": "(min-width: 860px) 50vw, 100vw", "card": "(min-width: 1100px) 380px, (min-width: 700px) 50vw, 100vw",
         "article": "(min-width: 800px) 760px, 100vw", "third": "(min-width: 700px) 33vw, 100vw"}
def srcset(slot, p, ext):
    m = MANIFEST[slot]
    return ", ".join(f"{p}assets/img/photos/{slot}-{w}.{ext} {w}w" for w in m["widths"])
def img(slot, p, cls="", eager=False, sizes="half"):
    v = IMG[slot]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    if isinstance(v, dict):
        return f'<img src="{p}assets/img/{v["file"]}" alt="{html.escape(v["alt"])}" {load} decoding="async" width="1200" height="800"{c}>'
    m = MANIFEST[slot]; sz = SIZES.get(sizes, sizes)
    mid = [w for w in m["widths"] if w >= 1200] or m["widths"][-1:]
    return (f'<picture><source type="image/avif" srcset="{srcset(slot, p, "avif")}" sizes="{sz}">'
            f'<source type="image/webp" srcset="{srcset(slot, p, "webp")}" sizes="{sz}">'
            f'<img src="{p}assets/img/photos/{slot}-{mid[0]}.jpg" srcset="{srcset(slot, p, "jpg")}" sizes="{sz}" alt="{html.escape(v)}" '
            f'{load} decoding="async" width="{m["w"]}" height="{m["h"]}"{c}></picture>')

def ph(t): return f'<span class="ph">[{t}]</span>'

NAV = [("index.html","Home"),("services.html","Services"),("fuel-fbo.html","Fuel &amp; FBO"),
       ("flight-training.html","Flight Training"),("charter.html","Charter"),("about.html","About"),
       ("blog/index.html","Blog")]

JSONLD_BIZ = {
  "@context":"https://schema.org","@type":["LocalBusiness"],"@id":SITE_URL+"#business",
  "name":"Copper Mountain Air, LLC","url":SITE_URL,
  "description":"Fuel (Jet A and 100LL), FBO services, FAA Part 61 flight training, and air and ground cargo at Nogales International Airport (KOLS) in Nogales, Arizona.",
  "telephone":"+1-520-287-9120","email":CONTACT_TO,"openingHours":["Mo-Sa 07:00-19:00","Su 07:00-17:00"],"priceRange":"",
  "logo":SITE_URL+"assets/img/logo-stacked-dark.svg","image":SITE_URL+"assets/img/og-image.jpg",
  "address":{"@type":"PostalAddress","streetAddress":"11 Access Way","addressLocality":"Nogales","addressRegion":"AZ","postalCode":"85621","addressCountry":"US"},
  "geo":{"@type":"GeoCoordinates","latitude":31.4177222,"longitude":-110.8478889},
  "areaServed":[{"@type":"City","name":"Nogales, AZ"},{"@type":"AdministrativeArea","name":"Santa Cruz County, AZ"},{"@type":"State","name":"Arizona"}],
  "containedInPlace":{"@type":"Airport","name":"Nogales International Airport","icaoCode":"KOLS",
     "address":{"@type":"PostalAddress","addressLocality":"Nogales","addressRegion":"AZ","postalCode":"85621","addressCountry":"US"}},
  "sameAs":[]
}

def head(title, desc, path, p, extra_ld=None, og_type="website", og_img=None):
    pre = (f'<link rel="preload" as="image" type="image/avif" imagesrcset="{srcset("hero", p, "avif")}" imagesizes="100vw" fetchpriority="high">\n') if path == "index.html" else ""
    url = SITE_URL + ("" if path == "index.html" else path)
    og = SITE_URL + "assets/img/" + (og_img or "og-image.jpg")
    ld = [JSONLD_BIZ] + ([extra_ld] if extra_ld else [])
    robots = '<meta name="robots" content="noindex, nofollow">\n' if (PREVIEW or path.startswith("preview/")) else ''
    return f"""<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0a141b">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="{p}assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Copper Mountain Air">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{og}">
<meta name="geo.region" content="US-AZ">
<meta name="geo.placename" content="Nogales, Arizona">
<link rel="preload" href="{p}assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
{pre}<link rel="stylesheet" href="{p}assets/css/site.css">
<script>document.documentElement.className="js";</script>
<script type="application/ld+json">{json.dumps(ld if len(ld)>1 else ld[0], ensure_ascii=False)}</script>
</head>"""

def header(path, p):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if (href == path or (href == "blog/index.html" and path.startswith("blog/"))) else ""
        items.append(f'<li><a href="{p}{href}"{cur}>{label}</a></li>')
    contact_cur = ' aria-current="page"' if path == "contact.html" else ""
    items.append(f'<li><a class="nav-cta" href="{p}contact.html"{contact_cur}>Contact</a></li>')
    bar = ('<div class="preview-bar"><strong>Preview draft.</strong> Not yet published.</div>') if PREVIEW else ""
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
{bar}
<header class="site-header"><div class="wrap">
  <a class="brand" href="{p}index.html" aria-label="Copper Mountain Air home"><img src="{p}assets/img/logo-light.svg" alt="Copper Mountain Air" width="305" height="40"></a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav id="site-nav" class="site-nav" aria-label="Primary"><ul>{''.join(items)}</ul></nav>
</div></header>
<main id="main">"""

def footer(p):
    return f"""</main>
<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div><img src="{p}assets/img/logo-stacked-light.svg" alt="Copper Mountain Air" width="138" height="120" loading="lazy" style="height:120px;width:auto;margin-bottom:1rem">
      <p>Fuel, FBO and cargo at Nogales International Airport (KOLS), serving Nogales and Santa Cruz County, Arizona.</p></div>
    <div><h3>Visit</h3><p>Copper Mountain Air, LLC<br>Nogales International Airport (KOLS)<br>{STREET}<br>Nogales, AZ 85621</p></div>
    <div><h3>Contact</h3><ul><li>Phone: {PHONE_LINK}</li><li><a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a></li><li>Hours: {HOURS_HTML}</li><li><a href="{p}contact.html">Send a message</a></li></ul></div>
    <div><h3>Explore</h3><ul><li><a href="{p}services.html">Services</a></li><li><a href="{p}fuel-fbo.html">Fuel &amp; FBO</a></li><li><a href="{p}flight-training.html">Flight training</a></li><li><a href="{p}blog/index.html">Blog</a></li></ul></div>
  </div>
  <div class="legal"><span>© 2026 Copper Mountain Air, LLC</span><span>On-demand charter is coming soon and is not yet offered.</span></div>
</div></footer>
<script src="{p}assets/js/site.js" defer></script>
</body>
</html>
"""

def page(path, title, desc, body, extra_ld=None, og_type="website"):
    p = "../" * path.count("/")
    out = head(title, desc, path, p, extra_ld, og_type) + "\n" + header(path, p) + "\n" + body(p) + "\n" + footer(p)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(out)
    PAGES.append(path)

PAGES = []
ARROW = '<span class="arrow" aria-hidden="true">→</span>'

def page_hero(eyebrow, h1, lede, badge=""):
    return f'<div class="page-hero"><div class="wrap">{badge}<p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p>{lede}</p></div></div>'

def cta(p, h="Need fuel, a ramp spot or a freight quote?", t="Tell us what you need and we'll get back to you."):
    return f'<section><div class="wrap"><div class="cta-band reveal"><div><h2>{h}</h2><p>{t}</p></div><div><a class="btn btn-dark" href="{p}contact.html">Contact us {ARROW}</a></div></div></div></section>'

AIRPORT_FACTS = """<div class="facts reveal">
 <div class="fact"><span class="k">Runway</span><span class="v">4/22</span><span class="s">7,200 × 100 ft asphalt</span></div>
 <div class="fact"><span class="k">Elevation</span><span class="v">3,955 ft</span><span class="s">MSL, surveyed</span></div>
 <div class="fact"><span class="k">CTAF / UNICOM</span><span class="v">122.8</span><span class="s">Non-towered field</span></div>
 <div class="fact"><span class="k">ASOS</span><span class="v">121.125</span><span class="s">Weather</span></div>
 <div class="fact"><span class="k">Fuel on field</span><span class="v">Jet A · 100LL</span><span class="s">From Copper Mountain Air</span></div>
 <div class="fact"><span class="k">Status</span><span class="v">Airport of entry</span><span class="s">International, per FAA data</span></div>
</div>
<p class="source">Source: FAA airport data via <a href="https://www.airnav.com/airport/KOLS" rel="noopener">AirNav (KOLS)</a>, effective 29 Oct 2026. Not for navigation.</p>"""

AIRNAV = 'https://www.airnav.com/airport/KOLS'
FUEL_PRICES = f'Current Jet A and 100LL prices are posted on <a href="{AIRNAV}" rel="noopener">AirNav</a>.'
POSTS = []
UNLISTED = []
def kols_link(p, text):
    """Only link the KOLS guide once that post is published (or in a local --drafts build)."""
    if any(x["slug"] == "kols-pilot-guide" for x in POSTS):
        return f'<p style="margin-top:1.5rem"><a class="btn btn-ghost" href="{p}blog/kols-pilot-guide.html">{text} {ARROW}</a></p>'
    return ""

# ---------- HOME ----------
def home(p):
    return f"""
<section class="hero" aria-label="Introduction" style="padding:0">
  <div class="hero-media">{img("hero", p, eager=True, sizes="full")}</div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Nogales International Airport · KOLS</p>
    <h1>Fuel, freight &amp; flight <span class="cu">on the border.</span></h1>
    <p class="lede">Copper Mountain Air keeps Southern Arizona moving: Jet A and Avgas on the ramp, FBO service at KOLS, Part 61 flight training, and air and ground cargo out of Nogales.</p>
    <div class="actions"><a class="btn btn-primary" href="{p}contact.html">Get in touch {ARROW}</a><a class="btn btn-ghost" href="{p}fuel-fbo.html">Fuel &amp; FBO</a></div>
    <div class="hero-strip"><span>Jet A</span><span>100LL Avgas</span><span>FBO</span><span>Flight training</span><span>Air &amp; ground cargo</span><span>Santa Cruz County, AZ</span></div>
  </div>
</section>

<section><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">What we do</p><h2>One stop at KOLS.</h2><p>Whether you're fueling up on a cross-country, parking for the night or moving a time-critical load, start here.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="media">{img("fuel", p, sizes="card")}</div><div class="body"><span class="num">01</span><h3>Fuel</h3><p>Jet A and 100LL Avgas at Nogales International. {FUEL_PRICES}</p><a class="more" href="{p}fuel-fbo.html">Fuel details {ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{img("fbo", p, sizes="card")}</div><div class="body"><span class="num">02</span><h3>FBO services</h3><p>Ground handling, ramp and tie-down parking, and hangar space on the field.</p><a class="more" href="{p}fuel-fbo.html#fbo">FBO services {ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{img("cargo", p, sizes="card")}</div><div class="body"><span class="num">03</span><h3>Cargo &amp; freight</h3><p>Time-critical freight out of Nogales by air and ground, including on-demand expedited freight.</p><a class="more" href="{p}services.html#cargo">Cargo services {ARROW}</a></div></article>
  </div>
</div></section>

<figure class="photo-band">{img("ramp-band", p, sizes="full")}<figcaption>Hangars at KOLS</figcaption></figure>

<section class="dark"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Flying in?</p><h2>Nogales International at a glance.</h2><p>A 7,200-foot runway at the foot of the Santa Cruz Valley, about 7 miles northeast of downtown Nogales.</p></div>
  {AIRPORT_FACTS}
  {kols_link(p, "Read the KOLS pilot guide")}
</div></section>

<section><div class="wrap split">
  <div class="frame reveal">{img("training", p)}</div>
  <div class="reveal"><p class="eyebrow">Flight training</p><h2>Learn to fly at KOLS.</h2>
    <p>FAA Part 61 single-engine flight training is available now at Nogales International Airport. Multi-engine training is arriving shortly, and FAA Part 141 flight school certification is in process.</p>
    <p>On-demand charter is coming soon and is not yet offered.</p>
    <p><a class="btn btn-dark" href="{p}contact.html?topic=Flight%20training">Start flight training {ARROW}</a></p>
    <p><a href="{p}flight-training.html">Flight training</a> · <a href="{p}charter.html">Charter</a></p></div>
</div></section>
{cta(p)}
"""

def services(p):
    return page_hero("Services", "Built for the border.", "Fuel, FBO services and cargo at Nogales International Airport (KOLS), serving Nogales, Santa Cruz County and Southern Arizona.") + f"""
<section id="cargo"><div class="wrap split">
  <div class="frame reveal">{img("cargo-sign", p)}</div>
  <div class="reveal"><p class="eyebrow">Cargo &amp; freight</p><h2>Air and ground, on demand.</h2>
    <p>When a shipment can't wait, we move it. Copper Mountain Air handles time-critical freight out of Nogales by ground and coordinates air cargo at KOLS.</p>
    <ul class="checks">
      <li>Ground trucking across Southern Arizona and beyond</li>
      <li>On-demand expedited freight</li>
      <li>Air cargo coordination and ramp handling at KOLS</li>
    </ul>
    <a class="btn btn-dark" href="{p}contact.html?topic=Cargo%20%2F%20freight">Request a freight quote {ARROW}</a></div>
</div>
<div class="wrap" style="padding-top:0">
  <div class="section-head reveal"><p class="eyebrow">Fleet</p><h2>Our trucks.</h2><p>Two trucks for on-demand moves, from smaller van loads to dock-height freight.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="body">
      <h3>Ford E-150 Cargo Van</h3>
      <ul class="checks">
        <li>Usable cargo length: 108 in (9 ft)</li>
        <li>Door opening width: approx. 55 in</li>
        <li>Max cargo height: 40 in</li>
        <li>Max payload: approx. 1,600 lbs</li>
      </ul>
    </div></article>
    <article class="card reveal"><div class="body">
      <h3>Hino 268 Box Truck</h3>
      <p>26-foot dock-height</p>
      <ul class="checks">
        <li>Cargo box length: 26 ft (dock-height)</li>
        <li>GVWR: 25,999 lbs (16,500 lbs empty weight)</li>
        <li>Max payload: up to 9,499 lbs theoretical (actual usable payload accounts for driver, fuel, equipment, and axle limits)</li>
      </ul>
    </div></article>
  </div>
</div></section>
<section class="sand" id="fuel"><div class="wrap split rev">
  <div class="frame reveal">{img("fuel", p)}</div>
  <div class="reveal"><p class="eyebrow">Fuel</p><h2>Jet A and 100LL.</h2>
    <p>Both jet fuel and Avgas are available on the field at Nogales International.</p>
    <ul class="checks"><li>Full-service Jet A (including with additive)</li><li>Full-service 100LL Avgas</li><li>Phillips 66</li><li>{WINGPOINTS}</li><li>{FUEL_PRICES}</li></ul>
    <a class="btn btn-dark" href="{p}fuel-fbo.html">Fuel &amp; FBO details {ARROW}</a></div>
</div></section>
<section id="fbo"><div class="wrap split">
  <div class="frame reveal">{img("fbo", p)}</div>
  <div class="reveal"><p class="eyebrow">FBO</p><h2>Your stop at KOLS.</h2>
    <ul class="checks"><li>Aircraft ground handling</li><li>Ramp and tie-down parking</li><li>Hangar leasing — call or email for current availability and rates</li><li>Passenger terminal and pilot lounge with Wi-Fi, restrooms, coffee and refreshments, and a flight-planning desk</li></ul>
    <a class="btn btn-dark" href="{p}fuel-fbo.html#fbo">See FBO services {ARROW}</a></div>
</div></section>
<section id="training"><div class="wrap split">
  <div class="frame reveal">{img("training", p)}</div>
  <div class="reveal"><p class="eyebrow">Flight training</p><h2>Learn to fly at KOLS.</h2>
    <p>FAA Part 61 single-engine flight training is available now at Nogales International Airport.</p>
    <ul class="checks">
      <li>Part 61 single-engine training, available now</li>
      <li>Multi-engine training arriving shortly</li>
      <li>FAA Part 141 flight school certification in process</li>
    </ul>
    <a class="btn btn-dark" href="{p}flight-training.html">Flight training details {ARROW}</a></div>
</div></section>
<section class="dark" id="charter"><div class="wrap split">
  <div class="frame reveal">{img("charter", p)}</div>
  <div class="reveal"><span class="badge soon">Coming soon</span><p class="eyebrow">Charter</p><h2>On-demand charter from KOLS.</h2>
    <p>An FAA Part 135 on-demand charter program is in development and is not yet offered. Join the interest list and we'll reach out when the service opens.</p>
    <a class="btn btn-ghost" href="{p}charter.html">Charter updates {ARROW}</a></div>
</div></section>
{cta(p)}"""

def fuel_fbo(p):
    return page_hero("Fuel &amp; FBO · KOLS", "Fuel up at Nogales International.", "Jet A and 100LL Avgas, plus ramp, hangar and handling services at Nogales International Airport (KOLS).") + f"""
<section id="fuel"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Fuel</p><h2>Jet A &amp; 100LL.</h2><p>{FUEL_PRICES}</p></div>
  <table class="price-table reveal"><thead><tr><th scope="col">Fuel</th><th scope="col">Service</th><th scope="col">Current price</th></tr></thead>
  <tbody><tr><td><strong>Jet A</strong> (including with additive)</td><td>Full service</td><td><a href="{AIRNAV}" rel="noopener">See current price on AirNav</a></td></tr>
  <tr><td><strong>100LL Avgas</strong></td><td>Full service</td><td><a href="{AIRNAV}" rel="noopener">See current price on AirNav</a></td></tr></tbody></table>
  <p class="note" style="margin-top:1rem">Phillips 66 · {WINGPOINTS} · Fuel hours: {HOURS} · {AFTER_HOURS} · Payment: {CARDS}.</p>
</div></section>
<section class="sand" id="fbo"><div class="wrap split">
  <div class="frame reveal">{img("fbo", p)}</div>
  <div class="reveal"><p class="eyebrow">FBO services</p><h2>Ramp, hangar &amp; handling.</h2>
    <ul class="checks"><li>Aircraft ground handling</li><li>Ramp and tie-down parking — call or email for current rates</li><li>Hangar leasing — call or email for current availability and rates</li><li>Passenger terminal and pilot lounge with Wi-Fi, restrooms, coffee and refreshments, and a flight-planning desk. We can also help with hotel and rental-car arrangements, and with catering.</li></ul>
    <a class="btn btn-dark" href="{p}contact.html?topic=FBO%20%2F%20ramp%20%2F%20hangar">Reserve a ramp spot or hangar {ARROW}</a></div>
</div></section>
<section class="dark"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Airport info</p><h2>KOLS for pilots.</h2></div>
  {AIRPORT_FACTS}
  {kols_link(p, "Full KOLS pilot guide")}
</div></section>
{cta(p, "Inbound to KOLS?", f"Let us know your ETA and fuel needs. Phone: {PHONE_LINK}")}"""

def flight_training(p):
    return page_hero("Flight Training", "Learn to fly at KOLS.", "FAA Part 61 single-engine flight training is available now at Nogales International Airport (KOLS).") + f"""
<section><div class="wrap split">
  <div class="frame reveal">{img("training", p)}</div>
  <div class="reveal"><p class="eyebrow">Available now</p><h2>Part 61 single-engine training.</h2>
    <p>Copper Mountain Air offers FAA Part 61 single-engine flight training on the field at Nogales International Airport.</p>
    <ul class="checks">
      <li>FAA Part 61 single-engine flight training, available now</li>
      <li>Multi-engine training arriving shortly</li>
      <li>FAA Part 141 flight school certification in process</li>
    </ul>
    <p>To get started, or to join the list for multi-engine training and Part 141 updates, call {PHONE_LINK}, email <a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a>, or send a note through the contact form.</p>
    <a class="btn btn-dark" href="{p}contact.html?topic=Flight%20training">Get started {ARROW}</a></div>
</div></section>{cta(p, "Ready to fly?", f"Call {PHONE_LINK} or email us and we'll help you get started.")}"""

def coming_soon_charter(p):
    hero = page_hero("Charter", "Fly direct from KOLS.", "An FAA Part 135 on-demand charter program from Nogales International is in development. It is not offered yet.", '<span class="badge soon">Coming soon</span>')
    return hero + f"""
<section><div class="wrap split">
  <div class="frame reveal">{img("charter", p)}</div>
  <div class="reveal"><span class="badge soon">Coming soon</span><h2>On-demand charter is in the works.</h2>
    <p>We're working toward FAA Part 135 on-demand charter from Nogales International. We can't book charter flights yet; join the interest list and we'll reach out when the service opens.</p>
    <a class="btn btn-dark" href="{p}contact.html?topic=Charter%20interest">Join the interest list {ARROW}</a></div>
</div></section>{cta(p, "Questions in the meantime?", "We're happy to talk. Fuel, FBO, cargo and Part 61 flight training are available today.")}"""

def about(p):
    return page_hero("About", "Southern Arizona's home field team.", "Copper Mountain Air, LLC is based at Nogales International Airport (KOLS) in Nogales, Arizona.") + f"""
<section><div class="wrap split">
  <figure class="frame reveal">{img("airfield", p)}</figure>
  <div class="reveal"><p class="eyebrow">Our story</p><h2>Rooted at KOLS.</h2>
    <p>Since 2024, Copper Mountain Air has been the fixed-base operator at Nogales International Airport (KOLS) in Santa Cruz County, Arizona, just north of the U.S.–Mexico border.</p>
    <p>We provide full-service Jet A and 100LL fueling, FBO ground support on the field, FAA Part 61 single-engine flight training, and on-demand expedited cargo by ground. Multi-engine training is arriving shortly, and FAA Part 141 flight school certification is in process. On-demand charter is in development and is not yet offered.</p></div>
</div></section>
<section><div class="wrap split rev">
  <figure class="frame reveal">{img("kols-guide", p)}</figure>
  <div class="reveal"><p class="eyebrow">On the field</p><h2>Part of Nogales International.</h2>
    <p>We work on the field every day alongside the pilots, tenants and neighbors who rely on KOLS, Santa Cruz County's public-use airport.</p></div>
</div></section>
<section class="sand"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Team</p><h2>Direct, hands-on service at KOLS.</h2><p>A locally led operation you can reach by phone or email when you need fuel, a ramp spot, a hangar, or a freight move.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="body"><h3>Seth Miller</h3><p>Principal</p><p>Leads Copper Mountain Air at Nogales International Airport, with a focus on dependable fuel, FBO service, flight training and on-demand cargo for the pilots and shippers who use KOLS.</p></div></article>
    <article class="card reveal"><div class="body"><h3>Operations at KOLS</h3><p>On the field every day</p><p>Our operations team handles fueling, ramp and hangar needs, and freight coordination. Call {PHONE_LINK} or email <a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a>.</p></div></article>
  </div>
</div></section>
<section class="dark"><div class="wrap"><div class="section-head reveal"><p class="eyebrow">Where we are</p><h2>Nogales International Airport (KOLS)</h2><p>About 7 miles northeast of Nogales in Santa Cruz County, Arizona. Address: {STREET}, Nogales, AZ 85621.</p></div>{AIRPORT_FACTS}</div></section>
{cta(p)}"""

def contact(p):
    opts = ["Fuel", "FBO / ramp / hangar", "Cargo / freight", "Flight training", "Charter interest", "Billing / payment", "Other"]
    return page_hero("Contact", "Let's talk.", "Fuel, ramp space, a freight quote, or a question: send us a note.") + f"""
<section><div class="wrap split" style="align-items:start">
  <form class="form reveal" id="contact-form" data-to="{CONTACT_TO}" action="mailto:{CONTACT_TO}" method="post" enctype="text/plain">
    <div class="row"><div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div></div>
    <div class="row"><div class="field"><label for="phone">Phone <span class="hint">Optional</span></label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="company">Company <span class="hint">Optional</span></label><input id="company" name="company" autocomplete="organization"></div></div>
    <div class="field"><label for="topic">What can we help with?</label><select id="topic" name="topic" required>{''.join(f'<option>{html.escape(o)}</option>' for o in opts)}</select></div>
    <div class="field"><label for="message">Message</label><textarea id="message" name="message" required placeholder="Tail number and ETA, fuel needs, or shipment details (pickup, delivery, pieces, weight)"></textarea></div>
    <div><button class="btn btn-primary" type="submit">Open in my email app {ARROW}</button></div>
    <p class="note" id="form-status" role="status" aria-live="polite"></p>
    <p class="note">This form opens a pre-filled email to <a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a> in your email app. Nothing is sent until you press Send there.</p>
  </form>
  <div class="contact-cards reveal">
    <div class="contact-card"><h3>Phone</h3><p>{PHONE_LINK}</p></div>
    <div class="contact-card"><h3>Email</h3><p><a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a></p></div>
    <div class="contact-card"><h3>Hours</h3><p>{HOURS_HTML}</p></div>
    <div class="contact-card"><h3>Location</h3><p>Nogales International Airport (KOLS)<br>{STREET}<br>Nogales, AZ 85621</p></div>
  </div>
</div></section>"""

# ---------- BLOG ----------
def load_posts():
    posts = []
    d = os.path.join(ROOT, "posts")
    for fn in sorted(os.listdir(d), key=lambda n: n.replace("DRAFT-", ""), reverse=True):
        if not fn.endswith(".md") or fn.startswith("_"): continue
        raw = open(os.path.join(d, fn)).read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        fm = {}
        for line in m.group(1).splitlines():
            if not line.strip() or line.lstrip().startswith("#"): continue
            k, v = line.split(":", 1); v = re.sub(r"\s+#.*$", "", v.strip()) if not v.strip().startswith('"') else v.strip()
            fm[k.strip()] = v.strip().strip('"')
        body = markdown.markdown(m.group(2), extensions=["tables"])
        body = re.sub(r"<p>\{\{gallery:([^}]*)\}\}</p>", lambda mm: "{{GALLERY:" + mm.group(1).strip() + "}}", body)
        body = re.sub(r"<p>\{\{figure:([^|}]*)\|([^}]*)\}\}</p>", lambda mm: "{{FIGURE:" + mm.group(1).strip() + "|" + mm.group(2).strip() + "}}", body)
        fm["body"] = re.sub(r"\[([A-Z0-9][^\]<]*)\]", lambda mm: ph(mm.group(1)), body)  # highlight [PLACEHOLDERS]
        fm["source"] = "posts/" + fn
        fm["draft"] = fm.get("published", "false").lower() != "true"
        if fm.get("unlisted", "false").lower() == "true":
            # Unlisted: rendered only at preview/<token>/<file>.html, never in any list, sitemap or nav; always noindex.
            assert re.fullmatch(r"[a-z0-9]{10,}", fm.get("unlisted_token", "")), "unlisted posts need a random unlisted_token"
            UNLISTED.append(fm); continue
        if fm["draft"] and not SHOW_DRAFTS:
            print("  skipping unpublished post:", fn); continue
        posts.append(fm)
    return posts

def blog_index(posts):
    def f(p):
        cards = "".join(f"""<article class="card post-card reveal"><div class="media">{img(x["image"], p, sizes="card")}</div><div class="body">
{'<span class="badge draft">Draft · not published</span>' if x["draft"] else ''}{f'<p class="meta">{html.escape(x["date"])}</p>' if x.get("date") and not x["date"].startswith("[") else ''}
<h3><a href="{p}blog/{x["slug"]}.html" style="color:inherit;text-decoration:none">{html.escape(x["title"])}</a></h3><p>{html.escape(x["description"])}</p>
<a class="more" href="{p}blog/{x["slug"]}.html">{"Read the draft" if x["draft"] else "Read more"} {ARROW}</a></div></article>""" for x in posts)
        return page_hero("Blog", "From the ramp.", "Airport news, pilot info and freight tips from Nogales International Airport (KOLS) and Santa Cruz County.") + f"""
<section><div class="wrap">{'<div class="draft-banner">LOCAL DRAFT REVIEW BUILD: posts marked Draft are not on the live site.</div>' if SHOW_DRAFTS else ''}{f'<div class="post-list">{cards}</div>' if posts else EMPTY_BLOG(p)}</div></section>"""
    return f

def EMPTY_BLOG(p):
    return f"""<div class="split reveal"><div class="frame">{img("kols-guide", p)}</div><div><span class="badge soon">First post coming soon</span>
<h2>New posts every month.</h2><p>We publish a new post each month: KOLS airport updates, pilot info, and freight tips for Santa Cruz County. Check back soon.</p>
<a class="btn btn-dark" href="{p}fuel-fbo.html">Fuel &amp; FBO info {ARROW}</a></div></div>"""

def expand(body, p):
    body = re.sub(r"\{\{GALLERY:([^}]*)\}\}", lambda m: '<div class="gallery">' + "".join(f'<figure>{img(s.strip(), p, sizes="third")}</figure>' for s in m.group(1).split(",")) + "</div>", body)
    return re.sub(r"\{\{FIGURE:([^|]*)\|([^}]*)\}\}", lambda m: f'<figure class="article-fig">{img(m.group(1), p, sizes="article")}<figcaption>{m.group(2)}</figcaption></figure>', body)

def blog_post(x):
    def f(p):
        return f"""<div class="page-hero"><div class="wrap">{'<span class="badge draft">Draft · for review</span>' if x["draft"] else ''}<p class="eyebrow"><a href="{p}blog/index.html" style="color:inherit">Blog</a></p><h1 style="text-transform:none;font-size:clamp(2rem,5vw,3.4rem)">{html.escape(x["title"])}</h1><p class="post-meta">Copper Mountain Air{" · " + html.escape(x["date"]) if x.get("date") and not x["date"].startswith("[") else ""}</p></div></div>
<section style="padding-top:0"><div class="wrap"><article class="article">
<div class="article-hero">{img(x["image"], p, eager=True, sizes="article")}</div>
{'<div class="draft-banner">UNLISTED PREVIEW — not linked anywhere on the site and hidden from search engines. Share this link only with people reviewing the post.</div>' if x.get("unlisted") == "true" else ''}{f'<div class="draft-banner">DRAFT — not published. Seth to review and approve before this goes live. Source file: <code>{x["source"]}</code></div>' if x["draft"] else ''}
{expand(x["body"], p)}
<p style="margin-top:2.5rem"><a class="btn btn-dark" href="{p}blog/index.html">← All posts</a></p>
</article></div></section>"""
    return f

def main():
    global POSTS
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"), ignore=shutil.ignore_patterns("README.md", "manifest.json"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    POSTS = load_posts()
    page("index.html", "Copper Mountain Air | Fuel, FBO, Flight Training & Cargo at Nogales International Airport (KOLS)",
         "Jet A and 100LL fuel, FBO services, FAA Part 61 flight training, and air and ground cargo at Nogales International Airport (KOLS) in Nogales, Santa Cruz County, Arizona.", home)
    page("services.html", "Services | Cargo, Fuel, FBO & Flight Training in Nogales, AZ | Copper Mountain Air",
         "Air and ground cargo, Jet A and 100LL fuel, FBO services, and FAA Part 61 flight training at Nogales International Airport (KOLS), serving Santa Cruz County, Arizona.", services)
    page("fuel-fbo.html", "Jet A & 100LL Fuel and FBO at KOLS | Copper Mountain Air",
         "Jet A and 100LL Avgas, ramp and tie-down parking, hangars and ground handling at Nogales International Airport (KOLS), Nogales, AZ.", fuel_fbo)
    page("flight-training.html", "Flight Training in Nogales, AZ | Copper Mountain Air",
         "FAA Part 61 single-engine flight training is available now at Nogales International Airport (KOLS). Multi-engine training is arriving shortly, and Part 141 certification is in process.", flight_training)
    page("charter.html", "Charter from Nogales, AZ (Coming Soon) | Copper Mountain Air",
         "On-demand charter from Nogales International Airport (KOLS) is coming soon. Join the interest list.", coming_soon_charter)
    page("about.html", "About Copper Mountain Air | Nogales International Airport (KOLS)",
         "Copper Mountain Air, LLC provides fuel, FBO services, FAA Part 61 flight training and cargo at Nogales International Airport in Santa Cruz County, Arizona.", about)
    page("contact.html", "Contact Copper Mountain Air | Nogales, AZ (KOLS)",
         "Contact Copper Mountain Air at Nogales International Airport (KOLS) for fuel, ramp space, hangars, flight training and freight quotes.", contact)
    posts = POSTS
    page("blog/index.html", "Blog | Copper Mountain Air, Nogales International Airport (KOLS)",
         "Airport news, pilot info and freight tips from Copper Mountain Air at Nogales International Airport (KOLS), Arizona.", blog_index(posts))
    for x in posts:
        ld = {"@context":"https://schema.org","@type":"BlogPosting","headline":x["title"],"description":x["description"],
              "author":{"@type":"Organization","name":"Copper Mountain Air, LLC"},"publisher":{"@id":SITE_URL+"#business"},
              "datePublished":"" if x["draft"] else x["date"],"mainEntityOfPage":SITE_URL+"blog/"+x["slug"]+".html"}
        page(f"blog/{x['slug']}.html", f"{'DRAFT: ' if x['draft'] else ''}{x['title']} | Copper Mountain Air", x["description"], blog_post(x), ld, "article")
    for x in UNLISTED:
        page(f"preview/{x['unlisted_token']}/{x.get('unlisted_file') or x['slug']}.html",
             f"PREVIEW: {x['title']} | Copper Mountain Air", x["description"], blog_post(x), None, "article")
    # 404
    page("404.html", "Page not found | Copper Mountain Air", "Page not found.",
         lambda p: page_hero("404", "Off the chart.", "That page isn't here.") + f'<section><div class="wrap"><a class="btn btn-dark" href="{SITE_URL}">Back to home</a></div></section>')
    f404 = os.path.join(OUT, "404.html"); t = open(f404).read()
    open(f404, "w").write(t.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<base href="{SITE_URL}">', 1))
    # sitemap + robots
    urls = [u for u in PAGES if u != "404.html" and not u.startswith("preview/")]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{SITE_URL}{'' if u=='index.html' else u}</loc></url>" for u in urls]
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    robots = ("# PREVIEW: block all crawlers until launch. Remove the Disallow line at launch.\nUser-agent: *\nDisallow: /\n" if PREVIEW
              else "User-agent: *\nAllow: /\n") + f"\nSitemap: {SITE_URL}sitemap.xml\n"
    open(os.path.join(OUT, "robots.txt"), "w").write(robots)
    print("built", len(PAGES), "pages")

if __name__ == "__main__":
    main()

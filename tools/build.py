"""Build the Copper Mountain Air static site.  Run: python3 tools/build.py
Pages are written to _site/ (GitHub Actions deploys that folder). Relative links only,
so the site works at the domain root on coppermountainair.com."""
import os, re, json, html, shutil, sys
import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "_site")                       # build output (deployed by GitHub Actions)
# --drafts renders unpublished posts too, for LOCAL review only. The deploy workflow never passes it.
SHOW_DRAFTS = "--drafts" in sys.argv
SITE_URL = "https://coppermountainair.com/"
PREVIEW = False                                         # True = noindex + preview banner
CONTACT_TO = "operations@coppermountainair.com"
# Contact form relay (Railway service cma-website-contact/contact-api) that emails CONTACT_TO via Resend.
CONTACT_ENDPOINT = "https://contact-api-production-d6d93922.up.railway.app/contact"
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
  # Official FAA Phoenix VFR Sectional crop (not a photo slot — files live in assets/img/charts/).
  "kols-sectional": {
    "alt": "FAA Phoenix VFR Sectional Chart centered on Nogales International Airport (KOLS)",
    "chart_dir": "assets/img/charts",
    "prefix": "kols-sectional",
    "widths": [480, 800, 1200, 1600, 2400],
    "w": 2400,
    "h": 1260,
  },
  "training":   "Yellow taxiway direction signs at Nogales International Airport",
  "charter":    "The runway at Nogales International Airport at dusk",
  "aero-1920":  "Row of 12th Aero Squadron biplanes on the grass at Camp Stephen D. Little near Nogales, 1920 (U.S. Air Service, public domain)",
  "fuel":       {"file": "fuel.svg", "alt": "Placeholder: fuel photo coming soon"},
  # Drop the real photo in as assets/img/josh-berg.jpg and change "file" below to "josh-berg.jpg".
  "josh-berg":  {"file": "josh-berg.svg", "alt": "Photo placeholder: Josh Berg, photo coming"},
}
SIZES = {"full": "100vw", "half": "(min-width: 860px) 50vw, 100vw", "card": "(min-width: 1100px) 380px, (min-width: 700px) 50vw, 100vw",
         "article": "(min-width: 800px) 760px, 100vw", "third": "(min-width: 700px) 33vw, 100vw"}
# Blog figures in assets/img/charts/. Approach plates are clickable full-resolution PNGs.
# The KOLS aerial is a responsive photo (clickable JPEG) with article-fig styling.
CHARTS = {
  "rnav-gps-a": {"file": "kols-rnav-gps-a", "w": 1331, "h": 1935,
                 "alt": "FAA RNAV (GPS)-A instrument approach procedure for Nogales International Airport (KOLS)"},
  "vor-b": {"file": "kols-vor-b", "w": 1331, "h": 1928,
            "alt": "FAA VOR-B instrument approach procedure for Nogales International Airport (KOLS)"},
  "airport-aerial": {"file": "kols-aerial", "w": 3840, "h": 2560,
                     "alt": "Aerial photograph of Nogales International Airport (KOLS) showing Runway 04/22, Taxiway A, and the ramp",
                     "kind": "photo", "full_ext": "jpg", "widths": [480, 800, 1200, 1600, 2400]},
}
def srcset(slot, p, ext):
    m = MANIFEST[slot]
    return ", ".join(f"{p}assets/img/photos/{slot}-{w}.{ext} {w}w" for w in m["widths"])
def srcset_custom(p, directory, prefix, widths, ext):
    return ", ".join(f"{p}{directory}/{prefix}-{w}.{ext} {w}w" for w in widths)
def img(slot, p, cls="", eager=False, sizes="half"):
    v = IMG[slot]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    if isinstance(v, dict) and v.get("chart_dir"):
        sz = SIZES.get(sizes, sizes)
        mid = [w for w in v["widths"] if w >= 1200] or v["widths"][-1:]
        d, prefix = v["chart_dir"], v["prefix"]
        return (f'<picture><source type="image/avif" srcset="{srcset_custom(p, d, prefix, v["widths"], "avif")}" sizes="{sz}">'
                f'<source type="image/webp" srcset="{srcset_custom(p, d, prefix, v["widths"], "webp")}" sizes="{sz}">'
                f'<img src="{p}{d}/{prefix}-{mid[0]}.jpg" srcset="{srcset_custom(p, d, prefix, v["widths"], "jpg")}" sizes="{sz}" alt="{html.escape(v["alt"])}" '
                f'{load} decoding="async" width="{v["w"]}" height="{v["h"]}"{c}></picture>')
    if isinstance(v, dict):
        return f'<img src="{p}assets/img/{v["file"]}" alt="{html.escape(v["alt"])}" {load} decoding="async" width="1200" height="800"{c}>'
    m = MANIFEST[slot]; sz = SIZES.get(sizes, sizes)
    mid = [w for w in m["widths"] if w >= 1200] or m["widths"][-1:]
    return (f'<picture><source type="image/avif" srcset="{srcset(slot, p, "avif")}" sizes="{sz}">'
            f'<source type="image/webp" srcset="{srcset(slot, p, "webp")}" sizes="{sz}">'
            f'<img src="{p}assets/img/photos/{slot}-{mid[0]}.jpg" srcset="{srcset(slot, p, "jpg")}" sizes="{sz}" alt="{html.escape(v)}" '
            f'{load} decoding="async" width="{m["w"]}" height="{m["h"]}"{c}></picture>')

def ph(t): return f'<span class="ph">[{t}]</span>'

# Home is reached from the logo; Cargo has its own page (Seth, Nov 19, 2026).
NAV = [("services.html","Services"),("fuel-fbo.html","Fuel &amp; FBO"),
       ("flight-training.html","Flight Training"),("cargo.html","Cargo"),("charter.html","Charter"),("about.html","About"),
       ("blog/index.html","Blog")]
# Page-specific assets. Leaflet 1.9.4 is vendored in assets/vendor/leaflet (BSD-2-Clause) so the map never depends on a CDN.
PAGE_CSS = {"about.html": ["assets/css/pages.css"], "flight-training.html": ["assets/vendor/leaflet/leaflet.css", "assets/css/pages.css"], "cargo.html": ["assets/css/pages.css"]}
PAGE_JS = {
  "index.html": ["assets/js/flightplan.js"],
  "fuel-fbo.html": ["assets/js/flightplan.js"],
  "flight-training.html": ["assets/vendor/leaflet/leaflet.js", "assets/js/kols.js"],
}

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
{pre}<link rel="stylesheet" href="{p}assets/css/site.css">{''.join(f'\n<link rel="stylesheet" href="{p}{c}">' for c in PAGE_CSS.get(path, []))}
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

SOCIAL = (
    ("Facebook", "https://www.facebook.com/410339535507235",
     '<path d="M22 12.07C22 6.48 17.52 2 11.93 2S1.86 6.48 1.86 12.07c0 5.02 3.66 9.18 8.44 9.93v-7.02H7.9v-2.91h2.4V9.84c0-2.38 1.41-3.69 3.57-3.69 1.03 0 2.12.18 2.12.18v2.33h-1.2c-1.18 0-1.55.73-1.55 1.48v1.78h2.64l-.42 2.91h-2.22V22c4.78-.75 8.44-4.91 8.44-9.93z"/>'),
    ("Instagram", "https://www.instagram.com/copper_mountain_air/",
     '<path d="M7.8 2h8.4A5.8 5.8 0 0 1 22 7.8v8.4A5.8 5.8 0 0 1 16.2 22H7.8A5.8 5.8 0 0 1 2 16.2V7.8A5.8 5.8 0 0 1 7.8 2zm0 1.8A4 4 0 0 0 3.8 7.8v8.4A4 4 0 0 0 7.8 20.2h8.4a4 4 0 0 0 4-4V7.8a4 4 0 0 0-4-4H7.8zM12 7.05A4.95 4.95 0 1 1 7.05 12 4.95 4.95 0 0 1 12 7.05zm0 1.8A3.15 3.15 0 1 0 15.15 12 3.15 3.15 0 0 0 12 8.85zM17.65 6.1a1.2 1.2 0 1 1-1.2 1.2 1.2 1.2 0 0 1 1.2-1.2z"/>'),
    ("TikTok", "https://www.tiktok.com/@copper.mountain.a0",
     '<path d="M14.2 3c.5 2.5 2.1 4.3 4.8 4.6v2.5c-1.6-.05-3.1-.55-4.4-1.4v6.8A6.2 6.2 0 1 1 8.4 9.1v2.7a3.5 3.5 0 1 0 2.4 3.3V3h3.4z"/>'),
)

def social_links():
    items = []
    for name, href, path in SOCIAL:
        items.append(
            f'<a href="{href}" target="_blank" rel="noopener" aria-label="Copper Mountain Air on {name}">'
            f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false">{path}</svg></a>'
        )
    return f'<nav class="social-links" aria-label="Copper Mountain Air on social media">{"".join(items)}</nav>'

def footer(p):
    return f"""</main>
<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div><img src="{p}assets/img/logo-stacked-light.svg" alt="Copper Mountain Air" width="138" height="120" loading="lazy" style="height:120px;width:auto;margin-bottom:1rem">
      <p>Fuel, FBO and cargo at Nogales International Airport (KOLS), serving Nogales and Santa Cruz County, Arizona.</p>
      {social_links()}</div>
    <div><h3>Visit</h3><p>Copper Mountain Air, LLC<br>Nogales International Airport (KOLS)<br>{STREET}<br>Nogales, AZ 85621</p></div>
    <div><h3>Contact</h3><ul><li>Phone: {PHONE_LINK}</li><li><a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a></li><li>Hours: {HOURS_HTML}</li><li><a href="{p}contact.html">Send a message</a></li></ul></div>
    <div><h3>Explore</h3><ul><li><a href="{p}services.html">Services</a></li><li><a href="{p}fuel-fbo.html">Fuel &amp; FBO</a></li><li><a href="{p}flight-training.html">Flight training</a></li><li><a href="{p}cargo.html">Cargo</a></li><li><a href="{p}charter.html">Charter</a></li><li><a href="{p}about.html">About</a></li><li><a href="{p}blog/index.html">Blog</a></li></ul></div>
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
    js = "".join(f'<script src="{p}{s}" defer></script>\n' for s in PAGE_JS.get(path, []))
    if js: out = out.replace(f'<script src="{p}assets/js/site.js" defer></script>\n', f'<script src="{p}assets/js/site.js" defer></script>\n{js}', 1)
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

AIRNAV = 'https://www.airnav.com/airport/KOLS'
# Official FAA Defense Internet NOTAM Service query, pre-filled for KOLS.
NOTAMS = "https://www.notams.faa.gov/dinsQueryWeb/queryRetrievalMapAction.do?reportType=Report&retrieveLocId=KOLS&actionType=notamRetrievalByICAOs&submit=View+NOTAMs"
# Nogales VOR/DME (OLS) 114.65, at field: AirNav navaid page and FAA Chart Supplement SW p. 68, both effective 29 Oct 2026. Type is VOR/DME (not VORTAC).
AIRPORT_FACTS = f"""<div class="facts reveal">
 <div class="fact"><span class="k">Runway</span><span class="v">4/22</span><span class="s">7,200 × 100 ft asphalt</span></div>
 <div class="fact"><span class="k">Elevation</span><span class="v">3,955 ft</span><span class="s">MSL, surveyed</span></div>
 <div class="fact"><span class="k">CTAF / UNICOM</span><span class="v">122.8</span><span class="s">Non-towered field</span></div>
 <div class="fact"><span class="k">ASOS</span><span class="v">121.125</span><span class="s">Weather</span></div>
 <div class="fact"><span class="k">Nogales VOR/DME</span><span class="v">114.65</span><span class="s">Ident OLS, at field</span></div>
 <div class="fact"><span class="k">Fuel on field</span><span class="v">Jet A · 100LL</span><span class="s">From Copper Mountain Air</span></div>
 <div class="fact"><span class="k">Status</span><span class="v">Airport of entry</span><span class="s">International, per FAA data</span></div>
</div>
<p class="source">Source: FAA airport data via <a href="{AIRNAV}" rel="noopener">AirNav (KOLS)</a>, effective 29 Oct 2026. Not for navigation. Check current <a href="{NOTAMS}" target="_blank" rel="noopener">KOLS NOTAMs on the FAA site</a>.</p>"""
FUEL_PRICES = f'Current Jet A and 100LL prices are posted on <a href="{AIRNAV}" rel="noopener">AirNav</a>.'
POSTS = []
UNLISTED = []
def kols_link(p, text):
    """Only link the KOLS guide once that post is published (or in a local --drafts build)."""
    if any(x["slug"] == "kols-pilot-guide" for x in POSTS):
        return f'<p style="margin-top:1.5rem"><a class="btn btn-ghost" href="{p}blog/kols-pilot-guide.html">{text} {ARROW}</a></p>'
    return ""


def flight_plan_widget():
    """Deep links to plan a flight into KOLS. Formats documented in assets/js/flightplan.js."""
    sky_apt = "https://skyvector.com/airport/OLS/Nogales-International-Airport"
    return f"""
<div class="flightplan reveal" id="plan-flight">
  <div class="flightplan-card">
    <p class="eyebrow">Flight planning</p>
    <h2>Plan your flight to KOLS.</h2>
    <p>Enter your departure airport to open a route to Nogales International (KOLS) in ForeFlight, Garmin Pilot or SkyVector. Leave it blank to open KOLS on its own.</p>
    <form id="flightplan-form" class="flightplan-form" action="#plan-flight" method="get">
      <div class="field">
        <label for="dep-icao">Departure airport <span class="hint">(ICAO, optional)</span></label>
        <input id="dep-icao" name="dep" type="text" inputmode="text" autocomplete="off" autocapitalize="characters" spellcheck="false" maxlength="8" placeholder="e.g. KTUS" aria-describedby="dep-hint flightplan-error">
        <p id="dep-hint" class="hint">Use a 3- or 4-character identifier, such as KTUS. Destination is always KOLS.</p>
        <p id="flightplan-error" class="flightplan-error" role="alert" hidden></p>
      </div>
      <div class="flightplan-actions">
        <a class="btn btn-primary" id="fp-foreflight" href="foreflightmobile://maps/search?q=KOLS">Open in ForeFlight</a>
        <a class="btn btn-dark" id="fp-garmin" href="garminpilot://airport?id=KOLS">Open in Garmin Pilot</a>
        <a class="btn btn-dark" id="fp-skyvector" href="{sky_apt}" target="_blank" rel="noopener">Open in SkyVector</a>
      </div>
    </form>
    <p class="note">ForeFlight opens in the app on iPad/iPhone. Garmin Pilot opens in the app on iPad, iPhone or Android. SkyVector opens in your browser on any device.</p>
    <p class="note">Garmin Pilot does not publish an official URL scheme; the route link is a commonly used format and may not load in every version. If it does not, enter the plan in the app or use SkyVector. These links are for planning only and are not a briefing or a filed flight plan.</p>
  </div>
</div>"""

# ---------- HOME ----------
def home(p):
    return f"""
<section class="hero" aria-label="Introduction" style="padding:0">
  <div class="hero-media">{img("hero", p, eager=True, sizes="full")}</div>
  <div class="wrap hero-inner">
    <p class="eyebrow">Nogales International Airport · KOLS</p>
    <h1>Fuel, freight &amp; flight <span class="cu">on the border.</span></h1>
    <p class="lede">Copper Mountain Air keeps Southern Arizona moving: Jet A and Avgas on the ramp, FBO service at KOLS, Part 61 flight training, and air and ground cargo out of Nogales.</p>
    <div class="actions"><a class="btn btn-primary" href="{p}contact.html">Get in touch {ARROW}</a><a class="btn btn-ghost" href="{p}fuel-fbo.html">Fuel &amp; FBO</a><a class="btn btn-ghost" href="#plan-flight">Plan your flight</a></div>
    <div class="hero-strip"><span>Jet A</span><span>100LL Avgas</span><span>FBO</span><span>Flight training</span><span>Air &amp; ground cargo</span><span>Santa Cruz County, AZ</span></div>
  </div>
</section>

<section><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">What we do</p><h2>One stop at KOLS.</h2><p>Whether you're fueling up on a cross-country, parking for the night or moving a time-critical load, start here.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="media">{img("fuel", p, sizes="card")}</div><div class="body"><span class="num">01</span><h3>Fuel</h3><p>Jet A and 100LL Avgas at Nogales International. {FUEL_PRICES}</p><a class="more" href="{p}fuel-fbo.html">Fuel details {ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{img("fbo", p, sizes="card")}</div><div class="body"><span class="num">02</span><h3>FBO services</h3><p>Ground handling, ramp and tie-down parking, and hangar space on the field.</p><a class="more" href="{p}fuel-fbo.html#fbo">FBO services {ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{img("cargo", p, sizes="card")}</div><div class="body"><span class="num">03</span><h3>Cargo &amp; freight</h3><p>Time-critical freight out of Nogales by air and ground, including on-demand expedited freight.</p><a class="more" href="{p}cargo.html">Cargo services {ARROW}</a></div></article>
  </div>
</div></section>

<figure class="photo-band">{img("ramp-band", p, sizes="full")}<figcaption>Hangars at KOLS</figcaption></figure>

<section class="dark"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Flying in?</p><h2>Nogales International at a glance.</h2><p>A 7,200-foot runway at the foot of the Santa Cruz Valley, about 7 miles northeast of downtown Nogales.</p></div>
  {AIRPORT_FACTS}
  {flight_plan_widget()}
  {kols_link(p, "Read the KOLS pilot guide")}
</div></section>

<section><div class="wrap split">
  <div class="frame reveal">{img("training", p)}</div>
  <div class="reveal"><p class="eyebrow">Flight training</p><h2>Learn to fly at KOLS.</h2>
    <p>FAA Part 61 single-engine flight training is available now at Nogales International Airport. Multi-engine training is arriving shortly, and FAA Part 141 flight school certification is in process.</p>
    <p>On-demand charter is coming soon and is not yet offered.</p>
    <p><a class="btn btn-dark" href="{p}contact.html?topic=Flight%20training">Start flight training {ARROW}</a></p>
    <p><a href="{p}flight-training.html">Flight training</a> · <a href="{p}cargo.html">Cargo</a> · <a href="{p}charter.html">Charter</a></p></div>
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
    <p style="display:flex;gap:.6rem;flex-wrap:wrap"><a class="btn btn-dark" href="{p}cargo.html">Cargo &amp; fleet details {ARROW}</a><a class="btn" style="border-color:#d9c9b5;color:var(--ink)" href="{p}contact.html?topic=Cargo%20%2F%20freight">Request a freight quote</a></p></div>
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
      <p>26-foot dock-height with liftgate</p>
      <ul class="checks">
        <li>Cargo box length: 26 ft (dock-height)</li>
        <li>Liftgate for ground-level loading and delivery</li>
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
  {flight_plan_widget()}
  {kols_link(p, "Full KOLS pilot guide")}
</div></section>
{cta(p, "Inbound to KOLS?", f"Let us know your ETA and fuel needs. Phone: {PHONE_LINK}")}"""

# ---------- FLIGHT TRAINING + CARGO (aviation pages) ----------
# KOLS data verified 2026-11-19 against the FAA Chart Supplement (SW, 29 Oct–24 Dec 2026, p. 68) and AirNav KOLS.
# Destination airports: coordinates from AirNav (FAA data); airspace/tower from the same Chart Supplement cycle.
# Distances are great-circle NM from the KOLS ARP; magnetic course uses KOLS 9°E variation. Not for navigation.
FLIGHTCIRCLE = "https://www.flightcircle.com/v1/"
KOLS = {"lat": 31.4177222, "lon": -110.8478889, "elev": "3,955"}
XC = [
  ("KFHU", "Sierra Vista Muni–Libby AAF", 31.5884611, -110.3443750, True,  "Class D (Libby Tower 124.95, weekday hours; Class G other times)", "Closest towered field: joint civil/military Class D practice."),
  ("KTUS", "Tucson International",        32.1170703, -110.9414625, True,  "Class C (Tucson Tower 118.3)", "Class C radar services and big-airport towered ops."),
  ("E95",  "Benson Muni",                 31.9994444, -110.3579722, False, "Non-towered · CTAF/UNICOM 122.8", "Non-towered cross-country stop in the San Pedro Valley."),
  ("KRYN", "Ryan Field",                  32.1422111, -111.1745792, True,  "Class D 6 a.m.–8 p.m. MST (Tower 125.8)", "Towered Class D practice west of Tucson."),
  ("KAVQ", "Marana Regional",             32.4095556, -111.2183889, False, "Non-towered · CTAF/UNICOM 123.0", "More than 50 NM straight-line: a qualifying long cross-country leg."),
  ("KDUG", "Bisbee Douglas International", 31.4689444, -109.6037500, False, "Non-towered · CTAF/UNICOM 123.0 (Class E 6 a.m.–9 p.m. MST)", "More than 50 NM straight-line: a qualifying long cross-country leg."),
]
def _gc(lat1, lon1, lat2, lon2):
    import math
    p1, p2 = math.radians(lat1), math.radians(lat2); dl = math.radians(lon2 - lon1)
    d = 2 * 3440.065 * math.asin(math.sqrt(math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2))
    b = (math.degrees(math.atan2(math.sin(dl) * math.cos(p2), math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl))) + 360) % 360
    return d, b
def xc_data():
    out = []
    for i, n, la, lo, twr, asp, why in XC:
        d, b = _gc(KOLS["lat"], KOLS["lon"], la, lo)
        out.append({"id": i, "name": n, "lat": la, "lon": lo, "towered": twr, "airspace": asp, "why": why,
                    "dist": round(d), "tc": f"{round(b) % 360:03d}", "mc": f"{round(b - 9) % 360:03d}"})
    return out

def ico(name):
    P = {
      "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
      "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
      "runway": '<path d="M9 2 5 22M15 2l4 20M12 4v3M12 10v3M12 16v3"/>',
      "mountain": '<path d="m3 20 6-11 4 6 2-3 6 8z"/><path d="M9 9 7.5 12"/>',
      "tower": '<path d="M8 22h8M10 22l1-11h2l1 11M7 8h10l-1 3H8zM12 2v6M9 5h6"/>',
      "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
      "compass": '<circle cx="12" cy="12" r="10"/><path d="m16.2 7.8-2.1 6.3-6.3 2.1 2.1-6.3z"/>',
      "fuel": '<path d="M3 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18M3 22h12M3 10h12M15 13h2a2 2 0 0 1 2 2v3a1.5 1.5 0 0 0 3 0V9l-3-3"/>',
      "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
      "truck": '<path d="M1 4h14v12H1zM15 9h4l3 3v4h-7z"/><circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="18.5" r="2"/>',
      "map": '<path d="m1 6 7-4 8 4 7-4v16l-7 4-8-4-7 4z"/><path d="M8 2v16M16 6v16"/>',
      "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
      "box": '<path d="m21 16-9 5-9-5V8l9-5 9 5z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
      "ext": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'

def wind_rose():
    import math
    c, R = 160, 140
    ticks = []
    for d in range(0, 360, 10):
        r1 = R - (14 if d % 30 == 0 else 7)
        a = math.radians(d)
        ticks.append(f'<line x1="{c + R*math.sin(a):.1f}" y1="{c - R*math.cos(a):.1f}" x2="{c + r1*math.sin(a):.1f}" y2="{c - r1*math.cos(a):.1f}" stroke="{"#e9a06a" if d % 90 == 0 else "rgba(230,237,241,.45)"}" stroke-width="{2 if d % 30 == 0 else 1}"/>')
    labels = []
    for d in range(0, 360, 30):
        a = math.radians(d); r = R - 28
        t = {0: "N", 90: "E", 180: "S", 270: "W"}.get(d, f"{d//10:02d}")
        labels.append(f'<text x="{c + r*math.sin(a):.1f}" y="{c - r*math.cos(a) + 5:.1f}" text-anchor="middle" font-size="{15 if d % 90 == 0 else 11}" fill="{"#e9a06a" if d % 90 == 0 else "#9fb0ba"}">{t}</text>')
    def at(b, r):
        a = math.radians(b); return c + r*math.sin(a), c - r*math.cos(a)
    x04, y04 = at(217, 70); x22, y22 = at(37, 70)
    return f'''<svg class="rose" viewBox="0 0 320 336" role="img" aria-label="Wind rose for KOLS Runway 04/22, drawn to magnetic north, with the live wind direction">
<defs><radialGradient id="rg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#14303f"/><stop offset="1" stop-color="#071017"/></radialGradient>
<marker id="ah" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" fill="#e9a06a"/></marker></defs>
<circle cx="160" cy="160" r="150" fill="url(#rg)" stroke="rgba(233,160,106,.35)"/>
<circle cx="160" cy="160" r="70" fill="none" stroke="rgba(230,237,241,.08)"/>
{''.join(ticks)}{''.join(labels)}
<g transform="rotate(37 160 160)"><rect x="146" y="66" width="28" height="188" rx="2" fill="#2a3640" stroke="#c9d4da" stroke-width="1.2"/>
<line x1="160" y1="104" x2="160" y2="216" stroke="#fff" stroke-width="1.5" stroke-dasharray="8 7"/>
<rect x="148" y="66" width="24" height="4" fill="#fff" opacity=".8"/><rect x="148" y="250" width="24" height="4" fill="#fff" opacity=".8"/></g>
<text class="rwy-end" data-rwy="04" x="{x04:.1f}" y="{y04 + 5:.1f}" text-anchor="middle" transform="rotate(37 {x04:.1f} {y04:.1f})">04</text>
<text class="rwy-end" data-rwy="22" x="{x22:.1f}" y="{y22 + 5:.1f}" text-anchor="middle" transform="rotate(217 {x22:.1f} {y22:.1f})">22</text>
<g id="wind-arrow" opacity="0" style="transition:transform .8s cubic-bezier(.2,.7,.2,1)"><line x1="160" y1="22" x2="160" y2="112" stroke="#e9a06a" stroke-width="5" stroke-linecap="round" marker-end="url(#ah)"/><circle cx="160" cy="22" r="6" fill="#e9a06a"/></g>
<circle cx="160" cy="160" r="4" fill="#e9a06a"/>
<text id="wind-label" x="160" y="331" text-anchor="middle" font-size="12" fill="#e6edf1">LOADING…</text>
<text x="300" y="20" text-anchor="end" font-size="10" fill="#9fb0ba">MAG</text>
</svg>'''

def flight_training(p):
    xc = xc_data()
    xc_json = json.dumps({"kols": KOLS, "dest": xc}).replace("</", "<\\/")
    fc = f'<a class="btn btn-glass" href="{FLIGHTCIRCLE}" target="_blank" rel="noopener">Student portal · FlightCircle {ARROW}</a>'
    xc_btns = "".join(f'<button class="xc" type="button" data-goto="{d["id"]}"><span class="id">{d["id"]}</span><span class="nm">{html.escape(d["name"])}</span><span class="d">{d["dist"]} NM<small>{d["mc"]}° mag</small></span><span class="as">{html.escape(d["airspace"])}</span></button>' for d in sorted(xc, key=lambda d: d["dist"]))
    steps = [
      ("01", "Discovery flight", "ask", "Call to schedule", "Your first lesson.", "Meet the airplane and fly it yourself with an instructor beside you, right here at KOLS. It's the easiest way to find out if flight training is for you.", ["Fly from a 7,200-ft runway", "See the Santa Cruz Valley from the air", "Talk through your goals, schedule and next steps"]),
      ("02", "Private pilot", "now", "Part 61 · Enrolling now", "Earn your private pilot certificate.", "FAA Part 61 single-engine training, available now at Nogales International. Train at your own pace with a schedule built around you.", ["Ground and flight training toward the FAA private pilot certificate", "Cross-country flying across Southern Arizona", "Towered Class C and Class D practice within about 50 NM"]),
      ("03", "Instrument rating", "ask", "Ask about availability", "Fly by the instruments.", "KOLS has a VOR/DME on the field plus RNAV (GPS)-A and VOR-B approaches, with Tucson Approach overhead. Ask us about instrument training.", ["On-field Nogales VOR/DME (114.65)", "Published RNAV (GPS)-A and VOR-B approaches", "Tucson Approach and Center services nearby"]),
      ("04", "Commercial pilot", "ask", "Ask about availability", "Take the next step.", "Ask us about commercial pilot training under Part 61 and how it fits with what you've already logged.", ["Build on your private and instrument training", "Real high-elevation and mountain flying", "Long cross-country legs to KDUG and KAVQ"]),
      ("05", "Multi-engine", "soon", "Arriving shortly", "Add a second engine.", "Multi-engine training is arriving shortly at Copper Mountain Air. Join the list and we'll reach out as soon as it opens.", ["Multi-engine add-on rating", "Join the interest list today", "Part 141 certification is in process"]),
      ("06", "Flight reviews & proficiency", "ask", "Ask about availability", "Stay sharp and current.", "Already a pilot? Ask us about flight reviews, proficiency flying and getting comfortable at a high-elevation, non-towered airport.", ["Flight reviews and proficiency flights", "Density-altitude and mountain-airport practice", "Non-towered pattern work on Runway 04/22"]),
    ]
    tabs = "".join(f'<button class="tab" role="tab" id="tab-{n}" aria-controls="tp-{n}" aria-selected="{"true" if i == 1 else "false"}" tabindex="{0 if i == 1 else -1}"><span class="n">{n}</span>{t}</button>' for i, (n, t, *_r) in enumerate(steps))
    panels = "".join(f'''<div class="tabpanel" role="tabpanel" id="tp-{n}" aria-labelledby="tab-{n}"{"" if i == 1 else " hidden"}>
  <div class="tp-body"><span class="status-badge {st}">{stl}</span><h3 style="font-size:clamp(1.5rem,3vw,2.1rem)">{h}</h3><p style="color:var(--muted);font-size:1.08rem">{d}</p>
    <p style="margin:1.4rem 0 0;display:flex;gap:.6rem;flex-wrap:wrap"><a class="btn btn-dark" href="{p}contact.html?topic=Flight%20training">Ask about {t.lower()} {ARROW}</a><a class="btn" style="border-color:#d9c9b5;color:var(--ink)" href="{PHONE_HREF}">Call {PHONE}</a></p></div>
  <div class="tp-side" data-step="{n}"><h4>What it looks like at KOLS</h4><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul></div>
</div>''' for i, (n, t, st, stl, h, d, li) in enumerate(steps))
    return f"""
<section class="xhero" aria-label="Flight training at KOLS">
  <div class="hero-media">{img("charter", p, eager=True, sizes="full")}</div><div class="grid-lines" aria-hidden="true"></div>
  <div class="wrap">
    <div class="xhero-inner">
      <div>
        <ul class="chips" aria-label="Training status">
          <li class="chip live"><i></i>FAA Part 61 · Enrolling now</li><li class="chip"><i></i>Single-engine · Active</li>
          <li class="chip soon"><i></i>Multi-engine · Arriving soon</li><li class="chip proc"><i></i>Part 141 · In process</li></ul>
        <p class="eyebrow">Flight Training · Nogales International · KOLS</p>
        <h1>Learn to fly <span class="cu">where the sky opens up.</span></h1>
        <p class="lede">FAA Part 61 single-engine flight training on a 7,200-foot runway at the foot of the Santa Cruz Valley. Non-towered, high-elevation and minutes from Tucson's Class C airspace, so you build real-world airmanship from your very first lesson.</p>
        <div class="actions"><a class="btn btn-primary" href="{p}contact.html?topic=Flight%20training" id="start-training">Start flight training {ARROW}</a>{fc}</div>
      </div>
      <aside class="livecard" aria-label="Live KOLS field status">
        <div class="top"><span class="tag">Live field status</span><span class="status" data-wx="status">Loading live KOLS data…</span></div>
        <div class="catbig"><span class="c" data-wx="cat">—</span><span class="w">Flight category</span></div>
        <div class="pill"><span class="led"></span><span data-wx="pill">KOLS · ASOS 121.125</span></div>
        <div class="mini"><div><span>Wind</span><b data-wx="wind">—</b></div><div><span>Visibility</span><b><span data-wx="vis">—</span> SM</b></div><div><span>Density alt</span><b data-wx="da">—</b></div></div>
        <a class="more" href="#conditions">Full ASOS panel ↓</a>
      </aside>
    </div>
    <div class="qstrip">
      <div><span>Field elevation</span><b>3,955 ft</b><small>MSL, surveyed</small></div>
      <div><span>Runway 04/22</span><b>7,200 × 100</b><small>ft · asphalt · MIRL</small></div>
      <div><span>CTAF / UNICOM</span><b>122.8</b><small>Non-towered field</small></div>
      <div><span>ASOS</span><b>121.125</b><small>520-287-9332</small></div>
      <div><span>Nogales VOR/DME</span><b>114.65</b><small>Ident OLS, at field</small></div>
      <div><span>Tucson Approach</span><b>118.75</b><small>App / Dep</small></div>
    </div>
  </div>
</section>

<section class="cockpit" id="conditions" aria-label="Live KOLS conditions"><div class="wrap" id="wx">
  <div class="section-head reveal"><p class="eyebrow">Live conditions · KOLS ASOS</p><h2>What the field is doing right now.</h2><p>Live observations from the Nogales International ASOS, refreshed every five minutes, with flight category, runway wind components and density altitude worked out for you.</p></div>
  <div class="catbar" role="list" aria-label="FAA flight categories">
    <div class="cat" role="listitem" data-cat="VFR"><b>VFR</b><span>Ceiling above 3,000 ft and visibility above 5 SM</span></div>
    <div class="cat" role="listitem" data-cat="MVFR"><b>MVFR</b><span>Ceiling 1,000–3,000 ft or visibility 3–5 SM</span></div>
    <div class="cat" role="listitem" data-cat="IFR"><b>IFR</b><span>Ceiling 500 to below 1,000 ft or visibility 1 to below 3 SM</span></div>
    <div class="cat" role="listitem" data-cat="LIFR"><b>LIFR</b><span>Ceiling below 500 ft or visibility below 1 SM</span></div>
  </div>
  <div class="panel-grid">
    <div class="glass"><h3>Runway 04/22 wind <small>Drawn to magnetic north</small></h3>
      {wind_rose()}
      <div class="comps"><div><span>Favored</span><b data-wx="rwy">—</b></div><div><span>Head / tail</span><b data-wx="head">—</b></div><div><span>Crosswind</span><b data-wx="cross">—</b></div></div>
      <p class="comps-sub" data-wx="rwy-sub"></p>
    </div>
    <div class="glass"><h3>ASOS readouts <small data-wx="ago"></small></h3>
      <div class="readouts">
        <div class="ro"><span>Wind</span><b data-wx="wind">—</b><small data-wx="wind-sub">&nbsp;</small></div>
        <div class="ro"><span>Visibility</span><b><span data-wx="vis">—</span> SM</b><small>Statute miles</small></div>
        <div class="ro"><span>Sky / ceiling</span><b data-wx="sky">—</b><small data-wx="sky-sub">&nbsp;</small></div>
        <div class="ro"><span>Temperature</span><b data-wx="temp">—</b><small data-wx="dew">&nbsp;</small></div>
        <div class="ro"><span>Altimeter</span><b data-wx="alt">—</b><small data-wx="alt-sub">inHg</small></div>
        <div class="ro hl"><span>Density altitude</span><b data-wx="da">—</b><small data-wx="da-sub">From field elevation, altimeter and temperature</small></div>
      </div>
      <div class="metar">
        <div><code data-wx="metar">Loading the latest KOLS METAR…</code><div class="meta">Observed <b data-wx="time">—</b> · <span data-wx="status"></span> <span data-wx="src"></span></div><div class="meta" data-wx="sample"></div></div>
        <div class="btns"><button class="mbtn" type="button" id="wx-refresh">↻ Refresh</button><button class="mbtn" type="button" id="wx-copy">Copy METAR</button><a class="mbtn" href="https://aviationweather.gov/data/metar/?ids=KOLS&amp;hours=0&amp;include_taf=yes" target="_blank" rel="noopener">AviationWeather.gov</a></div>
      </div>
    </div>
  </div>
  <div class="infocard">
    <div class="glass"><h3>KOLS airfield <small>FAA Chart Supplement, 29 Oct 2026 cycle</small></h3>
      <dl class="dl">
        <dt>Runway</dt><dd><b>04/22</b> · 7,200 × 100 ft asphalt · 1.6% up to the northeast · magnetic headings 037° / 217°</dd>
        <dt>Lighting</dt><dd>Medium-intensity runway lights (MIRL), pilot-activated on CTAF 122.8 · REIL both ends · rotating beacon</dd>
        <dt>Glidepath</dt><dd>4-light PAPI on the left: 3.0° Runway 04, 4.0° Runway 22</dd>
        <dt>Pattern</dt><dd>Left traffic both runways · Runway 22 is the calm-wind runway · Runway 22 threshold displaced 899 ft · Runway 04 touch-and-go not authorized</dd>
        <dt>Elevation</dt><dd>3,955 ft MSL (surveyed) · variation 9° E</dd>
        <dt>Approaches</dt><dd>RNAV (GPS)-A · VOR-B · Nogales VOR/DME (OLS) 114.65 on the field</dd>
        <dt>On field</dt><dd>Phillips 66 Jet A and 100LL, full service from Copper Mountain Air · {WINGPOINTS} · attended 7 a.m.–7 p.m.</dd>
        <dt>Entry</dt><dd>International airport of entry (U.S. Customs and Border Protection)</dd>
      </dl>
    </div>
    <div class="glass"><h3>Frequencies &amp; phones</h3>
      <div class="freqs">
        <div class="freq"><span>ASOS</span><b>121.125</b><small><a href="tel:+15202879332">520-287-9332</a></small></div>
        <div class="freq"><span>CTAF / UNICOM</span><b>122.8</b><small>Pilot-controlled lighting</small></div>
        <div class="freq"><span>Nogales VOR/DME</span><b>114.65</b><small>Ident OLS, at field</small></div>
        <div class="freq"><span>Tucson App / Dep</span><b>118.75</b><small>Clearance: <a href="tel:+15208296121">520-829-6121</a></small></div>
        <div class="freq"><span>Prescott Radio</span><b>122.4</b><small>RCO · close flight plans</small></div>
      </div>
      <p class="wx-foot">Weather: FAA ASOS via the <a href="https://www.weather.gov/documentation/services-web-api" target="_blank" rel="noopener">National Weather Service API</a> and the <a href="https://mesonet.agron.iastate.edu/" target="_blank" rel="noopener">Iowa Environmental Mesonet</a>. Airport data: FAA Chart Supplement and <a href="{AIRNAV}" target="_blank" rel="noopener">AirNav KOLS</a>. For situational awareness and training preview only. Not for navigation; get an official briefing before every flight.</p>
    </div>
  </div>
</div></section>

<section class="mapsec" id="map" aria-label="Training area map"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">FAA VFR Sectional · Training corridor</p><h2>Your classroom is Southern Arizona.</h2><p>Live FAA charts centered on Nogales International. Switch between the VFR Sectional, IFR Enroute Low, satellite and terrain, and tap a destination to see the cross-country leg.</p></div>
  <div class="mapwrap">
    <div><div id="kols-map" role="region" aria-label="Interactive FAA sectional chart map centered on KOLS"></div>
      <div class="legend"><span><i style="background:var(--copper)"></i>KOLS · home base</span><span><i style="background:#1d4ed8"></i>Towered (Class C/D)</span><span><i style="background:#7c3aed"></i>Non-towered</span><span><i class="ring"></i>25 / 50 NM rings</span></div>
      <div class="disclaimer">⚠ <span>Situational awareness and planning preview only. Not for navigation. Use current FAA charts and an official weather briefing for flight planning.</span></div>
    </div>
    <div class="xc-list" aria-label="Cross-country destinations">
      <button class="xc" type="button" data-goto="KOLS"><span class="id">KOLS</span><span class="nm">Nogales International · home base</span><span class="d">0 NM<small>3,955 ft</small></span><span class="as">Non-towered · CTAF 122.8 · ASOS 121.125</span></button>
      {xc_btns}
      <p class="wx-foot" style="margin:0">Straight-line distance and magnetic course from KOLS (9° E variation). Airspace and tower hours per the FAA Chart Supplement.</p>
    </div>
  </div>
</div>
<script type="application/json" id="xc-data">{xc_json}</script>
</section>

<section aria-label="Pilot training pathway"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Your pathway</p><h2>From first flight to the right seat.</h2><p>Pick where you are today. Part 61 single-engine training is available now; tap a step to see what it looks like at KOLS.</p></div>
  <div class="tabs" role="tablist" aria-label="Training steps">{tabs}</div>
  {panels}
  <div class="road" aria-hidden="true"><div><b>Discovery</b>First lesson</div><div><b>Private</b>Part 61 · now</div><div><b>Instrument</b>Ask us</div><div><b>Commercial</b>Ask us</div><div class="soon"><b>Multi-engine</b>Arriving shortly</div><div><b>Proficiency</b>Ask us</div></div>
  <div class="matrix">
    <div class="mx now"><span class="st">● Available now</span><h3>FAA Part 61 single-engine</h3><p>Flight training on the field at Nogales International Airport (KOLS).</p></div>
    <div class="mx soon"><span class="st">● Arriving shortly</span><h3>Multi-engine training</h3><p>Join the interest list and we'll reach out when it opens.</p></div>
    <div class="mx proc"><span class="st">● In process</span><h3>FAA Part 141 flight school</h3><p>Part 141 certification is currently in process.</p></div>
  </div>
</div></section>

<section class="dark" aria-label="Why train at KOLS"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Why Nogales?</p><h2>Why train at KOLS.</h2><p>Real-world flying from day one, without the congestion of a big-city airport.</p></div>
  <div class="why reveal">
    <div><span class="ic">{ico("runway")}</span><h3>A 7,200-ft runway, no tower lines</h3><p>Non-towered with <b>7,200 × 100 ft</b> of asphalt, so more of your lesson is spent flying and less waiting in line to take off.</p></div>
    <div><span class="ic">{ico("mountain")}</span><h3>High-elevation airmanship</h3><p>At <b>3,955 ft</b> field elevation with mountains all around, you learn density altitude and mountain flying for real, not just from a textbook.</p></div>
    <div><span class="ic">{ico("tower")}</span><h3>Towered airspace next door</h3><p>Sierra Vista (Class D) is <b>{xc[0]["dist"]} NM</b> away and Tucson International (Class C) is <b>{next(d for d in xc if d["id"]=="KTUS")["dist"]} NM</b>, an easy hop for radio and towered-airport practice.</p></div>
    <div><span class="ic">{ico("compass")}</span><h3>Instrument-ready field</h3><p>A <b>VOR/DME on the field</b>, published RNAV (GPS)-A and VOR-B approaches, and Tucson Approach overhead.</p></div>
    <div><span class="ic">{ico("sun")}</span><h3>Desert flying weather</h3><p>Southern Arizona's dry climate means flyable weather much of the year, and the live panel above shows you exactly what it's doing today.</p></div>
    <div><span class="ic">{ico("fuel")}</span><h3>Full-service FBO on the field</h3><p>Phillips 66 Jet A and 100LL, a pilot lounge and flight-planning desk, all from Copper Mountain Air at KOLS.</p></div>
  </div>
</div></section>

<figure class="photo-band">{img("kols-guide", p, sizes="full")}<figcaption>Runway 4-22 at KOLS</figcaption></figure>

<section aria-label="Student portal"><div class="wrap">
  <div class="fcband reveal">
    <div><p class="eyebrow">Students · FlightCircle</p><h2>Schedule and manage your training online.</h2><p>Copper Mountain Air uses FlightCircle for flight school scheduling and student accounts. Current students can sign in any time. New students: call or email us and we'll get your FlightCircle account set up.</p></div>
    <div class="btns"><a class="btn btn-primary" href="{FLIGHTCIRCLE}" target="_blank" rel="noopener">Sign in to FlightCircle {ARROW}</a><a class="btn btn-ghost" href="{p}contact.html?topic=Flight%20training">New student? Start here</a></div>
  </div>
</div></section>
{cta(p, "Ready to fly?", f'Call {PHONE_LINK} or email <a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a> and we’ll help you get started at KOLS.')}"""

def truck_svg(kind):
    if kind == "box":
        return '''<svg viewBox="0 0 520 210" role="img" aria-label="Illustration of a 26-foot box truck with a liftgate">
<defs><linearGradient id="bx" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f4e7d6"/><stop offset="1" stop-color="#d9c4aa"/></linearGradient><linearGradient id="cb" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#e9a06a"/><stop offset="1" stop-color="#c4703d"/></linearGradient></defs>
<ellipse cx="260" cy="192" rx="250" ry="8" fill="rgba(0,0,0,.45)"/>
<rect x="18" y="26" width="350" height="136" rx="6" fill="url(#bx)"/>
<rect x="18" y="26" width="350" height="12" rx="4" fill="#c9b293"/>
<g stroke="rgba(13,27,36,.12)" stroke-width="2">''' + "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="160"/>' for x in range(60, 368, 44)) + '''</g>
<text x="193" y="104" text-anchor="middle" font-family="Archivo,Arial" font-weight="900" font-size="26" fill="#0d1b24" letter-spacing="3">26 FT BOX</text>
<rect x="6" y="160" width="20" height="12" fill="#3a4a55"/><rect x="0" y="170" width="44" height="6" rx="2" fill="#86efac"/>
<text x="22" y="200" text-anchor="middle" font-family="Inter,Arial" font-weight="700" font-size="11" fill="#86efac">LIFTGATE</text>
<path d="M372 70h70c14 0 22 6 30 18l26 38c5 7 8 14 8 22v14H372z" fill="url(#cb)"/>
<path d="M386 82h52c8 0 13 3 18 10l18 28h-88z" fill="#0d1b24" opacity=".85"/>
<rect x="368" y="160" width="142" height="12" rx="3" fill="#2a3640"/><rect x="18" y="160" width="350" height="10" fill="#2a3640"/>
<g fill="#0d1b24"><circle cx="90" cy="174" r="22"/><circle cx="140" cy="174" r="22"/><circle cx="440" cy="174" r="22"/></g>
<g fill="#9fb0ba"><circle cx="90" cy="174" r="9"/><circle cx="140" cy="174" r="9"/><circle cx="440" cy="174" r="9"/></g>
<rect x="496" y="134" width="12" height="8" rx="2" fill="#fde68a"/>
</svg>'''
    return '''<svg viewBox="0 0 520 210" role="img" aria-label="Illustration of a full-size cargo van">
<defs><linearGradient id="vn" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f4e7d6"/><stop offset="1" stop-color="#d9c4aa"/></linearGradient></defs>
<ellipse cx="260" cy="192" rx="210" ry="8" fill="rgba(0,0,0,.45)"/>
<path d="M60 52c0-10 8-18 18-18h250c14 0 24 5 32 14l50 52c22 4 46 10 54 20 6 8 8 18 8 30v22H60z" fill="url(#vn)"/>
<path d="M340 52h12c8 0 14 3 19 8l40 44h-71z" fill="#0d1b24" opacity=".85"/>
<line x1="230" y1="40" x2="230" y2="158" stroke="rgba(13,27,36,.18)" stroke-width="2"/><line x1="335" y1="44" x2="335" y2="158" stroke="rgba(13,27,36,.18)" stroke-width="2"/>
<rect x="60" y="120" width="412" height="8" fill="#c4703d"/>
<text x="150" y="100" text-anchor="middle" font-family="Archivo,Arial" font-weight="900" font-size="22" fill="#0d1b24" letter-spacing="3">HOT SHOT</text>
<rect x="56" y="156" width="420" height="14" rx="4" fill="#2a3640"/>
<g fill="#0d1b24"><circle cx="130" cy="172" r="22"/><circle cx="400" cy="172" r="22"/></g>
<g fill="#9fb0ba"><circle cx="130" cy="172" r="9"/><circle cx="400" cy="172" r="9"/></g>
<rect x="462" y="130" width="12" height="8" rx="2" fill="#fde68a"/>
</svg>'''

def cargo(p):
    q = f"{p}contact.html?topic=Cargo%20%2F%20freight"
    return f"""
<section class="xhero cargo-hero" aria-label="Cargo from KOLS" style="min-height:min(86vh,820px)">
  <div class="hero-media">{img("cargo-sign", p, eager=True, sizes="full")}</div><div class="grid-lines" aria-hidden="true"></div>
  <div class="wrap">
    <div class="xhero-inner" style="grid-template-columns:1fr">
      <div>
        <ul class="chips" aria-label="Cargo capabilities"><li class="chip live"><i></i>Dispatch from KOLS</li><li class="chip"><i></i>Liftgate box truck</li><li class="chip"><i></i>Cargo van hot shots</li><li class="chip"><i></i>Ramp-to-truck</li></ul>
        <p class="eyebrow">Cargo · Nogales International Airport · KOLS</p>
        <h1>Freight that <span class="cu">can't wait.</span></h1>
        <p class="lede">Expedited ground and air-to-ground cargo from Nogales International Airport, right on the Nogales, Rio Rico and Santa Cruz County border corridor. Dock-to-dock, liftgate and ramp-to-truck moves, dispatched by our own team at KOLS.</p>
        <div class="actions"><a class="btn btn-primary" href="{PHONE_HREF}">Call dispatch · {PHONE} {ARROW}</a><a class="btn btn-glass" href="{q}">Request a freight quote</a></div>
      </div>
    </div>
    <div class="qstrip">
      <div><span>Box truck</span><b>Hino 268</b><small>26-ft dock-height · liftgate</small></div>
      <div><span>Cargo van</span><b>Ford E-150</b><small>Hot-shot and small loads</small></div>
      <div><span>Based at</span><b>KOLS</b><small>Nogales, AZ 85621</small></div>
      <div><span>Hours</span><b>7 days</b><small>Mon–Sat 7–7 · Sun 7–5</small></div>
    </div>
  </div>
</section>

<section aria-label="Cargo capabilities"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">What we move</p><h2>Ramp, dock and door.</h2><p>When a shipment can't wait for the next scheduled truck, call us. We handle time-critical freight out of Nogales by ground and coordinate air cargo on the ramp at KOLS.</p></div>
  <div class="caps">
    <article class="cap reveal"><span class="ic">{ico("plane")}</span><h3>Ramp-to-truck at KOLS</h3><p>Air cargo coordination and ramp handling on the field, with freight moved straight from the aircraft to our truck.</p></article>
    <article class="cap reveal"><span class="ic">{ico("box")}</span><h3>Nogales &amp; Rio Rico pickups</h3><p>Warehouse, plant and dock pickups across Nogales, Rio Rico and Santa Cruz County.</p></article>
    <article class="cap reveal"><span class="ic">{ico("map")}</span><h3>Southern Arizona &amp; beyond</h3><p>On-demand expedited ground moves across Southern Arizona and beyond.</p></article>
    <article class="cap reveal"><span class="ic">{ico("phone")}</span><h3>Direct dispatch</h3><p>Talk to our operations team at KOLS directly. No call centers, just the people moving your freight.</p></article>
  </div>
</div></section>

<section class="dark" id="fleet" aria-label="Fleet"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Fleet</p><h2>Two trucks, ready to roll.</h2><p>From a single urgent pallet to a full dock-height load.</p></div>
  <div class="fleet">
    <article class="truck reveal">
      <div class="art">{truck_svg("box")}</div>
      <div class="tb"><span class="kick">Box truck</span><h3>Hino 268</h3><p class="lead">26-foot dock-height box with a liftgate, for loading docks and ground-level deliveries alike.</p>
        <span class="feature">✓ Liftgate</span><span class="feature cu">✓ Dock-height</span>
        <div class="specs">
          <div><span>Cargo box</span><b>26 ft</b><small>Dock-height</small></div>
          <div><span>Liftgate</span><b>Yes</b><small>Ground-level loading &amp; delivery</small></div>
          <div><span>GVWR</span><b>25,999 lb</b><small>16,500 lb empty weight</small></div>
          <div><span>Max payload</span><b>Up to 9,499 lb</b><small>Theoretical</small></div>
        </div>
        <p class="note">Actual usable payload accounts for driver, fuel, equipment and axle limits.</p></div>
    </article>
    <article class="truck reveal">
      <div class="art">{truck_svg("van")}</div>
      <div class="tb"><span class="kick">Cargo van</span><h3>Ford E-150</h3><p class="lead">Ideal for urgent hot-shot runs and time-critical small shipments.</p>
        <span class="feature cu">✓ Hot-shot ready</span>
        <div class="specs">
          <div><span>Usable cargo length</span><b>108 in</b><small>9 ft</small></div>
          <div><span>Door opening width</span><b>≈ 55 in</b><small>Approx.</small></div>
          <div><span>Max cargo height</span><b>40 in</b><small>&nbsp;</small></div>
          <div><span>Max payload</span><b>≈ 1,600 lb</b><small>Approx.</small></div>
        </div></div>
    </article>
  </div>
</div></section>

<section aria-label="Request a quote"><div class="wrap split">
  <div class="frame reveal">{img("cargo", p)}</div>
  <div class="reveal"><p class="eyebrow">Get a quote</p><h2>What to send us.</h2>
    <p>Send these details and we'll get back to you with a quote.</p>
    <ul class="checks quote-list"><li>Pickup and delivery locations</li><li>Ready time and required delivery time</li><li>Pieces, dimensions and weight</li><li>Dock, liftgate or ramp handling needed</li><li>Any hazmat or special handling needs</li></ul>
    <div class="dispatch">
      <a href="{PHONE_HREF}"><span class="ic">{ico("phone")}</span><span><span class="lbl">Call dispatch</span><b>{PHONE}</b></span></a>
      <a href="mailto:{CONTACT_TO}?subject=Freight%20quote"><span class="ic">{ico("mail")}</span><span><span class="lbl">Email</span><b>{CONTACT_TO}</b></span></a>
    </div>
  </div>
</div></section>
{cta(p, "Freight that can't wait?", f'Call dispatch at {PHONE_LINK} or email <a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a>. Hours: {HOURS}.')}"""

def coming_soon_charter(p):
    hero = page_hero("Charter", "Fly direct from KOLS.", "An FAA Part 135 on-demand charter program from Nogales International is in development. It is not offered yet.", '<span class="badge soon">Coming soon</span>')
    return hero + f"""
<section><div class="wrap split">
  <div class="frame reveal">{img("charter", p)}</div>
  <div class="reveal"><span class="badge soon">Coming soon</span><h2>On-demand charter is in the works.</h2>
    <p>We're working toward FAA Part 135 on-demand charter from Nogales International. We can't book charter flights yet; join the interest list and we'll reach out when the service opens.</p>
    <a class="btn btn-dark" href="{p}contact.html?topic=Charter%20interest">Join the interest list {ARROW}</a></div>
</div></section>{cta(p, "Questions in the meantime?", "We're happy to talk. Fuel, FBO, cargo and Part 61 flight training are available today.")}"""

# History copy follows /workspace/cma-kols-history-research.md (Nov 19, 2026); every clause is tied to a source listed in HISTORY_SOURCES.
HISTORY_SOURCES = [
  ('Coffman Associates, <em>Airport Master Plan, Nogales International Airport</em>, Santa Cruz County, February 2015 (history chapter and Table 1B, development history)', 'https://web.archive.org/web/20250305003134/https://apps.azdot.gov/files/Airports/MP_PDF/Nogales/Nogales-Master-Plan-2015.pdf'),
  ('U.S. Army Corps of Engineers, Formerly Used Defense Sites: Camp Little; Camp Stephen D. Little historical marker (1978)', 'https://www.spl.usace.army.mil/Missions/Formerly-Used-Defense-Sites/Camp-Little/'),
  ('12th Aero Squadron and the U.S. Army Border Air Patrol (unit lineage, citing Maurer, <em>Aviation in the U.S. Army, 1919–1939</em>)', 'https://en.wikipedia.org/wiki/12th_Reconnaissance_Squadron'),
  ('U.S. Army Air Service photograph, 1920, “12th Aero Squadron at Camp Little near Nogales, Arizona” (public domain, Wikimedia Commons)', 'https://commons.wikimedia.org/wiki/File:12th_Aero_Squadron_-_Nogales_Arizona.jpg'),
  ('Bureau of Air Commerce, <em>Descriptions of Airports and Landing Fields in the United States</em> (1937), via the Davis-Monthan Airfield Register', 'https://dmairfield.org/places/nogales_az/index.html'),
  ('United States Code, 1946 supplement, airports of entry list; and 19 CFR § 122.13 (current)', 'https://www.ecfr.gov/current/title-19/chapter-I/part-122/subpart-B/section-122.13'),
  ('Historic airline records: Cavalcade of Wings (Arizona Airways; Frontier Airlines); The Airport Historian (Douglas, AZ); Departed Flights, OLS timetable of April 1, 1981', 'https://www.departedflights.com/OLS81intro.html'),
  ('<em>Nogales International</em>, “State grant to fund upgrades at Nogales International Airport,” January 28, 2022; and “Sky is the limit,” January 10, 2025', 'https://www.nogalesinternational.com/news/sky-is-the-limit-nogales-international-airport-lands-new-upgrades-management/article_e8215dc4-cd29-11ef-acd2-bf9c53f1ebae.html'),
]

def history(p):
    def fig(slot, cap, cls="crop"):
        return f'<figure class="tfig {cls}">{img(slot, p, sizes="(min-width: 980px) 560px, 100vw")}<figcaption>{cap}</figcaption></figure>'
    items = [
      ("pro", "Prologue", "1910–1933", "A border camp with an aviation field",
       """<p>U.S. Army troops arrived at Nogales in <b>November 1910</b> as the Mexican Revolution began. On <b>December 14, 1915</b>, the post was named Camp Stephen D. Little, for a private killed in the November 1915 border clash. At its largest the camp spread across a cantonment, a target range and an <b>aviation field</b>, the earliest documented flying field in Nogales. The Army formally abandoned Camp Little on <b>May 5, 1933</b>.</p>
<p class="note-pro">Camp Little stood at the north edge of the Nogales townsite. It was <b>not</b> today's airport, which sits 7 to 8 miles northeast of downtown on State Route 82.</p>"""),
      ("pro", "Prologue", "1920–1921", "DH-4s on border patrol",
       fig("aero-1920", "12th Aero Squadron aircraft at Camp Stephen D. Little's aviation field near Nogales, 1920. U.S. Air Service photo, public domain. This field predates today's SR 82 airport site by eight years.", "bw") +
       """<p>After World War I the Army Air Service flew the Mexican Border Air Patrol. The <b>12th Aero Squadron</b> moved its headquarters to “Nogales Field” on <b>April 12, 1920</b> and flew Dayton-Wright DH-4 patrols along the line. Headquarters shifted to Douglas in February 1921, a flight stayed on at Nogales, and the squadron regrouped in Texas that September.</p>
<p class="note-pro">This was the earlier military landing field near town, not the present airport.</p>"""),
      ("", "Founding", "1928", "The community buys an airfield",
       """<p>In <b>January 1928</b> the Santa Cruz County Chamber of Commerce bought land north of Nogales for a public airfield: the same property the airport occupies today. It opened in <b>March 1928</b> as a graded native-earth and grass rectangle, <b>1,980 by 4,180 feet</b>, where pilots could land in any direction.</p>
<p>The land was deeded to Santa Cruz County on <b>October 3, 1928</b>, and the county still owns it. The airport was officially dedicated in <b>September 1929</b>.</p>"""),
      ("", "Golden age", "1930s", "A short hop to the border",
       """<p>Tucson's Davis-Monthan pilot register (1925–1936) logs dozens of flights to and from Nogales, with pilots based here and plenty headed south. In the Prohibition years, the international line was only minutes away.</p>
<p>The county's 2015 Airport Master Plan identifies <b>Pickwick Airlines</b> as the field's first scheduled operator, with flights into Mexico. That service did not last.</p>"""),
      ("", "Gateway", "1937", "An international airport of entry",
       """<p>The federal government's 1937 airport handbook (Bureau of Air Commerce) already listed Nogales as an <b>international airport of entry</b>, then a gravel field. Nogales Municipal Airport appears on the 1946 U.S. Code list of airports of entry, and Nogales International Airport is still designated today under <b>19 CFR § 122.13</b>, with an on-field U.S. Customs and Border Protection port of entry.</p>"""),
      ("", "World War II", "1942–1945", "Federal funds pave the field",
       """<p>The remaining two parcels of land were deeded to the county in <b>December 1942</b>. The Master Plan records that the airport hosted a Navy V-5 training program and the Civil Air Patrol during the war.</p>
<p>On <b>March 31, 1944</b>, federally funded construction gave the airport its first paved runways:</p>
<ul><li>The original north–south grass strip was paved (500 × 2,500 ft).</li><li>A new <b>6,000-foot</b> northeast–southwest asphalt runway was built with a parallel taxiway and drainage. It is the backbone of today's Runway 04/22.</li></ul>
<p>A lighted apron followed in August 1944, and runway contact lights in June 1945.</p>"""),
      ("", "Airline era", "1946–1953", "DC-3s on the Nogales route",
       """<p><b>Arizona Airways</b>, flying Douglas DC-3s out of Phoenix, included Nogales on its route to Bisbee and Douglas from 1946 until statewide service ended on <b>March 1, 1948</b>.</p>
<p>On <b>June 1, 1950</b>, newly formed <b>Frontier Airlines</b> began DC-3 service on the Phoenix–Tucson–Nogales–Bisbee–Douglas route. The temporary route authority was not renewed in 1953.</p>"""),
      ("", "Mid-century", "1956–1981", "Fuel, a VOR and a small airline",
       """<ul><li><b>1956:</b> taxiway strips and tie-down hardstands.</li><li><b>1965:</b> the 6,000-foot runway is resurfaced and marked.</li><li><b>1967:</b> a fueling facility opens on the field.</li><li><b>1975:</b> a VOR/DME navigation aid, access road and power service are installed.</li></ul>
<p><b>Copper State Airlines</b> appears on an <b>April 1, 1981</b> timetable, flying a Piper Cherokee from Nogales to Sierra Vista/Fort Huachuca and Tucson.</p>"""),
      ("", "Modern field", "1984–1996", "Today's 7,200-foot runway",
       fig("kols-guide", "Runway 4-22 sign at Nogales International Airport today.") +
       """<p>The main runway was surfaced in 1984 and strengthened and repaved in 1989. Around 1988 the old north–south crosswind runway went out of use and has since disappeared. The current terminal building went up in <b>1993–94</b>.</p>
<p>In <b>1996</b> a 1,200-foot extension stretched the 1944 runway to today's <b>7,200 × 100 feet</b>, the runway pilots land on now.</p>"""),
      ("", "Modernization", "2002–2022", "Safety, lighting and guidance",
       fig("charter", "Runway lights at KOLS at dusk.") +
       """<p>From 2002 to 2011, nearly <b>$6 million</b> in FAA Airport Improvement Program grants funded perimeter fencing, guidance signs, runway and taxiway lighting, a runway rehabilitation, a new apron and taxiway work. Automated ASOS weather observations at the field are on record since at least 1999.</p>
<p>In <b>2022</b>, nearly <b>$2 million</b> in state grants funded a new LED rotating beacon, runway end identifier lights, runway edge lights, guidance signs and a new visual approach guidance system.</p>"""),
      ("now", "Today", "2024–present", "Copper Mountain Air at KOLS",
       fig("cargo", "The cargo sign on the field at KOLS today.") +
       f"""<p>In <b>2024</b>, Copper Mountain Air succeeded Tiffin Aviation as the full-service FBO at Nogales International Airport, bringing Phillips 66 fueling, flight training, and expedited cargo under one locally led roof on the field.</p>
<p>With Santa Cruz County investing in a new airport fuel farm and ongoing airfield upgrades, KOLS is heading into its second century ready for the next generation of Southern Arizona aviation.</p>
<p style="margin-top:1rem"><a class="btn btn-primary" href="{p}flight-training.html">Fly with us {ARROW}</a></p>"""),
    ]
    lis = "".join(f'<li class="{cls} reveal"><article class="tcard"><span class="era">{era}</span><span class="tyear">{yr}</span><h3>{h}</h3>{body}</article></li>' for cls, era, yr, h, body in items)
    srcs = "".join(f'<li>{t}. <a href="{u}" target="_blank" rel="noopener">Source</a></li>' for t, u in HISTORY_SOURCES)
    return f"""
<section class="heritage" id="history" aria-label="History of Nogales International Airport"><div class="wrap">
  <div class="lead-in">
    <div class="section-head reveal" style="margin:0"><p class="eyebrow">History of KOLS</p><h2>Nearly a century of border aviation.</h2></div>
    <p class="big reveal">Nogales International began in 1928 as a grass field the community bought for itself. It became a federal airport of entry, was paved in wartime, briefly saw airline DC-3s, and grew into the 7,200-foot border gateway pilots use today. And Nogales was flying even before that.</p>
  </div>
  <div class="hstats reveal">
    <div><b>1928</b><span>Today's field opened, March 1928</span></div>
    <div><b>1937</b><span>Listed as an international airport of entry</span></div>
    <div><b>1944</b><span>First paved runways, March 31</span></div>
    <div><b>7,200 ft</b><span>Runway 04/22 today, after the 1996 extension</span></div>
  </div>
  <ol class="tl">{lis}</ol>
  <div class="sources"><h3>Sources</h3><ol>{srcs}</ol>
    <p style="margin-top:.8rem">Dates follow the strongest primary record. Where sources conflict (for example, the first paved runway), we use the 2015 Master Plan's project table. Runway 04/22 was numbered 3/21 for most of its history.</p></div>
</div></section>"""

def about(p):
    hero = f"""
<section class="xhero about-hero" aria-label="About Copper Mountain Air" style="min-height:min(80vh,760px)">
  <div class="hero-media">{img("airfield", p, eager=True, sizes="full")}</div><div class="grid-lines" aria-hidden="true"></div>
  <div class="wrap">
    <div class="xhero-inner" style="grid-template-columns:1fr">
      <div>
        <ul class="chips" aria-label="At a glance"><li class="chip"><i></i>Santa Cruz County airport since 1928</li><li class="chip"><i></i>International airport of entry</li><li class="chip"><i></i>Full-service FBO since 2024</li></ul>
        <p class="eyebrow">About · Nogales International Airport · KOLS</p>
        <h1>Southern Arizona's <span class="cu">home field team.</span></h1>
        <p class="lede">Copper Mountain Air, LLC is the full-service FBO at Nogales International Airport (KOLS), a Santa Cruz County airport that has served this border community since 1928.</p>
        <div class="actions"><a class="btn btn-primary" href="#history">Nearly a century of KOLS history {ARROW}</a><a class="btn btn-glass" href="{p}contact.html">Contact us</a></div>
      </div>
    </div>
  </div>
</section>"""
    return hero + f"""
<section><div class="wrap split">
  <figure class="frame reveal">{img("training", p)}</figure>
  <div class="reveal"><p class="eyebrow">Our story</p><h2>Rooted at KOLS.</h2>
    <p>Since 2024, Copper Mountain Air has been the fixed-base operator at Nogales International Airport (KOLS) in Santa Cruz County, Arizona, just north of the U.S.–Mexico border.</p>
    <p>We provide full-service Jet A and 100LL fueling, FBO ground support on the field, FAA Part 61 single-engine flight training, and on-demand expedited cargo by ground. Multi-engine training is arriving shortly, and FAA Part 141 flight school certification is in process. On-demand charter is in development and is not yet offered.</p>
    <p><a class="btn btn-dark" href="#history">Read the airport's history {ARROW}</a></p></div>
</div></section>
{history(p)}
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
  <form class="form reveal" id="contact-form" data-to="{CONTACT_TO}" data-endpoint="{CONTACT_ENDPOINT}" action="{CONTACT_ENDPOINT}" method="POST">
    <div class="row"><div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div></div>
    <div class="row"><div class="field"><label for="phone">Phone <span class="hint">Optional</span></label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
    <div class="field"><label for="company">Company <span class="hint">Optional</span></label><input id="company" name="company" autocomplete="organization"></div></div>
    <div class="field"><label for="topic">What can we help with?</label><select id="topic" name="topic" required>{''.join(f'<option>{html.escape(o)}</option>' for o in opts)}</select></div>
    <div class="field"><label for="message">Message</label><textarea id="message" name="message" required placeholder="Tail number and ETA, fuel needs, or shipment details (pickup, delivery, pieces, weight)"></textarea></div>
    <input type="text" name="_honey" id="form-honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
    <input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="_subject" value="Website inquiry — Copper Mountain Air">
    <div><button class="btn btn-primary" type="submit" id="contact-submit">Send message {ARROW}</button></div>
    <p class="note" id="form-status" role="status" aria-live="polite"></p>
    <p class="note">Messages go directly to <a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a>. For immediate ramp or fuel needs, call {PHONE_LINK}.</p>
  </form>
  <div class="contact-cards reveal">
    <div class="contact-card"><h3>Phone</h3><p>{PHONE_LINK}</p></div>
    <div class="contact-card"><h3>Email</h3><p><a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a></p></div>
    <div class="contact-card"><h3>Hours</h3><p>{HOURS_HTML}</p></div>
    <div class="contact-card"><h3>Location</h3><p>Nogales International Airport (KOLS)<br>{STREET}<br>Nogales, AZ 85621</p></div>
    <div class="contact-card"><h3>Follow us</h3>{social_links()}</div>
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
        body = re.sub(r"<p>\{\{chart:([^|}]*)\|([^}]*)\}\}</p>", lambda mm: "{{CHART:" + mm.group(1).strip() + "|" + mm.group(2).strip() + "}}", body)
        body = re.sub(r"<p>\{\{charts:([^}]*)\}\}</p>", lambda mm: "{{CHARTS:" + mm.group(1).strip() + "}}", body)
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
{'<span class="badge draft">Draft · not published</span>' if x["draft"] else ''}{f'<p class="meta">{html.escape(fmt_date(x["date"]))}</p>' if x.get("date") and not x["date"].startswith("[") else ''}
<h3><a href="{p}blog/{x["slug"]}.html" style="color:inherit;text-decoration:none">{html.escape(x["title"])}</a></h3><p>{html.escape(x["description"])}</p>
<a class="more" href="{p}blog/{x["slug"]}.html">{"Read the draft" if x["draft"] else "Read more"} {ARROW}</a></div></article>""" for x in posts)
        return page_hero("Blog", "From the ramp.", "Airport news, pilot info and freight tips from Nogales International Airport (KOLS) and Santa Cruz County.") + f"""
<section><div class="wrap">{'<div class="draft-banner">LOCAL DRAFT REVIEW BUILD: posts marked Draft are not on the live site.</div>' if SHOW_DRAFTS else ''}{f'<div class="post-list">{cards}</div>' if posts else EMPTY_BLOG(p)}</div></section>"""
    return f

def EMPTY_BLOG(p):
    return f"""<div class="split reveal"><div class="frame">{img("kols-guide", p)}</div><div><span class="badge soon">First post coming soon</span>
<h2>New posts every month.</h2><p>We publish a new post each month: KOLS airport updates, pilot info, and freight tips for Santa Cruz County. Check back soon.</p>
<a class="btn btn-dark" href="{p}fuel-fbo.html">Fuel &amp; FBO info {ARROW}</a></div></div>"""

def chart_fig(cid, cap, p):
    meta = CHARTS[cid.strip()]
    src = f'{p}assets/img/charts/{meta["file"]}'
    if meta.get("kind") == "photo":
        widths = meta["widths"]
        d, prefix = "assets/img/charts", meta["file"]
        sz = SIZES["article"]
        mid = [w for w in widths if w >= 1200] or widths[-1:]
        full = f'{src}.{meta.get("full_ext", "jpg")}'
        picture = (
            f'<picture>'
            f'<source type="image/avif" srcset="{srcset_custom(p, d, prefix, widths, "avif")}" sizes="{sz}">'
            f'<source type="image/webp" srcset="{srcset_custom(p, d, prefix, widths, "webp")}" sizes="{sz}">'
            f'<img src="{p}{d}/{prefix}-{mid[0]}.jpg" srcset="{srcset_custom(p, d, prefix, widths, "jpg")}" sizes="{sz}" '
            f'alt="{html.escape(meta["alt"])}" width="{meta["w"]}" height="{meta["h"]}" loading="lazy" decoding="async">'
            f'</picture>'
        )
        return (f'<figure class="article-fig">'
                f'<a href="{full}" target="_blank" rel="noopener">{picture}</a>'
                f'<figcaption>{cap.strip()}</figcaption></figure>')
    return (f'<figure class="chart-fig">'
            f'<a href="{src}.png" target="_blank" rel="noopener">'
            f'<picture><source type="image/webp" srcset="{src}.webp">'
            f'<img src="{src}.png" alt="{html.escape(meta["alt"])}" width="{meta["w"]}" height="{meta["h"]}" loading="lazy" decoding="async">'
            f'</picture></a><figcaption>{cap.strip()}</figcaption></figure>')

def expand(body, p):
    body = re.sub(r"\{\{GALLERY:([^}]*)\}\}", lambda m: '<div class="gallery">' + "".join(f'<figure>{img(s.strip(), p, sizes="third")}</figure>' for s in m.group(1).split(",")) + "</div>", body)
    body = re.sub(r"\{\{FIGURE:([^|]*)\|([^}]*)\}\}", lambda m: f'<figure class="article-fig">{img(m.group(1), p, sizes="article")}<figcaption>{m.group(2)}</figcaption></figure>', body)
    body = re.sub(r"\{\{CHART:([^|]*)\|([^}]*)\}\}", lambda m: chart_fig(m.group(1), m.group(2), p), body)
    def grid(m):
        items = [part.strip() for part in m.group(1).split(";;") if part.strip()]
        figs = []
        for item in items:
            cid, cap = item.split("|", 1)
            figs.append(chart_fig(cid, cap, p))
        return '<div class="article-charts">' + "".join(figs) + "</div>"
    return re.sub(r"\{\{CHARTS:([^}]*)\}\}", grid, body)

def fmt_date(d):
    """'2026-11-19' -> 'November 19, 2026' for display; anything else passes through."""
    import datetime
    try: return datetime.date.fromisoformat(d).strftime("%B %-d, %Y")
    except (ValueError, TypeError): return d

def blog_post(x):
    def f(p):
        return f"""<div class="page-hero"><div class="wrap">{'<span class="badge draft">Draft · for review</span>' if x["draft"] else ''}<p class="eyebrow"><a href="{p}blog/index.html" style="color:inherit">Blog</a></p><h1 style="text-transform:none;font-size:clamp(2rem,5vw,3.4rem)">{html.escape(x["title"])}</h1><p class="post-meta">Copper Mountain Air{" · " + html.escape(fmt_date(x["date"])) if x.get("date") and not x["date"].startswith("[") else ""}</p></div></div>
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
         "FAA Part 61 single-engine flight training at Nogales International Airport (KOLS), with live KOLS ASOS weather, an FAA sectional training map and FlightCircle scheduling. Multi-engine arriving shortly; Part 141 in process.", flight_training)
    page("cargo.html", "Cargo & Expedited Freight from Nogales, AZ (KOLS) | Copper Mountain Air",
         "Expedited ground and air-to-ground cargo from Nogales International Airport (KOLS): a 26-ft dock-height Hino 268 box truck with liftgate, a Ford E-150 cargo van, and ramp-to-truck transfers.", cargo)
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
              else "User-agent: *\nAllow: /\nDisallow: /preview/\n") + f"\nSitemap: {SITE_URL}sitemap.xml\n"
    open(os.path.join(OUT, "robots.txt"), "w").write(robots)
    # Custom domain for GitHub Pages (workflow deploy uses the artifact, not the repo root).
    if not PREVIEW:
        open(os.path.join(OUT, "CNAME"), "w").write("coppermountainair.com\n")
    print("built", len(PAGES), "pages")

if __name__ == "__main__":
    main()

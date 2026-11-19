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
CONTACT_TO = "seth.miller@coppermountainair.com"
PAY_URL = "https://pay.coppermountainair.com"

# Image slots: swap "x.svg" -> "x.jpg" after dropping a real photo in assets/img/
IMG = {
  "hero":      ("hero.svg",      "Illustrated placeholder: desert mountains at dusk with an aircraft overhead"),
  "fbo":       ("fbo.svg",       "Placeholder for a photo of the Copper Mountain Air FBO at KOLS"),
  "fuel":      ("fuel.svg",      "Placeholder for a photo of aircraft fueling at KOLS"),
  "cargo":     ("cargo.svg",     "Placeholder for a photo of cargo operations"),
  "training":  ("training.svg",  "Placeholder for a flight training photo"),
  "charter":   ("charter.svg",   "Placeholder for a charter aircraft photo"),
  "about":     ("about.svg",     "Placeholder for a team or hangar photo"),
  "kols-guide":("kols-guide.svg","Placeholder for an aerial photo of Runway 4/22 at KOLS"),
  "event":     ("event.svg",     "Placeholder for a Wings & Wheels event photo"),
}
def img(slot, p, cls="", eager=False):
    f, alt = IMG[slot]
    attrs = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{p}assets/img/{f}" alt="{html.escape(alt)}" {attrs} decoding="async" width="1200" height="800"{f" class={cls!r}" if cls else ""}>'

def ph(t): return f'<span class="ph">[{t}]</span>'

NAV = [("index.html","Home"),("services.html","Services"),("fuel-fbo.html","Fuel &amp; FBO"),
       ("flight-training.html","Flight Training"),("charter.html","Charter"),("about.html","About"),
       ("blog/index.html","Blog"),("contact.html","Contact")]

JSONLD_BIZ = {
  "@context":"https://schema.org","@type":["LocalBusiness"],"@id":SITE_URL+"#business",
  "name":"Copper Mountain Air, LLC","url":SITE_URL,
  "description":"Fuel (Jet A and 100LL), FBO services, and air and ground cargo at Nogales International Airport (KOLS) in Nogales, Arizona.",
  "telephone":"","email":CONTACT_TO,"openingHours":"","priceRange":"",
  "logo":SITE_URL+"assets/img/logo.svg","image":SITE_URL+"assets/img/og-image.png",
  "address":{"@type":"PostalAddress","streetAddress":"","addressLocality":"Nogales","addressRegion":"AZ","postalCode":"85621","addressCountry":"US"},
  "geo":{"@type":"GeoCoordinates","latitude":31.4177222,"longitude":-110.8478889},
  "areaServed":[{"@type":"City","name":"Nogales, AZ"},{"@type":"AdministrativeArea","name":"Santa Cruz County, AZ"},{"@type":"State","name":"Arizona"}],
  "containedInPlace":{"@type":"Airport","name":"Nogales International Airport","icaoCode":"KOLS",
     "address":{"@type":"PostalAddress","addressLocality":"Nogales","addressRegion":"AZ","postalCode":"85621","addressCountry":"US"}},
  "sameAs":[]
}

def head(title, desc, path, p, extra_ld=None, og_type="website", og_img=None):
    url = SITE_URL + ("" if path == "index.html" else path)
    og = SITE_URL + "assets/img/" + (og_img or "og-image.png")
    ld = [JSONLD_BIZ] + ([extra_ld] if extra_ld else [])
    robots = '<meta name="robots" content="noindex, nofollow">\n' if PREVIEW else ''
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
<link rel="stylesheet" href="{p}assets/css/site.css">
<script>document.documentElement.className="js";</script>
<script type="application/ld+json">{json.dumps(ld if len(ld)>1 else ld[0], ensure_ascii=False)}</script>
</head>"""

def header(path, p):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if (href == path or (href == "blog/index.html" and path.startswith("blog/"))) else ""
        items.append(f'<li><a href="{p}{href}"{cur}>{label}</a></li>')
    items.append(f'<li><a class="pay" href="{PAY_URL}" rel="noopener">Pay online</a></li>')
    bar = ('<div class="preview-bar"><strong>Preview draft.</strong> Not yet published. '
           'Items in <span class="ph">[BRACKETS]</span> are placeholders awaiting confirmation.</div>') if PREVIEW else ""
    return f"""<body>
<a class="skip" href="#main">Skip to content</a>
{bar}
<header class="site-header"><div class="wrap">
  <a class="brand" href="{p}index.html" aria-label="Copper Mountain Air home"><img src="{p}assets/img/logo.svg" alt="Copper Mountain Air" width="200" height="40"></a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav id="site-nav" class="site-nav" aria-label="Primary"><ul>{''.join(items)}</ul></nav>
</div></header>
<main id="main">"""

def footer(p):
    return f"""</main>
<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div><img src="{p}assets/img/logo.svg" alt="Copper Mountain Air" width="200" height="40" style="height:40px;width:auto;margin-bottom:1rem">
      <p>Fuel, FBO and cargo at Nogales International Airport (KOLS), serving Nogales and Santa Cruz County, Arizona.</p></div>
    <div><h3>Visit</h3><p>Copper Mountain Air, LLC<br>Nogales International Airport (KOLS)<br>{ph("STREET ADDRESS")}<br>Nogales, AZ 85621</p></div>
    <div><h3>Contact</h3><ul><li>Phone: {ph("PHONE")}</li><li><a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a></li><li>Hours: {ph("HOURS")}</li><li><a href="{p}contact.html">Send a message</a></li></ul></div>
    <div><h3>Explore</h3><ul><li><a href="{p}services.html">Services</a></li><li><a href="{p}fuel-fbo.html">Fuel &amp; FBO</a></li><li><a href="{p}blog/index.html">Blog</a></li><li><a href="{PAY_URL}" rel="noopener">Pay online</a></li></ul></div>
  </div>
  <div class="legal"><span>© 2026 Copper Mountain Air, LLC</span><span>Flight training and charter are coming soon and are not yet offered.</span></div>
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

POSTS = []
def kols_link(p, text):
    """Only link the KOLS guide once that post is published (or in a local --drafts build)."""
    if any(x["slug"] == "kols-pilot-guide" for x in POSTS):
        return f'<p style="margin-top:1.5rem"><a class="btn btn-ghost" href="{p}blog/kols-pilot-guide.html">{text} {ARROW}</a></p>'
    return ""

# ---------- HOME ----------
def home(p):
    return f"""
<section class="hero" aria-label="Introduction" style="padding:0">
  <div class="hero-media">{img("hero", p, eager=True)}</div>
  {'<span class="slot-tag">Hero art placeholder · swap in assets/img/hero.jpg</span>' if IMG["hero"][0].endswith(".svg") else ''}
  <div class="wrap hero-inner">
    <p class="eyebrow">Nogales International Airport · KOLS</p>
    <h1>Fuel, freight &amp; flight <span class="cu">on the border.</span></h1>
    <p class="lede">Copper Mountain Air keeps Southern Arizona moving: Jet A and Avgas on the ramp, FBO service at KOLS, and air and ground cargo out of Nogales.</p>
    <div class="actions"><a class="btn btn-primary" href="{p}contact.html">Get in touch {ARROW}</a><a class="btn btn-ghost" href="{p}fuel-fbo.html">Fuel &amp; FBO</a></div>
    <div class="hero-strip"><span>Jet A</span><span>100LL Avgas</span><span>FBO</span><span>Air &amp; ground cargo</span><span>Santa Cruz County, AZ</span></div>
  </div>
</section>

<section><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">What we do</p><h2>One stop at KOLS.</h2><p>Whether you're fueling up on a cross-country, parking for the night or moving a time-critical load, start here.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="media">{img("fuel", p)}</div><div class="body"><span class="num">01</span><h3>Fuel</h3><p>Jet A and 100LL Avgas at Nogales International. Pricing: {ph("FUEL PRICES OR CALL FOR PRICE")}.</p><a class="more" href="{p}fuel-fbo.html">Fuel details {ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{img("fbo", p)}</div><div class="body"><span class="num">02</span><h3>FBO services</h3><p>Ground handling, ramp and tie-down parking, and hangar space on the field.</p><a class="more" href="{p}fuel-fbo.html#fbo">FBO services {ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{img("cargo", p)}</div><div class="body"><span class="num">03</span><h3>Cargo &amp; freight</h3><p>Time-critical freight out of Nogales by air and ground, including on-demand expedited freight.</p><a class="more" href="{p}services.html#cargo">Cargo services {ARROW}</a></div></article>
  </div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Flying in?</p><h2>Nogales International at a glance.</h2><p>A 7,200-foot runway at the foot of the Santa Cruz Valley, about 7 miles northeast of downtown Nogales.</p></div>
  {AIRPORT_FACTS}
  {kols_link(p, "Read the KOLS pilot guide")}
</div></section>

<section><div class="wrap split">
  <div class="frame reveal">{img("training", p)}</div>
  <div class="reveal"><span class="badge soon">Coming soon</span><h2>Flight training &amp; charter are on the way.</h2>
    <p>We're building a flight school and an on-demand charter service at KOLS. Neither is offered yet; we'll announce them here as soon as they're ready.</p>
    <p><a class="btn btn-dark" href="{p}contact.html?topic=Flight%20training%20interest">Join the interest list {ARROW}</a></p>
    <p><a href="{p}flight-training.html">Flight training</a> · <a href="{p}charter.html">Charter</a></p></div>
</div></section>
{cta(p)}
"""

def services(p):
    return page_hero("Services", "Built for the border.", "Fuel, FBO services and cargo at Nogales International Airport (KOLS), serving Nogales, Santa Cruz County and Southern Arizona.") + f"""
<section id="cargo"><div class="wrap split">
  <div class="frame reveal">{img("cargo", p)}</div>
  <div class="reveal"><p class="eyebrow">Cargo &amp; freight</p><h2>Air and ground, on demand.</h2>
    <p>When a shipment can't wait, we move it. Copper Mountain Air handles time-critical freight out of Nogales by ground and coordinates air cargo at KOLS.</p>
    <ul class="checks">
      <li>Ground trucking across Southern Arizona {ph("CONFIRM SERVICE AREA")}</li>
      <li>On-demand expedited freight</li>
      <li>Air cargo at KOLS {ph("CONFIRM AIR CARGO WORDING")}</li>
      <li>Vehicles / capacity: {ph("FLEET DETAILS")}</li>
    </ul>
    <a class="btn btn-dark" href="{p}contact.html?topic=Cargo%20%2F%20freight">Request a freight quote {ARROW}</a></div>
</div></section>
<section class="sand" id="fuel"><div class="wrap split rev">
  <div class="frame reveal">{img("fuel", p)}</div>
  <div class="reveal"><p class="eyebrow">Fuel</p><h2>Jet A and 100LL.</h2>
    <p>Both jet fuel and Avgas are available on the field at Nogales International.</p>
    <ul class="checks"><li>Jet A</li><li>100LL Avgas</li><li>Service type: {ph("FULL-SERVICE / SELF-SERVE")}</li><li>Pricing: {ph("FUEL PRICES OR CALL FOR PRICE")}</li></ul>
    <a class="btn btn-dark" href="{p}fuel-fbo.html">Fuel &amp; FBO details {ARROW}</a></div>
</div></section>
<section id="fbo"><div class="wrap split">
  <div class="frame reveal">{img("fbo", p)}</div>
  <div class="reveal"><p class="eyebrow">FBO</p><h2>Your stop at KOLS.</h2>
    <ul class="checks"><li>Aircraft ground handling</li><li>Ramp and tie-down parking</li><li>Hangar space {ph("AVAILABILITY")}</li><li>Passenger terminal and lounge {ph("CONFIRM AMENITIES")}</li></ul>
    <a class="btn btn-dark" href="{p}fuel-fbo.html#fbo">See FBO services {ARROW}</a></div>
</div></section>
<section class="dark"><div class="wrap">
  <div class="section-head reveal"><span class="badge soon">Coming soon</span><h2>Flight training and charter.</h2><p>Both are in development and not offered yet. Join the interest list and we'll let you know when they open.</p></div>
  <div class="grid cards">
    <article class="card reveal"><div class="media">{img("training", p)}</div><div class="body"><h3>Flight training</h3><p>A flight school at Nogales International, coming soon.</p><a class="more" href="{p}flight-training.html">Learn more {ARROW}</a></div></article>
    <article class="card reveal"><div class="media">{img("charter", p)}</div><div class="body"><h3>Charter</h3><p>On-demand charter flights from KOLS, coming soon.</p><a class="more" href="{p}charter.html">Learn more {ARROW}</a></div></article>
  </div>
</div></section>
{cta(p)}"""

def fuel_fbo(p):
    return page_hero("Fuel &amp; FBO · KOLS", "Fuel up at Nogales International.", "Jet A and 100LL Avgas, plus ramp, hangar and handling services at Nogales International Airport (KOLS).") + f"""
<section id="fuel"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Fuel</p><h2>Jet A &amp; 100LL.</h2><p>Prices change with the market. Until posted prices are set, call or message for today's price.</p></div>
  <table class="price-table reveal"><thead><tr><th scope="col">Fuel</th><th scope="col">Service</th><th scope="col">Price / gal</th></tr></thead>
  <tbody><tr><td><strong>Jet A</strong></td><td>{ph("FULL-SERVICE / SELF-SERVE")}</td><td>{ph("PRICE OR CALL FOR PRICE")}</td></tr>
  <tr><td><strong>100LL Avgas</strong></td><td>{ph("FULL-SERVICE / SELF-SERVE")}</td><td>{ph("PRICE OR CALL FOR PRICE")}</td></tr></tbody></table>
  <p class="note" style="margin-top:1rem">Fuel hours: {ph("HOURS")} · After-hours call-out: {ph("AFTER-HOURS POLICY")} · Payment: {ph("ACCEPTED CARDS / FUEL CARDS")}</p>
</div></section>
<section class="sand" id="fbo"><div class="wrap split">
  <div class="frame reveal">{img("fbo", p)}</div>
  <div class="reveal"><p class="eyebrow">FBO services</p><h2>Ramp, hangar &amp; handling.</h2>
    <ul class="checks"><li>Aircraft ground handling</li><li>Ramp and tie-down parking {ph("FEES OR CALL")}</li><li>Hangar leasing {ph("AVAILABILITY")}</li><li>Passenger terminal and lounge {ph("CONFIRM AMENITIES: restrooms, Wi-Fi, crew car, etc.")}</li></ul>
    <a class="btn btn-dark" href="{p}contact.html?topic=FBO%20%2F%20ramp%20%2F%20hangar">Reserve a ramp spot or hangar {ARROW}</a></div>
</div></section>
<section class="dark"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Airport info</p><h2>KOLS for pilots.</h2></div>
  {AIRPORT_FACTS}
  {kols_link(p, "Full KOLS pilot guide")}
</div></section>
{cta(p, "Inbound to KOLS?", "Let us know your ETA and fuel needs. Phone: <span class='ph'>[PHONE]</span>")}"""

def coming_soon(kind):
    def f(p):
        if kind == "training":
            hero = page_hero("Flight Training", "Learn to fly in Nogales.", "We're building a flight school at Nogales International Airport. It is not open yet.", '<span class="badge soon">Coming soon</span>')
            body = "A flight school at KOLS is in development. Programs, aircraft, instructors and pricing will be announced when the school is ready to enroll students."
            slot, topic, items = "training", "Flight%20training%20interest", ["Programs: " + ph("TBD"), "Aircraft: " + ph("TBD"), "Instructors: " + ph("TBD"), "Opening date: " + ph("TBD")]
        else:
            hero = page_hero("Charter", "Fly direct from KOLS.", "On-demand charter from Nogales International is in development. It is not offered yet.", '<span class="badge soon">Coming soon</span>')
            body = "We're working toward on-demand charter flights from Nogales International. We can't book charter flights yet; join the interest list and we'll reach out when the service opens."
            slot, topic, items = "charter", "Charter%20interest", ["Aircraft: " + ph("TBD"), "Destinations: " + ph("TBD"), "Launch date: " + ph("TBD")]
        return hero + f"""
<section><div class="wrap split">
  <div class="frame reveal">{img(slot, p)}</div>
  <div class="reveal"><span class="badge soon">Coming soon</span><h2>Not open yet, but close.</h2><p>{body}</p>
    <ul class="checks">{''.join(f'<li>{i}</li>' for i in items)}</ul>
    <a class="btn btn-dark" href="{p}contact.html?topic={topic}">Join the interest list {ARROW}</a></div>
</div></section>{cta(p, "Questions in the meantime?", "We're happy to talk. Fuel, FBO and cargo services are available today.")}"""
    return f

def about(p):
    return page_hero("About", "Southern Arizona's home field team.", "Copper Mountain Air, LLC is based at Nogales International Airport (KOLS) in Nogales, Arizona.") + f"""
<section><div class="wrap split">
  <div class="frame reveal">{img("about", p)}</div>
  <div class="reveal"><p class="eyebrow">Our story</p><h2>Rooted at KOLS.</h2>
    <p>{ph("COMPANY STORY: how Copper Mountain Air started, and what it stands for. Seth to provide.")}</p>
    <p>Today we provide fuel and FBO services on the field and move freight by air and ground for customers across Southern Arizona, with flight training and charter coming soon.</p></div>
</div></section>
<section class="sand"><div class="wrap">
  <div class="section-head reveal"><p class="eyebrow">Team</p><h2>The people behind the ramp.</h2><p>{ph("TEAM NAMES, ROLES, SHORT BIOS AND PHOTOS")}</p></div>
  <div class="grid cards">
    {''.join(f'<article class="card reveal"><div class="body"><h3>{ph("NAME")}</h3><p>{ph("ROLE")}</p><p>{ph("SHORT BIO")}</p></div></article>' for _ in range(3))}
  </div>
</div></section>
<section class="dark"><div class="wrap"><div class="section-head reveal"><p class="eyebrow">Where we are</p><h2>Nogales International Airport (KOLS)</h2><p>About 7 miles northeast of Nogales in Santa Cruz County, Arizona. Address: {ph("STREET ADDRESS")}, Nogales, AZ 85621.</p></div>{AIRPORT_FACTS}</div></section>
{cta(p)}"""

def contact(p):
    opts = ["Fuel", "FBO / ramp / hangar", "Cargo / freight", "Flight training interest", "Charter interest", "Billing / payment", "Other"]
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
    <div class="contact-card"><h3>Phone</h3><p>{ph("PHONE")}</p></div>
    <div class="contact-card"><h3>Email</h3><p><a href="mailto:{CONTACT_TO}">{CONTACT_TO}</a></p></div>
    <div class="contact-card"><h3>Hours</h3><p>{ph("HOURS")}</p></div>
    <div class="contact-card"><h3>Location</h3><p>Nogales International Airport (KOLS)<br>{ph("STREET ADDRESS")}<br>Nogales, AZ 85621</p></div>
    <div class="contact-card"><h3>Pay an invoice</h3><p><a href="{PAY_URL}" rel="noopener">pay.coppermountainair.com</a></p></div>
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
        fm["body"] = re.sub(r"\[([A-Z0-9][^\]<]*)\]", lambda mm: ph(mm.group(1)), body)  # highlight [PLACEHOLDERS]
        fm["source"] = "posts/" + fn
        fm["draft"] = fm.get("published", "false").lower() != "true"
        if fm["draft"] and not SHOW_DRAFTS:
            print("  skipping unpublished post:", fn); continue
        posts.append(fm)
    return posts

def blog_index(posts):
    def f(p):
        cards = "".join(f"""<article class="card post-card reveal"><div class="media">{img(x["image"], p)}</div><div class="body">
{'<span class="badge draft">Draft · not published</span>' if x["draft"] else ''}<p class="meta">{html.escape(x["date"])}</p>
<h3><a href="{p}blog/{x["slug"]}.html" style="color:inherit;text-decoration:none">{html.escape(x["title"])}</a></h3><p>{html.escape(x["description"])}</p>
<a class="more" href="{p}blog/{x["slug"]}.html">{"Read the draft" if x["draft"] else "Read more"} {ARROW}</a></div></article>""" for x in posts)
        return page_hero("Blog", "From the ramp.", "Airport news, pilot info and freight tips from Nogales International Airport (KOLS) and Santa Cruz County.") + f"""
<section><div class="wrap">{'<div class="draft-banner">LOCAL DRAFT REVIEW BUILD: posts marked Draft are not on the live site.</div>' if SHOW_DRAFTS else ''}{f'<div class="post-list">{cards}</div>' if posts else EMPTY_BLOG(p)}</div></section>"""
    return f

def EMPTY_BLOG(p):
    return f"""<div class="split reveal"><div class="frame">{img("kols-guide", p)}</div><div><span class="badge soon">First post coming soon</span>
<h2>New posts every month.</h2><p>We publish a new post each month: KOLS airport updates, pilot info, and freight tips for Santa Cruz County. Check back soon.</p>
<a class="btn btn-dark" href="{p}fuel-fbo.html">Fuel &amp; FBO info {ARROW}</a></div></div>"""

def blog_post(x):
    def f(p):
        return f"""<div class="page-hero"><div class="wrap">{'<span class="badge draft">Draft · for review</span>' if x["draft"] else ''}<p class="eyebrow"><a href="{p}blog/index.html" style="color:inherit">Blog</a></p><h1 style="text-transform:none;font-size:clamp(2rem,5vw,3.4rem)">{html.escape(x["title"])}</h1><p class="post-meta">Copper Mountain Air · {html.escape(x["date"])}</p></div></div>
<section style="padding-top:0"><div class="wrap"><article class="article">
<div class="article-hero">{img(x["image"], p, eager=True)}</div>
{f'<div class="draft-banner">DRAFT — not published. Seth to review and approve before this goes live. Source file: <code>{x["source"]}</code></div>' if x["draft"] else ''}
{x["body"]}
<p style="margin-top:2.5rem"><a class="btn btn-dark" href="{p}blog/index.html">← All posts</a></p>
</article></div></section>"""
    return f

def main():
    global POSTS
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"), ignore=shutil.ignore_patterns("README.md"))
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    POSTS = load_posts()
    page("index.html", "Copper Mountain Air | Fuel, FBO & Cargo at Nogales International Airport (KOLS)",
         "Jet A and 100LL fuel, FBO services, and air and ground cargo at Nogales International Airport (KOLS) in Nogales, Santa Cruz County, Arizona.", home)
    page("services.html", "Services | Cargo, Fuel & FBO in Nogales, AZ | Copper Mountain Air",
         "Air and ground cargo, Jet A and 100LL fuel, and FBO services at Nogales International Airport (KOLS), serving Santa Cruz County, Arizona.", services)
    page("fuel-fbo.html", "Jet A & 100LL Fuel and FBO at KOLS | Copper Mountain Air",
         "Jet A and 100LL Avgas, ramp and tie-down parking, hangars and ground handling at Nogales International Airport (KOLS), Nogales, AZ.", fuel_fbo)
    page("flight-training.html", "Flight Training in Nogales, AZ (Coming Soon) | Copper Mountain Air",
         "A flight school at Nogales International Airport (KOLS) is coming soon. Join the interest list.", coming_soon("training"))
    page("charter.html", "Charter from Nogales, AZ (Coming Soon) | Copper Mountain Air",
         "On-demand charter from Nogales International Airport (KOLS) is coming soon. Join the interest list.", coming_soon("charter"))
    page("about.html", "About Copper Mountain Air | Nogales International Airport (KOLS)",
         "Copper Mountain Air, LLC provides fuel, FBO and cargo services at Nogales International Airport in Santa Cruz County, Arizona.", about)
    page("contact.html", "Contact Copper Mountain Air | Nogales, AZ (KOLS)",
         "Contact Copper Mountain Air at Nogales International Airport (KOLS) for fuel, ramp space, hangars and freight quotes.", contact)
    posts = POSTS
    page("blog/index.html", "Blog | Copper Mountain Air, Nogales International Airport (KOLS)",
         "Airport news, pilot info and freight tips from Copper Mountain Air at Nogales International Airport (KOLS), Arizona.", blog_index(posts))
    for x in posts:
        ld = {"@context":"https://schema.org","@type":"BlogPosting","headline":x["title"],"description":x["description"],
              "author":{"@type":"Organization","name":"Copper Mountain Air, LLC"},"publisher":{"@id":SITE_URL+"#business"},
              "datePublished":"" if x["draft"] else x["date"],"mainEntityOfPage":SITE_URL+"blog/"+x["slug"]+".html"}
        page(f"blog/{x['slug']}.html", f"{'DRAFT: ' if x['draft'] else ''}{x['title']} | Copper Mountain Air", x["description"], blog_post(x), ld, "article")
    # 404
    page("404.html", "Page not found | Copper Mountain Air", "Page not found.",
         lambda p: page_hero("404", "Off the chart.", "That page isn't here.") + f'<section><div class="wrap"><a class="btn btn-dark" href="{SITE_URL}">Back to home</a></div></section>')
    f404 = os.path.join(OUT, "404.html"); t = open(f404).read()
    open(f404, "w").write(t.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<base href="{SITE_URL}">', 1))
    # sitemap + robots
    urls = [u for u in PAGES if u != "404.html"]
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

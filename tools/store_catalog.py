"""Copper Mountain Air merch catalog.

All collection and product data lives here so a new yearly lineup can be
added in one place. featured_collection() picks the latest collection whose
drop date has arrived and that has products. Older collections automatically
move to Past Collections and stay listed and purchasable.

To ship the 2027 Collection on January 1:
  1. Add a 2027 entry to STORE_COLLECTIONS (drop=date(2027, 1, 1)) with its products.
  2. Set next_year / next_drop on that entry (2028, January 1).
  3. Deploy. On or after 1 Jan 2027, 2027 becomes the featured section and
     2026 appears under Past Collections. No other code change is required.
"""
from __future__ import annotations

from datetime import date

STORE_IMG_WIDTHS = [640, 1024]

# Retail prices set by Seth on Nov 25, 2026. Do not copy Freedom Aviation pricing.
# Jacket is the Printful SOL'S 32000 embroidered unisex windbreaker (base ~$20.76).
STORE_PRICES = {
    "tee": 28,
    "long-sleeve": 34,
    "hoodie": 55,
    "quarter-zip": 58,
    "jacket": 52,
    "cap": 28,
    "sticker": 4,
    "koozie": 10,
    "luggage-tag": 14,
}

STORE_PRICE_LABELS = {k: f"${v}" for k, v in STORE_PRICES.items()}

PRODUCTS_2026 = [
    {"id": "v2-ridgeline-natural-tee", "kind": "tee",
     "eyebrow": "Tee · Natural", "eyebrow_es": "Camiseta · Natural",
     "name": "Ridgeline Wordmark Tee", "name_es": "Camiseta Ridgeline Wordmark",
     "desc": "A wide horizontal mountain and saguaro line, with the CMA mark as the peak and Copper Mountain Air set cleanly beneath.",
     "desc_es": "Una línea horizontal de montañas y saguaros, con la marca de CMA en la cumbre y Copper Mountain Air debajo.",
     "alt": "Natural tee flat-laid on wood, printed with a wide mountain ridgeline and the Copper Mountain Air wordmark",
     "alt_es": "Camiseta natural extendida sobre madera, con una línea de montañas y el logotipo de Copper Mountain Air"},
    {"id": "v2-left-chest-navy-tee", "kind": "tee",
     "eyebrow": "Tee · Navy · Left chest", "eyebrow_es": "Camiseta · Navy · Pecho izquierdo",
     "name": "Left-Chest Crest Tee", "name_es": "Camiseta con emblema al pecho",
     "desc": "A small CMA mark and stacked wordmark on the left chest — the quiet everyday shirt. Pairs with the runway back print.",
     "desc_es": "Una marca pequeña de CMA y el nombre apilado en el pecho izquierdo: la camiseta discreta para todos los días. Combina con el estampado de pista en la espalda.",
     "alt": "Navy tee with a small left-chest Copper Mountain Air crest and KOLS wordmark",
     "alt_es": "Camiseta navy con un pequeño emblema de Copper Mountain Air y KOLS en el pecho izquierdo"},
    {"id": "v2-back-print-navy-tee", "kind": "tee",
     "eyebrow": "Tee · Navy · Back print", "eyebrow_es": "Camiseta · Navy · Estampado en la espalda",
     "name": "Runway Approach Back Tee", "name_es": "Camiseta de aproximación a pista",
     "desc": "A tall desert-sunset poster on the back: a perspective runway aimed at the CMA peak, with “Elevate your approach” at the footer.",
     "desc_es": "Un cartel alto de atardecer desértico en la espalda: una pista en perspectiva dirigida a la cumbre de CMA, con “Elevate your approach” al pie.",
     "alt": "Back of a navy tee with a tall framed desert sunset and runway leading toward the Copper Mountain Air mark",
     "alt_es": "Espalda de una camiseta navy con un atardecer desértico enmarcado y una pista que apunta a la marca de Copper Mountain Air"},
    {"id": "v2-collegiate-vintage-black-tee", "kind": "tee",
     "eyebrow": "Tee · Vintage black", "eyebrow_es": "Camiseta · Negro vintage",
     "name": "Nogales Collegiate Tee", "name_es": "Camiseta collegiate de Nogales",
     "desc": "Arched NOGALES, straight ARIZONA, and a big athletic KOLS — no enclosing frame, faded three-color ink with a light screen-print distress.",
     "desc_es": "NOGALES en arco, ARIZONA en línea recta y un KOLS grande de estilo atlético, sin marco, en tres colores desgastados.",
     "alt": "Washed vintage black tee with arched NOGALES, ARIZONA and a large KOLS in collegiate lettering",
     "alt_es": "Camiseta negra vintage con NOGALES, ARIZONA en arco y un KOLS grande de estilo universitario"},
    {"id": "v2-postcard-vintage-bone-tee", "kind": "tee",
     "eyebrow": "Tee · Bone · Vintage", "eyebrow_es": "Camiseta · Hueso · Vintage",
     "name": "Greetings from Nogales Tee", "name_es": "Camiseta Greetings from Nogales",
     "desc": "A rectangular travel postcard in a faded three-color palette, with saguaros, a setting sun, and Greetings from Nogales across the sky.",
     "desc_es": "Una postal de viaje rectangular en tres colores desgastados, con saguaros, un sol poniente y Greetings from Nogales en el cielo.",
     "alt": "Bone tee on adobe tile printed with a distressed Greetings from Nogales travel postcard",
     "alt_es": "Camiseta color hueso sobre loseta de adobe, con una postal desgastada de Greetings from Nogales"},
    {"id": "v2-lousy-tshirt-sand-tee", "kind": "tee",
     "eyebrow": "Tee · Sand · Slogan", "eyebrow_es": "Camiseta · Arena · Eslogan",
     "name": "Lousy T-Shirt", "name_es": "Lousy T-Shirt",
     "desc": "“I came all the way to Nogales and all I got was this lousy t-shirt.” Classic centered souvenir stack, half-sun and saguaros up top.",
     "desc_es": "“I came all the way to Nogales and all I got was this lousy t-shirt.” El clásico recuerdito centrado, con un medio sol y saguaros arriba.",
     "alt": "Sand tee with a souvenir-stack slogan: I came all the way to Nogales and all I got was this lousy t-shirt",
     "alt_es": "Camiseta color arena con el eslogan de recuerdo: I came all the way to Nogales and all I got was this lousy t-shirt"},
    {"id": "v2-crosswind-navy-folded", "kind": "tee",
     "eyebrow": "Tee · Navy · Slogan", "eyebrow_es": "Camiseta · Navy · Eslogan",
     "name": "Nogales Crosswind Tee", "name_es": "Camiseta del viento cruzado de Nogales",
     "desc": "“I survived the Nogales crosswind.” Left-aligned field-report layout with a five-band windsock and a dashed runway footer.",
     "desc_es": "“I survived the Nogales crosswind.” Composición alineada a la izquierda, con una manga de viento de cinco bandas y una pista punteada al pie.",
     "alt": "Folded navy tee with a left-aligned aviation layout and a windsock, reading I survived the Nogales crosswind",
     "alt_es": "Camiseta navy doblada con una composición aeronáutica y una manga de viento que dice I survived the Nogales crosswind"},
    {"id": "v3-runway-04-22-asphalt-tee", "kind": "tee",
     "eyebrow": "Tee · Asphalt", "eyebrow_es": "Camiseta · Asfalto",
     "name": "Runway 04/22 Tee", "name_es": "Camiseta Runway 04/22",
     "desc": "Big runway numerals in asphalt-paint stencil, with threshold stripes and verified KOLS data: 7,200 × 100 ft, elev. 3,955 ft, CTAF 122.8.",
     "desc_es": "Números grandes de pista en plantilla de pintura de asfalto, con franjas de umbral y datos verificados de KOLS: 7,200 × 100 ft, elev. 3,955 ft, CTAF 122.8.",
     "alt": "Washed asphalt-grey tee printed with large runway numerals 04/22, threshold stripes, and verified KOLS airfield data",
     "alt_es": "Camiseta gris asfalto con los números de pista 04/22, franjas de umbral y datos verificados del aeródromo KOLS"},
    {"id": "v3-sectional-chart-ivory-tee", "kind": "tee",
     "eyebrow": "Tee · Ivory", "eyebrow_es": "Camiseta · Marfil",
     "name": "KOLS Sectional Chart Tee", "name_es": "Camiseta de carta seccional de KOLS",
     "desc": "A stylized Phoenix Sectional of the KOLS area — VOR rose, runway heading, and an FAA-style data block. Not a copy of a real chart, and not for navigation.",
     "desc_es": "Una seccional estilizada de Phoenix de la zona de KOLS: rosa VOR, rumbo de pista y un bloque de datos al estilo FAA. No es copia de una carta real ni sirve para navegación.",
     "alt": "Ivory tee on walnut wood printed with a stylized Phoenix sectional chart of the KOLS area",
     "alt_es": "Camiseta marfil sobre madera de nogal, con una carta seccional estilizada de Phoenix de la zona de KOLS"},
    {"id": "v3-topo-contours-olive-tee", "kind": "tee",
     "eyebrow": "Tee · Desert olive", "eyebrow_es": "Camiseta · Olivo desértico",
     "name": "Patagonia &amp; Santa Rita Topo Tee", "name_es": "Camiseta topo de Patagonia y Santa Rita",
     "desc": "Unframed topographic contours of the ranges around the field, parting around the CMA peak. Elevation and coordinates underneath.",
     "desc_es": "Curvas de nivel de las sierras alrededor del campo, abriéndose en la cumbre de CMA, sin marco. Elevación y coordenadas debajo.",
     "alt": "Desert olive tee on sandstone printed with topographic contour lines parting around the Copper Mountain Air mark",
     "alt_es": "Camiseta olivo desértico sobre arenisca, con curvas de nivel que se abren alrededor de la marca de Copper Mountain Air"},
    {"id": "v3-luggage-tag-heather-tee", "kind": "tee",
     "eyebrow": "Tee · Heather grey", "eyebrow_es": "Camiseta · Gris jaspeado",
     "name": "Nogales Intl Luggage Tag Tee", "name_es": "Camiseta de etiqueta de equipaje Nogales Intl",
     "desc": "A vintage airline claim tag for destination Arizona: OLS, Nogales Intl, Runway 04/22, field elev. 3,955 ft MSL, and a barcode stub.",
     "desc_es": "Una etiqueta vintage de equipaje con destino a Arizona: OLS, Nogales Intl, pista 04/22, elev. 3,955 ft MSL, y un talón con código de barras.",
     "alt": "Heather grey tee on cedar planks printed with a vintage airline luggage tag reading OLS / Nogales Intl",
     "alt_es": "Camiseta gris jaspeado sobre tablones de cedro, con una etiqueta vintage de equipaje que dice OLS / Nogales Intl"},
    {"id": "v2-postcard-sand-hoodie", "kind": "hoodie",
     "eyebrow": "Hoodie · Sand", "eyebrow_es": "Sudadera · Arena",
     "name": "Greetings from Nogales Hoodie", "name_es": "Sudadera Greetings from Nogales",
     "desc": "The full-color travel postcard on a heavyweight sand pullover — saguaros, sunset, and the CMA mark on the horizon.",
     "desc_es": "La postal de viaje a todo color en una sudadera pesada color arena: saguaros, atardecer y la marca de CMA en el horizonte.",
     "alt": "Sand hoodie hanging on an adobe wall, printed with a full-color Greetings from Nogales travel postcard",
     "alt_es": "Sudadera color arena colgada en un muro de adobe, con una postal a color de Greetings from Nogales"},
    {"id": "v3-monochrome-tonal-hoodie", "kind": "hoodie",
     "eyebrow": "Hoodie · Matte black", "eyebrow_es": "Sudadera · Negro mate",
     "name": "Fuel. Freight. Flight. Hoodie", "name_es": "Sudadera Fuel. Freight. Flight.",
     "desc": "A stealth tonal print on heavyweight black fleece: the CMA mark, Copper Mountain Air, and the three words that describe the operation.",
     "desc_es": "Un estampado tonal discreto sobre felpa negra de peso pesado: la marca de CMA, Copper Mountain Air y las tres palabras que describen la operación.",
     "alt": "Matte black hoodie on a hanger with a subtle tonal Copper Mountain Air mark and the line Fuel. Freight. Flight.",
     "alt_es": "Sudadera negra mate en una percha, con la marca sutil de Copper Mountain Air y la línea Fuel. Freight. Flight."},
    {"id": "v3-fbo-crew-quarter-zip", "kind": "quarter-zip",
     "eyebrow": "Quarter-zip · Navy · Line crew", "eyebrow_es": "Cierre de un cuarto · Navy · Line crew",
     "name": "Line Crew Quarter-Zip", "name_es": "Quarter-zip de Line Crew",
     "desc": "A small left-chest embroidered crest — Copper Mountain Air, KOLS, Line Crew — on a navy quarter-zip built for the ramp.",
     "desc_es": "Un pequeño emblema bordado en el pecho izquierdo — Copper Mountain Air, KOLS, Line Crew — en un quarter-zip navy hecho para la rampa.",
     "alt": "Navy quarter-zip pullover hanging on a concrete wall, with a small embroidered Copper Mountain Air crest on the left chest",
     "alt_es": "Sudadera navy con cierre de un cuarto colgada en un muro de concreto, con un pequeño emblema bordado de Copper Mountain Air en el pecho izquierdo"},
    {"id": "v2-saguaro-trucker-cap", "kind": "cap",
     "eyebrow": "Trucker cap · Navy / white", "eyebrow_es": "Gorra trucker · Navy / blanca",
     "name": "Saguaro Patch Cap", "name_es": "Gorra con parche de saguaro",
     "desc": "The only round design in the lineup: a five-color saguaro and KOLS patch on a white foam front, navy mesh and bill.",
     "desc_es": "El único diseño redondo de la línea: un parche de saguaro y KOLS en cinco colores sobre un frente de foam blanco, con malla y visera navy.",
     "alt": "Navy and white trucker cap on a rustic wood workbench with a circular saguaro and KOLS embroidered-style patch on the front panel",
     "alt_es": "Gorra trucker navy y blanca sobre un banco de madera, con un parche circular de saguaro y KOLS en el frente"},
    {"id": "v2-saguaro-sticker-toolbox", "kind": "sticker",
     "eyebrow": "Sticker · Die-cut", "eyebrow_es": "Calcomanía · Troquelada",
     "name": "Saguaro Patch Sticker", "name_es": "Calcomanía del parche de saguaro",
     "desc": "The same saguaro patch as a kiss-cut vinyl sticker — built to live on a toolbox, a flight bag, or a water bottle.",
     "desc_es": "El mismo parche de saguaro en una calcomanía de vinilo: pensada para una caja de herramientas, una bolsa de vuelo o una botella.",
     "alt": "Die-cut saguaro and KOLS sticker applied to the lid of a red workshop toolbox",
     "alt_es": "Calcomanía troquelada de saguaro y KOLS pegada en la tapa de una caja de herramientas roja"},
    {"id": "v2-saguaro-koozie-tailgate", "kind": "koozie",
     "eyebrow": "Koozie · Navy", "eyebrow_es": "Enfriador · Navy",
     "name": "Saguaro Patch Koozie", "name_es": "Enfriador del parche de saguaro",
     "desc": "The saguaro patch wrapped on a navy can cooler. A small, useful piece of the field to throw in a bag.",
     "desc_es": "El parche de saguaro en un enfriador de lata navy. Una pieza pequeña y útil del campo para llevar en la bolsa.",
     "alt": "Navy can koozie on a pickup tailgate at golden hour, printed with the circular saguaro and KOLS patch",
     "alt_es": "Enfriador de lata navy sobre la puerta de una pickup al atardecer, con el parche circular de saguaro y KOLS"},
]

STORE_COLLECTIONS = [
    {
        "year": 2026,
        "drop": date(2026, 1, 1),
        "next_year": 2027,
        "next_drop": "January 1",
        "next_drop_es": "el 1 de enero",
        "title": "2026 Collection",
        "title_es": "Colección 2026",
        "h2": "From the ramp at 3,955 feet.",
        "h2_es": "Desde la rampa a 3,955 pies.",
        "lede": "Designs built around the field: Runway 04/22, the Patagonia and Santa Rita ranges, a vintage luggage tag, and a couple of slogan tees that only make sense if you’ve landed here. Buy buttons will go live once checkout is connected.",
        "lede_es": "Diseños inspirados en el campo: la pista 04/22, las sierras de Patagonia y Santa Rita, una etiqueta vintage de equipaje y un par de camisetas con frases que solo tienen sentido si ha aterrizado aquí. Los botones de compra se activarán cuando esté conectado el pago.",
        "products": PRODUCTS_2026,
    },
    # Add the 2027 Collection here (drop=date(2027, 1, 1), products=[...]) when that lineup is ready.
]

STORE_SUPPLIES = [
    {"icon": "map",
     "name": "Charts", "name_es": "Cartas",
     "desc": "Sectional charts and other current paper charts for the field and the surrounding airspace.",
     "desc_es": "Cartas seccionales y otras cartas actuales en papel para el campo y el espacio aéreo de la zona."},
    {"icon": "compass",
     "name": "Plotters &amp; E6Bs", "name_es": "Plotters y E6B",
     "desc": "Plotters and E6B flight computers for planning and training.",
     "desc_es": "Plotters y computadoras de vuelo E6B para planificación e instrucción."},
    {"icon": "book",
     "name": "Logbooks", "name_es": "Bitácoras",
     "desc": "Pilot and aircraft logbooks for students and certificated pilots.",
     "desc_es": "Bitácoras de piloto y de aeronave para estudiantes y pilotos certificados."},
    {"icon": "headset",
     "name": "Headsets &amp; accessories", "name_es": "Audífonos y accesorios",
     "desc": "Headsets and small cockpit accessories when we have them in stock.",
     "desc_es": "Audífonos y accesorios pequeños de cabina cuando hay existencia."},
]


def featured_collection(today=None):
    """Latest collection whose drop date has arrived and that has products."""
    today = today or date.today()
    ready = [c for c in STORE_COLLECTIONS if c.get("products") and c["drop"] <= today]
    if not ready:
        return STORE_COLLECTIONS[0]
    return max(ready, key=lambda c: c["year"])


def past_collections(today=None):
    """Older collections, still listed and purchasable. Empty until a newer year is featured."""
    feat = featured_collection(today)
    return [c for c in STORE_COLLECTIONS
            if c["year"] < feat["year"] and c.get("products")]


def collection_tagline(coll, es=False):
    if es:
        return (f"Una nueva línea cada año — la Colección {coll['next_year']} "
                f"sale {coll['next_drop_es']}.")
    return (f"A new lineup every year — the {coll['next_year']} Collection "
            f"drops {coll['next_drop']}.")

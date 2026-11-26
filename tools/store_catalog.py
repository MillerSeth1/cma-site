"""Copper Mountain Air merch catalog.

All collection and product data lives here so a new yearly lineup can be
added in one place. featured_collection() picks the latest collection whose
drop date has arrived and that has products. Older collections automatically
move to Past Collections and stay listed and purchasable.

Apparel designs are one card with Style / Size / Color selectors. Add a
style by appending to the design's ``styles`` dict and dropping a matching
mockup in assets/img/store/. Hard goods (cap, sticker, koozie) stay simple
single-image cards.

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
    "snapback": 32,
    "dad-hat": 30,
    "polo": 38,
    "trucker": 38,
    "camp-cap": 36,
    "rope-cap": 34,
    "corduroy": 36,
    "washed-cap": 34,
    "suede-bill": 38,
    "sticker": 4,
    "koozie": 10,
    "luggage-tag": 14,
}

STORE_PRICE_LABELS = {k: f"${v}" for k, v in STORE_PRICES.items()}

APPAREL_SIZES = ["S", "M", "L", "XL", "2XL"]

STYLE_LABELS = {
    "tee": ("Tee", "Camiseta"),
    "long-sleeve": ("Long sleeve", "Manga larga"),
    "hoodie": ("Hoodie", "Sudadera"),
    "quarter-zip": ("Quarter-zip", "Quarter-zip"),
    "jacket": ("Jacket", "Chaqueta"),
    "polo": ("Polo", "Polo"),
    "snapback": ("Snapback", "Snapback"),
    "dad-hat": ("Dad hat", "Gorra dad"),
    "trucker": ("Trucker", "Trucker"),
    "camp-cap": ("Camp cap", "Gorra camp"),
    "rope-cap": ("Rope cap", "Gorra de cuerda"),
    "corduroy": ("Corduroy", "Pana"),
    "washed-cap": ("Washed cap", "Gorra lavada"),
    "suede-bill": ("Suede-bill cap", "Gorra de visera de ante"),
}

COLOR_LABELS = {
    "natural": ("Natural", "Natural"),
    "navy": ("Navy", "Navy"),
    "sand": ("Sand", "Arena"),
    "black": ("Black", "Negro"),
    "bone": ("Bone", "Hueso"),
    "vintage-black": ("Vintage black", "Negro vintage"),
    "asphalt": ("Asphalt", "Asfalto"),
    "ivory": ("Ivory", "Marfil"),
    "olive": ("Desert olive", "Olivo desértico"),
    "heather": ("Heather grey", "Gris jaspeado"),
    "navy-white": ("Navy / white", "Navy / blanca"),
    "white": ("White", "Blanco"),
    "khaki": ("Khaki", "Khaki"),
    "steel": ("Steel grey", "Gris acero"),
    "brown": ("Brown", "Marrón"),
    "evergreen": ("Evergreen", "Verde bosque"),
    "oak": ("Oak", "Roble"),
    "light-blue": ("Light blue", "Azul claro"),
    "black-white": ("Black / white", "Negro / blanca"),
    "brown-khaki": ("Brown / khaki", "Marrón / khaki"),
    "olive-green": ("Olive", "Olivo"),
}


def c(cid, image, alt, alt_es):
    return {"id": cid, "image": image, "alt": alt, "alt_es": alt_es}


def styles(**kwargs):
    return {sid: {"colors": colors} for sid, colors in kwargs.items()}


PRODUCTS_2026 = [
    {"id": "ridgeline", "picker": "apparel", "default_style": "tee", "default_color": "natural",
     "sizes": APPAREL_SIZES,
     "name": "Ridgeline Wordmark", "name_es": "Ridgeline Wordmark",
     "desc": "A wide horizontal mountain and saguaro line, with the CMA mark as the peak and Copper Mountain Air set cleanly beneath.",
     "desc_es": "Una línea horizontal de montañas y saguaros, con la marca de CMA en la cumbre y Copper Mountain Air debajo.",
     "styles": styles(
         tee=[c("natural", "v2-ridgeline-natural-tee",
                "Natural tee flat-laid on wood, printed with a wide mountain ridgeline and the Copper Mountain Air wordmark",
                "Camiseta natural extendida sobre madera, con una línea de montañas y el logotipo de Copper Mountain Air")],
         **{"long-sleeve": [c("natural", "ridgeline-natural-ls",
                "Natural long-sleeve shirt on wood, printed with a wide mountain ridgeline and the Copper Mountain Air wordmark",
                "Camiseta de manga larga natural sobre madera, con una línea de montañas y el logotipo de Copper Mountain Air")]},
         hoodie=[c("sand", "ridgeline-sand-hoodie",
                "Sand hoodie hanging on an adobe wall, printed with a wide mountain ridgeline and the Copper Mountain Air wordmark",
                "Sudadera color arena colgada en un muro de adobe, con una línea de montañas y el logotipo de Copper Mountain Air")],
     )},
    {"id": "left-chest", "picker": "apparel", "default_style": "tee", "default_color": "navy",
     "sizes": APPAREL_SIZES, "note": "Left chest", "note_es": "Pecho izquierdo",
     "name": "Left-Chest Crest", "name_es": "Emblema al pecho",
     "desc": "A small CMA mark and stacked wordmark on the left chest — the quiet everyday shirt. On the quarter-zip, jacket, and Port Authority polo the crest is embroidered. Pairs with the runway back print.",
     "desc_es": "Una marca pequeña de CMA y el nombre apilado en el pecho izquierdo: la camiseta discreta para todos los días. En el quarter-zip, la chaqueta y el polo Port Authority el emblema va bordado. Combina con el estampado de pista en la espalda.",
     "styles": styles(
         tee=[c("navy", "v2-left-chest-navy-tee",
                "Navy tee with a small left-chest Copper Mountain Air crest and KOLS wordmark",
                "Camiseta navy con un pequeño emblema de Copper Mountain Air y KOLS en el pecho izquierdo")],
         **{"long-sleeve": [c("navy", "left-chest-navy-ls",
                "Navy long-sleeve shirt with a small left-chest Copper Mountain Air crest and KOLS wordmark",
                "Camiseta de manga larga navy con un pequeño emblema de Copper Mountain Air y KOLS en el pecho izquierdo")]},
         hoodie=[c("black", "left-chest-black-hoodie",
                "Black hoodie with a small left-chest Copper Mountain Air crest and KOLS wordmark",
                "Sudadera negra con un pequeño emblema de Copper Mountain Air y KOLS en el pecho izquierdo")],
         **{"quarter-zip": [c("navy", "left-chest-navy-qz",
                "Navy quarter-zip with an embroidered Copper Mountain Air crest on the left chest",
                "Quarter-zip navy con un emblema bordado de Copper Mountain Air en el pecho izquierdo")]},
         jacket=[c("navy", "left-chest-navy-jacket",
                "Navy SOL'S windbreaker with an embroidered Copper Mountain Air crest on the left chest",
                "Cortavientos navy SOL'S con un emblema bordado de Copper Mountain Air en el pecho izquierdo")],
         polo=[
            c("navy", "left-chest-navy-polo",
              "Navy Port Authority polo hanging on a concrete wall, with an embroidered Copper Mountain Air crest on the left chest",
              "Polo navy Port Authority colgado en un muro de concreto, con un emblema bordado de Copper Mountain Air en el pecho izquierdo"),
            c("black", "left-chest-black-polo",
              "Black Port Authority polo hanging on a concrete wall, with an embroidered Copper Mountain Air crest on the left chest",
              "Polo negro Port Authority colgado en un muro de concreto, con un emblema bordado de Copper Mountain Air en el pecho izquierdo"),
            c("white", "left-chest-white-polo",
              "White Port Authority polo hanging on a concrete wall, with an embroidered Copper Mountain Air crest on the left chest",
              "Polo blanco Port Authority colgado en un muro de concreto, con un emblema bordado de Copper Mountain Air en el pecho izquierdo"),
            c("heather", "left-chest-heather-polo",
              "Heather grey Port Authority polo hanging on a concrete wall, with an embroidered Copper Mountain Air crest on the left chest",
              "Polo gris heather Port Authority colgado en un muro de concreto, con un emblema bordado de Copper Mountain Air en el pecho izquierdo"),
            c("steel", "left-chest-steel-polo",
              "Steel grey Port Authority polo hanging on a concrete wall, with an embroidered Copper Mountain Air crest on the left chest",
              "Polo gris acero Port Authority colgado en un muro de concreto, con un emblema bordado de Copper Mountain Air en el pecho izquierdo"),
         ],
     )},
    {"id": "runway-approach", "picker": "apparel", "default_style": "tee", "default_color": "navy",
     "sizes": APPAREL_SIZES, "note": "Back print", "note_es": "Estampado en la espalda",
     "name": "Runway Approach", "name_es": "Aproximación a pista",
     "desc": "A tall desert-sunset poster on the back: a perspective runway aimed at the CMA peak, with “Elevate your approach” at the footer.",
     "desc_es": "Un cartel alto de atardecer desértico en la espalda: una pista en perspectiva dirigida a la cumbre de CMA, con “Elevate your approach” al pie.",
     "styles": styles(
         tee=[c("navy", "v2-back-print-navy-tee",
                "Back of a navy tee with a tall framed desert sunset and runway leading toward the Copper Mountain Air mark",
                "Espalda de una camiseta navy con un atardecer desértico enmarcado y una pista que apunta a la marca de Copper Mountain Air")],
     )},
    {"id": "collegiate", "picker": "apparel", "default_style": "tee", "default_color": "vintage-black",
     "sizes": APPAREL_SIZES,
     "name": "Nogales Collegiate", "name_es": "Collegiate de Nogales",
     "desc": "Arched NOGALES, straight ARIZONA, and a big athletic KOLS — no enclosing frame, faded three-color ink with a light screen-print distress.",
     "desc_es": "NOGALES en arco, ARIZONA en línea recta y un KOLS grande de estilo atlético, sin marco, en tres colores desgastados.",
     "styles": styles(
         tee=[c("vintage-black", "v2-collegiate-vintage-black-tee",
                "Washed vintage black tee with arched NOGALES, ARIZONA and a large KOLS in collegiate lettering",
                "Camiseta negra vintage con NOGALES, ARIZONA en arco y un KOLS grande de estilo universitario")],
         **{"long-sleeve": [c("navy", "collegiate-navy-ls",
                "Navy long-sleeve shirt with arched NOGALES, ARIZONA and a large KOLS in collegiate lettering",
                "Camiseta de manga larga navy con NOGALES, ARIZONA en arco y un KOLS grande de estilo universitario")]},
         hoodie=[c("black", "collegiate-black-hoodie",
                "Black hoodie with arched NOGALES, ARIZONA and a large KOLS in collegiate lettering",
                "Sudadera negra con NOGALES, ARIZONA en arco y un KOLS grande de estilo universitario")],
     )},
    {"id": "greetings", "picker": "apparel", "default_style": "tee", "default_color": "bone",
     "sizes": APPAREL_SIZES,
     "name": "Greetings from Nogales", "name_es": "Greetings from Nogales",
     "desc": "A rectangular travel postcard — saguaros, a setting sun, and Greetings from Nogales across the sky. The tee is a faded three-color vintage print; the hoodie and long sleeve use the full-color postcard.",
     "desc_es": "Una postal de viaje rectangular, con saguaros, un sol poniente y Greetings from Nogales en el cielo. La camiseta es una impresión vintage en tres colores; la sudadera y la manga larga usan la postal a todo color.",
     "styles": styles(
         tee=[c("bone", "v2-postcard-vintage-bone-tee",
                "Bone tee on adobe tile printed with a distressed Greetings from Nogales travel postcard",
                "Camiseta color hueso sobre loseta de adobe, con una postal desgastada de Greetings from Nogales")],
         **{"long-sleeve": [c("natural", "postcard-natural-ls",
                "Natural long-sleeve shirt on wood, printed with a Greetings from Nogales travel postcard",
                "Camiseta de manga larga natural sobre madera, con una postal de Greetings from Nogales")]},
         hoodie=[c("sand", "v2-postcard-sand-hoodie",
                "Sand hoodie hanging on an adobe wall, printed with a full-color Greetings from Nogales travel postcard",
                "Sudadera color arena colgada en un muro de adobe, con una postal a color de Greetings from Nogales")],
     )},
    {"id": "lousy", "picker": "apparel", "default_style": "tee", "default_color": "sand",
     "sizes": APPAREL_SIZES,
     "name": "Lousy T-Shirt", "name_es": "Lousy T-Shirt",
     "desc": "“I came all the way to Nogales and all I got was this lousy t-shirt.” Classic centered souvenir stack, half-sun and saguaros up top.",
     "desc_es": "“I came all the way to Nogales and all I got was this lousy t-shirt.” El clásico recuerdito centrado, con un medio sol y saguaros arriba.",
     "styles": styles(
         tee=[c("sand", "v2-lousy-tshirt-sand-tee",
                "Sand tee with a souvenir-stack slogan: I came all the way to Nogales and all I got was this lousy t-shirt",
                "Camiseta color arena con el eslogan de recuerdo: I came all the way to Nogales and all I got was this lousy t-shirt")],
         **{"long-sleeve": [c("natural", "lousy-natural-ls",
                "Natural long-sleeve shirt with a souvenir-stack slogan: I came all the way to Nogales and all I got was this lousy t-shirt",
                "Camiseta de manga larga natural con el eslogan de recuerdo: I came all the way to Nogales and all I got was this lousy t-shirt")]},
         hoodie=[c("sand", "lousy-sand-hoodie",
                "Sand hoodie with a souvenir-stack slogan: I came all the way to Nogales and all I got was this lousy t-shirt",
                "Sudadera color arena con el eslogan de recuerdo: I came all the way to Nogales and all I got was this lousy t-shirt")],
     )},
    {"id": "crosswind", "picker": "apparel", "default_style": "tee", "default_color": "navy",
     "sizes": APPAREL_SIZES,
     "name": "Nogales Crosswind", "name_es": "Viento cruzado de Nogales",
     "desc": "“I survived the Nogales crosswind.” Left-aligned field-report layout with a five-band windsock and a dashed runway footer.",
     "desc_es": "“I survived the Nogales crosswind.” Composición alineada a la izquierda, con una manga de viento de cinco bandas y una pista punteada al pie.",
     "styles": styles(
         tee=[c("navy", "v2-crosswind-navy-folded",
                "Folded navy tee with a left-aligned aviation layout and a windsock, reading I survived the Nogales crosswind",
                "Camiseta navy doblada con una composición aeronáutica y una manga de viento que dice I survived the Nogales crosswind")],
         **{"long-sleeve": [c("navy", "crosswind-navy-ls",
                "Navy long-sleeve shirt with a left-aligned aviation layout and a windsock, reading I survived the Nogales crosswind",
                "Camiseta de manga larga navy con una composición aeronáutica y una manga de viento que dice I survived the Nogales crosswind")]},
         hoodie=[c("black", "crosswind-black-hoodie",
                "Black hoodie with a left-aligned aviation layout and a windsock, reading I survived the Nogales crosswind",
                "Sudadera negra con una composición aeronáutica y una manga de viento que dice I survived the Nogales crosswind")],
     )},
    {"id": "runway-0422", "picker": "apparel", "default_style": "tee", "default_color": "asphalt",
     "sizes": APPAREL_SIZES,
     "name": "Runway 04/22", "name_es": "Runway 04/22",
     "desc": "Big runway numerals in asphalt-paint stencil, with threshold stripes and verified KOLS data: 7,200 × 100 ft, elev. 3,955 ft, CTAF 122.8.",
     "desc_es": "Números grandes de pista en plantilla de pintura de asfalto, con franjas de umbral y datos verificados de KOLS: 7,200 × 100 ft, elev. 3,955 ft, CTAF 122.8.",
     "styles": styles(
         tee=[c("asphalt", "v3-runway-04-22-asphalt-tee",
                "Washed asphalt-grey tee printed with large runway numerals 04/22, threshold stripes, and verified KOLS airfield data",
                "Camiseta gris asfalto con los números de pista 04/22, franjas de umbral y datos verificados del aeródromo KOLS")],
         **{"long-sleeve": [c("navy", "runway-0422-navy-ls",
                "Navy long-sleeve shirt printed with large runway numerals 04/22, threshold stripes, and verified KOLS airfield data",
                "Camiseta de manga larga navy con los números de pista 04/22, franjas de umbral y datos verificados del aeródromo KOLS")]},
         hoodie=[c("black", "runway-0422-black-hoodie",
                "Black hoodie printed with large runway numerals 04/22, threshold stripes, and verified KOLS airfield data",
                "Sudadera negra con los números de pista 04/22, franjas de umbral y datos verificados del aeródromo KOLS")],
     )},
    {"id": "sectional", "picker": "apparel", "default_style": "tee", "default_color": "ivory",
     "sizes": APPAREL_SIZES,
     "name": "KOLS Sectional Chart", "name_es": "Carta seccional de KOLS",
     "desc": "A stylized Phoenix Sectional of the KOLS area — VOR rose, runway heading, and an FAA-style data block. Not a copy of a real chart, and not for navigation.",
     "desc_es": "Una seccional estilizada de Phoenix de la zona de KOLS: rosa VOR, rumbo de pista y un bloque de datos al estilo FAA. No es copia de una carta real ni sirve para navegación.",
     "styles": styles(
         tee=[c("ivory", "v3-sectional-chart-ivory-tee",
                "Ivory tee on walnut wood printed with a stylized Phoenix sectional chart of the KOLS area",
                "Camiseta marfil sobre madera de nogal, con una carta seccional estilizada de Phoenix de la zona de KOLS")],
         **{"long-sleeve": [c("natural", "sectional-natural-ls",
                "Natural long-sleeve shirt printed with a stylized Phoenix sectional chart of the KOLS area",
                "Camiseta de manga larga natural con una carta seccional estilizada de Phoenix de la zona de KOLS")]},
         hoodie=[c("sand", "sectional-sand-hoodie",
                "Sand hoodie printed with a stylized Phoenix sectional chart of the KOLS area",
                "Sudadera color arena con una carta seccional estilizada de Phoenix de la zona de KOLS")],
     )},
    {"id": "topo", "picker": "apparel", "default_style": "tee", "default_color": "olive",
     "sizes": APPAREL_SIZES,
     "name": "Patagonia &amp; Santa Rita Topo", "name_es": "Topo de Patagonia y Santa Rita",
     "desc": "Unframed topographic contours of the ranges around the field, parting around the CMA peak. Elevation and coordinates underneath.",
     "desc_es": "Curvas de nivel de las sierras alrededor del campo, abriéndose en la cumbre de CMA, sin marco. Elevación y coordenadas debajo.",
     "styles": styles(
         tee=[c("olive", "v3-topo-contours-olive-tee",
                "Desert olive tee on sandstone printed with topographic contour lines parting around the Copper Mountain Air mark",
                "Camiseta olivo desértico sobre arenisca, con curvas de nivel que se abren alrededor de la marca de Copper Mountain Air")],
         **{"long-sleeve": [c("navy", "topo-navy-ls",
                "Navy long-sleeve shirt printed with topographic contour lines parting around the Copper Mountain Air mark",
                "Camiseta de manga larga navy con curvas de nivel que se abren alrededor de la marca de Copper Mountain Air")]},
         hoodie=[c("black", "topo-black-hoodie",
                "Black hoodie printed with topographic contour lines parting around the Copper Mountain Air mark",
                "Sudadera negra con curvas de nivel que se abren alrededor de la marca de Copper Mountain Air")],
     )},
    {"id": "luggage-tag-tee", "picker": "apparel", "default_style": "tee", "default_color": "heather",
     "sizes": APPAREL_SIZES,
     "name": "Nogales Intl Luggage Tag", "name_es": "Etiqueta de equipaje Nogales Intl",
     "desc": "A vintage airline claim tag for destination Arizona: OLS, Nogales Intl, Runway 04/22, field elev. 3,955 ft MSL, and a barcode stub.",
     "desc_es": "Una etiqueta vintage de equipaje con destino a Arizona: OLS, Nogales Intl, pista 04/22, elev. 3,955 ft MSL, y un talón con código de barras.",
     "styles": styles(
         tee=[c("heather", "v3-luggage-tag-heather-tee",
                "Heather grey tee on cedar planks printed with a vintage airline luggage tag reading OLS / Nogales Intl",
                "Camiseta gris jaspeado sobre tablones de cedro, con una etiqueta vintage de equipaje que dice OLS / Nogales Intl")],
         **{"long-sleeve": [c("natural", "luggage-tag-natural-ls",
                "Natural long-sleeve shirt printed with a vintage airline luggage tag reading OLS / Nogales Intl",
                "Camiseta de manga larga natural con una etiqueta vintage de equipaje que dice OLS / Nogales Intl")]},
         hoodie=[c("sand", "luggage-tag-sand-hoodie",
                "Sand hoodie printed with a vintage airline luggage tag reading OLS / Nogales Intl",
                "Sudadera color arena con una etiqueta vintage de equipaje que dice OLS / Nogales Intl")],
     )},
    {"id": "tonal-hoodie", "picker": "apparel", "default_style": "hoodie", "default_color": "black",
     "sizes": APPAREL_SIZES,
     "name": "Fuel. Freight. Flight.", "name_es": "Fuel. Freight. Flight.",
     "desc": "A stealth tonal print on heavyweight black fleece: the CMA mark, Copper Mountain Air, and the three words that describe the operation. This design is on the hoodie only.",
     "desc_es": "Un estampado tonal discreto sobre felpa negra de peso pesado: la marca de CMA, Copper Mountain Air y las tres palabras que describen la operación. Este diseño es solo en sudadera.",
     "styles": styles(
         hoodie=[c("black", "v3-monochrome-tonal-hoodie",
                "Matte black hoodie on a hanger with a subtle tonal Copper Mountain Air mark and the line Fuel. Freight. Flight.",
                "Sudadera negra mate en una percha, con la marca sutil de Copper Mountain Air y la línea Fuel. Freight. Flight.")],
     )},
    {"id": "line-crew", "picker": "apparel", "default_style": "quarter-zip", "default_color": "navy",
     "sizes": APPAREL_SIZES, "note": "Line crew", "note_es": "Line crew",
     "name": "Line Crew", "name_es": "Line Crew",
     "desc": "A small left-chest crest — Copper Mountain Air, KOLS, Line Crew. Embroidered on the navy quarter-zip, the SOL’S 32000 windbreaker, and the Port Authority polo; printed on the tee and long sleeve.",
     "desc_es": "Un pequeño emblema al pecho izquierdo — Copper Mountain Air, KOLS, Line Crew. Bordado en el quarter-zip navy, el cortavientos SOL’S 32000 y el polo Port Authority; impreso en la camiseta y la manga larga.",
     "styles": styles(
         tee=[c("navy", "line-crew-navy-tee",
                "Navy tee with a small left-chest Copper Mountain Air Line Crew crest",
                "Camiseta navy con un pequeño emblema Line Crew de Copper Mountain Air en el pecho izquierdo")],
         **{"long-sleeve": [c("navy", "line-crew-navy-ls",
                "Navy long-sleeve shirt with a small left-chest Copper Mountain Air Line Crew crest",
                "Camiseta de manga larga navy con un pequeño emblema Line Crew de Copper Mountain Air en el pecho izquierdo")]},
         **{"quarter-zip": [c("navy", "v3-fbo-crew-quarter-zip",
                "Navy quarter-zip pullover hanging on a concrete wall, with a small embroidered Copper Mountain Air crest on the left chest",
                "Sudadera navy con cierre de un cuarto colgada en un muro de concreto, con un pequeño emblema bordado de Copper Mountain Air en el pecho izquierdo")]},
         jacket=[c("navy", "line-crew-navy-jacket",
                "Navy SOL'S windbreaker with an embroidered Copper Mountain Air Line Crew crest on the left chest",
                "Cortavientos navy SOL'S con un emblema bordado Line Crew de Copper Mountain Air en el pecho izquierdo")],
         polo=[
            c("navy", "line-crew-navy-polo",
              "Navy Port Authority polo hanging on a concrete wall, with an embroidered Copper Mountain Air Line Crew crest on the left chest",
              "Polo navy Port Authority colgado en un muro de concreto, con un emblema bordado Line Crew de Copper Mountain Air en el pecho izquierdo"),
            c("black", "line-crew-black-polo",
              "Black Port Authority polo hanging on a concrete wall, with an embroidered Copper Mountain Air Line Crew crest on the left chest",
              "Polo negro Port Authority colgado en un muro de concreto, con un emblema bordado Line Crew de Copper Mountain Air en el pecho izquierdo"),
         ],
     )},


    {"id": "leather-patch-trucker", "picker": "apparel", "default_style": "trucker", "default_color": "navy-white",
     "sizes": [],
     "name": "Leather Patch Trucker", "name_es": "Trucker con parche de cuero",
     "desc": "A structured Yupoong 6606 retro trucker with a saddle-leather patch: the official mountain mark, COPPER MOUNTAIN AIR®, and KOLS · NOGALES, AZ, laser-etched and stitched at the edge. One size, plastic snap. The leather patch is a specialty decoration on the 6606 blank.",
     "desc_es": "Un trucker estructurado Yupoong 6606 con un parche de cuero: el emblema oficial de montaña, COPPER MOUNTAIN AIR® y KOLS · NOGALES, AZ, grabados con láser y costura en el borde. Talla única, broche de plástico. El parche de cuero es una decoración especial sobre el blank 6606.",
     "styles": styles(
         trucker=[
            c("navy-white", "hat-leather-trucker-navy-white",
              "Navy and cream Yupoong 6606 trucker with a saddle-leather patch of the official Copper Mountain Air® mark and wordmark",
              "Trucker Yupoong 6606 navy y crema con un parche de cuero del emblema y el nombre oficiales de Copper Mountain Air®"),
            c("black-white", "hat-leather-trucker-black-white",
              "Black and white Yupoong 6606 trucker with a saddle-leather patch of the official Copper Mountain Air® mark and wordmark",
              "Trucker Yupoong 6606 negro y blanco con un parche de cuero del emblema y el nombre oficiales de Copper Mountain Air®"),
            c("brown-khaki", "hat-leather-trucker-brown-khaki",
              "Brown and khaki Yupoong 6606 trucker with a saddle-leather patch of the official Copper Mountain Air® mark and wordmark",
              "Trucker Yupoong 6606 marrón y khaki con un parche de cuero del emblema y el nombre oficiales de Copper Mountain Air®"),
            c("evergreen", "hat-leather-trucker-evergreen",
              "Evergreen Yupoong 6606 trucker with a saddle-leather patch of the official Copper Mountain Air® mark and wordmark",
              "Trucker Yupoong 6606 verde bosque con un parche de cuero del emblema y el nombre oficiales de Copper Mountain Air®"),
         ],
     )},
    {"id": "desert-woven-camp", "picker": "apparel", "default_style": "camp-cap", "default_color": "khaki",
     "sizes": [],
     "name": "Desert Woven Camp", "name_es": "Gorra camp de tejido desértico",
     "desc": "A Yupoong 7005 five-panel camp cap with a rectangular merrowed woven patch: sunset field, saguaro silhouettes, the official mountain mark, and COPPER MOUNTAIN AIR®. Not a round badge. One size.",
     "desc_es": "Una gorra camp de cinco paneles Yupoong 7005 con un parche tejido rectangular con borde merrow: atardecer, siluetas de saguaro, el emblema oficial de montaña y COPPER MOUNTAIN AIR®. No es un parche redondo. Talla única.",
     "styles": styles(
         **{"camp-cap": [
            c("khaki", "hat-woven-camp-khaki",
              "Khaki Yupoong 7005 five-panel camp cap with a rectangular woven sunset and saguaro patch and the official Copper Mountain Air® mark",
              "Gorra camp Yupoong 7005 khaki de cinco paneles con un parche tejido rectangular de atardecer y saguaros y el emblema oficial de Copper Mountain Air®"),
            c("navy", "hat-woven-camp-navy",
              "Navy Yupoong 7005 five-panel camp cap with a rectangular woven sunset and saguaro patch and the official Copper Mountain Air® mark",
              "Gorra camp Yupoong 7005 navy de cinco paneles con un parche tejido rectangular de atardecer y saguaros y el emblema oficial de Copper Mountain Air®"),
            c("olive-green", "hat-woven-camp-olive",
              "Olive Yupoong 7005 five-panel camp cap with a rectangular woven sunset and saguaro patch and the official Copper Mountain Air® mark",
              "Gorra camp Yupoong 7005 olivo de cinco paneles con un parche tejido rectangular de atardecer y saguaros y el emblema oficial de Copper Mountain Air®"),
            c("black", "hat-woven-camp-black",
              "Black Yupoong 7005 five-panel camp cap with a rectangular woven sunset and saguaro patch and the official Copper Mountain Air® mark",
              "Gorra camp Yupoong 7005 negra de cinco paneles con un parche tejido rectangular de atardecer y saguaros y el emblema oficial de Copper Mountain Air®"),
         ]},
     )},
    {"id": "kols-rope-cap", "picker": "apparel", "default_style": "rope-cap", "default_color": "navy",
     "sizes": [],
     "name": "KOLS Rope Cap", "name_es": "Gorra de cuerda KOLS",
     "desc": "A classic Richardson 258 rope cap with cream embroidery: a small official mountain mark, KOLS, runway-threshold bars, and COPPER MOUNTAIN AIR® above the rope. One size. Navy is a Richardson 258 Navy/White colorway; Black/White and Light Blue/White are in Printful's current 258 catalog.",
     "desc_es": "Una gorra clásica Richardson 258 con cuerda y bordado en crema: un pequeño emblema oficial de montaña, KOLS, barras de umbral de pista y COPPER MOUNTAIN AIR® sobre la cuerda. Talla única. El navy es el color Navy/White de Richardson 258; Black/White y Light Blue/White figuran en el catálogo actual de Printful.",
     "styles": styles(
         **{"rope-cap": [
            c("navy", "hat-rope-navy",
              "Navy Richardson 258 rope cap with cream embroidery of the official mark, KOLS, runway bars, and Copper Mountain Air®",
              "Gorra de cuerda Richardson 258 navy con bordado en crema del emblema oficial, KOLS, barras de pista y Copper Mountain Air®"),
            c("black", "hat-rope-black",
              "Black Richardson 258 rope cap with a white rope and cream embroidery of the official mark, KOLS, runway bars, and Copper Mountain Air®",
              "Gorra de cuerda Richardson 258 negra con cuerda blanca y bordado en crema del emblema oficial, KOLS, barras de pista y Copper Mountain Air®"),
            c("light-blue", "hat-rope-light-blue",
              "Light blue Richardson 258 rope cap with a white rope and cream embroidery of the official mark, KOLS, runway bars, and Copper Mountain Air®",
              "Gorra de cuerda Richardson 258 azul claro con cuerda blanca y bordado en crema del emblema oficial, KOLS, barras de pista y Copper Mountain Air®"),
         ]},
     )},
    {"id": "corduroy-script-cap", "picker": "apparel", "default_style": "corduroy", "default_color": "brown",
     "sizes": [],
     "name": "Corduroy Chain-Stitch", "name_es": "Gorra de pana con cadeneta",
     "desc": "A low-profile Big Accessories BA703 vintage corduroy cap with Copper Mountain Air® in cream chain-stitch script on the front. One size.",
     "desc_es": "Una gorra de pana vintage de perfil bajo Big Accessories BA703, con Copper Mountain Air® bordado en cadeneta color crema al frente. Talla única.",
     "styles": styles(
         corduroy=[
            c("brown", "hat-corduroy-brown",
              "Brown corduroy cap with Copper Mountain Air® in cream chain-stitch script",
              "Gorra de pana marrón con Copper Mountain Air® en cadeneta color crema"),
            c("black", "hat-corduroy-black",
              "Black corduroy cap with Copper Mountain Air® in cream chain-stitch script",
              "Gorra de pana negra con Copper Mountain Air® en cadeneta color crema"),
            c("navy", "hat-corduroy-navy",
              "Navy corduroy cap with Copper Mountain Air® in cream chain-stitch script",
              "Gorra de pana navy con Copper Mountain Air® en cadeneta color crema"),
            c("olive-green", "hat-corduroy-olive",
              "Olive corduroy cap with Copper Mountain Air® in cream chain-stitch script",
              "Gorra de pana olivo con Copper Mountain Air® en cadeneta color crema"),
         ],
     )},
    {"id": "vintage-wing-badge", "picker": "apparel", "default_style": "washed-cap", "default_color": "olive-green",
     "sizes": [],
     "name": "Vintage Wing Badge", "name_es": "Insignia de alas vintage",
     "desc": "A garment-washed Yupoong 6245EC EcoWash dad hat with a small embroidered airline-style wing badge: the official mountain mark in a gold and navy disc, COPPER MOUNTAIN AIR®, and EST. 2026. One size.",
     "desc_es": "Una gorra dad lavada Yupoong 6245EC EcoWash con una pequeña insignia bordada de alas de aerolínea: el emblema oficial de montaña en un disco dorado y navy, COPPER MOUNTAIN AIR® y EST. 2026. Talla única.",
     "styles": styles(
         **{"washed-cap": [
            c("olive-green", "hat-wings-olive",
              "Washed olive Yupoong EcoWash dad hat with an embroidered vintage wing badge and Copper Mountain Air®",
              "Gorra dad Yupoong EcoWash olivo lavado con una insignia bordada de alas vintage y Copper Mountain Air®"),
            c("black", "hat-wings-black",
              "Washed black Yupoong EcoWash dad hat with an embroidered vintage wing badge and Copper Mountain Air®",
              "Gorra dad Yupoong EcoWash negro lavado con una insignia bordada de alas vintage y Copper Mountain Air®"),
            c("navy", "hat-wings-navy",
              "Washed navy Yupoong EcoWash dad hat with an embroidered vintage wing badge and Copper Mountain Air®",
              "Gorra dad Yupoong EcoWash navy lavado con una insignia bordada de alas vintage y Copper Mountain Air®"),
            c("oak", "hat-wings-oak",
              "Washed oak Yupoong EcoWash dad hat with an embroidered vintage wing badge and Copper Mountain Air®",
              "Gorra dad Yupoong EcoWash oak lavado con una insignia bordada de alas vintage y Copper Mountain Air®"),
         ]},
     )},
    {"id": "suede-bill-leather", "picker": "apparel", "default_style": "suede-bill", "default_color": "olive-green",
     "sizes": [],
     "name": "Suede-Bill Leather Mark", "name_es": "Marca de cuero con visera de ante",
     "desc": "An unstructured cap with a chocolate suede visor and a small saddle-leather patch of the official mountain mark®, plus a side COPPER MOUNTAIN AIR wordmark. One size. A specialty two-tone blank — not in Printful's current catalog.",
     "desc_es": "Una gorra desestructurada con visera de ante chocolate y un pequeño parche de cuero con el emblema oficial de montaña®, más un Copper Mountain Air en el costado. Talla única. Un blank bicolor de proveedor especial, que no figura en el catálogo actual de Printful.",
     "styles": styles(
         **{"suede-bill": [
            c("olive-green", "hat-suede-olive",
              "Olive unstructured cap with a chocolate suede bill, a small leather official mark®, and a side Copper Mountain Air wordmark",
              "Gorra olivo desestructurada con visera de ante chocolate, un pequeño emblema oficial de cuero® y Copper Mountain Air en el costado"),
            c("navy", "hat-suede-navy",
              "Navy unstructured cap with a chocolate suede bill, a small leather official mark®, and a side Copper Mountain Air wordmark",
              "Gorra navy desestructurada con visera de ante chocolate, un pequeño emblema oficial de cuero® y Copper Mountain Air en el costado"),
            c("black", "hat-suede-black",
              "Black unstructured cap with a dark suede bill, a small leather official mark®, and a side Copper Mountain Air wordmark",
              "Gorra negra desestructurada con visera de ante oscura, un pequeño emblema oficial de cuero® y Copper Mountain Air en el costado"),
         ]},
     )},

    {"id": "saguaro-sticker", "picker": "simple", "kind": "sticker",
     "eyebrow": "Sticker · Die-cut", "eyebrow_es": "Calcomanía · Troquelada",
     "name": "Saguaro Patch Sticker", "name_es": "Calcomanía del parche de saguaro",
     "desc": "The same saguaro patch as a kiss-cut vinyl sticker — built to live on a toolbox, a flight bag, or a water bottle.",
     "desc_es": "El mismo parche de saguaro en una calcomanía de vinilo: pensada para una caja de herramientas, una bolsa de vuelo o una botella.",
     "image": "v2-saguaro-sticker-toolbox",
     "alt": "Die-cut saguaro and KOLS sticker applied to the lid of a red workshop toolbox",
     "alt_es": "Calcomanía troquelada de saguaro y KOLS pegada en la tapa de una caja de herramientas roja"},
    {"id": "saguaro-koozie", "picker": "simple", "kind": "koozie",
     "eyebrow": "Koozie · Navy", "eyebrow_es": "Enfriador · Navy",
     "name": "Saguaro Patch Koozie", "name_es": "Enfriador del parche de saguaro",
     "desc": "The saguaro patch wrapped on a navy can cooler. A small, useful piece of the field to throw in a bag.",
     "desc_es": "El parche de saguaro en un enfriador de lata navy. Una pieza pequeña y útil del campo para llevar en la bolsa.",
     "image": "v2-saguaro-koozie-tailgate",
     "alt": "Navy can koozie on a pickup tailgate at golden hour, printed with the circular saguaro and KOLS patch",
     "alt_es": "Enfriador de lata navy sobre la puerta de una pickup al atardecer, con el parche circular de saguaro y KOLS"},
]


def product_default(item):
    """Return (style_id, color_dict) for the card's initial mockup and price."""
    if item.get("picker") != "apparel":
        return item.get("kind"), {
            "id": item.get("default_color") or item.get("kind"),
            "image": item["image"],
            "alt": item["alt"],
            "alt_es": item["alt_es"],
        }
    style = item.get("default_style") or next(iter(item["styles"]))
    colors = item["styles"][style]["colors"]
    want = item.get("default_color")
    color = next((c for c in colors if c["id"] == want), colors[0])
    return style, color


def product_eyebrow(item, style_id, color_id, es=False):
    if item.get("picker") != "apparel":
        return item["eyebrow_es"] if es else item["eyebrow"]
    style = STYLE_LABELS[style_id][1 if es else 0]
    color = COLOR_LABELS.get(color_id, (color_id, color_id))[1 if es else 0]
    note = item.get("note_es" if es else "note")
    parts = [style, color] + ([note] if note else [])
    return " · ".join(parts)


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

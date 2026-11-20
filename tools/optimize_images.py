"""Make web images from Seth's originals (kept OUTSIDE the repo).
Usage: python3 tools/optimize_images.py /workspace/cma-website/photos
Writes assets/img/photos/<slot>-<width>.{avif,webp,jpg}: cropped, resized, sRGB, no EXIF/GPS/ICC metadata.
Never reads staff/ or _not-for-web/."""
import os, sys, json
from PIL import Image, ImageOps
SRC = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "photos")
# slot: (source, aspect w/h, focal (x,y) 0-1, widths)
SLOTS = {
 # No readable registration may appear in any published image (the photographed aircraft is not CMA's):
 # DSC09602 and DSC09575 show the tail number and are NOT used. DSC09616 is head-on, so no registration shows.
 "hero":      ("aircraft/Cessna414A_DSC09616.jpg", 16/9, (.5,.62), [640,960,1280,1920,2560]),
 "ramp-band": ("aircraft/Hangar_with_the_Hangar_Queen.jpg", 21/9, (.5,.56), [640,960,1280,1920]),
 "airfield":  ("kols/KOLS_2026-10-21_00.jpeg", 4/3, (.5,.5), [480,800,1200,1600]),
 "taxiway-signs": ("kols/KOLS_2026-10-21_02.jpeg", 4/3, (.5,.5), [480,800,1200,1600]),
 "fbo":       ("aircraft/Hangar_with_the_Hangar_Queen.jpg", 4/3, (.5,.5), [480,800,1200,1600]),
 "cargo":     ("kols/KOLS_2026-10-21_06.jpeg", 4/3, (.5,.5), [480,800,1200,1600]),
 "cargo-sign":("kols/KOLS_2026-10-21_01.jpeg", 4/3, (.5,.5), [480,800,1200,1600]),
 "kols-guide":("kols/KOLS_2026-10-21_03.jpeg", 1200/630, (.5,.5), [480,800,1200,1600]),
 "training":  ("kols/KOLS_2026-10-21_05.jpeg", 4/3, (.5,.5), [480,800,1200,1600]),
 "charter":   ("lighting/KOLS_lighting_fullsizerender.jpg", 4/3, (.5,.47), [480,800,1200,1600]),
 # Public domain: U.S. Army Air Service photo, 1920, "12th Aero Squadron at Camp Little near Nogales, Arizona"
 # (Wikimedia Commons File:12th_Aero_Squadron_-_Nogales_Arizona.jpg). Camp Little, NOT the present airport site.
 "aero-1920": ("history/12th_Aero_Squadron_-_Nogales_Arizona.jpg", 1500/886, (.5,.5), [480,800,1200,1500]),
 # Night lighting (phone photos; crop toward the lights / signs, not the empty sky).
 "fbo-night":  ("lighting/IMG_2122.jpg", 4/3, (.5,.82), [480,800,1200,1600]),
 "term-night": ("lighting/IMG_2126.jpg", 4/3, (.5,.82), [480,800,1200,1600]),
 # Wings & Wheels, Nov 8, 2026 (held off the home page in Nov 19; now used on /gallery.html).
 "ww-airplane":("wings-and-wheels/airplane-winner-HD.jpeg", 3/4, (.5,.5), [400,800,1200]),
 "ww-car":     ("wings-and-wheels/car-winner-HD.jpeg", 3/4, (.5,.5), [400,800,1200]),
 "ww-motorcycle":("wings-and-wheels/motorcycle-winner-HD.jpeg", 3/4, (.5,.5), [400,800,1200]),
}
# Regions blurred in the ORIGINAL before cropping: (x0, y0, x1, y1, radius).
# Hangar photo: partial registration on the high-wing aircraft parked behind the twin.
REDACT = {"aircraft/Hangar_with_the_Hangar_Queen.jpg": [(440, 735, 530, 795, 9)]}
def redact(im, src):
    from PIL import ImageFilter, ImageDraw
    for x0, y0, x1, y1, r in REDACT.get(src, []):
        blurred = im.filter(ImageFilter.GaussianBlur(r))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((x0, y0, x1, y1), radius=12, fill=255)
        im = Image.composite(blurred, im, mask.filter(ImageFilter.GaussianBlur(6)))  # feathered edge
    return im

def crop(im, aspect, focal):
    w, h = im.size
    if w / h > aspect: nw, nh = int(h * aspect), h
    else: nw, nh = w, int(w / aspect)
    fx, fy = focal
    x = min(max(int(fx * w - nw / 2), 0), w - nw); y = min(max(int(fy * h - nh / 2), 0), h - nh)
    return im.crop((x, y, x + nw, y + nh))
os.makedirs(OUT, exist_ok=True)
manifest = {}
for slot, (src, aspect, focal, widths) in SLOTS.items():
    assert "staff/" not in src and "_not-for-web" not in src
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src)))
    if "icc_profile" in im.info:
        from PIL import ImageCms; import io
        im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(im.info["icc_profile"])), ImageCms.createProfile("sRGB"), outputMode="RGB")
    im = crop(redact(im.convert("RGB"), src), aspect, focal); im.info = {}
    ws = [w for w in widths if w <= im.width] or [im.width]
    for w in ws:
        r = im.resize((w, round(w / aspect)), Image.LANCZOS); r.info = {}
        base = os.path.join(OUT, f"{slot}-{w}")
        r.save(base + ".jpg", "JPEG", quality=78, optimize=True, progressive=True)   # no exif/icc passed => stripped
        r.save(base + ".webp", "WEBP", quality=72, method=6)
        r.save(base + ".avif", "AVIF", quality=50, speed=6)
    manifest[slot] = {"widths": ws, "w": ws[-1], "h": round(ws[-1] / aspect)}
    print(slot, ws)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)


# Gallery exports keep a more natural aspect for the lightbox (metadata stripped).
# Lighting portraits are cropped 3:4 toward the signs so the empty night sky does not dominate.
GALLERY_OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "gallery")
# id: (source, alt, caption, group, aspect or None, focal)
GALLERY = {
 "ww-airplane": ("wings-and-wheels/airplane-winner-HD.jpeg",
    "Best Plane award presented in the terminal at Copper Mountain Air's first Wings & Wheels at Nogales International Airport",
    "Best Plane award, Copper Mountain Air's first Wings & Wheels at KOLS, November 8, 2026.",
    "Wings & Wheels", None, (.5,.5)),
 "ww-car": ("wings-and-wheels/car-winner-HD.jpeg",
    "Best Car award winner standing with an orange classic Chevrolet Camaro on the ramp at Nogales International Airport, mountains behind",
    "Best Car award, Wings & Wheels at KOLS, November 8, 2026.",
    "Wings & Wheels", None, (.5,.5)),
 "ww-motorcycle": ("wings-and-wheels/motorcycle-winner-HD.jpeg",
    "Best Motorcycle award winner standing with a black motorcycle on the ramp at Nogales International Airport, mountains behind",
    "Best Motorcycle award, Wings & Wheels at KOLS, November 8, 2026.",
    "Wings & Wheels", None, (.5,.5)),
 "airfield": ("kols/KOLS_2026-10-21_00.jpeg",
    "Taxiway A and D sign beside the runway at Nogales International Airport, with mountains in the distance",
    "Taxiway A and D sign looking toward the runway and the Santa Cruz Valley mountains.",
    "At the field", None, (.5,.5)),
 "taxiway-signs": ("kols/KOLS_2026-10-21_02.jpeg",
    "Yellow taxiway D and A direction signs at Nogales International Airport",
    "Taxiway D and A direction signs on the field at KOLS.",
    "At the field", None, (.5,.5)),
 "runway-22": ("kols/KOLS_2026-10-21_03.jpeg",
    "Red runway 22-4 location sign at Nogales International Airport",
    "Runway 22-4 location sign at Nogales International Airport.",
    "At the field", None, (.5,.5)),
 "taxiway-ad": ("kols/KOLS_2026-10-21_05.jpeg",
    "Yellow taxiway A and D signs beside the runway at Nogales International Airport, with mountains behind",
    "Taxiway A and D signs along the runway at KOLS.",
    "At the field", None, (.5,.5)),
 "cargo-field": ("kols/KOLS_2026-10-21_06.jpeg",
    "Yellow CARGO direction sign beside the airfield at Nogales International Airport, with hangars and mountains in the distance",
    "Cargo direction sign beside the airfield, looking toward the hangars at KOLS.",
    "At the field", None, (.5,.5)),
 "runway-dusk": ("lighting/KOLS_lighting_fullsizerender.jpg",
    "Runway at Nogales International Airport at dusk, with edge lights and a windsock",
    "Runway 4/22 at dusk, with edge lights and the windsock.",
    "At the field", 3/4, (.5,.72)),
 "fbo-night": ("lighting/IMG_2122.jpg",
    "Illuminated FBO taxiway sign and taxiway lights at Nogales International Airport at night",
    "FBO taxiway sign and taxiway lights at night.",
    "At the field", 3/4, (.5,.82)),
 "term-night": ("lighting/IMG_2126.jpg",
    "Illuminated terminal taxiway sign and airfield lights at Nogales International Airport at night",
    "Terminal taxiway sign and airfield lights at night.",
    "At the field", 3/4, (.5,.82)),
}
GALLERY_WIDTHS = [400, 800, 1600]
os.makedirs(GALLERY_OUT, exist_ok=True)
gallery_manifest = {"items": []}
for gid, (src, alt, caption, group, aspect, focal) in GALLERY.items():
    assert "staff/" not in src and "_not-for-web" not in src
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src)))
    if "icc_profile" in im.info:
        from PIL import ImageCms; import io
        im = ImageCms.profileToProfile(im, ImageCms.ImageCmsProfile(io.BytesIO(im.info["icc_profile"])), ImageCms.createProfile("sRGB"), outputMode="RGB")
    im = redact(im.convert("RGB"), src); im.info = {}
    if aspect:
        im = crop(im, aspect, focal)
    # Long-edge cap; never upscale.
    longest = max(im.size)
    ws = [w for w in GALLERY_WIDTHS if w <= longest] or [longest]
    # Record native aspect height at the largest width.
    lw = ws[-1]
    if im.width >= im.height:
        lh = round(im.height * lw / im.width)
    else:
        lh = lw
        lw = round(im.width * lh / im.height)
        # widths are long-edge; for portraits the named width is the height
        lw, lh = ws[-1], round(im.height * ws[-1] / max(im.size) * im.width / im.width)
        # simpler: scale by long edge
        scale = ws[-1] / max(im.size)
        lw, lh = round(im.width * scale), round(im.height * scale)
    for w in ws:
        scale = w / max(im.size)
        r = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        r.info = {}
        base = os.path.join(GALLERY_OUT, f"{gid}-{w}")
        r.save(base + ".jpg", "JPEG", quality=78, optimize=True, progressive=True)
        r.save(base + ".webp", "WEBP", quality=72, method=6)
        r.save(base + ".avif", "AVIF", quality=50, speed=6)
    gallery_manifest["items"].append({
        "id": gid, "group": group, "alt": alt, "caption": caption,
        "widths": ws, "w": lw, "h": lh,
    })
    print("gallery", gid, ws, f"{lw}x{lh}")
json.dump(gallery_manifest, open(os.path.join(GALLERY_OUT, "manifest.json"), "w"), indent=1)

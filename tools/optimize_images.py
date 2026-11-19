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
 "event":     ("wings-and-wheels/car-winner-HD.jpeg", 1200/630, (.5,.5), [480,800,1200,1600]),
 "community": ("wings-and-wheels/car-winner-HD.jpeg", 4/3, (.5,.55), [480,800,1200,1600]),
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

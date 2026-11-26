"""Optimize CMA merch mockups for the Store page.
Source PNGs stay outside the repo (store-preview/products/).
Writes assets/img/store/<id>-<width>.{webp,jpg} and optional avif, metadata stripped.
Each output file is kept under 300 KB.
"""
import os, json
from PIL import Image, ImageOps

SRC = os.environ.get("CMA_STORE_SRC", "/workspace/cma-merch/store-preview/products")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img", "store")
if len(__import__("sys").argv) > 1:
    SRC = __import__("sys").argv[1]
WIDTHS = [640, 1024]
MAX_BYTES = 300 * 1024

os.makedirs(OUT, exist_ok=True)
manifest = {"items": []}

def save_under(im, path, fmt, start_q, min_q):
    q = start_q
    while q >= min_q:
        im.info = {}
        if fmt == "JPEG":
            im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
        elif fmt == "WEBP":
            im.save(path, "WEBP", quality=q, method=6)
        elif fmt == "AVIF":
            im.save(path, "AVIF", quality=q, speed=6)
        if os.path.getsize(path) <= MAX_BYTES:
            return q, os.path.getsize(path)
        q -= 4
    return q, os.path.getsize(path)

for fn in sorted(os.listdir(SRC)):
    if not fn.lower().endswith(".png"):
        continue
    slug = os.path.splitext(fn)[0]
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, fn)))
    if "icc_profile" in im.info:
        from PIL import ImageCms
        import io
        im = ImageCms.profileToProfile(
            im,
            ImageCms.ImageCmsProfile(io.BytesIO(im.info["icc_profile"])),
            ImageCms.createProfile("sRGB"),
            outputMode="RGB",
        )
    im = im.convert("RGB")
    im.info = {}
    rec = {"id": slug, "widths": [], "w": im.width, "h": im.height, "files": {}}
    for w in WIDTHS:
        if w > im.width:
            continue
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.info = {}
        base = os.path.join(OUT, f"{slug}-{w}")
        rec["widths"].append(w)
        rec["files"][str(w)] = {}
        q, sz = save_under(r, base + ".jpg", "JPEG", 78, 50)
        rec["files"][str(w)]["jpg"] = {"q": q, "bytes": sz}
        q, sz = save_under(r, base + ".webp", "WEBP", 72, 45)
        rec["files"][str(w)]["webp"] = {"q": q, "bytes": sz}
        try:
            q, sz = save_under(r, base + ".avif", "AVIF", 50, 30)
            rec["files"][str(w)]["avif"] = {"q": q, "bytes": sz}
        except Exception as e:
            rec["files"][str(w)]["avif_error"] = str(e)
        sizes = " ".join(
            f"{ext}:{rec['files'][str(w)][ext]['bytes']}"
            for ext in rec["files"][str(w)]
            if isinstance(rec["files"][str(w)][ext], dict)
        )
        print(f"{slug}-{w} {sizes}")
    if rec["widths"]:
        rec["w"] = rec["widths"][-1]
        rec["h"] = round(im.height * rec["w"] / im.width)
    manifest["items"].append(rec)

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
over = []
for root, _, files in os.walk(OUT):
    for f in files:
        if f.endswith((".jpg", ".webp", ".avif")):
            p = os.path.join(root, f)
            sz = os.path.getsize(p)
            if sz > MAX_BYTES:
                over.append((p, sz))
print("items", len(manifest["items"]))
if over:
    print("OVER LIMIT:")
    for p, sz in over:
        print(sz, p)
    raise SystemExit(1)
print("all under 300 KB")

"""Build clean logo SVGs from Seth's Inkscape master (outside the repo).
Usage: python3 tools/make_logo.py tools/logo_parts.json
logo_parts.json holds the outerHTML of the mark group (g7208-2) and wordmark group (text2399-9),
extracted from photos/logos/Copper_Mountain_Air_Logo.svg (the only artwork inside its 1219.2 viewBox)."""
import re, json, sys, os
parts = json.load(open(sys.argv[1]))
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")
def clean(g):
    tr = re.search(r'<g[^>]*?transform="([^"]+)"', g.split(">")[0] + ">")
    ds = re.findall(r'\sd="([^"]+)"', g)
    ds = [re.sub(r"-?\d+\.\d+", lambda m: ("%.2f" % float(m.group())).rstrip("0").rstrip("."), d) for d in ds]
    body = "".join(f'<path d="{d}"/>' for d in ds)
    return f'<g transform="{tr.group(1)}">{body}</g>' if tr else f"<g>{body}</g>"
MARK, WORD = clean(parts["mark"]), clean(parts["word"])
# content boxes (root user units) measured in Chromium: mark 214,172-1025,788 ; word 192,858-1049,912
def svg(vb, inner, fill, label="Copper Mountain Air"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{label}"><title>{label}</title><g fill="{fill}">{inner}</g></svg>\n'
INK, SAND = "#0d1b24", "#f4e7d6"
stacked_vb = "172 152 897 780"
mark_vb = "194 152 851 656"
# Horizontal lockup: mark (616 tall) + wordmark scaled 4.4x (≈238 tall), vertically centred.
s = 4.4; mx0, my0, mh = 214, 172, 616; wx0, wy0, wh = 192, 858, 54
gap = 120; wx = 1025 + gap; wy = my0 + (mh - wh * s) / 2
lock_inner = MARK + f'<g transform="translate({wx - wx0*s:.1f} {wy - wy0*s:.1f}) scale({s})">{WORD}</g>'
lock_w = (wx + 857 * s) - mx0
lock_vb = f"{mx0-10} {my0-10} {lock_w+20:.0f} {mh+20}"
files = {
 "logo-stacked-dark.svg": svg(stacked_vb, MARK + WORD, INK), "logo-stacked-light.svg": svg(stacked_vb, MARK + WORD, SAND),
 "logo-dark.svg": svg(lock_vb, lock_inner, INK), "logo-light.svg": svg(lock_vb, lock_inner, SAND),
 "logo-mark-dark.svg": svg(mark_vb, MARK, INK), "logo-mark-light.svg": svg(mark_vb, MARK, SAND),
 "favicon.svg": f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="{INK}"/>'
                f'<svg x="5" y="7" width="54" height="50" viewBox="{mark_vb}"><g fill="{SAND}">{MARK}</g></svg></svg>\n',
}
for n, c in files.items():
    open(os.path.join(OUT, n), "w").write(c); print(n, len(c))
print("lockup aspect", round(lock_w / mh, 3))

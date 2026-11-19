"""Generate placeholder SVG art for each image slot in assets/img/.
Each placeholder is labeled with the real-photo file name that should replace it."""
import os
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

def label(text, cx, y=96, fs=40):
    x = cx - (len(text)*fs*0.6)/2
    return (f'<g font-family="Inter,Arial,sans-serif" font-size="{fs}" font-weight="700">'
            f'<rect x="{x-24}" y="{y-fs*1.25}" width="{len(text)*fs*0.6+48}" height="{fs*1.8}" rx="{fs*.9}" fill="#0d1b24" fill-opacity=".62" stroke="#f4e7d6" stroke-opacity=".5" stroke-dasharray="8 8" stroke-width="2"/>'
            f'<text x="{x}" y="{y}" fill="#f4e7d6">{text}</text></g>')

def scene(w, h, sky, sun, ridges, extra="", tag=None):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" role="img">',
         '<defs>',
         f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">' + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in sky) + '</linearGradient>',
         '<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd9a8"/><stop offset=".55" stop-color="#f0a15e" stop-opacity=".85"/><stop offset="1" stop-color="#f0a15e" stop-opacity="0"/></radialGradient>',
         '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .07 0"/></filter>',
         '</defs>',
         f'<rect width="{w}" height="{h}" fill="url(#sky)"/>']
    if sun:
        cx, cy, r = sun
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sun)"/>')
    for d, c in ridges:
        s.append(f'<path d="{d}" fill="{c}"/>')
    s.append(extra)
    s.append(f'<rect width="{w}" height="{h}" filter="url(#grain)"/>')
    if tag:
        s.append(label(tag, w/2))
    s.append('</svg>')
    return "\n".join(s)

def ridge(w, h, base, amp, seed, steps=14):
    import math
    pts = []
    for i in range(steps + 1):
        x = w * i / steps
        y = base - amp * (0.55 + 0.45 * math.sin(i * 1.7 + seed) * math.cos(i * 0.6 + seed * 2))
        pts.append(f"{x:.0f},{y:.0f}")
    return f"M0,{h} L" + " L".join(pts) + f" L{w},{h} Z"

PLANE = '<path d="M0 0 L60 -4 L74 -18 L82 -18 L78 -4 L110 -3 Q122 0 110 3 L78 4 L82 18 L74 18 L60 4 L0 0 Z M6 -1 L-8 -12 L-2 -12 L14 -2 Z M6 1 L-8 12 L-2 12 L14 2 Z" fill="#0d1b24"/>'

def plane(x, y, s, rot=-8, op=.9):
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})" opacity="{op}">{PLANE}</g>'

DUSK = [(0, "#132634"), (.45, "#5b3a3a"), (.72, "#c26a3c"), (1, "#f0b27a")]
NOON = [(0, "#2a5470"), (.6, "#8fb3c4"), (1, "#efdcc2")]
NIGHT = [(0, "#0b1620"), (.6, "#1d3242"), (1, "#7a4a33")]

def runway(w, h):
    # perspective runway converging to horizon
    hx, hy = w * .5, h * .7
    return (f'<path d="M{hx-14},{hy} L{hx+14},{hy} L{w*.78},{h} L{w*.22},{h} Z" fill="#1b2a33"/>'
            + "".join(f'<path d="M{hx-1.5 + (i*0)},{hy + (h-hy)*t0} L{hx+1.5},{hy + (h-hy)*t0} L{hx+1.5+ t1*6},{hy+(h-hy)*t1} L{hx-1.5-t1*6},{hy+(h-hy)*t1} Z" fill="#f4e7d6" opacity=".75"/>'
                      for i, (t0, t1) in enumerate([(.08, .14), (.22, .32), (.42, .56), (.7, .9)])))

slots = {
 "hero": (1920, 1080, DUSK, (1340, 640, 420), [(ridge(1920,1080,760,190,1),"#7a4630"),(ridge(1920,1080,840,150,4),"#4b2d27"),(ridge(1920,1080,930,120,7),"#24201f")],
          '<path d="M-40 380 C 400 300, 900 260, 1500 150" stroke="#ffe6c7" stroke-opacity=".35" stroke-width="3" fill="none" stroke-dasharray="2 10"/>' , None),
 "fbo": (1200, 800, NOON, (900, 260, 200), [(ridge(1200,800,560,120,2),"#b98a68"),(ridge(1200,800,640,90,5),"#8a5f45")], None, "PHOTO PLACEHOLDER · fbo.jpg"),
 "fuel": (1200, 800, DUSK, (300, 520, 260), [(ridge(1200,800,600,110,3),"#6b3d2c"),(ridge(1200,800,680,80,6),"#2a2220")], None, "PHOTO PLACEHOLDER · fuel.jpg"),
 "cargo": (1200, 800, NIGHT, (980, 560, 200), [(ridge(1200,800,600,100,8),"#3b2a26"),(ridge(1200,800,690,70,2),"#1a1715")], None, "PHOTO PLACEHOLDER · cargo.jpg"),
 "training": (1200, 800, NOON, (240, 200, 160), [(ridge(1200,800,620,140,9),"#a7764f"),(ridge(1200,800,700,80,1),"#6f4a35")], None, "PHOTO PLACEHOLDER · training.jpg"),
 "charter": (1200, 800, DUSK, (960, 420, 240), [(ridge(1200,800,620,140,11),"#5a3428"),(ridge(1200,800,700,90,3),"#211c1b")], None, "PHOTO PLACEHOLDER · charter.jpg"),
 "about": (1200, 800, NOON, (600, 300, 220), [(ridge(1200,800,560,160,13),"#c09070"),(ridge(1200,800,650,110,5),"#8b5a3f"),(ridge(1200,800,740,60,2),"#4a3128")], None, "PHOTO PLACEHOLDER · about.jpg"),
 "kols-guide": (1200, 630, NOON, (920, 200, 170), [(ridge(1200,630,450,90,4),"#b07d5a"),(ridge(1200,630,500,60,9),"#7d5440")], "RUNWAY", "PHOTO PLACEHOLDER · kols-guide.jpg"),
}
os.makedirs(OUT, exist_ok=True)
KEEP = {"fuel"}  # only slots that still have no real photo
for name, (w, h, sky, sun, ridges, extra, tag) in slots.items():
    if name not in KEEP: continue
    if extra == "RUNWAY":
        extra = runway(w, h)
    elif extra is None:
        extra = ""
    if name == "hero":
        extra += plane(1180, 300, 2.2, -9, .92)
    elif name in ("cargo", "charter", "training", "fbo"):
        extra += plane(w * .32, h * .3, 1.3, -10, .85)
    open(os.path.join(OUT, f"{name}.svg"), "w").write(scene(w, h, sky, sun, ridges, extra, tag))
print("wrote", len(slots), "placeholders")

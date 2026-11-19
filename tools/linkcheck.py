import re, sys, urllib.request, urllib.parse
base = sys.argv[1]
seen, todo, bad, ext = set(), [base], [], set()
def get(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent":"linkcheck"}), timeout=20)
    return r.status, r.read().decode("utf-8","ignore"), r.headers.get("content-type","")
while todo:
    u = todo.pop()
    if u in seen: continue
    seen.add(u)
    try: st, body, ct = get(u)
    except Exception as e: bad.append((u, str(e))); continue
    print(st, u)
    if "html" not in ct: continue
    for m in re.findall(r'(?:href|src)="([^"]+)"', body):
        if m.startswith(("mailto:","#","data:","tel:")): continue
        full = urllib.parse.urljoin(u, m).split("#")[0].split("?")[0]
        if full.startswith(base): todo.append(full)
        elif full.startswith("http"): ext.add(full)
for e in sorted(ext):
    try: st = urllib.request.urlopen(urllib.request.Request(e, headers={"User-Agent":"Mozilla/5.0"}), timeout=20).status; print(st, "EXT", e)
    except Exception as x: print("EXT-ERR", e, x)
print("BROKEN:", bad or "none", "| internal URLs checked:", len(seen))

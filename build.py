#!/usr/bin/env python3
"""megkerulhetetlen.hu aloldalak: content/*.json + templates/ -> docs/<slug>/index.html, QR-kódok docs/qr/."""
import json, glob, os, datetime, shutil, sys
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import segno

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = {"base_url": "https://megkerulhetetlen.hu", "year": datetime.date.today().year,
        "build": datetime.datetime.now().strftime("%Y%m%d%H%M")}
env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")), autoescape=True, undefined=StrictUndefined)
# soft-undefined for optional keys: wrap page dict so missing keys -> None
class Page(dict):
    def __getattr__(self, k): return self.get(k)

# 2026-10-08: a QR-kódok kimentek a kiadónak → ezek a slugok VÉGLEGESEK, a build megáll, ha bármelyik hiányzik
LOCKED_SLUGS = ["karizma","gundel-takacs-gabor","storycanvas","idokapszula","kocsis-attila","godor-zola","tusnadi-roland","bese-nora","bolya-imre","stressz-teszt","szauer-tamas","luminance","kamera-elotti-magabiztossag","hormonmentes","werk","podcast-booster","branding-roadmap"]
_present = {json.load(open(f, encoding="utf-8"))["slug"] for f in glob.glob(os.path.join(ROOT, "content", "*.json")) if not os.path.basename(f).startswith("_")}
_missing = [s for s in LOCKED_SLUGS if s not in _present]
if _missing:
    sys.exit(f"HIBA: nyomtatott QR-hoz tartozó slug hiányzik a content/ mappából: {_missing}. A slugokat NEM szabad módosítani (a QR-kódok a kiadónál vannak).")
if "--cname" not in sys.argv:
    print("FIGYELEM: --cname nélkül építesz; élesítés előtt `python3 build.py --cname` kell.")
pages = []
for f in sorted(glob.glob(os.path.join(ROOT, "content", "*.json"))):
    if os.path.basename(f).startswith("_"): continue
    p = Page(json.load(open(f, encoding="utf-8")))
    assert p["slug"] and p["template"] and p["title"], f
    out_dir = os.path.join(ROOT, "docs", p["slug"]); os.makedirs(out_dir, exist_ok=True)
    html = env.get_template(p["template"] + ".html").render(page=p, site=SITE, rel="../")
    html = html.replace('"/assets/', '"../assets/')  # tartalomfájlokban abszolút kép-útvonalak
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(html)
    # redirect aliases (old Notion slugs etc.)
    for alias in p.get("aliases", []):
        ad = os.path.join(ROOT, "docs", alias); os.makedirs(ad, exist_ok=True)
        open(os.path.join(ad, "index.html"), "w", encoding="utf-8").write(
            f'<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../{p["slug"]}/"><link rel="canonical" href="{SITE["base_url"]}/{p["slug"]}/"><title>Átirányítás</title><a href="../{p["slug"]}/">Tovább</a>')
    # QR
    qd = os.path.join(ROOT, "docs", "qr"); os.makedirs(qd, exist_ok=True)
    url = f'{SITE["base_url"]}/{p["slug"]}/'
    q = segno.make(url, error="q")
    q.save(os.path.join(qd, f'{p["slug"]}.svg'), scale=10, border=2, dark="#14181c")
    q.save(os.path.join(qd, f'{p["slug"]}.png'), scale=20, border=2, dark="#14181c")
    pages.append(p)
    print(f'  /{p["slug"]}/  <- {os.path.basename(f)}  [{p["template"]}]')

# próba-változatok: content/_variants.json → docs/<slug>/<variant>/index.html
vf=os.path.join(ROOT,"content","_variants.json")
if os.path.exists(vf):
    for v in json.load(open(vf,encoding="utf-8")):
        base=json.load(open(os.path.join(ROOT,"content",v["slug"]+".json"),encoding="utf-8")); base.update(v["overrides"]); pv=Page(base)
        html=env.get_template(pv["template"]+".html").render(page=pv, site=SITE, rel="../../").replace('"/assets/','"../../assets/').replace("<head>","<head><meta name=\"robots\" content=\"noindex\">")
        od=os.path.join(ROOT,"docs",v["slug"],v["name"]); os.makedirs(od,exist_ok=True); open(os.path.join(od,"index.html"),"w",encoding="utf-8").write(html)
        print(f'  /{v["slug"]}/{v["name"]}/  (próba-változat)')
# ideiglenes gyökér: a sales-landing jön ide később; addig egy sima lista
by_ch = {}
for p in pages: by_ch.setdefault(p.get("fejezet") or "Egyéb", []).append(p)
items = "".join(f'<h2>{ch}</h2><ul>' + "".join(f'<li><a href="{p["slug"]}/">{p["title"]}</a> <small>({p["template"]})</small></li>' for p in ps) + "</ul>" for ch, ps in by_ch.items())
open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8").write(f'''<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Megkerülhetetlen · aloldalak</title><meta name="robots" content="noindex"><link rel="stylesheet" href="assets/css/style.css"></head><body><main class="wrap" style="padding:40px 0"><p class="eyebrow">Ideiglenes nyitóoldal</p><h1>Megkerülhetetlen · a könyv aloldalai</h1><p class="muted">A gyökérre a könyv sales-landingje kerül. Ez a lista csak a munkához.</p>{items}<p><a href="qr/">QR-kódok</a></p></main></body></html>''')
# Nyomdai összesítő: QR-kódok + az összes éles aloldal, a könyv sorrendjében
ORDER = ["karizma","gundel-takacs-gabor","storycanvas","idokapszula","kocsis-attila","godor-zola","tusnadi-roland","bese-nora","bolya-imre","stressz-teszt","szauer-tamas","luminance","kamera-elotti-magabiztossag","hormonmentes","werk","podcast-booster","branding-roadmap"]
bys = {p["slug"]: p for p in pages}
ordered = [bys[s] for s in ORDER if s in bys] + [p for p in pages if p["slug"] not in ORDER]
import zipfile
zp = os.path.join(ROOT, "docs", "qr", "megkerulhetetlen-qr-kodok.zip")
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for p in ordered:
        for ext in ("svg", "png"): z.write(os.path.join(ROOT, "docs", "qr", f'{p["slug"]}.{ext}'), f'{p["slug"]}.{ext}')
TEMPLATE_HU = {"series": "Podcast-epizód", "story": "Nova storytelling", "lead": "Letölthető anyag / űrlap"}
cards = ""
for i, p in enumerate(ordered, 1):
    url = f'{SITE["base_url"]}/{p["slug"]}/'
    cards += f'''<div class="qr-card"><img src="../qr/{p["slug"]}.svg" alt="QR: {url}" width="220" height="220"><div class="qr-meta"><div class="qr-n">{i:02d}</div><div class="qr-ch">{p.get("fejezet") or "Fejezeten kívül"} · {TEMPLATE_HU.get(p["template"], p["template"])}</div><h3>{p["title"]}</h3><a class="qr-url" href="{url}">{url.replace("https://","")}</a><div class="qr-dl"><a href="../qr/{p["slug"]}.svg" download>SVG</a> · <a href="../qr/{p["slug"]}.png" download>PNG</a></div></div></div>'''
rows = "".join(f'<tr><td>{i:02d}</td><td>{p.get("fejezet") or "–"}</td><td><a href="{SITE["base_url"]}/{p["slug"]}/">{p["title"]}</a></td><td class="mono"><a href="{SITE["base_url"]}/{p["slug"]}/">megkerulhetetlen.hu/{p["slug"]}/</a></td></tr>' for i, p in enumerate(ordered, 1))
nyomda = f'''<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Megkerülhetetlen · QR-kódok és aloldalak a nyomdának</title><meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Unbounded:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/css/style.css?v={SITE["build"]}">
<style>
.qr-grid{{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}}
.qr-card{{display:flex;gap:16px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px;break-inside:avoid}}
.qr-card img{{width:150px;height:150px;flex:none;background:#fff;border-radius:8px}}
.qr-n{{font-family:var(--font-h);color:var(--teal);font-weight:700;font-size:13px}}
.qr-ch{{font-size:12px;color:var(--muted);margin:2px 0 6px}}
.qr-card h3{{font-size:14px;line-height:1.3;margin:0 0 6px;font-family:var(--font-b);font-weight:600}}
.qr-url{{font-size:13px;word-break:break-all;display:block}}
.qr-dl{{font-size:12px;color:var(--muted);margin-top:6px}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
td,th{{padding:9px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.mono{{font-size:13px}}
@media print{{.no-print,.qr-dl{{display:none}} body{{background:#fff}} .qr-card{{box-shadow:none}} a{{color:#000;text-decoration:none}}}}
</style></head><body>
<main class="wrap" style="padding:40px 0 60px">
<p class="author">Kaltenecker Kristóf</p>
<div class="wordmark" style="font-size:clamp(28px,5vw,44px)">Megkerül-<br>hetetlen</div>
<h1 style="margin-top:14px">QR-kódok és aloldalak a könyvhöz</h1>
<p class="muted">Összesen {len(ordered)} aloldal, a könyvben való megjelenés sorrendjében. Minden QR a megadott https-címre mutat, és a nyomtatáshoz SVG-ben (vektoros) és PNG-ben is letölthető. <a class="no-print" href="../qr/megkerulhetetlen-qr-kodok.zip" download><b>Összes QR egy ZIP-ben</b></a></p>
<h2 style="margin-top:28px">QR-kódok</h2>
<div class="qr-grid">{cards}</div>
<h2 style="margin-top:44px">Az élő aloldalak listája</h2>
<table><thead><tr><th>#</th><th>Fejezet</th><th>Oldal</th><th>Cím</th></tr></thead><tbody>{rows}</tbody></table>
<p class="small muted" style="margin-top:30px">Frissítve: {datetime.date.today().isoformat()} · Technikai megjegyzés a nyomdának: a QR-kódok hibajavítási szintje Q (25%), legalább 2 cm-es méretben és fehér háttéren nyomtatva olvashatók megbízhatóan.</p>
</main></body></html>'''
nd = os.path.join(ROOT, "docs", "nyomda"); os.makedirs(nd, exist_ok=True)
open(os.path.join(nd, "index.html"), "w", encoding="utf-8").write(nyomda)
open(os.path.join(ROOT, "docs", "qr", "index.html"), "w", encoding="utf-8").write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=../nyomda/"><title>Átirányítás</title><a href="../nyomda/">Tovább</a>')
cn=os.path.join(ROOT, "docs", "CNAME")
if "--cname" in sys.argv: open(cn, "w").write("megkerulhetetlen.hu\n")
elif os.path.exists(cn): os.remove(cn)
open(os.path.join(ROOT, "docs", ".nojekyll"), "w").write("")
print(f"{len(pages)} oldal kész.")

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

# ideiglenes gyökér: a sales-landing jön ide később; addig egy sima lista
by_ch = {}
for p in pages: by_ch.setdefault(p.get("fejezet") or "Egyéb", []).append(p)
items = "".join(f'<h2>{ch}</h2><ul>' + "".join(f'<li><a href="{p["slug"]}/">{p["title"]}</a> <small>({p["template"]})</small></li>' for p in ps) + "</ul>" for ch, ps in by_ch.items())
open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8").write(f'''<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Megkerülhetetlen · aloldalak</title><meta name="robots" content="noindex"><link rel="stylesheet" href="assets/css/style.css"></head><body><main class="wrap" style="padding:40px 0"><p class="eyebrow">Ideiglenes nyitóoldal</p><h1>Megkerülhetetlen · a könyv aloldalai</h1><p class="muted">A gyökérre a könyv sales-landingje kerül. Ez a lista csak a munkához.</p>{items}<p><a href="qr/">QR-kódok</a></p></main></body></html>''')
# QR index
qi = "".join(f'<div style="text-align:center"><img src="{p["slug"]}.svg" width="160" alt=""><br><small>/{p["slug"]}/</small></div>' for p in pages)
open(os.path.join(ROOT, "docs", "qr", "index.html"), "w", encoding="utf-8").write(f'<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>QR-kódok</title><meta name="robots" content="noindex"><link rel="stylesheet" href="../assets/css/style.css"></head><body><main class="wrap" style="padding:40px 0"><h1>QR-kódok a nyomdának</h1><p class="muted">SVG és PNG: /qr/&lt;slug&gt;.svg és .png</p><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:20px">{qi}</div></main></body></html>')
cn=os.path.join(ROOT, "docs", "CNAME")
if "--cname" in sys.argv: open(cn, "w").write("megkerulhetetlen.hu\n")
elif os.path.exists(cn): os.remove(cn)
open(os.path.join(ROOT, "docs", ".nojekyll"), "w").write("")
print(f"{len(pages)} oldal kész.")

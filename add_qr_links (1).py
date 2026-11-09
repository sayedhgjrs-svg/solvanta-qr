#!/usr/bin/env python3
"""Adds the QR Code Generator link to the footer of every Solvanta page and to sitemap.xml.

Usage:  python3 add_qr_links.py /path/to/site-copy [--dry-run]
Safe to run twice (it skips files that already have the link). Makes a .bak-qr copy of each file it changes.
"""
import os, re, shutil, sys

root = sys.argv[1] if len(sys.argv) > 1 else "."
dry = "--dry-run" in sys.argv
LINK = '<li><a href="/qr-generator/" class="hover:text-gold-400 transition-colors"><i class="fa-solid fa-angle-right text-xs mr-2 text-brand-500"></i>QR Code Generator</a></li>'
SITEMAP_URL = "https://tools.pulsesave.net/qr-generator/"
changed, skipped = [], []

for dp, dn, fn in os.walk(root):
    if os.path.basename(dp) == "qr-generator":
        continue
    if "index.html" not in fn:
        continue
    p = os.path.join(dp, "index.html")
    s = open(p, encoding="utf-8").read()
    if "/qr-generator/" in s:
        skipped.append((p, "already has link")); continue
    m = re.search(r'<li><a href="/image-resizer/"[^\n]*?</li>', s)
    if not m:
        skipped.append((p, "footer item not found")); continue
    new = s[:m.end()] + "\n                        " + LINK + s[m.end():]
    changed.append(p)
    if not dry:
        shutil.copy2(p, p + ".bak-qr")
        open(p, "w", encoding="utf-8").write(new)

sm = os.path.join(root, "sitemap.xml")
if os.path.exists(sm):
    t = open(sm, encoding="utf-8").read()
    if SITEMAP_URL in t:
        skipped.append((sm, "already listed"))
    elif "</urlset>" in t:
        changed.append(sm)
        if not dry:
            shutil.copy2(sm, sm + ".bak-qr")
            open(sm, "w", encoding="utf-8").write(t.replace("</urlset>", f"  <url><loc>{SITEMAP_URL}</loc></url>\n</urlset>"))
    else:
        skipped.append((sm, "no </urlset>"))
else:
    skipped.append((sm, "sitemap.xml not found"))

print(("DRY RUN - " if dry else "") + f"changed: {len(changed)}")
for c in changed: print("  +", c)
for p, why in skipped: print("  skipped:", p, "->", why)

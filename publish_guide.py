#!/usr/bin/env python3
"""Publishes the QR guide page and the updated QR generator page into a COPY of the Solvanta site.

Usage:  python3 publish_guide.py /path/to/site-copy [--dry-run]
The two HTML files (qr-guide.html, qr-generator-v2.html) must be in the same folder as this script.
Safe to run twice. It only writes these three things:
  guides/how-to-make-a-qr-code/index.html   (new page)
  qr-generator/index.html                   (replaced by the v2 page)
  sitemap.xml                               (adds the guide URL if missing)
"""
import os, shutil, sys

here = os.path.dirname(os.path.abspath(__file__))
root = sys.argv[1] if len(sys.argv) > 1 else "."
dry = "--dry-run" in sys.argv
GUIDE_URL = "https://tools.pulsesave.net/guides/how-to-make-a-qr-code/"
jobs = [("qr-guide.html", os.path.join("guides", "how-to-make-a-qr-code", "index.html")),
        ("qr-generator-v2.html", os.path.join("qr-generator", "index.html"))]

for src, dst in jobs:
    s = os.path.join(here, src)
    if not os.path.exists(s):
        sys.exit(f"missing file next to the script: {src}")
    d = os.path.join(root, dst)
    print(("would write " if dry else "writing ") + f"{dst}  ({os.path.getsize(s)} bytes)")
    if not dry:
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copyfile(s, d)

sm = os.path.join(root, "sitemap.xml")
if not os.path.exists(sm):
    print("sitemap.xml not found - skipped")
else:
    t = open(sm, encoding="utf-8").read()
    if GUIDE_URL in t:
        print("sitemap: guide already listed")
    elif "</urlset>" not in t:
        print("sitemap: no </urlset> - skipped")
    else:
        print(("would add " if dry else "adding ") + "guide URL to sitemap.xml")
        if not dry:
            open(sm, "w", encoding="utf-8").write(t.replace("</urlset>", f"  <url><loc>{GUIDE_URL}</loc></url>\n</urlset>"))

#!/usr/bin/env python3
"""
IndexNow bulk submitter for qantcore.space
Usage: python3 /opt/data/scripts/indexnow_submit.py [--sitemap] [--url URL]
"""
import urllib.request, ssl, json, sys, xml.etree.ElementTree as ET

KEY = "af6b31b1d07db24583da448b09758613"
SITE = "https://qantcore.space"
KEY_LOC = f"{SITE}/indexnow-{KEY}.txt"
ENDPOINTS = ["https://api.indexnow.org/indexnow", "https://yandex.com/indexnow"]

def get_sitemap_urls():
    ctx = ssl.create_default_context()
    req = urllib.request.Request(f'{SITE}/sitemap.xml')
    req.add_header('User-Agent', 'Mozilla/5.0')
    resp = urllib.request.urlopen(req, context=ctx)
    root = ET.fromstring(resp.read().decode())
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [elem.text for elem in root.findall('.//ns:loc', ns)]

urls = []
if '--sitemap' in sys.argv:
    urls = get_sitemap_urls()
    print(f"Sitemap: {len(urls)} URLs")
elif '--url' in sys.argv:
    idx = sys.argv.index('--url')
    urls = [sys.argv[idx+1]]
else:
    urls = get_sitemap_urls()

payload = json.dumps({
    "host": "qantcore.space",
    "key": KEY,
    "keyLocation": KEY_LOC,
    "urlList": urls
}).encode()

ctx = ssl.create_default_context()
for ep in ENDPOINTS:
    req = urllib.request.Request(ep, data=payload, method='POST')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    try:
        resp = urllib.request.urlopen(req, context=ctx)
        print(f"{ep}: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"{ep}: {e.code} {e.read().decode()[:200]}")

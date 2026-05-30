#!/usr/bin/env python3
"""
Bing URL Submission — batch 100 URLs/day
Usage: python3 /opt/data/scripts/bing_submit.py
"""
import urllib.request, ssl, json, xml.etree.ElementTree as ET, os

KEY = "db231b7e28394c9c82889f8027fff23f"
SITE = "https://qantcore.space"
STATE_FILE = "/tmp/bing_submit_state.txt"

ctx = ssl.create_default_context()

# Get all URLs from sitemap
req = urllib.request.Request(f'{SITE}/sitemap.xml')
req.add_header('User-Agent', 'Mozilla/5.0')
resp = urllib.request.urlopen(req, context=ctx)
root = ET.fromstring(resp.read().decode())
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
all_urls = [elem.text for elem in root.findall('.//ns:loc', ns)]

# Read progress
start_idx = 0
if os.path.exists(STATE_FILE):
    with open(STATE_FILE) as f:
        start_idx = int(f.read().strip())

# Submit next batch
batch = all_urls[start_idx:start_idx+100]
endpoint = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey={KEY}"
payload = json.dumps({"siteUrl": SITE, "urlList": batch}).encode()

req2 = urllib.request.Request(endpoint, data=payload, method='POST')
req2.add_header('Content-Type', 'application/json')
resp2 = urllib.request.urlopen(req2, context=ctx)
result = resp2.read().decode()

new_idx = min(start_idx + 100, len(all_urls))
with open(STATE_FILE, 'w') as f:
    f.write(str(new_idx))

print(f"Submitted: {start_idx}-{new_idx-1} ({len(batch)} URLs)")
print(f"Progress: {new_idx}/{len(all_urls)}")
if new_idx >= len(all_urls):
    print("DONE — all URLs submitted")

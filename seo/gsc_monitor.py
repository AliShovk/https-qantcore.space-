#!/usr/bin/env python3
"""
GSC Monitoring Script for qantcore.space
Usage: python3 /opt/data/scripts/gsc_monitor.py
Scheduled: daily via Hermes cron
"""
import json, time, urllib.request, urllib.parse, ssl, base64, sys
from datetime import datetime

KEY_PATH = '/opt/data/skills/seo/google-search-console/references/hermes-gsc-key.json'
SITE = 'https://qantcore.space/'

try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError:
    print("ERROR: cryptography not installed")
    sys.exit(1)

with open(KEY_PATH) as f:
    key = json.load(f)

def b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

private_key = serialization.load_pem_private_key(key['private_key'].encode(), password=None)

def get_token():
    header = b64url(json.dumps({"alg":"RS256","typ":"JWT"}).encode())
    now = int(time.time())
    payload = b64url(json.dumps({
        "iss": key['client_email'],
        "scope": "https://www.googleapis.com/auth/webmasters",
        "aud": key['token_uri'],
        "exp": now + 3600,
        "iat": now
    }).encode())
    msg = f"{header}.{payload}".encode()
    sig = private_key.sign(msg, padding.PKCS1v15(), hashes.SHA256())
    jwt = f"{header}.{payload}.{b64url(sig)}"
    
    ctx = ssl.create_default_context()
    data = urllib.parse.urlencode({
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt
    }).encode()
    req = urllib.request.Request(key['token_uri'], data=data, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    return json.loads(urllib.request.urlopen(req, context=ctx).read())['access_token']

token = get_token()
ctx = ssl.create_default_context()
encoded = urllib.parse.quote(SITE, safe='')

report = []
report.append(f"=== GSC Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
report.append(f"Site: {SITE}")

# 1. Sitemap status
sitemap_enc = urllib.parse.quote(f'{SITE}sitemap.xml', safe='')
req = urllib.request.Request(f'https://www.googleapis.com/webmasters/v3/sites/{encoded}/sitemaps/{sitemap_enc}')
req.add_header('Authorization', f'Bearer {token}')
try:
    resp = urllib.request.urlopen(req, context=ctx)
    sm = json.loads(resp.read())
    report.append(f"\n[SITEMAP]")
    report.append(f"  Last submitted: {sm.get('lastSubmitted', '?')}")
    report.append(f"  Last downloaded: {sm.get('lastDownloaded', '?')}")
    report.append(f"  Errors: {sm.get('errors', '?')}  Warnings: {sm.get('warnings', '?')}")
    for c in sm.get('contents', []):
        report.append(f"  {c.get('type')}: submitted={c.get('submitted')} indexed={c.get('indexed')}")
except Exception as e:
    report.append(f"\n[SITEMAP] ERROR: {e}")

# 2. Check sample URLs
sample_urls = [
    SITE,
    f'{SITE}catalog/product/',
    f'{SITE}product/cursor-ide',
    f'{SITE}compare/claude-vs-gpt/',
    f'{SITE}best/',
]
report.append(f"\n[URL INSPECTION]")
for url in sample_urls:
    req2 = urllib.request.Request(
        'https://searchconsole.googleapis.com/v1/urlInspection/index:inspect',
        data=json.dumps({"inspectionUrl": url, "siteUrl": SITE}).encode(),
        method='POST'
    )
    req2.add_header('Authorization', f'Bearer {token}')
    req2.add_header('Content-Type', 'application/json')
    try:
        resp2 = urllib.request.urlopen(req2, context=ctx)
        ins = json.loads(resp2.read())['inspectionResult']['indexStatusResult']
        state = ins.get('coverageState', '?')
        last_crawl = ins.get('lastCrawlTime', 'never')
        report.append(f"  {url.replace(SITE, '/')}: {state} (crawled: {last_crawl})")
    except Exception as e:
        report.append(f"  {url.replace(SITE, '/')}: ERROR {e}")

# 3. Search Analytics (last 7 days)
from datetime import datetime, timedelta
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

req3 = urllib.request.Request(
    f'https://www.googleapis.com/webmasters/v3/sites/{encoded}/searchAnalytics/query',
    data=json.dumps({
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 20,
        "aggregationType": "auto"
    }).encode(),
    method='POST'
)
req3.add_header('Authorization', f'Bearer {token}')
req3.add_header('Content-Type', 'application/json')
try:
    resp3 = urllib.request.urlopen(req3, context=ctx)
    analytics = json.loads(resp3.read())
    rows = analytics.get('rows', [])
    report.append(f"\n[SEARCH ANALYTICS] ({start_date} → {end_date})")
    if rows:
        total_clicks = sum(r['clicks'] for r in rows)
        total_impr = sum(r['impressions'] for r in rows)
        report.append(f"  Total: {total_clicks} clicks, {total_impr} impressions")
        report.append(f"  Top queries:")
        for r in rows[:10]:
            report.append(f"    {r['keys'][0][:50]}: {r['clicks']} clicks, {r['impressions']} impr, pos={r['position']:.1f}")
    else:
        report.append(f"  No data yet — site not yet in index")
except Exception as e:
    report.append(f"\n[ANALYTICS] ERROR: {e}")

print('\n'.join(report))

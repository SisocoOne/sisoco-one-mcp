"""Check a company (Python 3.9+, standard library only). No key needed for 25 lookups a day per IP.

Usage: python3 check.py [company] [country]     e.g. python3 check.py 03959649 GB
"""
import json, os, sys, urllib.error, urllib.parse, urllib.request

company = sys.argv[1] if len(sys.argv) > 1 else "03959649"
country = sys.argv[2] if len(sys.argv) > 2 else "GB"
base = os.environ.get("SISOCO_BASE_URL", "https://api.sisoco.co.uk")
headers = {"Authorization": f"Bearer {os.environ['SISOCO_API_KEY']}"} if os.environ.get("SISOCO_API_KEY") else {}

url = f"{base}/v1/check?" + urllib.parse.urlencode({"company": company, "country": country})
try:
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        print(json.dumps(json.load(r), indent=2))
except urllib.error.HTTPError as e:
    # Errors carry a stable `code`, a `doc_url` and what to do next.
    print(e.code, e.read().decode(), file=sys.stderr)
    sys.exit(1)

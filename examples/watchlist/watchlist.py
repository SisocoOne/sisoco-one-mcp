"""Watch ten UK companies and get a signed webhook for every event on them (Python 3.9+, standard library only).

Needs an account key with the `watch` scope (Free plan: 25 watched companies). Free preview keys are read-only.

    SISOCO_API_KEY=sisk_live_... WEBHOOK_URL=https://your.host/sisoco python3 watchlist.py

WEBHOOK_URL: https on port 443, public DNS name, answers 2xx (see ../webhook-receiver). Leave it unset to skip
the webhook and only poll the event feed.
"""
import json, os, urllib.error, urllib.parse, urllib.request

BASE = os.environ.get("SISOCO_BASE_URL", "https://api.sisoco.co.uk")
KEY = os.environ.get("SISOCO_API_KEY") or exit("Set SISOCO_API_KEY (create one at https://api.sisoco.co.uk/app)")

COMPANIES = [
    ("03959649", "easyJet plc"), ("00445790", "Tesco PLC"), ("00102498", "BP p.l.c."), ("00041424", "Unilever PLC"),
    ("01833679", "Vodafone Group plc"), ("00617987", "HSBC Holdings plc"), ("00048839", "Barclays PLC"),
    ("04190816", "BT Group plc"), ("04256886", "Marks and Spencer Group plc"), ("00185647", "J Sainsbury plc"),
]


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Authorization": f"Bearer {KEY}", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {path} -> {e.code} {e.read().decode()}")


# 1. A watchlist groups the companies you follow.
watchlist = call("POST", "/v1/watchlists", {"name": "Example"})["data"]
print("watchlist", watchlist["id"])

# 2. Add companies by registry number (up to 500 per call). client_reference is your own id, echoed on every event.
call("POST", f"/v1/watchlists/{watchlist['id']}/entities",
     {"entities": [{"identifier": i, "country": "GB", "client_reference": n} for i, n in COMPANIES]})
print("watching", len(COMPANIES), "companies")

# 3. Register a webhook. The signing secret is shown ONCE: store it where your receiver can read it.
if os.environ.get("WEBHOOK_URL"):
    hook = call("POST", "/v1/webhooks", {"url": os.environ["WEBHOOK_URL"], "event_types": []})["data"]
    print("webhook", hook["id"], "- store this secret now:", hook["secret"])
    # 4. One signed sample event (header Sisoco-Test: true) to check your endpoint and signature check.
    call("POST", f"/v1/webhooks/{hook['id']}/test")
    print(f"test event sent; see GET /v1/webhooks/{hook['id']}/deliveries")

# 5. The same events by polling. Keep meta.next_cursor and send it as `cursor` next time.
feed = call("GET", "/v1/events?" + urllib.parse.urlencode({"watchlist_id": watchlist["id"]}))
print("events so far:", len(feed["data"]), "next cursor:", (feed.get("meta") or {}).get("next_cursor"))

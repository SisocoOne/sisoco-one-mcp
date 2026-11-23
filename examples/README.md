# Sisoco One examples

Small, dependency-free samples for the three things most integrations do. Node 18+ or Python 3.9+; nothing to install.

| Folder | What it does | Key needed |
|---|---|---|
| [`check/`](check) | Check a company: identity, status, signals and recent events, each with its official source | None (25 lookups a day per IP); a key uses its quota |
| [`watchlist/`](watchlist) | Watch ten UK companies, register a webhook, send a signed test event, read the event feed | Account key with `watch` scope — free at [/app](https://api.sisoco.co.uk/app) (Free plan: 25 watched companies) |
| [`webhook-receiver/`](webhook-receiver) | Receive events: verify `Sisoco-Signature`, answer 2xx fast, dedupe on `event_id` | The webhook's `whsec_…` secret |

## Check a company

```sh
./check/check.sh 03959649 GB          # easyJet plc
node check/check.mjs 00519500 GB      # Tesco Stores Ltd
python3 check/check.py 552032534 FR   # Danone (SIREN)
```

## Watch companies and get webhooks

```sh
export SISOCO_API_KEY=sisk_live_...                  # from https://api.sisoco.co.uk/app
export WEBHOOK_URL=https://hooks.example.com/sisoco  # optional; https, port 443, public DNS name
node watchlist/watchlist.mjs                         # or: python3 watchlist/watchlist.py
```

The webhook's signing secret is printed **once**. Store it for your receiver.

## Receive webhooks

```sh
SISOCO_WEBHOOK_SECRET=whsec_... PORT=8080 node webhook-receiver/node/server.mjs
SISOCO_WEBHOOK_SECRET=whsec_... PORT=8080 python3 webhook-receiver/python/server.py
```

Put the receiver behind HTTPS on port 443 (reverse proxy, tunnel or your platform's router); deliveries do not follow redirects.

- **Signature:** `Sisoco-Signature: t=<unix seconds>,v1=<hex>`, HMAC-SHA256 with your secret over `<t>.<raw body>`. Verify the raw bytes before parsing, in constant time, within 5 minutes. During a secret rotation there are two `v1=` values: accept either.
- **Delivery:** at least once, retried with back-off for 24 hours. Dedupe on `event_id`; answer within 10 seconds.
- **Test events** carry the header `Sisoco-Test: true` and an `event_id` starting `evt_test_`.

Full reference: [webhooks guide](https://api.sisoco.co.uk/docs/webhooks), [API reference](https://api.sisoco.co.uk/docs/reference), [plans](https://api.sisoco.co.uk/plans).

All samples read `SISOCO_BASE_URL` (default `https://api.sisoco.co.uk`).

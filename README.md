# Sisoco One

[![mcptry status](https://mcptry.com/badge/uk.co.sisoco/uk-companies-house-ownership.svg)](https://mcptry.com/servers/uk.co.sisoco/uk-companies-house-ownership)

**Check and monitor UK and EU companies with your AI agent, from the official registers.**

Sisoco One is a remote MCP server and REST API for checking and monitoring UK and EU companies: identity, status, who owns and controls the company, corporate insolvency notices, LEIs and sanctions possible matches. Your agent can watch hundreds of companies (suppliers, customers, borrowers, holdings) and report what changed. Every fact carries its source.

- Website: https://api.sisoco.co.uk/
- MCP endpoint (streamable HTTP): `https://api.sisoco.co.uk/mcp`
- Official MCP Registry: `uk.co.sisoco/uk-companies-house-ownership`
- API reference: [OpenAPI 3.1](https://api.sisoco.co.uk/openapi.json) and [llms.txt](https://api.sisoco.co.uk/llms.txt)

This repository holds the connection guide, the registry entry ([`server.json`](server.json)) and [**examples**](examples): check a company, watch companies with a webhook, and a signed-webhook receiver in Node and Python. The server itself is hosted by Sisoco Partners; there is nothing to install.

## Try it without a key

Every client IP gets 25 free lookups a day with no key, over REST and MCP:

```sh
curl "https://api.sisoco.co.uk/v1/check?company=03959649&country=GB"
```

## Connect

**Claude Code**, no key:

```sh
claude mcp add --transport http sisoco-one https://api.sisoco.co.uk/mcp
```

**Free key** (no sign-up, no email; 100 lookups a month, read-only, valid 30 days, shown once):

```sh
curl -X POST https://api.sisoco.co.uk/v1/preview/keys \
  -H "content-type: application/json" \
  -d '{"source":"direct"}'
```

Then send it as a bearer token:

```sh
claude mcp add --transport http sisoco-one https://api.sisoco.co.uk/mcp \
  --header "Authorization: Bearer YOUR_KEY"
```

**Cursor** (`.cursor/mcp.json`) and other clients that take headers:

```json
{
  "mcpServers": {
    "sisoco-one": {
      "url": "https://api.sisoco.co.uk/mcp",
      "headers": { "Authorization": "Bearer YOUR_KEY" }
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `sisoco_check_company` | Identity, signals and recent events for a UK company number, French SIREN, LEI or name. Start here. |
| `sisoco_search_company` | Find a UK company number by name. |
| `sisoco_company_officers` | Directors, secretaries and LLP members of a UK company, current and former. |
| `sisoco_ownership_chain` | Who owns or controls a UK company, and who owns them; if the register lists no owner, why (e.g. listed-company exemption). |
| `sisoco_get_lei_record` | The GLEIF record for an LEI. |
| `sisoco_get_lei_parents` | Direct and ultimate parent companies of an LEI, any country (GLEIF Level 2). |
| `sisoco_recent_events` | What changed on a company recently. |

These are read-only. Each costs one lookup, the same as its REST equivalent.

### Monitoring (account API key)

| Tool | What it does |
|---|---|
| `sisoco_watch_many` | Watch a list of companies: up to 100 per call (1,000 per call over the REST API). |
| `sisoco_watchlist_changes` | What changed across every watched company since a date, or since the last call: insolvency notices, status changes, overdue filings, directors, changes of control, charges, possible sanctions matches, LEI lapses. |
| `sisoco_watch` / `sisoco_unwatch` | Watch or stop watching one company. |
| `sisoco_list_watched` | What is watched, and how much of the plan is used. |

Monitoring tools cost no lookups. They need an account API key: a free account watches 25 companies (work email, no card) at https://api.sisoco.co.uk/app. The same changes can be delivered as signed webhooks.

## What it returns

Facts from the record, never a verdict: no risk scores or "safe / risky" labels. When something is missing, the answer says so and why. Sanctions results are possible matches with a score, for a person to review.

## Sources

Free official sources licensed for commercial reuse, including Companies House, The Gazette, GLEIF, the French Annuaire des Entreprises and BODACC, and the UK, EU and US (OFAC) sanctions lists. The live list with licences is on the [website](https://api.sisoco.co.uk/).

## Pricing

Checks: free without a key (25 lookups a day) or with a free key (100 a month), then 2p a lookup. Monitoring: a free account watches 25 companies; paid plans are sized by companies watched, from £29 a month for 500. Details on the [website](https://api.sisoco.co.uk/#pricing).

## Terms and privacy

[Terms](https://api.sisoco.co.uk/terms) · [Privacy](https://api.sisoco.co.uk/privacy)

Sisoco One is a product of Sisoco Partners Ltd, registered in England and Wales, number 10548251, 118 Pall Mall, London SW1Y 5ED. Not affiliated with Companies House or any government body.

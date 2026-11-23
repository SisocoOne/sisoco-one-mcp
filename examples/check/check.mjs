// Check a company (Node 18+, no dependencies). No key needed for 25 lookups a day per IP.
// Usage: node check.mjs [company] [country]     e.g. node check.mjs 03959649 GB
const [company = '03959649', country = 'GB'] = process.argv.slice(2);
const base = process.env.SISOCO_BASE_URL ?? 'https://api.sisoco.co.uk';
const headers = process.env.SISOCO_API_KEY ? { Authorization: `Bearer ${process.env.SISOCO_API_KEY}` } : {};

const res = await fetch(`${base}/v1/check?${new URLSearchParams({ company, country })}`, { headers });
const body = await res.json();
if (!res.ok) {
  // Errors carry a stable `code`, a `doc_url` and what to do next.
  console.error(res.status, body.error ?? body);
  process.exit(1);
}
console.log(JSON.stringify(body, null, 2));

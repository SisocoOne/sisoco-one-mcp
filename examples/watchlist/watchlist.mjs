// Watch ten UK companies and get a signed webhook for every event on them (Node 18+, no dependencies).
// Needs an account key with the `watch` scope (Free plan: 25 watched companies). Free preview keys are read-only.
//
//   SISOCO_API_KEY=sisk_live_... WEBHOOK_URL=https://your.host/sisoco node watchlist.mjs
//
// WEBHOOK_URL: https on port 443, public DNS name, answers 2xx (see ../webhook-receiver). Leave it unset to skip
// the webhook and only poll the event feed.
const base = process.env.SISOCO_BASE_URL ?? 'https://api.sisoco.co.uk';
const key = process.env.SISOCO_API_KEY;
if (!key) throw new Error('Set SISOCO_API_KEY (create one at https://api.sisoco.co.uk/app)');
const headers = { Authorization: `Bearer ${key}`, 'content-type': 'application/json' };

async function call(method, path, body) {
  const res = await fetch(base + path, { method, headers, ...(body && { body: JSON.stringify(body) }) });
  const json = res.status === 204 ? null : await res.json();
  if (!res.ok) throw new Error(`${method} ${path} → ${res.status} ${JSON.stringify(json?.error ?? json)}`);
  return json;
}

const COMPANIES = [
  ['03959649', 'easyJet plc'], ['00445790', 'Tesco PLC'], ['00102498', 'BP p.l.c.'], ['00041424', 'Unilever PLC'],
  ['01833679', 'Vodafone Group plc'], ['00617987', 'HSBC Holdings plc'], ['00048839', 'Barclays PLC'],
  ['04190816', 'BT Group plc'], ['04256886', 'Marks and Spencer Group plc'], ['00185647', 'J Sainsbury plc'],
];

// 1. A watchlist groups the companies you follow.
const watchlist = (await call('POST', '/v1/watchlists', { name: 'Example' })).data;
console.log('watchlist', watchlist.id);

// 2. Add companies by registry number (up to 500 per call). client_reference is your own id, echoed on every event.
await call('POST', `/v1/watchlists/${watchlist.id}/entities`, {
  entities: COMPANIES.map(([identifier, name]) => ({ identifier, country: 'GB', client_reference: name })),
});
console.log('watching', COMPANIES.length, 'companies');

// 3. Register a webhook. The signing secret is shown ONCE: store it where your receiver can read it.
if (process.env.WEBHOOK_URL) {
  const hook = (await call('POST', '/v1/webhooks', { url: process.env.WEBHOOK_URL, event_types: [] })).data;
  console.log('webhook', hook.id, '— store this secret now:', hook.secret);
  // 4. One signed sample event (header Sisoco-Test: true) to check your endpoint and signature check.
  await call('POST', `/v1/webhooks/${hook.id}/test`);
  console.log('test event sent; see GET /v1/webhooks/' + hook.id + '/deliveries');
}

// 5. The same events by polling. Keep meta.next_cursor and send it as `cursor` next time.
const feed = await call('GET', `/v1/events?watchlist_id=${encodeURIComponent(watchlist.id)}`);
console.log('events so far:', feed.data.length, 'next cursor:', feed.meta?.next_cursor ?? null);

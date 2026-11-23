// Minimal Sisoco One webhook receiver (Node 18+, no dependencies).
//
//   SISOCO_WEBHOOK_SECRET=whsec_... PORT=8080 node server.mjs
//
// Put it behind HTTPS on port 443 with a public DNS name (a reverse proxy, a tunnel or your platform's router):
// Sisoco One only delivers to https:// on 443 and does not follow redirects.
import { createServer } from 'node:http';
import { verifySisocoSignature } from './verify.mjs';

const secret = process.env.SISOCO_WEBHOOK_SECRET;
if (!secret) throw new Error('Set SISOCO_WEBHOOK_SECRET to the whsec_… shown when you registered the webhook');
const seen = new Set(); // Delivery is at least once: dedupe on event_id (use your database in production).

const server = createServer((req, res) => {
  if (req.method !== 'POST') return res.writeHead(405).end();
  const chunks = [];
  req.on('data', (c) => chunks.push(c));
  req.on('end', () => {
    const raw = Buffer.concat(chunks); // verify the exact bytes received, before JSON parsing
    if (!verifySisocoSignature(raw, req.headers['sisoco-signature'], secret)) return res.writeHead(401).end('bad signature');
    const event = JSON.parse(raw.toString('utf8'));
    // Answer within 10 seconds; do slow work after replying.
    res.writeHead(200).end('ok');
    if (seen.has(event.event_id)) return;
    seen.add(event.event_id);
    const test = req.headers['sisoco-test'] === 'true' ? ' (test)' : '';
    console.log(`${event.event_id} ${event.type ?? ''} ${event.client_reference ?? ''}${test}`);
  });
});

server.listen(Number(process.env.PORT ?? 8080), () => console.log('listening on', server.address().port));
export default server;

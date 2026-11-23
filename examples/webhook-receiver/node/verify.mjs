import { createHmac, timingSafeEqual } from 'node:crypto';

/**
 * true when `signatureHeader` (the Sisoco-Signature header) was made with
 * `secret` over `rawBody` (a string or Buffer of the exact bytes received)
 * within `toleranceSeconds` of now. Same code as https://api.sisoco.co.uk/docs/webhooks
 */
export function verifySisocoSignature(rawBody, signatureHeader, secret, toleranceSeconds = 300) {
  const parts = String(signatureHeader)
    .split(',')
    .map((p) => p.trim().split('=', 2));
  const t = Number(parts.find(([k]) => k === 't')?.[1]);
  // One v1 per active secret (two during a secret rotation): accept any that matches.
  const signatures = parts.filter(([k, v]) => k === 'v1' && v).map(([, v]) => Buffer.from(v, 'utf8'));
  if (!Number.isInteger(t) || signatures.length === 0) return false;
  if (Math.abs(Math.floor(Date.now() / 1000) - t) > toleranceSeconds) return false;
  const expected = Buffer.from(createHmac('sha256', secret).update(`${t}.`).update(rawBody).digest('hex'), 'utf8');
  return signatures.some((b) => b.length === expected.length && timingSafeEqual(expected, b));
}

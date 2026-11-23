"""Minimal Sisoco One webhook receiver (Python 3.9+, standard library only).

    SISOCO_WEBHOOK_SECRET=whsec_... PORT=8080 python3 server.py

Put it behind HTTPS on port 443 with a public DNS name (a reverse proxy, a tunnel or your platform's router):
Sisoco One only delivers to https:// on 443 and does not follow redirects.
"""
import json, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from verify import verify_sisoco_signature

SECRET = os.environ.get("SISOCO_WEBHOOK_SECRET") or exit("Set SISOCO_WEBHOOK_SECRET to the whsec_... from registration")
seen = set()  # Delivery is at least once: dedupe on event_id (use your database in production).


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        raw = self.rfile.read(int(self.headers.get("content-length", 0)))  # exact bytes, before JSON parsing
        if not verify_sisoco_signature(raw, self.headers.get("sisoco-signature", ""), SECRET):
            self.send_response(401); self.end_headers(); self.wfile.write(b"bad signature"); return
        event = json.loads(raw)
        # Answer within 10 seconds; do slow work after replying.
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")
        if event.get("event_id") in seen:
            return
        seen.add(event.get("event_id"))
        test = " (test)" if self.headers.get("sisoco-test") == "true" else ""
        print(event.get("event_id"), event.get("type", ""), event.get("client_reference") or "", test, flush=True)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    print("listening on", port, flush=True)
    ThreadingHTTPServer(("", port), Handler).serve_forever()

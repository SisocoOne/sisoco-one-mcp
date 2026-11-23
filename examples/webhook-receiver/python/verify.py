"""Sisoco One webhook signature check. Same code as https://api.sisoco.co.uk/docs/webhooks"""
import hashlib, hmac, time


def verify_sisoco_signature(raw_body: bytes, header: str, secret: str, tolerance: int = 300) -> bool:
    pairs = [p.strip().split("=", 1) for p in header.split(",") if "=" in p]
    try:
        t = int(next((v for k, v in pairs if k == "t"), ""))
    except ValueError:
        return False
    # One v1 per active secret (two during a secret rotation): accept any that matches.
    signatures = [v for k, v in pairs if k == "v1"]
    if abs(time.time() - t) > tolerance or not signatures:
        return False
    expected = hmac.new(secret.encode(), f"{t}.".encode() + raw_body, hashlib.sha256).hexdigest()
    return any(hmac.compare_digest(expected, s) for s in signatures)

import time
import json
import base64
import hmac
import hashlib
from flask import Blueprint, current_app, request, jsonify

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("utf-8")


def _make_jwt(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b = _b64url_encode(json.dumps(header).encode("utf-8"))
    payload_b = _b64url_encode(json.dumps(payload).encode("utf-8"))
    signing = (header_b + "." + payload_b).encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), signing, hashlib.sha256).digest()
    sig_b = _b64url_encode(sig)
    return header_b + "." + payload_b + "." + sig_b


@auth_bp.route("/token", methods=["POST"])
def issue_token():
    """Issue a short-lived HS256 JWT for uploads.

    Accepts an `X-API-Key` header which must match `UPLOAD_API_KEY` config.
    Returns JSON `{token: <jwt>}` with `role: uploader` and `exp` claim.
    """
    api_key = request.headers.get("X-API-Key")
    expected = current_app.config.get("UPLOAD_API_KEY")
    if not expected:
        return jsonify({"error": "not configured"}), 503
    # support comma-separated keys
    valid_keys = [k.strip() for k in expected.split(",") if k.strip()]
    if not api_key or api_key not in valid_keys:
        return jsonify({"error": "forbidden"}), 403

    secret = current_app.config.get("UPLOAD_JWT_SECRET")
    if not secret:
        return jsonify({"error": "jwt not configured"}), 503

    ttl = int(current_app.config.get("UPLOAD_JWT_TTL", 15 * 60))
    now = int(time.time())
    payload = {"role": "uploader", "exp": now + ttl}
    token = _make_jwt(payload, secret)
    return jsonify({"token": token}), 200

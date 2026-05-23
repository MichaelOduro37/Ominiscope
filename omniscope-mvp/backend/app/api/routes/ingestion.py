import os
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    send_from_directory,
    abort,
)
from werkzeug.utils import secure_filename
import base64
import hmac
import hashlib
import json
import time

ingestion_bp = Blueprint("ingestion", __name__, url_prefix="/ingest")


def upload_dir():
    return current_app.config.get("UPLOAD_DIR")


@ingestion_bp.route("/files", methods=["GET"])
def list_files():
    d = upload_dir()
    try:
        files = sorted(os.listdir(d))
    except Exception:
        files = []
    return jsonify({"files": files})


@ingestion_bp.route("/files/<path:filename>", methods=["GET"])
def get_file(filename):
    d = upload_dir()
    safe = secure_filename(filename)
    full = os.path.join(d, safe)
    if not os.path.exists(full):
        abort(404)
    return send_from_directory(d, safe, as_attachment=False)


def _verify_upload_bearer_token(token: str):
    payload = _verify_upload_jwks_token(token)
    if payload is not None:
        return payload
    return _verify_upload_hs256_token(token)


def _verify_upload_jwks_token(token: str):
    jwks_url = current_app.config.get("UPLOAD_JWT_JWKS_URL")
    if not jwks_url:
        return None
    try:
        from app.auth.oidc import verify_jwt_via_jwks

        audience = current_app.config.get("UPLOAD_JWT_AUDIENCE")
        return verify_jwt_via_jwks(token, jwks_url, audience=audience)
    except Exception:
        return None


def _verify_upload_hs256_token(token: str):
    jwt_secret = current_app.config.get("UPLOAD_JWT_SECRET")
    if not jwt_secret:
        return None
    try:
        return _verify_jwt_hs256(token, jwt_secret)
    except Exception:
        return None


def _is_upload_rbac_enabled():
    return current_app.config.get("RBAC_ENABLED", False) and not current_app.config.get(
        "TESTING", False
    )


def _is_valid_upload_api_key():
    expected = current_app.config.get("UPLOAD_API_KEY")
    if not expected:
        return False
    api_key = request.headers.get("X-API-Key")
    valid_keys = [k.strip() for k in expected.split(",") if k.strip()]
    return bool(api_key and api_key in valid_keys)


def _authorize_bearer_upload():
    auth = request.headers.get("Authorization", "")
    if not auth or not auth.lower().startswith("bearer "):
        return None
    token = auth.split(None, 1)[1].strip()
    payload = _verify_upload_bearer_token(token)
    if not payload or not _jwt_allows_upload(payload):
        return jsonify({"error": "forbidden"}), 403
    return None


def _authorize_technician_upload():
    role = request.headers.get("X-Role", "")
    if role != "Technician":
        return jsonify({"error": "forbidden"}), 403
    return None


def _authorize_upload_request():
    if not _is_upload_rbac_enabled():
        return None
    if _is_valid_upload_api_key():
        return None

    auth = request.headers.get("Authorization", "")
    if auth and auth.lower().startswith("bearer "):
        bearer_error = _authorize_bearer_upload()
        if bearer_error is not None:
            return bearer_error
        return None

    bearer_error = _authorize_bearer_upload()
    if bearer_error is not None:
        return bearer_error

    return _authorize_technician_upload()


@ingestion_bp.route("/upload", methods=["POST"])
def upload_file():
    auth_error = _authorize_upload_request()
    if auth_error is not None:
        return auth_error

    # quick size check from the request headers when available
    max_bytes = current_app.config.get("UPLOAD_MAX_BYTES")
    if request.content_length and max_bytes and request.content_length > max_bytes:
        return jsonify({"error": "payload too large"}), 413

    if "file" not in request.files:
        return jsonify({"error": "no file part"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "empty filename"}), 400
    filename = secure_filename(f.filename)
    # basic content type and extension restrictions
    allowed_mimes = current_app.config.get("UPLOAD_ALLOWED_MIMETYPES")
    allowed_exts = current_app.config.get("UPLOAD_ALLOWED_EXTENSIONS")
    if allowed_mimes and (f.mimetype and f.mimetype not in allowed_mimes):
        return jsonify({"error": "unsupported media type"}), 415
    if allowed_exts:
        _, ext = os.path.splitext(filename)
        if ext and ext.lower() not in allowed_exts:
            return jsonify({"error": "unsupported file extension"}), 415

    d = upload_dir()
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, filename)
    f.save(path)
    # post-save size enforcement (in case request.content_length was not present)
    try:
        if max_bytes and os.path.getsize(path) > max_bytes:
            os.remove(path)
            return jsonify({"error": "file too large"}), 413
    except OSError:
        # if we can't stat/remove, signal server error
        return jsonify({"error": "internal error"}), 500
    # simple audit
    audit = current_app.config.setdefault("AUDIT_LOG", [])
    audit.append({"action": "upload", "file": filename})
    return jsonify({"saved": filename}), 201


def _b64url_decode(value: str) -> bytes:
    # add padding
    rem = len(value) % 4
    if rem:
        value += "=" * (4 - rem)
    return base64.urlsafe_b64decode(value.encode("utf-8"))


def _verify_jwt_hs256(token: str, secret: str):
    """Minimal HS256 JWT verifier returning the payload dict or raising."""
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid token")
    header_b, payload_b, sig_b = parts
    try:
        header = json.loads(_b64url_decode(header_b))
        payload = json.loads(_b64url_decode(payload_b))
    except Exception as e:
        raise ValueError("invalid token payload") from e

    if header.get("alg") != "HS256":
        raise ValueError("unsupported alg")

    signing_input = (header_b + "." + payload_b).encode("utf-8")
    expected_sig = hmac.new(
        secret.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    try:
        sig = _b64url_decode(sig_b)
    except Exception:
        raise ValueError("invalid signature")

    if not hmac.compare_digest(expected_sig, sig):
        raise ValueError("signature mismatch")

    # check exp if present
    now = int(time.time())
    exp = payload.get("exp")
    if exp is not None and int(exp) < now:
        raise ValueError("token expired")

    return payload


def _jwt_allows_upload(payload: dict) -> bool:
    # policy: require role 'uploader' or scope containing 'upload'
    role = payload.get("role")
    if role == "uploader":
        return True
    scope = payload.get("scope", "")
    if isinstance(scope, str) and "upload" in scope.split():
        return True
    if isinstance(scope, list) and "upload" in scope:
        return True
    return False

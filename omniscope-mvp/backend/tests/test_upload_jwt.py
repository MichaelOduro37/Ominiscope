import io
import json
import base64
import hmac
import hashlib
import time
from app import create_app


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


def test_upload_with_valid_jwt(tmp_path):
    secret = "test-secret"
    exp = int(time.time()) + 60
    payload = {"role": "uploader", "exp": exp}
    token = _make_jwt(payload, secret)

    app = create_app(
        {
            "TESTING": False,
            "UPLOAD_DIR": str(tmp_path),
            "RBAC_ENABLED": True,
            "UPLOAD_JWT_SECRET": secret,
        }
    )
    client = app.test_client()
    data = {"file": (io.BytesIO(b"hello"), "ok.txt")}
    rv = client.post(
        "/ingest/upload",
        data=data,
        content_type="multipart/form-data",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert rv.status_code == 201


def test_upload_with_invalid_jwt(tmp_path):
    secret = "test-secret"
    bad_secret = "bad"
    exp = int(time.time()) + 60
    payload = {"role": "uploader", "exp": exp}
    token = _make_jwt(payload, bad_secret)

    app = create_app(
        {
            "TESTING": False,
            "UPLOAD_DIR": str(tmp_path),
            "RBAC_ENABLED": True,
            "UPLOAD_JWT_SECRET": secret,
        }
    )
    client = app.test_client()
    data = {"file": (io.BytesIO(b"hello"), "ok.txt")}
    rv = client.post(
        "/ingest/upload",
        data=data,
        content_type="multipart/form-data",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert rv.status_code == 403

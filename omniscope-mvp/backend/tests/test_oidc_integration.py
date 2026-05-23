import json
import threading
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from app.auth import oidc


def _b64url_uint(n: int) -> str:
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    s = base64.urlsafe_b64encode(b).decode("ascii")
    return s.rstrip("=")


def _make_jwks_pubkey(kid: str, pubkey):
    numbers = pubkey.public_numbers()
    return {
        "kty": "RSA",
        "kid": kid,
        "use": "sig",
        "alg": "RS256",
        "n": _b64url_uint(numbers.n),
        "e": _b64url_uint(numbers.e),
    }


class JWKSHandler(BaseHTTPRequestHandler):
    def __init__(self, jwks_json, *args, **kwargs):
        self._jwks = jwks_json
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if any(self.path.endswith(suffix) for suffix in ("/jwks.json", ".well-known/jwks.json")):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(self._jwks).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def _run_jwks_server(jwks, host="127.0.0.1"):
    # pick a free port by binding to 0
    def handler(*args, **kwargs):
        JWKSHandler(jwks, *args, **kwargs)

    server = HTTPServer((host, 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    return server, f"http://{host}:{port}/.well-known/jwks.json"


def test_rs256_jwks_flow():
    # generate RSA key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    kid = "integration-kid"

    jwk = _make_jwks_pubkey(kid, public_key)
    jwks = {"keys": [jwk]}

    server, jwks_url = _run_jwks_server(jwks)
    try:
        # create token signed with private key
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        payload = {"role": "uploader"}
        token = jwt.encode(payload, pem, algorithm="RS256", headers={"kid": kid})

        # verify via our helper
        verified = oidc.verify_jwt_via_jwks(token, jwks_url)
        assert verified.get("role") == "uploader"
    finally:
        server.shutdown()

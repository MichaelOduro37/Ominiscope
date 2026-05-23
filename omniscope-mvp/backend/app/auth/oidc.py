"""OIDC/JWKS helper for verifying RS256 JWTs from an issuer's JWKS endpoint.

This is a lightweight implementation suitable for development. It caches the
JWKS keys in memory for the lifetime of the process. In production you should
add robust caching and error handling.
"""
from typing import Dict, Any
import time
import requests
import jwt
from jwt import algorithms


_JWKS_CACHE: Dict[str, Dict[str, Any]] = {}


def _fetch_jwks(jwks_url: str) -> Dict[str, Any]:
    data = requests.get(jwks_url, timeout=5)
    data.raise_for_status()
    return data.json()


def get_public_key_from_jwks(jwks_url: str, kid: str):
    now = int(time.time())
    cache = _JWKS_CACHE.get(jwks_url)
    if cache and cache.get("expires_at", 0) > now:
        jwks = cache["jwks"]
    else:
        jwks = _fetch_jwks(jwks_url)
        # cache for 10 minutes
        _JWKS_CACHE[jwks_url] = {"jwks": jwks, "expires_at": now + 600}

    keys = jwks.get("keys", [])
    for k in keys:
        if k.get("kid") == kid:
            return algorithms.RSAAlgorithm.from_jwk(k)
    raise KeyError("kid not found in jwks")


def verify_jwt_via_jwks(token: str, jwks_url: str, audience: str = None) -> Dict[str, Any]:
    """Verify RS256 token using JWKS. Returns payload dict or raises JWT errors."""
    unverified = jwt.get_unverified_header(token)
    kid = unverified.get("kid")
    if not kid:
        raise jwt.InvalidTokenError("missing kid")
    pubkey = get_public_key_from_jwks(jwks_url, kid)
    options = {"verify_aud": bool(audience)}
    payload = jwt.decode(token, key=pubkey, algorithms=["RS256"], audience=audience, options=options)
    return payload

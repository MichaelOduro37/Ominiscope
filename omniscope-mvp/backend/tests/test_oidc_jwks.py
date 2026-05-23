import json
from unittest.mock import patch, MagicMock

from app.auth import oidc


def test_get_public_key_from_jwks_caches_and_returns_key():
    jwks_url = "https://example.com/.well-known/jwks.json"
    kid = "my-key-id"
    sample_jwks = {"keys": [{"kid": kid, "kty": "RSA", "n": "abc", "e": "AQAB"}]}

    # mock requests.get to return the sample jwks
    mock_resp = MagicMock()
    mock_resp.json.return_value = sample_jwks
    mock_resp.raise_for_status.return_value = None

    with patch("app.auth.oidc.requests.get", return_value=mock_resp) as rg, patch(
        "app.auth.oidc.algorithms.RSAAlgorithm.from_jwk", return_value="PUBKEY"
    ) as from_jwk:
        # first call should fetch via requests.get and call from_jwk
        key = oidc.get_public_key_from_jwks(jwks_url, kid)
        assert key == "PUBKEY"
        rg.assert_called_once_with(jwks_url, timeout=5)
        from_jwk.assert_called_once()

        # second call should hit cache and not call requests.get again
        rg.reset_mock()
        key2 = oidc.get_public_key_from_jwks(jwks_url, kid)
        assert key2 == "PUBKEY"
        rg.assert_not_called()


def test_get_public_key_from_jwks_missing_kid_raises():
    jwks_url = "https://example.com/.well-known/jwks.json"
    sample_jwks = {"keys": [{"kid": "other", "kty": "RSA"}]}
    mock_resp = MagicMock()
    mock_resp.json.return_value = sample_jwks
    mock_resp.raise_for_status.return_value = None

    with patch("app.auth.oidc.requests.get", return_value=mock_resp):
        try:
            oidc.get_public_key_from_jwks(jwks_url, "missing-kid")
            assert False, "expected KeyError"
        except KeyError:
            pass

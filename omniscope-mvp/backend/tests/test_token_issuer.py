import io
from app import create_app


def test_issue_token_and_use(tmp_path):
    secret = "test-secret"
    api_key = "key1"
    app = create_app(
        {
            "TESTING": False,
            "UPLOAD_DIR": str(tmp_path),
            "RBAC_ENABLED": True,
            "UPLOAD_JWT_SECRET": secret,
            "UPLOAD_API_KEY": api_key,
        }
    )
    client = app.test_client()

    # request token with valid API key
    rv = client.post(
        "/auth/token",
        headers={"X-API-Key": api_key},
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert "token" in data
    token = data["token"]

    # use token to upload
    data = {"file": (io.BytesIO(b"hello"), "ok.txt")}
    rv2 = client.post(
        "/ingest/upload",
        data=data,
        content_type="multipart/form-data",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert rv2.status_code == 201


def test_issue_token_with_bad_key(tmp_path):
    secret = "test-secret"
    api_key = "key1"
    app = create_app(
        {
            "TESTING": False,
            "UPLOAD_DIR": str(tmp_path),
            "RBAC_ENABLED": True,
            "UPLOAD_JWT_SECRET": secret,
            "UPLOAD_API_KEY": api_key,
        }
    )
    client = app.test_client()

    rv = client.post(
        "/auth/token",
        headers={"X-API-Key": "bad"},
    )
    assert rv.status_code == 403

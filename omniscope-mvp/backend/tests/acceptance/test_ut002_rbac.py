import io
from app import create_app


def test_upload_rbac(tmp_path):
    upload_dir = str(tmp_path)
    # simulate production: RBAC enabled and not TESTING
    # set a known upload API key for the test
    app = create_app(
        {
            "TESTING": False,
            "RBAC_ENABLED": True,
            "UPLOAD_DIR": upload_dir,
            "UPLOAD_API_KEY": "secret-key",
        }
    )
    client = app.test_client()

    # Wrong API key should be forbidden
    data = {"file": (io.BytesIO(b"hello world"), "test.txt")}
    rv = client.post(
        "/api/v1/ingestion/upload",
        data=data,
        content_type="multipart/form-data",
        headers={"X-API-Key": "wrong"},
    )
    assert rv.status_code == 403

    # Correct API key should be allowed (recreate file stream)
    data = {"file": (io.BytesIO(b"hello world"), "test.txt")}
    rv = client.post(
        "/api/v1/ingestion/upload",
        data=data,
        content_type="multipart/form-data",
        headers={"X-API-Key": "secret-key"},
    )
    assert rv.status_code == 201
    assert rv.get_json().get("saved") == "test.txt"

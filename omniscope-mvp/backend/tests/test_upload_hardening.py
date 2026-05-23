import io
import os
from app import create_app


def test_upload_oversize(tmp_path):
    app = create_app(
        {"TESTING": True, "UPLOAD_DIR": str(tmp_path), "UPLOAD_MAX_BYTES": 10}
    )
    client = app.test_client()
    data = {"file": (io.BytesIO(b"x" * 20), "big.txt")}
    rv = client.post("/ingest/upload", data=data, content_type="multipart/form-data")
    assert rv.status_code == 413
    # ensure no file was left behind
    assert not os.listdir(str(tmp_path))


def test_upload_disallowed_type(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "UPLOAD_DIR": str(tmp_path),
            "UPLOAD_ALLOWED_MIMETYPES": ["text/plain"],
            "UPLOAD_ALLOWED_EXTENSIONS": [".txt"],
        }
    )
    client = app.test_client()
    # upload a png-named file which Werkzeug will treat as image/png
    data = {"file": (io.BytesIO(b"\x89PNG\r\n"), "bad.png")}
    rv = client.post("/ingest/upload", data=data, content_type="multipart/form-data")
    assert rv.status_code == 415
    assert not os.listdir(str(tmp_path))

from app import create_app


def test_ut004_adversarial_input(tmp_path):
    # Placeholder: ensure server doesn't crash on strange payloads
    upload_dir = str(tmp_path)
    app = create_app({"TESTING": True, "UPLOAD_DIR": upload_dir})
    client = app.test_client()

    rv = client.post(
        "/ingest/upload", data={"not_a_file": "x"}, content_type="multipart/form-data"
    )
    # should return 400 (no file part)
    assert rv.status_code == 400

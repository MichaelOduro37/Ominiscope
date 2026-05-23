from app import create_app


def test_ut003_document_extraction(tmp_path):
    # Placeholder: simulate extraction endpoint returning stored artifact
    upload_dir = str(tmp_path)
    app = create_app({"TESTING": True, "UPLOAD_DIR": upload_dir})
    client = app.test_client()

    # This is a placeholder asserting the extraction route will exist later
    rv = client.get("/ingest/files")
    assert rv.status_code == 200

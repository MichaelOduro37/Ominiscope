from app import create_app


def test_ut005_engine_regression(tmp_path):
    # Placeholder: ensure engine regression harness will run in CI later
    upload_dir = str(tmp_path)
    app = create_app({'TESTING': True, 'UPLOAD_DIR': upload_dir})
    client = app.test_client()

    rv = client.get('/ingest/files')
    assert rv.status_code == 200

import io
from app import create_app


def test_list_upload_and_get_file(tmp_path):
    upload_dir = str(tmp_path)
    app = create_app({'TESTING': True, 'UPLOAD_DIR': upload_dir})
    client = app.test_client()

    rv = client.get('/ingest/files')
    assert rv.status_code == 200
    assert rv.get_json() == {'files': []}

    data = {'file': (io.BytesIO(b'hello world'), 'test.txt')}
    rv = client.post('/ingest/upload', data=data, content_type='multipart/form-data')
    assert rv.status_code == 201
    assert rv.get_json().get('saved') == 'test.txt'

    rv = client.get('/ingest/files')
    assert rv.status_code == 200
    assert 'test.txt' in rv.get_json().get('files', [])

    rv = client.get('/ingest/files/test.txt')
    assert rv.status_code == 200
    assert rv.data == b'hello world'


def test_upload_invalid_no_file(tmp_path):
    app = create_app({'TESTING': True, 'UPLOAD_DIR': str(tmp_path)})
    client = app.test_client()
    rv = client.post('/ingest/upload', data={}, content_type='multipart/form-data')
    assert rv.status_code == 400
    assert 'error' in rv.get_json()

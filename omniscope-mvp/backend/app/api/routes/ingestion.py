import os
from flask import Blueprint, current_app, jsonify, request, send_from_directory, abort
from werkzeug.utils import secure_filename

ingestion_bp = Blueprint('ingestion', __name__, url_prefix='/ingest')


def upload_dir():
    return current_app.config.get('UPLOAD_DIR')


@ingestion_bp.route('/files', methods=['GET'])
def list_files():
    d = upload_dir()
    try:
        files = sorted(os.listdir(d))
    except Exception:
        files = []
    return jsonify({'files': files})


@ingestion_bp.route('/files/<path:filename>', methods=['GET'])
def get_file(filename):
    d = upload_dir()
    safe = secure_filename(filename)
    full = os.path.join(d, safe)
    if not os.path.exists(full):
        abort(404)
    return send_from_directory(d, safe, as_attachment=False)


@ingestion_bp.route('/upload', methods=['POST'])
def upload_file():
    # RBAC: if enabled and not in TESTING, only Technician may upload
    if current_app.config.get('RBAC_ENABLED', False) and not current_app.config.get('TESTING', False):
        role = request.headers.get('X-Role', '')
        if role != 'Technician':
            return jsonify({'error': 'forbidden'}), 403

    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400
    filename = secure_filename(f.filename)
    d = upload_dir()
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, filename)
    f.save(path)
    # simple audit
    audit = current_app.config.setdefault('AUDIT_LOG', [])
    audit.append({'action': 'upload', 'file': filename})
    return jsonify({'saved': filename}), 201

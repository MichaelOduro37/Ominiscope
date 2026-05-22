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
    # Authorization: if RBAC is enabled and not TESTING, require a valid API key
    if current_app.config.get('RBAC_ENABLED', False) and not current_app.config.get('TESTING', False):
        # prefer API key header; legacy X-Role Technician allowed for backward compatibility
        api_key = request.headers.get('X-API-Key')
        expected = current_app.config.get('UPLOAD_API_KEY')
        if expected:
            # support comma-separated keys
            valid_keys = [k.strip() for k in expected.split(',') if k.strip()]
            if not api_key or api_key not in valid_keys:
                return jsonify({'error': 'forbidden'}), 403
        else:
            # fallback: allow only Technician role when no API key configured
            role = request.headers.get('X-Role', '')
            if role != 'Technician':
                return jsonify({'error': 'forbidden'}), 403

    # quick size check from the request headers when available
    max_bytes = current_app.config.get('UPLOAD_MAX_BYTES')
    if request.content_length and max_bytes and request.content_length > max_bytes:
        return jsonify({'error': 'payload too large'}), 413

    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400
    filename = secure_filename(f.filename)
    # basic content type and extension restrictions
    allowed_mimes = current_app.config.get('UPLOAD_ALLOWED_MIMETYPES')
    allowed_exts = current_app.config.get('UPLOAD_ALLOWED_EXTENSIONS')
    if allowed_mimes and (f.mimetype and f.mimetype not in allowed_mimes):
        return jsonify({'error': 'unsupported media type'}), 415
    if allowed_exts:
        _, ext = os.path.splitext(filename)
        if ext and ext.lower() not in allowed_exts:
            return jsonify({'error': 'unsupported file extension'}), 415

    d = upload_dir()
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, filename)
    f.save(path)
    # post-save size enforcement (in case request.content_length was not present)
    try:
        if max_bytes and os.path.getsize(path) > max_bytes:
            os.remove(path)
            return jsonify({'error': 'file too large'}), 413
    except OSError:
        # if we can't stat/remove, signal server error
        return jsonify({'error': 'internal error'}), 500
    # simple audit
    audit = current_app.config.setdefault('AUDIT_LOG', [])
    audit.append({'action': 'upload', 'file': filename})
    return jsonify({'saved': filename}), 201

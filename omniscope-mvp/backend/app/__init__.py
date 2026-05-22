import os
from flask import Flask


def create_app(config=None):
    """Create and configure the Flask application.

    Accepts an optional config dict which will override defaults (used by tests).
    """
    app = Flask(__name__)

    # sensible default upload directory (project-level `uploads/`)
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    default_upload = os.path.join(base, 'uploads')
    app.config.setdefault('UPLOAD_DIR', default_upload)
    # RBAC: disabled by default for local/dev; enable in production/CI by setting this
    app.config.setdefault('RBAC_ENABLED', False)

    # apply test/override config
    if config:
        app.config.update(config)

    # register blueprints
    try:
        from .api.routes.ingestion import ingestion_bp, list_files, get_file, upload_file
        app.register_blueprint(ingestion_bp)

        # lightweight job queue for orchestration stubs (in-memory for now)
        app.jobs = []

        # register aura blueprint (orchestration stub)
        from .api.routes.aura import aura_bp, plan, process_next, job_status
        app.register_blueprint(aura_bp)
        app.job_results = {}

        # Add API v1 aliases so both `/ingest/*` and `/api/v1/ingestion/*` work
        app.add_url_rule('/api/v1/ingestion/files', 'ingestion.list_files_v1', list_files, methods=['GET'])
        app.add_url_rule('/api/v1/ingestion/files/<path:filename>', 'ingestion.get_file_v1', get_file, methods=['GET'])
        app.add_url_rule('/api/v1/ingestion/upload', 'ingestion.upload_file_v1', upload_file, methods=['POST'])
        app.add_url_rule('/api/v1/aura/plan', 'aura.plan_v1', plan, methods=['POST'])
        app.add_url_rule('/api/v1/aura/process', 'aura.process_v1', process_next, methods=['POST'])
        app.add_url_rule('/api/v1/aura/jobs/<job_id>', 'aura.job_status_v1', job_status, methods=['GET'])
    except Exception:
        # allow import errors to surface during testing/runtime
        raise

    return app

import os
from typing import Mapping

from flask import Flask


def create_app(config: Mapping[str, object] | None = None):
    """Create and configure the Flask application.

    Accepts an optional config dict which will override defaults (used by tests).
    """
    app = Flask(__name__)

    config_overrides = dict(config or {})

    # sensible default upload directory (project-level `uploads/`)
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    default_upload = os.path.join(base, "uploads")
    app.config["UPLOAD_DIR"] = config_overrides.get("UPLOAD_DIR", default_upload)
    # RBAC: disabled by default for local/dev; enable in production/CI by setting this
    app.config["RBAC_ENABLED"] = config_overrides.get("RBAC_ENABLED", False)
    # simple API key for upload endpoints (list or comma-separated keys)
    app.config["UPLOAD_API_KEY"] = config_overrides.get("UPLOAD_API_KEY", None)
    # upload hardening defaults
    app.config["UPLOAD_MAX_BYTES"] = config_overrides.get(
        "UPLOAD_MAX_BYTES", 10 * 1024 * 1024
    )
    app.config["UPLOAD_ALLOWED_MIMETYPES"] = config_overrides.get(
        "UPLOAD_ALLOWED_MIMETYPES",
        [
            "text/plain",
            "application/json",
            "text/csv",
            "application/octet-stream",
        ],
    )
    app.config["UPLOAD_ALLOWED_EXTENSIONS"] = config_overrides.get(
        "UPLOAD_ALLOWED_EXTENSIONS",
        [".txt", ".csv", ".json"],
    )
    app.config["UPLOAD_JWT_SECRET"] = config_overrides.get("UPLOAD_JWT_SECRET", None)
    app.config["UPLOAD_JWT_JWKS_URL"] = config_overrides.get(
        "UPLOAD_JWT_JWKS_URL", None
    )
    app.config["UPLOAD_JWT_AUDIENCE"] = config_overrides.get(
        "UPLOAD_JWT_AUDIENCE", None
    )
    # register blueprints
    from .api.routes.ingestion import (
        ingestion_bp,
        list_files,
        get_file,
        upload_file,
    )

    app.register_blueprint(ingestion_bp)

    # Use an in-memory store for tests, otherwise persist jobs in SQLite.
    from .core.job_store import JobStore

    is_testing = bool(config_overrides.get("TESTING", False))
    job_db_override = config_overrides.get("JOB_DB")
    if isinstance(job_db_override, str) and job_db_override:
        db_path = job_db_override
    else:
        os.makedirs(app.instance_path, exist_ok=True)
        db_path = os.path.join(app.instance_path, "jobs-test.db" if is_testing else "jobs.db")

    job_store = JobStore(db_path)
    app.extensions["job_store"] = job_store

    def close_job_store(_exception: BaseException | None = None) -> None:
        store = app.extensions.get("job_store")
        if store is not None:
            store.close()

    app.teardown_appcontext(close_job_store)

    # register aura blueprint (orchestration uses job_store)
    from .api.routes.aura import aura_bp, plan, process_next, job_status

    app.register_blueprint(aura_bp)

    # register auth/token issuer blueprint
    from .api.routes.auth import auth_bp, issue_token

    app.register_blueprint(auth_bp)
    app.add_url_rule(
        "/api/v1/auth/token",
        "auth.issue_token_v1",
        issue_token,
        methods=["POST"],
    )

    # Add API v1 aliases so both `/ingest/*` and `/api/v1/ingestion/*` work
    app.add_url_rule(
        "/api/v1/ingestion/files",
        "ingestion.list_files_v1",
        list_files,
        methods=["GET"],
    )
    app.add_url_rule(
        "/api/v1/ingestion/files/<path:filename>",
        "ingestion.get_file_v1",
        get_file,
        methods=["GET"],
    )
    app.add_url_rule(
        "/api/v1/ingestion/upload",
        "ingestion.upload_file_v1",
        upload_file,
        methods=["POST"],
    )
    app.add_url_rule("/api/v1/aura/plan", "aura.plan_v1", plan, methods=["POST"])
    app.add_url_rule(
        "/api/v1/aura/process", "aura.process_v1", process_next, methods=["POST"]
    )
    app.add_url_rule(
        "/api/v1/aura/jobs/<job_id>",
        "aura.job_status_v1",
        job_status,
        methods=["GET"],
    )
    return app

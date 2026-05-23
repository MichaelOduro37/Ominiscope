import os
from flask import Flask


def create_app(config=None):
    """Create and configure the Flask application.

    Accepts an optional config dict which will override defaults (used by tests).
    """
    app = Flask(__name__)

    # sensible default upload directory (project-level `uploads/`)
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    default_upload = os.path.join(base, "uploads")
    app.config.setdefault("UPLOAD_DIR", default_upload)
    # RBAC: disabled by default for local/dev; enable in production/CI by setting this
    app.config.setdefault("RBAC_ENABLED", False)
    # simple API key for upload endpoints (list or comma-separated keys)
    app.config.setdefault("UPLOAD_API_KEY", None)
    # upload hardening defaults
    app.config.setdefault("UPLOAD_MAX_BYTES", 10 * 1024 * 1024)
    app.config.setdefault(
        "UPLOAD_ALLOWED_MIMETYPES",
        [
            "text/plain",
            "application/json",
            "text/csv",
            "application/octet-stream",
        ],
    )
    app.config.setdefault(
        "UPLOAD_ALLOWED_EXTENSIONS",
        [".txt", ".csv", ".json"],
    )

    # apply test/override config
    if config:
        app.config.update(config)

    # register blueprints
    try:
        from .api.routes.ingestion import (
            ingestion_bp,
            list_files,
            get_file,
            upload_file,
        )

        app.register_blueprint(ingestion_bp)

        # Use an in-memory store for tests, otherwise persist jobs in SQLite.
        from .core.job_store import JobStore

        db_path = app.config.get("JOB_DB")
        if not db_path:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            data_dir = os.path.join(base, "data")
            os.makedirs(data_dir, exist_ok=True)
            db_path = os.path.join(data_dir, "jobs.db")

        if app.config.get("TESTING", False):
            app.job_store = JobStore(":memory:")
        else:
            app.job_store = JobStore(db_path)

        # register aura blueprint (orchestration uses job_store)
        from .api.routes.aura import aura_bp, plan, process_next, job_status

        app.register_blueprint(aura_bp)

        # register auth/token issuer blueprint
        try:
            from .api.routes.auth import auth_bp, issue_token

            app.register_blueprint(auth_bp)
            app.add_url_rule(
                "/api/v1/auth/token",
                "auth.issue_token_v1",
                issue_token,
                methods=["POST"],
            )
        except Exception:
            # token issuer optional; surface errors normally
            raise

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
    except Exception:
        # allow import errors to surface during testing/runtime
        raise

    return app

import uuid
from flask import Response
from flask import Blueprint, request, jsonify, current_app

aura_bp = Blueprint("aura", __name__)


def _get_job_store():
    return current_app.extensions.get("job_store")


@aura_bp.route("/aura/plan", methods=["POST"])
def plan() -> tuple[Response, int]:
    """Accept an orchestration plan request and enqueue a lightweight job.

    Returns a job id and queued status. This is a test-friendly stub used by
    acceptance tests and early integration work.
    """
    payload = request.get_json(silent=True) or {}
    job_id = uuid.uuid4().hex
    # persist into the job store when available
    store = _get_job_store()
    if store:
        job_id = store.enqueue(payload)
        return jsonify({"job_id": job_id, "status": "queued"}), 201

    # fallback to non-persistent in-memory queue
    job = {"id": job_id, "payload": payload, "status": "queued"}
    try:
        current_app.jobs.append(job)
    except Exception:
        current_app.jobs = [job]
    return jsonify({"job_id": job_id, "status": "queued"}), 201


@aura_bp.route("/aura/process", methods=["POST"])
def process_next() -> tuple[Response, int] | tuple[str, int]:
    """Process the next queued job synchronously (test stub).

    Pops the first queued job, simulates processing, and stores a result
    in `current_app.job_results` keyed by job id.
    """
    # If a job store is configured, use it to process the next queued job
    store = _get_job_store()
    if store:
        result = store.process_next()
        if result is None:
            return "", 204
        resp = jsonify(
            {
                "job_id": result.get("job_id"),
                "status": "done",
                "result": result,
            }
        )
        return resp, 200

    # fallback to in-memory processing
    jobs = getattr(current_app, "jobs", [])
    if not jobs:
        return "", 204

    job = jobs.pop(0)
    job_id = job["id"]
    job["status"] = "processing"

    # simulate generation of a result (mock findings)
    count = len(job.get("payload", {}).get("inputs", []))
    summary = f"Processed {count} inputs"
    result = {
        "job_id": job_id,
        "summary": summary,
        "findings": [
            {
                "engine_id": "mock-engine-1",
                "confidence": 0.92,
                "output": "sample finding",
            }
        ],
    }

    # store results on the app for retrieval
    results = getattr(current_app, "job_results", None)
    if results is None:
        current_app.job_results = {}
        results = current_app.job_results
    results[job_id] = {"status": "done", "result": result}

    job["status"] = "done"
    return jsonify({"job_id": job_id, "status": "done", "result": result}), 200


@aura_bp.route("/aura/jobs/<job_id>", methods=["GET"])
def job_status(job_id: str) -> tuple[Response, int]:
    store = _get_job_store()
    if store:
        res = store.get_job(job_id)
        if res is None:
            return jsonify({"message": "job not found"}), 404
        return jsonify(res), 200

    results = getattr(current_app, "job_results", {})
    if job_id not in results:
        return jsonify({"message": "job not found"}), 404
    return jsonify(results[job_id]), 200

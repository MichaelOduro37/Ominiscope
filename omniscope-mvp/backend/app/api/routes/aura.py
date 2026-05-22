import uuid
from flask import Blueprint, request, jsonify, current_app

aura_bp = Blueprint('aura', __name__)


@aura_bp.route('/aura/plan', methods=['POST'])
def plan():
    """Accept an orchestration plan request and enqueue a lightweight job.

    Returns a job id and queued status. This is a test-friendly stub used by
    acceptance tests and early integration work.
    """
    payload = request.get_json(silent=True) or {}
    job_id = uuid.uuid4().hex
    job = {'id': job_id, 'payload': payload, 'status': 'queued'}

    # append to in-memory job list on the app (if present)
    try:
        current_app.jobs.append(job)
    except Exception:
        # ensure safe failure in environments without jobs list
        current_app.jobs = [job]

    return jsonify({'job_id': job_id, 'status': 'queued'}), 201


@aura_bp.route('/aura/process', methods=['POST'])
def process_next():
    """Process the next queued job synchronously (test stub).

    Pops the first queued job, simulates processing, and stores a result
    in `current_app.job_results` keyed by job id.
    """
    # find next queued job
    jobs = getattr(current_app, 'jobs', [])
    if not jobs:
        return jsonify({'message': 'no jobs queued'}), 204

    job = jobs.pop(0)
    job_id = job['id']
    job['status'] = 'processing'

    # simulate generation of a result (mock findings)
    result = {
        'job_id': job_id,
        'summary': f"Processed {len(job.get('payload', {}).get('inputs', []))} inputs",
        'findings': [
            {'engine_id': 'mock-engine-1', 'confidence': 0.92, 'output': 'sample finding'}
        ],
    }

    # store results on the app for retrieval
    results = getattr(current_app, 'job_results', None)
    if results is None:
        current_app.job_results = {}
        results = current_app.job_results
    results[job_id] = {'status': 'done', 'result': result}

    job['status'] = 'done'
    return jsonify({'job_id': job_id, 'status': 'done', 'result': result}), 200


@aura_bp.route('/aura/jobs/<job_id>', methods=['GET'])
def job_status(job_id):
    results = getattr(current_app, 'job_results', {})
    if job_id not in results:
        return jsonify({'message': 'job not found'}), 404
    return jsonify(results[job_id]), 200

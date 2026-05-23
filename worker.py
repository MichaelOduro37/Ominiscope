import time
from app import create_app


def run_worker(poll_interval: float = 2.0):
    """Run a simple in-process worker that polls the JobStore and processes jobs.

    This is intentionally lightweight for development/testing. For production
    use a dedicated worker system (RQ, Celery, or a Kubernetes Job).
    """
    app = create_app()

    # If job_store is not configured (very small dev setups) just return.
    if not hasattr(app, "job_store") or app.job_store is None:
        print("No job_store configured on app; stopping worker.")
        return

    print("Starting job worker (press Ctrl+C to stop)...")
    try:
        while True:
            result = app.job_store.process_next()
            if result is None:
                time.sleep(poll_interval)
            else:
                # In a real worker you would send notifications or persist
                # additional telemetry. Keep this simple for dev.
                print("Processed job:", result.get("job_id"))
    except KeyboardInterrupt:
        print("Worker stopped by user")


if __name__ == "__main__":
    run_worker()

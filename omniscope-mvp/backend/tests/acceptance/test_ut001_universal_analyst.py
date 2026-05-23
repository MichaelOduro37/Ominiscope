from app import create_app


def test_ut001_universal_analyst(tmp_path):
    # Placeholder acceptance test for UT-001 that ensures the ingestion files exist
    upload_dir = str(tmp_path)
    # seed sample files
    p1 = tmp_path / "deepseek_text_20260521_3388f9.txt"
    p1.write_text("sample instrument data")
    p2 = tmp_path / "deepseek_text_20260521_6c4295.txt"
    p2.write_text("threat letter")
    p3 = tmp_path / "deepseek_text_20260521_1f9965.txt"
    p3.write_text("supplier table")

    app = create_app({"TESTING": True, "UPLOAD_DIR": upload_dir})
    client = app.test_client()

    rv = client.get("/ingest/files")
    assert rv.status_code == 200
    data = rv.get_json()
    assert "deepseek_text_20260521_3388f9.txt" in data.get("files", [])

    # exercise orchestration stub
    plan_payload = {
        "query": "synthesize report",
        "inputs": ["deepseek_text_20260521_3388f9.txt"],
    }
    rv2 = client.post("/api/v1/aura/plan", json=plan_payload)
    assert rv2.status_code == 201
    j = rv2.get_json()
    assert "job_id" in j and j.get("status") == "queued"
    job_id = j["job_id"]

    # process queued job synchronously via test stub
    rv3 = client.post("/api/v1/aura/process")
    assert rv3.status_code == 200
    p = rv3.get_json()
    assert p.get("job_id") == job_id and p.get("status") == "done"

    # fetch job status/result
    rv4 = client.get(f"/api/v1/aura/jobs/{job_id}")
    assert rv4.status_code == 200
    js = rv4.get_json()
    assert js.get("status") == "done" and "result" in js

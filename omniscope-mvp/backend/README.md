# OmniScope Backend

Run the Flask backend and tests.

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run tests:

```powershell
cd omniscope-mvp/backend
python -m pytest -q
```

API endpoints (both supported):
- `/ingest/*`
- `/api/v1/ingestion/*`

RBAC (optional):
- To enable RBAC set `RBAC_ENABLED=True` in app config or production env.
- Uploads require header `X-Role: Technician` when RBAC is enabled.

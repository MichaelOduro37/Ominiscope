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

OIDC / JWKS (optional):
- To validate RS256 tokens via your IdP, set `UPLOAD_JWT_JWKS_URL` to the issuer's JWKS endpoint.
- Optionally set `UPLOAD_JWT_AUDIENCE` to require an audience claim for tokens.
- For development you can still use `UPLOAD_JWT_SECRET` (HS256) as a fallback.

Title: feat: aura orchestration + OIDC JWKS support, tests, CI

Summary
-------
This branch implements the initial Aura orchestration endpoints and improves upload security and test coverage. Key highlights:

- App factory and ingestion endpoints (upload/list/get) with upload hardening.
- Short-lived token issuer endpoint and optional OIDC JWKS verification (RS256) with HS256 fallback for dev.
- `JobStore` timezone fix and simple in-process worker for dev/testing.
- Extensive tests: unit tests for token issuer and upload flow, JWKS unit tests, and an RS256 integration test that spins up a local JWKS endpoint.
- CI workflow updated to install required deps (including `cryptography`) and run linters + tests.

Files changed (high level)
-------------------------
- `omniscope-mvp/backend/app/auth/oidc.py` — JWKS verifier helper (caching, RS256).
- `omniscope-mvp/backend/app/api/routes/ingestion.py` — prefer JWKS verification via `UPLOAD_JWT_JWKS_URL`, fall back to `UPLOAD_JWT_SECRET`.
- `omniscope-mvp/backend/requirements.txt` — added `PyJWT`, `requests`, `cryptography` (for integration test).
- `omniscope-mvp/backend/tests/*` — new unit + integration tests for JWKS/JWT flows.
- `.github/workflows/ci.yml` — consolidated CI job that installs deps and runs linters and pytest.
- `omniscope-mvp/backend/README.md` — documented `UPLOAD_JWT_JWKS_URL` and `UPLOAD_JWT_AUDIENCE` config.

Testing
-------
All backend tests pass locally (including the new integration test):

```
cd omniscope-mvp/backend
python -m pytest -q
```

Notes for reviewers
------------------
- The JWKS verifier uses an in-memory cache with a short TTL; for production consider replacing it with a robust cache or library that supports rotation and backoff.
- The integration test generates an RSA key at test time and serves a lightweight local JWKS endpoint — CI installs `cryptography` so the test will run there.
- For production, configure `UPLOAD_JWT_JWKS_URL` and `UPLOAD_JWT_AUDIENCE` and enable `RBAC_ENABLED=True` as needed.

Suggested PR body updates
-------------------------
Please paste the contents of this file into the PR body on GitHub or replace the existing description for clarity. If you want, I can also open/update the PR via `gh` if you provide a token or run the command locally.

Change-log / Commits
- Multiple focused commits on `feat/aura-orchestration` implementing features and tests.

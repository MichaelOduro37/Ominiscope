PR Checklist — feat/aura-orchestration

Use this checklist when reviewing or finalizing the PR.

- [ ] Tests: all backend tests pass locally and in CI (`python -m pytest -q`).
- [ ] Linters: Black and flake8 are satisfied (CI runs `black --check` and `flake8`).
- [ ] Security: production `UPLOAD_JWT_JWKS_URL` and `UPLOAD_JWT_AUDIENCE` configured in environment; secrets are stored in the environment/secret manager (do not commit secrets).
- [ ] RBAC: enable `RBAC_ENABLED` in deployment when required; verify upload flow with API key and JWKS tokens.
- [ ] CI: `.github/workflows/ci.yml` updated to install `cryptography` so RS256 integration test runs in CI.
- [ ] Docs: `omniscope-mvp/backend/README.md` updated with JWKS/audience guidance.
- [ ] Review: confirm `JobStore` timezone fix and worker behavior align with production expectations (consider using RQ/Celery for production).
- [ ] Release notes: add a short note describing JWKS support, tests, and CI changes.

Copy/paste this checklist into the PR description or use it as a review guide.

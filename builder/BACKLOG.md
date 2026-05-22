# Backlog (Developer task breakdown)

- Ingestion
  - Implement and test `upload_assets` in `backend/app/api/routes/ingestion.py`.
  - Persist files to `upload_dir` configured in `backend/app/core/config.py`.
  - Add audit events via `record_audit_event`.

- UI
  - Wire `frontend/components/data/upload-ingestion-panel.tsx` to `frontend/lib/api.ts::uploadAndIngestFiles`.
  - Display ingest results and canonical assets.

- Planner & Orchestration
  - Add `/aura/plan` stub in backend; implement planner to return plan_steps, selected_engines, reasoning_summary, confidence.
  - Implement job queue and worker scaffolding.

- Engines
  - Add document extraction (attachments route + `app/services/extraction.py`).
  - Add mock spectral and stylometry engines for PoC.

- Governance & Security
  - Add prompt injection scanner (pre-process prompts).
  - Enforce `require_capability` checks and log audit events.

- Testing
  - Extend `backend/tests/test_api.py` for RBAC and Universal Analyst fixture.
  - Add CI job running engine regression datasets.

Each task should reference the files above and produce unit/integration tests.


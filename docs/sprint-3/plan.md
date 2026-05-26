# Sprint 3 Plan

Goal: wire the scaffolding into a minimal end-to-end flow.

Timebox: 2 weeks (adjustable).

Scope
- API to DB wiring for assets, versions, cubes, and pipelines.
- API to worker job submission and result handling.
- Web to API fetch stubs and health surface.
- Minimal end-to-end smoke path (ingest -> pipeline -> report stub).

Out of Scope
- Full ingestion pipelines and data extraction.
- Full auth and RBAC enforcement.
- Production-grade UI components.

Phases and Deliverables

Phase 0 - Integration plan
- Deliverables: interface contracts and sequence diagram.
- Acceptance: integration points defined and agreed.

Phase 1 - API to DB wiring
- Deliverables: CRUD stubs for assets, versions, cubes.
- Acceptance: endpoints persist to database.

Phase 2 - API to worker wiring
- Deliverables: enqueue jobs and capture results.
- Acceptance: pipeline status updates reflect worker output.

Phase 3 - Web to API wiring
- Deliverables: fetch health and list stubs.
- Acceptance: UI renders live data from API.

Phase 4 - Smoke path
- Deliverables: documented steps for a minimal ingest -> report run.
- Acceptance: end-to-end demo works locally.

Dependencies
- Decide local dev database and storage layout.

Checks
- Update docs and progress after each phase.

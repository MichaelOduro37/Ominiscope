# Sprint 2 Plan

Goal: ship the architecture skeleton and initial scaffolding for internal v1.

Timebox: 2 weeks (adjustable).

Scope
- Tech stack decision and system overview.
- Repository layout and baseline README.
- Backend API skeleton with health, auth placeholder, and core resources.
- Data model stubs for assets, versions, cubes, and pipelines.
- Basic job queue worker skeleton.
- Frontend shell with core routes and AURA workspace stub.

Out of Scope
- Full data ingestion implementation.
- Production auth integration and SSO.
- Full UI design system and charts.

Phases and Deliverables

Phase 0 - Architecture baseline
- Deliverables: system overview and stack decisions.
- Acceptance: core services and data stores defined.

Phase 1 - Backend skeleton
- Deliverables: FastAPI app, routing, health endpoint, stubs for AURA and ingestion.
- Acceptance: app runs and returns stub responses.

Phase 2 - Data model stubs
- Deliverables: SQLAlchemy models and migrations for core objects.
- Acceptance: migration runs with empty schema.

Phase 3 - Worker skeleton
- Deliverables: queue worker and job contracts.
- Acceptance: worker processes stub jobs.

Phase 4 - Frontend shell
- Deliverables: Vite React app with routes for Dashboard, AURA, Reports.
- Acceptance: navigation and placeholder pages render.

Dependencies
- Decide dev database and local object storage.

Checks
- Update docs and progress after each phase.

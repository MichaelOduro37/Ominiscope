# OMNISCOPE Consolidated Specification

Purpose:
Build OmniScope — web PWA + optional on‑prem OmniBridge agent that unifies ingestion, the canonical Data‑Cube, multi‑engine analysis, AURA orchestration, and governance.

Core components:
- Ingest: multipart uploads, OmniBridge instrument streams, APIs, email, legacy import.
- Data‑Cube: preserve raw payload, metadata, immutable provenance, and versioning.
- Engine Layer: sandboxed, chainable plugins (WASM/container).
- AURA: planner/orchestrator that selects engines, monitors runs, assembles confidence-scored reports with provenance.
- UI Workspace: chat/planner, upload panel, persisted assets, Dispute Panel for conflicts.
- Governance: zero‑trust access, dynamic masking/redaction, immutable audit ledger, adversarial input scanning.

Non-functional priorities:
- Security: zero‑trust, field-level encryption, prompt-injection defenses, RBAC capability checks.
- Observability: telemetry, job tracing, audit events.
- Extensibility: plugin marketplace, no-code pipeline builder, CI/regression with certified datasets.

References in repo:
- `backend/app/services/data_cube.py` (ingest & canonicalization)
- `backend/app/api/routes/ingestion.py` (upload endpoints)
- `backend/app/api/routes/attachments.py` (document extraction)
- `frontend/components/data/upload-ingestion-panel.tsx` (UI)

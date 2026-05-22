# Roadmap (high priority milestones)

M1 — Core ingest & Data‑Cube (2–4w)
- Implement multipart upload endpoint, persist files to `UPLOAD_DIR`.
- Canonicalize assets, save canonical records, record audit events.
- UI: `UploadIngestionPanel` connected to backend.

M2 — AURA planner & orchestration (3–6w)
- `/aura/plan` endpoint and planner service.
- Lightweight orchestrator, job queue, provenance capture.

M3 — Engines & Universal Analyst (3–8w)
- Document intelligence, stylometry, spectral engine, anomaly detection.
- Pass Universal Analyst Test.

M4 — Governance & security (2–4w)
- Dynamic masking, immutable audit ledger, prompt/injection scanner, RBAC enforcement.

M5 — Extensibility & marketplace (4–8w)
- Sandbox (WASM/container), plugin registry, no-code pipeline builder.

M6 — Scale & ops
- CI/regression harness, monitoring, on‑prem packaging, documented deployment.


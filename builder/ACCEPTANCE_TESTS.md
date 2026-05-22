# Acceptance Tests

UT-001 — Universal Analyst Test
- Setup: Incident with three assets:
  - `uploads/deepseek_text_20260521_3388f9.txt` (sample/instrument/spectrum)
  - `uploads/deepseek_text_20260521_6c4295.txt` (threat letter / text asset)
  - `uploads/deepseek_text_20260521_1f9965.txt` (supplier / table)
- Action: Request AURA orchestration of the incident.
- Expect:
  - Combined report containing: spectral (XRD/MS) match, stylometry author cluster, supplier ordering anomaly.
  - Each finding includes: engine id, input asset refs, output, confidence score, and provenance chain.
  - If engines conflict, Dispute Panel shows both analyses and requires human resolution.
- Pass criteria: Report contains all three findings + provenance and confidence.

UT-002 — Upload & RBAC
- POST `/api/v1/ingestion/upload` with Viewer headers → 403.
- Same POST with Technician headers → 200 and files persisted to `UPLOAD_DIR`.

UT-003 — Document Extraction
- POST `/api/v1/attachments/extractions` with base64 content → extracted entities, keywords, risk_terms, stored artifact.

UT-004 — Adversarial Input Handling
- Submit prompt with injection patterns → request blocked/quarantined with logged audit event.

UT-005 — Engine Regression
- For each engine, run certified test dataset and assert metrics above threshold in CI.


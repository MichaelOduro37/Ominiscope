# OmniScope System Overview (v1)

## 1. Stack Decisions
- Backend: Python 3.12, FastAPI, Uvicorn
- ORM and migrations: SQLAlchemy + Alembic
- Database: Postgres (metadata, audit, pipelines)
- Object storage: local filesystem in dev, S3-compatible in prod
- Queue: Redis + RQ for background jobs
- Frontend: React + Vite + TypeScript

## 2. Core Services
- api: request handling, auth placeholder, AURA orchestration endpoints
- worker: background jobs and engine execution
- web: PWA frontend

## 3. Data Stores
- postgres: assets, versions, cubes, pipeline runs, audits
- object storage: raw payloads and derived artifacts
- cache: redis for queues and rate limiting

## 4. Directory Layout (target)
- apps/api
- apps/worker
- apps/web
- docs/
- uploads/

## 5. Security Baseline
- RBAC and ABAC enforced at API layer.
- Audit event logging for all access and execution.
- Sandbox policy for engines.

## 6. Next Implementation Steps
- Scaffold api service with core routes and models.
- Add worker job contracts.
- Add frontend shell and routing.

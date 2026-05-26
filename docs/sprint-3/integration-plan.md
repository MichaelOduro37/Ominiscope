# Sprint 3 Integration Plan

## 1. Interfaces

### 1.1 Web -> API
- GET /health
- POST /ingestion/ingest
- POST /aura/orchestrations
- GET /assets
- GET /pipelines/{id}

### 1.2 API -> DB
- data_assets
- data_versions
- data_cubes
- pipeline_runs

### 1.3 API -> Worker
- enqueue ingest job
- enqueue pipeline job
- consume job results

## 2. Sequence (Minimal End-to-End)

1) Web triggers ingest
2) API validates and stores asset + version
3) API enqueues ingest job
4) Worker returns job result
5) API updates pipeline run
6) Web fetches updated status

## 3. Contracts

- IngestRequest: name, source_type, metadata
- OrchestrationRequest: request_id, user_id, goal, context
- JobResult: status, payload

## 4. Error Handling
- API returns 400 on validation errors
- API returns 503 if worker unavailable
- Worker retries on transient errors

## 5. Observability
- trace_id for every API request
- job_id in worker logs
- pipeline_id propagated end-to-end

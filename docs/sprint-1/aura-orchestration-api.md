# AURA Orchestration API (v1)

This document defines the internal API for AURA orchestration, including request and response contracts, pipeline lifecycle, and error model.

## 1. Purpose
AURA turns a user goal into a validated, auditable pipeline that produces evidence-backed outputs. The API ensures every run emits provenance and audit events and respects policy constraints.

## 2. API Style
- Internal JSON API over HTTPS (REST-style).
- Async pipeline execution with event stream for status updates.
- Idempotent submission using client request IDs.

## 3. Core Concepts
- Goal: natural language or structured intent.
- Pipeline: ordered steps, dependencies, and resource budgets.
- Step: an action bound to an engine and inputs.
- Artifact: a stored result (DataCube, chart, report, model).
- Decision: human approval or dispute resolution outcome.

## 4. Request Contract

### 4.1 Create Orchestration
POST /aura/orchestrations

Fields:
- request_id (string, required)
- user_id (string, required)
- goal (string, required)
- context (object, optional)
  - data_refs[] (asset_id, version_id, cube_id)
  - constraints (time_window, region, budget)
  - persona (exec, analyst, operator)
  - risk_level (low, medium, high)
- output_spec (object, optional)
  - report_format (brief, full, notebook)
  - artifacts[] (chart, table, model, dashboard)
  - citations (required, optional)
- policy (object, optional)
  - approval_required (true, false)
  - masking_policy_id
  - retention_policy_id

## 5. Response Contract

### 5.1 Create Orchestration Response
Fields:
- orchestration_id
- pipeline_id
- status (queued, running, blocked, completed, failed, cancelled)
- next_action (none, await_approval, provide_data, resolve_dispute)
- warnings[]
- trace_id

### 5.2 Pipeline Result
GET /aura/pipelines/{pipeline_id}

Fields:
- pipeline_id
- status
- steps[]
  - step_id
  - step_type
  - engine_id
  - status
  - inputs[]
  - outputs[]
  - started_at
  - ended_at
- artifacts[]
- findings[]
  - claim
  - confidence
  - evidence_ids[]
  - assumptions[]
- provenance_event_ids[]
- audit_event_ids[]

## 6. Pipeline Lifecycle

States:
- queued -> running -> completed
- queued -> cancelled
- running -> blocked (await approval or data)
- running -> failed

Transitions:
- blocked -> running after approval or data provided
- failed -> running only with explicit retry

Step Status:
- pending, running, skipped, failed, completed

## 7. Step Types
- ingest
- extract
- transform
- analyze
- validate
- report
- export

## 8. Approval Gates
- High-risk actions require explicit approval.
- Approval results in a Decision object linked to the pipeline.
- Disputes create a blocked state until resolved.

## 9. Error Model

Error object:
- code
- message
- category
- details
- trace_id

Categories:
- validation_error
- policy_denied
- data_not_found
- engine_unavailable
- timeout
- resource_limit
- dependency_failure
- conflict_detected

## 10. Observability
- Every request emits a trace_id.
- ProvenanceEvent and AuditEvent IDs are returned in results.
- Metrics: pipeline latency, engine utilization, error rates.

## 11. Security and Policy Enforcement
- RBAC and ABAC enforced on all data refs.
- Sensitive data is masked based on policy.
- Output artifacts inherit the highest sensitivity of inputs.

## 12. Example

Request:
```json
{
  "request_id": "req_01HXYZ",
  "user_id": "u_123",
  "goal": "Find root cause of vibration spike in turbine A",
  "context": {
    "data_refs": [{"asset_id": "a_1001", "version_id": "v3"}],
    "risk_level": "medium",
    "persona": "analyst"
  },
  "output_spec": {
    "report_format": "full",
    "artifacts": ["chart", "table"],
    "citations": "required"
  },
  "policy": {
    "approval_required": false
  }
}
```

Response:
```json
{
  "orchestration_id": "o_2001",
  "pipeline_id": "p_3001",
  "status": "queued",
  "next_action": "none",
  "warnings": [],
  "trace_id": "t_9001"
}
```

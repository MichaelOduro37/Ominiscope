# Security Baseline (RBAC/ABAC and Audit Events) v1

This document defines the minimum access control and audit requirements for internal v1.

## 1. RBAC Roles (v1)

- Admin: full system control, policy management, and audit access.
- Security: audit review, incident response, policy approval.
- Executive: read access to dashboards and approved reports.
- Analyst: read/write for pipelines, reports, and datasets within scope.
- Operator: limited read/write for assigned workflows and capture.
- Viewer: read-only access to approved reports.
- Service: automation accounts with scoped API access.

## 2. ABAC Attributes (v1)

User attributes:
- department
- role
- clearance_level (low, medium, high)
- region
- project_id
- device_trust_level

Data attributes:
- sensitivity (public, internal, restricted, regulated)
- classification (pii, phi, ip, export_controlled)
- owner_department
- retention_policy_id
- legal_hold

Policy examples:
- Only users with clearance_level >= data.sensitivity can access.
- Users can access data only within their project_id unless Admin.
- Regulated data requires Security approval for export.
- Access from untrusted devices is read-only and masked.

## 3. Access Matrix (Summary)

- Admin: all actions on all resources.
- Security: read all, approve exports, read audit logs.
- Executive: read dashboards and approved reports only.
- Analyst: create/run pipelines, edit reports, access datasets in scope.
- Operator: execute assigned workflows, submit captures.
- Viewer: read approved reports only.
- Service: scoped read/write for approved automation tasks.

## 4. Approval Gates

- High-risk analyses (risk_level = high) require Security approval.
- Exports of regulated data require dual approval (Security + Admin).
- Plugin installation requires Admin approval.
- Autonomous actions can be paused by Admin or Security.

## 5. Audit Events (Minimum)

- auth.login
- auth.logout
- auth.failed_login
- data.ingest
- data.access
- data.export
- data.masking_apply
- pipeline.create
- pipeline.run
- pipeline.fail
- report.create
- report.approve
- report.export
- policy.change
- plugin.install
- plugin.update
- user.role_change
- system.pause_aura

## 6. Data Masking Rules

- PII/PHI fields masked by default for non-privileged roles.
- Partial reveal requires explicit approval.
- Masking decisions logged as audit events.
- Outputs inherit the highest input sensitivity.

## 7. Incident Response Triggers

- Unauthorized access attempt.
- Repeated policy violations.
- Suspicious export patterns.
- Engine sandbox violation.

## 8. Retention

- Audit logs retained for 3 years by default.
- Regulated data audit logs retained for 7 years.

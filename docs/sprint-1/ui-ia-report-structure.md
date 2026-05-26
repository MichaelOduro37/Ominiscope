# UI IA and Report Structure (v1)

This document defines the information architecture and the standard report structure for internal v1.

## 1. IA Map (Top-Level)

- Home Dashboard
- Data Catalog
- Analysis Workspace (AURA)
- Pipelines
- Reports
- Knowledge Graph
- Tasks and Approvals
- Admin and Governance
- Plugin Manager
- Templates Library

## 2. Core Screens

### 2.1 Home Dashboard
- Role-based landing view (exec, analyst, operator, admin).
- Key insights, active pipelines, and flagged decisions.

### 2.2 Data Catalog
- Browse assets, versions, and cubes.
- Filters by domain, sensitivity, owner, and tags.
- Quick preview of metadata and provenance.

### 2.3 Analysis Workspace (AURA)
- Prompt area with context attachments.
- Generated pipeline preview with editable steps.
- Live run status and artifacts panel.

### 2.4 Pipelines
- List of pipeline runs with status and owners.
- Step-level logs and provenance trace.
- Retry and versioning controls.

### 2.5 Reports
- Report list with audit and approval state.
- Structured report viewer and export options.

### 2.6 Knowledge Graph
- Entity explorer with relationship view.
- Evidence links to assets and reports.

### 2.7 Tasks and Approvals
- Review queue for human approvals.
- Dispute panel for conflicting results.

### 2.8 Admin and Governance
- RBAC and ABAC policy editor.
- Audit log and compliance controls.

### 2.9 Plugin Manager
- Installed engines, versions, and health status.
- Enable, disable, and update controls.

### 2.10 Templates Library
- Reusable pipeline templates and report blueprints.

## 3. Navigation Model
- Left nav for primary sections.
- Contextual right panel for details, artifacts, and evidence.
- Global search for assets, entities, and reports.

## 4. Role-Based Views

Exec:
- KPI dashboard, decision briefs, and risk alerts.

Analyst:
- Data catalog, pipelines, reports, and AURA.

Operator:
- Guided workflows, offline capture, and checklists.

Admin:
- Governance, audit, and system health.

## 5. Standard Report Structure

1) Executive Summary
- Question, answer, and decision recommendation.

2) Scope and Context
- Inputs, constraints, and assumptions.

3) Data and Evidence
- Data sources, versions, and provenance.

4) Methodology
- Pipeline steps, engines, and parameters.

5) Findings
- Claims with confidence and evidence links.

6) Risks and Uncertainties
- Known gaps, conflicts, and sensitivity notes.

7) Actions and Approvals
- Required approvals, action items, and owners.

8) Appendices
- Raw outputs, charts, logs, and audit references.

## 6. Key User Journeys

- Ask a question -> attach data -> review pipeline -> run -> approve -> report.
- Ingest a dataset -> auto-cube -> link entities -> explore -> report.
- Resolve conflict -> dispute panel -> human decision -> audit log.

## 7. Accessibility and Mobile
- WCAG 2.2 AA compliance targets.
- Mobile capture for field workflows with offline sync.

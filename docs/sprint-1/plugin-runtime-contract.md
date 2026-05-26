# Plugin Runtime Contract and Sandbox Policy (v1)

This document defines how analysis engines are packaged, validated, executed, and audited in OmniScope. The contract supports internal domain packs and third-party extensions while preserving security and reproducibility.

## 1. Scope and Goals
- Provide a stable engine interface for all domain packs.
- Enforce sandbox isolation and least-privilege data access.
- Capture provenance, audit, and reproducibility for every run.
- Allow phased expansion from internal to external plugins.

## 2. Engine Package Structure

Required files:
- manifest.json
- engine.wasm or container image reference
- schema.json (input and output contract)
- README.md (usage and assumptions)

Optional:
- tests/ (reference fixtures)
- benchmarks/ (performance baselines)

## 3. Manifest Contract (manifest.json)

Fields:
- id (string)
- name (string)
- version (semver)
- runtime (wasm, container)
- entrypoint
- description
- owner (team or vendor)
- capabilities[] (analysis, transform, validate, visualize)
- inputs[] (data cube types supported)
- outputs[] (artifact types)
- resource_profile (cpu, memory_mb, gpu, timeout_sec)
- network_policy (none, allowlist)
- storage_policy (ephemeral, workspace)
- data_access (read_only, read_write)
- compatibility (omniscope_min_version)

## 4. Input and Output Contract

Inputs:
- data_refs[] (asset_id, version_id, cube_id)
- parameters (engine-specific)
- policies (masking, retention)

Outputs:
- artifacts[] (DataCube, report, chart, model)
- findings[] (claim, confidence, evidence_ids[])
- provenance_event_id
- audit_event_id

## 5. Execution Lifecycle

1) Validate manifest and schema.
2) Resolve data refs and apply masking.
3) Stage inputs to sandboxed workspace.
4) Execute engine with resource limits.
5) Collect outputs and verify schema.
6) Store artifacts and emit provenance and audit events.
7) Cleanup sandbox and revoke temporary access.

## 6. Sandbox Policy

Isolation:
- WASM runs in a restricted runtime with no syscalls outside the approved API.
- Containers run in rootless mode with seccomp and read-only base images.

Network:
- Default deny.
- Allowlist only for approved data sources.

Filesystem:
- Ephemeral workspace only.
- No access to host filesystem or secrets.

Secrets:
- Never embedded in packages.
- Injected at runtime via vault references and short-lived tokens.

## 7. Resource Limits

Baseline limits (default):
- CPU: 2 cores
- Memory: 2 GB
- GPU: none
- Timeout: 15 minutes
- Disk: 5 GB ephemeral

Limits are overrideable by policy for trusted internal engines.

## 8. Security and Verification
- Code signing required for all packages.
- Static scanning for malware and unsafe calls.
- Regression tests must pass for internal engines.
- Compatibility checks block outdated engines.

## 9. Observability and Audit
- Every run emits a trace_id.
- Logs are scoped per engine and retained by policy.
- Metrics: runtime, error rates, resource usage.

## 10. Error Model
- validation_error
- policy_denied
- data_not_found
- sandbox_violation
- timeout
- resource_limit
- engine_failure

## 11. Example Manifest

```json
{
  "id": "engine.spectra.peakfit",
  "name": "Spectral Peak Fitter",
  "version": "1.0.0",
  "runtime": "wasm",
  "entrypoint": "peakfit",
  "description": "Peak fitting for IR and Raman spectra",
  "owner": "materials-lab",
  "capabilities": ["analysis"],
  "inputs": ["spectrum"],
  "outputs": ["table", "chart"],
  "resource_profile": {"cpu": 2, "memory_mb": 1024, "gpu": false, "timeout_sec": 300},
  "network_policy": "none",
  "storage_policy": "ephemeral",
  "data_access": "read_only",
  "compatibility": {"omniscope_min_version": "0.1.0"}
}
```

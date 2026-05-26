# OmniScope Data Cube Schema (v1)

This document defines the canonical data cube model, metadata dictionary, and ingestion flow for internal v1.

## 1. Canonical Model Overview
Every input becomes a versioned DataAsset and a DataCube representation. The raw payload is immutable and never overwritten. Derived cubes reference their provenance.

Key principles:
- Immutable raw data with versioning.
- Normalized units and coordinate systems.
- Provenance for every transformation.
- One schema for all modalities, extended by domain namespaces.

## 2. Core Objects

### 2.1 DataAsset
Represents a logical dataset across versions.
- id (ULID)
- name
- source_type (file, api, device, form, email)
- owner_id
- created_at
- tags[]
- sensitivity (public, internal, restricted, regulated)
- retention_policy_id

### 2.2 DataVersion
Represents an immutable snapshot of a DataAsset.
- id (ULID)
- asset_id
- version_label (v1, v2, etc.)
- checksum (sha256)
- size_bytes
- raw_uri
- created_at
- ingested_by
- mime_type
- format

### 2.3 DataCube
Canonical representation of a DataVersion.
- id (ULID)
- version_id
- cube_type (text, table, image, timeseries, spectrum, chromatogram, audio, video, mesh3d, sequence, document, json)
- shape[] (dimension sizes)
- axes[]
- channels[]
- storage_uri
- summary_stats
- created_at

### 2.4 Axis
Defines a dimension of the cube.
- name (time, x, y, z, wavelength, frequency, token, row, column, etc.)
- axis_type (temporal, spatial, spectral, categorical, sequence)
- unit
- coordinate_system
- range
- resolution

### 2.5 Channel
Defines a data channel within the cube.
- name (intensity, temperature, amplitude, value)
- data_type (float, int, bool, string, category)
- unit
- missing_value_rule
- stats (min, max, mean, std, count)

### 2.6 DataSlice
Optional optimized slice of a cube.
- id (ULID)
- cube_id
- axis_ranges
- slice_format
- storage_uri
- created_at

### 2.7 Entity
Knowledge graph node linked to assets and cubes.
- id (ULID)
- entity_type (material, person, asset, location, regulation, instrument)
- label
- attributes
- links[]

### 2.8 Relationship
Knowledge graph edge.
- id (ULID)
- subject_id
- predicate
- object_id
- confidence
- evidence_ids[]

### 2.9 Annotation
User or system note on any object.
- id (ULID)
- target_id
- author_id
- content
- annotation_type (note, decision, dispute, label)
- created_at

### 2.10 ProvenanceEvent
Captures all transformations.
- id (ULID)
- event_type (ingest, extract, transform, analyze, export)
- actor_id
- input_ids[]
- output_ids[]
- parameters
- started_at
- ended_at
- engine_id

### 2.11 AuditEvent
Security and compliance audit trail.
- id (ULID)
- actor_id
- action
- target_id
- policy_id
- timestamp
- ip_address

## 3. Metadata Dictionary (v1)

### 3.1 Identification
- asset_name
- asset_id
- version_id
- source_system
- source_uri

### 3.2 Temporal
- created_at
- captured_at
- updated_at
- timezone

### 3.3 Spatial
- latitude
- longitude
- altitude
- coordinate_system
- spatial_resolution

### 3.4 Instrument and Device
- instrument_vendor
- instrument_model
- instrument_serial
- calibration_date
- operator_id

### 3.5 Content and Format
- mime_type
- encoding
- format
- language
- schema_version

### 3.6 Units and Normalization
- unit_system (SI, imperial)
- unit_overrides
- normalization_applied

### 3.7 Quality
- completeness_score
- anomaly_flags[]
- validation_errors[]

### 3.8 Security and Compliance
- sensitivity
- data_classification
- masking_policy_id
- retention_policy_id
- legal_hold

### 3.9 Provenance
- source_type
- source_chain[]
- transform_history[]
- derived_from_ids[]

### 3.10 Domain Extensions
- domain.* (namespaced fields for domain packs)

## 4. Ingestion Flow (v1)

1) Register asset and owner context.
2) Capture raw payload and compute checksum.
3) Extract metadata and infer cube_type.
4) Normalize units and coordinate systems.
5) Create DataVersion and DataCube entries.
6) Generate initial Entity and Relationship nodes.
7) Apply policies: masking, retention, access checks.
8) Index for search and semantic retrieval.
9) Emit ProvenanceEvent and AuditEvent.

## 5. Validation and Quality Gates
- Schema validation for each cube_type.
- Unit consistency checks.
- Required metadata per sensitivity class.
- Anomaly detection (missing fields, unexpected ranges).

## 6. Versioning Rules
- Raw payload is immutable.
- Any change creates a new DataVersion.
- Derived cubes link to their inputs via ProvenanceEvent.

## 7. Notes for Phase 2
- AURA orchestration will use ProvenanceEvent and AuditEvent as first-class outputs.
- Domain packs can define domain.* extensions without changing core schema.

# OmniScope API (Skeleton)

This is the internal v1 backend skeleton for OmniScope.

## Run (dev)

1) Create a virtual environment and install dependencies.
2) Start the API:

```
python -m uvicorn app.main:app --reload
```

## Notes
- This is a stub API for Sprint 2 Phase 1.
- Endpoints return placeholder responses until the data layer is implemented.

## Migrations (stub)

Alembic files are included for the initial schema. Update the database URL in
`app/core/settings.py` before running migrations.

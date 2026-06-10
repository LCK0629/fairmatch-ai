# Version 2 Frontend Integration

## Architecture

```text
HTML/CSS/JS
      ↓
FastAPI
      ↓
FairMatch Backend
      ↓
OR-Tools Solver
```

The Version 2 frontend connects to the FastAPI wrapper and reuses the existing FairMatch backend. The solver, fairness logic, explanation logic, and optimisation objective remain unchanged.

## Localhost Serving

The Version 2 frontend is now served through localhost rather than opened directly with `file://`.

```text
Frontend: http://127.0.0.1:5500
API:      http://127.0.0.1:8000
```

`START_V2.bat` starts both services and opens the frontend URL in the default browser.

## Endpoints Used

### GET /health

Purpose:
Check whether the API is available.

Frontend use:
Displays `API Connected` or `API Offline` in the dashboard header.

### GET /samples

Purpose:
Load available sample datasets.

Frontend use:
Populates the dataset selector dynamically. The frontend does not hardcode dataset options.

### POST /allocate

Purpose:
Run allocation using the existing FairMatch backend.

Frontend use:
Updates:
- allocation overview cards
- allocation result table
- fairness metric cards
- explanation panel

### POST /compare-fairness

Purpose:
Compare `fairness_weight = 0` against a fairness-aware run.

Frontend use:
Updates:
- baseline metrics
- fairness-aware metrics
- changed assignments
- changed satisfaction
- warning message when applicable

## Frontend Data Flow

```text
Dataset
↓
API
↓
Solver
↓
Response
↓
Dashboard
```

The dashboard starts with static preview data. After a successful API response, the preview is replaced with real backend data.

## Error Handling Strategy

Handled failures:
- API unavailable
- health check failure
- sample loading failure
- no dataset selected
- invalid API response
- allocation error
- comparison error
- API validation error for invalid payloads

User-facing behaviour:
- The dashboard does not crash.
- A message panel displays clear status or error text.
- Static preview data remains visible until real backend data is available.

## Prototype CORS Note

The Version 2 FastAPI prototype currently uses permissive CORS settings:

```python
allow_origins=["*"]
```

This is acceptable for local portfolio prototyping, where the frontend is opened from local files and must call the local API server.

For production deployment, this should be restricted to trusted frontend origins.

## Current Limitations

- The frontend is still plain HTML/CSS/JS.
- No database is connected.
- No authentication is implemented.
- The dashboard currently uses sample datasets returned by the API.
- Custom upload support is not implemented in the Version 2 static frontend yet.

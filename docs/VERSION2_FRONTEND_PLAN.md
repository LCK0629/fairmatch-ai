# FairMatch AI Version 2 Frontend Plan

## Product Vision

FairMatch AI is an Explainable Fairness-Aware Allocation Platform.

Version 2 prepares the project for a professional product and portfolio frontend. The goal is to provide:

- Fair Allocation
- Transparent Decisions
- Counterfactual Analysis

through a polished web experience that feels like a real decision-support product rather than a student prototype.

Version 2 must reuse the existing FairMatch backend. The solver, fairness helpers, counterfactual logic, and explanation logic remain stable.

## Architecture

```text
Frontend (HTML/CSS/JS)
        ↓
FastAPI API Layer
        ↓
Existing FairMatch Backend
        ↓
OR-Tools Solver
```

The backend must be reused. Version 2 must not rewrite the solver or replace OR-Tools.

## Planned Pages

### 1. Landing Page

Purpose:
Introduce FairMatch AI as a product.

Content:
- Product hero
- Problem statement
- Product pillars
- Architecture summary
- Start action

### 2. Mode Selection

Purpose:
Let users choose the allocation context.

Modes:
- School Mode
- Work Mode (Coming Soon)

School Mode remains the active product path. Work Mode is a future extension and should be visually marked as unavailable or coming soon.

### 3. Dashboard

Purpose:
Provide the main decision-support workspace.

Sections:
- Overview
- Allocation
- Fairness
- Explanation
- Comparison

The dashboard should present results clearly without exposing internal debug details.

### 4. Future Work Page

Purpose:
Show the portfolio roadmap and planned extensions.

Content:
- Supervisor fairness
- Counterfactual workload comparison
- What-if simulation
- PDF report export
- Multi-user accounts

## Planned API Endpoints

### GET /health

Purpose:
Confirm that the API service is running.

Request:
No request body.

Response:

```json
{
  "status": "ok",
  "service": "FairMatch AI API"
}
```

### GET /samples

Purpose:
List available sample datasets for the frontend.

Request:
No request body.

Response:

```json
{
  "samples": [
    {
      "id": "school_sample",
      "name": "School Sample",
      "mode": "school"
    },
    {
      "id": "fairness_weight_tradeoff",
      "name": "Fairness Weight Trade-Off",
      "mode": "school"
    }
  ]
}
```

### POST /allocate

Purpose:
Run the existing allocation engine for a submitted allocation problem.

Request:
Allocation JSON using the existing FairMatch input schema.

Response:
Allocation result containing:
- solver status
- objective value
- assignments
- fairness metrics
- workload gap
- structured explanations

### POST /compare-fairness

Purpose:
Compare a baseline allocation against a fairness-aware allocation.

Request:
Allocation JSON plus a fairness-weight setting for the fairness-aware run.

Response:
Counterfactual comparison containing:
- baseline result
- fairness-aware result
- changed assignments
- total satisfaction comparison
- fairness gap comparison
- Gini coefficient comparison
- fairness improvement status

## UI Design Direction

Target references:
- Stripe
- Linear
- Notion
- OpenAI

Characteristics:
- Premium SaaS style
- Strong typography
- Large hero section
- Product-first messaging
- Clean cards
- Professional tables
- Minimal clutter
- Clear decision-support hierarchy

The interface should first explain why the product matters before asking the user to choose datasets or run allocation.

## Development Phases

### Phase 1: Static Landing Page

Create a static product landing page using HTML, CSS, and JavaScript.

Goal:
Establish the Version 2 visual identity and product story.

### Phase 2: FastAPI Wrapper

Create a lightweight API layer around the existing backend.

Goal:
Expose stable endpoints without changing the solver or optimisation logic.

### Phase 3: Frontend to API Connection

Connect the frontend to FastAPI endpoints.

Goal:
Allow the product frontend to run allocation and fairness comparison through the backend service.

### Phase 4: Dashboard Pages

Build the main dashboard pages for overview, allocation, fairness, explanations, and comparison.

Goal:
Replace the Streamlit demo experience with a portfolio-ready product interface.

### Phase 5: Portfolio Polish

Improve visual polish, responsiveness, error states, loading states, and demo readiness.

Goal:
Make FairMatch AI presentable as a professional portfolio product.

## Risk Control

- Version 1.0 remains stable.
- The `main` branch remains untouched during Version 2 planning.
- The `v1.0` tag remains preserved.
- The existing backend is reused.
- No solver rewrite is planned.
- No optimisation objective change is planned.
- Existing tests remain valid.
- Version 2 work happens on the `v2-frontend` branch.

## Current Status

Status:
Planning only.

Created:
- Version 2 frontend plan
- `frontend/` placeholder folder
- `api/` placeholder folder

Not implemented yet:
- React
- Next.js
- FastAPI
- Database
- Full frontend dashboard

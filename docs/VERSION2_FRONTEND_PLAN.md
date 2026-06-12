# FairMatch AI Version 2 Frontend Plan

## Product Vision

FairMatch AI is an Explainable Fairness-Aware Allocation Platform.

Version 2 prepares the project for a professional product and portfolio frontend. The goal is to provide:

- Fair Allocation
- Transparent Decisions
- Counterfactual Analysis

through a polished web experience that feels like a real decision-support product rather than a student prototype.

Version 2 must reuse the existing FairMatch backend. The solver, fairness helpers, counterfactual logic, and explanation logic remain stable.

Version 2.2 focuses on product polish, visual hierarchy and dashboard readability.

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

## Product Navigation

Version 2.1 includes product-level navigation across the main frontend pages.

Navigation links:
- Product
- Architecture
- Demo
- Future Work
- School Mode
- Work Mode
- Home

Section anchors exist on the landing page:
- `#product`
- `#architecture`
- `#demo`
- `#future-work`

Cross-mode navigation exists between:
- School Mode dashboard: `dashboard.html`
- Work Mode product preview: `work.html`

Work Mode remains a product preview. Backend implementation remains future work.

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
- Work Mode

School Mode remains the active product path with real backend integration.

Work Mode product preview added in Version 2.1. Backend implementation remains future work.

School Mode and Work Mode are connected through frontend navigation. Users can move directly between the School Mode dashboard and Work Mode product preview without returning to the landing page.

### 3. School Mode Dashboard

Purpose:
Provide the main decision-support workspace for student-to-project allocation.

Sections:
- Overview
- Allocation
- Fairness
- Explanation
- Comparison

The dashboard should present results clearly without exposing internal debug details.

### 4. Work Mode Product Preview

Purpose:
Show how FairMatch AI can extend into employee-to-task and employee-to-shift allocation.

Status:
Product preview added in Version 2.1. Backend implementation remains future work.

Content:
- Work Mode hero
- Employee-to-task and employee-to-shift scenario
- Planned capabilities
- School Mode vs Work Mode comparison
- Shared Person-to-Item engine concept
- Work Mode roadmap

### 5. Future Work Page

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
- Work Mode backend is not implemented in Version 2.1.

## Current Status

Status:
Version 2.2 product frontend prototype.

Created:
- Version 2 frontend plan
- Static landing page
- Product section anchors
- Complete product navigation
- Product polish for visual hierarchy and dashboard readability
- School Mode dashboard with real FastAPI integration
- Work Mode product preview page
- Cross-mode frontend navigation between School Mode and Work Mode
- FastAPI wrapper
- Localhost launcher

Not implemented yet:
- React
- Next.js
- Database
- Authentication
- Work Mode backend allocation

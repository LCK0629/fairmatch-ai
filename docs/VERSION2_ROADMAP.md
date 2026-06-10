# Version 2 Roadmap

## Purpose

This document prepares future Version 2 planning.

Version 2 is not implemented in this release. The Version 1 allocation engine is considered complete and stable. Future work should build around that foundation without weakening the validated solver, fairness, explanation, and counterfactual logic.

## Frontend

### React

Motivation:
React could support a more interactive product interface than Streamlit, including reusable components, richer client-side interactions, and a more polished user experience.

Expected benefit:

- improved visual control
- reusable UI components
- better interaction design
- easier future integration with API endpoints

Implementation complexity:
Medium to High.

Current status:
Planning only.

### Next.js

Motivation:
Next.js could provide a production-style web application foundation with routing, server-side rendering options, and a stronger deployment path.

Expected benefit:

- professional frontend architecture
- page routing for dashboard, reports, and simulations
- easier deployment as a web app
- improved project presentation for future demos

Implementation complexity:
High.

Current status:
Planning only.

## Backend

### FastAPI

Motivation:
FastAPI could expose the current solver, fairness metrics, explanations, and counterfactual comparison through HTTP endpoints.

Expected benefit:

- clean separation between frontend and backend
- API-driven dashboard
- easier integration with React or Next.js
- future support for external tools and automated workflows

Implementation complexity:
Medium.

Current status:
Planning only.

## Data Layer

### PostgreSQL

Motivation:
PostgreSQL could store users, datasets, allocation runs, results, fairness reports, and audit history.

Expected benefit:

- persistent allocation records
- historical comparison of runs
- multi-user data support
- stronger reporting and audit trail

Implementation complexity:
High.

Current status:
Planning only.

## Features

### Supervisor Fairness

Motivation:
Version 1 supports supervisor limits as hard constraints, but does not report supervisor fairness as a separate metric.

Expected benefit:

- better workload transparency for academic staff
- clearer explanation of supervisor load distribution
- stronger fairness evaluation beyond student satisfaction

Implementation complexity:
Medium.

Current status:
Planned enhancement.

### Counterfactual Workload

Motivation:
Version 1 supports fairness counterfactual comparison. Workload balancing should eventually receive the same comparison treatment.

Expected benefit:

- show whether workload balancing changed assignments
- clarify trade-offs between satisfaction, fairness, and workload
- improve explanation strength for workload-sensitive cases

Implementation complexity:
Medium.

Current status:
Planned enhancement.

### What-If Simulation

Motivation:
Coordinators may want to test policy changes such as project capacity changes, supervisor limit changes, or fairness weight changes before finalising allocation.

Expected benefit:

- supports scenario planning
- improves decision confidence
- makes FairMatch AI more useful as a real decision support platform

Implementation complexity:
Medium to High.

Current status:
Research extension.

### PDF Reports

Motivation:
Stakeholders may need a shareable report containing allocation results, fairness metrics, explanation summaries, and counterfactual comparison.

Expected benefit:

- professional reporting output
- easier review and approval
- stronger FYP presentation artefact

Implementation complexity:
Medium.

Current status:
Presentation enhancement.

### Multi-user Accounts

Motivation:
A future deployed version may need separate accounts for administrators, coordinators, supervisors, and reviewers.

Expected benefit:

- role-based access
- saved datasets and allocation runs
- improved audit trail
- closer fit to institutional workflows

Implementation complexity:
High.

Current status:
Long-term planning.

## Version 2 Starting Point

Recommended starting point:

```text
Create an API boundary around the existing backend using FastAPI.
```

Reason:
The current solver and evaluation logic are already validated. A clear API boundary makes it easier to build a React or Next.js frontend without rewriting the allocation engine.

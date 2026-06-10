# Decisions

This file records major design decisions.

## Decision Log Format

```text
Decision:
Date:
Status:
Context:
Decision:
Rationale:
Consequences:
```

## Decision 1: Use Python Backend

Date: 2026-06-10

Status: Accepted

Context:

FairMatch AI needs clear data handling and strong optimisation library support.

Decision:

Use Python for the backend.

Rationale:

Python is readable, suitable for FYP development, and works well with OR-Tools.

Consequences:

The project uses Python dataclasses, JSON input, and pytest tests.

## Decision 2: Use Google OR-Tools CP-SAT

Date: 2026-06-10

Status: Accepted

Context:

The project needs binary assignment variables, hard constraints, soft constraints, and weighted objectives.

Decision:

Use Google OR-Tools CP-SAT.

Rationale:

CP-SAT is suitable for scheduling and allocation problems with fairness constraints.

Consequences:

FairMatch AI remains a constraint optimisation platform, not a machine learning or LLM recommender.

## Decision 3: Use Shared People-to-Items Model

Date: 2026-06-10

Status: Accepted

Context:

School Mode and Work Mode have similar allocation structure.

Decision:

Represent both modes as people allocated to items.

Rationale:

This keeps the model reusable while allowing mode-specific labels and extensions.

Consequences:

Students and employees share the `Person` model. Projects, tasks, and shifts share the `Item` model.

## Decision 4: Add Skills and Workload to Core Model

Date: 2026-06-10

Status: Accepted

Context:

The initial model was preference-based only and too simple for the final FYP requirement.

Decision:

Add person skills, item required skills, person workload limits, item workload, and supervisor limits.

Rationale:

Skill matching and workload balancing are essential for realistic allocation.

Consequences:

The solver can block ineligible assignments and penalise uneven workload spread.

## Decision 5: Keep Frontend and API Out of Current Scope

Date: 2026-06-10

Status: Accepted

Context:

The backend model and documentation need to be stable before UI or API work.

Decision:

Do not add frontend, FastAPI, Streamlit, or LLM logic yet.

Rationale:

Premature interface work would distract from the core optimisation model.

Consequences:

The project remains CLI-based for now.

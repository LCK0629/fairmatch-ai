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

Represent both modes as people allocated to items internally.

Rationale:

This keeps the model reusable while allowing mode-specific labels and extensions.

Consequences:

Students and employees can share the `Person` model. Projects, tasks, and shifts can share the `Item` model. The roadmap still prioritises School Mode first.

## Decision 4: Add Skills and Workload to Core Model

Date: 2026-06-10

Status: Accepted

Context:

The initial model was preference-based only and too simple for the final FYP requirement.

Decision:

Add person skills, item required skills, workload limits, item workload, and supervisor limits.

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

## Decision 6: Refocus Roadmap on School Mode First

Date: 2026-06-10

Status: Accepted

Context:

The official requirement emphasises a scheduling and allocation engine with fairness, workload balance, stakeholder preferences, and transparent decision logic. The project had been documenting both School Mode and Work Mode as parallel directions, which risks spreading effort too broadly.

Decision:

Refocus the roadmap so Phase 1 delivers School Mode end-to-end first:

```text
Student -> Project allocation
```

Work Mode remains a future extension unless time allows.

Rationale:

A complete and explainable Student to Project allocation engine is stronger for the FYP than two partially finished modes. School Mode directly demonstrates allocation, fairness, supervisor workload, stakeholder preferences, and transparent decision logic.

Consequences:

Immediate implementation should prioritise School Mode datasets, constraints, explanations, tests, and fairness evaluation. Dashboard work is nice-to-have and should not distract from the core engine.

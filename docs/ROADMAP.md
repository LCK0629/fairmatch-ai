# Roadmap

## Strategic Focus

FairMatch AI will focus first on a complete School Mode allocation engine.

Main FYP scope:

```text
Explainable Fairness-Aware Project Allocation Engine
```

The goal is to deliver a strong Student to Project allocation system before expanding to other modes.

## Phase 1: School Mode End-to-End

Priority: Core.

Build a complete Student to Project allocation engine.

Phase 1 should include:

- concrete School Mode sample dataset
- student profiles
- project profiles
- student preferences
- student skill matching
- project capacity constraints
- supervisor workload constraints
- fairness-aware objective function
- CLI execution path
- tests for feasible and infeasible cases

Success criteria:

- every valid student allocation can be solved through the backend
- hard constraints are respected
- results include fairness and workload indicators
- School Mode tests cover core behaviour

## Phase 2: Explanation Engine

Priority: Core.

Implement systematic transparent decision logic.

Phase 2 should include:

- structured explanation fields
- preference-rank explanation
- skill-match explanation
- capacity explanation
- supervisor workload explanation
- fairness trade-off explanation
- infeasibility explanation when no solution exists

Success criteria:

- users can understand why each assignment happened
- explanations are generated consistently
- explanations are suitable for FYP evaluation and demonstration

## Phase 3: Fairness Metrics and Evaluation

Priority: Core.

Add mathematically grounded fairness metrics.

Phase 3 should include:

- satisfaction gap
- minimum satisfaction
- average satisfaction
- first-choice allocation count
- low-ranked allocation count
- supervisor workload distribution
- fairness-performance trade-off reporting

Success criteria:

- fairness is measurable, not only described
- metrics can compare different allocation runs
- documentation explains each metric clearly

## Phase 4: Work Mode

Priority: Future extension.

Keep Work Mode as a future extension unless time allows.

Possible Work Mode features:

- employee to task allocation
- employee to shift allocation
- employee skills
- task requirements
- employee workload limits
- shift coverage constraints

Success criteria:

- Work Mode reuses the shared allocation model
- Work Mode does not delay completion of School Mode

## Phase 5: Dashboard

Priority: Nice-to-have.

A dashboard is useful for demonstration but is not the core priority.

Possible dashboard features:

- upload or edit sample data
- run allocation
- view assignments
- view fairness metrics
- view explanations

Success criteria:

- dashboard supports the completed backend
- dashboard does not replace the core optimisation engine

## Current Next Step

Define concrete School Mode sample datasets and edge cases.

The next implementation work should prioritise:

- realistic student data
- realistic project data
- supervisor limits
- skill requirements
- expected allocation behaviours
- tests for School Mode constraints

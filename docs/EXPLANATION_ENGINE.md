# Explanation Engine

## Purpose

The Explanation Engine is Phase 2 of FairMatch AI.

Its purpose is to make School Mode allocation decisions transparent and reviewable. Instead of returning only a final Student to Project assignment, the system now returns structured explanation data for each assignment.

This supports the official FYP requirement for transparent decision logic.

## Structured Explanation Schema

Each assignment includes an `ExplanationDetail` object.

Current schema:

```python
@dataclass(frozen=True)
class ExplanationDetail:
    person_id: str
    item_id: str
    assigned_item: str
    preference_rank: int | None
    satisfaction: int
    skill_match: bool
    capacity_note: str
    skill_note: str
    first_choice_note: str
    supervisor_note: str
    fairness_note: str
    workload_note: str
    summary: str
```

## Explanation Rules

Each assignment explanation should include:

1. Assigned project
2. Preference rank
3. Satisfaction score
4. Skill eligibility result
5. Capacity status
6. Supervisor constraint note
7. Fairness note
8. Workload note
9. Human-readable summary

The current schema also includes `first_choice_note` to explain why the student's first choice was or was not assigned where possible.

## First-Choice Rejection Notes

When the assigned project is not the student's first choice, the engine checks for likely reasons:

- first-choice project reached capacity
- student lacked required skills for the first-choice project
- supervisor limit affected the feasible set
- first-choice project would exceed the student's workload limit
- fairness objective may have favoured another assignment
- workload balancing may have favoured another assignment

If the assigned project is the student's first choice, the note states that directly.

## Current Limitations

The current Explanation Engine provides structured evidence and likely reasons. It does not yet produce a formal counterfactual proof.

This means the system can say:

```text
First choice was not assigned because the project reached capacity and fairness may have favoured another assignment.
```

But it cannot yet prove that one specific constraint was the only decisive cause.

Reason:

Google OR-Tools CP-SAT returns an optimal or feasible assignment, but it does not automatically return a causal explanation for every rejected alternative.

## Future Plan

Future explanation work should add:

- explicit first-choice rejection tests
- counterfactual checks for first-choice projects
- fairness trade-off explanation comparing low and high fairness-weight runs
- workload trade-off explanation comparing low and high workload-balance-weight runs
- infeasibility explanations for failed allocation runs
- user-facing explanation formatting for a future dashboard

## Phase 2 Status

Phase 2 has started.

Completed so far:

- structured explanation data model
- assignment-level capacity notes
- assignment-level skill notes
- first-choice notes
- supervisor notes
- fairness notes
- workload notes
- human-readable summaries

Next step:

Add tests for first-choice rejection and constraint-driven explanations.

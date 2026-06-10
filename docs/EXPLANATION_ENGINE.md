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

Fairness and workload notes are heuristic indicators. The current implementation adds these notes when the corresponding objective weight is active and the student did not receive their first choice. This is useful decision context, but it does not prove that fairness or workload balancing was the decisive cause for that specific student's rejected first choice.

## Objective-Aware Explanation

Objective-aware explanations describe which optimisation objectives were active during a solver run.

Example:

```text
fairness objective may have influenced the allocation
```

Meaning:

The fairness objective was active in the optimisation. This is useful context, but it does not prove that fairness changed a specific assignment.

## Counterfactual Explanation

Counterfactual explanations compare two completed solver runs.

For fairness, the comparison is:

```text
fairness_weight = 0
```

versus:

```text
fairness_weight > 0
```

Example:

```text
Comparing fairness_weight = 0 and fairness_weight = 3 shows that Student One's assignment changed and fairness_gap improved.
```

Meaning:

Fairness demonstrably changed the allocation result for at least one student and improved at least one fairness metric.

The counterfactual comparison helper reports:

- total satisfaction before and after fairness weighting
- satisfaction gap before and after fairness weighting
- max-min value before and after fairness weighting
- Gini coefficient before and after fairness weighting
- students whose assigned projects changed
- students whose satisfaction scores changed
- whether fairness improved according to the reported metrics

## CLI Explanation Output

The CLI now exposes explanation and fairness reporting in a demo-ready format.

Normal allocation:

```bash
python -m backend.fairmatch.cli data/school_cases/fairness_weight_tradeoff.json
```

or:

```bash
python -m backend.fairmatch.cli --input data/school_cases/fairness_weight_tradeoff.json
```

The normal output includes:

- solver status
- objective value
- total satisfaction
- average satisfaction
- fairness gap
- max-min value
- Gini coefficient
- workload gap
- assignment summaries
- first-choice notes
- fairness notes
- workload notes

Counterfactual fairness comparison:

```bash
python -m backend.fairmatch.cli data/school_cases/fairness_weight_tradeoff.json --compare-fairness
```

This prints:

- baseline allocation with `fairness_weight = 0`
- fairness-aware allocation with `fairness_weight = 3`
- counterfactual comparison showing assignment changes and fairness metric changes

## Current Limitations

The current Explanation Engine provides structured evidence and likely reasons. It now includes a fairness-run counterfactual comparison, but it does not yet produce a formal counterfactual proof for every rejected alternative.

This means the system can say:

```text
First choice was not assigned because the project reached capacity and fairness may have favoured another assignment.
```

But the assignment-level note cannot yet prove that one specific constraint was the only decisive cause for every individual first-choice rejection.

In particular:

- Capacity, skill eligibility, supervisor limit, and max workload notes are based on directly checked constraint conditions.
- Fairness and workload balancing notes are based on active objective weights.
- A fairness or workload note should be read as "this objective may have influenced the allocation", not as confirmed causal attribution.

Reason:

Google OR-Tools CP-SAT returns an optimal or feasible assignment, but it does not automatically return a causal explanation for every rejected alternative.

## Explanation Test Coverage

Current tests cover:

- capacity-driven first-choice rejection
- skill-driven first-choice rejection
- workload-driven first-choice rejection
- fairness heuristic note when a non-first-choice assignment occurs under an active fairness objective
- counterfactual fairness comparison between `fairness_weight = 0` and `fairness_weight > 0`

## Future Plan

Future explanation work should add:

- counterfactual checks for first-choice projects
- workload trade-off explanation comparing low and high workload-balance-weight runs
- objective attribution checks that rerun controlled variants to determine whether fairness or workload balancing changed a specific assignment
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
- counterfactual fairness comparison helper

Next step:

Expose counterfactual fairness comparison results through CLI output and future dashboard visualisation.

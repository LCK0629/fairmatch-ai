# Validation Report: School Mode Solver Audit

## Scope

This report audits the current School Mode solver for FairMatch AI.

Files reviewed:

- `data/school_sample.json`
- `backend/fairmatch/models.py`
- `backend/fairmatch/solver.py`
- `tests/test_solver.py`
- `tests/test_school_cases.py`

The purpose is to check whether School Mode fields already present in the sample data are actually used by the solver.

## Summary

The current solver does use the main School Mode fields:

- `required_skills`
- `supervisor_id`
- `supervisor_limits`
- `workload_balance_weight`
- `fairness_weight`
- project `capacity`
- student preference order

However, some fields affect allocation directly as hard constraints, while others affect allocation indirectly through the objective function.

## Field-by-Field Audit

### 1. Does `required_skills` affect allocation?

Status: Yes.

Evidence:

In `solver.py`, every student-project pair is checked with `_has_required_skills`.

If a student does not satisfy a project's required skills, the assignment variable is forced to zero:

```text
x[student, project] = 0
```

This makes skill eligibility a hard constraint.

Relevant behaviour:

- A student cannot be assigned to a project unless all required project skills are present in the student's skills.
- This is tested by `test_skill_requirements_block_ineligible_assignments`.
- Additional School Mode edge cases include skill bottleneck and skill gap scenarios.

Assessment:

`required_skills` is actively and correctly used.

### 2. Does `supervisor_id` affect allocation?

Status: Yes, but only when `supervisor_limits` is provided.

Evidence:

Each item can have a `supervisor_id`. The solver groups projects by supervisor when applying `supervisor_limits`.

If no matching supervisor limit exists, `supervisor_id` is still included in explanations but does not restrict the solve.

Relevant behaviour:

- `supervisor_id` links projects to a supervisor workload rule.
- It is not a constraint by itself.
- It becomes meaningful when `supervisor_limits` contains the same supervisor ID.

Assessment:

`supervisor_id` is used correctly as a reference field for supervisor limit constraints. It should be documented as a linking field, not an independent constraint.

### 3. Does `supervisor_limits` affect allocation?

Status: Yes.

Evidence:

For each supervisor limit, the solver finds all projects with the matching `supervisor_id` and limits the total number of assigned students across those projects.

The constraint is:

```text
sum(x[student, project] for projects supervised by supervisor) <= supervisor_limit
```

Relevant behaviour:

- A supervisor can be limited across multiple projects.
- This can make a problem infeasible even when project capacity is sufficient.
- This is tested by the supervisor limit edge case.

Assessment:

`supervisor_limits` is actively used as a hard constraint.

### 4. Does `workload_balance_weight` affect allocation?

Status: Yes, through the objective function.

Evidence:

The solver calculates workload per person:

```text
workload = current_workload + assigned project workload
```

It then calculates:

```text
workload_gap = max_workload - min_workload
```

The objective subtracts:

```text
workload_balance_weight * workload_gap
```

Relevant behaviour:

- A higher `workload_balance_weight` makes uneven student workload less desirable.
- This is a soft constraint, not a hard constraint.
- Student `max_workload` remains a separate hard constraint.

Assessment:

`workload_balance_weight` affects allocation when there are multiple feasible solutions with different workload spreads.

Limitation:

The current workload balancing is person-based. The roadmap also discusses supervisor workload balance, but the current objective does not yet calculate a supervisor workload gap. Supervisor workload is currently handled only through hard `supervisor_limits`.

### 5. Does `fairness_weight` affect allocation?

Status: Yes, through the objective function.

Evidence:

The solver calculates satisfaction for each student, then derives:

```text
fairness_gap = max_satisfaction - min_satisfaction
```

The objective subtracts:

```text
fairness_weight * fairness_gap
```

Relevant behaviour:

- A higher `fairness_weight` makes unequal satisfaction distribution less desirable.
- This is a soft constraint, not a hard constraint.
- It affects allocation only when the solver has multiple feasible choices with different satisfaction gaps.

Assessment:

`fairness_weight` is actively used.

Scoring update:

The solver now uses a fixed scoring scale:

```text
1st = 3
2nd = 2
3rd = 1
unranked or lower-ranked = 0
```

This keeps satisfaction scores comparable when students submit preference lists of different lengths.

### 6. Does project `capacity` affect allocation?

Status: Yes.

Evidence:

For each project, the solver adds:

```text
sum(x[student, project] for student in students) <= capacity[project]
```

Relevant behaviour:

- Projects cannot receive more students than their capacity.
- The solver also validates that total capacity is at least the number of people when every student must be assigned.

Assessment:

Project `capacity` is actively and correctly used as a hard constraint.

### 7. Does student preference order affect allocation?

Status: Yes.

Evidence:

The solver converts each student's ranked project list into a satisfaction score.

Current scoring:

```text
1st choice = 3
2nd choice = 2
3rd choice = 1
unranked or lower-ranked = 0
```

Higher-ranked projects receive higher scores.

Relevant behaviour:

- Preference order affects `total_satisfaction`.
- `total_satisfaction` is part of the objective function.
- Preference rank is also included in the assignment explanation.

Assessment:

Preference order is actively used.

Assessment:

Preference order is actively used through a fixed scoring scale. This resolves the earlier issue where longer preference lists could inflate satisfaction scores.

## Tests Reviewed

Current tests cover:

- happy path assignment
- skill eligibility blocking
- infeasible workload case
- balanced feasible School Mode case
- skill bottleneck case
- controlled fairness-weight comparison case
- insufficient capacity validation
- skill gap infeasibility
- supervisor limit infeasibility
- workload limit infeasibility
- invalid preference reference validation

Note on `balanced_feasible.json`:

Daniel Lim is intentionally constrained to the web project by skill eligibility. This is deliberate because the dataset is meant to show that a balanced feasible case can still include realistic eligibility restrictions. The test should verify valid assignment quality without assuming every future feasible assignment must have a ranked preference.

The tests provide useful coverage, but full execution was not verified during this audit because local dependencies may not be installed.

## Controlled Fairness Weight Result

The project includes `data/school_cases/fairness_weight_tradeoff.json` to verify that `fairness_weight` can change optimisation behaviour.

The case is designed so:

- one allocation has higher total satisfaction but worse satisfaction gap
- another allocation has lower total satisfaction but better satisfaction gap

Expected behaviour:

```text
low fairness_weight:
  favours higher total satisfaction
  accepts a larger fairness gap

high fairness_weight:
  accepts lower total satisfaction
  favours a smaller fairness gap
```

The corresponding test verifies:

- both runs are feasible
- project capacity is respected
- skill eligibility is respected
- low `fairness_weight` produces higher total satisfaction
- high `fairness_weight` produces a lower fairness gap
- low and high `fairness_weight` produce different assignment behaviour
- the high-fairness run includes a non-first-choice assignment with a fairness objective note

Status:

The validation report and test coverage are now aligned. The controlled test is implemented in `tests/test_school_cases.py` as `test_fairness_weight_changes_optimisation_behaviour`.

Explanation limitation:

The fairness note in `first_choice_note` is a heuristic explanation signal. It confirms that the fairness objective was active in a run where the student did not receive their first choice, but it does not prove that fairness was the sole or decisive cause for that individual rejection. Stronger causal attribution would require counterfactual checks or controlled reruns that compare alternative objective settings for the same student-project decision.

## Overall Assessment

The School Mode solver is not merely reading fields passively. It actively uses most of the School Mode fields in constraints or objective terms.

Strong areas:

- project capacity is a hard constraint
- skill eligibility is a hard constraint
- supervisor limits are hard constraints
- workload limits are hard constraints
- preference order affects optimisation
- fairness and workload balance are represented in the objective
- assignment explanations now use structured explanation fields

Main issues to address next:

1. Supervisor workload balance is not yet a soft objective metric.
2. More tests should compare solver output under different `workload_balance_weight` values.
3. Explanation notes identify fairness and workload settings, but deeper counterfactual reasoning is still future work.

## Phase 2 Structured Explanation Engine Status

Assignments now include an `ExplanationDetail` object instead of a single explanation string.

Current structured fields:

- `person_id`
- `item_id`
- `assigned_item`
- `preference_rank`
- `satisfaction`
- `skill_match`
- `capacity_note`
- `skill_note`
- `first_choice_note`
- `supervisor_note`
- `fairness_note`
- `workload_note`
- `summary`

This closes the first Phase 2 design step by making explanations structured and testable. The current engine explains assignment facts, optimisation settings, and likely first-choice rejection reasons.

Current limitation:

First-choice rejection notes are not yet formal counterfactual proofs. They identify likely constraint and objective factors such as capacity, skill eligibility, supervisor limits, fairness weighting, and workload balancing. Exact causal attribution remains future work.

Documentation consistency note:

Capacity, skill eligibility, supervisor limit, and max workload notes are derived from direct constraint checks. Fairness and workload balancing notes are derived from whether the corresponding objective weights are active, so they should be read as "may have influenced the allocation" rather than confirmed causal explanations.

## Recommended Next Step

Add tests for first-choice rejection and constraint-driven explanations.

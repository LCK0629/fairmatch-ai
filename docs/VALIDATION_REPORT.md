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
- insufficient capacity validation
- skill gap infeasibility
- supervisor limit infeasibility
- workload limit infeasibility
- invalid preference reference validation

The tests provide useful coverage, but full execution was not verified during this audit because local dependencies may not be installed.

## Overall Assessment

The School Mode solver is not merely reading fields passively. It actively uses most of the School Mode fields in constraints or objective terms.

Strong areas:

- project capacity is a hard constraint
- skill eligibility is a hard constraint
- supervisor limits are hard constraints
- workload limits are hard constraints
- preference order affects optimisation
- fairness and workload balance are represented in the objective
- assignment explanations include key decision details

Main issues to address next:

1. Supervisor workload balance is not yet a soft objective metric.
2. More tests should compare solver output under different `fairness_weight` and `workload_balance_weight` values.
3. Explanation logic should eventually describe fairness trade-offs, not only assignment facts.

## Recommended Next Step

Add tests proving that changing `fairness_weight` can change allocation decisions in a controlled School Mode case.

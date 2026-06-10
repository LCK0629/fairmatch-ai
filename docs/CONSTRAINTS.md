# Constraints

## Scope Priority

The constraint roadmap now prioritises School Mode first:

```text
students -> projects
```

Work Mode constraints should remain documented as possible future extensions, but implementation priority should stay on a complete Student to Project allocation engine.

## Decision Variables

The core School Mode decision variable is:

```text
x[student, project] = 1 if student is assigned to project
x[student, project] = 0 otherwise
```

Generic form:

```text
x[person, item]
```

The generic form may support Work Mode later, but School Mode should drive the immediate design.

## Phase 1 Hard Constraints

Hard constraints must be satisfied.

### One Project Per Student

Each student should receive exactly one project.

```text
sum(x[student, project] for project in projects) = 1
```

### Project Capacity

A project cannot exceed its student capacity.

```text
sum(x[student, project] for student in students) <= capacity[project]
```

### Skill Eligibility

A student should only be assigned to a project when the student's skills satisfy the project's required skills.

```text
x[student, project] = 0
if required_skills[project] is not a subset of skills[student]
```

### Supervisor Workload Limit

Each supervisor should have a maximum number of assigned students or supervised project load.

```text
sum(x[student, project] for project supervised by supervisor) <= supervisor_limit[supervisor]
```

### Valid Input References

All preferences and constraints must reference valid student, project, and supervisor IDs.

## Phase 1 Soft Constraints

Soft constraints affect solution quality and may be traded off.

### Student Preference Satisfaction

Higher-ranked projects should receive higher satisfaction scores.

```text
first choice > second choice > third choice > unranked
```

### Fairness Across Students

The solver should avoid extreme differences in satisfaction.

Initial metric:

```text
fairness_gap = max_student_satisfaction - min_student_satisfaction
```

### Supervisor Workload Balance

The solver should avoid unnecessary workload concentration among supervisors.

Possible metric:

```text
supervisor_workload_gap = max_supervisor_load - min_supervisor_load
```

This is a Phase 1 priority because the official topic includes workload balance.

## Objective Function Direction

Phase 1 objective direction:

```text
maximise student_preference_satisfaction
         - fairness_penalty
         - supervisor_workload_penalty
```

The exact mathematical objective can evolve, but it should remain explainable.

## Fairness Modelling Direction

Fairness should be mathematically grounded and documented.

Phase 1 starts with satisfaction gap.

Phase 3 should expand evaluation with metrics such as:

- minimum satisfaction
- satisfaction distribution
- count of first-choice assignments
- count of low-ranked assignments
- supervisor load distribution
- fairness-performance trade-off analysis

## Transparent Decision Logic

Every assignment should eventually explain:

- assigned student
- assigned project
- preference rank
- satisfaction score
- skill match
- project capacity status
- supervisor workload impact
- fairness trade-off

## Future Work Mode Constraints

Work Mode may later reuse the generic model for:

- employee task preferences
- employee skills
- task or shift requirements
- employee workload limits
- shift coverage constraints

These are future extension constraints, not Phase 1 priority.

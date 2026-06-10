# Constraints

## Decision Variables

The core decision variable is:

```text
x[person, item] = 1 if person is assigned to item
x[person, item] = 0 otherwise
```

Examples:

```text
x[s1, p1] = 1
x[e1, t1] = 1
```

## Hard Constraints

Hard constraints must be satisfied.

### One Assignment Per Person

Each person currently receives exactly one item.

```text
sum(x[person, item] for item in items) = 1
```

### Item Capacity

An item cannot exceed its capacity.

```text
sum(x[person, item] for person in people) <= capacity[item]
```

### Skill Eligibility

A person cannot be assigned to an item unless they satisfy all required skills.

```text
x[person, item] = 0 if required_skills[item] is not a subset of skills[person]
```

### Person Workload Limit

A person cannot exceed their maximum workload.

```text
current_workload[person] + assigned_workload[person] <= max_workload[person]
```

### Supervisor Workload Limit

When supervisor limits are provided, the total number of people assigned to that supervisor's items cannot exceed the limit.

```text
sum(x[person, item] for item supervised by supervisor) <= supervisor_limit[supervisor]
```

## Soft Constraints

Soft constraints affect solution quality and are represented through the objective function.

### Preference Satisfaction

Higher-ranked choices receive higher satisfaction scores.

```text
first choice > second choice > third choice > unranked
```

### Satisfaction Fairness

The solver penalises a large satisfaction gap.

```text
fairness_gap = max_satisfaction - min_satisfaction
```

### Workload Balance

The solver penalises a large workload gap.

```text
workload_gap = max_workload - min_workload
```

## Objective Function

Current objective:

```text
maximise total_satisfaction
         - fairness_weight * fairness_gap
         - workload_balance_weight * workload_gap
```

This means the solver prefers allocations that:

- satisfy preferences
- avoid unfair satisfaction spread
- avoid uneven workload spread

## Fairness Modelling

Fairness is modelled as a measurable optimisation term, not as a vague rule.

Current fairness metric:

```text
max_satisfaction - min_satisfaction
```

Future fairness extensions may include:

- minimum satisfaction floor
- number of first-choice assignments
- number of low-satisfaction assignments
- workload variance
- supervisor workload distribution

## Transparent Decision Logic

Every assignment should explain:

- preference rank
- satisfaction score
- skill eligibility
- resulting workload
- capacity compliance
- supervisor limit check

This supports decision review by users and assessors.

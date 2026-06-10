# Fairness Evaluation

## Scope

This document compares fairness metrics for School Mode in FairMatch AI.

School Mode focuses on:

```text
students -> projects
```

The current solver uses fixed preference satisfaction scoring:

```text
1st choice = 3
2nd choice = 2
3rd choice = 1
unranked or lower-ranked = 0
```

This fixed scale allows fairness metrics to compare students consistently.

## Metrics Compared

This document compares:

1. Satisfaction Gap
2. Max-Min Fairness
3. Gini Coefficient

## Metric 1: Satisfaction Gap

### Definition

Satisfaction Gap measures the difference between the most satisfied student and the least satisfied student.

### Formula

```text
satisfaction_gap = max(satisfaction_scores) - min(satisfaction_scores)
```

Lower is better.

### Advantages

- Easy to understand.
- Easy to explain to non-technical users.
- Directly identifies whether some students are much worse off than others.
- Already represented in the current solver as `fairness_gap`.

### Disadvantages

- Only looks at the two extreme students.
- Does not show how the middle students are distributed.
- Two allocations can have the same gap but very different overall distributions.

### Applicability to School Mode

Satisfaction Gap is useful as the first fairness metric for Student to Project allocation because it directly answers:

```text
How far apart are the best and worst student outcomes?
```

It is suitable for the current Phase 1 solver.

## Metric 2: Max-Min Fairness

### Definition

Max-Min Fairness focuses on improving the least satisfied student's outcome.

Instead of asking only how large the gap is, it asks:

```text
What is the lowest satisfaction score received by any student?
```

### Formula

```text
maximise min(satisfaction_scores)
```

For reporting a completed allocation:

```text
max_min_value = min(satisfaction_scores)
```

Higher is better.

### Advantages

- Protects the worst-off student.
- Matches fairness intuition in allocation problems.
- Useful when the project wants to avoid very poor individual outcomes.
- Easy to explain as "raise the floor".

### Disadvantages

- May ignore total satisfaction after the minimum is improved.
- Can treat many allocations as equal if they have the same minimum score.
- Needs to be combined with other metrics to avoid weak overall outcomes.

### Applicability to School Mode

Max-Min Fairness is highly applicable to School Mode because project allocation should avoid leaving any student with a very poor match when better alternatives exist.

It is especially useful when:

- many students compete for popular projects
- some students have limited eligible choices
- fairness is more important than maximising only total preference score

## Metric 3: Gini Coefficient

### Definition

The Gini Coefficient measures inequality across the full satisfaction distribution.

It considers all pairs of student satisfaction scores, not only the highest and lowest.

### Formula

For `n` students with satisfaction scores `s_i`:

```text
Gini = sum_i(sum_j(abs(s_i - s_j))) / (2 * n^2 * mean(s))
```

Lower is better.

Typical interpretation:

```text
0 = perfect equality
higher value = more unequal satisfaction distribution
```

If all satisfaction scores are zero, FairMatch AI should report Gini as `0` for equality but also separately report that total satisfaction is poor.

### Advantages

- Uses the full distribution.
- More informative than only comparing maximum and minimum.
- Useful for comparing different allocation runs.
- Can detect broad inequality patterns.

### Disadvantages

- Harder to explain to non-technical users.
- Less intuitive than Satisfaction Gap.
- Can look fair when everyone receives equally poor outcomes, so it must be reported with total satisfaction and minimum satisfaction.

### Applicability to School Mode

Gini is useful for Phase 3 evaluation because it gives a mathematically grounded view of fairness across all students.

It should be used as an evaluation metric rather than the first optimisation objective.

## Comparison Summary

| Metric | Better Direction | Main Question | Best Use |
| --- | --- | --- | --- |
| Satisfaction Gap | Lower | How far apart are best and worst outcomes? | Simple fairness penalty in solver |
| Max-Min Fairness | Higher | How good is the worst student outcome? | Protecting the least satisfied student |
| Gini Coefficient | Lower | How unequal is the full distribution? | Post-solve fairness evaluation |

## Evaluation Method

The datasets were evaluated using the current fixed scoring scale.

Because local OR-Tools execution may not be available in every environment, the comparison below is based on the same decision rules and objective structure used by the solver:

```text
maximise total_satisfaction
         - fairness_weight * satisfaction_gap
         - workload_balance_weight * workload_gap
```

The evaluation checks feasible School Mode assignments against:

- project capacity
- student skill eligibility
- student workload limits
- supervisor limits
- preference satisfaction

Invalid input datasets are marked as validation cases rather than fairness cases.

## Existing School Mode Dataset Results

| Dataset | Status | Satisfaction Scores | Satisfaction Gap | Max-Min Value | Gini | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `data/school_sample.json` | Feasible | `[3, 3, 2, 3, 2]` | 1 | 2 | 0.092 | Competitive sample with multiple students targeting the AI project. |
| `data/school_cases/balanced_feasible.json` | Feasible | `[3, 3, 3, 3, 3, 3]` | 0 | 3 | 0.000 | Ideal balanced case where all students receive first choice. |
| `data/school_cases/skill_bottleneck_feasible.json` | Feasible | `[2, 2]` | 0 | 2 | 0.000 | Skills force both students away from first choice, but outcomes remain equal. |
| `data/school_cases/insufficient_capacity_infeasible.json` | Infeasible / validation failure | N/A | N/A | N/A | N/A | Total project capacity is lower than student count. |
| `data/school_cases/invalid_preference_reference.json` | Invalid input | N/A | N/A | N/A | N/A | Preference references a missing project ID and should fail validation. |
| `data/school_cases/skill_gap_infeasible.json` | Infeasible | N/A | N/A | N/A | N/A | No student-project assignment satisfies required skills. |
| `data/school_cases/supervisor_limit_infeasible.json` | Infeasible | N/A | N/A | N/A | N/A | Supervisor limit prevents assigning all students. |
| `data/school_cases/workload_limit_infeasible.json` | Infeasible | N/A | N/A | N/A | N/A | Project workload exceeds the student's maximum workload. |

## Interpretation

### `school_sample.json`

This is now the most useful active sample for demonstrating trade-offs.

It has:

- a popular AI project
- multiple eligible students competing for that project
- supervisor limits that affect the feasible allocation space
- non-identical satisfaction scores

Fairness metrics show:

```text
Satisfaction Gap = 1
Max-Min Value = 2
Gini = 0.092
```

This indicates a relatively fair allocation, but not perfect equality.

### `balanced_feasible.json`

This is the clean ideal case.

Fairness metrics show:

```text
Satisfaction Gap = 0
Max-Min Value = 3
Gini = 0.000
```

All students receive first choice, so all three metrics agree that the allocation is fair.

### `skill_bottleneck_feasible.json`

This case shows why fairness metrics must be interpreted with total satisfaction.

Fairness metrics show:

```text
Satisfaction Gap = 0
Max-Min Value = 2
Gini = 0.000
```

The allocation is equal, but both students receive second choice due to skill eligibility constraints.

## Recommendation

FairMatch AI should report all three metrics together:

```text
Satisfaction Gap
Max-Min Value
Gini Coefficient
```

Recommended Phase 1 use:

- keep Satisfaction Gap in the solver objective
- report Max-Min Value in solver output
- report Gini Coefficient in evaluation output
- report total satisfaction and average satisfaction beside fairness metrics

Recommended Phase 3 use:

- compare allocation runs using all three metrics
- add fairness-performance trade-off reporting
- show total satisfaction beside fairness metrics
- explain that equal outcomes can still be poor if all satisfaction scores are low

## Code-Level Helper Layer

Fairness metrics are now implemented in:

```text
backend/fairmatch/fairness.py
```

Current helper functions:

- satisfaction gap
- max-min value
- Gini coefficient
- total satisfaction
- average satisfaction

These helpers are integrated into `AllocationResult` for feasible solver runs. Infeasible runs report zero-valued fairness metrics because no allocation distribution exists.

Important:

The helper layer is a reporting and evaluation layer. It does not change the OR-Tools optimisation objective.

## Next Step

Use the helper layer to compare fairness results across controlled School Mode scenarios and future counterfactual explanation checks.

# System Flow

## Current Flow

```text
Input Data
    ↓
Data Loader / Validator
    ↓
Scoring Engine
    ↓
OR-Tools CP-SAT Model Builder
    ↓
Solver
    ↓
Fairness Evaluator
    ↓
Explanation Engine
    ↓
CLI / Future Dashboard
```

## 1. Input Data

The system reads JSON input files.

Current examples:

- `data/school_sample.json`
- `data/work_sample.json`

## 2. Data Loader / Validator

The loader converts JSON into dataclasses.

The validator checks IDs, mode, capacities, preference references, and workload values.

## 3. Scoring Engine

The scoring engine converts ranked preferences into satisfaction scores.

The solver uses these scores in the objective function.

## 4. OR-Tools CP-SAT Model Builder

The model builder creates:

- assignment decision variables
- capacity constraints
- skill eligibility constraints
- workload constraints
- supervisor limit constraints
- fairness metrics
- workload balance metrics

## 5. Solver

Google OR-Tools CP-SAT solves the model.

Possible statuses:

- OPTIMAL
- FEASIBLE
- INFEASIBLE
- UNKNOWN

## 6. Fairness Evaluator

The solver result includes:

- total satisfaction
- minimum satisfaction
- maximum satisfaction
- fairness gap
- minimum workload
- maximum workload
- workload gap

These values help users judge whether the allocation is balanced.

## 7. Explanation Engine

Each assignment includes a transparent explanation.

The explanation describes:

- the assignment
- preference rank
- skill match
- workload impact
- capacity compliance
- supervisor limit handling

## 8. CLI / Future Dashboard

The CLI prints JSON output.

A future dashboard may later present the same results visually, but no frontend is part of this stage.

## School Mode Flow

```text
students
  -> projects
  -> preferences and skills
  -> project capacity and supervisor limits
  -> CP-SAT allocation
  -> fair project assignment explanations
```

## Work Mode Flow

```text
employees
  -> tasks or shifts
  -> preferences, skills, and workload limits
  -> task capacity
  -> CP-SAT allocation
  -> fair task or shift assignment explanations
```

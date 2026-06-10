# Architecture

## Architecture Overview

FairMatch AI uses a backend-first architecture focused on data validation, scoring, constraint optimisation, fairness evaluation, and explanation.

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

## Current Implementation

The current repository contains:

```text
backend/fairmatch/models.py
backend/fairmatch/solver.py
backend/fairmatch/cli.py
data/school_sample.json
data/work_sample.json
tests/test_solver.py
```

The implementation is still backend-only. No frontend, FastAPI, Streamlit, or LLM logic has been added.

## Input Data

Input data is currently provided as JSON.

Input includes:

- mode
- people
- items
- preferences
- fairness weight
- workload balance weight
- supervisor limits when relevant

## Data Loader / Validator

The loader converts JSON dictionaries into Python dataclasses.

The validator checks:

- valid mode
- non-empty people and items
- sufficient total capacity
- unique person IDs
- unique item IDs
- preferences reference valid IDs
- workload limits are valid
- item capacity and workload values are valid

## Scoring Engine

The scoring engine converts ranked preferences into satisfaction scores.

Example:

```text
first choice = highest score
second choice = lower score
unranked item = 0
```

Skill matching is currently treated as an eligibility rule. A person cannot be assigned to an item if they do not satisfy the required skills.

## OR-Tools CP-SAT Model Builder

The model builder creates binary decision variables:

```text
x[person, item]
```

The variable equals `1` if the person is assigned to the item, and `0` otherwise.

## Solver

The solver uses Google OR-Tools CP-SAT to search for a feasible or optimal allocation.

The objective combines:

- total preference satisfaction
- satisfaction fairness gap
- workload balance gap

## Fairness Evaluator

The current fairness metric is satisfaction spread:

```text
fairness_gap = max_satisfaction - min_satisfaction
```

The solver penalises large fairness gaps.

Workload balance is measured separately:

```text
workload_gap = max_workload - min_workload
```

## Explanation Engine

Each assignment includes a plain-language explanation containing:

- assigned person
- assigned item
- preference rank
- satisfaction score
- skill match result
- workload after assignment
- capacity compliance
- supervisor limit check when relevant

## CLI / Future Dashboard

The current interface is a CLI.

Future dashboard work may be added after the backend model is stable. The dashboard should display inputs, results, fairness metrics, and assignment explanations.

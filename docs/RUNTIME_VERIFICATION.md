# Runtime Verification

## Purpose

This document records the runtime verification pass for FairMatch AI.

Scope:

- verify local dependency setup
- verify OR-Tools installation
- verify pytest installation
- run the test suite
- run `school_sample.json`
- run `fairness_weight_tradeoff.json`
- run counterfactual fairness comparison output

No new features, objective changes, or future-work implementations were added during this verification pass.

## Environment

```text
Date: 2026-06-10
Operating system: Windows
Shell: PowerShell
Project folder: C:\Users\cheek\Projects\fairMatch
System Python: 3.11.9
Runtime environment: project-local .venv
Virtual environment Python: 3.11.9
```

## Commands Used

### Initial Dependency Check

System Python version:

```powershell
python --version
```

Observed:

```text
Python 3.11.9
```

OR-Tools check:

```powershell
python -c "import ortools; print(ortools.__version__)"
```

Observed failure:

```text
ModuleNotFoundError: No module named 'ortools'
```

pytest check:

```powershell
python -m pytest --version
```

Observed failure:

```text
No module named pytest
```

### Fix Applied

A project-local virtual environment was created:

```powershell
python -m venv .venv
```

Dependencies were installed into `.venv`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This avoided modifying the system Python environment.

### Verified Dependency Versions

Python:

```powershell
.\.venv\Scripts\python.exe --version
```

Observed:

```text
Python 3.11.9
```

OR-Tools:

```powershell
.\.venv\Scripts\python.exe -c "import ortools; print(ortools.__version__)"
```

Observed:

```text
9.15.6755
```

pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest --version
```

Observed:

```text
pytest 8.4.2
```

## Test Suite Result

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Observed:

```text
collected 21 items

tests\test_cli.py ..                                                     [  9%]
tests\test_fairness.py ...                                               [ 23%]
tests\test_school_cases.py ............                                  [ 80%]
tests\test_solver.py ....                                                [100%]

21 passed in 31.20s
```

## CLI Run: `school_sample.json`

Command:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_sample.json
```

Observed summary:

```text
Status: OPTIMAL
Objective value: 10.0
Total satisfaction: 13
Average satisfaction: 2.60
Fairness gap: 1
Max-min value: 2
Gini coefficient: 0.092
Workload gap: 1
```

Observed assignments:

```text
Alicia Tan -> AI Timetable Assistant
Benjamin Lee -> AI Timetable Assistant
Chloe Wong -> Smart Campus Feedback Portal
Daniel Lim -> Smart Campus Feedback Portal
Evelyn Goh -> Student Performance Dashboard
```

Observed explanation output:

```text
Alicia Tan: Assigned project is the student's first choice.
Benjamin Lee: Assigned project is the student's first choice.
Chloe Wong: First choice was not assigned because first-choice project reached capacity; supervisor limit affected the feasible set; fairness objective may have favoured another assignment; workload balancing may have favoured another assignment.
Daniel Lim: Assigned project is the student's first choice.
Evelyn Goh: First choice was not assigned because first-choice project reached capacity; supervisor limit affected the feasible set; fairness objective may have favoured another assignment; workload balancing may have favoured another assignment.
```

Result:

```text
school_sample.json ran successfully.
```

## CLI Run: `fairness_weight_tradeoff.json`

Command:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json
```

Observed summary:

```text
Status: OPTIMAL
Objective value: 7.0
Total satisfaction: 7
Average satisfaction: 2.33
Fairness gap: 2
Max-min value: 1
Gini coefficient: 0.190
Workload gap: 0
```

Observed assignments:

```text
Student One -> Popular AI Project
Student Two -> Documentation Project
Student Three -> Data Quality Project
```

Observed explanation output:

```text
Student One: Assigned project is the student's first choice.
Student Two: First choice was not assigned because first-choice project reached capacity.
Student Three: Assigned project is the student's first choice.
```

Result:

```text
fairness_weight_tradeoff.json ran successfully.
```

## CLI Run: Counterfactual Fairness Comparison

Command:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness
```

### Baseline Output

```text
Baseline Allocation: fairness_weight = 0
Status: OPTIMAL
Objective value: 7.0
Total satisfaction: 7
Average satisfaction: 2.33
Fairness gap: 2
Max-min value: 1
Gini coefficient: 0.190
Workload gap: 0
```

Baseline assignments:

```text
Student One -> Popular AI Project
Student Two -> Documentation Project
Student Three -> Data Quality Project
```

### Fairness-Aware Output

```text
Fairness-Aware Allocation: fairness_weight = 3
Status: OPTIMAL
Objective value: 2.0
Total satisfaction: 5
Average satisfaction: 1.67
Fairness gap: 1
Max-min value: 1
Gini coefficient: 0.133
Workload gap: 0
```

Fairness-aware assignments:

```text
Student One -> Documentation Project
Student Two -> Data Quality Project
Student Three -> Popular AI Project
```

### Counterfactual Output

```text
Total satisfaction: 7 -> 5
Fairness gap: 2 -> 1
Max-min value: 1 -> 1
Gini coefficient: 0.190 -> 0.133
Fairness improved: True
```

Changed assignments:

```text
s1: p1 -> p3
s2: p3 -> p2
s3: p2 -> p1
```

Changed satisfaction:

```text
s1: 3 -> 1
s2: 1 -> 2
s3: 3 -> 2
```

Result:

```text
Counterfactual fairness comparison ran successfully.
```

## Failures

### Failure 1: Missing OR-Tools in System Python

Command:

```powershell
python -c "import ortools; print(ortools.__version__)"
```

Failure:

```text
ModuleNotFoundError: No module named 'ortools'
```

Fix:

Installed dependencies into project-local `.venv`.

### Failure 2: Missing pytest in System Python

Command:

```powershell
python -m pytest --version
```

Failure:

```text
No module named pytest
```

Fix:

Installed dependencies into project-local `.venv`.

### Non-Issue: First OR-Tools Version Check Timeout

One OR-Tools version check timed out during verification. The check was rerun with a longer timeout and succeeded:

```text
9.15.6755
```

## Fixes

Applied fixes:

- created `.venv`
- installed `requirements.txt` into `.venv`
- reran dependency checks through `.venv`
- reran tests through `.venv`
- reran CLI commands through `.venv`

No code fixes were required for the runtime verification pass.

## Final Verification Status

```text
OR-Tools installed: Yes
pytest installed: Yes
Tests passing: Yes, 21 passed
school_sample.json runs: Yes
fairness_weight_tradeoff.json runs: Yes
counterfactual CLI output runs: Yes
Objective modified: No
Future work implemented: No
```

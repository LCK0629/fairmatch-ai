# Runtime Verification

## Purpose

This document records the Round 17 runtime verification pass for FairMatch AI.

The goal was to verify that the current system runs correctly after adding:

- School Mode allocation engine
- OR-Tools CP-SAT solver
- fairness metric helper layer
- structured explanation engine
- counterfactual fairness comparison
- demo-ready CLI
- text and JSON output modes

No optimisation features, fairness logic, explanation logic, Work Mode implementation, or dashboard work were added during this pass.

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

## Setup Commands

System Python version:

```powershell
python --version
```

Observed:

```text
Python 3.11.9
```

Create or refresh the project virtual environment:

```powershell
python -m venv .venv
```

Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The verification used the `.venv` Python executable directly. This is equivalent to activating the virtual environment for the executed commands and avoids modifying system Python packages.

## Installed Package Versions

Dependency installation result:

```text
Requirement already satisfied: ortools<10,>=9.10 ... (9.15.6755)
Requirement already satisfied: pytest<9,>=8.0 ... (8.4.2)
Requirement already satisfied: absl-py ... (2.4.0)
Requirement already satisfied: numpy ... (2.4.6)
Requirement already satisfied: pandas ... (3.0.3)
Requirement already satisfied: protobuf ... (6.33.6)
Requirement already satisfied: typing-extensions ... (4.15.0)
Requirement already satisfied: immutabledict ... (4.3.1)
Requirement already satisfied: colorama ... (0.4.6)
Requirement already satisfied: iniconfig ... (2.3.0)
Requirement already satisfied: packaging ... (26.2)
Requirement already satisfied: pluggy ... (1.6.0)
Requirement already satisfied: pygments ... (2.20.0)
Requirement already satisfied: python-dateutil ... (2.9.0.post0)
Requirement already satisfied: tzdata ... (2026.2)
Requirement already satisfied: six ... (1.17.0)
```

Version checks:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -c "import ortools; print(ortools.__version__)"
.\.venv\Scripts\python.exe -m pytest --version
```

Observed:

```text
Python 3.11.9
9.15.6755
pytest 8.4.2
```

Installation warnings:

```text
[notice] A new release of pip is available: 24.0 -> 26.1.2
```

This is informational only. No dependency installation failure occurred.

## Compile Verification

Command:

```powershell
.\.venv\Scripts\python.exe -m compileall backend tests
```

Observed:

```text
Listing 'backend'...
Listing 'backend\fairmatch'...
Compiling 'backend\fairmatch\__init__.py'...
Compiling 'backend\fairmatch\cli.py'...
Compiling 'backend\fairmatch\counterfactual.py'...
Compiling 'backend\fairmatch\fairness.py'...
Compiling 'backend\fairmatch\models.py'...
Compiling 'backend\fairmatch\solver.py'...
Listing 'tests'...
Compiling 'tests\test_cli.py'...
Compiling 'tests\test_fairness.py'...
Compiling 'tests\test_school_cases.py'...
Compiling 'tests\test_solver.py'...
```

Result:

```text
Compile verification passed.
No compile errors observed.
```

## Test Suite Verification

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Observed:

```text
collected 24 items

tests\test_cli.py .....                                                  [ 20%]
tests\test_fairness.py ...                                               [ 33%]
tests\test_school_cases.py ............                                  [ 83%]
tests\test_solver.py ....                                                [100%]

24 passed in 1.48s
```

Result:

```text
Tests passed: 24
Tests failed: 0
```

## CLI Text Output Verification

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

Verification:

```text
status appears: yes
assignments appear: yes
fairness metrics appear: yes
explanations appear: yes
```

## CLI JSON Output Verification

Command:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_sample.json --output json
```

Observed key fields:

```json
{
  "mode": "school",
  "status": "OPTIMAL",
  "objective_value": 10.0,
  "total_satisfaction": 13,
  "average_satisfaction": 2.6,
  "fairness_gap": 1,
  "max_min_value": 2,
  "gini_coefficient": 0.09230769230769231,
  "workload_gap": 1
}
```

Observed structured explanation field:

```json
{
  "person_id": "s1",
  "item_id": "p1",
  "assigned_item": "AI Timetable Assistant",
  "preference_rank": 1,
  "satisfaction": 3,
  "skill_match": true,
  "first_choice_note": "Assigned project is the student's first choice.",
  "fairness_note": "Fairness weight 2 was applied through the satisfaction gap objective.",
  "workload_note": "Workload becomes 2/3; workload balance weight 1 was included in the objective."
}
```

Additional JSON validation command:

```powershell
.\.venv\Scripts\python.exe -c "import json, subprocess, sys; out=subprocess.check_output([sys.executable, '-m', 'backend.fairmatch.cli', 'data\\school_sample.json', '--output', 'json'], text=True); data=json.loads(out); assert data['status']=='OPTIMAL'; assert 'fairness_gap' in data; assert data['assignments'][0]['explanation']['summary']; print('school_sample json valid')"
```

Observed:

```text
school_sample json valid
```

Verification:

```text
valid JSON: yes
fairness metrics included: yes
structured explanations included: yes
```

## Counterfactual Text Output Verification

Command:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness
```

Observed baseline summary:

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

Observed fairness-aware summary:

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

Observed counterfactual comparison:

```text
Total satisfaction: 7 -> 5
Fairness gap: 2 -> 1
Max-min value: 1 -> 1
Gini coefficient: 0.190 -> 0.133
Fairness improved: True
Changed assignments:
- s1: p1 -> p3
- s2: p3 -> p2
- s3: p2 -> p1
Changed satisfaction:
- s1: 3 -> 1
- s2: 1 -> 2
- s3: 3 -> 2
```

Verification:

```text
baseline run displayed: yes
fairness run displayed: yes
assignment changes displayed: yes
fairness metric changes displayed: yes
```

## Counterfactual JSON Output Verification

Command:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness --output json
```

Observed top-level JSON keys:

```json
{
  "baseline_result": {},
  "fairness_result": {},
  "counterfactual_comparison": {},
  "warning": null
}
```

Observed counterfactual fields:

```json
{
  "baseline_total_satisfaction": 7,
  "fairness_total_satisfaction": 5,
  "baseline_fairness_gap": 2,
  "fairness_fairness_gap": 1,
  "baseline_max_min_value": 1,
  "fairness_max_min_value": 1,
  "baseline_gini_coefficient": 0.19047619047619047,
  "fairness_gini_coefficient": 0.13333333333333333,
  "fairness_improved": true
}
```

Observed changed assignments:

```json
{
  "s1": ["p1", "p3"],
  "s2": ["p3", "p2"],
  "s3": ["p2", "p1"]
}
```

Additional JSON validation command:

```powershell
.\.venv\Scripts\python.exe -c "import json, subprocess, sys; out=subprocess.check_output([sys.executable, '-m', 'backend.fairmatch.cli', 'data\\school_cases\\fairness_weight_tradeoff.json', '--compare-fairness', '--output', 'json'], text=True); data=json.loads(out); assert 'baseline_result' in data; assert 'fairness_result' in data; assert 'counterfactual_comparison' in data; assert 'warning' in data; print('counterfactual json valid')"
```

Observed:

```text
counterfactual json valid
```

Verification:

```text
baseline_result present: yes
fairness_result present: yes
counterfactual_comparison present: yes
warning present: yes
valid JSON: yes
```

## Warnings

Installation warning:

```text
[notice] A new release of pip is available: 24.0 -> 26.1.2
```

Assessment:

This is not a project failure. The current dependency installation completed successfully, and no pip upgrade was required for verification.

## Fixes Applied

No code fixes were required.

Operational cleanup:

- removed `__pycache__` directories generated by compile and test commands
- removed `.pytest_cache`

The project-local `.venv` remains in place and is ignored by git.

## Final Verification Status

```text
Python verified: yes
OR-Tools installed: yes
pytest installed: yes
compileall passed: yes
tests passing: yes, 24 passed
CLI text output works: yes
CLI JSON output works: yes
counterfactual text output works: yes
counterfactual JSON output works: yes
optimisation logic modified: no
fairness logic modified: no
explanation logic modified: no
Work Mode implemented: no
dashboard implemented: no
```

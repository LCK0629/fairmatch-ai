# Step 1: Initial FairMatch AI Project Structure

This document explains what was built in the first step of the FairMatch AI project.

FairMatch AI is a fairness-aware allocation platform for CSIT-26-S3-06. The system is designed to support two allocation scenarios:

- School Mode: allocate students to projects.
- Work Mode: allocate employees to tasks.

The first step focused on creating a safe, clean backend foundation. No complex frontend was built yet.

## Local Project Location

The project was created outside OneDrive to avoid sync conflicts, accidental cloud changes, and unnecessary filesystem noise.

```text
C:\Users\cheek\Projects\fairMatch
```

This location is safer than system folders such as `C:\Windows` or `C:\Program Files`, and cleaner than a synced OneDrive directory.

## GitHub Repository

The project was pushed to:

```text
https://github.com/LCK0629/fairmatch-ai
```

The remote repository already contained a simple initial `README.md`, so the local project history was merged safely instead of force-pushing over the remote content.

## Project Structure Created

```text
fairMatch/
  backend/
    fairmatch/
      __init__.py
      cli.py
      models.py
      solver.py
  data/
    school_sample.json
    work_sample.json
  docs/
    step_1_initial_project_structure.md
  tests/
    test_solver.py
  .gitignore
  README.md
  requirements.txt
```

## Backend Technology Choice

The backend is written in Python.

Python was chosen because it is suitable for optimisation workflows, easy to read, and works well with Google OR-Tools.

The optimisation engine selected is:

```text
Google OR-Tools CP-SAT
```

CP-SAT is useful for allocation problems because it can model binary decisions, capacity limits, assignment constraints, and fairness objectives.

## Dependencies

The dependency file created is:

```text
requirements.txt
```

It currently contains:

```text
ortools>=9.10,<10
pytest>=8.0,<9
```

Dependencies were not installed automatically. This was intentional to avoid changing the computer environment without explicit permission.

## Main Backend Files

### `backend/fairmatch/models.py`

This file defines the core data structures used by the backend.

It includes:

- `Person`: represents a student or employee.
- `Item`: represents a project or task.
- `AllocationInput`: represents the full input problem.
- `Assignment`: represents one person assigned to one item.
- `AllocationResult`: represents the solver output.
- `load_allocation_input`: converts JSON input into Python data objects.

The same model supports both School Mode and Work Mode.

### `backend/fairmatch/solver.py`

This file contains the first version of the allocation solver.

The solver creates a CP-SAT model where each possible person-to-item pairing is represented as a yes-or-no decision variable.

The solver enforces these rules:

- Each person must be assigned to exactly one item.
- Each item cannot exceed its capacity.
- Preference rankings are converted into satisfaction scores.
- The solver tries to maximise total satisfaction.
- The solver also penalises unfairness between the most satisfied and least satisfied assigned people.

The fairness idea is implemented by calculating:

```text
fairness_gap = max_satisfaction - min_satisfaction
```

The objective is:

```text
maximise total_satisfaction - fairness_weight * fairness_gap
```

This means the system does not only chase the highest total preference score. It also tries to avoid outcomes where one person gets a very good result while another gets a much worse result.

### `backend/fairmatch/cli.py`

This file provides a simple command-line entry point.

It can load a JSON input file, run the solver, and print the allocation result as JSON.

Example commands:

```powershell
python -m backend.fairmatch.cli --input data\school_sample.json
python -m backend.fairmatch.cli --input data\work_sample.json
```

These commands require dependencies to be installed first.

## Sample Data

Two sample JSON files were created.

### `data/school_sample.json`

This file demonstrates School Mode.

It includes:

- Four students.
- Three projects.
- Project capacity limits.
- Student project preferences.
- A fairness weight.

The goal is to allocate students to projects while balancing preference satisfaction and fairness.

### `data/work_sample.json`

This file demonstrates Work Mode.

It includes:

- Four employees.
- Three tasks.
- Task capacity limits.
- Employee task preferences.
- A fairness weight.

The same solver can process this mode because the underlying problem is still person-to-item allocation.

## Test File

The file created is:

```text
tests/test_solver.py
```

It contains a small solver test for a simple School Mode case. The test checks that every student receives an assignment when capacity is sufficient.

The test was added as an initial safety net, but full tests were not run because OR-Tools has not been installed yet.

## Safety Measures Taken

Several safety choices were made during the first step:

- The project was created outside OneDrive.
- No dependencies were installed automatically.
- No background services were started.
- No complex frontend was created.
- No system directories were modified.
- A `.gitignore` file was added to avoid committing virtual environments, cache files, and local environment files.
- The existing GitHub repository history was merged safely instead of overwritten.

## Current Limitations

The first step is intentionally small and foundational.

Current limitations:

- No web API has been created yet.
- No database has been added.
- No authentication has been added.
- No frontend has been built.
- The fairness model is simple and should be expanded later.
- The solver currently assumes every person must receive exactly one item.
- The sample data is small and meant for demonstration only.

## Suggested Next Steps

Recommended next steps:

1. Add a FastAPI backend API.
2. Add request and response validation.
3. Add more test cases for capacity, infeasible inputs, and fairness behaviour.
4. Add result explanation output so users can understand why assignments were made.
5. Add a simple frontend only after the backend behaviour is stable.

The first step successfully created a clean backend foundation for FairMatch AI without making unnecessary changes to the computer.

# FairMatch AI

FairMatch AI is a fairness-aware allocation platform for CSIT-26-S3-06.

It supports two allocation modes:

- School Mode: allocate students to projects.
- Work Mode: allocate employees to tasks.

The backend is written in Python and uses Google OR-Tools CP-SAT as the optimisation engine.

## Project Structure

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
  tests/
    test_solver.py
  requirements.txt
  README.md
```

## Safety Notes

This initial project does not install dependencies automatically, does not start background services, and does not change system settings. It only reads JSON input files and writes results to standard output when you run the CLI.

## Install Dependencies

From this folder, create and activate a virtual environment first, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run Examples

```powershell
python -m backend.fairmatch.cli --input data\school_sample.json
python -m backend.fairmatch.cli --input data\work_sample.json
```

## Data Model

Each input JSON file contains:

- `mode`: `school` or `work`.
- `people`: students or employees.
- `items`: projects or tasks.
- `preferences`: ranked item choices for each person.
- `fairness_weight`: how strongly the solver should reduce satisfaction gaps.

The solver maximises preference satisfaction while penalising unfair spread between the most and least satisfied assigned people.
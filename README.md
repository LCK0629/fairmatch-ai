# FairMatch AI

FairMatch AI is a fairness-aware allocation platform for CSIT-26-S3-06: Intelligent Scheduling and Allocation System with Fairness Constraints.

It is a constraint optimisation and decision support platform. It is not an LLM recommendation system.

Product positioning:

FairMatch AI is an Explainable Fairness-Aware Allocation Platform for university project allocation. It helps administrators and academic coordinators move beyond manual assignment lists by producing valid allocations, measuring fairness, explaining decisions, and comparing fairness-aware outcomes against baseline alternatives.

It supports two allocation modes:

- School Mode: allocate students to projects while considering preferences, skill match, project capacity, supervisor workload, and fairness.
- Work Mode: allocate employees to tasks or shifts while considering preferences, skill match, task requirements, workload limits, and fairness.

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
  docs/
    PROJECT_CONTEXT.md
    ARCHITECTURE.md
    DATA_MODEL.md
    CONSTRAINTS.md
    SYSTEM_FLOW.md
    DECISIONS.md
    DEVELOPMENT_LOG.md
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

Default output is human-readable text for demonstrations.

Machine-readable JSON output is also available:

```powershell
python -m backend.fairmatch.cli data\school_sample.json --output json
```

Run a counterfactual fairness comparison:

```powershell
python -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness
```

The comparison uses `fairness_weight = 0` as the baseline and `fairness_weight = 3` by default for the fairness-aware run. You can override the comparison weight:

```powershell
python -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness --fairness-weight 5
```

Counterfactual comparison can also be emitted as JSON:

```powershell
python -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness --output json
```

## Run Dashboard

FairMatch AI also includes a Streamlit product demo for presentation:

```powershell
streamlit run app.py
```

## Run Version 2 API

Version 2 includes a FastAPI wrapper around the existing FairMatch backend:

```powershell
uvicorn api.main:app --reload
```

Available endpoints:

- `GET /health`
- `GET /samples`
- `POST /allocate`
- `POST /compare-fairness`

The API reuses the existing backend solver, fairness metrics, explanation data, and counterfactual comparison logic.

### Version 2 Frontend

Run the API:

```powershell
uvicorn api.main:app --reload
```

Then open:

```text
frontend/index.html
```

The Version 2 dashboard checks `GET /health`, loads datasets from `GET /samples`,
runs allocation through `POST /allocate`, and runs fairness comparison through
`POST /compare-fairness`.

### Version 2 Quick Start

Double click:

```text
START_V2.bat
```

The launcher:

- checks that `.venv` exists
- starts FastAPI in a separate terminal window
- opens `frontend/index.html` in the default browser
- launches the Version 2 product experience

## One-Click Launch

Double click:

```text
START_FAIRMATCH.bat
```

to launch the FairMatch AI dashboard.

The launcher checks for the local `.venv`, activates it, opens the browser, and starts Streamlit. If `.venv` is missing, it shows setup instructions instead.

The Streamlit product experience follows a two-stage product flow:

- premium landing page introducing the value before asking for data
- Start Experience flow into the decision support workspace
- collapsed scenario setup for sample dataset selection and custom JSON upload
- tabbed workspace for Overview, Allocation, Fairness, Explanations, and Comparison
- large fairness metric cards for presentation
- professional allocation table and readable explanation cards
- counterfactual fairness comparison for baseline vs fairness-aware runs

## Data Model

Each input JSON file contains:

- `mode`: `school` or `work`.
- `people`: students or employees.
- `items`: projects or tasks.
- `people`: students or employees, including skills and workload limits.
- `items`: projects, tasks, or shifts, including capacity, required skills, workload, and optional supervisor ID.
- `preferences`: ranked item choices for each person.
- `supervisor_limits`: optional supervisor workload limits.
- `fairness_weight`: how strongly the solver should reduce satisfaction gaps.
- `workload_balance_weight`: how strongly the solver should reduce workload gaps.

The solver maximises preference satisfaction while penalising unfair spread between the most and least satisfied assigned people and uneven workload distribution. Each assignment includes a transparent explanation with preference rank, skill match, workload impact, and capacity reasoning.

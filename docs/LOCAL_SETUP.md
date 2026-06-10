# Local Setup Guide

## Purpose

This guide explains how to run FairMatch AI locally without changing the system Python installation.

The recommended setup uses a project-local virtual environment:

```text
.venv/
```

This folder is ignored by git and should not be committed.

## Environment

Verified environment:

```text
Operating system: Windows
Python: 3.11.9
Project folder: C:\Users\cheek\Projects\fairMatch
```

## Create Virtual Environment

Run from the project root:

```powershell
python -m venv .venv
```

## Install Dependencies

Run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This installs:

- Google OR-Tools
- pytest
- OR-Tools runtime dependencies

## Verify Dependencies

Check Python:

```powershell
.\.venv\Scripts\python.exe --version
```

Check OR-Tools:

```powershell
.\.venv\Scripts\python.exe -c "import ortools; print(ortools.__version__)"
```

Check pytest:

```powershell
.\.venv\Scripts\python.exe -m pytest --version
```

## Run Tests

Run:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Expected result:

```text
21 passed
```

## Run CLI Examples

Run the main School Mode sample:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_sample.json
```

Run the controlled fairness trade-off sample:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json
```

Run the counterfactual fairness comparison:

```powershell
.\.venv\Scripts\python.exe -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness
```

## Safety Notes

This setup:

- does not modify system Python packages
- does not start background services
- does not create a frontend server
- does not write output files during normal CLI runs
- keeps installed dependencies inside `.venv/`

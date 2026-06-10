# Development Log

This file records development rounds for FairMatch AI.

## Log Entry Format

```text
Round:

Completed:
- item

Rationale:
reason

Next Step:
next action
```

## Round 1 - Initial Project Structure

Completed:

- Created initial backend folder structure
- Created initial Python package structure
- Created sample School Mode JSON data
- Created sample Work Mode JSON data
- Created requirements file
- Created initial README
- Created initial step-one documentation
- Pushed initial project to GitHub

Rationale:

The project needed a clean backend-first foundation outside OneDrive before further development.

Next Step:

Create a stable Markdown documentation system for project context, architecture, data model, constraints, system flow, decisions, and development history.

## Round 2 - Markdown Documentation System

Completed:

- Created docs folder
- Created project context documentation
- Created architecture documentation
- Created data model documentation
- Created constraint design documentation
- Created system flow documentation
- Created decision log
- Created development log

Rationale:

The project needs a stable Markdown context system before implementing the OR-Tools solver.

Next Step:

Define concrete School Mode and Work Mode sample datasets.

## Round 3 - Core Model Upgrade

Completed:

- Upgraded person model with skills and workload fields
- Upgraded item model with required skills, workload, and supervisor ID
- Added supervisor limits to allocation input
- Added skill eligibility as a hard constraint
- Added person workload limits as a hard constraint
- Added workload gap as a soft balancing metric
- Added transparent assignment explanations
- Updated School Mode sample dataset
- Updated Work Mode sample dataset
- Added tests for skill eligibility and workload infeasibility
- Updated project documentation for the stronger FYP-ready model

Rationale:

The original allocation demo only considered preferences, capacity, and satisfaction fairness. The FYP requirement needs a stronger decision support model that includes skill matching, workload balancing, supervisor workload, and transparent explanations.

Next Step:

Review the upgraded sample datasets and define additional realistic edge cases for testing.

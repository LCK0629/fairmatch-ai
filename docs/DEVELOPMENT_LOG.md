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

## Round 4 - School Mode Roadmap Refocus

Completed:

- Refocused project context around the main FYP scope
- Defined the main scope as Explainable Fairness-Aware Project Allocation Engine
- Clarified that School Mode is Phase 1 priority
- Moved Work Mode to future extension status
- Updated constraint documentation for Student to Project allocation first
- Added roadmap documentation
- Added decision record for the School Mode first strategy
- Preserved dashboard as nice-to-have rather than core priority

Rationale:

The official requirement emphasises a scheduling and allocation engine with fairness, workload balance, stakeholder preferences, and transparent decision logic. A complete School Mode engine is a stronger FYP delivery target than spreading effort across School Mode, Work Mode, and dashboard work too early.

Next Step:

Define concrete School Mode sample datasets and edge cases for Student to Project allocation.

## Round 5 - School Mode Edge Cases and Solver Validation Tests

Completed:

- Created `data/school_cases/` for School Mode edge case datasets
- Added balanced feasible Student to Project allocation case
- Added skill bottleneck feasible case
- Added insufficient capacity validation case
- Added skill gap infeasible case
- Added supervisor limit infeasible case
- Added workload limit infeasible case
- Added invalid preference reference validation case
- Revised the main School Mode sample so multiple students compete for a popular AI project
- Adjusted the main School Mode sample so supervisor limits add a real constraint beyond project capacity
- Added School Mode tests that load the JSON edge cases
- Added assertions for assignment completeness, skill eligibility, explanations, fairness metrics, workload metrics, validation errors, and infeasible solver outcomes

Rationale:

Phase 1 requires a complete School Mode allocation engine. Concrete edge cases make the solver behaviour testable against project capacity, skill matching, supervisor workload, workload limits, invalid inputs, and transparent explanation requirements.

Next Step:

Install test dependencies in a virtual environment and run the School Mode validation suite with OR-Tools available.

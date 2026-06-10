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

## Round 6 - Fixed Preference Satisfaction Scoring

Completed:

- Replaced preference-list-length-based satisfaction scoring
- Added fixed satisfaction scale: 1st choice = 3, 2nd choice = 2, 3rd choice = 1, unranked or lower-ranked = 0
- Updated solver satisfaction variable bounds to use the fixed maximum score
- Added regression test for students with different preference list lengths receiving equal first-choice satisfaction scores
- Updated constraint documentation
- Updated validation report to mark the scoring issue as resolved

Rationale:

Fairness metrics require comparable satisfaction scores across students. The previous scoring method gave higher maximum scores to students who submitted longer preference lists, which could distort `fairness_gap`.

Next Step:

Add controlled tests showing how different `fairness_weight` values affect allocation decisions.

## Round 7 - School Case Test Assumption Cleanup

Completed:

- Documented that Daniel Lim is intentionally constrained to the web project in `balanced_feasible.json`
- Relaxed the balanced School Mode test so it no longer assumes every assignment must have a ranked preference
- Kept the test focused on valid assignments, skill matching, explanations, and non-negative fairness/workload metrics

Rationale:

The balanced case should remain useful for demonstrating skill eligibility. The test should not overfit to the current dataset by requiring every assigned project to appear in every student's ranked preference list.

Next Step:

Add controlled tests showing how different `fairness_weight` values affect allocation decisions.

## Round 8 - Controlled Fairness Weight Comparison

Status:
Completed

Completed:

- Added controlled fairness-weight comparison test case
- Verified whether fairness_weight changes solver behaviour
- Documented result in validation report

Rationale:

Fairness is a core FYP requirement, so the project must demonstrate that fairness weighting has measurable impact on allocation behaviour.

Next Step:

Implement code-level fairness metric helpers for satisfaction gap, max-min value, Gini coefficient, total satisfaction, and average satisfaction.

## Round 9 - Fairness Weight Trade-Off Test Fix

Status:
Completed

Completed:
- Added a real test for `fairness_weight_tradeoff.json`
- Verified low and high fairness weights produce different optimisation behaviour
- Resolved mismatch between validation documentation and test coverage

Rationale:
The validation report claimed that fairness-weight behaviour was tested, but the test was missing. This round closes the Phase 1 validation gap before moving into the Explanation Engine phase.

Next Step:
Start Phase 2 by designing a structured Explanation Engine.

## Round 10 - Structured Explanation Engine Design

Status:
Completed

Completed:
- Started Phase 2 Explanation Engine
- Added structured explanation data model
- Refactored assignment explanations away from simple string-only logic
- Added documentation for explanation rules and limitations

Rationale:
The official FYP topic requires transparent decision logic. Structured explanations make allocation decisions easier to inspect, test, and later display in a dashboard.

Next Step:
Add tests for first-choice rejection and constraint-driven explanations.

## Round 11 - First-Choice Rejection Explanation Tests

Status:
Completed

Completed:
- Added tests for capacity-driven first-choice rejection
- Added tests for skill-driven first-choice rejection
- Added tests for workload-driven first-choice rejection
- Added tests for fairness-influenced first-choice rejection

Rationale:
Transparent decision logic requires the system to explain not only why a student was assigned to a project, but also why their first-choice project was not selected.

Next Step:
Add code-level fairness metric helpers for:
- satisfaction gap
- max-min value
- Gini coefficient
- total satisfaction
- average satisfaction

## Round 12 - Explanation Heuristic Documentation Alignment

Status:
Completed

Completed:
- Documented that fairness and workload first-choice notes are heuristic indicators
- Clarified that current explanation logic does not prove causal attribution
- Updated validation wording for fairness-influenced explanation tests

Rationale:
The explanation engine currently adds fairness and workload "may have" notes when the corresponding objective weights are active. This is useful context, but it is not a counterfactual proof, so documentation must not overclaim causality.

Next Step:
Design counterfactual explanation checks that compare alternative allocations or rerun controlled scenarios to support stronger causal claims.

## Round 13 - Fairness Metric Helper Layer

Status:
Completed

Completed:
- Added `backend/fairmatch/fairness.py`
- Implemented satisfaction gap, max-min value, total satisfaction, average satisfaction, and Gini coefficient helpers
- Integrated fairness reporting metrics into `AllocationResult`
- Added tests for fairness helper functions
- Added tests proving solver results expose the new fairness metrics
- Updated fairness and validation documentation

Rationale:
Fairness metrics should be executable, testable project logic instead of documentation-only formulas. A helper layer makes the metrics reusable for solver results, validation reports, and future explanation work.

Next Step:
Use the helper layer to compare controlled School Mode scenarios and design counterfactual explanation checks.

## Round 14 - Counterfactual Fairness Explanation

Status:
Completed

Completed:
- Added counterfactual comparison helper
- Compared fairness and non-fairness allocations
- Identified assignment changes caused by fairness weighting
- Strengthened transparent decision logic

Rationale:
The previous explanation engine could identify that fairness was active, but could not determine whether fairness actually changed assignments.

Counterfactual comparison provides stronger evidence.

Next Step:
Expose fairness comparison results through CLI output and future dashboard visualisation.

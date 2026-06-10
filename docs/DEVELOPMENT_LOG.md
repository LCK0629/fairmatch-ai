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

## Round 15 - Demo-Ready CLI Explanation Output

Status:
Completed

Completed:
- Replaced raw JSON-only CLI output with readable allocation summaries
- Exposed fairness metrics in normal CLI output
- Exposed structured explanation notes in normal CLI output
- Added `--compare-fairness` CLI mode
- Printed baseline versus fairness-aware allocation comparison
- Printed counterfactual assignment, satisfaction, and fairness metric changes
- Added tests for CLI allocation and counterfactual comparison formatting

Rationale:
The project needs a simple demo path before any frontend work. CLI output should clearly show allocation results, fairness metrics, and transparent decision logic.

Next Step:
Run the full CLI and solver test suite once the local environment has `pytest` and OR-Tools installed.

## Round 16 - CLI Output Mode Polish

Status:
Completed

Completed:
- Added text/json output mode
- Preserved demo-friendly text output
- Added machine-readable JSON output
- Added fairness comparison warning or override
- Updated tests and documentation

Rationale:
The project now supports both human-readable demonstrations and machine-readable output for future dashboard integration.

Next Step:
Run full runtime verification using pytest and OR-Tools in a local virtual environment.

## Round 17 - Runtime Verification

Status:
Completed

Completed:
- Installed runtime dependencies
- Verified compile success
- Verified test suite
- Verified CLI text output
- Verified CLI JSON output
- Verified counterfactual comparison output
- Created runtime verification report

Rationale:
The project has completed the core allocation engine and must be verified in a clean environment before presentation-layer development.

Next Step:
Build a lightweight Streamlit dashboard if runtime verification remains stable.

## Round 18 - Lightweight Streamlit Dashboard

Status:
Completed

Completed:
- Added Streamlit dependency
- Built lightweight dashboard
- Added dataset selection
- Added allocation result table
- Added fairness metrics display
- Added explanation display
- Added counterfactual fairness comparison

Rationale:
The backend and CLI are verified. A lightweight dashboard improves demonstration quality without changing optimisation logic.

Next Step:
Prepare FYP report, presentation slides, and demo script.

## Round 19 - Product-Style Landing Page and Dashboard UI

Status:
Completed

Completed:
- Added a product-style landing page
- Added Start flow into the dashboard
- Upgraded dashboard visual structure and spacing
- Preserved dataset selection and custom JSON upload
- Preserved allocation results, fairness metrics, explanations, and counterfactual comparison
- Updated README and demo script for the new dashboard flow

Rationale:
The backend and dashboard are functional. A more mature two-stage UI improves the FYP demonstration experience without changing backend optimisation logic.

Next Step:
Use the dashboard flow to prepare the final FYP presentation slides and demo rehearsal.

## Round 20 - Mature Product Flow Redesign

Status:
Completed

Completed:
- Redesigned the Streamlit app into a clearer landing page and product dashboard flow
- Replaced the administrative sidebar layout with a top scenario panel
- Added tabbed views for allocation, fairness metrics, counterfactual comparison, and dataset review
- Enlarged fairness metric presentation for demo readability
- Reworked explanations into a focused student detail panel instead of full-page stacked expanders
- Updated README, demo script, and future work documentation

Rationale:
The previous dashboard was functional but still felt like an internal tool. A mature FYP product demo needs stronger visual hierarchy, clearer value introduction, and a cleaner workflow without changing backend optimisation logic.

Next Step:
Verify the redesigned dashboard visually and rehearse the final presentation flow.

## Round 21 - Version 1 Release Preparation

Status:
Completed

Completed:
- Reviewed repository status, runtime artifacts, documentation, tests, dashboard, and backend structure
- Confirmed `.gitignore` covers `.venv/`, `__pycache__/`, `.pytest_cache/`, and Python bytecode files
- Cleaned product documentation wording for FairMatch AI and Explainable Fairness-Aware Allocation Platform positioning
- Created Version 1 release notes
- Created Version 2 roadmap planning document
- Verified compile success
- Verified test suite success
- Verified CLI output still runs
- Verified dashboard HTTP response

Rationale:
The allocation engine is complete for Version 1. The project needs a stable release checkpoint before future frontend and platform work begins.

Next Step:
Create the `v1.0` Git tag after committing the release preparation changes.

## Round 22 - Version 2 Frontend Planning

Status:
Completed

Completed:
- Created and switched to the `v2-frontend` branch
- Created Version 2 frontend planning documentation
- Documented the product frontend vision
- Documented the planned frontend, FastAPI, backend, and solver architecture
- Documented planned pages and API endpoints
- Created placeholder `frontend/` and `api/` folders
- Confirmed Version 1.0 remains stable and untouched

Rationale:
FairMatch AI Version 1.0 is complete and frozen as the FYP system. Version 2 should evolve the project into a portfolio-ready product experience while reusing the existing backend and preserving the validated solver.

Next Step:
Create a static Version 2 landing page prototype in the `frontend/` folder.

## Round 24 - Streamlit UI Polish Fixes

Status:
Completed

Completed:
- Removed duplicate landing navigation
- Fixed fairness metric grid layout
- Added invalid JSON error handling
- Verified tests still pass

Rationale:
The Streamlit app should remain stable and presentation-ready while Version 2 frontend work begins. These fixes reduce duplicate navigation, improve fairness metric readability, and prevent invalid uploaded allocation data from breaking the app.

Next Step:
Continue Version 2 frontend prototyping after confirming the Streamlit app remains stable.

## Round 25 - Product Mode Selection Experience

Status:
Completed

Completed:
- Added a product-focused Mode Selection section to the Version 2 static frontend
- Added School Mode as the active allocation experience
- Added Work Mode as a Coming Soon placeholder
- Updated landing-page navigation and hero action to guide users into scenario selection
- Added premium SaaS card styling, hover treatment, badges, and responsive layout

Rationale:
Version 2 should feel like a product experience rather than a generic prototype. Mode selection introduces FairMatch AI as a multi-domain allocation platform while keeping School Mode as the active, validated path.

Next Step:
Create a static `dashboard.html` placeholder for the School Mode product workspace.

## Round 26 - Static V2 School Mode Dashboard Prototype

Status:
Completed

Completed:
- Created static School Mode dashboard page
- Added allocation overview cards
- Added allocation result table
- Added fairness metrics section
- Added explanation panel
- Added counterfactual comparison preview
- Linked dashboard from Version 2 landing page

Rationale:
The Version 2 product frontend needs a real destination after Mode Selection. This static dashboard prototype shows how School Mode will look before FastAPI backend integration.

Next Step:
Create FastAPI wrapper around the existing FairMatch backend.

## Round 27 - FastAPI Backend Wrapper

Status:
Completed

Completed:
- Added FastAPI dependency
- Added Uvicorn dependency
- Created `api/main.py`
- Added `GET /health`
- Added `GET /samples`
- Added `POST /allocate`
- Added `POST /compare-fairness`
- Added safe invalid payload handling
- Added API tests
- Updated README with API run instructions

Rationale:
Version 2 needs a clean API layer between the static product frontend and the existing FairMatch backend. The API wrapper allows future frontend integration while preserving the validated solver, fairness metrics, explanation logic, and counterfactual comparison layer.

Next Step:
Connect the static Version 2 frontend to the FastAPI endpoints.

## Round 28 - Frontend API Integration

Status:
Completed

Completed:
- Connected frontend to FastAPI
- Added health monitoring
- Added dynamic dataset loading
- Connected allocation endpoint
- Connected fairness comparison endpoint
- Replaced static dashboard data with real backend data
- Added frontend error handling

Rationale:
Version 2 now moves from static prototype to real product by connecting the HTML frontend to the verified FairMatch backend.

Next Step:
Create one-click launcher for API + Frontend and polish Version 2 user experience.

## Round 29 - Version 2 One-Click Launcher

Status:
Completed

Completed:
- Added START_V2.bat
- Added startup checks
- Added FastAPI startup
- Added frontend auto-launch
- Added Version 2 quick start documentation

Rationale:
A product should be easy to run and demonstrate. The launcher removes manual startup steps.

Next Step:
Perform a full Version 2 UX review and visual polish.

## Round 30 - Version 2 API Offline Debug and Verification

Status:
Completed

Completed:
- Verified that `GET /health` returns `{"status":"ok","service":"FairMatch AI API"}` when FastAPI is running
- Verified that `GET /samples` returns sample datasets and payloads
- Identified that the dashboard shows API Offline when the frontend opens before the API is ready
- Added frontend health-check retry behaviour
- Updated `START_V2.bat` to wait for the `/health` endpoint before opening the frontend
- Verified compile success
- Verified test suite success
- Stopped the temporary debug API process and removed debug logs

Rationale:
The Version 2 frontend depends on the local FastAPI service. Startup timing can cause a false API Offline message if the browser opens before the API is ready. Waiting for `/health` and retrying in the frontend makes the demo flow more reliable.

Next Step:
Run `START_V2.bat` manually for an end-to-end browser check.

## Round 31 - V2 Prototype Cleanup

Status:
Completed

Completed:
- Removed duplicate Streamlit back-to-landing action
- Removed unused API helper code
- Moved local import to top-level
- Documented permissive CORS as a prototype-only setting
- Verified tests still pass

Rationale:
Before UX review, the Version 2 prototype should be cleaned of small duplication, dead code, and undocumented prototype assumptions.

Next Step:
Perform Version 2 UX review and visual polish.

## Round 32 - Localhost Frontend Server

Status:
Completed

Completed:
- Added localhost frontend server
- Updated launcher
- Opens frontend through localhost
- Preserved FastAPI integration

Rationale:
Serving frontend through localhost provides a more realistic product experience than opening raw HTML files.

Next Step:
Perform Version 2 UX review and visual polish.

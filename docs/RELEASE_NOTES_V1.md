# Release Notes - Version 1

## Version Name

```text
FairMatch AI v1.0 - Stable FYP Version
```

## Release Date

```text
2026-06-11
```

## Release Summary

FairMatch AI v1.0 is the stable FYP release of the School Mode allocation engine and product demonstration experience.

This version focuses on:

- School Mode student-to-project allocation
- fairness-aware optimisation
- structured explanation output
- counterfactual fairness comparison
- CLI and Streamlit product demonstration
- validation and runtime verification

The allocation engine is considered complete for Version 1.

## Completed Features

### Core Allocation Engine

- Python backend package
- Google OR-Tools CP-SAT solver
- School Mode allocation
- project capacity constraints
- skill eligibility constraints
- supervisor limit constraints
- student workload limit constraints
- preference-based satisfaction scoring
- fixed preference scoring scale:
  - first choice = 3
  - second choice = 2
  - third choice = 1
  - unranked = 0

### Fairness Layer

- satisfaction gap
- max-min value
- total satisfaction
- average satisfaction
- Gini coefficient
- workload gap reporting

### Explanation Layer

- structured `ExplanationDetail` model
- assignment summary
- first-choice note
- capacity note
- skill note
- supervisor note
- fairness note
- workload note

### Counterfactual Fairness Comparison

- baseline run with `fairness_weight = 0`
- fairness-aware run with `fairness_weight > 0`
- changed assignment detection
- changed satisfaction detection
- fairness metric comparison

### CLI

- text output mode
- JSON output mode
- normal allocation command
- counterfactual fairness comparison command
- warning when fairness comparison weight is 0

### Streamlit Product Experience

- premium landing page
- product value sections
- problem section
- architecture section
- decision support workspace
- Overview tab
- Allocation tab
- Fairness tab
- Explanations tab
- Comparison tab
- sample dataset selection
- custom JSON upload

## Validation Status

Validation documents:

- `docs/VALIDATION_REPORT.md`
- `docs/FAIRNESS_EVALUATION.md`
- `docs/EXPLANATION_ENGINE.md`

Automated validation covers:

- solver happy path
- skill eligibility blocking
- fixed satisfaction scoring
- infeasible workload case
- School Mode edge cases
- insufficient capacity validation
- skill gap infeasibility
- supervisor limit infeasibility
- workload limit infeasibility
- invalid preference reference validation
- fairness metric helpers
- controlled fairness-weight comparison
- counterfactual fairness comparison
- CLI text and JSON output

Current test status:

```text
24 tests passing
```

## Runtime Verification Status

Runtime verification document:

- `docs/RUNTIME_VERIFICATION.md`

Verified:

- Python 3.11.9 environment
- OR-Tools installation
- pytest installation
- compile verification
- full test suite
- CLI text output
- CLI JSON output
- counterfactual text output
- counterfactual JSON output

## Dashboard Features

The Streamlit dashboard is a presentation layer only. It does not implement optimisation logic.

Dashboard capabilities:

- premium product landing page
- Start Experience flow
- scenario setup
- sample dataset selection
- custom JSON upload
- allocation result table
- executive overview cards
- fairness metric cards
- structured explanation cards
- fairness comparison cards

## Known Limitations

- Work Mode is documented but not completed for Version 1.
- Supervisor fairness is not yet reported as a separate soft metric.
- Workload counterfactual comparison is not yet implemented.
- First-choice rejection explanations identify likely factors but are not full causal proofs.
- Pareto frontier analysis is not implemented.
- What-if simulation is not implemented.
- PDF report export is not implemented.
- The Streamlit dashboard is single-user and local-first.

## Future Work

Future work is documented in:

- `docs/FUTURE_WORK.md`
- `docs/VERSION2_ROADMAP.md`

Planned Version 2 exploration areas:

- React or Next.js frontend
- FastAPI backend
- PostgreSQL data layer
- supervisor fairness metric
- counterfactual workload comparison
- what-if simulation
- PDF reports
- multi-user accounts

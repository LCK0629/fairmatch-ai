# FYP Report Mapping

## Purpose

This document maps the existing FairMatch AI project assets to a standard FYP report structure.

It does not write the final report. It identifies which project materials can support each chapter, what content is still missing, and what visuals should be prepared.

## Chapter 1 - Introduction

Suggested chapter focus:

- problem statement
- motivation
- objectives
- project scope

### Existing Project Assets Available

- `README.md`
  - high-level project description
  - product positioning paragraph
  - School Mode and Work Mode summary
- `docs/PROJECT_CONTEXT.md`
  - FYP topic code
  - main FYP scope
  - problem statement
  - target users
  - School Mode priority
  - Work Mode future extension position
- `docs/PRODUCT_STORY.md`
  - product narrative
  - problem framing
  - stakeholder value
  - product positioning
- `docs/DEMO_SCRIPT.md`
  - opening script
  - key message
  - project goal

### Missing Content Still Required

- Formal research aim statement.
- Numbered project objectives.
- Clear project scope and out-of-scope list.
- Short background on why student-project allocation matters in university settings.
- Brief statement of expected contribution.

### Recommended Screenshots

- FairMatch AI landing page.
- Dashboard first screen showing product workspace.

### Recommended Tables

- Table: Project objectives and how FairMatch AI addresses each one.
- Table: Stakeholders and expected benefits.
- Table: Scope boundaries: included vs deferred.

### Recommended Diagrams

- Problem context diagram:

```text
Students
  ->
Limited Projects
  ->
Supervisor Constraints
  ->
Fairness and Explanation Requirements
```

- Product positioning diagram:

```text
Optimisation + Fairness + Explanation + Counterfactual Analysis
```

## Chapter 2 - Literature Review

Suggested chapter focus:

- allocation systems
- fairness in allocation
- explainable decision support
- optimisation systems

### Existing Project Assets Available

- `docs/PROJECT_CONTEXT.md`
  - explains why constraint optimisation is suitable
  - states that FairMatch AI is not an LLM recommendation system
- `docs/PRODUCT_STORY.md`
  - explains why traditional manual allocation is insufficient
  - positions transparency and fairness as product needs
- `docs/FUTURE_WORK.md`
  - identifies future research extensions such as Pareto frontier analysis and what-if simulation
- `docs/VALIDATION_REPORT.md`
  - documents fairness metrics and solver behaviour

### Missing Content Still Required

This chapter still needs external academic and technical sources. Topics to discuss:

- student-project allocation problem
- matching and assignment systems
- constraint programming and optimisation
- Google OR-Tools CP-SAT or CP-SAT-style optimisation
- fairness-aware allocation
- satisfaction-based fairness metrics
- Gini coefficient in allocation or inequality measurement
- explainable decision support systems
- counterfactual explanation or counterfactual analysis in decision support
- workload balancing in scheduling and allocation

Do not treat current project documentation as literature review evidence. It can guide the structure, but Chapter 2 should cite external sources.

### Recommended Screenshots

- Usually no application screenshots are needed in the literature review.
- Optional: conceptual figure comparing traditional allocation and fairness-aware decision support.

### Recommended Tables

- Table: Comparison of allocation approaches.
  - manual allocation
  - preference-only allocation
  - optimisation-based allocation
  - fairness-aware optimisation
- Table: Fairness metric concepts.
  - satisfaction gap
  - max-min value
  - Gini coefficient
- Table: Explainability methods relevant to decision support.

### Recommended Diagrams

- Literature concept map:

```text
Allocation Problem
  ->
Optimisation
  ->
Fairness Metrics
  ->
Explainable Decision Support
```

- Comparison diagram:

```text
Traditional Assignment
  -> final allocation only

FairMatch AI Approach
  -> allocation + fairness + explanation + comparison
```

## Chapter 3 - System Design

Suggested chapter focus:

- architecture
- data model
- constraints
- fairness model
- explanation engine

### Existing Project Assets Available

- `docs/PROJECT_CONTEXT.md`
  - system scope
  - stakeholder requirements
  - transparency requirements
- `docs/ARCHITECTURE.md`
  - architecture flow if included in the repository
- `docs/DATA_MODEL.md`
  - data model details if included in the repository
- `docs/CONSTRAINTS.md`
  - hard constraints
  - soft constraints
  - objective design
- `docs/SYSTEM_FLOW.md`
  - flow from input to result if included in the repository
- `docs/EXPLANATION_ENGINE.md`
  - structured explanation schema and limitations
- `docs/FAIRNESS_EVALUATION.md`
  - fairness metric definitions and comparison if included in the repository
- `docs/PRODUCT_STORY.md`
  - non-technical product flow
- `app.py`
  - dashboard flow: landing page, scenario panel, tabbed workspace

### Missing Content Still Required

- Formal system architecture diagram.
- Formal data flow diagram.
- Entity relationship or JSON schema-style diagram for:
  - students
  - projects
  - preferences
  - supervisor limits
  - allocation result
  - explanation detail
- Clear explanation of hard constraints vs soft constraints.
- Mathematical notation for key decision variables and objective function.
- Design rationale for choosing School Mode first.

### Recommended Screenshots

- Dashboard scenario panel.
- Allocation tab with assignment table and decision detail panel.
- Fairness tab with metric cards.
- Counterfactual tab.

### Recommended Tables

- Table: Data fields and purpose.
- Table: Hard constraints.
  - exactly one project per student
  - project capacity
  - skill eligibility
  - supervisor limits
  - workload limits
- Table: Soft objectives.
  - total satisfaction
  - fairness gap penalty
  - workload gap penalty
- Table: Explanation fields.
  - summary
  - first-choice note
  - skill note
  - capacity note
  - fairness note
  - workload note

### Recommended Diagrams

Main architecture diagram:

```text
Input Data
  ->
Data Loader / Validator
  ->
Scoring Engine
  ->
OR-Tools CP-SAT Model Builder
  ->
Solver
  ->
Fairness Evaluator
  ->
Explanation Engine
  ->
Counterfactual Comparison
  ->
Dashboard
```

Simplified report diagram:

```text
Input
  ->
Solver
  ->
Fairness
  ->
Explanation
  ->
Dashboard
```

## Chapter 4 - Implementation

Suggested chapter focus:

- OR-Tools solver
- fairness helper layer
- counterfactual module
- Streamlit dashboard

### Existing Project Assets Available

- `backend/fairmatch/solver.py`
  - OR-Tools CP-SAT model
  - hard constraints
  - objective function
  - assignment explanation construction
- `backend/fairmatch/models.py`
  - data classes
  - allocation input/result models
  - structured `ExplanationDetail`
- `backend/fairmatch/fairness.py`
  - satisfaction gap
  - max-min value
  - total satisfaction
  - average satisfaction
  - Gini coefficient
- `backend/fairmatch/counterfactual.py`
  - baseline vs fairness-aware comparison helper
- `backend/fairmatch/cli.py`
  - text output
  - JSON output
  - counterfactual CLI mode
- `app.py`
  - Streamlit dashboard
  - landing page
  - scenario panel
  - allocation, fairness, counterfactual, and dataset tabs
- `data/school_sample.json`
  - main School Mode sample dataset
- `data/school_cases/fairness_weight_tradeoff.json`
  - controlled fairness comparison dataset
- `README.md`
  - setup and run commands

### Missing Content Still Required

- Short implementation environment section.
- Clear module-by-module implementation explanation.
- Selected code snippets for key functions.
- Explanation of why UI does not duplicate solver logic.
- Explanation of why backend logic remains separate from Streamlit presentation.

### Recommended Screenshots

- CLI text output showing fairness metrics.
- CLI JSON output sample if useful.
- Streamlit landing page.
- Streamlit allocation tab.
- Streamlit fairness tab.
- Streamlit counterfactual tab.

### Recommended Tables

- Table: Implementation modules and responsibilities.
  - `models.py`
  - `solver.py`
  - `fairness.py`
  - `counterfactual.py`
  - `cli.py`
  - `app.py`
- Table: Dataset files and purpose.
- Table: CLI commands and expected output.

### Recommended Diagrams

- Module interaction diagram:

```text
models.py
  ->
solver.py
  ->
fairness.py
  ->
counterfactual.py
  ->
cli.py / app.py
```

- Dashboard flow diagram:

```text
Landing Page
  ->
Scenario Panel
  ->
Allocation Tab
  ->
Fairness Tab
  ->
Counterfactual Tab
```

## Chapter 5 - Evaluation

Suggested chapter focus:

- validation report
- runtime verification
- fairness metrics
- controlled fairness comparison
- test suite

### Existing Project Assets Available

- `docs/VALIDATION_REPORT.md`
  - solver field audit
  - fairness weight behaviour
  - structured explanation status
  - counterfactual comparison status
  - CLI demonstration status
- `docs/RUNTIME_VERIFICATION.md`
  - Python version
  - package versions
  - compile verification
  - pytest result
  - CLI output verification
  - JSON output verification
  - counterfactual output verification
- `tests/`
  - solver tests
  - school case tests
  - fairness metric tests
  - CLI tests
- `data/school_cases/`
  - edge case datasets
  - controlled fairness trade-off dataset
- `docs/FAIRNESS_EVALUATION.md`
  - fairness metric comparison if included in the repository

### Missing Content Still Required

- Evaluation methodology section.
- Explanation of test categories.
- Summary of datasets used for validation.
- Tables of test cases and expected outcomes.
- Discussion of limitations:
  - fairness notes are objective-aware, not full causal proof
  - supervisor fairness metric is deferred
  - workload counterfactual comparison is deferred
  - Work Mode is future extension
- Interpretation of fairness trade-off results.

### Recommended Screenshots

- Test suite result showing `24 passed`.
- Runtime verification command output.
- CLI normal allocation output.
- CLI counterfactual output.
- Dashboard fairness metric cards.
- Dashboard counterfactual comparison.

### Recommended Tables

- Table: Test suite summary.
  - test file
  - purpose
  - number of tests
  - result
- Table: Runtime environment.
  - OS
  - Python version
  - OR-Tools version
  - pytest version
- Table: Fairness metrics and interpretation.
  - satisfaction gap
  - max-min value
  - Gini coefficient
- Table: Controlled fairness comparison.
  - baseline total satisfaction
  - fairness total satisfaction
  - baseline fairness gap
  - fairness fairness gap
  - changed assignments
- Table: Edge case datasets and validation purpose.

### Recommended Diagrams

- Evaluation pipeline:

```text
Sample Data
  ->
Solver Run
  ->
Metrics
  ->
Tests
  ->
Runtime Verification
```

- Counterfactual comparison diagram:

```text
fairness_weight = 0
  vs
fairness_weight > 0
  ->
compare assignments and fairness metrics
```

## Chapter 6 - Conclusion and Future Work

Suggested chapter focus:

- achievements
- limitations
- future work backlog

### Existing Project Assets Available

- `docs/FUTURE_WORK.md`
  - supervisor fairness metric
  - counterfactual workload comparison
  - first-choice counterfactual proof
  - Pareto frontier analysis
  - what-if simulation
  - Streamlit dashboard status
  - PDF report export
- `docs/PRODUCT_STORY.md`
  - future vision
  - product-level summary
- `docs/VALIDATION_REPORT.md`
  - limitations and recommended next steps
- `docs/DEVELOPMENT_LOG.md`
  - implementation progress by round
- `docs/PROJECT_CONTEXT.md`
  - scope and Work Mode position

### Missing Content Still Required

- Concise conclusion paragraph.
- Summary of achieved objectives.
- Explicit contribution statement.
- Honest limitation discussion.
- Future work prioritisation.
- Reflection on what was learned from validation.

### Recommended Screenshots

- Final dashboard screenshot.
- Optional roadmap screenshot or future work slide.

### Recommended Tables

- Table: Objectives achieved.
- Table: Limitations and mitigation.
- Table: Future work priority.
  - Priority A: planned enhancements
  - Priority B: research extensions
  - Priority C: presentation features

### Recommended Diagrams

- Future roadmap:

```text
Current Core
  ->
Supervisor Fairness
  ->
Workload Counterfactual
  ->
What-If Simulation
  ->
PDF Reporting
```

- Final contribution summary:

```text
Valid Allocation
  +
Fairness Evaluation
  +
Structured Explanation
  +
Counterfactual Comparison
```

## Cross-Chapter Asset Index

### Documents

- `README.md`: overview, setup, product positioning, dashboard run instructions
- `docs/PROJECT_CONTEXT.md`: problem, scope, target users, School Mode priority
- `docs/PRODUCT_STORY.md`: product narrative and stakeholder value
- `docs/PRESENTATION_OUTLINE.md`: slide structure and recommended visuals
- `docs/DEMO_SCRIPT.md`: live demo sequence and explanation wording
- `docs/FUTURE_WORK.md`: future enhancement backlog
- `docs/VALIDATION_REPORT.md`: solver and validation findings
- `docs/RUNTIME_VERIFICATION.md`: environment and runtime proof
- `docs/DEVELOPMENT_LOG.md`: implementation timeline

### Code Files

- `backend/fairmatch/models.py`: data and result models
- `backend/fairmatch/solver.py`: allocation solver
- `backend/fairmatch/fairness.py`: fairness metric helpers
- `backend/fairmatch/counterfactual.py`: fairness comparison helper
- `backend/fairmatch/cli.py`: CLI output
- `app.py`: Streamlit dashboard

### Data and Tests

- `data/school_sample.json`: main demo dataset
- `data/school_cases/fairness_weight_tradeoff.json`: controlled fairness comparison
- `tests/`: automated validation suite

## Next Recommended Report Preparation Step

Create the actual Chapter 1 draft first.

Reason:
The problem statement, motivation, objectives, and scope are already well supported by:

- `docs/PROJECT_CONTEXT.md`
- `docs/PRODUCT_STORY.md`
- `README.md`
- `docs/DEMO_SCRIPT.md`

After Chapter 1, prepare Chapter 3 diagrams because the architecture, data model, constraints, fairness model, and explanation engine already exist in the project assets.

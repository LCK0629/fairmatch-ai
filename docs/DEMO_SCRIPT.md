# FYP Demo Script

## Demo Title

FairMatch AI: Explainable Fairness-Aware Project Allocation Engine

FYP topic:

```text
CSIT-26-S3-06: Intelligent Scheduling and Allocation System with Fairness Constraints
```

## Demo Goal

Show that FairMatch AI can:

- allocate students to projects
- respect hard constraints
- optimise preference satisfaction
- measure fairness
- explain allocation decisions
- compare fairness-aware and non-fairness allocations

## Key Message

FairMatch AI is not an LLM recommendation system.

It is a constraint optimisation and decision support platform using Google OR-Tools CP-SAT.

The system focuses on:

1. School Mode
2. Fairness
3. Explanation
4. Validation

The Streamlit dashboard is a lightweight presentation layer on top of the verified backend.

## Pre-Demo Setup

Open a terminal in the project folder:

```powershell
cd C:\Users\cheek\Projects\fairMatch
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the dashboard:

```powershell
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Suggested Timing

Total demo time:

```text
6 to 8 minutes
```

Suggested split:

- 1 minute: project problem and goal
- 2 minutes: normal allocation
- 2 minutes: explanations and fairness metrics
- 2 minutes: counterfactual fairness comparison
- 1 minute: validation and future work

## Opening Script

Say:

```text
This project is FairMatch AI, an explainable fairness-aware allocation system for CSIT-26-S3-06.

The main use case is School Mode, where students need to be allocated to projects.

Manual allocation can be unfair or hard to justify because it must consider student preferences, project capacity, required skills, supervisor workload, and fairness at the same time.

FairMatch AI models this as a constraint optimisation problem using Google OR-Tools CP-SAT.
```

Then say:

```text
The goal is not to replace human decision makers.
The goal is to provide a transparent decision support system that produces valid allocations, reports fairness metrics, and explains why assignments were made.
```

## Dashboard Overview

Action:

Open the Streamlit dashboard.

Point out:

- product-style landing page
- `Start` button
- dataset selection in the sidebar
- sample dataset options
- custom JSON upload
- `Run Allocation`
- `Run Fairness Comparison`

Say:

```text
The app starts with a product-style landing page and then moves into the dashboard.
The dashboard is intentionally lightweight.
The optimisation logic is not implemented inside the UI.
It reuses the existing backend functions: load_allocation_input, solve_allocation, and compare_fairness_runs.
```

Action:

Click:

```text
Start
```

Expected result:

The product dashboard opens.

## Demo Part 1: Normal Allocation

Action:

1. Select:

```text
School Sample
```

2. Click:

```text
Run Allocation
```

Expected result:

The dashboard displays:

- solver status
- fairness metrics
- allocation table
- explanation expanders

Say:

```text
Here the solver has produced an optimal allocation.
Each student is assigned to exactly one project, and every project capacity constraint is respected.
```

Point to the assignment table.

Say:

```text
The table shows the main allocation result: student, assigned project, satisfaction score, and preference rank.
The satisfaction score is based on a fixed scoring scale:
first choice is 3, second choice is 2, third choice is 1, and unranked is 0.
```

## Demo Part 2: Fairness Metrics

Action:

Point to the fairness metric cards.

Explain each metric briefly:

```text
Total satisfaction shows the overall preference score.
Average satisfaction shows the average student outcome.
Fairness gap measures the difference between the most satisfied and least satisfied student.
Max-min value shows the worst student outcome.
Gini coefficient measures inequality across the full satisfaction distribution.
Workload gap shows the spread in assigned workload.
```

Say:

```text
The system does not only maximise total satisfaction.
It also reports whether outcomes are balanced across students.
This is important because a high total score can still hide unfair individual outcomes.
```

## Demo Part 3: Explanation Engine

Action:

Open one or two explanation expanders.

Recommended examples:

- one student who received first choice
- one student who did not receive first choice

Say:

```text
Each assignment includes a structured explanation.
The explanation includes a summary, first-choice note, fairness note, and workload note.
```

For a first-choice assignment, say:

```text
For this student, the system explains that the assigned project was the student's first choice.
It also confirms that fairness and workload objectives were part of the optimisation run.
```

For a non-first-choice assignment, say:

```text
For this student, the system explains why the first choice was not assigned.
For example, the first-choice project may have reached capacity, or supervisor limits may have affected the feasible allocation set.
```

Important clarification:

```text
Some explanation notes are direct constraint checks, such as capacity or skill eligibility.
Fairness and workload notes are objective-aware explanations.
They indicate that those objectives may have influenced the result, but they are not always individual causal proof.
```

## Demo Part 4: Counterfactual Fairness Comparison

Action:

1. Select:

```text
Fairness Weight Trade-Off
```

2. Keep comparison fairness weight as:

```text
3
```

3. Click:

```text
Run Fairness Comparison
```

Expected result:

The dashboard displays:

- total satisfaction before and after fairness weighting
- fairness gap before and after fairness weighting
- Gini coefficient before and after fairness weighting
- max-min value before and after fairness weighting
- whether fairness improved
- changed assignments
- changed satisfaction

Say:

```text
This is the counterfactual fairness comparison.
The system compares a baseline run with fairness_weight = 0 against a fairness-aware run with fairness_weight = 3.
```

Then say:

```text
This gives stronger evidence than simply saying fairness was active.
It shows whether changing the fairness weight actually changed assignments and fairness metrics.
```

Point to changed assignments.

Say:

```text
Here we can see which students changed project between the baseline and fairness-aware run.
```

Point to changed satisfaction.

Say:

```text
We can also see how each changed student's satisfaction score changed.
This makes the fairness trade-off transparent.
```

Explain the trade-off:

```text
In this controlled case, total satisfaction may decrease, but the fairness gap and Gini coefficient improve.
This demonstrates the trade-off between maximising total preference satisfaction and reducing unfair outcome distribution.
```

## Demo Part 5: Validation

Say:

```text
The backend has been runtime verified.
The test suite passed with 24 tests.
The tests cover solver behaviour, school edge cases, fairness metrics, explanations, counterfactual comparison, and CLI output.
```

Mention:

```text
The project also includes runtime verification documentation that records the environment, dependency versions, compile verification, pytest results, CLI output, JSON output, and counterfactual output.
```

## Demo Part 6: Future Work

Say:

```text
The current project focuses on the core School Mode allocation engine, fairness, explanation, and validation.
```

Then mention intentionally deferred work:

- supervisor fairness metric
- counterfactual workload comparison
- first-choice counterfactual proof
- Pareto frontier analysis
- what-if simulation
- PDF report export

Say:

```text
These are documented as future work because the priority was to build a credible and validated allocation engine first, before adding advanced research extensions or presentation features.
```

## Closing Script

Say:

```text
To conclude, FairMatch AI demonstrates how constraint optimisation can support fair and explainable student-project allocation.

It produces valid allocations, reports fairness metrics, explains individual assignments, and compares fairness-aware decisions against a non-fairness baseline.

The main contribution is a transparent decision support workflow for allocation problems where fairness and explainability matter.
```

## Backup CLI Demo

If the dashboard does not open, use the CLI.

Normal allocation:

```powershell
python -m backend.fairmatch.cli data\school_sample.json
```

JSON output:

```powershell
python -m backend.fairmatch.cli data\school_sample.json --output json
```

Counterfactual comparison:

```powershell
python -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness
```

Counterfactual JSON:

```powershell
python -m backend.fairmatch.cli data\school_cases\fairness_weight_tradeoff.json --compare-fairness --output json
```

## Demo Checklist

Before presenting:

- confirm `.venv` is activated
- confirm `streamlit run app.py` starts
- confirm dashboard opens at `http://localhost:8501`
- click `Start`
- select `School Sample`
- click `Run Allocation`
- open at least one explanation expander
- select `Fairness Weight Trade-Off`
- click `Run Fairness Comparison`
- explain assignment changes and fairness metric changes

## Common Questions

### Is this an AI chatbot or LLM system?

No. FairMatch AI is a constraint optimisation system using Google OR-Tools CP-SAT.

### Does the system guarantee every student gets their first choice?

No. Project capacity, skill eligibility, supervisor limits, workload limits, and fairness trade-offs may prevent that.

### Why can total satisfaction decrease in the fairness-aware run?

Because fairness weighting may choose a more balanced allocation even if the total preference score is slightly lower.

### Does the dashboard contain optimisation logic?

No. The dashboard calls the existing backend solver and comparison helpers.

### Is Work Mode completed?

No. Work Mode is documented as a future extension. The FYP scope prioritises School Mode.

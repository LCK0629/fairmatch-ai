# Product Story: FairMatch AI

## What Problem Are We Solving?

Universities often allocate students to projects manually. This process looks simple at first, but it becomes difficult when many students compete for limited project places and every project has different capacity, skill, and supervision requirements.

Common challenges include:

- popular projects become oversubscribed
- some students consistently receive poor outcomes
- supervisors may become overloaded
- allocation decisions are difficult to justify
- fairness is difficult to measure

Traditional allocation approaches are often insufficient because they focus mainly on producing a final assignment list. They may not show whether the outcome is fair, why a student did not receive a preferred project, or whether a supervisor workload issue influenced the decision.

Manual spreadsheets can record decisions, but they do not naturally explain trade-offs. Simple first-come-first-served or preference-only methods can also create unfair outcomes when capacity, skills, and workload constraints interact.

FairMatch AI addresses this gap by treating allocation as a decision support problem, not only a matching problem.

## What Is FairMatch AI?

FairMatch AI is:

```text
An Explainable Fairness-Aware Allocation Platform
```

It is not:

```text
Just an allocation algorithm
```

FairMatch AI combines:

- optimisation
- fairness evaluation
- transparent explanations
- counterfactual analysis

The platform helps decision makers create valid allocations, inspect whether outcomes are balanced, understand why decisions were made, and compare fairness-aware outcomes against baseline alternatives.

FairMatch AI is also not an LLM recommendation system. It does not guess allocations from prompts. It uses structured input data, explicit constraints, measurable objectives, and explainable outputs.

## Who Uses FairMatch AI?

Primary user:

```text
University administrators
```

University administrators need a reliable way to coordinate student-project allocation across many stakeholders. FairMatch AI helps them produce allocations that are valid, fairer, and easier to defend.

Secondary users:

```text
Academic coordinators
Supervisors
Students
```

Academic coordinators benefit because the system gives them a repeatable allocation workflow and clear decision evidence.

Supervisors benefit because supervisor capacity and workload limits can be included in the allocation process, reducing the risk of uneven supervision loads.

Students benefit because preferences and skill eligibility are considered explicitly, and allocation decisions can be explained rather than appearing arbitrary.

## How Does It Work?

FairMatch AI follows a simple decision support flow:

```text
Input Data
↓
Constraint Solver
↓
Fairness Evaluation
↓
Explanation Engine
↓
Counterfactual Analysis
↓
Decision Support Dashboard
```

Users provide structured allocation data such as students, projects, preferences, skills, project capacity, and supervisor limits.

The solver creates a valid allocation based on the rules.

Fairness evaluation then measures whether satisfaction is evenly distributed.

The explanation engine describes assignment outcomes in human-readable form.

Counterfactual analysis compares baseline and fairness-aware runs so users can see whether fairness weighting changed the result.

The dashboard presents these outputs in a product-style workflow for review and demonstration.

## What Makes It Different?

Traditional allocation systems:

- produce assignments

FairMatch AI:

- produces assignments
- measures fairness
- explains decisions
- compares alternative outcomes

This difference matters because allocation decisions affect real students and real academic workloads. A final assignment list is not enough when stakeholders ask why one student received a project and another did not.

Transparency helps decision makers justify outcomes, identify trade-offs, and communicate allocation decisions more responsibly. It also reduces the risk that fairness is treated as a vague intention instead of a measurable part of the process.

## Core Product Pillars

### Fair Allocation

FairMatch AI balances preferences, skills, workload, and capacity. It does not only chase the highest total satisfaction score; it also reports whether satisfaction is distributed fairly across students.

### Transparent Decisions

Every assignment includes explanation details. Users can inspect preference rank, satisfaction score, skill eligibility, first-choice notes, fairness notes, and workload notes.

### Counterfactual Analysis

FairMatch AI helps users understand how fairness changes outcomes. By comparing a baseline allocation with a fairness-aware allocation, the platform shows whether assignments, satisfaction scores, and fairness metrics changed.

## Example Scenario

Imagine a school allocation round with:

```text
100 students
20 projects
5 supervisors
```

Without FairMatch AI, administrators may need to manually compare student preferences, project capacities, required skills, and supervisor availability. Popular projects can quickly become oversubscribed, and it may be hard to notice whether some students are consistently receiving weaker outcomes.

With FairMatch AI, the allocation process becomes more structured:

- students and projects are loaded as input data
- the solver creates a valid allocation
- fairness metrics show whether outcomes are balanced
- explanations help justify individual assignments
- counterfactual comparison shows what changed when fairness was prioritised

The result is not just a list of assignments. It is a decision package that supports review, discussion, and presentation.

## Future Vision

Future enhancements are documented in `docs/FUTURE_WORK.md`.

Planned and possible future improvements include:

- supervisor fairness metrics
- workload comparison
- what-if simulation
- PDF reports

These are future enhancements, not missing core functionality. The current project prioritises the foundation first:

1. School Mode
2. Fairness
3. Explanation
4. Validation

Once that foundation is stable, FairMatch AI can grow into a richer decision support platform with deeper simulation, reporting, and presentation features.

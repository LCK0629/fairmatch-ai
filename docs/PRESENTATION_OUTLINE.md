# FairMatch AI Presentation Outline

Suggested duration:

```text
8 to 10 minutes
```

Presentation goal:

Show FairMatch AI as an explainable fairness-aware allocation platform for university student-project allocation.

## Slide 1 - Problem

Objective:
Introduce why student-project allocation is a real decision problem, not only an administrative task.

Key talking points:

- Universities often allocate students to projects manually.
- Manual allocation becomes difficult when many students compete for limited places.
- The process must consider preferences, skills, project capacity, supervisor limits, and fairness at the same time.
- A final assignment list is not enough if stakeholders cannot understand or justify the decisions.

Recommended visuals/screenshots:

- Simple diagram showing students competing for limited project slots.
- Screenshot of the FairMatch AI landing page title.
- Optional visual: `100 students -> 20 projects -> 5 supervisors`.

## Slide 2 - Existing Challenges

Objective:
Show the specific allocation pain points that FairMatch AI addresses.

Key talking points:

- Popular projects can become oversubscribed.
- Some students may consistently receive poor outcomes.
- Supervisors may become overloaded.
- Decisions can be difficult to explain after allocation is complete.
- Fairness is hard to measure using spreadsheets or informal manual review.

Recommended visuals/screenshots:

- Four challenge cards:
  - Oversubscribed projects
  - Unfair outcomes
  - Supervisor constraints
  - Lack of transparency
- Optional screenshot or mock table showing competing preferences.

## Slide 3 - FairMatch AI

Objective:
Position FairMatch AI as a product, not just a solver.

Key talking points:

- FairMatch AI is an Explainable Fairness-Aware Allocation Platform.
- It is not just an allocation algorithm.
- It is not an LLM recommendation system.
- It combines optimisation, fairness evaluation, transparent explanations, and counterfactual analysis.
- The goal is to support decision makers, not replace them.

Recommended visuals/screenshots:

- Product positioning statement:

```text
FairMatch AI
Explainable Fairness-Aware Allocation Platform
```

- Screenshot of the product-style landing page.
- Simple product capability row: Optimisation, Fairness, Explanation, Counterfactual.

## Slide 4 - Core Product Pillars

Objective:
Explain the three main product pillars clearly before showing system details.

Key talking points:

- Fair Allocation:
  Balance student preferences, skills, project capacity, supervisor workload, and fairness.
- Transparent Decisions:
  Each assignment includes structured explanation details.
- Counterfactual Analysis:
  Compare baseline and fairness-aware runs to understand how fairness changes outcomes.

Recommended visuals/screenshots:

- Three-pillar layout:
  - Fair Allocation
  - Transparent Decisions
  - Counterfactual Analysis
- Screenshot of dashboard tabs: Allocation, Fairness, Counterfactual, Dataset.

## Slide 5 - System Architecture

Objective:
Explain the system flow in a simple, non-technical way.

Key talking points:

- Users provide structured input data.
- The solver creates a valid allocation.
- Fairness evaluation measures satisfaction distribution.
- The explanation engine describes assignment decisions.
- Counterfactual analysis compares baseline and fairness-aware outcomes.
- The dashboard presents the results for review.

Recommended visuals/screenshots:

```text
Input Data
  ->
Solver
  ->
Fairness
  ->
Explanation
  ->
Dashboard
```

Optional expanded flow:

```text
Input Data
  ->
Constraint Solver
  ->
Fairness Evaluation
  ->
Explanation Engine
  ->
Counterfactual Analysis
  ->
Decision Support Dashboard
```

## Slide 6 - Fairness Evaluation

Objective:
Show how FairMatch AI makes fairness measurable.

Key talking points:

- Fairness is not treated as a vague idea.
- Satisfaction Gap measures the difference between the highest and lowest satisfaction score.
- Max-Min value shows the worst student outcome.
- Gini coefficient measures inequality across the satisfaction distribution.
- These metrics help decision makers compare allocation quality beyond total satisfaction.

Recommended visuals/screenshots:

- Screenshot of the Fairness tab with metric cards.
- Small metric explanation table:
  - Satisfaction Gap: spread between best and worst outcomes
  - Max-Min: lowest individual satisfaction
  - Gini: inequality across outcomes

## Slide 7 - Explanation Engine

Objective:
Demonstrate transparent decision logic for individual assignments.

Key talking points:

- The system does not only return final assignments.
- Each assignment includes structured explanation fields.
- Explanations include preference rank, satisfaction score, skill eligibility, first-choice notes, fairness notes, and workload notes.
- First-choice notes help explain why a student may not receive their top project.
- Current explanations identify constraint and objective factors; full causal proof is future work.

Recommended visuals/screenshots:

- Screenshot of the Allocation tab showing the assignment table and Decision Detail panel.
- Highlight one example:
  - Student assigned project
  - Preference rank
  - First-choice note
  - Fairness/workload notes

## Slide 8 - Counterfactual Comparison

Objective:
Show how FairMatch AI evaluates whether fairness weighting changes the outcome.

Key talking points:

- The system compares two allocation runs:

```text
baseline: fairness_weight = 0
fairness-aware: fairness_weight > 0
```

- This shows whether fairness actually changed assignments or satisfaction distribution.
- The comparison reports total satisfaction, fairness gap, max-min value, Gini coefficient, changed assignments, and changed satisfaction.
- This makes fairness trade-offs easier to explain.

Recommended visuals/screenshots:

- Screenshot of the Counterfactual tab.
- Before/after metric cards:
  - Total satisfaction
  - Fairness gap
  - Gini coefficient
- Small changed assignments table.

## Slide 9 - Live Demo

Objective:
Demonstrate the product flow using the Streamlit dashboard.

Key talking points:

- Start from the landing page.
- Enter the dashboard.
- Select `School Sample`.
- Run allocation.
- Show allocation table and one explanation detail.
- Open the Fairness tab and explain metric cards.
- Select `Fairness Weight Trade-Off`.
- Run fairness comparison.
- Open Counterfactual tab and explain changed outcomes.

Recommended visuals/screenshots:

- Live dashboard preferred.
- Backup screenshots:
  - Landing page
  - Allocation tab
  - Fairness tab
  - Counterfactual tab

Timing suggestion:

```text
2 to 3 minutes
```

## Slide 10 - Future Work

Objective:
Clarify what is intentionally deferred and why.

Key talking points:

- The current project prioritises School Mode, fairness, explanation, and validation.
- Future enhancements are documented, not missing core functionality.
- Planned and possible future work:
  - supervisor fairness metric
  - workload comparison
  - first-choice counterfactual proof
  - what-if simulation
  - PDF report export
- These would extend the platform after the core allocation engine remains stable.

Recommended visuals/screenshots:

- Roadmap style list:
  - Core complete
  - Advanced fairness analysis
  - What-if simulation
  - Reporting/export

## Slide 11 - Conclusion

Objective:
End with the main contribution and why it matters.

Key talking points:

- FairMatch AI turns project allocation into a transparent decision support workflow.
- It produces valid assignments.
- It measures fairness.
- It explains decisions.
- It compares fairness-aware outcomes against a baseline.
- The main contribution is not only optimisation, but explainable fairness-aware allocation for academic decision making.

Recommended visuals/screenshots:

- Final summary graphic:

```text
Valid Allocation
  +
Fairness Metrics
  +
Decision Explanations
  +
Counterfactual Evidence
```

- Closing screenshot of the product dashboard.

## Timing Plan

Suggested timing:

- Slide 1: 45 seconds
- Slide 2: 45 seconds
- Slide 3: 60 seconds
- Slide 4: 60 seconds
- Slide 5: 60 seconds
- Slide 6: 60 seconds
- Slide 7: 60 seconds
- Slide 8: 60 seconds
- Slide 9: 2 to 3 minutes
- Slide 10: 45 seconds
- Slide 11: 30 seconds

Total:

```text
8 to 10 minutes
```

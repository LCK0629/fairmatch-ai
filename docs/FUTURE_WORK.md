# Future Work Backlog

## Purpose

This document records future enhancements that are intentionally deferred.

FairMatch AI prioritised the core FYP delivery in this order:

1. School Mode
2. Fairness
3. Explanation
4. Validation

Advanced research extensions and presentation features are valuable, but they should not weaken the core allocation engine. The deferred items below are documented as future work, not missing requirements.

## Priority A - Planned Enhancements

These items directly strengthen the current School Mode allocation engine and explanation system.

### Supervisor Fairness Metric

Description:
Add a metric that measures how evenly students are distributed across supervisors, not only whether each supervisor stays below a hard limit.

Motivation:
The current solver supports `supervisor_limits` as a hard constraint, but it does not yet evaluate supervisor workload fairness as a soft metric.

Expected Benefit:
The system can report whether supervisor workload is balanced, making allocation quality easier to justify to academic staff.

Implementation Complexity:
Medium.

Current Status:
Deferred. Supervisor limits are implemented, but supervisor fairness reporting is not yet implemented.

### Counterfactual Workload Comparison

Description:
Compare runs with `workload_balance_weight = 0` and `workload_balance_weight > 0` to determine whether workload balancing changed assignments or workload distribution.

Motivation:
The project already supports counterfactual comparison for fairness weighting. Workload balancing should eventually receive the same transparent comparison treatment.

Expected Benefit:
Users can see whether workload balancing actually changed the allocation instead of only seeing that the workload objective was active.

Implementation Complexity:
Medium.

Current Status:
Deferred. Fairness counterfactual comparison is implemented first.

### First-Choice Counterfactual Proof

Description:
For each student who does not receive their first choice, run controlled checks to determine whether assigning that first choice would violate capacity, skills, supervisor limits, workload limits, or objective trade-offs.

Motivation:
Current first-choice notes identify likely reasons. A stronger proof would show whether a rejected first-choice assignment was impossible or only less optimal.

Expected Benefit:
Improves transparent decision logic and makes explanations stronger for FYP evaluation.

Implementation Complexity:
High.

Current Status:
Deferred. Assignment-level notes and fairness-run counterfactual comparison exist, but full first-choice causal proof is future work.

## Priority B - Research Extensions

These items extend the optimisation analysis and are useful for deeper evaluation.

### Pareto Frontier Analysis

Description:
Generate multiple allocation runs across different fairness and satisfaction weights to show trade-offs between total satisfaction, fairness gap, max-min value, Gini coefficient, and workload gap.

Motivation:
A single objective weight can hide the broader trade-off space. Pareto analysis would show which allocations are efficient and which are dominated.

Expected Benefit:
Provides stronger academic evaluation and supports discussion of fairness-performance trade-offs.

Implementation Complexity:
High.

Current Status:
Deferred. Current work focuses on one controlled fairness comparison instead of full frontier analysis.

### What-If Simulation

Description:
Allow users to modify inputs such as project capacity, supervisor limits, student preferences, or fairness weights and compare the resulting allocation.

Motivation:
Decision makers often need to test policy changes before finalising allocation rules.

Expected Benefit:
Makes FairMatch AI useful as a decision support tool, not only a one-shot solver.

Implementation Complexity:
Medium to High.

Current Status:
Deferred. CLI comparison exists for one fairness scenario, but general what-if simulation is not yet implemented.

## Priority C - Presentation Features

These items improve usability and demonstration value but are not core to the optimisation engine.

### Streamlit Dashboard

Description:
Build a simple dashboard to upload or select datasets, run allocation, view assignments, inspect fairness metrics, and read explanations.

Motivation:
A dashboard would make the project easier to demonstrate to non-technical users.

Expected Benefit:
Improves presentation quality and makes the system more accessible.

Implementation Complexity:
Medium.

Current Status:
Deferred. The project deliberately prioritised backend, fairness, explanation, validation, and CLI output before UI.

### PDF Report Export

Description:
Generate a PDF report containing allocation results, fairness metrics, explanation notes, and counterfactual comparison summaries.

Motivation:
Stakeholders may need a shareable allocation report for review, approval, or documentation.

Expected Benefit:
Creates a polished final artefact for demonstrations and stakeholder communication.

Implementation Complexity:
Medium.

Current Status:
Deferred. CLI output now exposes the required information, but PDF formatting/export is future work.

## Summary

The deferred backlog is intentional.

FairMatch AI first needs a credible core:

- a validated School Mode allocation engine
- measurable fairness metrics
- structured explanation logic
- controlled counterfactual fairness comparison
- repeatable test cases
- demo-ready CLI output

Only after that foundation is stable should the project expand into advanced analysis, dashboards, and exported presentation artefacts.

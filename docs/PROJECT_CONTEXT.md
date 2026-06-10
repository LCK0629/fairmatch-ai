# Project Context

## Project Title

FairMatch AI: Intelligent Scheduling and Allocation System with Fairness Constraints.

## FYP Topic Code

CSIT-26-S3-06.

## Core Identity

FairMatch AI is a constraint optimisation and decision support platform.

FairMatch AI is not an LLM recommendation system. It does not generate assignments from natural language guesses or machine learning predictions. The system models allocation as a structured optimisation problem using Google OR-Tools CP-SAT.

## Problem Statement

Allocation decisions are difficult when people compete for limited projects, tasks, or shifts. Manual allocation can accidentally violate capacity limits, ignore skill fit, overload supervisors or employees, and create unfair outcomes.

FairMatch AI addresses this by making allocation rules explicit:

- who can be assigned
- what each person prefers
- what each item requires
- what capacities must be respected
- how workload should be balanced
- how fairness is measured
- why the final decision was made

## Target Users

Primary users:

- project coordinators
- lecturers and supervisors
- course administrators
- team leads
- operations coordinators

Secondary users:

- students receiving project allocations
- employees receiving task or shift assignments
- reviewers checking fairness and transparency

## School Mode

School Mode allocates students to projects.

It should consider:

- student preferences
- student skills
- project required skills
- project capacity
- supervisor workload limits
- fairness across students

## Work Mode

Work Mode allocates employees to tasks or shifts.

It should consider:

- employee preferences
- employee skills
- task or shift requirements
- item capacity
- employee workload limits
- workload balance across employees
- fairness across employees

## Why Fairness Matters

Allocation systems should avoid giving highly desirable outcomes to only a few people while leaving others with poor matches. Fairness does not mean everyone receives their first choice. It means the system should explicitly measure and reduce unfair spread where possible.

## Why Workload Balance Matters

An allocation can satisfy preferences but still be operationally poor if one supervisor or employee becomes overloaded. FairMatch AI treats workload as part of decision quality, not an afterthought.

## Why Transparent Decision Logic Matters

Users need to understand why an assignment happened. The system should report preference rank, skill eligibility, workload impact, capacity compliance, and fairness trade-offs so allocation decisions can be reviewed.

## Why Google OR-Tools CP-SAT Is Suitable

Google OR-Tools CP-SAT is suitable because FairMatch AI needs:

- binary assignment decisions
- hard constraints
- soft constraints
- weighted objective functions
- feasibility detection
- explainable optimisation structure

This fits a constraint optimisation approach better than a black-box recommendation approach.

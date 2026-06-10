# Project Context

## Project Title

FairMatch AI: Intelligent Scheduling and Allocation System with Fairness Constraints.

## FYP Topic Code

CSIT-26-S3-06.

## Main FYP Scope

```text
Explainable Fairness-Aware Project Allocation Engine
```

The project roadmap is now focused on completing School Mode first. The primary system to build is a Student to Project allocation engine that supports fairness constraints, workload balance, stakeholder preferences, and transparent decision logic.

## Core Identity

FairMatch AI is a constraint optimisation and decision support platform.

FairMatch AI is not an LLM recommendation system. It does not generate assignments from natural language guesses, chat prompts, or machine learning predictions. The system models allocation as a structured optimisation problem using Google OR-Tools CP-SAT.

## Problem Statement

Project allocation is difficult when many students compete for limited project places. Manual allocation can accidentally:

- exceed project capacity
- ignore student preferences
- ignore student skill fit
- overload supervisors
- create unfair distribution of good outcomes
- produce decisions that are hard to explain

FairMatch AI addresses this by making the allocation rules explicit, measurable, and reviewable.

## Primary Target Users

Primary users for Phase 1:

- course coordinators
- lecturers
- project supervisors
- academic administrators

Secondary users:

- students receiving project allocations
- assessors reviewing whether the allocation method is fair and explainable

## Phase 1 Priority: School Mode

School Mode allocates students to projects.

It should consider:

- student preferences
- student skills
- project required skills
- project capacity
- supervisor workload limits
- fairness across students
- transparent explanation for each assignment

This is the core FYP delivery target.

## Work Mode Position

Work Mode remains a future extension unless time allows.

Work Mode may later allocate employees to tasks or shifts, but it is no longer the immediate roadmap priority. The current documentation and implementation direction should prioritise Student to Project allocation first.

## Why Fairness Matters

Fairness matters because an allocation system should not only maximise total preference satisfaction. It should also avoid outcomes where a small group receives very strong matches while others receive poor matches.

In School Mode, fairness may consider:

- satisfaction score spread
- number of students receiving low-ranked projects
- minimum satisfaction level
- distribution of project opportunities

## Why Workload Balance Matters

Supervisor workload is part of allocation quality. A technically valid allocation can still be poor if one supervisor receives too many students or too many demanding projects.

For Phase 1, workload balance should focus mainly on supervisor workload and project capacity.

## Why Stakeholder Preferences Matter

The official requirement includes stakeholder preferences. In Phase 1, stakeholder preferences include:

- student project preferences
- project skill requirements
- supervisor capacity or workload constraints
- academic coordination rules

## Why Transparent Decision Logic Matters

The system should not return only a final assignment. It should explain:

- why the student was eligible
- how the assigned project ranked in the student's preferences
- how project capacity was respected
- whether supervisor workload limits were respected
- how fairness influenced the result

Transparent decision logic is central to the FYP value.

## Phase 2 Priority: Structured Explanation Engine

Phase 2 changes explanations from a single plain-text sentence into structured explanation data.

Each assignment should expose separate explanation fields for:

- assigned project
- preference rank
- satisfaction score
- skill eligibility
- capacity impact
- supervisor limit impact
- fairness weight impact
- workload balancing impact
- first-choice assignment or rejection reason
- human-readable summary

This structure allows future CLI, report, or dashboard output to show clear reasoning without parsing a free-form string.

## Why Google OR-Tools CP-SAT Is Suitable

Google OR-Tools CP-SAT is suitable because FairMatch AI needs:

- binary assignment decisions
- hard constraints
- soft constraints
- weighted objective functions
- feasibility detection
- explainable optimisation structure

This fits a constraint optimisation approach better than a black-box recommendation approach.

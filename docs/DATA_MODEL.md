# Data Model

## Shared Model

FairMatch AI uses one shared allocation model for both modes.

```text
School Mode: students -> projects
Work Mode: employees -> tasks or shifts
Shared Model: people -> items
```

## Person

A person represents a student or employee.

Fields:

```text
id
name
skills
max_workload
current_workload
```

Example:

```json
{
  "id": "s1",
  "name": "Alicia Tan",
  "skills": ["python", "data"],
  "max_workload": 3,
  "current_workload": 0
}
```

## Item

An item represents a project, task, or shift.

Fields:

```text
id
name
capacity
required_skills
workload
supervisor_id
```

Example:

```json
{
  "id": "p1",
  "name": "AI Timetable Assistant",
  "capacity": 2,
  "required_skills": ["python"],
  "workload": 2,
  "supervisor_id": "sup_ai"
}
```

## Preferences

Preferences are ranked item IDs for each person.

Example:

```json
{
  "s1": ["p1", "p2", "p3"]
}
```

The solver converts ranks into satisfaction scores.

## Supervisor Limits

Supervisor limits control how many students can be assigned to projects under the same supervisor.

Example:

```json
{
  "supervisor_limits": {
    "sup_ai": 2,
    "sup_cyber": 1
  }
}
```

This is mainly used in School Mode, but the same pattern can be reused for managers or team leads in Work Mode.

## Allocation Input

Current input shape:

```json
{
  "mode": "school",
  "fairness_weight": 2,
  "workload_balance_weight": 1,
  "supervisor_limits": {},
  "people": [],
  "items": [],
  "preferences": {}
}
```

## Assignment Output

Each assignment includes:

```text
person_id
person_name
item_id
item_name
satisfaction
preference_rank
workload
skill_match
explanation
```

The explanation is part of the data model because transparency is a project requirement.

## Allocation Result

The allocation result includes:

```text
mode
status
objective_value
assignments
total_satisfaction
min_satisfaction
max_satisfaction
fairness_gap
min_workload
max_workload
workload_gap
```

## Data Model Principles

- Use stable IDs for people and items.
- Keep School Mode and Work Mode compatible with the shared model.
- Store skills explicitly.
- Store workload explicitly.
- Include explanation fields in outputs.
- Keep fairness metrics visible in the result.

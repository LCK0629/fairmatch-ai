from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AllocationMode = Literal["school", "work"]


@dataclass(frozen=True)
class Person:
    id: str
    name: str
    skills: list[str]
    max_workload: int
    current_workload: int = 0


@dataclass(frozen=True)
class Item:
    id: str
    name: str
    capacity: int = 1
    required_skills: list[str] | None = None
    workload: int = 1
    supervisor_id: str | None = None


@dataclass(frozen=True)
class AllocationInput:
    mode: AllocationMode
    people: list[Person]
    items: list[Item]
    preferences: dict[str, list[str]]
    fairness_weight: int = 1
    workload_balance_weight: int = 1
    supervisor_limits: dict[str, int] | None = None


@dataclass(frozen=True)
class ExplanationDetail:
    person_id: str
    item_id: str
    assigned_item: str
    preference_rank: int | None
    satisfaction: int
    skill_match: bool
    capacity_note: str
    skill_note: str
    first_choice_note: str
    supervisor_note: str
    fairness_note: str
    workload_note: str
    summary: str


@dataclass(frozen=True)
class Assignment:
    person_id: str
    person_name: str
    item_id: str
    item_name: str
    satisfaction: int
    preference_rank: int | None
    workload: int
    skill_match: bool
    explanation: ExplanationDetail


@dataclass(frozen=True)
class AllocationResult:
    mode: AllocationMode
    status: str
    objective_value: float
    assignments: list[Assignment]
    total_satisfaction: int
    min_satisfaction: int
    max_satisfaction: int
    fairness_gap: int
    min_workload: int
    max_workload: int
    workload_gap: int


def load_allocation_input(payload: dict) -> AllocationInput:
    people = [
        Person(
            id=str(person["id"]),
            name=str(person["name"]),
            skills=[str(skill) for skill in person.get("skills", [])],
            max_workload=int(person.get("max_workload", 1)),
            current_workload=int(person.get("current_workload", 0)),
        )
        for person in payload["people"]
    ]
    items = [
        Item(
            id=str(item["id"]),
            name=str(item["name"]),
            capacity=int(item.get("capacity", 1)),
            required_skills=[str(skill) for skill in item.get("required_skills", [])],
            workload=int(item.get("workload", 1)),
            supervisor_id=str(item["supervisor_id"]) if item.get("supervisor_id") is not None else None,
        )
        for item in payload["items"]
    ]

    return AllocationInput(
        mode=payload["mode"],
        people=people,
        items=items,
        preferences={str(person_id): [str(item_id) for item_id in item_ids] for person_id, item_ids in payload["preferences"].items()},
        fairness_weight=int(payload.get("fairness_weight", 1)),
        workload_balance_weight=int(payload.get("workload_balance_weight", 1)),
        supervisor_limits={
            str(supervisor_id): int(limit)
            for supervisor_id, limit in payload.get("supervisor_limits", {}).items()
        },
    )

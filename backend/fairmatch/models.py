from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

AllocationMode = Literal["school", "work"]


@dataclass(frozen=True)
class Person:
    id: str
    name: str


@dataclass(frozen=True)
class Item:
    id: str
    name: str
    capacity: int = 1


@dataclass(frozen=True)
class AllocationInput:
    mode: AllocationMode
    people: list[Person]
    items: list[Item]
    preferences: dict[str, list[str]]
    fairness_weight: int = 1


@dataclass(frozen=True)
class Assignment:
    person_id: str
    person_name: str
    item_id: str
    item_name: str
    satisfaction: int


@dataclass(frozen=True)
class AllocationResult:
    mode: AllocationMode
    status: str
    objective_value: float
    assignments: list[Assignment]
    min_satisfaction: int
    max_satisfaction: int


def load_allocation_input(payload: dict) -> AllocationInput:
    people = [Person(id=str(person["id"]), name=str(person["name"])) for person in payload["people"]]
    items = [
        Item(id=str(item["id"]), name=str(item["name"]), capacity=int(item.get("capacity", 1)))
        for item in payload["items"]
    ]

    return AllocationInput(
        mode=payload["mode"],
        people=people,
        items=items,
        preferences={str(person_id): [str(item_id) for item_id in item_ids] for person_id, item_ids in payload["preferences"].items()},
        fairness_weight=int(payload.get("fairness_weight", 1)),
    )
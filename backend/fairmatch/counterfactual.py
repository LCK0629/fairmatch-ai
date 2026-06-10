from __future__ import annotations

from dataclasses import dataclass

from .models import AllocationResult


@dataclass(frozen=True)
class CounterfactualComparison:
    baseline_total_satisfaction: int
    fairness_total_satisfaction: int
    baseline_fairness_gap: int
    fairness_fairness_gap: int
    baseline_max_min_value: int
    fairness_max_min_value: int
    baseline_gini_coefficient: float
    fairness_gini_coefficient: float
    changed_assignments: dict[str, tuple[str, str]]
    changed_satisfaction: dict[str, tuple[int, int]]
    fairness_improved: bool


def compare_fairness_runs(
    baseline_result: AllocationResult,
    fairness_result: AllocationResult,
) -> CounterfactualComparison:
    baseline_assignments = {
        assignment.person_id: assignment
        for assignment in baseline_result.assignments
    }
    fairness_assignments = {
        assignment.person_id: assignment
        for assignment in fairness_result.assignments
    }
    shared_people = set(baseline_assignments) & set(fairness_assignments)

    changed_assignments = {
        person_id: (
            baseline_assignments[person_id].item_id,
            fairness_assignments[person_id].item_id,
        )
        for person_id in shared_people
        if baseline_assignments[person_id].item_id != fairness_assignments[person_id].item_id
    }
    changed_satisfaction = {
        person_id: (
            baseline_assignments[person_id].satisfaction,
            fairness_assignments[person_id].satisfaction,
        )
        for person_id in shared_people
        if baseline_assignments[person_id].satisfaction != fairness_assignments[person_id].satisfaction
    }

    fairness_improved = (
        fairness_result.fairness_gap < baseline_result.fairness_gap
        or fairness_result.max_min_value > baseline_result.max_min_value
        or fairness_result.gini_coefficient < baseline_result.gini_coefficient
    )

    return CounterfactualComparison(
        baseline_total_satisfaction=baseline_result.total_satisfaction,
        fairness_total_satisfaction=fairness_result.total_satisfaction,
        baseline_fairness_gap=baseline_result.fairness_gap,
        fairness_fairness_gap=fairness_result.fairness_gap,
        baseline_max_min_value=baseline_result.max_min_value,
        fairness_max_min_value=fairness_result.max_min_value,
        baseline_gini_coefficient=baseline_result.gini_coefficient,
        fairness_gini_coefficient=fairness_result.gini_coefficient,
        changed_assignments=changed_assignments,
        changed_satisfaction=changed_satisfaction,
        fairness_improved=fairness_improved,
    )

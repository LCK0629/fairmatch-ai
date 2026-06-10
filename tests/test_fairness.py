import pytest

from backend.fairmatch.fairness import (
    calculate_average_satisfaction,
    calculate_gini_coefficient,
    calculate_max_min_value,
    calculate_satisfaction_gap,
    calculate_total_satisfaction,
)
from backend.fairmatch.models import load_allocation_input
from backend.fairmatch.solver import solve_allocation


def test_fairness_metric_helpers_calculate_satisfaction_distribution():
    scores = [3, 3, 0]

    assert calculate_total_satisfaction(scores) == 6
    assert calculate_average_satisfaction(scores) == 2
    assert calculate_satisfaction_gap(scores) == 3
    assert calculate_max_min_value(scores) == 0
    assert calculate_gini_coefficient(scores) == pytest.approx(1 / 3)


def test_fairness_metric_helpers_handle_empty_and_zero_scores():
    assert calculate_total_satisfaction([]) == 0
    assert calculate_average_satisfaction([]) == 0.0
    assert calculate_satisfaction_gap([]) == 0
    assert calculate_max_min_value([]) == 0
    assert calculate_gini_coefficient([]) == 0.0
    assert calculate_gini_coefficient([0, 0, 0]) == 0.0


def test_allocation_result_reports_fairness_metrics():
    payload = {
        "mode": "school",
        "people": [
            {"id": "s1", "name": "Student One", "skills": ["python"], "max_workload": 3},
            {"id": "s2", "name": "Student Two", "skills": ["web"], "max_workload": 3},
        ],
        "items": [
            {"id": "p1", "name": "Python Project", "capacity": 1, "required_skills": ["python"], "workload": 1},
            {"id": "p2", "name": "Web Project", "capacity": 1, "required_skills": ["web"], "workload": 1},
        ],
        "preferences": {
            "s1": ["p1", "p2"],
            "s2": ["p2", "p1"],
        },
    }

    result = solve_allocation(load_allocation_input(payload))

    assert result.status in {"OPTIMAL", "FEASIBLE"}
    assert result.total_satisfaction == 6
    assert result.average_satisfaction == 3
    assert result.fairness_gap == 0
    assert result.max_min_value == 3
    assert result.gini_coefficient == 0

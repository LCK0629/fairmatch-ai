from copy import deepcopy
import json
from pathlib import Path

import pytest

from backend.fairmatch.models import load_allocation_input
from backend.fairmatch.solver import solve_allocation


CASES_DIR = Path(__file__).resolve().parents[1] / "data" / "school_cases"


def load_case(name: str):
    return json.loads((CASES_DIR / name).read_text(encoding="utf-8"))


def item_by_id(payload: dict) -> dict:
    return {item["id"]: item for item in payload["items"]}


def assignment_by_person(result) -> dict:
    return {assignment.person_id: assignment.item_id for assignment in result.assignments}


def test_balanced_school_case_assigns_every_student_and_respects_constraints():
    result = solve_allocation(load_allocation_input(load_case("balanced_feasible.json")))

    assert result.status in {"OPTIMAL", "FEASIBLE"}
    assert len(result.assignments) == 6
    assert {assignment.person_id for assignment in result.assignments} == {
        "s1",
        "s2",
        "s3",
        "s4",
        "s5",
        "s6",
    }
    assert all(assignment.skill_match for assignment in result.assignments)
    assert all(assignment.satisfaction >= 0 for assignment in result.assignments)
    assert all(
        assignment.preference_rank is None or assignment.preference_rank >= 1
        for assignment in result.assignments
    )
    assert all("capacity respected" in assignment.explanation.capacity_note for assignment in result.assignments)
    assert all("Required skills satisfied" in assignment.explanation.skill_note for assignment in result.assignments)
    assert all(assignment.explanation.first_choice_note for assignment in result.assignments)
    assert all(assignment.explanation.supervisor_note for assignment in result.assignments)
    assert all(assignment.explanation.fairness_note for assignment in result.assignments)
    assert all(assignment.explanation.workload_note for assignment in result.assignments)
    assert all(assignment.explanation.summary for assignment in result.assignments)
    assert result.fairness_gap >= 0
    assert result.workload_gap >= 0


def test_skill_bottleneck_case_prioritises_eligibility_over_preferences():
    result = solve_allocation(load_allocation_input(load_case("skill_bottleneck_feasible.json")))

    assignments = {assignment.person_id: assignment.item_id for assignment in result.assignments}
    assert result.status in {"OPTIMAL", "FEASIBLE"}
    assert assignments == {
        "s_python": "p_python",
        "s_web": "p_web",
    }
    assert all(assignment.skill_match for assignment in result.assignments)


def test_fairness_weight_changes_optimisation_behaviour():
    payload = load_case("fairness_weight_tradeoff.json")
    low_fairness_payload = deepcopy(payload)
    high_fairness_payload = deepcopy(payload)
    low_fairness_payload["fairness_weight"] = 0
    high_fairness_payload["fairness_weight"] = 3

    low_fairness_result = solve_allocation(load_allocation_input(low_fairness_payload))
    high_fairness_result = solve_allocation(load_allocation_input(high_fairness_payload))

    assert low_fairness_result.status in {"OPTIMAL", "FEASIBLE"}
    assert high_fairness_result.status in {"OPTIMAL", "FEASIBLE"}

    for result in (low_fairness_result, high_fairness_result):
        assert len(result.assignments) == 3
        assert all(assignment.skill_match for assignment in result.assignments)
        projects = item_by_id(payload)
        for project_id in projects:
            assigned_count = sum(1 for assignment in result.assignments if assignment.item_id == project_id)
            assert assigned_count <= projects[project_id]["capacity"]

    assert low_fairness_result.total_satisfaction > high_fairness_result.total_satisfaction
    assert low_fairness_result.fairness_gap > high_fairness_result.fairness_gap
    assert assignment_by_person(low_fairness_result) != assignment_by_person(high_fairness_result)
    assert any(
        "fairness objective" in assignment.explanation.first_choice_note
        for assignment in high_fairness_result.assignments
        if assignment.preference_rank != 1
    )


def test_first_choice_rejection_explains_capacity_reason():
    result = solve_allocation(load_allocation_input(load_case("first_choice_capacity_rejection.json")))

    assert result.status in {"OPTIMAL", "FEASIBLE"}
    rejected_assignment = next(
        assignment for assignment in result.assignments if assignment.preference_rank != 1
    )
    assert "first-choice project reached capacity" in rejected_assignment.explanation.first_choice_note


def test_first_choice_rejection_explains_skill_reason():
    result = solve_allocation(load_allocation_input(load_case("first_choice_skill_rejection.json")))

    assert result.status in {"OPTIMAL", "FEASIBLE"}
    assignment = result.assignments[0]
    assert assignment.item_id == "p_web"
    assert "student lacked required skills" in assignment.explanation.first_choice_note


def test_first_choice_rejection_explains_workload_reason():
    result = solve_allocation(load_allocation_input(load_case("first_choice_workload_rejection.json")))

    assert result.status in {"OPTIMAL", "FEASIBLE"}
    assignment = result.assignments[0]
    assert assignment.item_id == "p_light"
    assert "would exceed the student's workload limit" in assignment.explanation.first_choice_note


def test_insufficient_capacity_case_fails_validation():
    with pytest.raises(ValueError, match="total item capacity"):
        solve_allocation(load_allocation_input(load_case("insufficient_capacity_infeasible.json")))


def test_skill_gap_case_is_solver_infeasible():
    result = solve_allocation(load_allocation_input(load_case("skill_gap_infeasible.json")))

    assert result.status == "INFEASIBLE"
    assert result.assignments == []


def test_supervisor_limit_case_is_solver_infeasible():
    result = solve_allocation(load_allocation_input(load_case("supervisor_limit_infeasible.json")))

    assert result.status == "INFEASIBLE"
    assert result.assignments == []


def test_workload_limit_case_is_solver_infeasible():
    result = solve_allocation(load_allocation_input(load_case("workload_limit_infeasible.json")))

    assert result.status == "INFEASIBLE"
    assert result.assignments == []


def test_invalid_preference_reference_fails_validation():
    with pytest.raises(ValueError, match="unknown item ids"):
        solve_allocation(load_allocation_input(load_case("invalid_preference_reference.json")))

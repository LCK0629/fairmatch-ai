import json
from pathlib import Path

import pytest

from backend.fairmatch.models import load_allocation_input
from backend.fairmatch.solver import solve_allocation


CASES_DIR = Path(__file__).resolve().parents[1] / "data" / "school_cases"


def load_case(name: str):
    return json.loads((CASES_DIR / name).read_text(encoding="utf-8"))


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
    assert all(assignment.preference_rank is not None for assignment in result.assignments)
    assert all("capacity is respected" in assignment.explanation for assignment in result.assignments)
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

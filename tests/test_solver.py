from backend.fairmatch.models import load_allocation_input
from backend.fairmatch.solver import solve_allocation


def test_school_sample_assigns_every_student():
    payload = {
        "mode": "school",
        "people": [
            {"id": "s1", "name": "Student One", "skills": ["python"], "max_workload": 3},
            {"id": "s2", "name": "Student Two", "skills": ["web"], "max_workload": 3},
        ],
        "items": [
            {"id": "p1", "name": "Project One", "capacity": 1, "required_skills": ["python"], "workload": 2},
            {"id": "p2", "name": "Project Two", "capacity": 1, "required_skills": ["web"], "workload": 2},
        ],
        "preferences": {
            "s1": ["p1", "p2"],
            "s2": ["p2", "p1"],
        },
    }

    result = solve_allocation(load_allocation_input(payload))

    assert result.status in {"OPTIMAL", "FEASIBLE"}
    assert len(result.assignments) == 2
    assert {assignment.person_id for assignment in result.assignments} == {"s1", "s2"}
    assert all(assignment.skill_match for assignment in result.assignments)
    assert all(assignment.explanation.summary for assignment in result.assignments)
    assert all(assignment.explanation.capacity_note for assignment in result.assignments)
    assert all(assignment.explanation.first_choice_note for assignment in result.assignments)


def test_skill_requirements_block_ineligible_assignments():
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
            "s1": ["p2", "p1"],
            "s2": ["p1", "p2"],
        },
    }

    result = solve_allocation(load_allocation_input(payload))

    assignments = {assignment.person_id: assignment.item_id for assignment in result.assignments}
    assert assignments == {"s1": "p1", "s2": "p2"}


def test_first_choice_score_is_fixed_for_different_preference_list_lengths():
    payload = {
        "mode": "school",
        "people": [
            {"id": "s_long", "name": "Long List Student", "skills": ["python"], "max_workload": 3},
            {"id": "s_short", "name": "Short List Student", "skills": ["python"], "max_workload": 3},
        ],
        "items": [
            {"id": "p1", "name": "Project One", "capacity": 1, "required_skills": ["python"], "workload": 1},
            {"id": "p2", "name": "Project Two", "capacity": 1, "required_skills": ["python"], "workload": 1},
            {"id": "p3", "name": "Project Three", "capacity": 1, "required_skills": ["python"], "workload": 1},
            {"id": "p4", "name": "Project Four", "capacity": 1, "required_skills": ["python"], "workload": 1},
            {"id": "p5", "name": "Project Five", "capacity": 1, "required_skills": ["python"], "workload": 1},
        ],
        "preferences": {
            "s_long": ["p1", "p3", "p4", "p5", "p2"],
            "s_short": ["p2", "p3", "p4"],
        },
    }

    result = solve_allocation(load_allocation_input(payload))

    scores = {assignment.person_id: assignment.satisfaction for assignment in result.assignments}
    ranks = {assignment.person_id: assignment.preference_rank for assignment in result.assignments}
    assert ranks == {"s_long": 1, "s_short": 1}
    assert scores == {"s_long": 3, "s_short": 3}
    assert result.fairness_gap == 0


def test_workload_limit_can_make_problem_infeasible():
    payload = {
        "mode": "work",
        "people": [
            {"id": "e1", "name": "Employee One", "skills": ["analysis"], "max_workload": 1},
        ],
        "items": [
            {"id": "t1", "name": "Large Task", "capacity": 1, "required_skills": ["analysis"], "workload": 2},
        ],
        "preferences": {
            "e1": ["t1"],
        },
    }

    result = solve_allocation(load_allocation_input(payload))

    assert result.status == "INFEASIBLE"
    assert result.assignments == []

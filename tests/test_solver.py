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
    assert all(assignment.explanation for assignment in result.assignments)


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

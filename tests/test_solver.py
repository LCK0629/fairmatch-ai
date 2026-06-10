from backend.fairmatch.models import load_allocation_input
from backend.fairmatch.solver import solve_allocation


def test_school_sample_assigns_every_student():
    payload = {
        "mode": "school",
        "people": [
            {"id": "s1", "name": "Student One"},
            {"id": "s2", "name": "Student Two"},
        ],
        "items": [
            {"id": "p1", "name": "Project One", "capacity": 1},
            {"id": "p2", "name": "Project Two", "capacity": 1},
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
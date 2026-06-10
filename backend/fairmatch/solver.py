from __future__ import annotations

from ortools.sat.python import cp_model

from .models import AllocationInput, AllocationResult, Assignment


UNKNOWN_PREFERENCE_SCORE = 0


def solve_allocation(problem: AllocationInput) -> AllocationResult:
    """Solve a fairness-aware allocation problem with OR-Tools CP-SAT."""
    _validate_problem(problem)

    model = cp_model.CpModel()
    assignment_vars: dict[tuple[str, str], cp_model.IntVar] = {}

    for person in problem.people:
        for item in problem.items:
            assignment_vars[(person.id, item.id)] = model.new_bool_var(f"assign_{person.id}_{item.id}")

    for person in problem.people:
        model.add_exactly_one(assignment_vars[(person.id, item.id)] for item in problem.items)

    for item in problem.items:
        model.add(sum(assignment_vars[(person.id, item.id)] for person in problem.people) <= item.capacity)

    satisfaction_terms = []
    satisfaction_by_person: dict[str, cp_model.IntVar] = {}
    max_score = max((len(choices) for choices in problem.preferences.values()), default=0)

    for person in problem.people:
        score_terms = []
        ranked_choices = problem.preferences.get(person.id, [])
        for item in problem.items:
            score = _preference_score(item.id, ranked_choices)
            term = assignment_vars[(person.id, item.id)] * score
            satisfaction_terms.append(term)
            score_terms.append(term)

        satisfaction = model.new_int_var(0, max_score, f"satisfaction_{person.id}")
        model.add(satisfaction == sum(score_terms))
        satisfaction_by_person[person.id] = satisfaction

    min_satisfaction = model.new_int_var(0, max_score, "min_satisfaction")
    max_satisfaction = model.new_int_var(0, max_score, "max_satisfaction")
    model.add_min_equality(min_satisfaction, list(satisfaction_by_person.values()))
    model.add_max_equality(max_satisfaction, list(satisfaction_by_person.values()))

    fairness_gap = model.new_int_var(0, max_score, "fairness_gap")
    model.add(fairness_gap == max_satisfaction - min_satisfaction)

    total_satisfaction = sum(satisfaction_terms)
    model.maximize(total_satisfaction - (problem.fairness_weight * fairness_gap))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    status = solver.solve(model)

    readable_status = solver.status_name(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return AllocationResult(
            mode=problem.mode,
            status=readable_status,
            objective_value=0,
            assignments=[],
            min_satisfaction=0,
            max_satisfaction=0,
        )

    people_by_id = {person.id: person for person in problem.people}
    items_by_id = {item.id: item for item in problem.items}
    assignments: list[Assignment] = []

    for person in problem.people:
        ranked_choices = problem.preferences.get(person.id, [])
        for item in problem.items:
            if solver.boolean_value(assignment_vars[(person.id, item.id)]):
                assignments.append(
                    Assignment(
                        person_id=person.id,
                        person_name=people_by_id[person.id].name,
                        item_id=item.id,
                        item_name=items_by_id[item.id].name,
                        satisfaction=_preference_score(item.id, ranked_choices),
                    )
                )

    return AllocationResult(
        mode=problem.mode,
        status=readable_status,
        objective_value=solver.objective_value,
        assignments=assignments,
        min_satisfaction=int(solver.value(min_satisfaction)),
        max_satisfaction=int(solver.value(max_satisfaction)),
    )


def _preference_score(item_id: str, ranked_choices: list[str]) -> int:
    if item_id not in ranked_choices:
        return UNKNOWN_PREFERENCE_SCORE
    return len(ranked_choices) - ranked_choices.index(item_id)


def _validate_problem(problem: AllocationInput) -> None:
    if problem.mode not in {"school", "work"}:
        raise ValueError("mode must be either 'school' or 'work'")
    if not problem.people:
        raise ValueError("at least one person is required")
    if not problem.items:
        raise ValueError("at least one item is required")
    if sum(item.capacity for item in problem.items) < len(problem.people):
        raise ValueError("total item capacity must be at least the number of people")
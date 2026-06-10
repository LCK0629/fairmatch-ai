from __future__ import annotations

from ortools.sat.python import cp_model

from .models import AllocationInput, AllocationResult, Assignment, Item, Person


UNKNOWN_PREFERENCE_SCORE = 0
FIRST_CHOICE_SCORE = 3
SECOND_CHOICE_SCORE = 2
THIRD_CHOICE_SCORE = 1
MAX_PREFERENCE_SCORE = FIRST_CHOICE_SCORE


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

    for person in problem.people:
        for item in problem.items:
            if not _has_required_skills(person, item):
                model.add(assignment_vars[(person.id, item.id)] == 0)

    for supervisor_id, limit in (problem.supervisor_limits or {}).items():
        supervised_items = [item for item in problem.items if item.supervisor_id == supervisor_id]
        if supervised_items:
            model.add(
                sum(
                    assignment_vars[(person.id, item.id)]
                    for person in problem.people
                    for item in supervised_items
                )
                <= limit
            )

    satisfaction_terms = []
    satisfaction_by_person: dict[str, cp_model.IntVar] = {}
    max_score = MAX_PREFERENCE_SCORE
    workload_by_person: dict[str, cp_model.IntVar] = {}
    max_possible_workload = max(
        (person.current_workload + max((item.workload for item in problem.items), default=0) for person in problem.people),
        default=0,
    )

    for person in problem.people:
        score_terms = []
        workload_terms = []
        ranked_choices = problem.preferences.get(person.id, [])
        for item in problem.items:
            score = _preference_score(item.id, ranked_choices)
            term = assignment_vars[(person.id, item.id)] * score
            satisfaction_terms.append(term)
            score_terms.append(term)
            workload_terms.append(assignment_vars[(person.id, item.id)] * item.workload)

        satisfaction = model.new_int_var(0, max_score, f"satisfaction_{person.id}")
        model.add(satisfaction == sum(score_terms))
        satisfaction_by_person[person.id] = satisfaction

        workload = model.new_int_var(0, max_possible_workload, f"workload_{person.id}")
        model.add(workload == person.current_workload + sum(workload_terms))
        model.add(workload <= person.max_workload)
        workload_by_person[person.id] = workload

    min_satisfaction = model.new_int_var(0, max_score, "min_satisfaction")
    max_satisfaction = model.new_int_var(0, max_score, "max_satisfaction")
    model.add_min_equality(min_satisfaction, list(satisfaction_by_person.values()))
    model.add_max_equality(max_satisfaction, list(satisfaction_by_person.values()))

    fairness_gap = model.new_int_var(0, max_score, "fairness_gap")
    model.add(fairness_gap == max_satisfaction - min_satisfaction)

    min_workload = model.new_int_var(0, max_possible_workload, "min_workload")
    max_workload = model.new_int_var(0, max_possible_workload, "max_workload")
    model.add_min_equality(min_workload, list(workload_by_person.values()))
    model.add_max_equality(max_workload, list(workload_by_person.values()))

    workload_gap = model.new_int_var(0, max_possible_workload, "workload_gap")
    model.add(workload_gap == max_workload - min_workload)

    total_satisfaction = sum(satisfaction_terms)
    model.maximize(
        total_satisfaction
        - (problem.fairness_weight * fairness_gap)
        - (problem.workload_balance_weight * workload_gap)
    )

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
            total_satisfaction=0,
            min_satisfaction=0,
            max_satisfaction=0,
            fairness_gap=0,
            min_workload=0,
            max_workload=0,
            workload_gap=0,
        )

    people_by_id = {person.id: person for person in problem.people}
    items_by_id = {item.id: item for item in problem.items}
    assignments: list[Assignment] = []

    for person in problem.people:
        ranked_choices = problem.preferences.get(person.id, [])
        for item in problem.items:
            if solver.boolean_value(assignment_vars[(person.id, item.id)]):
                preference_rank = _preference_rank(item.id, ranked_choices)
                satisfaction = _preference_score(item.id, ranked_choices)
                assigned_workload = person.current_workload + item.workload
                assignments.append(
                    Assignment(
                        person_id=person.id,
                        person_name=people_by_id[person.id].name,
                        item_id=item.id,
                        item_name=items_by_id[item.id].name,
                        satisfaction=satisfaction,
                        preference_rank=preference_rank,
                        workload=assigned_workload,
                        skill_match=_has_required_skills(person, item),
                        explanation=_build_explanation(person, item, preference_rank, satisfaction, assigned_workload),
                    )
                )

    return AllocationResult(
        mode=problem.mode,
        status=readable_status,
        objective_value=solver.objective_value,
        assignments=assignments,
        total_satisfaction=sum(assignment.satisfaction for assignment in assignments),
        min_satisfaction=int(solver.value(min_satisfaction)),
        max_satisfaction=int(solver.value(max_satisfaction)),
        fairness_gap=int(solver.value(fairness_gap)),
        min_workload=int(solver.value(min_workload)),
        max_workload=int(solver.value(max_workload)),
        workload_gap=int(solver.value(workload_gap)),
    )


def _preference_score(item_id: str, ranked_choices: list[str]) -> int:
    if item_id not in ranked_choices:
        return UNKNOWN_PREFERENCE_SCORE
    rank_index = ranked_choices.index(item_id)
    return max(MAX_PREFERENCE_SCORE - rank_index, UNKNOWN_PREFERENCE_SCORE)


def _preference_rank(item_id: str, ranked_choices: list[str]) -> int | None:
    if item_id not in ranked_choices:
        return None
    return ranked_choices.index(item_id) + 1


def _has_required_skills(person: Person, item: Item) -> bool:
    required_skills = set(item.required_skills or [])
    return required_skills.issubset(set(person.skills))


def _build_explanation(
    person: Person,
    item: Item,
    preference_rank: int | None,
    satisfaction: int,
    assigned_workload: int,
) -> str:
    preference_text = (
        f"ranked choice #{preference_rank}"
        if preference_rank is not None
        else "an unranked but feasible option"
    )
    skill_text = (
        "required skills satisfied"
        if item.required_skills
        else "no specific skill requirement"
    )
    supervisor_text = (
        f"supervisor limit checked for {item.supervisor_id}"
        if item.supervisor_id
        else "no supervisor limit"
    )
    return (
        f"{person.name} was assigned to {item.name}: {preference_text}, "
        f"satisfaction score {satisfaction}, {skill_text}, workload becomes "
        f"{assigned_workload}/{person.max_workload}, {supervisor_text}, and item capacity is respected."
    )


def _validate_problem(problem: AllocationInput) -> None:
    if problem.mode not in {"school", "work"}:
        raise ValueError("mode must be either 'school' or 'work'")
    if not problem.people:
        raise ValueError("at least one person is required")
    if not problem.items:
        raise ValueError("at least one item is required")
    if sum(item.capacity for item in problem.items) < len(problem.people):
        raise ValueError("total item capacity must be at least the number of people")
    people_ids = {person.id for person in problem.people}
    item_ids = {item.id for item in problem.items}
    if len(people_ids) != len(problem.people):
        raise ValueError("person ids must be unique")
    if len(item_ids) != len(problem.items):
        raise ValueError("item ids must be unique")
    for person_id, ranked_items in problem.preferences.items():
        if person_id not in people_ids:
            raise ValueError(f"preferences reference unknown person id: {person_id}")
        unknown_items = set(ranked_items) - item_ids
        if unknown_items:
            raise ValueError(f"preferences reference unknown item ids: {sorted(unknown_items)}")
    for person in problem.people:
        if person.max_workload < person.current_workload:
            raise ValueError(f"max_workload is lower than current_workload for person {person.id}")
    for item in problem.items:
        if item.capacity < 0:
            raise ValueError(f"capacity cannot be negative for item {item.id}")
        if item.workload < 0:
            raise ValueError(f"workload cannot be negative for item {item.id}")

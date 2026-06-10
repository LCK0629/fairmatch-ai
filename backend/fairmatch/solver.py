from __future__ import annotations

from ortools.sat.python import cp_model

from .fairness import (
    calculate_average_satisfaction,
    calculate_gini_coefficient,
    calculate_max_min_value,
    calculate_satisfaction_gap,
    calculate_total_satisfaction,
)
from .models import AllocationInput, AllocationResult, Assignment, ExplanationDetail, Item, Person


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
            average_satisfaction=0.0,
            min_satisfaction=0,
            max_satisfaction=0,
            fairness_gap=0,
            max_min_value=0,
            gini_coefficient=0.0,
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
                assigned_count = sum(
                    1
                    for candidate_person in problem.people
                    if solver.boolean_value(assignment_vars[(candidate_person.id, item.id)])
                )
                supervisor_count = _assigned_supervisor_count(problem, assignment_vars, solver, item.supervisor_id)
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
                        explanation=_build_explanation(
                            problem=problem,
                            assignment_vars=assignment_vars,
                            solver=solver,
                            person=person,
                            item=item,
                            preference_rank=preference_rank,
                            satisfaction=satisfaction,
                            assigned_workload=assigned_workload,
                            assigned_count=assigned_count,
                            supervisor_count=supervisor_count,
                        ),
                    )
                )

    satisfaction_scores = [assignment.satisfaction for assignment in assignments]

    return AllocationResult(
        mode=problem.mode,
        status=readable_status,
        objective_value=solver.objective_value,
        assignments=assignments,
        total_satisfaction=calculate_total_satisfaction(satisfaction_scores),
        average_satisfaction=calculate_average_satisfaction(satisfaction_scores),
        min_satisfaction=int(solver.value(min_satisfaction)),
        max_satisfaction=int(solver.value(max_satisfaction)),
        fairness_gap=calculate_satisfaction_gap(satisfaction_scores),
        max_min_value=calculate_max_min_value(satisfaction_scores),
        gini_coefficient=calculate_gini_coefficient(satisfaction_scores),
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
    problem: AllocationInput,
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
    solver: cp_model.CpSolver,
    person: Person,
    item: Item,
    preference_rank: int | None,
    satisfaction: int,
    assigned_workload: int,
    assigned_count: int,
    supervisor_count: int,
) -> ExplanationDetail:
    preference_text = (
        f"ranked choice #{preference_rank}"
        if preference_rank is not None
        else "an unranked but feasible option"
    )
    capacity_note = (
        f"Project capacity respected: {assigned_count}/{item.capacity} slot(s) used."
    )
    skill_note = (
        f"Required skills satisfied: {', '.join(item.required_skills or [])}."
        if item.required_skills
        else "No specific skill requirement was defined for this project."
    )
    first_choice_note = _build_first_choice_note(problem, assignment_vars, solver, person, item)
    supervisor_limit = (problem.supervisor_limits or {}).get(item.supervisor_id or "")
    supervisor_note = (
        f"Supervisor {item.supervisor_id} limit respected: {supervisor_count}/{supervisor_limit} assigned."
        if item.supervisor_id and supervisor_limit is not None
        else (
            f"Supervisor {item.supervisor_id} recorded, but no supervisor limit was configured."
            if item.supervisor_id
            else "No supervisor limit applies to this project."
        )
    )
    fairness_note = (
        f"Fairness weight {problem.fairness_weight} was applied through the satisfaction gap objective."
        if problem.fairness_weight
        else "Fairness weight is 0, so satisfaction gap did not affect this optimisation run."
    )
    workload_note = (
        f"Workload becomes {assigned_workload}/{person.max_workload}; workload balance weight "
        f"{problem.workload_balance_weight} was included in the objective."
        if problem.workload_balance_weight
        else f"Workload becomes {assigned_workload}/{person.max_workload}; workload balance weight is 0."
    )
    summary = (
        f"{person.name} was assigned to {item.name}: {preference_text}, "
        f"satisfaction score {satisfaction}, skill eligibility satisfied, and capacity respected."
    )
    return ExplanationDetail(
        person_id=person.id,
        item_id=item.id,
        assigned_item=item.name,
        preference_rank=preference_rank,
        satisfaction=satisfaction,
        skill_match=_has_required_skills(person, item),
        capacity_note=capacity_note,
        skill_note=skill_note,
        first_choice_note=first_choice_note,
        supervisor_note=supervisor_note,
        fairness_note=fairness_note,
        workload_note=workload_note,
        summary=summary,
    )


def _build_first_choice_note(
    problem: AllocationInput,
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
    solver: cp_model.CpSolver,
    person: Person,
    assigned_item: Item,
) -> str:
    ranked_choices = problem.preferences.get(person.id, [])
    if not ranked_choices:
        return "No first choice was submitted for this student."

    first_choice_id = ranked_choices[0]
    if assigned_item.id == first_choice_id:
        return "Assigned project is the student's first choice."

    items_by_id = {item.id: item for item in problem.items}
    first_choice = items_by_id.get(first_choice_id)
    if first_choice is None:
        return "First choice could not be evaluated because it does not match a known project."

    reasons: list[str] = []
    if not _has_required_skills(person, first_choice):
        reasons.append("student lacked required skills for the first-choice project")

    first_choice_assigned_count = sum(
        1
        for candidate_person in problem.people
        if solver.boolean_value(assignment_vars[(candidate_person.id, first_choice.id)])
    )
    if first_choice_assigned_count >= first_choice.capacity:
        reasons.append("first-choice project reached capacity")

    supervisor_limit = (problem.supervisor_limits or {}).get(first_choice.supervisor_id or "")
    if first_choice.supervisor_id and supervisor_limit is not None:
        supervisor_count = _assigned_supervisor_count(
            problem,
            assignment_vars,
            solver,
            first_choice.supervisor_id,
        )
        if supervisor_count >= supervisor_limit:
            reasons.append("supervisor limit affected the feasible set")

    if person.current_workload + first_choice.workload > person.max_workload:
        reasons.append("first-choice project would exceed the student's workload limit")

    if problem.fairness_weight:
        reasons.append("fairness objective may have favoured another assignment")
    if problem.workload_balance_weight:
        reasons.append("workload balancing may have favoured another assignment")

    if not reasons:
        return (
            "First choice was not assigned; exact causal attribution is not available yet "
            "because CP-SAT returns the selected optimum without a counterfactual proof."
        )
    return "First choice was not assigned because " + "; ".join(reasons) + "."


def _assigned_supervisor_count(
    problem: AllocationInput,
    assignment_vars: dict[tuple[str, str], cp_model.IntVar],
    solver: cp_model.CpSolver,
    supervisor_id: str | None,
) -> int:
    if supervisor_id is None:
        return 0
    return sum(
        1
        for person in problem.people
        for item in problem.items
        if item.supervisor_id == supervisor_id and solver.boolean_value(assignment_vars[(person.id, item.id)])
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

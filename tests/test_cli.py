from backend.fairmatch.cli import print_allocation_result, print_counterfactual_comparison
from backend.fairmatch.counterfactual import CounterfactualComparison
from backend.fairmatch.models import AllocationResult, Assignment, ExplanationDetail


def test_print_allocation_result_shows_metrics_and_explanation_notes(capsys):
    explanation = ExplanationDetail(
        person_id="s1",
        item_id="p1",
        assigned_item="Project One",
        preference_rank=1,
        satisfaction=3,
        skill_match=True,
        capacity_note="Project capacity respected: 1/1 slot(s) used.",
        skill_note="Required skills satisfied: python.",
        first_choice_note="Assigned project is the student's first choice.",
        supervisor_note="No supervisor limit applies to this project.",
        fairness_note="Fairness weight 1 was applied through the satisfaction gap objective.",
        workload_note="Workload becomes 1/3; workload balance weight 1 was included in the objective.",
        summary="Student One was assigned to Project One.",
    )
    result = AllocationResult(
        mode="school",
        status="OPTIMAL",
        objective_value=3,
        assignments=[
            Assignment(
                person_id="s1",
                person_name="Student One",
                item_id="p1",
                item_name="Project One",
                satisfaction=3,
                preference_rank=1,
                workload=1,
                skill_match=True,
                explanation=explanation,
            )
        ],
        total_satisfaction=3,
        average_satisfaction=3.0,
        min_satisfaction=3,
        max_satisfaction=3,
        fairness_gap=0,
        max_min_value=3,
        gini_coefficient=0.0,
        min_workload=1,
        max_workload=1,
        workload_gap=0,
    )

    print_allocation_result("Allocation Result", result)

    output = capsys.readouterr().out
    assert "Status: OPTIMAL" in output
    assert "Average satisfaction: 3.00" in output
    assert "Gini coefficient: 0.000" in output
    assert "Student One -> Project One" in output
    assert "First-choice note:" in output
    assert "Fairness note:" in output
    assert "Workload note:" in output


def test_print_counterfactual_comparison_shows_changed_assignments(capsys):
    comparison = CounterfactualComparison(
        baseline_total_satisfaction=7,
        fairness_total_satisfaction=5,
        baseline_fairness_gap=3,
        fairness_fairness_gap=1,
        baseline_max_min_value=0,
        fairness_max_min_value=1,
        baseline_gini_coefficient=0.19,
        fairness_gini_coefficient=0.13,
        changed_assignments={"s1": ("p1", "p2")},
        changed_satisfaction={"s1": (3, 2)},
        fairness_improved=True,
    )

    print_counterfactual_comparison(comparison)

    output = capsys.readouterr().out
    assert "Counterfactual Fairness Comparison" in output
    assert "Total satisfaction: 7 -> 5" in output
    assert "Fairness gap: 3 -> 1" in output
    assert "s1: p1 -> p2" in output
    assert "s1: 3 -> 2" in output

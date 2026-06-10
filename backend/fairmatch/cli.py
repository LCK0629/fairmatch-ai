from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path

from .counterfactual import CounterfactualComparison, compare_fairness_runs
from .models import AllocationResult
from .models import load_allocation_input
from .solver import solve_allocation


DEFAULT_COMPARISON_FAIRNESS_WEIGHT = 3
FAIRNESS_COMPARISON_WARNING = (
    "Warning: baseline and fairness run both use fairness_weight = 0. "
    "Counterfactual comparison may not be meaningful."
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a FairMatch AI allocation sample.")
    parser.add_argument("input_path", nargs="?", help="Path to a FairMatch JSON input file.")
    parser.add_argument("--input", dest="input_option", help="Path to a FairMatch JSON input file.")
    parser.add_argument(
        "--compare-fairness",
        action="store_true",
        help="Compare fairness_weight = 0 against a fairness-aware run.",
    )
    parser.add_argument(
        "--fairness-weight",
        type=int,
        default=DEFAULT_COMPARISON_FAIRNESS_WEIGHT,
        help="Fairness weight to use for --compare-fairness.",
    )
    parser.add_argument(
        "--output",
        choices=("text", "json"),
        default="text",
        help="Output format. Use text for demos or json for machine-readable output.",
    )
    args = parser.parse_args()

    selected_input = args.input_option or args.input_path
    if selected_input is None:
        parser.error("an input file is required; pass a path or use --input")

    input_path = Path(selected_input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))

    if args.compare_fairness:
        _run_fairness_comparison(payload, args.fairness_weight, args.output)
        return

    result = solve_allocation(load_allocation_input(payload))
    if args.output == "json":
        print(json.dumps(asdict(result), indent=2))
        return

    print_allocation_result("Allocation Result", result)


def _run_fairness_comparison(payload: dict, fairness_weight: int, output: str) -> None:
    baseline_result, fairness_result, comparison, warning = build_fairness_comparison(payload, fairness_weight)

    if output == "json":
        print(
            json.dumps(
                {
                    "baseline_result": asdict(baseline_result),
                    "fairness_result": asdict(fairness_result),
                    "counterfactual_comparison": asdict(comparison),
                    "warning": warning,
                },
                indent=2,
            )
        )
        return

    if warning:
        print("Warning:")
        print(warning.removeprefix("Warning: "))
        print()

    print_allocation_result("Baseline Allocation: fairness_weight = 0", baseline_result)
    print()
    print_allocation_result(
        f"Fairness-Aware Allocation: fairness_weight = {fairness_weight}",
        fairness_result,
    )
    print()
    print_counterfactual_comparison(comparison)


def build_fairness_comparison(
    payload: dict,
    fairness_weight: int,
) -> tuple[AllocationResult, AllocationResult, CounterfactualComparison, str | None]:
    baseline_payload = deepcopy(payload)
    fairness_payload = deepcopy(payload)
    baseline_payload["fairness_weight"] = 0
    fairness_payload["fairness_weight"] = fairness_weight

    baseline_result = solve_allocation(load_allocation_input(baseline_payload))
    fairness_result = solve_allocation(load_allocation_input(fairness_payload))
    comparison = compare_fairness_runs(baseline_result, fairness_result)
    warning = FAIRNESS_COMPARISON_WARNING if fairness_weight == 0 else None
    return baseline_result, fairness_result, comparison, warning


def print_allocation_result(title: str, result: AllocationResult) -> None:
    print(f"=== {title} ===")
    print(f"Status: {result.status}")
    print(f"Objective value: {result.objective_value}")
    print(f"Total satisfaction: {result.total_satisfaction}")
    print(f"Average satisfaction: {result.average_satisfaction:.2f}")
    print(f"Fairness gap: {result.fairness_gap}")
    print(f"Max-min value: {result.max_min_value}")
    print(f"Gini coefficient: {result.gini_coefficient:.3f}")
    print(f"Workload gap: {result.workload_gap}")

    if not result.assignments:
        print("Assignments: none")
        return

    print("Assignments:")
    for assignment in result.assignments:
        print(f"- {assignment.person_name} -> {assignment.item_name}")
        print(f"  Satisfaction: {assignment.satisfaction}")
        print(f"  Preference rank: {_format_preference_rank(assignment.preference_rank)}")
        print(f"  Summary: {assignment.explanation.summary}")
        print(f"  First-choice note: {assignment.explanation.first_choice_note}")
        print(f"  Fairness note: {assignment.explanation.fairness_note}")
        print(f"  Workload note: {assignment.explanation.workload_note}")


def print_counterfactual_comparison(comparison: CounterfactualComparison) -> None:
    print("=== Counterfactual Fairness Comparison ===")
    print("Baseline: fairness_weight = 0")
    print("Fairness-aware: fairness_weight > 0")
    print(
        "Total satisfaction: "
        f"{comparison.baseline_total_satisfaction} -> {comparison.fairness_total_satisfaction}"
    )
    print(
        "Fairness gap: "
        f"{comparison.baseline_fairness_gap} -> {comparison.fairness_fairness_gap}"
    )
    print(
        "Max-min value: "
        f"{comparison.baseline_max_min_value} -> {comparison.fairness_max_min_value}"
    )
    print(
        "Gini coefficient: "
        f"{comparison.baseline_gini_coefficient:.3f} -> {comparison.fairness_gini_coefficient:.3f}"
    )
    print(f"Fairness improved: {comparison.fairness_improved}")

    if comparison.changed_assignments:
        print("Changed assignments:")
        for person_id, (baseline_item, fairness_item) in sorted(comparison.changed_assignments.items()):
            print(f"- {person_id}: {baseline_item} -> {fairness_item}")
    else:
        print("Changed assignments: none")

    if comparison.changed_satisfaction:
        print("Changed satisfaction:")
        for person_id, (baseline_score, fairness_score) in sorted(comparison.changed_satisfaction.items()):
            print(f"- {person_id}: {baseline_score} -> {fairness_score}")
    else:
        print("Changed satisfaction: none")


def _format_preference_rank(preference_rank: int | None) -> str:
    if preference_rank is None:
        return "unranked"
    return str(preference_rank)


if __name__ == "__main__":
    main()

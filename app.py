from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import streamlit as st

from backend.fairmatch.counterfactual import compare_fairness_runs
from backend.fairmatch.models import AllocationResult, load_allocation_input
from backend.fairmatch.solver import solve_allocation


SAMPLE_DATASETS = {
    "School Sample": Path("data/school_sample.json"),
    "Fairness Weight Trade-Off": Path("data/school_cases/fairness_weight_tradeoff.json"),
}
DEFAULT_FAIRNESS_WEIGHT = 3


def main() -> None:
    st.set_page_config(page_title="FairMatch AI", layout="wide")
    st.title("FairMatch AI")
    st.caption("Explainable fairness-aware Student to Project allocation")

    payload = load_payload_from_sidebar()
    if payload is None:
        st.info("Select a sample dataset or upload a JSON file to begin.")
        return

    with st.sidebar:
        st.divider()
        run_allocation = st.button("Run Allocation", type="primary", use_container_width=True)
        run_comparison = st.button("Run Fairness Comparison", use_container_width=True)
        fairness_weight = st.number_input(
            "Comparison fairness weight",
            min_value=0,
            max_value=20,
            value=DEFAULT_FAIRNESS_WEIGHT,
            step=1,
        )

    st.subheader("Dataset Preview")
    render_dataset_preview(payload)

    if run_allocation:
        result = solve_payload(payload)
        render_allocation_result(result)

    if run_comparison:
        render_fairness_comparison(payload, int(fairness_weight))


def load_payload_from_sidebar() -> dict[str, Any] | None:
    with st.sidebar:
        st.header("Dataset")
        source = st.radio("Input source", ["Sample dataset", "Upload JSON"], index=0)

        if source == "Sample dataset":
            selected_name = st.selectbox("Sample", list(SAMPLE_DATASETS))
            return read_json_file(SAMPLE_DATASETS[selected_name])

        uploaded_file = st.file_uploader("Upload allocation JSON", type=["json"])
        if uploaded_file is None:
            return None

        try:
            return json.loads(uploaded_file.getvalue().decode("utf-8"))
        except json.JSONDecodeError as exc:
            st.error(f"Invalid JSON file: {exc}")
            return None


def read_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def solve_payload(payload: dict[str, Any]) -> AllocationResult:
    return solve_allocation(load_allocation_input(payload))


def render_dataset_preview(payload: dict[str, Any]) -> None:
    people_count = len(payload.get("people", []))
    item_count = len(payload.get("items", []))
    metric_columns = st.columns(4)
    metric_columns[0].metric("Mode", str(payload.get("mode", "unknown")))
    metric_columns[1].metric("People", people_count)
    metric_columns[2].metric("Projects", item_count)
    metric_columns[3].metric("Fairness Weight", int(payload.get("fairness_weight", 0)))

    with st.expander("Raw JSON"):
        st.json(payload)


def render_allocation_result(result: AllocationResult) -> None:
    st.subheader("Allocation Result")
    st.write(f"Solver status: `{result.status}`")

    render_fairness_metrics(result)
    render_assignment_table(result)
    render_explanations(result)


def render_fairness_metrics(result: AllocationResult) -> None:
    st.subheader("Fairness Metrics")
    first_row = st.columns(3)
    second_row = st.columns(3)

    first_row[0].metric("Total Satisfaction", result.total_satisfaction)
    first_row[1].metric("Average Satisfaction", f"{result.average_satisfaction:.2f}")
    first_row[2].metric("Fairness Gap", result.fairness_gap)
    second_row[0].metric("Max-Min Value", result.max_min_value)
    second_row[1].metric("Gini Coefficient", f"{result.gini_coefficient:.3f}")
    second_row[2].metric("Workload Gap", result.workload_gap)


def render_assignment_table(result: AllocationResult) -> None:
    st.subheader("Assignments")
    rows = [
        {
            "Student": assignment.person_name,
            "Assigned Project": assignment.item_name,
            "Satisfaction": assignment.satisfaction,
            "Preference Rank": assignment.preference_rank or "Unranked",
        }
        for assignment in result.assignments
    ]
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.warning("No assignments were returned by the solver.")


def render_explanations(result: AllocationResult) -> None:
    st.subheader("Explanations")
    if not result.assignments:
        st.info("No explanations are available because no assignments were returned.")
        return

    for assignment in result.assignments:
        with st.expander(f"{assignment.person_name} -> {assignment.item_name}"):
            st.write(assignment.explanation.summary)
            st.markdown(f"**First-choice note:** {assignment.explanation.first_choice_note}")
            st.markdown(f"**Fairness note:** {assignment.explanation.fairness_note}")
            st.markdown(f"**Workload note:** {assignment.explanation.workload_note}")


def render_fairness_comparison(payload: dict[str, Any], fairness_weight: int) -> None:
    baseline_payload = deepcopy(payload)
    fairness_payload = deepcopy(payload)
    baseline_payload["fairness_weight"] = 0
    fairness_payload["fairness_weight"] = fairness_weight

    baseline_result = solve_payload(baseline_payload)
    fairness_result = solve_payload(fairness_payload)
    comparison = compare_fairness_runs(baseline_result, fairness_result)

    st.subheader("Counterfactual Fairness Comparison")
    if fairness_weight == 0:
        st.warning(
            "Baseline and fairness-aware runs both use fairness_weight = 0. "
            "The comparison may not be meaningful."
        )

    metric_columns = st.columns(3)
    metric_columns[0].metric(
        "Total Satisfaction",
        f"{comparison.baseline_total_satisfaction} -> {comparison.fairness_total_satisfaction}",
    )
    metric_columns[1].metric(
        "Fairness Gap",
        f"{comparison.baseline_fairness_gap} -> {comparison.fairness_fairness_gap}",
    )
    metric_columns[2].metric(
        "Gini Coefficient",
        f"{comparison.baseline_gini_coefficient:.3f} -> {comparison.fairness_gini_coefficient:.3f}",
    )

    second_row = st.columns(3)
    second_row[0].metric(
        "Max-Min Value",
        f"{comparison.baseline_max_min_value} -> {comparison.fairness_max_min_value}",
    )
    second_row[1].metric("Fairness Improved", "Yes" if comparison.fairness_improved else "No")
    second_row[2].metric("Changed Assignments", len(comparison.changed_assignments))

    st.markdown("#### Changed Assignments")
    changed_assignment_rows = [
        {
            "Student ID": person_id,
            "Baseline Project": baseline_item,
            "Fairness Project": fairness_item,
        }
        for person_id, (baseline_item, fairness_item) in sorted(comparison.changed_assignments.items())
    ]
    if changed_assignment_rows:
        st.dataframe(changed_assignment_rows, use_container_width=True, hide_index=True)
    else:
        st.info("No assignment changes were detected.")

    st.markdown("#### Changed Satisfaction")
    changed_satisfaction_rows = [
        {
            "Student ID": person_id,
            "Baseline Satisfaction": baseline_score,
            "Fairness Satisfaction": fairness_score,
        }
        for person_id, (baseline_score, fairness_score) in sorted(comparison.changed_satisfaction.items())
    ]
    if changed_satisfaction_rows:
        st.dataframe(changed_satisfaction_rows, use_container_width=True, hide_index=True)
    else:
        st.info("No satisfaction changes were detected.")


if __name__ == "__main__":
    main()

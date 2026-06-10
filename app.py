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
    st.set_page_config(page_title="FairMatch AI", page_icon="FM", layout="wide")
    apply_theme()

    if "dashboard_started" not in st.session_state:
        st.session_state.dashboard_started = False

    if st.session_state.dashboard_started:
        render_dashboard()
    else:
        render_landing_page()


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f4f6f8;
            --surface: #ffffff;
            --ink: #1f2937;
            --muted: #64748b;
            --line: #d7dde5;
            --primary: #145c72;
            --primary-dark: #0f3f50;
        }

        .stApp {
            background: var(--bg);
            color: var(--ink);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"], #MainMenu, footer {
            display: none;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }

        [data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid var(--line);
        }

        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            color: var(--ink);
            opacity: 1;
        }

        [data-testid="stSidebar"] [data-baseweb="select"] > div,
        [data-testid="stSidebar"] [data-baseweb="input"] > div {
            background: #ffffff;
            border-color: var(--line);
            color: var(--ink);
        }

        [data-testid="stSidebar"] input {
            background: #ffffff;
            color: var(--ink);
        }

        [data-testid="stSidebar"] button[kind="secondary"] {
            background: #ffffff;
            color: var(--ink);
            border-color: var(--line);
        }

        [data-testid="stSidebar"] [role="radio"][aria-checked="true"] {
            background-color: var(--primary);
            border-color: var(--primary);
        }

        [data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {
            border-color: #334155;
        }

        [data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child > div {
            background-color: transparent;
        }

        [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) > div:first-child {
            border-color: var(--primary);
        }

        [data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) > div:first-child > div {
            background-color: var(--primary);
        }

        h1, h2, h3 {
            color: var(--ink);
            letter-spacing: 0;
        }

        p, li, span {
            letter-spacing: 0;
        }

        div[data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 14px 16px;
        }

        div[data-testid="stMetric"] * {
            color: var(--ink);
            opacity: 1;
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        .stButton > button {
            border-radius: 6px;
            min-height: 42px;
            font-weight: 600;
            border: 1px solid var(--line);
            background: #ffffff;
            color: var(--ink);
            box-shadow: none;
        }

        .stButton > button:hover {
            border-color: var(--primary);
            color: var(--primary);
            background: #f8fafc;
        }

        .stButton > button[kind="primary"] {
            background: var(--primary);
            border-color: var(--primary);
            color: #ffffff;
        }

        .stButton > button[kind="primary"] *,
        .stButton > button[kind="primary"] p,
        .stButton > button[kind="primary"] span {
            color: #ffffff;
        }

        .stButton > button[kind="primary"]:hover {
            background: var(--primary-dark);
            border-color: var(--primary-dark);
            color: #ffffff;
        }

        .fm-shell {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 28px;
        }

        .fm-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 26px;
        }

        .fm-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 700;
            font-size: 1.02rem;
        }

        .fm-logo {
            width: 36px;
            height: 36px;
            border-radius: 6px;
            background: var(--primary);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.95rem;
        }

        .fm-small {
            color: var(--muted);
            font-size: 0.9rem;
        }

        .fm-hero {
            max-width: 760px;
            padding: 18px 0 10px;
        }

        .fm-kicker {
            color: var(--primary);
            font-weight: 700;
            font-size: 0.92rem;
            margin-bottom: 10px;
        }

        .fm-title {
            font-size: 2.45rem;
            line-height: 1.15;
            margin: 0 0 14px;
            color: var(--ink);
        }

        .fm-lede {
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.65;
            max-width: 720px;
            margin-bottom: 24px;
        }

        .fm-divider {
            height: 1px;
            background: var(--line);
            margin: 26px 0;
        }

        .fm-feature-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
        }

        .fm-feature {
            border: 1px solid var(--line);
            border-radius: 6px;
            background: #fbfcfd;
            padding: 14px;
            min-height: 118px;
        }

        .fm-feature-title {
            font-weight: 700;
            color: var(--ink);
            font-size: 0.95rem;
            margin-bottom: 8px;
        }

        .fm-feature-text {
            color: var(--muted);
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .fm-status {
            background: #ffffff;
            border: 1px solid var(--line);
            border-left: 4px solid var(--primary);
            border-radius: 6px;
            padding: 12px 14px;
            margin-bottom: 16px;
            color: var(--muted);
        }

        .fm-status strong {
            color: var(--ink);
        }

        .fm-section-title {
            margin-top: 18px;
            margin-bottom: 10px;
            color: var(--ink);
            font-size: 1.15rem;
        }

        .fm-note {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.5;
        }

        @media (max-width: 900px) {
            .fm-feature-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .fm-title {
                font-size: 2rem;
            }
        }

        @media (max-width: 620px) {
            .fm-feature-grid {
                grid-template-columns: 1fr;
            }

            .fm-header {
                align-items: flex-start;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_landing_page() -> None:
    st.markdown(
        """
        <div class="fm-shell">
            <div class="fm-header">
                <div class="fm-brand">
                    <div class="fm-logo">FM</div>
                    <div>FairMatch AI</div>
                </div>
                <div class="fm-small">CSIT-26-S3-06</div>
            </div>
            <div class="fm-hero">
                <div class="fm-kicker">Explainable fairness-aware allocation</div>
                <h1 class="fm-title">Student to Project Allocation Dashboard</h1>
                <div class="fm-lede">
                    FairMatch AI helps coordinators allocate students to projects using
                    constraint optimisation, fairness metrics, and structured decision
                    explanations.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_column, right_column = st.columns([0.22, 0.78])
    with left_column:
        if st.button("Start", type="primary", use_container_width=True):
            st.session_state.dashboard_started = True
            st.rerun()
    with right_column:
        st.markdown(
            '<div class="fm-note">Open the dashboard to run allocation scenarios and inspect fairness outcomes.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="fm-feature-grid">
            <div class="fm-feature">
                <div class="fm-feature-title">Constraint Solver</div>
                <div class="fm-feature-text">Uses OR-Tools CP-SAT with hard constraints and weighted objectives.</div>
            </div>
            <div class="fm-feature">
                <div class="fm-feature-title">Fairness Metrics</div>
                <div class="fm-feature-text">Reports satisfaction gap, max-min value, Gini coefficient, and workload gap.</div>
            </div>
            <div class="fm-feature">
                <div class="fm-feature-title">Transparent Logic</div>
                <div class="fm-feature-text">Shows assignment summaries, first-choice notes, fairness notes, and workload notes.</div>
            </div>
            <div class="fm-feature">
                <div class="fm-feature-title">Counterfactual View</div>
                <div class="fm-feature-text">Compares baseline and fairness-aware allocation runs.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard() -> None:
    render_dashboard_header()
    payload = load_payload_from_sidebar()
    if payload is None:
        st.info("Select a sample dataset or upload a JSON file to begin.")
        return

    with st.sidebar:
        st.divider()
        st.subheader("Actions")
        run_allocation = st.button("Run Allocation", type="primary", use_container_width=True)
        run_comparison = st.button("Run Fairness Comparison", use_container_width=True)
        fairness_weight = st.number_input(
            "Comparison fairness weight",
            min_value=0,
            max_value=20,
            value=DEFAULT_FAIRNESS_WEIGHT,
            step=1,
        )
        st.divider()
        if st.button("Back to Landing Page", use_container_width=True):
            st.session_state.dashboard_started = False
            st.rerun()

    render_dataset_preview(payload)

    if run_allocation:
        result = solve_payload(payload)
        render_allocation_result(result)

    if run_comparison:
        render_fairness_comparison(payload, int(fairness_weight))


def render_dashboard_header() -> None:
    st.markdown(
        """
        <div class="fm-header">
            <div class="fm-brand">
                <div class="fm-logo">FM</div>
                <div>FairMatch AI Dashboard</div>
            </div>
            <div class="fm-small">Decision Support Console</div>
        </div>
        <div class="fm-status">
            <strong>School Mode:</strong>
            allocate students to projects with fairness metrics and structured explanations.
        </div>
        """,
        unsafe_allow_html=True,
    )


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
    st.markdown('<h3 class="fm-section-title">Dataset</h3>', unsafe_allow_html=True)
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
    st.markdown('<h3 class="fm-section-title">Allocation Result</h3>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="fm-status">
            <strong>Solver status:</strong> {result.status}
            &nbsp;&nbsp; <strong>Objective value:</strong> {result.objective_value}
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_fairness_metrics(result)
    render_assignment_table(result)
    render_explanations(result)


def render_fairness_metrics(result: AllocationResult) -> None:
    st.markdown('<h3 class="fm-section-title">Fairness Metrics</h3>', unsafe_allow_html=True)
    first_row = st.columns(3)
    second_row = st.columns(3)

    first_row[0].metric("Total Satisfaction", result.total_satisfaction)
    first_row[1].metric("Average Satisfaction", f"{result.average_satisfaction:.2f}")
    first_row[2].metric("Fairness Gap", result.fairness_gap)
    second_row[0].metric("Max-Min Value", result.max_min_value)
    second_row[1].metric("Gini Coefficient", f"{result.gini_coefficient:.3f}")
    second_row[2].metric("Workload Gap", result.workload_gap)


def render_assignment_table(result: AllocationResult) -> None:
    st.markdown('<h3 class="fm-section-title">Assignments</h3>', unsafe_allow_html=True)
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
    st.markdown('<h3 class="fm-section-title">Explanations</h3>', unsafe_allow_html=True)
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

    st.markdown(
        '<h3 class="fm-section-title">Counterfactual Fairness Comparison</h3>',
        unsafe_allow_html=True,
    )
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

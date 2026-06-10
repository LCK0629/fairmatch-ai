from __future__ import annotations

from copy import deepcopy
from html import escape
import json
from pathlib import Path
from typing import Any

import streamlit as st

from backend.fairmatch.counterfactual import CounterfactualComparison, compare_fairness_runs
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
    initialise_state()

    if st.session_state.dashboard_started:
        render_dashboard()
    else:
        render_landing_page()


def initialise_state() -> None:
    defaults = {
        "dashboard_started": False,
        "active_payload": read_json_file(SAMPLE_DATASETS["School Sample"]),
        "active_dataset_name": "School Sample",
        "allocation_result": None,
        "comparison": None,
        "baseline_result": None,
        "fairness_result": None,
        "comparison_warning": "",
        "comparison_fairness_weight": DEFAULT_FAIRNESS_WEIGHT,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg: #f5f7fa;
            --surface: #ffffff;
            --surface-soft: #f9fafb;
            --ink: #182230;
            --muted: #667085;
            --line: #d8dee8;
            --primary: #145c72;
            --primary-dark: #0f3f50;
            --accent: #8a5a12;
            --positive: #176b4d;
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
            max-width: 1180px;
            padding-top: 1.35rem;
            padding-bottom: 2.5rem;
        }

        h1, h2, h3, p, li, span {
            letter-spacing: 0;
        }

        h1, h2, h3 {
            color: var(--ink);
        }

        .stButton > button {
            border-radius: 6px;
            min-height: 42px;
            font-weight: 650;
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

        div[data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 16px 18px;
        }

        div[data-testid="stMetric"] * {
            color: var(--ink);
            opacity: 1;
        }

        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        label[data-baseweb="radio"] > div:first-child {
            border-color: #334155;
        }

        label[data-baseweb="radio"] > div:first-child > div {
            background-color: transparent;
        }

        label[data-baseweb="radio"]:has(input:checked) > div:first-child {
            border-color: var(--primary) !important;
        }

        label[data-baseweb="radio"]:has(input:checked) > div:first-child > div {
            background-color: var(--primary) !important;
        }

        input[type="radio"] {
            accent-color: var(--primary) !important;
        }

        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] *,
        [data-testid="stRadio"] p,
        [data-testid="stRadio"] span {
            color: var(--ink) !important;
            opacity: 1 !important;
        }

        [data-baseweb="select"] > div,
        [data-baseweb="input"] > div,
        [data-baseweb="base-input"] {
            background: #ffffff !important;
            border-color: var(--line) !important;
            color: var(--ink) !important;
        }

        [data-baseweb="select"] *,
        [data-baseweb="input"] *,
        [data-baseweb="base-input"] *,
        input {
            color: var(--ink) !important;
        }

        [data-testid="stNumberInput"] button {
            background: #ffffff !important;
            border-color: var(--line) !important;
            color: var(--ink) !important;
        }

        [data-testid="stNumberInput"] button * {
            color: var(--ink) !important;
        }

        [data-testid="stFileUploader"] section {
            background: #ffffff !important;
            border: 1px solid var(--line) !important;
            border-radius: 8px;
        }

        [data-testid="stFileUploader"] section * {
            color: var(--ink) !important;
        }

        [data-testid="stFileUploader"] button {
            background: #ffffff !important;
            border: 1px solid var(--line) !important;
            color: var(--ink) !important;
        }

        button[data-baseweb="tab"] {
            color: var(--muted) !important;
        }

        button[data-baseweb="tab"] * {
            color: var(--muted) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--primary) !important;
            border-bottom-color: var(--primary) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] * {
            color: var(--primary) !important;
        }

        [data-baseweb="tab-highlight"] {
            background-color: var(--primary) !important;
        }

        .fm-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 16px;
        }

        .fm-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 750;
            color: var(--ink);
        }

        .fm-logo {
            width: 38px;
            height: 38px;
            border-radius: 7px;
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
            font-size: 0.92rem;
        }

        .fm-landing {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            min-height: 520px;
            padding: 34px;
            display: grid;
            grid-template-columns: minmax(0, 1.1fr) minmax(300px, 0.9fr);
            gap: 34px;
            align-items: center;
        }

        .fm-kicker {
            color: var(--primary);
            font-size: 0.92rem;
            font-weight: 750;
            margin-bottom: 12px;
        }

        .fm-title {
            color: var(--ink);
            font-size: 2.75rem;
            line-height: 1.12;
            margin: 0 0 18px;
            max-width: 760px;
        }

        .fm-lede {
            color: var(--muted);
            font-size: 1.04rem;
            line-height: 1.7;
            max-width: 720px;
            margin-bottom: 26px;
        }

        .fm-hero-panel {
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--surface-soft);
            padding: 22px;
        }

        .fm-panel-title {
            font-weight: 750;
            color: var(--ink);
            margin-bottom: 12px;
        }

        .fm-signal-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin-top: 14px;
        }

        .fm-signal {
            border: 1px solid var(--line);
            border-radius: 7px;
            background: #ffffff;
            padding: 13px;
        }

        .fm-signal-value {
            color: var(--ink);
            font-size: 1.35rem;
            font-weight: 800;
            line-height: 1.1;
        }

        .fm-signal-label {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 4px;
        }

        .fm-flow {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 20px;
        }

        .fm-chip {
            border: 1px solid var(--line);
            border-radius: 999px;
            background: #ffffff;
            color: var(--ink);
            font-size: 0.84rem;
            padding: 7px 11px;
        }

        .fm-dashboard-header {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 22px;
            margin-bottom: 18px;
        }

        .fm-dashboard-title {
            font-size: 1.75rem;
            line-height: 1.2;
            font-weight: 800;
            margin: 0 0 8px;
            color: var(--ink);
        }

        .fm-dashboard-copy {
            color: var(--muted);
            line-height: 1.6;
            max-width: 860px;
            margin: 0;
        }

        .fm-band {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 16px;
        }

        .fm-section-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 750;
            margin-bottom: 6px;
            text-transform: uppercase;
        }

        .fm-section-title {
            color: var(--ink);
            font-size: 1.18rem;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .fm-note {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .fm-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 16px;
            min-height: 120px;
        }

        .fm-metric-card {
            background: var(--surface);
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 18px;
            min-height: 112px;
        }

        .fm-metric-label {
            color: var(--muted);
            font-size: 0.84rem;
            font-weight: 650;
            margin-bottom: 8px;
        }

        .fm-metric-value {
            color: var(--ink);
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.1;
        }

        .fm-metric-hint {
            color: var(--muted);
            font-size: 0.8rem;
            margin-top: 7px;
        }

        .fm-status-line {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 12px;
        }

        .fm-pill {
            border-radius: 999px;
            border: 1px solid var(--line);
            background: var(--surface-soft);
            color: var(--ink);
            padding: 7px 10px;
            font-size: 0.84rem;
        }

        .fm-pill strong {
            color: var(--primary);
        }

        .fm-explanation-title {
            color: var(--ink);
            font-weight: 800;
            font-size: 1.05rem;
            margin-bottom: 8px;
        }

        .fm-explanation-summary {
            color: var(--ink);
            line-height: 1.55;
            margin-bottom: 12px;
        }

        .fm-explanation-note {
            border-top: 1px solid var(--line);
            padding-top: 10px;
            margin-top: 10px;
            color: var(--muted);
            line-height: 1.5;
            font-size: 0.92rem;
        }

        .fm-table {
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 8px;
            overflow: hidden;
            font-size: 0.92rem;
        }

        .fm-table th {
            background: #f8fafc;
            color: var(--muted);
            font-weight: 750;
            text-align: left;
            padding: 11px 12px;
            border-bottom: 1px solid var(--line);
        }

        .fm-table td {
            color: var(--ink);
            padding: 11px 12px;
            border-bottom: 1px solid #edf1f5;
            vertical-align: top;
        }

        .fm-table tr:last-child td {
            border-bottom: none;
        }

        @media (max-width: 920px) {
            .fm-landing {
                grid-template-columns: 1fr;
                min-height: auto;
            }

            .fm-title {
                font-size: 2.25rem;
            }

            .fm-topbar {
                align-items: flex-start;
                flex-direction: column;
            }
        }

        @media (max-width: 620px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .fm-landing {
                padding: 22px;
            }

            .fm-title {
                font-size: 2rem;
            }

            .fm-signal-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_landing_page() -> None:
    st.markdown(
        """
        <div class="fm-topbar">
            <div class="fm-brand">
                <div class="fm-logo">FM</div>
                <div>FairMatch AI</div>
            </div>
            <div class="fm-small">CSIT-26-S3-06</div>
        </div>
        <section class="fm-landing">
            <div>
                <div class="fm-kicker">Explainable fairness-aware allocation</div>
                <h1 class="fm-title">Decision support for student-project allocation</h1>
                <div class="fm-lede">
                    FairMatch AI helps coordinators produce valid allocations, inspect fairness
                    trade-offs, and explain allocation decisions using a constraint optimisation
                    engine built on Google OR-Tools CP-SAT.
                </div>
                <div class="fm-flow">
                    <div class="fm-chip">School Mode first</div>
                    <div class="fm-chip">Fairness metrics</div>
                    <div class="fm-chip">Structured explanations</div>
                    <div class="fm-chip">Counterfactual comparison</div>
                </div>
            </div>
            <div class="fm-hero-panel">
                <div class="fm-panel-title">Core demonstration flow</div>
                <div class="fm-note">
                    Start with a dataset, run the allocation engine, inspect fairness metrics,
                    then compare fairness-aware and baseline outcomes.
                </div>
                <div class="fm-signal-grid">
                    <div class="fm-signal">
                        <div class="fm-signal-value">1</div>
                        <div class="fm-signal-label">School Mode scope</div>
                    </div>
                    <div class="fm-signal">
                        <div class="fm-signal-value">24</div>
                        <div class="fm-signal-label">verified tests</div>
                    </div>
                    <div class="fm-signal">
                        <div class="fm-signal-value">5</div>
                        <div class="fm-signal-label">fairness measures</div>
                    </div>
                    <div class="fm-signal">
                        <div class="fm-signal-value">0</div>
                        <div class="fm-signal-label">LLM decisions</div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    start_column, note_column = st.columns([0.24, 0.76])
    with start_column:
        if st.button("Start Dashboard", type="primary", use_container_width=True):
            st.session_state.dashboard_started = True
            st.session_state.comparison_fairness_weight = DEFAULT_FAIRNESS_WEIGHT
            st.rerun()
    with note_column:
        st.markdown(
            '<div class="fm-note">The dashboard uses the existing backend solver and comparison helpers.</div>',
            unsafe_allow_html=True,
        )


def render_dashboard() -> None:
    render_dashboard_header()
    render_scenario_panel()

    tabs = st.tabs(["Allocation", "Fairness", "Counterfactual", "Dataset"])
    with tabs[0]:
        render_allocation_workspace(st.session_state.allocation_result)
    with tabs[1]:
        render_fairness_workspace(st.session_state.allocation_result)
    with tabs[2]:
        render_counterfactual_workspace(
            st.session_state.comparison,
            st.session_state.baseline_result,
            st.session_state.fairness_result,
            st.session_state.comparison_warning,
        )
    with tabs[3]:
        render_dataset_workspace(st.session_state.active_payload)


def render_dashboard_header() -> None:
    st.markdown(
        """
        <div class="fm-topbar">
            <div class="fm-brand">
                <div class="fm-logo">FM</div>
                <div>FairMatch AI</div>
            </div>
            <div class="fm-small">Decision Support Console</div>
        </div>
        <section class="fm-dashboard-header">
            <div class="fm-section-label">School Mode</div>
            <h1 class="fm-dashboard-title">Project allocation workspace</h1>
            <p class="fm-dashboard-copy">
                Select a scenario, run the optimiser, and review allocation quality through
                assignments, fairness metrics, structured explanations, and counterfactual
                fairness comparison.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_scenario_panel() -> None:
    st.markdown('<div class="fm-section-label">Scenario</div>', unsafe_allow_html=True)
    st.markdown('<div class="fm-section-title">Dataset and run controls</div>', unsafe_allow_html=True)

    source_column, dataset_column, upload_column = st.columns([0.24, 0.34, 0.42])
    with source_column:
        source = st.radio(
            "Input source",
            ["Sample dataset", "Upload JSON"],
            index=0,
            horizontal=False,
        )
    with dataset_column:
        selected_name = st.selectbox("Sample dataset", list(SAMPLE_DATASETS))
    with upload_column:
        uploaded_file = st.file_uploader("Custom allocation JSON", type=["json"])

    payload = resolve_payload(source, selected_name, uploaded_file)
    if payload is not None:
        st.session_state.active_payload = payload
        st.session_state.active_dataset_name = selected_name if source == "Sample dataset" else "Uploaded JSON"

    render_dataset_summary(st.session_state.active_payload, st.session_state.active_dataset_name)

    action_columns = st.columns([0.2, 0.24, 0.2, 0.36])
    with action_columns[0]:
        if st.button("Run Allocation", type="primary", use_container_width=True):
            st.session_state.allocation_result = solve_payload(st.session_state.active_payload)
    with action_columns[1]:
        if st.button("Run Fairness Comparison", use_container_width=True):
            run_fairness_comparison(int(st.session_state.comparison_fairness_weight))
    with action_columns[2]:
        st.number_input(
            "Fairness weight",
            min_value=0,
            max_value=20,
            step=1,
            key="comparison_fairness_weight",
        )
    with action_columns[3]:
        if st.button("Back to Landing Page", use_container_width=True):
            st.session_state.dashboard_started = False
            st.rerun()


def resolve_payload(
    source: str,
    selected_name: str,
    uploaded_file: Any,
) -> dict[str, Any] | None:
    if source == "Sample dataset":
        return read_json_file(SAMPLE_DATASETS[selected_name])

    if uploaded_file is None:
        st.info("Upload a JSON dataset to replace the current scenario.")
        return st.session_state.active_payload

    try:
        return json.loads(uploaded_file.getvalue().decode("utf-8"))
    except json.JSONDecodeError as exc:
        st.error(f"Invalid JSON file: {exc}")
        return st.session_state.active_payload


def read_json_file(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def solve_payload(payload: dict[str, Any]) -> AllocationResult:
    return solve_allocation(load_allocation_input(payload))


def run_fairness_comparison(fairness_weight: int) -> None:
    baseline_payload = deepcopy(st.session_state.active_payload)
    fairness_payload = deepcopy(st.session_state.active_payload)
    baseline_payload["fairness_weight"] = 0
    fairness_payload["fairness_weight"] = fairness_weight

    baseline_result = solve_payload(baseline_payload)
    fairness_result = solve_payload(fairness_payload)
    comparison = compare_fairness_runs(baseline_result, fairness_result)

    st.session_state.baseline_result = baseline_result
    st.session_state.fairness_result = fairness_result
    st.session_state.comparison = comparison
    st.session_state.comparison_warning = (
        "Baseline and fairness-aware runs both use fairness_weight = 0. The comparison may not be meaningful."
        if fairness_weight == 0
        else ""
    )


def render_dataset_summary(payload: dict[str, Any], dataset_name: str) -> None:
    people_count = len(payload.get("people", []))
    item_count = len(payload.get("items", []))
    fairness_weight = int(payload.get("fairness_weight", 0))
    mode = str(payload.get("mode", "unknown"))
    st.markdown(
        f"""
        <div class="fm-status-line">
            <div class="fm-pill"><strong>Dataset</strong> {escape(dataset_name)}</div>
            <div class="fm-pill"><strong>Mode</strong> {escape(mode)}</div>
            <div class="fm-pill"><strong>People</strong> {people_count}</div>
            <div class="fm-pill"><strong>Projects</strong> {item_count}</div>
            <div class="fm-pill"><strong>Fairness Weight</strong> {fairness_weight}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_allocation_workspace(result: AllocationResult | None) -> None:
    if result is None:
        render_empty_state("Run Allocation to review project assignments and decision explanations.")
        return

    st.markdown(
        f"""
        <div class="fm-status-line">
            <div class="fm-pill"><strong>Status</strong> {escape(result.status)}</div>
            <div class="fm-pill"><strong>Objective</strong> {result.objective_value}</div>
            <div class="fm-pill"><strong>Total Satisfaction</strong> {result.total_satisfaction}</div>
            <div class="fm-pill"><strong>Fairness Gap</strong> {result.fairness_gap}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    table_column, explanation_column = st.columns([0.64, 0.36])
    with table_column:
        st.markdown('<div class="fm-section-title">Assigned Projects</div>', unsafe_allow_html=True)
        rows = allocation_rows(result)
        if rows:
            render_html_table(rows)
        else:
            st.warning("No assignments were returned by the solver.")

    with explanation_column:
        st.markdown('<div class="fm-section-title">Decision Detail</div>', unsafe_allow_html=True)
        render_explanation_detail(result)


def allocation_rows(result: AllocationResult) -> list[dict[str, Any]]:
    return [
        {
            "Student": assignment.person_name,
            "Assigned Project": assignment.item_name,
            "Satisfaction": assignment.satisfaction,
            "Preference Rank": assignment.preference_rank or "Unranked",
        }
        for assignment in result.assignments
    ]


def render_explanation_detail(result: AllocationResult) -> None:
    if not result.assignments:
        st.info("No explanations are available.")
        return

    names = [f"{assignment.person_name} -> {assignment.item_name}" for assignment in result.assignments]
    selected = st.selectbox("Student explanation", names)
    assignment = result.assignments[names.index(selected)]
    explanation = assignment.explanation

    st.markdown(
        f"""
        <div class="fm-card">
            <div class="fm-explanation-title">{escape(assignment.person_name)} assigned to {escape(assignment.item_name)}</div>
            <div class="fm-explanation-summary">{escape(explanation.summary)}</div>
            <div class="fm-explanation-note"><strong>First choice:</strong> {escape(explanation.first_choice_note)}</div>
            <div class="fm-explanation-note"><strong>Fairness:</strong> {escape(explanation.fairness_note)}</div>
            <div class="fm-explanation-note"><strong>Workload:</strong> {escape(explanation.workload_note)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_fairness_workspace(result: AllocationResult | None) -> None:
    if result is None:
        render_empty_state("Run Allocation to inspect satisfaction and fairness metrics.")
        return

    st.markdown('<div class="fm-section-title">Fairness Overview</div>', unsafe_allow_html=True)
    metric_cards(
        [
            ("Total Satisfaction", result.total_satisfaction, "Overall preference score"),
            ("Average Satisfaction", f"{result.average_satisfaction:.2f}", "Mean student outcome"),
            ("Fairness Gap", result.fairness_gap, "Highest minus lowest satisfaction"),
            ("Max-Min Value", result.max_min_value, "Worst student satisfaction"),
            ("Gini Coefficient", f"{result.gini_coefficient:.3f}", "Distribution inequality"),
            ("Workload Gap", result.workload_gap, "Spread in assigned workload"),
        ]
    )

    st.markdown(
        """
        <div class="fm-band">
            <div class="fm-section-label">Interpretation</div>
            <div class="fm-note">
                Lower fairness gap and lower Gini coefficient indicate more balanced outcomes.
                Total satisfaction should be read together with fairness metrics because a high
                total score can still hide uneven individual outcomes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_cards(metrics: list[tuple[str, Any, str]]) -> None:
    for start in range(0, len(metrics), 3):
        columns = st.columns(3)
        for column, (label, value, hint) in zip(columns, metrics[start : start + 3]):
            with column:
                st.markdown(
                    f"""
                    <div class="fm-metric-card">
                        <div class="fm-metric-label">{escape(str(label))}</div>
                        <div class="fm-metric-value">{escape(str(value))}</div>
                        <div class="fm-metric-hint">{escape(str(hint))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_counterfactual_workspace(
    comparison: CounterfactualComparison | None,
    baseline_result: AllocationResult | None,
    fairness_result: AllocationResult | None,
    warning: str,
) -> None:
    if comparison is None or baseline_result is None or fairness_result is None:
        render_empty_state("Run Fairness Comparison to compare baseline and fairness-aware outcomes.")
        return

    if warning:
        st.warning(warning)

    st.markdown('<div class="fm-section-title">Baseline vs Fairness-Aware Run</div>', unsafe_allow_html=True)
    metric_cards(
        [
            (
                "Total Satisfaction",
                f"{comparison.baseline_total_satisfaction} -> {comparison.fairness_total_satisfaction}",
                "Preference trade-off",
            ),
            (
                "Fairness Gap",
                f"{comparison.baseline_fairness_gap} -> {comparison.fairness_fairness_gap}",
                "Lower is better",
            ),
            (
                "Gini Coefficient",
                f"{comparison.baseline_gini_coefficient:.3f} -> {comparison.fairness_gini_coefficient:.3f}",
                "Lower is more equal",
            ),
            (
                "Max-Min Value",
                f"{comparison.baseline_max_min_value} -> {comparison.fairness_max_min_value}",
                "Worst-outcome comparison",
            ),
            ("Fairness Improved", "Yes" if comparison.fairness_improved else "No", "Metric comparison result"),
            ("Changed Assignments", len(comparison.changed_assignments), "Students assigned differently"),
        ]
    )

    changed_column, satisfaction_column = st.columns(2)
    with changed_column:
        st.markdown('<div class="fm-section-title">Changed Assignments</div>', unsafe_allow_html=True)
        changed_assignment_rows = [
            {
                "Student ID": person_id,
                "Baseline Project": baseline_item,
                "Fairness Project": fairness_item,
            }
            for person_id, (baseline_item, fairness_item) in sorted(comparison.changed_assignments.items())
        ]
        if changed_assignment_rows:
            render_html_table(changed_assignment_rows)
        else:
            st.info("No assignment changes were detected.")

    with satisfaction_column:
        st.markdown('<div class="fm-section-title">Changed Satisfaction</div>', unsafe_allow_html=True)
        changed_satisfaction_rows = [
            {
                "Student ID": person_id,
                "Baseline Satisfaction": baseline_score,
                "Fairness Satisfaction": fairness_score,
            }
            for person_id, (baseline_score, fairness_score) in sorted(comparison.changed_satisfaction.items())
        ]
        if changed_satisfaction_rows:
            render_html_table(changed_satisfaction_rows)
        else:
            st.info("No satisfaction changes were detected.")


def render_dataset_workspace(payload: dict[str, Any]) -> None:
    left_column, right_column = st.columns([0.36, 0.64])
    with left_column:
        st.markdown('<div class="fm-section-title">Scenario Summary</div>', unsafe_allow_html=True)
        render_dataset_summary(payload, st.session_state.active_dataset_name)
    with right_column:
        st.markdown('<div class="fm-section-title">Raw Dataset</div>', unsafe_allow_html=True)
        st.json(payload)


def render_empty_state(message: str) -> None:
    st.markdown(
        f"""
        <div class="fm-band">
            <div class="fm-section-label">Ready</div>
            <div class="fm-note">{escape(message)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_html_table(rows: list[dict[str, Any]]) -> None:
    if not rows:
        return

    headers = list(rows[0])
    header_html = "".join(f"<th>{escape(str(header))}</th>" for header in headers)
    body_html = ""
    for row in rows:
        cells = "".join(f"<td>{escape(str(row.get(header, '')))}</td>" for header in headers)
        body_html += f"<tr>{cells}</tr>"

    st.markdown(
        f"""
        <table class="fm-table">
            <thead><tr>{header_html}</tr></thead>
            <tbody>{body_html}</tbody>
        </table>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

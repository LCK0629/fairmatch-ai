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
            --bg: #f6f7f9;
            --surface: #ffffff;
            --surface-soft: #fafbfc;
            --ink: #101828;
            --muted: #667085;
            --quiet: #98a2b3;
            --line: #d9dee7;
            --primary: #145c72;
            --primary-dark: #0f4050;
            --primary-soft: #e7f1f4;
            --gold: #9a6a1f;
            --green: #166c4d;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(20, 92, 114, 0.08), transparent 30%),
                var(--bg);
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
            padding-top: 1.25rem;
            padding-bottom: 2.5rem;
        }

        h1, h2, h3, p, li, span {
            letter-spacing: 0;
        }

        .stButton > button {
            border-radius: 8px;
            min-height: 44px;
            font-weight: 700;
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

        [data-testid="stWidgetLabel"],
        [data-testid="stWidgetLabel"] *,
        [data-testid="stRadio"] p,
        [data-testid="stRadio"] span {
            color: var(--ink) !important;
            opacity: 1 !important;
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

        [data-testid="stNumberInput"] button,
        [data-testid="stFileUploader"] button {
            background: #ffffff !important;
            border: 1px solid var(--line) !important;
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

        button[data-baseweb="tab"] {
            color: var(--muted) !important;
            font-weight: 700 !important;
        }

        button[data-baseweb="tab"] * {
            color: var(--muted) !important;
        }

        button[data-baseweb="tab"][aria-selected="true"],
        button[data-baseweb="tab"][aria-selected="true"] * {
            color: var(--primary) !important;
        }

        [data-baseweb="tab-highlight"] {
            background-color: var(--primary) !important;
        }

        .fm-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 20px;
        }

        .fm-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 800;
            color: var(--ink);
        }

        .fm-logo {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: var(--ink);
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

        .fm-hero {
            background: linear-gradient(180deg, #ffffff 0%, #fbfcfd 100%);
            border: 1px solid var(--line);
            border-radius: 14px;
            min-height: 560px;
            padding: 52px;
            display: grid;
            grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
            gap: 44px;
            align-items: center;
            box-shadow: 0 18px 50px rgba(16, 24, 40, 0.06);
        }

        .fm-kicker {
            color: var(--primary);
            font-size: 0.92rem;
            font-weight: 800;
            margin-bottom: 14px;
            text-transform: uppercase;
        }

        .fm-hero-title {
            color: var(--ink);
            font-size: 4rem;
            line-height: 1;
            margin: 0 0 16px;
            font-weight: 850;
        }

        .fm-hero-subtitle {
            color: var(--ink);
            font-size: 1.35rem;
            font-weight: 750;
            margin-bottom: 18px;
        }

        .fm-hero-copy {
            color: var(--muted);
            font-size: 1.12rem;
            line-height: 1.75;
            max-width: 680px;
            margin-bottom: 26px;
        }

        .fm-preview {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: #ffffff;
            padding: 20px;
            box-shadow: 0 14px 34px rgba(16, 24, 40, 0.08);
        }

        .fm-preview-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            padding: 12px 0;
            border-bottom: 1px solid #edf1f5;
        }

        .fm-preview-row:last-child {
            border-bottom: none;
        }

        .fm-preview-label {
            color: var(--muted);
            font-size: 0.86rem;
        }

        .fm-preview-value {
            color: var(--ink);
            font-size: 1.28rem;
            font-weight: 850;
        }

        .fm-section {
            margin-top: 26px;
        }

        .fm-section-heading {
            color: var(--ink);
            font-size: 1.75rem;
            line-height: 1.2;
            font-weight: 850;
            margin: 0 0 10px;
        }

        .fm-section-copy {
            color: var(--muted);
            line-height: 1.7;
            max-width: 820px;
            margin-bottom: 16px;
        }

        .fm-card-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
        }

        .fm-value-card {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 24px;
            min-height: 178px;
            box-shadow: 0 8px 24px rgba(16, 24, 40, 0.04);
        }

        .fm-card-title {
            color: var(--ink);
            font-size: 1.15rem;
            font-weight: 850;
            margin-bottom: 10px;
        }

        .fm-card-copy {
            color: var(--muted);
            line-height: 1.65;
            font-size: 0.96rem;
        }

        .fm-problem {
            background: var(--ink);
            color: #ffffff;
            border-radius: 14px;
            padding: 34px;
            display: grid;
            grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
            gap: 28px;
            align-items: start;
        }

        .fm-problem .fm-section-heading,
        .fm-problem strong {
            color: #ffffff;
        }

        .fm-problem .fm-section-copy,
        .fm-problem p {
            color: #d0d5dd;
        }

        .fm-flow-box {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 28px;
        }

        .fm-arch-flow {
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
            max-width: 560px;
            margin: 0 auto;
        }

        .fm-arch-step {
            border: 1px solid var(--line);
            border-radius: 10px;
            padding: 16px;
            background: var(--surface-soft);
            text-align: center;
            color: var(--ink);
            font-weight: 800;
            min-height: 86px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .fm-arch-arrow {
            color: var(--primary);
            font-weight: 850;
            text-align: center;
            font-size: 1.1rem;
            line-height: 1;
        }

        .fm-cta-band {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 28px;
            display: grid;
            grid-template-columns: minmax(0, 1fr) 260px;
            gap: 18px;
            align-items: center;
        }

        .fm-dashboard-shell {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 28px;
            margin-bottom: 18px;
            box-shadow: 0 12px 36px rgba(16, 24, 40, 0.05);
        }

        .fm-dashboard-title {
            color: var(--ink);
            font-size: 2.1rem;
            line-height: 1.1;
            font-weight: 850;
            margin: 0 0 10px;
        }

        .fm-dashboard-copy {
            color: var(--muted);
            max-width: 820px;
            line-height: 1.65;
            margin: 0;
        }

        .fm-control-panel {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 18px;
        }

        .fm-label {
            color: var(--muted);
            font-size: 0.78rem;
            font-weight: 850;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        .fm-title {
            color: var(--ink);
            font-size: 1.2rem;
            font-weight: 850;
            margin-bottom: 10px;
        }

        .fm-note {
            color: var(--muted);
            font-size: 0.94rem;
            line-height: 1.6;
        }

        .fm-status-line {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
        }

        .fm-pill {
            border-radius: 999px;
            border: 1px solid var(--line);
            background: var(--surface-soft);
            color: var(--ink);
            padding: 8px 11px;
            font-size: 0.84rem;
        }

        .fm-pill strong {
            color: var(--primary);
        }

        .fm-executive-grid,
        .fm-metric-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }

        .fm-exec-card,
        .fm-metric-card {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 22px;
            min-height: 130px;
        }

        .fm-exec-label,
        .fm-metric-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 750;
            margin-bottom: 10px;
        }

        .fm-exec-value,
        .fm-metric-value {
            color: var(--ink);
            font-size: 2.35rem;
            font-weight: 850;
            line-height: 1;
        }

        .fm-exec-hint,
        .fm-metric-hint {
            color: var(--muted);
            font-size: 0.84rem;
            margin-top: 10px;
            line-height: 1.45;
        }

        .fm-table {
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 12px;
            overflow: hidden;
            font-size: 0.94rem;
        }

        .fm-table th {
            background: #f8fafc;
            color: var(--muted);
            font-weight: 800;
            text-align: left;
            padding: 13px 14px;
            border-bottom: 1px solid var(--line);
        }

        .fm-table td {
            color: var(--ink);
            padding: 13px 14px;
            border-bottom: 1px solid #edf1f5;
            vertical-align: top;
        }

        .fm-table tr:last-child td {
            border-bottom: none;
        }

        .fm-explain-card {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
        }

        .fm-explain-title {
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 850;
            margin-bottom: 8px;
        }

        .fm-explain-copy {
            color: var(--muted);
            line-height: 1.65;
        }

        .fm-compare-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
        }

        .fm-compare-card {
            background: #ffffff;
            border: 1px solid var(--line);
            border-radius: 12px;
            padding: 20px;
            min-height: 190px;
        }

        .fm-compare-title {
            color: var(--ink);
            font-weight: 850;
            font-size: 1.12rem;
            margin-bottom: 12px;
        }

        .fm-compare-line {
            display: flex;
            justify-content: space-between;
            gap: 14px;
            border-top: 1px solid #edf1f5;
            padding: 10px 0;
            color: var(--muted);
        }

        .fm-compare-line strong {
            color: var(--ink);
        }

        @media (max-width: 980px) {
            .fm-hero,
            .fm-problem,
            .fm-cta-band {
                grid-template-columns: 1fr;
            }

            .fm-card-grid,
            .fm-arch-flow,
            .fm-executive-grid,
            .fm-metric-grid,
            .fm-compare-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            .fm-hero-title {
                font-size: 3rem;
            }
        }

        @media (max-width: 640px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .fm-hero {
                padding: 28px;
            }

            .fm-hero-title {
                font-size: 2.45rem;
            }

            .fm-card-grid,
            .fm-arch-flow,
            .fm-executive-grid,
            .fm-metric-grid,
            .fm-compare-grid {
                grid-template-columns: 1fr;
            }

            .fm-nav {
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
        <div class="fm-nav">
            <div class="fm-brand">
                <div class="fm-logo">FM</div>
                <div>FairMatch AI</div>
            </div>
            <div class="fm-small">CSIT-26-S3-06</div>
        </div>

        <section class="fm-hero">
            <div>
                <div class="fm-kicker">Explainable Fairness-Aware Allocation Engine</div>
                <h1 class="fm-hero-title">FairMatch AI</h1>
                <div class="fm-hero-subtitle">Explainable Fairness-Aware Allocation Engine</div>
                <div class="fm-hero-copy">
                    Make allocation decisions transparent,<br>
                    fair and explainable.
                </div>
                <div class="fm-note">
                    FairMatch AI helps universities move from manual assignment lists to
                    evidence-backed allocation decisions with optimisation, fairness evaluation,
                    structured explanations, and counterfactual comparison.
                </div>
            </div>
            <div class="fm-preview">
                <div class="fm-label">Decision preview</div>
                <div class="fm-preview-row">
                    <div>
                        <div class="fm-preview-label">Allocation quality</div>
                        <div class="fm-preview-value">Valid</div>
                    </div>
                    <div class="fm-pill"><strong>Checked</strong></div>
                </div>
                <div class="fm-preview-row">
                    <div>
                        <div class="fm-preview-label">Fairness signal</div>
                        <div class="fm-preview-value">Measured</div>
                    </div>
                    <div class="fm-pill"><strong>Gini</strong></div>
                </div>
                <div class="fm-preview-row">
                    <div>
                        <div class="fm-preview-label">Decision logic</div>
                        <div class="fm-preview-value">Explainable</div>
                    </div>
                    <div class="fm-pill"><strong>Structured</strong></div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    cta_column, spacer_column = st.columns([0.28, 0.72])
    with cta_column:
        if st.button("Start Experience", type="primary", use_container_width=True):
            st.session_state.dashboard_started = True
            st.session_state.comparison_fairness_weight = DEFAULT_FAIRNESS_WEIGHT
            st.rerun()
    with spacer_column:
        st.markdown(
            '<div class="fm-note">Open the decision support workspace when you are ready to run an allocation scenario.</div>',
            unsafe_allow_html=True,
        )

    render_product_value_section()
    render_problem_section()
    render_architecture_section()
    render_landing_cta()


def render_product_value_section() -> None:
    st.markdown(
        """
        <section class="fm-section">
            <h2 class="fm-section-heading">Built for fairer allocation decisions</h2>
            <div class="fm-section-copy">
                FairMatch AI is designed around the questions coordinators need to answer:
                who was assigned, whether the outcome is balanced, and how the decision can be explained.
            </div>
            <div class="fm-card-grid">
                <div class="fm-value-card">
                    <div class="fm-card-title">Fair Allocation</div>
                    <div class="fm-card-copy">Balance preferences, skills, capacity and workload.</div>
                </div>
                <div class="fm-value-card">
                    <div class="fm-card-title">Transparent Decisions</div>
                    <div class="fm-card-copy">Every allocation includes explanation details.</div>
                </div>
                <div class="fm-value-card">
                    <div class="fm-card-title">Counterfactual Analysis</div>
                    <div class="fm-card-copy">Understand how fairness changes outcomes.</div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_problem_section() -> None:
    st.markdown(
        """
        <section class="fm-section fm-problem">
            <div>
                <div class="fm-label">Problem</div>
                <h2 class="fm-section-heading">Allocation is easy to list, hard to justify.</h2>
            </div>
            <div>
                <p>
                    Universities struggle to allocate students fairly when projects are
                    oversubscribed and resources are limited.
                </p>
                <p>
                    FairMatch AI provides optimisation, fairness evaluation and decision
                    transparency so coordinators can review allocation quality instead of only
                    accepting a final assignment list.
                </p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_architecture_section() -> None:
    st.markdown(
        """
        <section class="fm-section fm-flow-box">
            <div class="fm-label">Architecture</div>
            <h2 class="fm-section-heading">From input data to explainable decisions</h2>
            <div class="fm-arch-flow">
                <div class="fm-arch-step">Input</div>
                <div class="fm-arch-arrow">&darr;</div>
                <div class="fm-arch-step">Constraint Solver</div>
                <div class="fm-arch-arrow">&darr;</div>
                <div class="fm-arch-step">Fairness Evaluation</div>
                <div class="fm-arch-arrow">&darr;</div>
                <div class="fm-arch-step">Explanation Engine</div>
                <div class="fm-arch-arrow">&darr;</div>
                <div class="fm-arch-step">Decision Support Dashboard</div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_landing_cta() -> None:
    st.markdown(
        """
        <section class="fm-section fm-cta-band">
            <div>
                <div class="fm-label">Start experience</div>
                <h2 class="fm-section-heading">Review allocation as a decision, not a spreadsheet.</h2>
                <div class="fm-section-copy">
                    Enter the product workspace to run allocation, inspect fairness,
                    read explanations, and compare fairness-aware outcomes.
                </div>
            </div>
            <div></div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    cta_column, _ = st.columns([0.24, 0.76])
    with cta_column:
        if st.button("Launch Dashboard", type="primary", use_container_width=True):
            st.session_state.dashboard_started = True
            st.session_state.comparison_fairness_weight = DEFAULT_FAIRNESS_WEIGHT
            st.rerun()


def render_dashboard() -> None:
    render_dashboard_header()
    render_scenario_controls()

    tabs = st.tabs(["Overview", "Allocation", "Fairness", "Explanations", "Comparison"])
    with tabs[0]:
        render_overview()
    with tabs[1]:
        render_allocation()
    with tabs[2]:
        render_fairness()
    with tabs[3]:
        render_explanations()
    with tabs[4]:
        render_comparison()


def render_dashboard_header() -> None:
    st.markdown(
        """
        <div class="fm-nav">
            <div class="fm-brand">
                <div class="fm-logo">FM</div>
                <div>FairMatch AI</div>
            </div>
            <div class="fm-small">Decision Support Workspace</div>
        </div>
        <section class="fm-dashboard-shell">
            <div class="fm-label">Product workspace</div>
            <h1 class="fm-dashboard-title">Allocation decisions, explained.</h1>
            <p class="fm-dashboard-copy">
                Run a school allocation scenario, inspect the result, measure fairness,
                read decision explanations, and compare what changes when fairness is prioritised.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_scenario_controls() -> None:
    with st.expander("Scenario setup", expanded=False):
        source_column, dataset_column, upload_column = st.columns([0.22, 0.34, 0.44])
        with source_column:
            source = st.radio("Input source", ["Sample dataset", "Upload JSON"], index=0)
        with dataset_column:
            selected_name = st.selectbox("Sample dataset", list(SAMPLE_DATASETS))
        with upload_column:
            uploaded_file = st.file_uploader("Custom allocation JSON", type=["json"])

        payload = resolve_payload(source, selected_name, uploaded_file)
        if payload is not None:
            st.session_state.active_payload = payload
            st.session_state.active_dataset_name = selected_name if source == "Sample dataset" else "Uploaded JSON"

        render_dataset_summary(st.session_state.active_payload, st.session_state.active_dataset_name)

        action_columns = st.columns([0.22, 0.26, 0.2, 0.32])
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
    st.markdown(
        f"""
        <div class="fm-status-line">
            <div class="fm-pill"><strong>Scenario</strong> {escape(dataset_name)}</div>
            <div class="fm-pill"><strong>Students</strong> {len(payload.get("people", []))}</div>
            <div class="fm-pill"><strong>Projects</strong> {len(payload.get("items", []))}</div>
            <div class="fm-pill"><strong>Fairness Weight</strong> {int(payload.get("fairness_weight", 0))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview() -> None:
    payload = st.session_state.active_payload
    result = st.session_state.allocation_result
    cards = [
        ("Students", len(payload.get("people", [])), "Included in current scenario"),
        ("Projects", len(payload.get("items", [])), "Available allocation options"),
        ("Assignments", len(result.assignments) if result else 0, "Generated by the solver"),
        ("Status", result.status.title() if result else "Ready", "Current allocation state"),
    ]
    render_exec_cards(cards)

    st.markdown(
        """
        <section class="fm-section fm-flow-box">
            <div class="fm-label">Executive summary</div>
            <h2 class="fm-section-heading">FairMatch AI reviews allocation quality from four angles.</h2>
            <div class="fm-section-copy">
                The workspace separates the decision into assignment outcome, fairness quality,
                explanation clarity, and counterfactual impact. This keeps the experience focused
                on decision support rather than data administration.
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_exec_cards(cards: list[tuple[str, Any, str]]) -> None:
    html = '<div class="fm-executive-grid">'
    for label, value, hint in cards:
        html += (
            '<div class="fm-exec-card">'
            f'<div class="fm-exec-label">{escape(str(label))}</div>'
            f'<div class="fm-exec-value">{escape(str(value))}</div>'
            f'<div class="fm-exec-hint">{escape(str(hint))}</div>'
            "</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_allocation() -> None:
    result = st.session_state.allocation_result
    if result is None:
        render_empty_state("Run Allocation from Scenario setup to view assigned projects.")
        return

    st.markdown(
        """
        <div class="fm-label">Allocation</div>
        <h2 class="fm-section-heading">Assigned projects</h2>
        <div class="fm-section-copy">
            Each student receives one project assignment. The table keeps the outcome readable:
            who was assigned, to which project, and how closely the assignment matched preference.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_html_table(allocation_rows(result))


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


def render_fairness() -> None:
    result = st.session_state.allocation_result
    if result is None:
        render_empty_state("Run Allocation to inspect fairness metrics.")
        return

    st.markdown(
        """
        <div class="fm-label">Fairness</div>
        <h2 class="fm-section-heading">Fairness is measured, not assumed.</h2>
        <div class="fm-section-copy">
            These metrics show whether preference satisfaction is balanced across students.
            Total satisfaction is useful, but fairness metrics reveal whether weaker outcomes
            are concentrated on a small group.
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_metric_cards(
        [
            ("Total Satisfaction", result.total_satisfaction, "Overall preference score"),
            ("Average Satisfaction", f"{result.average_satisfaction:.2f}", "Mean student outcome"),
            ("Fairness Gap", result.fairness_gap, "Difference between highest and lowest satisfaction"),
            ("Max-Min Value", result.max_min_value, "Worst individual satisfaction outcome"),
            ("Gini Coefficient", f"{result.gini_coefficient:.3f}", "Inequality across satisfaction distribution"),
            ("Workload Gap", result.workload_gap, "Spread in assigned workload"),
        ]
    )


def render_metric_cards(metrics: list[tuple[str, Any, str]]) -> None:
    html = '<div class="fm-metric-grid">'
    for label, value, hint in metrics:
        html += (
            '<div class="fm-metric-card">'
            f'<div class="fm-metric-label">{escape(str(label))}</div>'
            f'<div class="fm-metric-value">{escape(str(value))}</div>'
            f'<div class="fm-metric-hint">{escape(str(hint))}</div>'
            "</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_explanations() -> None:
    result = st.session_state.allocation_result
    if result is None:
        render_empty_state("Run Allocation to review structured explanation details.")
        return

    st.markdown(
        """
        <div class="fm-label">Explanations</div>
        <h2 class="fm-section-heading">Every allocation should be readable.</h2>
        <div class="fm-section-copy">
            Review one student at a time. Each card summarises the assignment and keeps
            first-choice, fairness, and workload notes separate.
        </div>
        """,
        unsafe_allow_html=True,
    )
    names = [f"{assignment.person_name} -> {assignment.item_name}" for assignment in result.assignments]
    selected = st.selectbox("Choose student", names)
    selected_index = names.index(selected)

    for index, assignment in enumerate(result.assignments):
        title = f"{assignment.person_name} -> {assignment.item_name}"
        expanded = index == selected_index
        with st.expander(title, expanded=expanded):
            explanation = assignment.explanation
            st.markdown(
                f"""
                <div class="fm-explain-card">
                    <div class="fm-explain-title">{escape(assignment.person_name)} assigned to {escape(assignment.item_name)}</div>
                    <div class="fm-explain-copy">{escape(explanation.summary)}</div>
                </div>
                <div class="fm-explain-card">
                    <div class="fm-explain-title">First-choice note</div>
                    <div class="fm-explain-copy">{escape(explanation.first_choice_note)}</div>
                </div>
                <div class="fm-explain-card">
                    <div class="fm-explain-title">Fairness note</div>
                    <div class="fm-explain-copy">{escape(explanation.fairness_note)}</div>
                </div>
                <div class="fm-explain-card">
                    <div class="fm-explain-title">Workload note</div>
                    <div class="fm-explain-copy">{escape(explanation.workload_note)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_comparison() -> None:
    comparison = st.session_state.comparison
    baseline_result = st.session_state.baseline_result
    fairness_result = st.session_state.fairness_result

    if comparison is None or baseline_result is None or fairness_result is None:
        render_empty_state("Run Fairness Comparison from Scenario setup to compare baseline and fairness-aware outcomes.")
        return

    if st.session_state.comparison_warning:
        st.warning(st.session_state.comparison_warning)

    st.markdown(
        """
        <div class="fm-label">Comparison</div>
        <h2 class="fm-section-heading">Before fairness, after fairness, and what changed.</h2>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="fm-compare-grid">
            <div class="fm-compare-card">
                <div class="fm-compare-title">Before Fairness</div>
                {comparison_line("Total satisfaction", comparison.baseline_total_satisfaction)}
                {comparison_line("Fairness gap", comparison.baseline_fairness_gap)}
                {comparison_line("Gini coefficient", f"{comparison.baseline_gini_coefficient:.3f}")}
            </div>
            <div class="fm-compare-card">
                <div class="fm-compare-title">After Fairness</div>
                {comparison_line("Total satisfaction", comparison.fairness_total_satisfaction)}
                {comparison_line("Fairness gap", comparison.fairness_fairness_gap)}
                {comparison_line("Gini coefficient", f"{comparison.fairness_gini_coefficient:.3f}")}
            </div>
            <div class="fm-compare-card">
                <div class="fm-compare-title">Why It Matters</div>
                <div class="fm-explain-copy">
                    Fairness-aware optimisation can reduce uneven satisfaction outcomes.
                    In this comparison, fairness improved: <strong>{escape("Yes" if comparison.fairness_improved else "No")}</strong>.
                    Changed assignments: <strong>{len(comparison.changed_assignments)}</strong>.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="fm-section"></div><h2 class="fm-section-heading">What Changed</h2>', unsafe_allow_html=True)
    changed_assignment_rows = [
        {
            "Student ID": person_id,
            "Before Fairness": baseline_item,
            "After Fairness": fairness_item,
        }
        for person_id, (baseline_item, fairness_item) in sorted(comparison.changed_assignments.items())
    ]
    if changed_assignment_rows:
        render_html_table(changed_assignment_rows)
    else:
        st.info("No assignment changes were detected.")


def comparison_line(label: str, value: Any) -> str:
    return (
        '<div class="fm-compare-line">'
        f'<span>{escape(str(label))}</span>'
        f'<strong>{escape(str(value))}</strong>'
        "</div>"
    )


def render_empty_state(message: str) -> None:
    st.markdown(
        f"""
        <section class="fm-flow-box">
            <div class="fm-label">Ready</div>
            <div class="fm-note">{escape(message)}</div>
        </section>
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
        f'<table class="fm-table"><thead><tr>{header_html}</tr></thead><tbody>{body_html}</tbody></table>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.fairmatch.counterfactual import compare_fairness_runs
from backend.fairmatch.models import load_allocation_input
from backend.fairmatch.solver import solve_allocation


app = FastAPI(
    title="FairMatch AI API",
    description="FastAPI wrapper for the existing FairMatch AI backend.",
    version="2.0.0-prototype",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEFAULT_COMPARISON_FAIRNESS_WEIGHT = 3
FAIRNESS_COMPARISON_WARNING = (
    "baseline and fairness run both use fairness_weight = 0. "
    "Counterfactual comparison may not be meaningful."
)

SAMPLES = [
    {
        "id": "school_sample",
        "name": "School Sample",
        "mode": "school",
        "path": "data/school_sample.json",
    },
    {
        "id": "fairness_weight_tradeoff",
        "name": "Fairness Weight Trade-Off",
        "mode": "school",
        "path": "data/school_cases/fairness_weight_tradeoff.json",
    },
]


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "FairMatch AI API",
    }


@app.get("/samples")
def samples() -> dict[str, list[dict[str, Any]]]:
    return {
        "samples": [
            {
                **sample,
                "payload": _read_sample_payload(sample["path"]),
            }
            for sample in SAMPLES
        ]
    }


@app.post("/allocate")
def allocate(payload: dict[str, Any]) -> dict[str, Any]:
    result = _solve_payload(payload)
    return _allocation_response(result)


@app.post("/compare-fairness")
def compare_fairness(
    payload: dict[str, Any],
    fairness_weight: int = DEFAULT_COMPARISON_FAIRNESS_WEIGHT,
) -> dict[str, Any]:
    baseline_payload = deepcopy(payload)
    fairness_payload = deepcopy(payload)
    baseline_payload["fairness_weight"] = 0
    fairness_payload["fairness_weight"] = fairness_weight

    baseline_result = _solve_payload(baseline_payload)
    fairness_result = _solve_payload(fairness_payload)
    comparison = compare_fairness_runs(baseline_result, fairness_result)

    return {
        "baseline_result": _allocation_response(baseline_result),
        "fairness_result": _allocation_response(fairness_result),
        "counterfactual_comparison": asdict(comparison),
        "warning": FAIRNESS_COMPARISON_WARNING if fairness_weight == 0 else None,
    }


def _solve_payload(payload: dict[str, Any]):
    try:
        return solve_allocation(load_allocation_input(payload))
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=f"Invalid allocation payload: {exc}") from exc


def _allocation_response(result) -> dict[str, Any]:
    return asdict(result)


def _read_sample_payload(path: str) -> dict[str, Any]:
    try:
        import json

        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=500, detail=f"Unable to load sample dataset: {exc}") from exc


def sample_path(sample_id: str) -> Path:
    for sample in SAMPLES:
        if sample["id"] == sample_id:
            return Path(sample["path"])
    raise ValueError(f"Unknown sample id: {sample_id}")

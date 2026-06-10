import json
from pathlib import Path

import pytest
from fastapi import HTTPException

from api.main import allocate, compare_fairness, health, samples


def load_sample(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_health_endpoint():
    assert health() == {
        "status": "ok",
        "service": "FairMatch AI API",
    }


def test_samples_endpoint_lists_available_datasets():
    response = samples()
    sample_ids = {sample["id"] for sample in response["samples"]}

    assert "school_sample" in sample_ids
    assert "fairness_weight_tradeoff" in sample_ids
    assert all("payload" in sample for sample in response["samples"])
    assert all(sample["payload"]["mode"] == "school" for sample in response["samples"])


def test_allocate_endpoint_returns_result_metrics_and_explanations():
    payload = load_sample("data/school_sample.json")

    response = allocate(payload)

    assert response["status"] in {"OPTIMAL", "FEASIBLE"}
    assert "objective_value" in response
    assert response["assignments"]
    assert "total_satisfaction" in response
    assert "average_satisfaction" in response
    assert "fairness_gap" in response
    assert "gini_coefficient" in response
    assert response["assignments"][0]["explanation"]["summary"]


def test_compare_fairness_endpoint_returns_counterfactual_data():
    payload = load_sample("data/school_cases/fairness_weight_tradeoff.json")

    response = compare_fairness(payload, fairness_weight=3)

    assert response["baseline_result"]["status"] in {"OPTIMAL", "FEASIBLE"}
    assert response["fairness_result"]["status"] in {"OPTIMAL", "FEASIBLE"}
    assert response["counterfactual_comparison"]["fairness_improved"] is True
    assert response["counterfactual_comparison"]["changed_assignments"]
    assert response["warning"] is None


def test_compare_fairness_endpoint_warns_when_weight_is_zero():
    payload = load_sample("data/school_cases/fairness_weight_tradeoff.json")

    response = compare_fairness(payload, fairness_weight=0)

    assert response["warning"]
    assert "Counterfactual comparison may not be meaningful" in response["warning"]


def test_allocate_endpoint_handles_invalid_payload_safely():
    with pytest.raises(HTTPException) as exc_info:
        allocate({"mode": "school"})

    assert exc_info.value.status_code == 400
    assert "Invalid allocation payload" in exc_info.value.detail

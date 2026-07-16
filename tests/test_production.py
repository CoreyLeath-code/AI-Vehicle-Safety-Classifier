import json

import pytest

from mcp_adapter import handle_mcp_request
from n8n_webhook import app
from predict import classify_driving_conditions, load_config


@pytest.mark.parametrize(
    ("scenario", "expected"),
    [
        (("clear", "high", "light", "alert"), (100, "low")),
        (("rain", "medium", "heavy", "distracted"), (25, "high")),
        (("fog", "low", "moderate", "drowsy"), (0, "high")),
        (("rain", "high", "light", "alert"), (80, "low")),
        (("clear", "medium", "heavy", "distracted"), (45, "medium")),
    ],
)
def test_safety_boundaries(scenario, expected):
    score, risk, explanation = classify_driving_conditions(*scenario)
    assert (score, risk) == expected
    assert explanation


@pytest.mark.parametrize("field", range(4))
def test_unknown_values_are_rejected(field):
    scenario = ["clear", "high", "light", "alert"]
    scenario[field] = "unknown"
    with pytest.raises(ValueError):
        classify_driving_conditions(*scenario)


def test_configuration_load_and_invalid_document(tmp_path):
    assert load_config()["model"]["num_classes"] == 2
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(str(invalid))


def test_adapter_contract():
    payload = {
        "weather": "clear",
        "visibility": "high",
        "traffic": "light",
        "driver_state": "alert",
    }
    assert handle_mcp_request("classify_conditions", payload)["safety_score"] == 100
    with pytest.raises(ValueError, match="unknown tool"):
        handle_mcp_request("delete_everything", payload)
    with pytest.raises(ValueError, match="missing required"):
        handle_mcp_request("classify_conditions", {})
    with pytest.raises(ValueError, match="unknown fields"):
        handle_mcp_request("classify_conditions", {**payload, "extra": True})


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_health_readiness_and_metrics(client):
    assert client.get("/health").status_code == 200
    assert client.get("/live").status_code == 200
    assert client.get("/ready").json == {"ready": True}
    assert b"vehicle_safety_http_requests_total" in client.get("/metrics").data


def test_api_success(client):
    response = client.post(
        "/n8n/classify",
        json={
            "tool": "classify_conditions",
            "input": {
                "weather": "rain",
                "visibility": "low",
                "traffic": "heavy",
                "driver_state": "drowsy",
            },
        },
    )
    assert response.status_code == 200
    assert response.json["risk_level"] == "high"


def test_api_negative_contracts(client):
    assert client.post("/n8n/classify", data="x").status_code == 415
    assert client.post(
        "/n8n/classify", data="null", content_type="application/json"
    ).status_code == 400
    assert client.post("/n8n/classify", json={"input": {}}).status_code == 422
    assert client.post(
        "/n8n/classify", json={"tool": "unknown", "input": {}}
    ).status_code == 422


def test_json_result_is_serializable():
    result = handle_mcp_request(
        "classify_conditions",
        {
            "weather": "snow",
            "visibility": "medium",
            "traffic": "moderate",
            "driver_state": "alert",
        },
    )
    json.dumps(result)

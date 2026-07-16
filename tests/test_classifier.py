import pytest

from mcp_adapter import handle_mcp_request


@pytest.mark.parametrize(
    ("payload", "risk"),
    [
        (
            {
                "weather": "rain",
                "visibility": "low",
                "traffic": "heavy",
                "driver_state": "drowsy",
            },
            "high",
        ),
        (
            {
                "weather": "clear",
                "visibility": "high",
                "traffic": "light",
                "driver_state": "alert",
            },
            "low",
        ),
    ],
)
def test_classification_regression(payload, risk):
    result = handle_mcp_request("classify_conditions", payload)
    assert result["risk_level"] == risk
    assert 0 <= result["safety_score"] <= 100


def test_invalid_tool_is_rejected():
    with pytest.raises(ValueError, match="unknown tool"):
        handle_mcp_request("invalid_tool", {})

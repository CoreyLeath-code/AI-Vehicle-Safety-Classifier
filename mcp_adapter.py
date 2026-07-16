"""Validated adapter between HTTP tool calls and domain scoring."""

from __future__ import annotations

from typing import Any

from predict import classify_driving_conditions

_REQUIRED_FIELDS = ("weather", "visibility", "traffic", "driver_state")


def classify_conditions(input_data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise ValueError("input must be a JSON object")
    missing = [field for field in _REQUIRED_FIELDS if field not in input_data]
    unknown = sorted(set(input_data) - set(_REQUIRED_FIELDS))
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")
    if unknown:
        raise ValueError(f"unknown fields: {', '.join(unknown)}")
    score, risk, explanation = classify_driving_conditions(
        input_data["weather"],
        input_data["visibility"],
        input_data["traffic"],
        input_data["driver_state"],
    )
    return {"safety_score": score, "risk_level": risk, "explanation": explanation}


def handle_mcp_request(tool_name: str, input_payload: dict[str, Any]) -> dict[str, Any]:
    if tool_name != "classify_conditions":
        raise ValueError(f"unknown tool: {tool_name}")
    return classify_conditions(input_payload)

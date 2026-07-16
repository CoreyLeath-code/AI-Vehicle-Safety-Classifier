"""Production HTTP entry point for deterministic vehicle-condition scoring."""

from __future__ import annotations

import logging
import os
import time

from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from mcp_adapter import handle_mcp_request

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

REQUESTS = Counter(
    "vehicle_safety_http_requests_total",
    "HTTP requests",
    ("method", "path", "status"),
)
LATENCY = Histogram(
    "vehicle_safety_http_request_duration_seconds",
    "HTTP request latency",
    ("method", "path"),
)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", "16384"))
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[os.getenv("RATE_LIMIT", "60 per minute")],
    storage_uri="memory://",
)


@app.before_request
def begin_request() -> None:
    request.environ["request_started"] = time.perf_counter()


@app.after_request
def record_metrics(response):
    route = request.url_rule.rule if request.url_rule else "unmatched"
    REQUESTS.labels(request.method, route, str(response.status_code)).inc()
    started = request.environ.get("request_started", time.perf_counter())
    LATENCY.labels(request.method, route).observe(time.perf_counter() - started)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Cache-Control"] = "no-store"
    return response


@app.get("/health")
@app.get("/live")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.get("/ready")
def readiness_check():
    return jsonify({"ready": True}), 200


@app.get("/metrics")
@limiter.exempt
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.post("/n8n/classify")
def classify_webhook():
    if not request.is_json:
        return jsonify({"error": "content type must be application/json"}), 415
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "request body must be a JSON object"}), 400
    try:
        result = handle_mcp_request(
            payload.get("tool", "classify_conditions"),
            payload.get("input", {}),
        )
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 422
    except Exception:
        logger.exception("classification failed")
        return jsonify({"error": "internal service error"}), 500
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )

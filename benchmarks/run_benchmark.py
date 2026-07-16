"""Seeded API benchmark producing versioned JSON evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import time
import tracemalloc
from datetime import UTC, datetime
from pathlib import Path

from n8n_webhook import app

SCHEMA_VERSION = "1.0.0"
PAYLOAD = {
    "tool": "classify_conditions",
    "input": {
        "weather": "rain",
        "visibility": "low",
        "traffic": "heavy",
        "driver_state": "drowsy",
    },
}


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * fraction))]


def run(iterations: int, warmup: int) -> dict:
    client = app.test_client()
    for _ in range(warmup):
        client.post("/n8n/classify", json=PAYLOAD)

    latencies = []
    tracemalloc.start()
    started_all = time.perf_counter()
    for _ in range(iterations):
        started = time.perf_counter_ns()
        response = client.post("/n8n/classify", json=PAYLOAD)
        if response.status_code != 200:
            raise RuntimeError(f"benchmark request failed: {response.status_code}")
        latencies.append((time.perf_counter_ns() - started) / 1_000_000)
    elapsed = time.perf_counter() - started_all
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "schema_version": SCHEMA_VERSION,
        "benchmark": "in_process_http_classification",
        "parameters": {"iterations": iterations, "warmup": warmup, "payload": PAYLOAD},
        "metrics": {
            "latency_average_ms": round(statistics.mean(latencies), 4),
            "latency_median_ms": round(statistics.median(latencies), 4),
            "latency_p95_ms": round(percentile(latencies, 0.95), 4),
            "latency_p99_ms": round(percentile(latencies, 0.99), 4),
            "latency_min_ms": round(min(latencies), 4),
            "latency_max_ms": round(max(latencies), 4),
            "throughput_requests_per_second": round(iterations / elapsed, 2),
            "success_rate": 1.0,
            "peak_python_memory_bytes": peak,
        },
        "provenance": {
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "payload_sha256": hashlib.sha256(
                json.dumps(PAYLOAD, sort_keys=True).encode(), usedforsecurity=False
            ).hexdigest(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=5000)
    parser.add_argument("--warmup", type=int, default=100)
    parser.add_argument("--output", type=Path, default=Path("benchmarks/latest.json"))
    args = parser.parse_args()
    if args.iterations < 1 or args.warmup < 0:
        parser.error("iterations must be positive and warmup non-negative")
    result = run(args.iterations, args.warmup)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

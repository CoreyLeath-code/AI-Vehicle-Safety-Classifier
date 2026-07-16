from benchmarks.run_benchmark import run


def test_benchmark_schema_and_success():
    result = run(iterations=5, warmup=1)
    assert result["schema_version"] == "1.0.0"
    assert result["metrics"]["success_rate"] == 1.0
    assert result["metrics"]["latency_p99_ms"] > 0
    assert len(result["provenance"]["payload_sha256"]) == 64

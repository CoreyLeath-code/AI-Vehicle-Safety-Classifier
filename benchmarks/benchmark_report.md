# Benchmark report

CI generates `latest.json` for every pull request. It is the canonical result because it binds
measurements to a commit and runner. The JSON contains average, median, p95, p99, min/max latency,
throughput, success rate, peak Python memory, payload hash, environment, and timestamp.

| Metric | Source |
|---|---|
| Latency distribution | `metrics.latency_*_ms` |
| Throughput | `metrics.throughput_requests_per_second` |
| Peak allocation | `metrics.peak_python_memory_bytes` |
| Reproducibility | `parameters` and `provenance` |

Do not copy hardware-dependent values into this report. Download the CI artifact and compare it
with a prior artifact only when schema, payload hash, parameters, Python, and platform are compatible.

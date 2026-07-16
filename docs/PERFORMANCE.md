# Performance and benchmark guide

Run `python benchmarks/run_benchmark.py`. CI records average, median, p95, p99, min/max latency,
requests/second, success rate, peak Python allocation, payload hash, platform, Python, and UTC time.

This in-process test isolates application overhead; it is not a network capacity promise. Compare
only compatible schema, payload, parameters, runtime, and hardware. Run k6 or Locust against
staging for 1/10/100/1,000/10,000-user scenarios with TLS and shared rate limiting. CNN accuracy,
training, GPU, and loss metrics remain unavailable until a versioned dataset and model exist.

# Benchmark Protocol — AI Vehicle Safety Classifier

The supported benchmark measures the deterministic HTTP classification path. It does not compare CNNs or baseline ML models because the repository does not currently contain the versioned dataset/model evidence needed to reproduce such a comparison.

## Reproduce

```bash
python -m pip install -r requirements-dev.txt
python benchmarks/run_benchmark.py \
  --iterations 1000 \
  --warmup 50 \
  --output benchmarks/latest.json
```

## Audited baseline

Commit: `49c6722be68bb7cc121e98f8304405d09c388530`

| Metric | Value |
|---|---:|
| Success rate | 100% |
| Median latency | 1.0764 ms |
| Average latency | 1.0951 ms |
| p95 latency | 1.1803 ms |
| p99 latency | 1.4806 ms |
| Throughput | 909.74 requests/s |
| Peak traced Python memory | 376,893 bytes |

The run used Python 3.11.16 on a GitHub-hosted Ubuntu 24.04 runner and 1,000 measured requests after 50 warm-up requests.

## Validity boundary

This is an in-process Flask test-client benchmark. It excludes network/TLS overhead, multi-process contention, external rate-limit storage, ingress/load balancers, and CNN inference. Treat changes across repeated CI artifacts as regression evidence; do not treat one run as a capacity guarantee.

## Future model benchmark requirements

Any CNN-vs-baseline comparison must include dataset hash/license, immutable split manifest, seeds, preprocessing, hyperparameters, model digests, class support, confidence intervals, and exact commands/commit provenance before numbers are published.

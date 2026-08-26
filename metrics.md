# AI Vehicle Safety Classifier — Evidence Register

This file distinguishes reproducible engineering measurements from model-quality evidence that is not yet available.

## Verified engineering evidence

Audited green `main` baseline: `49c6722be68bb7cc121e98f8304405d09c388530`.

| Metric | Audited value | Protocol |
|---|---:|---|
| Tests | 19 passed | `pytest` on Python 3.11.16 |
| Core branch coverage | 96.03% | `pytest-cov`; enforced gate >=90% |
| Benchmark requests | 1,000 measured + 50 warm-up | Flask in-process test client |
| Success rate | 100% | Non-200 responses fail benchmark |
| Median latency | 1.0764 ms | Fixed hashed request payload |
| Average latency | 1.0951 ms | Fixed hashed request payload |
| p95 latency | 1.1803 ms | Fixed hashed request payload |
| p99 latency | 1.4806 ms | Fixed hashed request payload |
| Throughput | 909.74 requests/s | Single-process in-process benchmark |
| Peak traced Python memory | 376,893 bytes | `tracemalloc` during measured loop |
| Runtime dependency audit | No known vulnerabilities found | `pip-audit -r requirements-runtime.txt` |

These results are hardware/runtime sensitive. They do not establish production concurrency, network latency, or CNN inference performance.

## CNN model-quality evidence

The repository does not currently contain a redistributable versioned labeled dataset and signed trained model artifact sufficient to reproduce model-quality numbers. Therefore the following are intentionally **not claimed**:

- accuracy;
- precision;
- recall;
- F1;
- ROC-AUC;
- confusion matrix;
- threshold/calibration quality;
- subgroup performance;
- ablation deltas;
- training loss or GPU throughput.

A future model evaluation must record dataset identity/license, split strategy, leakage checks, seeds, dependency versions, training config, model digest, class support, uncertainty, and the exact command/commit used to generate every number.

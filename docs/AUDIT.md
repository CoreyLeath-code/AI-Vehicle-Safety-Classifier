# L6 Engineering Audit

## Executive assessment

The repository has a solid deterministic service core, strong CI/security scaffolding, explicit Kubernetes hardening, and a reproducible performance harness. Its largest senior-level weakness was **evidence integrity**: several research documents presented CNN accuracy, F1, dataset statistics, and ablation results without a versioned dataset/model trail capable of regenerating those numbers.

This audit treats truthful system boundaries as a release requirement. The validated production path is the deterministic vehicle-condition risk API. The CNN path remains research-only until the missing evidence is supplied.

## L6 scorecard

| Area | Assessment | Evidence / gap |
|---|---|---|
| API correctness | Strong | Strict allow-list validation, negative contracts, deterministic outputs |
| Test discipline | Strong for serving core | 19 tests; 96.03% audited core branch coverage; >=90% CI gate |
| Observability | Good | Prometheus request counter and latency histogram; health/live/ready endpoints |
| Security | Good | Bandit, pip-audit, CodeQL, Trivy filesystem/image scans, SPDX SBOM |
| Container/Kubernetes | Good | UID 10001, read-only filesystem, dropped caps, seccomp, resource limits, probes, default-deny network policy |
| Performance evidence | Good within stated boundary | Versioned in-process benchmark with warm-up, latency distribution, throughput, memory, payload hash and runtime provenance |
| Release engineering | Improved in v1.1.0 | GitHub Release + GHCR package workflow, semantic and immutable SHA tags |
| Distributed-systems maturity | Partial | Process-local rate limiting; no shared Redis state, auth boundary, tracing, SLOs or real concurrent load/soak test |
| CNN evidence | Not release-qualified | No immutable dataset manifest or signed model artifact; model metrics intentionally withdrawn |
| Safety validation | Not established | No domain certification, ODD definition, hazard analysis, calibrated model evidence or field validation |

## Findings and treatment

### P0 — unsupported research claims

**Finding:** `metrics.md`, `Benchmark.md`, `ablation_study.md`, `dataset_stats.md`, and the previous model card contained exact CNN/dataset numbers that could not be reproduced from committed artifacts.

**Risk:** a senior reviewer cannot distinguish measured results from portfolio decoration; this undermines trust in every other claim.

**Treatment:** numeric model claims were removed and replaced with a reproducibility contract. The README now publishes only CI-derived engineering measurements and explicitly labels the CNN lane as research-only.

### P0 — serving/model boundary ambiguity

**Finding:** repository branding can imply that the deployed service performs computer-vision inference even though the validated HTTP path uses deterministic condition inputs.

**Risk:** misleading architecture and incorrect operational expectations.

**Treatment:** README architecture and system-design diagrams now separate the deterministic serving path from the optional offline CNN path.

### P1 — release/package gap

**Finding:** no GitHub Release or GitHub Package existed despite mature CI/container assets.

**Treatment:** `release.yml` publishes `v1.1.0` plus `ghcr.io/coreyleath-code/ai-vehicle-safety-classifier:v1.1.0` and an immutable commit-SHA image tag. Existing releases are never mutated.

### P1 — distributed runtime limitations

**Finding:** Flask-Limiter uses process-local in-memory storage.

**Risk:** limits are inconsistent across replicas and reset on process restart.

**Next treatment:** shared Redis-backed limits, gateway identity/authentication, correlation IDs, OpenTelemetry traces, explicit SLOs, concurrent load tests, and rollout/rollback drills.

### P1 — benchmark external validity

**Finding:** the benchmark uses Flask's in-process test client.

**Risk:** excellent microbenchmark values may be mistaken for production network capacity.

**Treatment:** README and benchmark documentation explicitly state the protocol boundary. A future container-level benchmark should include controlled CPU/memory, concurrency, repeated trials, confidence intervals, TLS/network path, and regression thresholds.

### P2 — CNN promotion gates

Before image inference is considered release-qualified, require:

- immutable licensed dataset manifest and hashes;
- deterministic grouped splits and leakage checks;
- fixed seeds/dependency lock/training config;
- trained model digest/signature;
- precision, recall, F1, confusion matrix, class support, calibration and relevant subgroup slices;
- uncertainty/fail-closed behavior;
- deployment-target latency and memory evidence;
- drift, rollback and monitoring plan;
- intended-use/excluded-use and domain safety review.

## Audited baseline hard evidence

Green `main` baseline: `49c6722be68bb7cc121e98f8304405d09c388530`, GitHub-hosted Ubuntu 24.04, Python 3.11.16.

- 19/19 tests passed in 0.63 seconds.
- Core branch coverage: 96.03%.
- `pip-audit`: no known runtime dependency vulnerabilities.
- In-process benchmark: 1,000 measured requests after 50 warm-ups, 100% success, median 1.0764 ms, p95 1.1803 ms, p99 1.4806 ms, 909.74 requests/s, 376,893 bytes peak traced Python memory.
- Deployment validation builds the image, checks UID 10001, starts it under 512 MiB / 1 CPU constraints, exercises health/readiness/classification, and validates Kubernetes manifests.

These values are evidence for that commit and environment, not permanent guarantees.

## Merge/release gate

The v1.1.0 PR must not merge until all available PR checks are green. Any failing unit, API, benchmark, security, container, or manifest check must be patched on the branch first. After merge, the release workflow is expected to publish both the GitHub Release and GHCR package from the merged commit.

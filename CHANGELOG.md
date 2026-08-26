# Changelog

## [Unreleased]

## [2026-08-26] v1.1.0

### Added
- L6-style architecture and system-design documentation.
- Reproducibility/hard-evidence dashboard tied to CI artifacts.
- Research benchmark protocol with explicit threats-to-validity boundaries.
- Engineering Q&A and prioritized roadmap.
- GitHub Release + GHCR container package workflow with semantic and immutable commit-SHA tags.

### Changed
- Reframed the validated serving path as a deterministic vehicle-condition risk API.
- Clarified that CNN image inference is an offline research path until dataset/model evidence is versioned.
- Replaced unsupported CNN accuracy/F1/ROC-AUC, dataset statistics, and ablation numbers with reproducibility requirements.
- Expanded the engineering audit around evidence integrity, distributed-runtime gaps, release gates, and model-promotion criteria.

### Verified baseline before this release PR
- `main` commit `49c6722be68bb7cc121e98f8304405d09c388530`: 19/19 tests passed, 96.03% core branch coverage, no known runtime dependency vulnerabilities from `pip-audit`.
- CI benchmark: 1,000 measured requests after 50 warm-ups, 100% success, 1.0764 ms median, 1.1803 ms p95, 1.4806 ms p99, 909.74 requests/s, 376,893 bytes peak traced Python memory.

## [2025-06-12] v1.0.1
- Fixed memory leak in C++ classifier (historical changelog entry; not independently re-verified by this audit).
- Improved input validation in `predict.py`.

## [2025-05-30] v1.0.0
- Initial project release (historical changelog entry).

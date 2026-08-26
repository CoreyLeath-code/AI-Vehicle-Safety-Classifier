# Model Card — CNN Research Path

## Status

**Research-only / not release-qualified.** The repository contains CNN training and inference code, but no versioned redistributable labeled dataset and signed trained model artifact are present. The deterministic HTTP service is the currently validated serving path.

## Intended research use

The CNN code is intended to explore binary image classification for vehicle/driving-safety research. It must not be represented as a certified driver-assistance, insurance, legal, emergency-intervention, or autonomous-driving system without a separate domain validation program.

## Architecture in code

The repository contains TensorFlow-oriented image preprocessing/model-loading hooks and an offline training/evaluation path under `src/`. Image inference is loaded lazily and is not required by the deterministic service runtime.

## Dataset

No immutable dataset manifest is currently available in the repository. Class counts, split ratios, environment distribution, and dataset-derived claims are therefore intentionally unspecified. See `dataset_stats.md` for the evidence required before publication.

## Model-quality metrics

**Unavailable.** Accuracy, precision, recall, F1, ROC-AUC, confusion matrix, calibration, subgroup slices, and ablation deltas are not published as verified results because the repository cannot currently regenerate them end to end.

## Risks and limitations

- Unknown behavior outside any future documented training distribution.
- Safety-domain false negatives and false positives may have asymmetric costs.
- Single-frame classification cannot capture temporal driving context by itself.
- Camera, lighting, weather, geography, vehicle interior/exterior, and collection-source shifts may materially change performance.
- Confidence scores must not be treated as calibrated probabilities without calibration evidence.
- A model artifact must not be promoted into the service solely because aggregate accuracy looks acceptable.

## Promotion criteria

Before serving CNN predictions, require:

1. dataset identity, license, hashes, and immutable split manifest;
2. duplicate/leakage checks;
3. fixed seeds and dependency lock;
4. reproducible training configuration and command;
5. model artifact digest/signature;
6. class support, confusion matrix, precision, recall, F1, calibration and relevant subgroup slices;
7. uncertainty/fail-closed policy;
8. latency and memory measurements on the actual deployment target;
9. drift/rollback plan;
10. review of intended use and excluded use by the appropriate domain stakeholders.

## Engineering evidence

The deterministic API path has reproducible CI, coverage, security, container, Kubernetes, and benchmark evidence documented in `README.md` and `metrics.md`. Those engineering measurements do not substitute for CNN model validation.

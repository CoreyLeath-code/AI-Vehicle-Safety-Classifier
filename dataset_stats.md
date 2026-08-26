# Dataset Evidence Status — AI Vehicle Safety Classifier

The repository currently does **not** include a versioned redistributable labeled image dataset or immutable dataset manifest sufficient to verify class counts, environmental distributions, correlations, or train/validation/test proportions.

Accordingly, previous numeric dataset statistics have been removed from the evidence surface.

## Required dataset manifest

Before model-quality claims are published, add a machine-readable manifest containing:

- dataset name, source, version, and license;
- file/content hashes;
- class definitions and per-class support;
- capture/source provenance that can be legally documented;
- image dimensions and preprocessing policy;
- train/validation/test membership for every example;
- split-generation seed and grouping strategy;
- duplicate and near-duplicate leakage checks;
- known missingness, imbalance, and sampling limitations;
- subgroup/environment slices relevant to lighting, weather, camera/source, and other intended-domain factors.

Model metrics in `metrics.md` and `model_card.md` remain unavailable until this evidence exists.

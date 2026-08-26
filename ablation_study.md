# CNN Ablation Study — Reproducibility Contract

No CNN ablation result is currently considered verified in this repository because there is no immutable labeled dataset manifest and versioned trained-artifact set from which to regenerate the reported variants.

## Planned variants

A future controlled study may compare:

- full configured CNN;
- no dropout;
- no batch normalization;
- reduced-depth CNN;
- optimizer substitution.

## Required protocol

Every row in a future ablation table must record:

1. dataset hash and license;
2. identical train/validation/test split manifest;
3. preprocessing and augmentation configuration;
4. fixed seeds and dependency versions;
5. one changed factor per variant;
6. training command and Git commit;
7. model artifact digest;
8. class support and confusion matrix;
9. precision, recall, F1 and calibration where appropriate;
10. repeated runs or confidence intervals when stochastic variation is material.

Until those artifacts exist, numeric ablation deltas are intentionally omitted.

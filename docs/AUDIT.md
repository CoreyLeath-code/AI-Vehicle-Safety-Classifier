# Production readiness audit

## Executive summary

The repository has an interpretable deterministic safety-scoring core and a documented CNN
research direction. Before this change, public model claims were not backed by versioned data,
model artifacts, or executable provenance. CI did not install the documented stack, unknown inputs
received plausible scores, exceptions leaked to clients, and the container ran as root.

## Findings and treatment

| Priority | Finding | Risk | Treatment |
|---|---|---|---|
| P0 | Unverified CNN metrics presented as facts | Misleading evaluation | README now distinguishes reproducible evidence from unavailable model evidence |
| P0 | Unknown inputs received fallback scores | Unsafe false confidence | Strict allow-list validation and negative tests |
| P0 | Root, oversized container | Runtime/supply-chain exposure | Minimal runtime lock, UID 10001, read-only deployment |
| P1 | Non-representative CI | False green builds | Pinned inputs and enforcing 90% core coverage |
| P1 | Raw exception responses | Information disclosure | Sanitized 500 and explicit 4xx contracts |
| P1 | No benchmark provenance | Non-repeatable performance claims | Versioned JSON benchmark and artifact |

## Strengths

Deterministic logic is explainable and inexpensive, CNN dependencies load lazily, configuration is
externalized, and the project is MIT licensed.

## Residual risk

No redistributable labeled dataset or signed CNN artifact is present; accuracy, precision, recall,
F1, ROC-AUC, confusion matrix, training/GPU metrics, and loss curves cannot be regenerated. The
in-memory limiter is process-local; multi-replica internet deployment needs a shared Redis backend
and gateway authentication. This is not a certified automotive safety component.

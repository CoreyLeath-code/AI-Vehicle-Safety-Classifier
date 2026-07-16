# Architecture

```mermaid
flowchart LR
  C[Client or n8n] --> G[Gateway TLS and identity]
  G --> A[Flask scoring API]
  A --> V[Schema and enum validation]
  V --> R[Deterministic risk engine]
  R --> O[JSON result]
  A --> P[Prometheus metrics]
  D[Versioned image dataset] --> T[Offline CNN training]
  T --> E[Evaluation and model card]
  E --> S[Signed model artifact]
  S -. optional inference .-> A
```

The reproducible deterministic engine is the serving boundary. CNN work stays offline until its
dataset and artifact are available, preventing startup dependency on TensorFlow and reducing the
production image's size and attack surface.

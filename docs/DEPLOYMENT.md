# Deployment guide

Build and smoke test:

```bash
docker build -t ai-vehicle-safety-classifier:local .
docker run --rm --read-only --tmpfs /tmp --cap-drop ALL \
  --security-opt no-new-privileges -p 127.0.0.1:5000:5000 \
  ai-vehicle-safety-classifier:local
curl --fail http://127.0.0.1:5000/health
```

Promotion requires green CI/security checks, SPDX SBOM retention, an immutable signed digest,
staging probes/API validation, resource review, monitoring, and a rollback owner. Apply the network
policy, deployment, and service after replacing the example tag with the release digest. Roll back
with `kubectl rollout undo deployment/vehicle-safety-classifier` and verify health, errors, p95
latency, and success rate. The current stateless service requires no database or secrets.

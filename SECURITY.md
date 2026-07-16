# Security policy

Report vulnerabilities through GitHub private vulnerability reporting; do not open a public issue.
Include the affected commit, reproduction, impact, and minimal proof of concept. Maintainers target
acknowledgement within five business days.

The default branch and latest release receive security fixes. CI runs CodeQL, Bandit, dependency,
secret, misconfiguration, repository, and image scans and produces an SPDX SBOM. The service
validates input, rate-limits requests, sanitizes failures, and runs non-root with least privilege.

This classifier is not a certified safety control. Internet deployments require TLS and
authentication at a managed gateway plus a shared rate-limit backend.

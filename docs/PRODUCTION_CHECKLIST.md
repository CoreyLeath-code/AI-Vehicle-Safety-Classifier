# Production checklist

- [ ] Format, lint, static analysis, tests, and >=90% core coverage pass
- [ ] Compatible benchmark shows no unexplained regression
- [ ] CodeQL, dependency, secret, license, source, and image scans pass
- [ ] SPDX SBOM retained; immutable image signature verified
- [ ] UID 10001, read-only filesystem, dropped capabilities, and limits confirmed
- [ ] Startup/liveness/readiness, metrics, API, environment, and model checks pass
- [ ] Logs contain no secrets or raw exceptions; alerts have owners
- [ ] Database connectivity recorded as not applicable
- [ ] Prior digest, rollback command, owner, and incident channel recorded

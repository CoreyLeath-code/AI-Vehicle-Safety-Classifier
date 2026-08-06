# n8n automation

## Scope and audit

This repository exposes a Flask endpoint at `/n8n/classify` for deterministic vehicle-condition scoring and already includes an n8n workflow definition. The original definition targeted `http://localhost:5000` and included placeholder Slack and Google Sheets destinations; neither is portable to a self-hosted n8n deployment or verifiable from the repository.

This change keeps the classification route, removes unconfigured outbound destinations, and makes the definition inactive until a service deployment is explicitly configured. It does not claim vehicle-safety certification, deploy n8n, or create any webhook URL.

## Required configuration

Use a self-hosted n8n deployment. Configure these variables in the n8n environment, not in repository files:

| Variable | Required | Purpose |
| --- | --- | --- |
| `N8N_BASE_URL` | Yes | Base URL of the self-hosted n8n instance. n8n uses this to construct webhook URLs; the workflow JSON does not hard-code one. |
| `VEHICLE_SAFETY_API_BASE_URL` | Yes for the classifier workflow | Base URL of the deployed Flask classifier service. The workflow appends `/n8n/classify`; it has no fallback localhost URL. |
| `GITHUB_OWNER` | Yes for label bootstrap | Set to `CoreyLeath-code`. |
| `GITHUB_TOKEN` | Optional | Fallback for GitHub API access only; store it in the environment or n8n credential store, never in workflow JSON. |

The label bootstrap also requires one organization-wide GitHub OAuth credential in the n8n credential store with permission to read/create repository labels. No credentials are committed.

## Workflow definitions

### Vehicle safety classifier

- **Definition:** `vehicle_safety_workflow.json`
- **Trigger:** An n8n webhook, path `vehicle-safety`, after the administrator activates the imported workflow.
- **Actions:** Relays weather, visibility, traffic, and driver-state input to the configured classifier endpoint, then returns that service’s response to the webhook caller.
- **Does not do:** Send Slack alerts, write Google Sheets records, assume a local service, or activate itself.
- **Manual execution:** Deploy the Flask service, set `VEHICLE_SAFETY_API_BASE_URL`, import the JSON, bind any organization controls required by the n8n installation, then activate and test it with a non-sensitive payload.
- **Failure recovery:** Disable the workflow if the target service is unavailable or responds incorrectly. Inspect the n8n execution and service logs, correct configuration, then retest before reactivation.

### Label bootstrap

- **Definition:** `n8n/label-bootstrap.json`
- **Trigger:** Manual execution only.
- **Actions:** Reads existing labels and creates only missing labels from the requested organization set. Existing labels are not edited, including their colors.
- **Manual execution:** Import it, bind the GitHub OAuth credential, confirm `GITHUB_OWNER`, and run once.
- **Failure recovery:** Correct credential permissions and rerun. It is idempotent because only labels absent from the prior GET response are posted.

## Deliberately skipped automation

- **Slack alerts and Google Sheets logging:** no Slack channel, Google Sheet, data-retention policy, or credential is configured in the repository. Adding them would invent infrastructure and potentially export safety-related data.
- **GitHub PR/issue automation:** the repository already has open CI/security automation work, while no review/comment policy is established here. This PR avoids duplicate automation.
- **Benchmark/security/release automation:** existing GitHub Actions already provide these responsibilities.
- **Model-training or safety-decision automation:** the CNN path lacks a versioned labeled dataset and signed model artifact, and the README explicitly identifies model-quality evaluation as unavailable.

## Validation

The workflow JSON is parsed from the committed branch, checked to be inactive, and scanned for token-shaped values before the pull request is opened. Runtime validation is not performed here because no self-hosted n8n host, service deployment, or credential binding is available.
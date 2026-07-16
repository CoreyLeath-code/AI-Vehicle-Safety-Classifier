# Contributing

Create a focused branch and pull request. Install `requirements-dev.txt`, then run:

```bash
ruff check predict.py mcp_adapter.py n8n_webhook.py benchmarks tests
bandit -q -r predict.py mcp_adapter.py n8n_webhook.py
pip-audit -r requirements-runtime.txt
pytest
python benchmarks/run_benchmark.py
```

Document behavior changes and add positive, negative, edge-case, and regression tests. Never update
benchmark or model claims without the generating command, data/artifact version, seed, and complete
environment provenance.

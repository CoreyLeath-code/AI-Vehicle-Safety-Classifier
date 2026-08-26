FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Keep the runtime OS patched instead of accepting vulnerable packages from a
# moving base tag. Trivy blocks HIGH/CRITICAL findings in CI.
RUN apt-get update \
    && apt-get install --only-upgrade -y --no-install-recommends \
       openssl libssl3t64 openssl-provider-legacy \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-runtime.txt .
RUN python -m pip install --upgrade \
      "pip>=26.1,<27" "setuptools>=80.9,<81" "wheel>=0.46.2,<0.47" \
      "jaraco.context>=6.1,<7" \
    && python -m pip install -r requirements-runtime.txt \
    # pip/setuptools/wheel are build/install tooling, not application runtime
    # dependencies. Removing them also removes their vendored packages and
    # reduces the final attack surface scanned by Trivy.
    && python -m pip uninstall -y pip setuptools wheel jaraco.context \
    && groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app

COPY --chown=10001:10001 mcp_adapter.py predict.py n8n_webhook.py ./
USER 10001:10001
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)"]
CMD ["gunicorn", "--bind=0.0.0.0:5000", "--workers=2", "--threads=4", "--timeout=30", "n8n_webhook:app"]

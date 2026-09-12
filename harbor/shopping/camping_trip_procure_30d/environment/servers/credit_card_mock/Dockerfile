FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --timeout 120 --retries 10 "mcp==1.25.0"
RUN pip install --no-cache-dir --timeout 120 --retries 10 "hatchling==1.27.0"

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir --no-deps --no-build-isolation .

# Mount host's envs/<server>/<env_name>/ at /env-seed (read-only).
# Entrypoint copies the seed into /env (container-internal, writable),
# then the server creates runtime.db and applies init.sql inside /env.
# host envs/ is never written to.
EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "mkdir -p /env && cp -r /env-seed/. /env/ && exec credit-card-mock --host 0.0.0.0 --port 8000 --env /env"]

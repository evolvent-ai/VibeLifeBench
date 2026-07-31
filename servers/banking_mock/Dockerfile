FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

# Mount host's envs/<server>/<env_name>/ at /env-seed (read-only).
# Entrypoint copies the seed into /env (container-internal, writable),
# then the server creates runtime.db and applies init.sql inside /env.
# host envs/ is never written to.
EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "mkdir -p /env && cp -r /env-seed/. /env/ && exec banking-mock --host 0.0.0.0 --port 8000 --env /env"]

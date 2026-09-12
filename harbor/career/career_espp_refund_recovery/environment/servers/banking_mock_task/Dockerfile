FROM python:3.12-slim

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ENV HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} NO_PROXY=${NO_PROXY}

WORKDIR /app

COPY wheels /wheels
COPY servers/banking_mock_task/src ./src
ENV PYTHONPATH=/app/src
RUN pip install --no-cache-dir --no-index --find-links=/wheels "mcp==1.25.0" "typing-extensions>=4.9.0"

# Mount host's envs/<server>/<env_name>/ at /env-seed (read-only).
# Entrypoint copies the seed into /env (container-internal, writable),
# then the server creates runtime.db and applies init.sql inside /env.
# host envs/ is never written to.
EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "mkdir -p /env && cp -r /env-seed/. /env/ && exec python -m banking_mock.server --host 0.0.0.0 --port 8000 --env /env"]

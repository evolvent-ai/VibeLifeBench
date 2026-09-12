ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}
# Harbor's nested Docker daemon may require its proxy for package bootstrap.
# These are optional build arguments and remain empty in normal deployments.
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ENV HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} NO_PROXY=${NO_PROXY}
RUN apt-get update && apt-get install -y --no-install-recommends bash ca-certificates curl jq procps sqlite3 && rm -rf /var/lib/apt/lists/*
COPY wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels "mcp==1.25.0" "PyYAML==6.0.3"
COPY evidence-collector /opt/evidence-collector
RUN chmod +x /opt/evidence-collector/collect
WORKDIR /workspace
USER root

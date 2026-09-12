ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}
RUN apt-get update && apt-get install -y --no-install-recommends bash ca-certificates coreutils curl jq procps sqlite3 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "mcp==1.25.0" "PyYAML==6.0.3"
RUN mkdir -p /etc/codex && printf 'model = "sub2api-gpt-5.6-sol"\nmodel_reasoning_effort = "xhigh"\nweb_search = "disabled"\n' > /etc/codex/config.toml
COPY evidence-collector /opt/evidence-collector
RUN chmod +x /opt/evidence-collector/collect
WORKDIR /workspace

ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}
COPY workspace/ /seed/
COPY workspace-init/init.sh /usr/local/bin/init-workspace
RUN chmod +x /usr/local/bin/init-workspace
ENTRYPOINT ["/usr/local/bin/init-workspace"]

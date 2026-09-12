ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}
COPY workspace /workspace-seed
COPY world-controller/step-release-map.json /step-release-map.json
COPY workspace-init/init.sh /init.sh
RUN chmod +x /init.sh
ENTRYPOINT ["/init.sh"]

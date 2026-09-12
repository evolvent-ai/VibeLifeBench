FROM python:3.12-slim

COPY wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels "mcp==1.25.0"

ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ENV HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} NO_PROXY=${NO_PROXY}

COPY world-controller/controller.py /opt/world-controller/controller.py
COPY world-controller/snapshot /opt/world-controller/snapshot
COPY world-controller/step-release-map.json /opt/world-controller/step-release-map.json
COPY world-controller/releases /opt/world-controller/releases
COPY evidence-collector/harbor_env.py /opt/world-controller/capture/harbor_env.py
COPY evidence-collector/snapshot_capture.py /opt/world-controller/capture/snapshot_capture.py
RUN chmod +x /opt/world-controller/snapshot \
    && mkdir -p \
        /evidence \
        /workspace-source \
        /banking-env \
        /brokerage-env \
        /job-board-env \
        /email-env \
        /calendar-env \
        /legal-search-env \
        /notion-env \
        /controller-state

EXPOSE 8090
ENTRYPOINT ["python", "/opt/world-controller/controller.py", "serve"]

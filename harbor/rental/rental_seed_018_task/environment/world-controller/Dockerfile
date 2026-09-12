FROM python:3.12-slim

RUN pip install --no-cache-dir "mcp==1.25.0"

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
        /listing-platform-env \
        /email-env \
        /calendar-env \
        /legal-search-env \
        /maps-env \
        /notion-env \
        /notification-hub-env \
        /review-platform-env \
        /controller-state \
        /maps-env \
        /review-platform-env

EXPOSE 8090
ENTRYPOINT ["python", "/opt/world-controller/controller.py", "serve"]

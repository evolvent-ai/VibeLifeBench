ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl sqlite3 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir "mcp==1.25.0"

COPY world-controller/controller.py /opt/world-controller/controller.py
COPY world-controller/snapshot /opt/world-controller/snapshot
COPY world-controller/step-release-map.json /opt/world-controller/step-release-map.json
COPY world-controller/releases /opt/world-controller/releases
COPY evidence-collector/harbor_env.py /opt/world-controller/capture/harbor_env.py
COPY evidence-collector/snapshot_capture.py /opt/world-controller/capture/snapshot_capture.py
RUN chmod +x /opt/world-controller/snapshot \
    && mkdir -p /controller-state /evidence /world-clock /workspace-source \
        /calendar-env \
        /content-platform-env \
        /delivery-logistics-env \
        /ecommerce-env \
        /email-env \
        /hotel-booking-env \
        /maps-env \
        /notification-hub-env \
        /notion-env \
        /rail-booking-env \
        /weather-env

EXPOSE 8090
ENTRYPOINT ["python", "/opt/world-controller/controller.py", "serve"]

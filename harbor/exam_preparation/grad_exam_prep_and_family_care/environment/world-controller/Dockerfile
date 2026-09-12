FROM python:3.12-slim

COPY world-controller/controller.py /opt/world-controller/controller.py
COPY world-controller/snapshot /opt/world-controller/snapshot
COPY world-controller/step-release-map.json /opt/world-controller/step-release-map.json
COPY world-controller/controller-config.json /opt/world-controller/controller-config.json
COPY world-controller/releases /opt/world-controller/releases
COPY evidence-collector/harbor_env.py /opt/world-controller/capture/harbor_env.py
COPY evidence-collector/snapshot_capture.py /opt/world-controller/capture/snapshot_capture.py
RUN pip install --no-cache-dir "mcp==1.25.0"
RUN chmod +x /opt/world-controller/snapshot \
    && mkdir -p /evidence /workspace-source /banking-env /calendar-env /ecommerce-env \
       /email-env /health-tracker-env /notion-env /notification-hub-env \
       /controller-state /world-clock

EXPOSE 8090
ENTRYPOINT ["python", "/opt/world-controller/controller.py", "serve"]

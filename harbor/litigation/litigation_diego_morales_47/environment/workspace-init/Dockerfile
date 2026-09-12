# Same base as every other service in this task. A second base image (alpine)
# meant the delivery depended on one more registry pull that could — and did —
# fail with a connection reset, taking the whole run down before step 1. One
# base image keeps the environment buildable from what the package already
# needs (Tencent delivery gate G0: buildable from delivered files alone).
FROM python:3.12-slim

COPY workspace/ /seed/
COPY workspace-init/init.sh /usr/local/bin/init-workspace
RUN chmod +x /usr/local/bin/init-workspace

ENTRYPOINT ["/usr/local/bin/init-workspace"]

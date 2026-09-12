FROM python:3.12-slim
COPY workspace /workspace-seed
COPY workspace-init/init.sh /init.sh
RUN chmod +x /init.sh
ENTRYPOINT ["/init.sh"]

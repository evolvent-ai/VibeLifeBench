FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir --timeout 120 --retries 10 "mcp==1.25.0"
RUN pip install --no-cache-dir --timeout 120 --retries 10 "hatchling==1.27.0"

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir --no-deps --no-build-isolation .

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "mkdir -p /env && cp -r /env-seed/. /env/ && exec delivery-logistics-mock --host 0.0.0.0 --port 8000 --env /env"]

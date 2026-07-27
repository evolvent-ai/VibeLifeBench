FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "-c", "mkdir -p /env && cp -r /env-seed/. /env/ && exec visa-and-advisory-mock --host 0.0.0.0 --port 8000 --env /env"]

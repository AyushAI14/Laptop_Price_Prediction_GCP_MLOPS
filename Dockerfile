FROM python:3.13-slim

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8080

# Use the shell form to properly expand the $PORT variable provided by Cloud Run
CMD ["sh", "-c", "uvicorn gcp.deployment.cloud_run.app:app --host 0.0.0.0 --port ${PORT}"]
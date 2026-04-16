# Optional — local or CI API image (control plane only). Graph explorer auto-start
# is disabled; use compose with a separate Streamlit service for production UI patterns.
FROM python:3.13-slim-bookworm

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8420
CMD ["python", "scripts/serve-api.py", "--host", "0.0.0.0", "--port", "8420", "--no-graph-explorer"]

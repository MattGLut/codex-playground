FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app and templates explicitly
COPY app /app/app
COPY templates /app/templates

# Optional: copy static, configs, etc.
# COPY static /app/static

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

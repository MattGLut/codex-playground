FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary folders and files
COPY app /app/app
COPY templates /app/templates
COPY docker-compose.yml /app/docker-compose.yml
COPY setup.sh /app/setup.sh

# Optionally copy other files like README or tests if needed
# COPY tests /app/tests

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

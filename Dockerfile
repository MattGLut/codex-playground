FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl ffmpeg libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY app /app/app
COPY templates /app/templates
COPY static /app/static
COPY setup.sh /app/setup.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

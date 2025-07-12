# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app ./app
COPY .env ./

# Expose port
EXPOSE 8000

# Run the app with Uvicorn (no reload, production settings)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

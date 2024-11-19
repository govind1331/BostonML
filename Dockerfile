# Use Python 3.8 slim as base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the training code and other necessary files
COPY trainer.py .
COPY job_config.py .

# Set Python path
ENV PYTHONPATH=/app

# Create directories for model artifacts
RUN mkdir -p /app/models /app/metrics

# Set default command
ENTRYPOINT ["python", "trainer.py"]
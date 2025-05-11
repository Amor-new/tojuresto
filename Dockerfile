# Use official Python slim image
FROM python:3.10-slim

# Set environment variables early
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Set workdir
WORKDIR /app

# Install system dependencies (only what's needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Copy app files
COPY . .

# Expose port (optional but helps readability)
EXPOSE 8000

# Launch app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "toju_food.wsgi:application"]

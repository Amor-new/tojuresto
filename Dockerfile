FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application files into the container
COPY . /app/
WORKDIR /app

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Start the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "toju_food.wsgi:application"]

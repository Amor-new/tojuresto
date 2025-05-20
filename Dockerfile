# Use official Python slim image
FROM python:3.11-alpine3.19

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    KUBECTL_VERSION="v1.29.0"

# Set workdir
WORKDIR /app

# Upgrade base system packages & install dependencies 
RUN apk update && apk upgrade && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    libpng-dev \
    freetype-dev \
    lcms2-dev \
    tiff-dev \
    tk \
    tcl \
    curl \
    bash

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code
COPY . .

# Expose port for Django/Gunicorn
EXPOSE 8000

# Set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

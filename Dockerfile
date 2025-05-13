# Use official Python slim image
FROM python:3.14-rc-alpine3.21

# Set environment variables early
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    KUBECTL_VERSION="v1.29.0"

# Set workdir
WORKDIR /app

# Install system dependencies (Pillow, psycopg, etc.) + curl & gnupg for secure downloads
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    libjpeg \
    libpng-dev \
    openjpeg-dev \
    freetype-dev \
    lcms2-dev \
    tiff-dev \
    tk \
    tcl \
    libpq=17.5-r0 \
    postgresql-dev=17.5-r0 \
    curl \
    bash


# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app source
COPY . .

# Expose port
EXPOSE 8000

# Entry script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

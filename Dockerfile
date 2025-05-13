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
    libpq \
    postgresql-dev \
    curl \
    bash

# -------------------------------
# Install kubectl securely
# -------------------------------
RUN curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" && \
    echo "Verifying kubectl binary checksum..." && \
    curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl.sha256" && \
    echo "$(cat kubectl.sha256)  kubectl" | sha256sum -c - && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl kubectl.sha256

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

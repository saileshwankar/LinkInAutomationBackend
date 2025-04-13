# Start from a lightweight base image
FROM python:3.12-alpine

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED 1

# Install system dependencies (including Chromium for Selenium)
RUN apk update && apk add --no-cache \
    bash \
    curl \
    chromium \
    chromium-chromedriver \
    git \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
    python3-dev \
    py3-pip \
    jpeg-dev \
    zlib-dev

# Set display environment variable (for headless browser)
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy your code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set Chromium path for Selenium
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Expose port (same as Flask default)
EXPOSE 8080

# Use Gunicorn to serve the app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]

FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    xz-utils \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libvulkan1 \
    xdg-utils \
    ca-certificates \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver (matching Chrome version)
RUN bash -c '\
  CHROME_VERSION=$(google-chrome --version | awk "{print \$3}" | cut -d "." -f 1) && \
  DRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}) && \
  wget -q https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip && \
  unzip chromedriver_linux64.zip && \
  mv chromedriver /usr/local/bin/chromedriver && \
  chmod +x /usr/local/bin/chromedriver && \
  rm chromedriver_linux64.zip \
'

ENV CHROME_BIN=/usr/bin/google-chrome
ENV PATH=$PATH:/usr/local/bin/chromedriver

# Set work directory
WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port if needed
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]

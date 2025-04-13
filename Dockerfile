FROM python:3.12-slim

# Install Chrome dependencies & Chrome
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 \
    libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils libu2f-udev \
    libvulkan1 libgbm1 libxshmfence1 libxss1 libxi6 libxcursor1 libxinerama1 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome.deb && rm google-chrome.deb

# Install ChromeDriver (matching Chrome version, 114 in your case)
RUN wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PATH=$PATH:/usr/local/bin/chromedriver

# Set working directory
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port
EXPOSE 8080

# Start the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]

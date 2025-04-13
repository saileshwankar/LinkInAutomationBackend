# Use Selenium's standalone Chrome image
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Switch to root for package installation
USER root

# Python is included, but update just in case
RUN apt-get update && apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set Chrome options for headless (optional but useful for consistency)
ENV CHROME_OPTIONS="--no-sandbox --disable-dev-shm-usage --disable-gpu --disable-software-rasterizer --headless=new"

# Switch back to seluser (as required by base image)
USER seluser

# Copy and install Python requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Set environment for Flask
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Expose Flask port
EXPOSE 5000

# Start Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

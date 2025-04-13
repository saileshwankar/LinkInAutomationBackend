# Use Selenium's standalone Chrome image
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Install Python & pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Set Chrome flags via environment variable
ENV CHROME_OPTIONS="--no-sandbox --disable-dev-shm-usage --headless=new --disable-gpu"

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Flask environment settings
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Start Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

# Use Selenium's standalone Chrome image
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Install Python & pip (already included, but for safety)
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Optional: Set Chrome flags via ENV (can be used inside your app)
ENV CHROME_OPTIONS="--no-sandbox --disable-dev-shm-usage --disable-gpu --disable-software-rasterizer --headless=new"
USER seluser

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . .

# Flask environment variables
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Expose Flask port
EXPOSE 5000

# Set default user back to seluser (recommended by Selenium image)
USER seluser

# Start Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

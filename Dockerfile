# Use the Selenium + Chrome base image
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Install Python & pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production

# Expose Flask's default port
EXPOSE 5000

# Start Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

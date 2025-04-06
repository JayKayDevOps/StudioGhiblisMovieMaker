# Update Dockerfile to install Gunicorn for production
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install required packages
COPY requirements.txt requirements.txt

# Install dependencies, including Gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Copy the entire project into the container
COPY . .

# Expose the port your Flask app uses
EXPOSE 5000

# Set the entrypoint to ensure execution of entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# No need for CMD here, it's handled in entrypoint.sh
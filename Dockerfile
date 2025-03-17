FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install required packages
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port your Flask app uses
EXPOSE 5000

# Set the entrypoint to ensure the entrypoint.sh script is executed
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the Flask app
CMD ["python", "app/app.py"]
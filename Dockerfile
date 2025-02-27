FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file and install required packages
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port your Flask app uses
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app/app.py"]
#!/bin/bash

# Exit script on any error
set -e

# Debug: List contents of /app and /app/app
echo "📂 Current contents of /app:"
ls /app
echo "📂 Current contents of /app/app:"
ls /app/app

# Run the seed script
echo "🔄 Running seed.py to seed the database..."
if python /app/seed.py; then
    echo "✅ Database seeding completed successfully!"
else
    echo "❌ Database seeding failed. Exiting..."
    exit 1
fi

# Start the Flask app using Gunicorn in production mode
echo "🚀 Starting Flask application with Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 run:app
import os

class Config:
    """Base configuration with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Use Docker service name for DB_HOST when using Docker Compose
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'db')  # Use 'db' as service name from docker-compose.yml
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'moviemaking_db')

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    # Log Database URI for debugging (Optional)
    print(f"Connecting to database at {DB_HOST}:{DB_PORT}")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries in development

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

# Load config dynamically based on environment
env = os.getenv('FLASK_ENV', 'development')
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

# Print environment for verification
print(f"Running in {env} mode")

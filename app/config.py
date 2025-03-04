import os

class Config:
    """Base configuration with common settings."""
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration (local database)."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries
    CREATE_DB = True  # Automatically create tables in development

    # Hardcoded local database settings
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "moviemaking_db"

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class ProductionConfig(Config):
    """Production configuration (Amazon RDS via environment variables)."""
    DEBUG = False
    CREATE_DB = False  # Avoid auto-init in production

    # Load environment variables
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")  # Default to 5432
    DB_NAME = os.getenv("DB_NAME")

    # Only enforce environment variable validation in production
    if os.getenv("FLASK_ENV") == "production":
        missing_vars = [var for var in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"] if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"❌ Missing required environment variables: {', '.join(missing_vars)}")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        if all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]) else None
    )

# Dictionary to map environment names to config classes
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

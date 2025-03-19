import boto3
import os
import json

def get_secret(secret_name, region_name="eu-west-1"):
    """Retrieve secret from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        secret_value = client.get_secret_value(SecretId=secret_name)
        secret = json.loads(secret_value['SecretString'])
        return secret
    except Exception as e:
        raise Exception(f"Error retrieving secret: {e}")

class Config:
    """Base configuration with common settings."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
        # Use Docker service name for DB_HOST when using Docker Compose - used for runnning localy
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
    
class DevelopmentConfig2(Config):
    """Development configuration (AWS database)."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries
    CREATE_DB = True  # Automatically create tables in development
    
  # Environment variables for other configurations
    DB_USER = os.getenv('DB_USER', 'DB_Admin')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '2ZnaqSZ:')
    DB_HOST = os.getenv('DB_HOST', 'mydbinstance.endpoint.amazonaws.com')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'moviemaking_dev')

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    # Mask the password in logs
    print(f"Connecting to database at {DB_HOST}:{DB_PORT} with user {DB_USER}")


class ProductionConfig(Config):
    """Production configuration (Amazon RDS via AWS Secrets Manager)."""
    DEBUG = False
    CREATE_DB = False

    # Securely load AWS Secrets Manager
    region_name = os.getenv("AWS_REGION", "eu-west-1")
    try:
        secrets = get_secret(secret_name="DB_PASSWORD_DEV", region_name=region_name)
        DB_PASSWORD = secrets.get("DB_PASSWORD")
    except Exception as e:
        print(f"Warning: Failed to retrieve secret. Using fallback. Error: {e}")
        

    # Load remaining environment variables
    DB_USER = os.getenv("DB_USER")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")

    # Validate required variables in production
    if os.getenv("FLASK_ENV") == "production":
        required_vars = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"]
        missing_vars = [var for var in required_vars if not locals().get(var)]
        if missing_vars:
            raise ValueError(f"❌ Missing required environment variables: {', '.join(missing_vars)}")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Dictionary to map environment names to config classes
config = {
    "development2": DevelopmentConfig2,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
# Dynamically load the configuration
flask_env = os.getenv("FLASK_ENV", "development2")
selected_config = config.get(flask_env, DevelopmentConfig2)
print(f"Using configuration: {selected_config.__name__}")
import os
import logging  # Import logging module
from flask import Flask
from flask_login import LoginManager
from sqlalchemy import text, inspect
from models import db, User
from config import config  # Import configuration from config.py
from routes.public_routes import public_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file named app.log
        logging.StreamHandler()         # Log to the console
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # Load configuration
    env = os.getenv("FLASK_ENV", "development2")  # Use environment variable or default
    app.config.from_object(config[env])
    logger.info(f"Environment set to {env}")

    # Initialize extensions
    db.init_app(app)
    logger.info("Database initialized")

    # Database connection test and table checks
    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            logger.info(f"Database connected successfully to {app.config.get('DB_HOST', 'Unknown Host')}")

            # Check for existing tables
            inspector = inspect(db.engine)
            tables_exist = bool(inspector.get_table_names())

            if tables_exist:
                logger.info("Tables exist in the database.")
            else:
                logger.warning("No tables found in the database.")
                if app.config.get("CREATE_DB", False):  # Check CREATE_DB flag
                    logger.info("CREATE_DB enabled. Initializing database...")
                    try:
                        db.create_all()
                        logger.info("Database tables created successfully!")
                    except Exception as e:
                        logger.error(f"An error occurred while creating tables: {e}")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")

    # Register Blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    logger.info("Blueprints registered successfully")

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    logger.info("Flask-Login initialized")

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

# Run the Flask App
if __name__ == "__main__":
    app = create_app()
    logger.info("Starting the Flask app...")
    app.run(host="0.0.0.0", port=5000, debug=True)




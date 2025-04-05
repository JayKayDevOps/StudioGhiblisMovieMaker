import os
import subprocess
import logging  # Import logging module
from flask import Flask
from flask_login import LoginManager
from secure import Secure
from sqlalchemy import text, inspect

from app.config import config
from app.models import db, User
from app.routes.public_routes import public_bp
from app.routes.user_routes import user_bp
from app.routes.admin_routes import admin_bp

login_manager = LoginManager()

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

secure_headers = Secure.with_default_headers()


def _add_security_headers(response):
    """ add security headers, allow external assets for Bootstrap, jQuery, Font Awesome"""
    secure_headers.set_headers(response)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com https://cdnjs.cloudflare.com https://code.jquery.com https://kit.fontawesome.com;"
        "script-src 'self' 'unsafe-inline'  https://code.jquery.com https://cdnjs.cloudflare.com https://kit.fontawesome.com; "
        #"img-src 'self' https://placehold.co; "
        "font-src 'self' https://fonts.gstatic.com https://ka-f.fontawesome.com; "
        "connect-src 'self' https://ka-f.fontawesome.com; "  # for JS requests e.g. fetch, XHR, WebSockets
    )
    return response


def create_app(env="development"):
    """Application factory for creating and configuring the Flask app."""
    
    app = Flask(__name__)
    app.config.from_object(config[env])

    app.after_request(_add_security_headers)

    # Register blueprints
    print("🔧 Registering Blueprints...")
    app.register_blueprint(public_bp, url_prefix='/public')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp)

    logger.info("Blueprints registered successfully")

    with app.app_context():
        print("🔍 Registered Admin Blueprint Endpoints:")
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith(admin_bp.name + "."):
                print(f"➡️ {rule} -> {rule.endpoint}")

    # Initialize database
    try:
        db.init_app(app)
        with app.app_context():
            db.session.execute(text("SELECT 1"))
            print(f"✅ Database connected to {app.config.get('DB_HOST', 'Unknown Host')}")

            inspector = inspect(db.engine)
            tables_exist = bool(inspector.get_table_names())

            if app.config.get("CREATE_DB", False) and not tables_exist:
                print("⚠️ No tables found and CREATE_DB is enabled. Creating tables...")
                db.create_all()
                print("✅ Tables created successfully.")

    except Exception as e:
        print(f"❌ Database connection failed: {e}")

    # Setup login manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    logger.info("Flask-Login initialized")

    return app

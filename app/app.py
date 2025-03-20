# src/app/app.py - Flask App Using config.py
import os
import subprocess  # To execute db_init.py
from flask import Flask
from flask_login import LoginManager
from .models import db, User
from sqlalchemy import text, inspect
from .config import config  # Import configuration from config.py
from .routes.public_routes import public_bp
from .routes.user_routes import user_bp
from .routes.admin_routes import admin_bp

# Load Configuration Based on Environment
env = os.getenv('FLASK_ENV', 'development')  # Get the environment
app = Flask(__name__)
app.config.from_object(config[env])  # Load the appropriate config

# Register Blueprints for different routes
app.register_blueprint(public_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

# Initialize Database
try:
    db.init_app(app)
    with app.app_context():
        # Test database connection
        db.session.execute(text('SELECT 1'))
        print(f'✅ Database connected successfully to {app.config.get("DB_HOST", "Unknown Host")}')
        
        # # Check if tables exist
        inspector = inspect(db.engine)
        tables_exist = bool(inspector.get_table_names())

        # Only run db_init.py if CREATE_DB is True and tables are missing
        if app.config.get("CREATE_DB", False) and not tables_exist:
            print("⚠️ No tables found and CREATE_DB is enabled. Running db_init.py...")
            with app.app_context():
                db.create_all()
                print("✅ Database tables created successfully!")

except Exception as e:
    print(f'❌ Database connection failed: {e}')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Run the Flask App
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000, debug=app.config.get('DEBUG', True))
    app.run()

# docker run --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=moviemaking_db -p 5432:5432 -d postgres
# src/app/app.py - Flask App Using config.py
from flask import Flask
from flask_login import LoginManager
from models import db, User
from sqlalchemy import text
from config import config  # Import configuration from config.py
import os
from routes.public_routes import public_bp
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp


# Load Configuration Based on Environment
env = os.getenv('FLASK_ENV', 'development')
app = Flask(__name__)
app.config.from_object(config[env])

# register blueprints for different routes
app.register_blueprint(public_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

# Initialize Database
try:
    db.init_app(app)
    with app.app_context():
        db.session.execute(text('SELECT 1'))  # Simple query to test connection
        print(f'✅ Database connected successfully to {app.config["DB_HOST"]}')
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
    app.run(host="0.0.0.0", port=5000, debug=app.config.get('DEBUG', True))
    # app.run()

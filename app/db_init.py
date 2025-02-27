from app import db, app

# Initialize DB inside the Flask app context
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

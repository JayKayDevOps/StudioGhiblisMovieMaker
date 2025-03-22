import os
import sys
from flask import Flask
from datetime import date
from app.config import config  # Import configurations
from app.models import db, User, Course, Module, CourseModule, Subscription  # Import models

# Ensure Python recognizes "app" as a package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Get environment setting
env = os.getenv("FLASK_ENV", "development")
app_config = config[env]  # Load the correct configuration

# Create the Flask app and apply config
print(f"Seeding database for {env} environment...")
app = Flask(__name__)
app.config.from_object(app_config)

# Initialize the database with the app
db.init_app(app)

def seed_database():
    """Populate the database with dummy users, courses, modules, and subscriptions."""
    with app.app_context():
        # Ensure all tables exist
        db.create_all()

        # Clear existing data
        db.session.query(Subscription).delete()
        db.session.query(CourseModule).delete()
        db.session.query(Module).delete()
        db.session.query(Course).delete()
        db.session.query(User).delete()
        db.session.commit()

        print("✅ Old data cleared.")

        # Create admin user
        admin = User(first_name="Studio", second_name="Ghibli Admin", email="admin@ghibli.com", role="admin")
        admin.set_password("admin123")

        # Create dummy customers
        users = [
            User(first_name="Hayao", second_name="Miyazaki", email="miyazaki@example.com"),
            User(first_name="Isao", second_name="Takahata", email="takahata@example.com"),
            User(first_name="Yoshifumi", second_name="Kondō", email="kondo@example.com"),
            User(first_name="Hiromasa", second_name="Yonebayashi", email="yonebayashi@example.com")
        ]
        for user in users:
            user.set_password("password123")

        db.session.add(admin)
        db.session.add_all(users)
        db.session.commit()  # ✅ Commit so IDs are assigned

        print("✅ Users added.")

        # Create dummy courses
        courses = [
            Course(name="Moving Castle Creations", description="A 3D animation workshop inspired by Howl's Moving Castle.", price=150.00),
            Course(name="Ghibli Storytelling Masterclass", description="Learn storytelling secrets from Studio Ghibli films.", price=200.00),
            Course(name="Anime Character Design", description="Sketch and design your own anime characters!", price=100.00),
            Course(name="Hand-Drawn Animation Basics", description="A deep dive into the world of traditional 2D animation.", price=180.00)
        ]
        db.session.add_all(courses)
        db.session.commit()  # ✅ Commit so IDs are assigned

        print("✅ Courses added.")

        # Create dummy modules
        modules = [
            Module(title="Concept Art Basics", description="Learn how to create concept art for animations."),
            Module(title="Character Animation", description="Study movement and animation techniques."),
            Module(title="Storyboard Design", description="Develop strong storytelling through visual storyboarding."),
            Module(title="Voice Acting & Sound", description="Explore voice-over techniques and sound design.")
        ]
        db.session.add_all(modules)
        db.session.commit()  # ✅ Commit so IDs are assigned

        print("✅ Modules added.")

        # Assign modules to courses
        course_modules = [
            CourseModule(course_id=courses[0].id, module_id=modules[0].id),
            CourseModule(course_id=courses[0].id, module_id=modules[1].id),
            CourseModule(course_id=courses[1].id, module_id=modules[2].id),
            CourseModule(course_id=courses[2].id, module_id=modules[3].id),
        ]
        db.session.add_all(course_modules)
        db.session.commit()

        print("✅ Course modules added.")

        # Create dummy subscriptions (AFTER committing users & courses)
        subscriptions = [
            Subscription(user_id=users[0].id, course_id=courses[0].id, special_requests="Need extra animation tools."),
            Subscription(user_id=users[1].id, course_id=courses[1].id, special_requests="Would love a Q&A with the instructor."),
            Subscription(user_id=users[2].id, course_id=courses[2].id, special_requests="Prefer digital sketching over hand-drawn."),
            Subscription(user_id=users[3].id, course_id=courses[3].id, special_requests="Need subtitles for better understanding."),
        ]
        db.session.add_all(subscriptions)
        db.session.commit()

        print("✅ Subscriptions added successfully!")

if __name__ == "__main__":
    print("Seeding database...")
    seed_database()

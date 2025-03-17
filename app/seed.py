import os
import logging
import boto3
from flask import Flask
from datetime import date
from config import config  # Import configurations
from models import db, User, Course, Module, CourseModule, Subscription  # Import models

# Flask app configuration
env = os.getenv("FLASK_ENV", "development")  # Determine environment (default: development)
app_config = config[env]  # Load configuration based on environment

app = Flask(__name__)
app.config.from_object(app_config)

# Initialize the database with the Flask app
db.init_app(app)

# CloudWatch Configuration
LOG_GROUP_NAME = "/ecs/flask-app-service"
LOG_STREAM_NAME = f"database_seeding-{date.today().isoformat()}"  # Custom log stream for database seeding
session = boto3.Session(region_name="eu-west-1")  # Replace with your region (e.g., "us-east-1")
logs_client = session.client('logs')

# Create the log group (if it doesn't already exist)
try:
    logs_client.create_log_group(logGroupName=LOG_GROUP_NAME)
except logs_client.exceptions.ResourceAlreadyExistsException:
    pass  # Log group already exists

# Create the log stream (if it doesn't already exist)
try:
    logs_client.create_log_stream(logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME)
except logs_client.exceptions.ResourceAlreadyExistsException:
    pass  # Log stream already exists

class CloudWatchHandler(logging.Handler):
    """Custom logging handler for sending logs to CloudWatch."""
    def emit(self, record):
        log_entry = self.format(record)
        try:
            logs_client.put_log_events(
                logGroupName=LOG_GROUP_NAME,
                logStreamName=LOG_STREAM_NAME,
                logEvents=[
                    {
                        'timestamp': int(record.created * 1000),  # Convert to milliseconds
                        'message': log_entry
                    }
                ]
            )
        except Exception as e:
            print(f"❌ Failed to log to CloudWatch: {e}")

# Logger for database seeding operations
seeding_logger = logging.getLogger('database_seeding')
seeding_logger.setLevel(logging.INFO)
seeding_logger.addHandler(CloudWatchHandler())

# Seed database function
def seed_database():
    """Populate the database with dummy users, courses, modules, and subscriptions."""
    with app.app_context():
        try:
            # Clear existing data
            try:
                db.session.query(Subscription).delete()
                db.session.query(CourseModule).delete()
                db.session.query(Module).delete()
                db.session.query(Course).delete()
                db.session.query(User).delete()
                db.session.commit()
                seeding_logger.info("✅ Old data cleared successfully.")
            except Exception as e:
                db.session.rollback()
                seeding_logger.error(f"❌ Failed to clear old data: {e}")
                return

            # Add an admin user
            try:
                admin = User(first_name="Studio", second_name="Ghibli Admin", email="admin@ghibli.com", role="admin")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                seeding_logger.info("✅ Admin user added.")
            except Exception as e:
                db.session.rollback()
                seeding_logger.error(f"❌ Failed to add admin user: {e}")
                return

            # Add dummy users
            try:
                users = [
                    User(first_name="Hayao", second_name="Miyazaki", email="miyazaki@example.com"),
                    User(first_name="Isao", second_name="Takahata", email="takahata@example.com"),
                    User(first_name="Yoshifumi", second_name="Kondō", email="kondo@example.com"),
                    User(first_name="Hiromasa", second_name="Yonebayashi", email="yonebayashi@example.com")
                ]
                for user in users:
                    user.set_password("password123")
                db.session.add_all(users)
                db.session.commit()
                seeding_logger.info("✅ Users added to the database.")
            except Exception as e:
                db.session.rollback()
                seeding_logger.error(f"❌ Failed to add users: {e}")
                return

            # Add dummy courses
            try:
                courses = [
                    Course(name="Moving Castle Creations", description="A 3D animation workshop inspired by Howl's Moving Castle.", price=150.00),
                    Course(name="Ghibli Storytelling Masterclass", description="Learn storytelling secrets from Studio Ghibli films.", price=200.00),
                    Course(name="Anime Character Design", description="Sketch and design your own anime characters!", price=100.00),
                    Course(name="Hand-Drawn Animation Basics", description="A deep dive into traditional 2D animation.", price=180.00)
                ]
                db.session.add_all(courses)
                db.session.commit()
                seeding_logger.info("✅ Courses added to the database.")
            except Exception as e:
                db.session.rollback()
                seeding_logger.error(f"❌ Failed to add courses: {e}")
                return

            # Add dummy modules
            try:
                modules = [
                    Module(title="Concept Art Basics", description="Learn how to create concept art for animations."),
                    Module(title="Character Animation", description="Study movement and animation techniques."),
                    Module(title="Storyboard Design", description="Develop strong storytelling through visual storyboarding."),
                    Module(title="Voice Acting & Sound", description="Explore voice-over techniques and sound design.")
                ]
                db.session.add_all(modules)
                db.session.commit()
                seeding_logger.info("✅ Modules added to the database.")
            except Exception as e:
                db.session.rollback()
                seeding_logger.error(f"❌ Failed to add modules: {e}")
                return

            # Assign modules to courses
            try:
                course_modules = [
                    CourseModule(course_id=courses[0].id, module_id=modules[0].id),
                    CourseModule(course_id=courses[0].id, module_id=modules[1].id),
                    CourseModule(course_id=courses[1].id, module_id=modules[2].id),
                    CourseModule(course_id=courses[2].id, module_id=modules[3].id),
                ]
                db.session.add_all(course_modules)
                db.session.commit()
                seeding_logger.info("✅ Course-module relationships added.")
            except Exception as e:
                db.session.rollback()
                seeding_logger.error(f"❌ Failed to assign modules to courses: {e}")
                return

            # Add dummy subscriptions
            try:
                subscriptions = [
                    Subscription(user_id=users[0].id, course_id=courses[0].id, special_requests="Need extra animation tools."),
                    Subscription(user_id=users[1].id, course_id=courses[1].id, special_requests="Would love a Q&A with the instructor."),
                    Subscription(user_id=users[2].id, course_id=courses[2].id, special_requests="Prefer digital sketching over hand-drawn."),
                    Subscription(user_id=users[3].id, course_id=courses[3].id, special_requests="Need subtitles for better understanding.")
                ]
                db.session.add_all(subscriptions)
                db.session.commit()
                seeding_logger.info("✅ Subscriptions added successfully.")
            except Exception as e:
                db.session.rollback()
                seeding_logger.error(f"❌ Failed to add subscriptions: {e}")
                return

            # Success log
            seeding_logger.info("✅ Database seeding completed successfully!")
            print("✅ Database seeding completed successfully!")
        except Exception as e:
            # Fallback error handling for unforeseen issues
            seeding_logger.error(f"❌ Unexpected error during database seeding: {e}")
            print(f"❌ Unexpected error during database seeding: {e}")


if __name__ == "__main__":
    seed_database()

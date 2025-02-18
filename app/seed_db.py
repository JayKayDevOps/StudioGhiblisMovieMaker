from app import app, db
from models import User, Course, Subscription
from datetime import date
import random

def seed_database():
    """Populate the database with dummy users, courses, and subscriptions."""

    with app.app_context():
        # Clear existing data
        db.session.query(Subscription).delete()
        db.session.query(User).delete()
        db.session.query(Course).delete()
        db.session.commit()

        print("✅ Old data cleared.")

        # Create admin user
        admin = User(full_name="Studio Ghibli Admin", email="admin@ghibli.com", role="admin")
        admin.set_password("admin123")

        # Create dummy customers
        users = [
            User(full_name="Hayao Miyazaki", email="miyazaki@example.com"),
            User(full_name="Isao Takahata", email="takahata@example.com"),
            User(full_name="Yoshifumi Kondō", email="kondo@example.com"),
            User(full_name="Hiromasa Yonebayashi", email="yonebayashi@example.com")
        ]

        for user in users:
            user.set_password("password123")

        db.session.add(admin)
        db.session.add_all(users)

        print("✅ Users added.")

        # Create dummy courses
        courses = [
            Course(name="Moving Castle Creations", description="A 3D animation workshop inspired by Howl's Moving Castle.",
                   price=150.00, start_date=date(2024, 3, 1), end_date=date(2024, 3, 5)),
            Course(name="Ghibli Storytelling Masterclass", description="Learn storytelling secrets from Studio Ghibli films.",
                   price=200.00, start_date=date(2024, 4, 10), end_date=date(2024, 4, 15)),
            Course(name="Anime Character Design", description="Sketch and design your own anime characters!",
                   price=100.00, start_date=date(2024, 5, 5), end_date=date(2024, 5, 10)),
            Course(name="Hand-Drawn Animation Basics", description="A deep dive into the world of traditional 2D animation.",
                   price=180.00, start_date=date(2024, 6, 1), end_date=date(2024, 6, 7))
        ]

        db.session.add_all(courses)

        print("✅ Courses added.")

        # Create dummy subscriptions
        subscriptions = [
            Subscription(user_id=users[0].id, course_id=courses[0].id, special_requests="Need extra animation tools."),
            Subscription(user_id=users[1].id, course_id=courses[1].id, special_requests="Would love a Q&A with the instructor."),
            Subscription(user_id=users[2].id, course_id=courses[2].id, special_requests="Prefer digital sketching over hand-drawn."),
            Subscription(user_id=users[3].id, course_id=courses[3].id, special_requests="Need subtitles for better understanding."),
        ]

        db.session.add_all(subscriptions)

        db.session.commit()

        print("✅ subscriptions added successfully!")

if __name__ == "__main__":
    seed_database()
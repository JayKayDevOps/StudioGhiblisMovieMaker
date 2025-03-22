import pytest
from app.services.user_service import UserService
from app.models import db, User, Course, Subscription
from datetime import datetime


@pytest.fixture
def user_service():
    return UserService()


def test_get_user_bookings(user_service, app):

    with app.app_context():
        # Arrange
        user = User(first_name="Sophie", second_name="Hatter", email="sophie@castle.com")
        user.set_password("howl")
        course = Course(name="Castle Magic 101", description="Flying lessons", price=300)
        db.session.add_all([user, course])
        db.session.commit()

        sub = Subscription(
            user_id=user.id,
            course_id=course.id,
            status="confirmed",
            subscription_date=datetime(2024, 2, 1, 9, 0, 0),
            special_requests="Room with a view"
        )
        db.session.add(sub)
        db.session.commit()

        # Act
        bookings = user_service.get_user_bookings(user.id)

        # Assert
        assert len(bookings) == 1
        assert bookings[0]["course_name"] == "Castle Magic 101"
        assert bookings[0]["status"] == "confirmed"
        assert bookings[0]["subscription_date"] == "2024-02-01 09:00:00"

def test_book_course_success(user_service, app):

    with app.app_context():
        # Arrange
        user = User(first_name="Shun", second_name="Kazama", email="shun@kokuriko.com")
        user.set_password("123")
        course = Course(name="Film Club", description="Rooftop stories", price=120)
        db.session.add_all([user, course])
        db.session.commit()

        # Act
        result = user_service.book_course(user.id, course.id, "Vegan lunch please")

        # Assert
        assert result is True
        booking = Subscription.query.filter_by(user_id=user.id, course_id=course.id).first()
        assert booking is not None
        assert booking.special_requests == "Vegan lunch please"
        assert booking.status == "pending"


def test_book_course_duplicate(user_service, app):

    with app.app_context():
        # Arrange
        user = User(first_name="Shizuku", second_name="Tsukishima", email="shizuku@example.com")
        user.set_password("123")
        course = Course(name="Storytelling", description="Novel writing", price=90)
        db.session.add_all([user, course])
        db.session.commit()

        # First booking
        user_service.book_course(user.id, course.id, "Quiet seat")

        # Act: Try booking again
        result = user_service.book_course(user.id, course.id, "Window seat")

        # Assert
        assert result is False
import pytest
from app.services.admin_service import AdminService
from datetime import datetime
from app.models import db, User, Course, Subscriptions, Module, CourseModule


@pytest.fixture
def admin_service():
    return AdminService()


def test_get_all_users(app):
    """Test retrieving all users in an in-memory SQLite database."""

    with app.app_context():  # ✅ Ensure we use Flask's context
        # Arrange: Add test users with a valid password
        user1 = User(first_name="Test", second_name="User1", email="user1@example.com", role="customer")
        user1.set_password("password123")  # ✅ Fix: Set password

        user2 = User(first_name="Test", second_name="User2", email="user2@example.com", role="admin")
        user2.set_password("password123")  # ✅ Fix: Set password

        db.session.add_all([user1, user2])
        db.session.commit()

        # Act: Fetch users from the service
        admin_service = AdminService()
        users = admin_service.get_all_users()

        # Assert: Verify the output
        assert len(users) == 2
        assert users[0]["email"] == "user1@example.com"
        assert users[1]["role"] == "admin"


def test_get_all_bookings(admin_service, app):

    with app.app_context():
        # Arrange: create user, course, and subscription
        user = User(first_name="Hayao", second_name="Miyazaki", email="hayao@example.com", role="customer")
        user.set_password("password123")
        course = Course(name="Ghibli Storytelling", description="Deep dive", price=199.99)

        db.session.add_all([user, course])
        db.session.commit()

        subscription = Subscriptions(
            user_id=user.id,
            course_id=course.id,
            status="confirmed",
            subscription_date=datetime(2024, 1, 1, 12, 0, 0),
            special_requests="None"
        )

        db.session.add(subscription)
        db.session.commit()

        # Act
        results = admin_service.get_all_bookings()

        # Assert
        assert len(results) == 1
        booking = results[0]
        assert booking["user_name"] == "Hayao Miyazaki"
        assert booking["user_email"] == "hayao@example.com"
        assert booking["course_name"] == "Ghibli Storytelling"
        assert booking["status"] == "confirmed"
        assert booking["subscription_date"] == "2024-01-01 12:00:00"

def test_delete_booking_success(admin_service, app):

    with app.app_context():
        # Arrange
        user = User(first_name="Test", second_name="User", email="del@example.com")
        user.set_password("123")
        course = Course(name="Delete Test", description="...", price=50.0)
        db.session.add_all([user, course])
        db.session.commit()

        sub = Subscriptions(user_id=user.id, course_id=course.id, status="confirmed")
        db.session.add(sub)
        db.session.commit()

        # Act
        result = admin_service.delete_booking(sub.id)

        # Assert
        assert result is True
        assert db.session.get(Subscriptions, sub.id) is None


def test_update_booking_status_not_found(admin_service):
    with pytest.raises(RuntimeError) as exc_info:
        admin_service.update_booking_status(9999, "confirmed")
    assert "Error updating booking status" in str(exc_info.value)



def test_update_booking_status_success(admin_service, app):

    with app.app_context():
        # Arrange
        user = User(first_name="Test", second_name="User", email="status@example.com")
        user.set_password("123")
        course = Course(name="Status Course", description="...", price=50.0)
        db.session.add_all([user, course])
        db.session.commit()

        booking = Subscriptions(user_id=user.id, course_id=course.id, status="pending")
        db.session.add(booking)
        db.session.commit()

        # Act
        success = admin_service.update_booking_status(booking.id, "confirmed")

        # Assert
        assert success is True
        assert booking.status == "confirmed"


def test_delete_booking_not_found(admin_service):
    with pytest.raises(RuntimeError) as exc_info:
        admin_service.delete_booking(12345)
    assert "Error deleting booking" in str(exc_info.value)

def test_get_all_course_details(admin_service, app):
    with app.app_context():
        # Arrange
        course = Course(name="Spirited Animation", description="2D Magic", price=250.0)
        module1 = Module(title="Drawing Spirits", description="Concept art and styling")
        module2 = Module(title="Animating Movement", description="Make your spirits move!")

        db.session.add_all([course, module1, module2])
        db.session.commit()

        mapping1 = CourseModule(course_id=course.id, module_id=module1.id)
        mapping2 = CourseModule(course_id=course.id, module_id=module2.id)

        db.session.add_all([mapping1, mapping2])
        db.session.commit()

        # Act
        result = admin_service.get_all_course_details()

        # Assert
        assert len(result) == 1
        course_data = result[0]
        assert course_data["course_name"] == "Spirited Animation"
        assert len(course_data["modules"]) == 2
        module_titles = {m["module_title"] for m in course_data["modules"]}
        assert "Drawing Spirits" in module_titles
        assert "Animating Movement" in module_titles

def test_update_booking_success(admin_service, app):
    with app.app_context():
        user = User(first_name="Edit", second_name="Test", email="edit@example.com")
        user.set_password("test123")
        course = Course(name="Editing Course", description="...", price=100)
        db.session.add_all([user, course])
        db.session.commit()

        booking = Subscriptions(user_id=user.id, course_id=course.id, status="pending", special_requests="Old notes")
        db.session.add(booking)
        db.session.commit()

        # Act
        result = admin_service.update_booking(booking.id, new_status="confirmed", special_requests="New notes")

        # Assert
        assert result is True
        updated = db.session.get(Subscriptions, booking.id)
        assert updated.status == "confirmed"
        assert updated.special_requests == "New notes"


def test_update_booking_not_found(admin_service):
    with pytest.raises(RuntimeError) as e:
        admin_service.update_booking(9999, new_status="confirmed")
    assert "Error updating booking" in str(e.value)

def test_create_course_success(admin_service, app):
    with app.app_context():
        course_id = admin_service.create_course(
            name="Test Course",
            description="Learn movie magic",
            price=99.99
        )

        from app.models import Course
        course = db.session.get(Course, course_id)

        assert course is not None
        assert course.name == "Test Course"
        assert abs(course.price - 99.99) < 1e-6

def test_update_course_success(admin_service, app):
    with app.app_context():
        from app.models import Course

        course = Course(name="Old Name", description="Old Desc", price=10.0)
        db.session.add(course)
        db.session.commit()

        success = admin_service.update_course(
            course.id,
            name="New Name",
            description="Updated Desc",
            price=25.0
        )

        updated = db.session.get(Course, course.id)

        assert success is True
        assert updated.name == "New Name"
        assert updated.description == "Updated Desc"
        assert abs(updated.price - 25.0) < 1e-6

def test_delete_course_success(admin_service, app):
    with app.app_context():
        from app.models import Course, CourseModule, Module

        course = Course(name="To Delete", description="...", price=42.0)
        module = Module(title="Attached", description="Module")
        db.session.add_all([course, module])
        db.session.commit()

        link = CourseModule(course_id=course.id, module_id=module.id)
        db.session.add(link)
        db.session.commit()

        result = admin_service.delete_course(course.id)

        assert result is True
        assert db.session.get(Course, course.id) is None
        assert db.session.query(CourseModule).filter_by(course_id=course.id).count() == 0

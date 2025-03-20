from app.services.admin_service import AdminService
from app.models.models import db, User


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

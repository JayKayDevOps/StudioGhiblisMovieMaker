import pytest
from app.app import app as flask_app  # Ensure correct import
from app.models import db  # Import database models

@pytest.fixture
def app():
    """Flask app configured for testing with an in-memory database."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # ✅ Use in-memory SQLite instead of real DB
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False  # Disable CSRF for easier testing
    })

    with flask_app.app_context():
        db.create_all()  # ✅ Create fresh tables in SQLite memory

    yield flask_app  # Provide app to tests

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()  # ✅ Clean up after tests

@pytest.fixture
def client(app):
    """Flask test client to simulate requests."""
    return app.test_client()

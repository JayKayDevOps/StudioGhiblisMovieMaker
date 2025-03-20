import pytest
from app.app import app as flask_app  # Changed import to use app/app.py directly
from app.models.models import db

@pytest.fixture
def app():
    """Flask app configured for testing with an in-memory database."""
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False
    })

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Flask test client to simulate requests."""
    return app.test_client()

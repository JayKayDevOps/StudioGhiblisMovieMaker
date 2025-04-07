# tests/conftest.py

import pytest
from app import create_app
from app.models import db

@pytest.fixture(scope="function")
def app():
    """Creates a Flask app configured for testing with in-memory DB."""
    app = create_app("testing")

    # Setup without maintaining context
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Yield outside any context
    yield app

    # Cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    """Returns Flask test client for making requests."""
    return app.test_client()


@pytest.fixture()
def runner(app):
    """Returns Flask CLI runner (if you use CLI commands)."""
    return app.test_cli_runner()

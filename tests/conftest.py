# tests/conftest.py

import pytest
from app import create_app
from app.models import db  

@pytest.fixture(scope="session")
def app():
    """Creates a Flask app configured for testing with in-memory DB."""
    app = create_app("testing")

    with app.app_context():
        db.create_all()  # Create tables in-memory before any tests
        yield app
        db.drop_all()    # Clean up after all tests are done


@pytest.fixture()
def client(app):
    """Returns Flask test client for making requests."""
    return app.test_client()


@pytest.fixture()
def runner(app):
    """Returns Flask CLI runner (if you use CLI commands)."""
    return app.test_cli_runner()

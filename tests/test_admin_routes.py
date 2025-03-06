# This file is a place holder for the test cases.
import pytest
from app import create_app
from app import admin_bp
 

def create_app():
    app = create_app("flask_test.cfg")
    app.register_blueprint(admin_bp)
    return app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_admin_dashboard(client):
    response = client.get('/admin')
    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data

def test_admin_bookings(client):
    response = client.get('/admin/bookings')
    assert response.status_code == 200
    assert b"Admin Bookings" in response.data

def test_admin_users(client):
    response = client.get('/admin/users')
    assert response.status_code == 200
    assert b"Admin View Users" in response.data

def test_update_booking_status(client):
    response = client.post('/admin/bookings/1/status')
    assert response.status_code == 200
    assert b"Booking Status Updated for 1" in response.data

def test_delete_booking(client):
    response = client.delete('/admin/bookings/1')
    assert response.status_code == 200
    assert b"Booking 1 Deleted" in response.data


from flask import Blueprint, render_template
from app.services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__)
admin_service = AdminService()  

@admin_bp.route('/admin/login', methods=['GET'])
def admin_login():
    print("Admin Login page")
    return render_template("AdminLogin.html")

@admin_bp.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    print("Admin Dashboard Page")
    return render_template("AdminHome.html")

@admin_bp.route('/admin/bookings')
def admin_bookings():
    """Fetch all course bookings and render the admin bookings page."""
    try:
        bookings = admin_service.get_all_bookings()  # Fetch bookings from the service
        return render_template("admin_bookings.html", bookings=bookings)
    except Exception as e:
        print(f"❌ Error fetching bookings: {e}")
        return render_template("error.html", error_message="Failed to load bookings.")

@admin_bp.route('/admin/users')
def admin_users():
    """Fetch all users and render the admin users page."""
    try:
        users = admin_service.get_all_users()  # Fetch users from the service
        return render_template("admin_users.html", users=users)
    except Exception as e:
        print(f"❌ Error fetching users: {e}")
        return render_template("error.html", error_message="Failed to load users.")

@admin_bp.route('/admin/bookings/<int:booking_id>/status', methods=['POST'])
def update_booking_status(booking_id):
    print(f"Update Booking Status {booking_id}")
    return f"Booking Status Updated for {booking_id}"

@admin_bp.route('/admin/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    print(f"Delete Booking {booking_id}")
    return f"Booking {booking_id} Deleted"
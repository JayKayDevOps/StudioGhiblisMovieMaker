from flask import Blueprint
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    print("Admin Dashboard")
    return "Admin Dashboard"

@admin_bp.route('/admin/bookings')
def admin_bookings():
    print("Admin View Bookings")
    return "Admin Bookings"

@admin_bp.route('/admin/users')
def admin_users():
    print("Admin View Users")
    return "Admin Users"

@admin_bp.route('/admin/bookings/<int:booking_id>/status', methods=['POST'])
def update_booking_status(booking_id):
    print(f"Update Booking Status {booking_id}")
    return f"Booking Status Updated for {booking_id}"

@admin_bp.route('/admin/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    print(f"Delete Booking {booking_id}")
    return f"Booking {booking_id} Deleted"
import logging
from flask import Blueprint, render_template, request, render_template, redirect, url_for
from app.services.admin_service import AdminService
from models import User
from services.admin_service import AdminService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Ensure logs are sent to stdout for CloudWatch
    ]
)
logger = logging.getLogger(__name__)

# Define Blueprint
admin_bp = Blueprint('admin', __name__)
admin_service = AdminService()  

@admin_bp.route('/admin/login', methods=['GET'])
def admin_login():
    print("Admin Login page")
    return render_template("AdminLogin.html")

@admin_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_dashboard():
    """Handle admin login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate form inputs
        if not email or not password:
            logger.warning("Login attempt with missing email or password.")
            return render_template("AdminLogin.html", error="Email and password are required.")

        try:
            # Query the database for an admin user
            admin = User.query.filter_by(email=email, role='admin').first()

            # Validate password
            if admin and admin.check_password(password):
                logger.info(f"Admin login successful for email: {email}")
                return redirect(url_for('admin.admin_home'))
            else:
                logger.warning(f"Login attempt failed for email: {email}")
                return render_template("AdminLogin.html", error="Invalid email or password.")
        except Exception as e:
            logger.error(f"Error during login process: {e}", exc_info=True)
            return render_template("error.html", error_message="Unexpected error occurred during login.")

    return render_template("AdminLogin.html")


@admin_bp.route('/admin/home', methods=['GET'])
def admin_home():
    """Render the admin home page."""
    logger.info("Rendering admin home page.")
    return render_template("AdminHome.html")


@admin_bp.route('/admin/bookings', methods=['GET'])
def admin_bookings():
    """Fetch and render all course bookings."""
    try:
        admin_service = AdminService()
        bookings = admin_service.get_all_bookings()
        if not bookings:
            logger.warning("No bookings found.")
            return render_template("AdminBookings.html", bookings=[])
        logger.info(f"Successfully fetched {len(bookings)} bookings.")
        return render_template("AdminBookings.html", bookings=bookings)
    except Exception as e:
        logger.error(f"Error fetching bookings: {e}", exc_info=True)
        return render_template("error.html", error_message="Failed to load bookings.")


@admin_bp.route('/admin/users', methods=['GET'])
def admin_users():
    """Fetch and render all users."""
    try:
        admin_service = AdminService()
        users = admin_service.get_all_users()
        if not users:
            logger.warning("No users found.")
            return render_template("AdminUsers.html", users=[])
        logger.info(f"Successfully fetched {len(users)} users.")
        return render_template("AdminUsers.html", users=users)
    except Exception as e:
        logger.error(f"Error fetching users: {e}", exc_info=True)
        return render_template("error.html", error_message="Failed to load users.")


@admin_bp.route('/admin/courses', methods=['GET'])
def list_courses():
    """Fetch and render all courses."""
    try:
        admin_service = AdminService()
        courses = admin_service.get_all_course_details()
        if not courses:
            logger.warning("No courses found.")
            return render_template("AdminCourseList.html", courses=[])
        logger.info(f"Successfully fetched {len(courses)} courses.")
        return render_template("AdminCourseList.html", courses=courses)
    except Exception as e:
        logger.error(f"Error fetching courses: {e}", exc_info=True)
        return render_template("error.html", error_message="Failed to load courses.")


@admin_bp.route('/admin/bookings/<int:booking_id>/status', methods=['POST'])
def update_booking_status(booking_id):
    """Update the status of a booking."""
    try:
        new_status = request.form.get('status')
        logger.info(f"Updating booking status for ID: {booking_id} to {new_status}")
        # Add logic to update the booking's status
        return f"Booking status updated for ID {booking_id}."
    except Exception as e:
        logger.error(f"Failed to update booking status for ID {booking_id}: {e}", exc_info=True)
        return f"Failed to update booking status for ID {booking_id}.", 500


@admin_bp.route('/admin/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """Delete a booking by its ID."""
    try:
        logger.info(f"Deleting booking with ID: {booking_id}")
        # Add logic to delete the booking
        return f"Booking {booking_id} deleted successfully."
    except Exception as e:
        logger.error(f"Failed to delete booking with ID {booking_id}: {e}", exc_info=True)
        return f"Failed to delete booking {booking_id}.", 500
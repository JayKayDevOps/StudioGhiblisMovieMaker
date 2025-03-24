import logging
from flask import Blueprint, render_template, request, render_template, redirect, url_for
from app.services.admin_service import AdminService
from app.models import User 
from app.services.admin_service import AdminService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Ensure logs are sent to stdout for CloudWatch
    ]
)
logger = logging.getLogger(__name__)

error_template = "error.html"
not_implemented = NotImplementedError("Implement this logic")

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
            return render_template(error_template, error_message="Unexpected error occurred during login.")

    return render_template("AdminLogin.html")


@admin_bp.route('/admin/home', methods=['GET'])
def admin_home():
    """Render the admin home page."""
    logger.info("Rendering admin home page.")
    return render_template("AdminHome.html")


@admin_bp.route('/admin/bookings', methods=['GET'])
def admin_get_all_bookings():
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
        return render_template(error_template, error_message="Failed to load bookings.")


@admin_bp.route('/admin/users', methods=['GET'])
def admin_get_all_users():
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
        return render_template(error_template, error_message="Failed to load users.")


@admin_bp.route('/admin/courses', methods=['GET'])
def admin_get_all_courses():
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
        return render_template(error_template, error_message="Failed to load courses.")


@admin_bp.route('/admin/bookings/<int:booking_id>/status', methods=['POST'])
def update_booking_status(booking_id):
    """Update the status of a booking."""
    try:
        new_status = request.form.get('status')
        logger.info(f"Updating booking status for ID: {booking_id} to {new_status}")
        admin_service.update_booking_status(booking_id, new_status=new_status)
        return f"Booking status updated for ID {booking_id}."
    except Exception as e:
        logger.error(f"Failed to update booking status for ID {booking_id}: {e}", exc_info=True)
        return render_template(error_template, error_message="Failed to update booking status.")

@admin_bp.route('/admin/bookings/<int:booking_id>', methods=['PATCH'])
def update_booking(booking_id):
    """Update a booking by its ID."""
    try:
        logger.info(f"Updating booking with ID: {booking_id}")
        updated_booking = request.form.get('booking')
        admin_service.update_booking(booking_id, updated_booking)
        # Add logic to update the booking
        return f"Booking {booking_id} updated successfully."
    except Exception as e:
        logger.error(f"Failed to update booking with ID {booking_id}: {e}", exc_info=True)
        return render_template(error_template, error_message="Failed to load bookings"), 500

@admin_bp.route('/admin/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    """Delete a booking by its ID."""
    raise not_implemented
    try:
        logger.info(f"Deleting booking with ID: {booking_id}")
        # Add logic to delete the booking
        return f"Booking {booking_id} deleted successfully."
    except Exception as e:
        logger.error(f"Failed to delete booking with ID {booking_id}: {e}", exc_info=True)
        return render_template(error_template, error_message="Failed to delete booking"), 500


# Create a new course
@admin_bp.route('/admin/courses', methods=['POST'])
def create_course():
    try:
        data = request.form
        name = data.get("name")
        description = data.get("description")
        price = float(data.get("price"))

        course_id = admin_service.create_course(name, description, price)

        raise not_implemented
        return f"Course created with ID {course_id}", 201

    except Exception as e:
        logger.error(f"Failed to create course: {e}", exc_info=True)
        return render_template(error_template, error_message="Failed to create course"), 500


@admin_bp.route('/admin/courses/<int:course_id>', methods=['PATCH'])
def update_course(course_id):
    try:
        data = request.form
        name = data.get("name")
        description = data.get("description")
        price = data.get("price")

        result = admin_service.update_course(course_id, name, description, float(price) if price else None)

        if result:
            raise not_implemented
            return f"Course {course_id} updated successfully", 200
        else:
            logger.error(f"Course {course_id} not found")
            return render_template(error_template, error_message="Course not found"), 404

    except Exception as e:
        logger.error(f"Failed to update course {course_id}: {e}", exc_info=True)
        return render_template(error_template, error_message="Failed to update course"), 500

# Delete course
@admin_bp.route('/admin/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        result = admin_service.delete_course(course_id)
        if result:
            raise not_implemented
            return f"Course {course_id} deleted successfully", 200
        else:
            logger.error(f"Course {course_id} not found")
            return render_template(error_template, error_message="Course not found"), 404

    except Exception as e:
        logger.error(f"Failed to delete course {course_id}: {e}", exc_info=True)
        return render_template(error_template, error_message="Failed to delete course"), 500
import logging
from app.models import db, Subscriptions, User, Course
from app.services.user_service import UserService
from flask import Blueprint, render_template, request, redirect, url_for


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
user_service = UserService()
user_id = 1 # mocked for now 

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():
    raise not_implemented

@user_bp.route('/book-course/<int:course_id>', methods=['POST'])
def book_course():
    try:
        course_id = int(request.form.get('course_id'))
        success = user_service.book_course(user_id, course_id)
        if success:
            raise not_implemented
            return f"✅ Course {course_id} successfully booked"
        else:
            return f"⚠️ You’ve already booked Course {course_id}"

    except Exception as e:
        logger.error(f"❌ Error booking course: {e}", exc_info=True)
        return render_template(error_template, error_message="Failed to book course."), 500

@user_bp.route('/my-courses')
def my_courses():
    try:
        bookings = user_service.get_user_bookings(user_id)
        course_names = ", ".join([b["course_name"] for b in bookings])
        raise not_implemented

    except Exception as e:
        logger.error(f"❌ Error fetching user courses: {e}", exc_info=True)
        return "❌ Failed to retrieve your courses", 500

@user_bp.route('/logout')
def logout():
    raise not_implemented

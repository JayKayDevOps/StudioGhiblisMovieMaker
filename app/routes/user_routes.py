from app.models import db, Subscription, User, Course

from flask import Blueprint
user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():
    print("User Dashboard")
    return "User Dashboard"

@user_bp.route('/book-course/<int:course_id>', methods=['GET', 'POST'])
def book_course(course_id):
    print(f"Book Course {course_id}")
    return f"Book Course {course_id}"

@user_bp.route('/logout')
def logout():
    print("Logout")
    return "Logged out"

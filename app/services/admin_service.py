# This module contains the service layer for admin-related database operations.
import logging
from app.models import db, Subscriptions, User, Course, CourseModule, Module
from sqlalchemy.orm import joinedload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AdminService:
    """Service layer for admin-related database operations."""

    def __init__(self, db_session=None):
        """Allow injecting a mock database session for testing."""
        self.db_session = db_session or db.session

    def get_all_bookings(self):
        """Fetch all course bookings with user and course details."""
        print("Getting bookings from the database...")
        logger.info("Fetching all bookings from the database...")
        try:
            bookings = db.session.query(
                Subscriptions.id,
                User.first_name,
                User.second_name,
                User.email,
                Course.name.label("course_name"),

                Subscriptions.status,
                Subscriptions.subscription_date
            ).join(User, Subscriptions.user_id == User.id)\
             .join(Course, Subscriptions.course_id == Course.id)\
             .all()

            logger.debug(f"Fetched bookings: {bookings}")
            

            return [
                {
                    "booking_id": b.id,
                    "user_name": f"{b.first_name} {b.second_name}",
                    "user_email": b.email,
                    "course_name": b.course_name,
                    "status": b.status,
                    "subscription_date": b.subscription_date.strftime("%Y-%m-%d %H:%M:%S")
                }
                for b in bookings
            ]
        except Exception as e:
            logger.error("Failed to fetch bookings", exc_info=True)
            raise RuntimeError("Error fetching bookings from the database.") from e

    def get_all_users(self):
        """Fetch all users for the admin panel."""
        logger.info("Fetching all users from the database...")
        try:
            users = db.session.query(
                User.id,
                User.first_name,
                User.second_name,
                User.email,
                User.role
            ).all()

            logger.debug(f"Fetched users: {users}")
            
            # Convert query results to a list of dictionaries
            return [
                {
                    "user_id": u.id,
                    "full_name": f"{u.first_name} {u.second_name}",
                    "email": u.email,
                    "role": u.role
                }
                for u in users
            ]
        except Exception as e:
            logger.error("Failed to fetch users", exc_info=True)
            raise RuntimeError("Error fetching users from the database.") from e

    def get_all_course_details(self):
        """Fetch all courses along with their associated modules."""
        logger.info("Fetching all course details from the database...")
        try:
            # Query all courses, eagerly loading their modules and module details
            courses = db.session.query(Course).options(
                joinedload(Course.modules).joinedload(CourseModule.module)
            ).all()

            # Structure the result as a list of dictionaries for easier consumption
            course_details = [
                {
                    "course_id": course.id,
                    "course_name": course.name,
                    "course_description": course.description,
                    "course_price": course.price,
                    "modules": [
                        {
                            "module_id": module.module.id,
                            "module_title": module.module.title,
                            "module_description": module.module.description
                        }
                        for module in course.modules
                    ]
                }
                for course in courses
            ]

            logger.info(f"Successfully fetched details for {len(course_details)} courses.")
            return course_details
        except Exception as e:
            logger.error("Failed to fetch course details", exc_info=True)
            raise RuntimeError("Error fetching course details from the database.") from e

    def update_booking_status(self, booking_id, new_status):
        """Update the status of a booking."""
        logger.info(f"Updating booking status for ID: {booking_id} to {new_status}...")
        try:
            booking = self.db_session.get(Subscriptions, booking_id)
            if not booking:
                logger.warning(f"No booking found with ID {booking_id}.")
                raise ValueError(f"No booking found for ID: {booking_id}")

            booking.status = new_status
            self.db_session.commit()
            logger.info(f"Booking status updated successfully for ID: {booking_id}.")
            return True
        except Exception as e:
            logger.error("Failed to update booking status", exc_info=True)
            raise RuntimeError("Error updating booking status.") from e

    def delete_booking(self, booking_id):
        """Delete a booking by its ID."""
        logger.info(f"Deleting booking with ID: {booking_id}...")
        try:
            booking = self.db_session.get(Subscriptions, booking_id)
            if not booking:
                logger.warning(f"No booking found with ID {booking_id}.")
                raise ValueError(f"No booking found for ID: {booking_id}")

            self.db_session.delete(booking)
            self.db_session.commit()
            logger.info(f"Booking deleted successfully for ID: {booking_id}.")
            return True
        except Exception as e:
            logger.error("Failed to delete booking", exc_info=True)
            raise RuntimeError("Error deleting booking.") from e






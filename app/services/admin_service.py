# This module contains the service layer for admin-related database operations.
import logging
from app.models import db, Subscriptions, User, Course, CourseModule, Module
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

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
            # Use self.db_session instead of db.session
            bookings = self.db_session.query(
                Subscriptions.id,
                User.first_name,
                User.second_name,
                User.email,
                Course.name.label("course_name"),
                Subscriptions.status,
                Subscriptions.subscription_date
            ).join(User, Subscriptions.user_id == User.id) \
                .join(Course, Subscriptions.course_id == Course.id) \
                .all()

            # Log count instead of full data to avoid exposing sensitive information
            logger.debug(f"Fetched {len(bookings)} bookings")

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
            self.db_session.rollback()  # Add rollback
            logger.error("Failed to fetch bookings", exc_info=True)
            raise RuntimeError("Error fetching bookings from the database.") from e

    def get_all_users(self):
        """Fetch all users for the admin panel."""
        logger.info("Fetching all users from the database...")
        try:
            # Use self.db_session instead of db.session
            users = self.db_session.query(
                User.id,
                User.first_name,
                User.second_name,
                User.email,
                User.role
            ).filter(User.role!='admin').all()

            # Log count instead of full data to avoid exposing sensitive information
            logger.debug(f"Fetched {len(users)} users")

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
            self.db_session.rollback()  # Add rollback
            logger.error("Failed to fetch users", exc_info=True)
            raise RuntimeError("Error fetching users from the database.") from e

    def get_all_course_details(self):
        """Fetch all courses along with their associated modules."""
        logger.info("Fetching all course details from the database...")
        try:
            # Use self.db_session instead of db.session
            # Query all courses, eagerly loading their modules and module details
            courses = self.db_session.query(Course).options(
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
            self.db_session.rollback()  # Add rollback
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
        except ValueError as ve:
            # Re-raise ValueError without rolling back
            raise
        except Exception as e:
            self.db_session.rollback()  # Add rollback
            logger.error("Failed to update booking status", exc_info=True)
            raise RuntimeError("Error updating booking status.") from e

    def delete_booking(self, booking_id):
        """Delete a booking by its ID."""
        try:
            # Fetch the booking
            booking = self.get_booking(booking_id)

            if not booking:
                logger.warning(f"Booking with ID {booking_id} not found.")
                raise ValueError(f"Booking with ID {booking_id} not found.")

            # Use session.in_transaction() instead of is_active
            # Reattach the booking if necessary (use proper session state check)
            booking = self.db_session.merge(booking)

            # Delete the booking
            self.db_session.delete(booking)
            self.db_session.commit()

            # Optional: Log success
            logger.info(f"Successfully deleted booking with ID: {booking_id}")
            return True
        except ValueError as e:
            # Handle case where booking is not found
            logger.warning(str(e))
            raise
        except Exception as e:
            # Handle unexpected errors
            self.db_session.rollback()  # Ensure rollback happens
            logger.error("Failed to delete booking", exc_info=True)
            raise RuntimeError("Error deleting booking.") from e

    def get_booking(self, booking_id):
        """Fetch a booking by its ID."""
        return self.db_session.get(Subscriptions, booking_id)


    def update_booking(self, booking_id, **kwargs,):
        """Update a booking by its ID."""
        try:
            # Fetch the booking by ID
            booking = self.get_booking(booking_id)

            # Handle case where booking does not exist
            if not booking:
                logger.warning(f"Booking with ID {booking_id} not found.")
                raise ValueError(f"Booking with ID {booking_id} not found.")

            # Use session.merge() instead of checking is_active
            booking = self.db_session.merge(booking)

            # Update booking attributes
            for key, value in kwargs.items():
                if hasattr(booking, key):
                    setattr(booking, key, value)
                else:
                    logger.warning(f"Attribute '{key}' does not exist on booking and was ignored.")

            # Commit changes to the database
            self.db_session.commit()

            # Log success
            logger.info(f"Successfully updated booking with ID {booking_id}.")
            return booking

        except ValueError as ve:
            # Handle cases where the booking is not found
            logger.error(str(ve))
            raise
        except Exception as e:
            # Rollback session on unexpected errors
            self.db_session.rollback()
            logger.error("Failed to update booking", exc_info=True)
            raise RuntimeError("Error updating booking.") from e

    def create_course(self, name, description, price):
        """Create a new course."""
        logger.info(f"Creating course: {name}")
        try:
            course = Course(name=name, description=description, price=price)
            self.db_session.add(course)
            self.db_session.commit()
            logger.info(f"Course '{name}' created with ID: {course.id}")
            return course.id
        except Exception as e:
            self.db_session.rollback()  # Add rollback
            logger.error("Failed to create course", exc_info=True)
            raise RuntimeError("Error creating course.") from e

    def update_course(self, course_id, name=None, description=None, price=None):
        """Update course details."""
        logger.info(f"Updating course ID {course_id}")
        try:
            course = self.db_session.get(Course, course_id)
            if not course:
                raise ValueError("Course not found.")

            # Use session.merge() instead of checking is_active
            course = self.db_session.merge(course)

            # Update course attributes
            if name:
                course.name = name
            if description:
                course.description = description
            if price is not None:
                course.price = price

            self.db_session.commit()
            return True
        except ValueError as ve:
            # Re-raise ValueError without rolling back
            raise
        except Exception as e:
            self.db_session.rollback()  # Add rollback
            logger.error("Failed to update course", exc_info=True)
            raise RuntimeError("Error updating course.") from e

    def delete_course(self, course_id):
        """Delete a course and its module mappings."""
        logger.info(f"Deleting course ID {course_id}")
        try:
            course = self.db_session.get(Course, course_id)
            if not course:
                raise ValueError("Course not found.")

            # Use session.merge() instead of checking is_active
            course = self.db_session.merge(course)

            # Check for existing subscriptions
            subscriptions = self.db_session.query(Subscriptions).filter_by(course_id=course_id).first()
            if subscriptions:
                logger.warning(f"Cannot delete course ID {course_id} as it has active subscriptions")
                raise ValueError("Cannot delete course with active subscriptions")

            # Delete CourseModule mappings first
            self.db_session.query(CourseModule).filter_by(course_id=course_id).delete()

            # Delete the course
            self.db_session.delete(course)
            self.db_session.commit()
            logger.info(f"Successfully deleted course ID {course_id}")
            return True

        except ValueError as ve:
            # Handle cases where the course is not found
            logger.warning(f"Course with ID {course_id} not found: {ve}")
            raise

        except Exception as e:
            # Rollback session on unexpected errors
            self.db_session.rollback()
            logger.error("Failed to delete course", exc_info=True)
            raise RuntimeError("Error deleting course.") from e

    def get_existing_course(self):
        """
        Check if a course already exists in the database.
        :return: The existing course if found, otherwise None.
        """
        try:
            # Use self.db_session instead of direct query
            existing_course = self.db_session.query(Course).first()
            return existing_course  # Returns the first course found, or None if no courses exist
        except Exception as e:
            # Log the error and re-raise it for debugging purposes
            self.db_session.rollback()  # Add rollback
            logger.error(f"An error occurred while checking for existing courses: {e}")
            return None

    def add_course(self, course_data):
        """
        Add a new course to the database.

        :param course_data: Dictionary with course details (e.g., name, description, price).
        :return: The created course ID if successful, None otherwise.
        """
        try:
            logger.info("Starting to add a new course.")

            # Add the course
            new_course = Course(
                name=course_data['name'],
                description=course_data.get('description'),
                price=course_data['price']
            )
            self.db_session.add(new_course)
            self.db_session.flush()  # Generate the course ID
            logger.info(f"Course added: ID={new_course.id}, Name={new_course.name}")

            # Commit the course
            self.db_session.commit()
            logger.info("Course committed successfully.")
            return new_course.id

        except Exception as e:
            logger.error(f"Error occurred while adding course: {str(e)}", exc_info=True)
            self.db_session.rollback()
            logger.info("Database changes rolled back.")
            return None

    def add_modules_to_course(self, course_id, module_data):
        """
        Add modules to an existing course.

        :param course_id: The ID of the course to which modules are being added.
        :param module_data: List of dictionaries containing module details (e.g., title, description).
        :return: True if the operation was successful, False otherwise.
        """
        try:
            logger.info(f"Starting to add modules to course ID: {course_id}")

            # Check if the course exists - use self.db_session
            course = self.db_session.query(Course).get(course_id)
            if not course:
                logger.warning(f"Course with ID={course_id} not found.")
                return False

            # Add each module and create CourseModule mappings
            for module in module_data:
                new_module = Module(
                    title=module['title'],
                    description=module.get('description')
                )
                self.db_session.add(new_module)
                self.db_session.flush()  # Generate the module ID
                logger.info(f"Module added: ID={new_module.id}, Title={new_module.title}")

                # Create CourseModule mapping
                course_module_mapping = CourseModule(course_id=course_id, module_id=new_module.id)
                self.db_session.add(course_module_mapping)
                logger.info(f"CourseModule mapping created: CourseID={course_id}, ModuleID={new_module.id}")

            # Commit all changes
            self.db_session.commit()
            logger.info("Modules committed successfully.")
            return True

        except Exception as e:
            logger.error(f"Error occurred while adding modules: {str(e)}", exc_info=True)
            self.db_session.rollback()
            logger.info("Database changes rolled back.")
            return False

    def get_bookings_by_course(self, course_id):
        """
        Fetch bookings for a specific course with user and course details.

        :param course_id: ID of the course to filter bookings by.
        :return: List of bookings for the specified course.
        """
        print(f"Getting bookings for Course ID {course_id}...")
        logger.info(f"Fetching bookings for Course ID {course_id} from the database...")

        try:
            # Use self.db_session instead of db.session
            bookings = self.db_session.query(
                Subscriptions.id,
                User.first_name,
                User.second_name,
                User.email,
                Course.name.label("course_name"),
                Subscriptions.status,
                Subscriptions.subscription_date
            ).join(User, Subscriptions.user_id == User.id) \
                .join(Course, Subscriptions.course_id == Course.id) \
                .filter(Subscriptions.course_id == course_id) \
                .all()

            # Log count instead of full data
            logger.debug(f"Fetched {len(bookings)} bookings for Course ID {course_id}")

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
            self.db_session.rollback()  # Add rollback
            logger.error(f"Failed to fetch bookings for Course ID {course_id}", exc_info=True)
            raise RuntimeError(f"Error fetching bookings for Course ID {course_id} from the database.") from e

    def get_all_courses(self):
        """
        Fetch all courses from the database, sorted by course ID (highest first).
        Returns a list of course dictionaries.
        """
        try:
            # Use self.db_session instead of direct query
            courses = self.db_session.query(Course).order_by(Course.id.desc()).all()

            # Return as a list of dictionaries
            return [{'id': course.id, 'name': course.name} for course in courses]

        except SQLAlchemyError as e:
            self.db_session.rollback()  # Add rollback
            logger.error(f"Database error while fetching courses: {e}", exc_info=True)
            return []
        except Exception as e:
            self.db_session.rollback()  # Add rollback
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return []

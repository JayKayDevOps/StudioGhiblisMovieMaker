
import logging
from app.models import db, Subscriptions, User, Course, CourseModule, Module
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UserService:
    def get_user_bookings(self, user_id):
        """Fetch all bookings made by a specific user."""
        try:
            bookings = db.session.query(
                Subscriptions.id,
                Course.name.label("course_name"),
                Subscriptions.status,
                Subscriptions.subscription_date
            ).join(Course, Subscriptions.course_id == Course.id)\
             .filter(Subscriptions.user_id == user_id)\
             .all()

            return [
                {
                    "booking_id": b.id,
                    "course_name": b.course_name,
                    "status": b.status,
                    "subscription_date": b.subscription_date.strftime("%Y-%m-%d %H:%M:%S")
                }
                for b in bookings
            ]
        except Exception as e:
            print(f"❌ Error fetching user bookings: {e}")
            return []

    def book_course(self, user_id, course_id, special_requests=None):
        """Create a course subscription for a user."""
        try:
            # Prevent duplicate booking
            existing = db.session.query(Subscriptions).filter_by(
                user_id=user_id, course_id=course_id
            ).first()
            if existing:
                return False  # Already booked

            booking = Subscriptions(
                user_id=user_id,
                course_id=course_id,
                special_requests=special_requests or "",
                status="pending"
            )
            db.session.add(booking)
            db.session.commit()
            return True
        except Exception as e:
            print(f"❌ Error booking course: {e}")
            return False

    def __init__(self, db_session=None):
        """Allow injecting a mock database session for testing."""
        self.db_session = db_session or db.session

    def get_all_bookings(self, user_id):
        if not user_id or not isinstance(user_id, int):
            logger.error(f"Invalid user_id provided: {user_id}")
            return []  # Return an empty list if user_id is not valid

        """Fetch all course bookings with user and course details."""
        logger.info(f"Fetching bookings for user_id: {user_id} from the database...")
        try:
            # Query subscriptions, joining with User and Course tables
            bookings = db.session.query(
                Subscriptions.id,
                User.first_name,
                User.second_name,
                User.email,
                Course.name.label("course_name"),
                Course.description,
                Course.price,
                Subscriptions.special_requests,
                Subscriptions.status,
                Subscriptions.subscription_date
            ).join(User, Subscriptions.user_id == User.id)\
             .join(Course, Subscriptions.course_id == Course.id)\
             .filter(Subscriptions.user_id == user_id)\
             .all()

            if not bookings:
                logger.info(f"No bookings found for user_id: {user_id}")
                return []

            logger.debug(f"Fetched bookings: {bookings}")
            
            # Convert results to a list of dictionaries
            return [
                {   
                    "user_name": f"{b.first_name} {b.second_name}",
                    "User.first_name": b.first_name,
                    "User.second_name,": b.second_name,
                    "user_email": b.email,
                    "course_name": b.course_name,
                    "booking_id": b.id,
                    "status": b.status,
                    "subscription_date": b.subscription_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "Subscriptions.special_requests": b.special_requests,
                    "Course.price": b.price
                }
                for b in bookings
            ]
        except Exception as e:
            logger.error("Failed to fetch bookings", exc_info=True)
            raise RuntimeError("Unable to fetch your bookings due to a database error. Please try again later.") from e
   



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

 
    
    def get_user_data(self, user_id):
        """Fetch user data using the provided user ID."""
        if not user_id:
            logger.error("Invalid user ID provided.")
            return None

        logger.info(f"Fetching data for user ID: {user_id}")
        try:
            # Fetch user data from the database
            user = db.session.query(User).filter_by(id=user_id).first()
            
            if not user:
                logger.warning(f"No data found for user ID: {user_id}")
                return None
            
            logger.debug(f"Fetched user data: {user}")
            return user
        except Exception as e:
            logger.error("Error fetching user data from the database", exc_info=True)
            raise RuntimeError("Error fetching user data.") from e
        
    

    def update_user(self, user_id, **kwargs):
        """
        Update a user's details.
        :param user_id: The ID of the user to update.
        :param kwargs: The fields to update (e.g., first_name, email).
        :return: Tuple (success: bool, message: str)
        """
        try:
            # Fetch the user from the database
            user = self.db_session.query(User).filter_by(id=user_id).first()
            if not user:
                logger.error(f"User with ID {user_id} not found.")
                return False, "User not found."

            # Update fields dynamically
            for key, value in kwargs.items():
                if key is 'password':
                    user.set_password(value)
                else:
                    if hasattr(user, key) and key != 'id':  # Prevent updating 'id'
                        setattr(user, key, value)

            # Commit the changes
            self.db_session.commit()
            logger.info(f"User with ID {user_id} updated successfully.")
            return True, "User updated successfully."
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"An error occurred while updating user with ID {user_id}: {e}", exc_info=True)
            return False, "An unexpected error occurred."
    
    def create_user(self, password, **kwargs):
        """
        Create a new user.
        :param password: Raw password to be hashed using set_password().
        :param kwargs: Other user fields (e.g., first_name, email).
        :return: Tuple (success: bool, message: str)
        """
        try:
            # Create a new user instance
            user = User()
            for key, value in kwargs.items():
                if hasattr(user, key) and key != 'id':  # Prevent updating 'id'
                    setattr(user, key, value)

            user.set_password(password)  # Use the model's set_password() method

            # Add the new user to the database
            db.session.add(user)
            db.session.commit()
            logger.info(f"User {user.first_name} {user.second_name} created successfully.")
            return True, "User created successfully."
        except IntegrityError as e:
            self.db_session.rollback()
            logger.error(f"Integrity Error: {e}")
            return False, "Email must be unique."
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"An error occurred while creating a new user: {e}", exc_info=True)
            return False, "An unexpected error occurred."
        

    def update_password(self, user_id, new_password):
        """
        Update a user's password.
        :param user_id: The ID of the user whose password is being updated.
        :param new_password: The new password to set.
        :return: Tuple (success: bool, message: str)
        """
        try:
            # Fetch the user from the database
            user = self.db_session.query(User).filter_by(id=user_id).first()
            if not user:
                logger.error(f"User with ID {user_id} not found.")
                return False, "User not found."

            # Hash and set the new password
            user.set_password(new_password)
            self.db_session.commit()
            logger.info(f"Password for user with ID {user_id} updated successfully.")
            return True, "Password updated successfully."

        except Exception as e:
            self.db_session.rollback()
            logger.error(f"An error occurred while updating password for user with ID {user_id}: {e}", exc_info=True)
            return False, "An unexpected error occurred."        
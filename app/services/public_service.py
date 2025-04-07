import logging
from app.models import db, Subscriptions, User, Course, CourseModule, Module
from sqlalchemy.orm import joinedload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PublicService:
    """Service layer for public-related database operations."""

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







import logging
from flask import Blueprint, request, render_template
from app.models import Course
from app.services.public_service import PublicService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Ensure logs are sent to stdout for CloudWatch
    ]
)
logger = logging.getLogger(__name__)

public_bp = Blueprint('public', __name__)

@public_bp.route('/home', methods=['GET'])
def home():
    """Render the homepage."""
    logger.info("Rendering homepage.")
    return render_template("Homepage.html")  # Render the template


@public_bp.route('/search', methods=['GET', 'POST'])
def search_courses():
    """Search for courses based on user input."""
    results = None  # Default to None to indicate no search performed yet

    if request.method == 'GET':
        # Retrieve search parameters from the form
        name = request.args.get('name')
        price = request.args.get('price')
        keywords = request.args.get('query')

        # Build the query dynamically only if at least one parameter exists
        if name or price or keywords:
            query = Course.query
            if name:
                query = query.filter(Course.name.ilike(f"%{name}%"))
            if price:
                query = query.filter(Course.price.ilike(f"%{price}%"))
            if keywords:
                query = query.filter(
                    (Course.name.ilike(f"%{keywords}%")) |
                    (Course.description.ilike(f"%{keywords}%"))
                )

            # Execute query and fetch results
            try:
                results = query.all()  # Only fetch results if conditions exist
                logger.info(f"Search results fetched successfully: {len(results)} results found.")
            except Exception as e:
                logger.error(f"Error fetching search results: {e}", exc_info=True)
                results = []

    # Pass search parameters to the template
    return render_template('Search.html', results=results, name=name, price=price, query=keywords)



@public_bp.route('/courses', methods=['GET'])
def list_courses():
    """Fetch and render all courses."""
    try:
        public_service = PublicService()
        courses = public_service.get_all_course_details()
        if not courses:
            logger.warning("No courses found.")
            return render_template("CourseList.html", courses=[])
        logger.info(f"Successfully fetched {len(courses)} courses.")
        return render_template("CourseList.html", courses=courses)
    except Exception as e:
        logger.error(f"Error fetching courses: {e}", exc_info=True)
        return render_template("error.html", error_message="Failed to load courses.")



@public_bp.route('/courses/<int:course_id>', methods=['GET'])
def course_detail(course_id):
    """Display details for a specific course."""
    logger.info(f"Fetching details for course ID: {course_id}")
    # You can fetch course details by ID here
    return f"Course Detail for {course_id}"



@public_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Render register page or handle user registration."""
    logger.info("Rendering register page or handling registration form submission.")
    return render_template("Homepage.html")

@public_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Render """
    logger.info("Rendering .")
    return render_template("Homepage.html")

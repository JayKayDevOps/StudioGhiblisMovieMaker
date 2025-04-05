import logging
from app.models import db, Subscriptions, User, Course
from app.services.user_service import UserService
from flask import Blueprint, request, render_template, redirect, url_for, flash ,session
from flask_login import login_user, logout_user, current_user

from app.utils.decorators import role_required


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

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate form inputs
        if not email or not password:
            logger.warning("Login attempt with missing email or password.")
            return render_template("UserLogin.html", error="Email and password are required.")

        try:
            # Query the database for a user
            print('email: ', email)
            print('password: ', password)
            print('\n\n')
            user = User.query.filter_by(email=email).first()
            print(user)


            # Validate password
            if user and user.check_password(password):
                # Use Flask-Login's login_user instead of session
                login_user(user)

                logger.info(f"User login successful for email: {email}")

                # Redirect based on role
                if user.role == 'admin':
                    return redirect(url_for('admin.admin_home'))

                else:
                    # Default for users with no specific role
                    return redirect(url_for('user.view_bookings'))
            else:
                logger.warning(f"Login attempt failed for email: {email}")
                return render_template("UserLogin.html", error="Invalid email or password.")
        except Exception as e:
            logger.error(f"Error during login process: {e}", exc_info=True)
            print('rendering error template:')
            return render_template("error.html", error_message="Unexpected error occurred during login.")

    return render_template("UserLogin.html")


@user_bp.route('/booking', methods=['GET', 'POST'])
@role_required('customer')
def booking():
    course = None
    user_service = UserService()  

    if request.method == 'GET':
        # Handle GET request for course_id or course_name
        course_id = request.args.get('course_id')
        course_name = request.args.get('course_name')
        print(course)  # Check if course.id exists

        if course_id:
            # Query the course by course_id
            course = Course.query.get(course_id)
        elif course_name:
            # Query the course by course_name
            course = Course.query.filter_by(name=course_name).first()
        else:
            # Neither course_id nor course_name provided
            return render_template("error.html", error_message="No course information provided. Please try again.")

        if not course:
            # Handle case where course is not found
            return render_template("error.html", error_message="Course not found. Please try again.")

        # Render the booking confirmation page with the found course
        return render_template("BookingConfirmation.html", course=course, course_id=course.id)
    

    elif request.method == 'POST':
        # Retrieve course_id from the form data
        course_id = request.form.get('course_id')
        course = Course.query.get(course_id) if course_id else None

        # Handle POST request for user login
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Login successful, store user ID in session
            session['user_id'] = user.id  # Store user ID in the session
             # Call the service to book the course
            special_requests = request.form.get('special_requests', None)
            booking_successful = user_service.book_course(
                user_id=user.id,
                course_id=course_id,
                special_requests=special_requests
            )

            if booking_successful:
                flash('Success! Booking confirmed. Go to your profile page to see details.', 'success')
                booking_confirmation = True
            else:
                flash('This course is already booked.', 'error')
        else:
            # Login failed
            flash('Invalid credentials. Please try again.', 'error')

    # Redirect to the user's bookings page
    return redirect(url_for('user.view_bookings'))

  


@user_bp.route('/book_course/<int:course_id>', methods=['GET', 'POST'])
@role_required('customer')
def booking_confirmation(course_id):
    if request.method == 'GET':
        course = Course.query.get(course_id)  # Fetch the course from the database
    if not course:
        flash('Course not found!', 'error')
        return redirect(url_for('public.search'))  # Redirect if the course is invalid
    return render_template('BookingConfirmation.html', course=course)

@user_bp.route('/register', methods=['GET', 'POST'])
@role_required('customer')
def register():
    """
    Handle user registration. Prevent logged-in users from accessing the registration page.
    """
    user_id = session.get('user_id')  # Check if user is logged in

    if user_id:
        # Flash a message and redirect logged-in users
            flash("You are already logged in and cannot register again.", "error")
            return redirect(url_for('public.home'))


    # Render register page or handle user registration
    logger.info("Rendering register page or handling registration form submission.")
    return render_template("Register.html")


@user_bp.route('/my_bookings', methods=['GET'])
@role_required('customer')
def view_bookings():
    # Get the logged-in user's ID from the session
    user_id = session.get('user_id')
    
    if not user_id:
        # If no user is logged in, redirect to login page or show an error
        flash('You need to log in to view your bookings.', 'error')
        return redirect(url_for('public.home'))
    
    # Use the user service to get the user's data and bookings
    user_service = UserService()
    user_data = user_service.get_user_data(user_id)  # Assign user_data here
    bookings = user_service.get_all_bookings(user_id)  # Assign bookings here
    
    # Check if user_data or bookings is missing
    if not user_data or not bookings:
        flash('We could not find your bookings or profile data. Please log in and/or book a course.', 'error')
        return redirect(url_for('public.home'))
    
    # Return template with bookings if they exist
    return render_template('MyBookings.html', bookings=bookings)


@user_bp.route('/update/<int:user_id>', methods=['POST'])
@role_required('customer')
def update_user(user_id):
    user_service = UserService()  # Initialize the UserService
    
    try:
        # Get data from the form
        form_data = request.form

        # Convert form data to a dictionary (key-value pairs)
        data = {key: value for key, value in form_data.items() if value}

        # Enforce role as 'customer'
        data['role'] = 'customer'

        # Hash the password if it's provided
        if 'password' in data:
            data['password'] = generate_password_hash(data['password'])

        # Validate that the user_id exists
        user = user_service.get_user(user_id)  # Assuming get_user(user_id) fetches a user object
        if not user:
            flash("User not found. Please try again.", "error")
            return render_template("error.html", error_message="User not found.")

        # Call the UserService to update user details
        success, message = user_service.update_user(user_id, **data)  # Use the UserService instance

        if success:
            flash("User updated successfully!", "success")
            return redirect(url_for('public.home'))
        else:
            flash(f"Failed to update user: {message}", "error")
            return render_template("user_update.html", error_message=message, user_id=user_id)

    except Exception as e:
        # Handle unexpected errors
        flash(f"An unexpected error occurred: {e}", "error")
        return render_template("error.html", error_message="An unexpected error occurred. Please try again later.")
    
    
@user_bp.route('/create', methods=['POST'])
@role_required('customer')
def create_user():
    user_service = UserService()  # Initialize the UserService

    try:
        # Get data from the form submission
        form_data = request.form

        # Convert form data to a dictionary (key-value pairs)
        data = {key: value for key, value in form_data.items() if value}

        # Enforce the role as 'customer'
        data['role'] = 'customer'

        # Validate required fields
        required_fields = ['first_name', 'second_name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Hash the password using the User model's set_password() method
        password = data['password']
        del data['password']
        
        # Call the UserService to create a new user
        success, message = user_service.create_user(**data, password=password)

        if success:
            flash(message, "success")
            return redirect(url_for('public.home'))
        else:
            flash(f"Failed to create user: {message}", "error")
            return render_template("Register.html", message=message)

    except ValueError as ve:
        flash(str(ve), "error")
        return render_template("Register.html", message=str(ve))

    except Exception as e:
        flash(f"Unexpected Error: {str(e)}", "error")
        return render_template("Register.html", message=str(e))
    



@user_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        logger.info(f"Admin logged out: {current_user.email}")
        logout_user()
        flash("You have been logged out successfully.", "success")
    return redirect(url_for('public.home'))

@user_bp.route('/book-course/<int:course_id>', methods=['POST'])
@role_required('customer')
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
@role_required('customer')
def my_courses():
    try:
        bookings = user_service.get_user_bookings(user_id)
        course_names = ", ".join([b["course_name"] for b in bookings])
        raise not_implemented

    except Exception as e:
        logger.error(f"❌ Error fetching user courses: {e}", exc_info=True)
        return "❌ Failed to retrieve your courses", 500



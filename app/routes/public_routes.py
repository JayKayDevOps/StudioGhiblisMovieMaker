from flask import Blueprint
public_bp = Blueprint('public', __name__)

@public_bp.route('/', methods=['GET'])
def home():
    print("Home Page")
    return "<h1>Home Page</h1>"

@public_bp.route('/courses')
def list_courses():
    print("List Courses")
    return "Courses List"

@public_bp.route('/courses/<int:course_id>')
def course_detail(course_id):
    print(f"Course Detail for {course_id}")
    return f"Course Detail for {course_id}"

@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    print("Login")
    return "Login Page"

@public_bp.route('/register', methods=['GET', 'POST'])
def register():
    print("Register")
    return "Register Page"
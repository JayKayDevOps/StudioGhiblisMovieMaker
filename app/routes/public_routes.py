from flask import request, redirect, url_for, render_template, flash, Blueprint
from flask_login import login_user
from app.models import User

from models import User
public_bp = Blueprint('public', __name__)

@public_bp.route('/', methods=['GET'])
def root():
   return render_template('homepage.html')

@public_bp.route('/search', methods=['GET'])
def search():
    return render_template('Search.html')
    

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
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")

            # 🔀 Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))  # adjust route name
            else:
                return redirect(url_for('user.dashboard'))

        flash("Invalid email or password", "danger")

    return render_template("login.html")
from flask_login import logout_user

@public_bp.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('public.login'))


@public_bp.route('/register', methods=['GET', 'POST'])
def register():
    print("Register")
    return "Register Page"
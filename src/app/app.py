from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import config
from models import db, User, Course, Booking

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(config["development"])  # Use "production" in live environment

# Initialize Database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect unauthorized users to login page

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --------------------------------
# ROUTES
# --------------------------------

@app.route("/")
def home():
    """Homepage showing available courses."""
    courses = Course.query.all()
    return render_template("index.html", courses=courses)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login."""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Handles user logout."""
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration route."""
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    """User dashboard showing their bookings."""
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", bookings=bookings)

@app.route("/admin")
@login_required
def admin():
    """Admin dashboard for managing courses and bookings."""
    if current_user.role != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("dashboard"))

    bookings = Booking.query.all()
    return render_template("admin.html", bookings=bookings)

@app.route("/book-course/<int:course_id>", methods=["GET", "POST"])
@login_required
def book_course(course_id):
    """Handles course booking by users."""
    course = Course.query.get_or_404(course_id)

    if request.method == "POST":
        special_requests = request.form.get("special_requests", "")

        booking = Booking(user_id=current_user.id, course_id=course_id, special_requests=special_requests)
        db.session.add(booking)
        db.session.commit()

        flash("Course booked successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("book_course.html", course=course)

# --------------------------------
# RUN THE APP
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)
